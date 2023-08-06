from ewelink import EWeLink
from ewelink.types import AppCredentials, EmailUserCredentials
from typing import Literal

from .account_connector import Account, Connector


class EWeLinkAccount(Account):
    type: Literal["eWeLink"]
    app: AppCredentials
    user: EmailUserCredentials

    def connector(self) -> Connector:
        return EWeLinkConnector(self)


class EWeLinkConnector(Connector):
    def __init__(self, account: EWeLinkAccount) -> None:
        self._ewelink = EWeLink(app_cred=account.app, user_cred=account.user)

    async def close(self) -> None:
        await self._ewelink.close()

    async def set_light_state(self, name: str, state: bool) -> None:
        devices = await self._ewelink.get_thing_list()

        for device in devices:
            if device.name == name:
                params = {"switch": "on" if state else "off"}
                await self._ewelink.update_thing_status(device, params)
