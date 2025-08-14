from datetime import datetime, timedelta


def is_battle_time() -> bool:
    # 获取当前时间
    current_time = datetime.now().time()

    # 定义时间区间
    start_time1 = datetime.strptime("11:00", "%H:%M").time()
    end_time1 = datetime.strptime("14:00", "%H:%M").time()

    start_time2 = datetime.strptime("19:00", "%H:%M").time()
    end_time2 = datetime.strptime("22:00", "%H:%M").time()

    # 判断当前时间是否在指定区间内
    return (start_time1 <= current_time <= end_time1) or (start_time2 <= current_time <= end_time2)


# 判断是否在同一天（已给出）
def is_same_day_with_offset(date_str: str, offset_hour=5) -> bool:
    time_format = "%Y-%m-%d %H:%M:%S"
    given_time = datetime.strptime(date_str, time_format)
    now = datetime.now()

    today_start = now.replace(hour=offset_hour, minute=0, second=0, microsecond=0)
    if now < today_start:
        today_start -= timedelta(days=1)

    return today_start.date() == given_time.date()


# 判断是否在同一个月
def is_same_month_with_offset(date_str: str, offset_hour=5) -> bool:
    time_format = "%Y-%m-%d %H:%M:%S"
    given_time = datetime.strptime(date_str, time_format)
    now = datetime.now()

    current_month_start = now.replace(hour=offset_hour, minute=0, second=0, microsecond=0, day=1)
    if now < current_month_start:
        current_month_start -= timedelta(days=1)

    return current_month_start.year == given_time.year and current_month_start.month == given_time.month


# 判断是否在同一周
def is_same_week_with_offset(date_str: str, offset_hour=5) -> bool:
    time_format = "%Y-%m-%d %H:%M:%S"
    given_time = datetime.strptime(date_str, time_format)
    now = datetime.now()

    current_week_start = now.replace(hour=offset_hour, minute=0, second=0, microsecond=0)
    current_week_start -= timedelta(days=current_week_start.weekday())  # 调整到周一
    if now < current_week_start:
        current_week_start -= timedelta(weeks=1)

    return current_week_start.isocalendar()[1] == given_time.isocalendar()[1] and \
        current_week_start.year == given_time.year
