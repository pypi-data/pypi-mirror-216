import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from pydantic import BaseModel, Field
from typing import Any


class Location(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class DynamicTime(ABC):
    ...

    @abstractmethod
    def anchor(self, time: datetime, location: Location) -> datetime:
        ...


class OffsetTime(DynamicTime):
    def __init__(self, duration: str):
        match = re.match(r"^([0-9]+)\:([0-9]{2})$", duration)

        if match is None:
            raise ValueError(f"{duration} is not a valid duration format.")

        self._offset = timedelta(
            hours=int(match.group(1)),
            minutes=int(match.group(2)),
        )

    def __eq__(self, o: Any) -> bool:
        if isinstance(o, OffsetTime):
            return self._offset == o._offset

        return NotImplemented

    def anchor(self, time: datetime, location: Location) -> datetime:
        return time + self._offset
