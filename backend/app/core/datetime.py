"""Module related to datetime."""

from datetime import date, datetime, time
from typing import NewType, TypeVar, cast

import pytz

NaiveDatetime = NewType("NaiveDatetime", datetime)  # non-aware datetime
AwareDatetime = NewType("AwareDatetime", datetime)  # timezone aware datetime
DatetimeLike = TypeVar("DatetimeLike", NaiveDatetime, AwareDatetime)

TIMEZONE = "Europe/London"
tz = pytz.timezone(TIMEZONE)


def utc_now() -> AwareDatetime:
    """Return UTC datetime."""
    return cast(AwareDatetime, datetime.now(tz=pytz.UTC))


def now() -> AwareDatetime:
    """Return London datetime."""
    return cast(AwareDatetime, datetime.now(tz=pytz.timezone(TIMEZONE)))


def today() -> date:
    """Return London date."""
    return now().date()


def datetime_localize(tzname: str, dt: datetime) -> AwareDatetime:
    """Correct way to add timezone to an unaware datetime."""
    if dt.tzinfo is not None:
        raise Exception("Datetime should be timezone-unaware.")
    return cast(AwareDatetime, pytz.timezone(tzname).localize(dt))


def combine(dt: date, t: time) -> AwareDatetime:
    """Combine a date with a time, then localize to the London timezone."""
    return localize(datetime.combine(dt, t))


def localize(dt: datetime) -> AwareDatetime:
    """Localize a datetime to London timezone."""
    return datetime_localize(TIMEZONE, dt)
