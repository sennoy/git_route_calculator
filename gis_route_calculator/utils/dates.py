import copy
import datetime
from dataclasses import dataclass


@dataclass
class DateTimeRange:
    left: datetime.datetime
    right: datetime.datetime


def datetime_range_for_day(dt: datetime.datetime):
    left = copy.deepcopy(dt)
    left = left.replace(hour=0, minute=0, second=0, microsecond=0)
    right = left + datetime.timedelta(days=1)
    return DateTimeRange(
        left=left,
        right=right
    )
