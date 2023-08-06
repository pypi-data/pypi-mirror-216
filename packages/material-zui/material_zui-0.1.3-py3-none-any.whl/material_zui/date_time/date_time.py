from datetime import datetime, timedelta


def now() -> datetime: return datetime.now()


def add_days(date: datetime, days: int) -> datetime:
    diff = timedelta(days=days)
    return date + diff


def to_date(date: str) -> datetime:
    return datetime.strptime(date, "%Y-%m-%d")


def to_date_str(date_time: datetime) -> str:
    return datetime.strftime(date_time, "%Y-%m-%d")


def to_date_time(date_time: str) -> datetime:
    return datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S")
