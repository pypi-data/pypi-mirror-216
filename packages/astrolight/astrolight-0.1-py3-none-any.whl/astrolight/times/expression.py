import logging
import re
from datetime import datetime, timedelta
from itertools import pairwise
from pydantic import BaseModel
from typing import Any, Literal, Type, TypeVar, Union

from .dynamic_time import DynamicTime, Location, OffsetTime
from .sun_time import SunriseTime, SunsetTime

ONE_DAY = timedelta(days=1)

CUSTOM_DYNAMIC_TIMES = {
    "SUNRISE": SunriseTime(),
    "SUNSET": SunsetTime(),
}

DynamicTimeExpressionType = TypeVar("DynamicTimeExpressionType", bound="DynamicTimeExpression")


class DynamicTimeExpression(BaseModel):
    expr: list[tuple[Literal["+", "-"], DynamicTime]]

    class Config:
        arbitrary_types_allowed = True

    def anchor(self, time: datetime, location: Location) -> datetime:

        t = time
        for sign, dynamic_time in self.expr:
            dt = dynamic_time.anchor(time, location) - time

            if sign == "+":
                t += dt
            elif sign == "-":
                t -= dt
            else:
                raise ValueError()

        return t

    # ------------------------ #
    # Alternative Constructors #
    # ------------------------ #

    @classmethod
    def from_string(
        cls: Type[DynamicTimeExpressionType],
        string: str,
    ) -> DynamicTimeExpressionType:
        splitz = ["+"] + [s.strip() for s in re.split(r"(\+|\-)", string)]
        logging.debug(f"Splitting {string} => {splitz}")
        terms = [*pairwise(splitz)][::2]

        expr = []
        for sign, term in terms:
            if term in CUSTOM_DYNAMIC_TIMES:
                dynamic_time = CUSTOM_DYNAMIC_TIMES[term]  # type: ignore
            else:
                dynamic_time = OffsetTime(term)

            expr.append((sign, dynamic_time))

        return cls(expr=expr)  # type: ignore

    # ------------------- #
    # Pydantic Validators #
    # ------------------- #

    @classmethod
    def __get_validators__(cls):  # type: ignore
        yield cls.convert_from_string
        yield cls.validate

    @classmethod
    def convert_from_string(
        cls: Type[DynamicTimeExpressionType],
        v: Any,
    ) -> Union[DynamicTimeExpressionType, Any]:
        if isinstance(v, str):
            return cls.from_string(v)

        return v

    @classmethod
    def validate(
        cls: Type[DynamicTimeExpressionType],
        v: Any,
    ) -> DynamicTimeExpressionType:
        if isinstance(v, cls):
            return v

        raise TypeError()
