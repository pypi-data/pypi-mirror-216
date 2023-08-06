from plugp100.api.tapo_client import TapoClient, Json
from plugp100.responses.device_state import PlugDeviceState
from plugp100.common.functional.either import Either
from plugp100.requests.set_device_info.set_plug_info_params import SetPlugInfoParams
from plugp100.responses.energy_info import EnergyInfo
from plugp100.responses.power_info import PowerInfo


class PlugDevice:

    def __init__(self, api: TapoClient, address: str):
        self.api = api
        self.address = address

    async def login(self) -> Either[True, Exception]:
        return await self.api.login(self.address)

    async def get_state(self) -> Either[PlugDeviceState, Exception]:
        return (await self.api.get_device_info()) | PlugDeviceState.from_json

    async def on(self) -> Either[True, Exception]:
        return await self.api.set_device_info_with_encode(SetPlugInfoParams(True))

    async def off(self) -> Either[True, Exception]:
        return await self.api.set_device_info_with_encode(SetPlugInfoParams(False))

    async def get_energy_usage(self) -> Either[EnergyInfo, Exception]:
        return await self.api.get_energy_usage()

    async def get_current_power(self) -> Either[PowerInfo, Exception]:
        return await self.api.get_current_power()

    async def get_state_as_json(self) -> Either[Json, Exception]:
        return await self.api.get_device_info()