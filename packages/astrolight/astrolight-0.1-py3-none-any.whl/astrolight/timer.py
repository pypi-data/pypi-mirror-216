from datetime import datetime, timedelta
from pydantic import BaseModel, Field

from .times import DynamicTimeExpression, Location

ONE_DAY = timedelta(days=1)


class Timer(BaseModel):
    after: DynamicTimeExpression
    until: DynamicTimeExpression
    lights: list[str] = Field(default_factory=list)

    def is_active(self, time: datetime, location: Location) -> bool:
        today = datetime(*time.timetuple()[:3])

        # Start by tracing backwards
        date = today

        while self.until.anchor(date, location) > time:
            if self.after.anchor(date, location) <= time:
                return True

            date -= ONE_DAY

        # Trace forward if neccesary
        date = today
        while self.after.anchor(date, location) <= time:
            if self.until.anchor(date, location) > time:
                return True
            date += ONE_DAY

        return False
