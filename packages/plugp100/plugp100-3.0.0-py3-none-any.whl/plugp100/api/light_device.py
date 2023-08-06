from plugp100.api.tapo_client import TapoClient, Json
from plugp100.requests.set_device_info.set_light_color_info_params import LightColorDeviceInfoParams
from plugp100.requests.set_device_info.set_light_info_params import LightDeviceInfoParams
from plugp100.responses.device_state import LightDeviceState
from plugp100.common.functional.either import Either
from plugp100.requests.set_device_info.set_plug_info_params import SetPlugInfoParams


class LightDevice:

    def __init__(self, api: TapoClient, address: str):
        self.api = api
        self.address = address

    async def login(self) -> Either[True, Exception]:
        return await self.api.login(self.address)

    async def get_state(self) -> Either[LightDeviceState, Exception]:
        return (await self.api.get_device_info()) | LightDeviceState.from_json

    async def on(self) -> Either[True, Exception]:
        return await self.api.set_device_info_with_encode(SetPlugInfoParams(True))

    async def off(self) -> Either[True, Exception]:
        return await self.api.set_device_info_with_encode(SetPlugInfoParams(False))

    async def set_brightness(self, brightness: int) -> Either[True, Exception]:
        return await self.api.set_device_info_with_encode(LightDeviceInfoParams(brightness=brightness))

    async def set_hue_saturation(self, hue: int, saturation: int) -> Either[True, Exception]:
        return await self.api.set_device_info_with_encode(LightColorDeviceInfoParams(hue=hue, saturation=saturation, color_temp=0))

    async def set_color_temperature(self, color_temperature: int) -> Either[True, Exception]:
        return await self.api.set_device_info_with_encode(LightColorDeviceInfoParams(color_temp=color_temperature))

    async def get_state_as_json(self) -> Either[Json, Exception]:
        return await self.api.get_device_info()