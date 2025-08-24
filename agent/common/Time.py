from datetime import datetime, timedelta


# 是不是金戈时间
def is_battle_time() -> bool:
    current_time = datetime.now().time()

    start_time1 = datetime.strptime("11:00", "%H:%M").time()
    end_time1 = datetime.strptime("14:00", "%H:%M").time()

    start_time2 = datetime.strptime("19:00", "%H:%M").time()
    end_time2 = datetime.strptime("22:00", "%H:%M").time()

    return (start_time1 <= current_time <= end_time1) or (start_time2 <= current_time <= end_time2)


def is_tao_yuan_time() -> int:
    current_time = datetime.now().time()

    start_time1 = datetime.strptime("11:00", "%H:%M").time()
    end_time1 = datetime.strptime("15:00", "%H:%M").time()

    start_time2 = datetime.strptime("17:00", "%H:%M").time()
    end_time2 = datetime.strptime("22:00", "%H:%M").time()

    start_time3 = datetime.strptime("00:00", "%H:%M").time()
    end_time3 = datetime.strptime("05:00", "%H:%M").time()

    if start_time3 <= current_time <= end_time3:
        return 3
    if current_time < start_time1:
        return 0
    elif start_time1 <= current_time <= end_time1:
        return 1
    elif end_time1 <= current_time <= start_time2:
        return 2
    elif start_time2 <= current_time <= end_time2:
        return 3
    else:
        return -1


REFRESH_HOUR = 5


def _adjust_datetime(arg_date: datetime, refresh_hour: int = REFRESH_HOUR) -> datetime:
    """
        根据刷新时间调整日期
        如果当前时间小于刷新时间，则认为是前一天
        """
    if arg_date.hour < refresh_hour:
        return arg_date - timedelta(days=1)
    return arg_date


def is_same_day_with_today(date_str: str) -> bool:
    if date_str is None:
        return False
    time_format = "%Y-%m-%d %H:%M:%S"
    given_time = _adjust_datetime(datetime.strptime(date_str, time_format))
    today = _adjust_datetime(datetime.now())

    return today.date() == given_time.date()


# 判断是否在同一个月
def is_same_month_with_today(date_str: str) -> bool:
    if date_str is None:
        return False
    time_format = "%Y-%m-%d %H:%M:%S"
    given_time = _adjust_datetime(datetime.strptime(date_str, time_format))
    today = _adjust_datetime(datetime.now())

    return today.year == given_time.year and today.month == given_time.month


# 判断是否在同一周
def is_same_week_with_today(date_str: str) -> bool:
    if date_str is None:
        return False
    time_format = "%Y-%m-%d %H:%M:%S"
    given_time = _adjust_datetime(datetime.strptime(date_str, time_format))
    today = _adjust_datetime(datetime.now())

    y1, w1, _ = given_time.isocalendar()
    y2, w2, _ = today.isocalendar()
    return (y1 == y2) and (w1 == w2)
