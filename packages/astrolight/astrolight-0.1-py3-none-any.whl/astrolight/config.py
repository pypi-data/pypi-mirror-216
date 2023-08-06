from pydantic import BaseModel

from .ewelink_connector import EWeLinkAccount
from .timer import Timer
from .times import Location

# AccountType = Union[EWeLinkAccount]
AccountType = EWeLinkAccount


class Config(BaseModel):
    location: Location
    accounts: list[AccountType]
    on: list[Timer]
