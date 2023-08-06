from abc import ABC, abstractmethod
from pydantic import BaseModel


class Connector(ABC):
    ...

    @abstractmethod
    async def close(self) -> None:
        ...

    @abstractmethod
    async def set_light_state(self, name: str, state: bool) -> None:
        ...


class Account(BaseModel, ABC):
    ...

    @abstractmethod
    def connector(self) -> Connector:
        ...
