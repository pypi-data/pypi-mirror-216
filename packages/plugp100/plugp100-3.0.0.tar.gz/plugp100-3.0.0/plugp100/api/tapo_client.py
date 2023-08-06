import logging
from dataclasses import dataclass
from time import time
from typing import Optional, Any

import aiohttp
import jsons

from plugp100.api.light_effect import LightEffect
from plugp100.common.functional.either import Either, Right
from plugp100.common.utils.http_client import AsyncHttp
from plugp100.common.utils.json_utils import dataclass_encode_json
from plugp100.requests.handshake_params import HandshakeParams
from plugp100.requests.login_device import LoginDeviceParams
from plugp100.requests.secure_passthrough_params import SecurePassthroughParams
from plugp100.requests.tapo_request import TapoRequest
from plugp100.responses.child_device_list import ChildDeviceList
from plugp100.responses.energy_info import EnergyInfo
from plugp100.responses.power_info import PowerInfo
from plugp100.responses.tapo_response import TapoResponse
from plugp100.encryption.key_pair import KeyPair
from plugp100.encryption.tp_link_cipher import TpLinkCipher, TpLinkCipherCryptography


logger = logging.getLogger(__name__)

Json = dict[str, Any]


@dataclass
class Session:
    url: str
    key_pair: KeyPair
    chiper: TpLinkCipher
    cookie_token: Optional[str]
    token: Optional[str]


class TapoClient:
    TERMINAL_UUID = "88-00-DE-AD-52-E1"

    def __init__(
            self,
            username: str,
            password: str,
            http_session: Optional[aiohttp.ClientSession] = None,
    ):
        self.username = username
        self.password = password
        self.http = AsyncHttp(aiohttp.ClientSession() if http_session is None else http_session)
        self.session = None

    async def login(self, url: str) -> Either[True, Exception]:
        handshake = await self._handshake(url)
        if isinstance(handshake, Right):
            token_or_error = await self._login_request(self.username, self.password)
            self.session.token = token_or_error.value if isinstance(token_or_error, Right) else None
            return token_or_error.map(lambda _: True)

        return handshake

    async def get_device_info(self) -> Either[Json, Exception]:
        get_info_request = TapoRequest.get_device_info()
        return (await self._execute_with_passthrough(get_info_request, require_token=True)) \
            .map(lambda x: x.result)

    async def get_device_usage(self) -> Either[Json, Exception]:
        get_usage_request = TapoRequest.get_device_usage()
        response = await self._execute_with_passthrough(get_usage_request, require_token=True)
        return response.map(lambda x: x.result)

    async def get_energy_usage(self) -> Either[EnergyInfo, Exception]:
        get_energy_request = TapoRequest.get_energy_usage()
        response = await self._execute_with_passthrough(get_energy_request, require_token=True)
        return response.map(lambda x: EnergyInfo(x.result))

    async def get_current_power(self) -> Either[PowerInfo, Exception]:
        get_current_power = TapoRequest.get_current_power()
        response = await self._execute_with_passthrough(get_current_power, require_token=True)
        return response.map(lambda x: PowerInfo(x.result))

    async def set_device_info(self, device_info: Json) -> Either[True, Exception]:
        request = TapoRequest.set_device_info(device_info) \
            .with_terminal_uuid(self.TERMINAL_UUID) \
            .with_request_time_milis(time())
        response = await self._execute_with_passthrough(request, require_token=True)
        return response.map(lambda _: True)

    async def set_device_info_with_encode(self, device_info) -> Either[True, Exception]:
        return await self.set_device_info(dataclass_encode_json(device_info))

    async def set_lighting_effect(self, light_effect: LightEffect) -> Either[True, Exception]:
        request = TapoRequest.set_lighting_effect(light_effect)\
            .with_terminal_uuid(self.TERMINAL_UUID)\
            .with_request_time_milis(time())
        response = await self._execute_with_passthrough(request, require_token=True)
        return response.map(lambda _: True)

    async def get_child_device_list(self) -> Either[ChildDeviceList, Exception]:
        request = TapoRequest.get_child_device_list() \
            .with_terminal_uuid(self.TERMINAL_UUID) \
            .with_request_time_milis(time())
        response = await self._execute_with_passthrough(request, require_token=True)
        return response.map(lambda x: ChildDeviceList.from_json(**x.result))

    async def get_child_device_component_list(self) -> Either[Json, Exception]:
        request = TapoRequest.get_child_device_component_list() \
            .with_terminal_uuid(self.TERMINAL_UUID) \
            .with_request_time_milis(time())
        response = await self._execute_with_passthrough(request, require_token=True)
        return response.map(lambda x: x.result)

    async def _login_request(self, username: str, password: str) -> Either[str, Exception]:
        login_device_params = LoginDeviceParams(username, password)
        login_request = TapoRequest.login(login_device_params) \
            .with_request_time_milis(time())
        response_as_dict = await self._execute_with_passthrough(login_request)
        return response_as_dict.map(lambda x: x.result['token'])

    async def _handshake(self, url: str) -> Either[True, Exception]:
        logger.debug("Will perform handshaking...")
        logger.debug("Generating keypair")

        url = f"http://{url}/app"
        key_pair = KeyPair.create_key_pair()

        handshake_params = HandshakeParams(key_pair.get_public_key())
        logger.debug(f"Handshake params: {jsons.dumps(handshake_params)}")

        request = TapoRequest.handshake(handshake_params)
        request_body = jsons.loads(jsons.dumps(request))
        logger.debug(f"Request {request_body}")

        response = await self.http.async_make_post(url, json=request_body)
        resp_dict = await response.json(content_type=None)
        logger.debug(f"Device responded with: {resp_dict}")
        response_or_error = TapoResponse.from_json(resp_dict).validate().map(lambda _: True)

        if isinstance(response_or_error, Right):
            cookie_token = response.cookies.get('TP_SESSIONID').value
            logger.debug(f"Got TP_SESSIONID token: ...{cookie_token[5:]}")

            logger.debug("Decoding handshake key...")
            handshake_key = resp_dict['result']['key']
            tp_link_cipher = TpLinkCipherCryptography.create_from_keypair(handshake_key, key_pair)

            self.session = Session(url, key_pair, tp_link_cipher, cookie_token, token=None)
            return Right(True)
        else:
            return response_or_error

    async def _execute_with_passthrough(
            self,
            request: TapoRequest,
            require_token: bool = False
    ) -> Either[TapoResponse[Json], Exception]:
        encrypted_request = self.session.chiper.encrypt(jsons.dumps(request))
        passthrough_request = TapoRequest.secure_passthrough(SecurePassthroughParams(encrypted_request))
        request_body = jsons.loads(jsons.dumps(passthrough_request))

        logger.debug(f"Request body: {request_body}")

        response_encrypted = await self.http.async_make_post_cookie(
            self.session.url if not require_token else f"{self.session.url}?token={self.session.token}",
            request_body,
            {'TP_SESSIONID': self.session.cookie_token}
        )
        response_as_dict: dict = await response_encrypted.json(content_type=None)
        logger.debug(f"Device responded with: {response_as_dict}")

        return TapoResponse.from_json(response_as_dict) \
            .validate() \
            .map(lambda response: jsons.loads(self.session.chiper.decrypt(response.result['response']))) \
            .bind(lambda decrypted_response: TapoResponse.from_json(decrypted_response).validate())
