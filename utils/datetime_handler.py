from datetime import datetime

from django.utils import timezone
from datetime import datetime, date
import calendar


def get_current_datetime():
    return timezone.now()


def str_to_datetime(data: str, dt_format: str = "%Y-%m-%d %H:%M:%S") -> datetime:
    try:
        return datetime.strptime(data, dt_format)
    except Exception as e:
        raise ValueError("올바르지 않은 기간 입니다.")


def get_first_second(dt: datetime):
    return datetime(dt.year, dt.month, dt.day, dt.hour, 00, 00)


def datetime_to_str(dt: datetime, dt_format: str = "%Y-%m-%d %H:%M:%S"):
    try:
        return datetime.strftime(dt, dt_format)
    except Exception as e:
        raise ValueError("올바르지 않은 날짜 형식입니다.")
