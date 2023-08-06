from datetime import datetime
from suntime import Sun

from .dynamic_time import DynamicTime, Location


class SunriseTime(DynamicTime):
    def anchor(self, time: datetime, location: Location) -> datetime:
        sunrise = (
            Sun(location.latitude, location.longitude)
            .get_sunrise_time(time)
            .astimezone(time.tzinfo)
        )

        if time.tzinfo is None:
            sunrise = sunrise.replace(tzinfo=None)

        return sunrise


class SunsetTime(DynamicTime):
    def anchor(self, time: datetime, location: Location) -> datetime:
        sunset = (
            Sun(location.latitude, location.longitude).get_sunset_time(time).astimezone(time.tzinfo)
        )

        if time.tzinfo is None:
            sunset = sunset.replace(tzinfo=None)

        return sunset
