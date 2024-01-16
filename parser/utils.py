from parser.errors import ParserException

intervals = {
    "seconds": ["секунда", "секунды", "секунду", "секунд"],
    "minutes": ["минуту", "минуты", "минут", "минута"],
    "hours": ["час", "часа", "часов", ],
    "days": ["день", "дня", "дней", "сутки","суток",],
    "weeks": ["неделя", "недели", "недель","неделю",],
    "months": ["месяц", "месяца", "месяцев", ],
    "years": ["год", "года", "лет", ],
}

# проверка в интервалах
def check_in_intervals(interval: str) -> str | None:
    interval = interval.strip().lower()
    for key, value in intervals.items():
        for item in value:
            if item == interval or item + ',' == interval:
                return key

    return None


variants = {
    "day_of_week": ["понедельник", "вторник", "среду", "четверг", "пятницу", "субботу", "воскресенье", ],
    "month": ["", "января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября",
              "ноября", "декабря", ]
}

# проверка вариантов
def check_variants(interval: str) -> list | None:
    interval = interval.strip().lower()
    for key, value in variants.items():
        for item in value:
            if item == interval or item + ',' == interval:
                return [key, value.index(item)]

    return None

################################################################################

# проверка попадания в дипазон дней
def check_days(days: int):
    if not isinstance(days, int): raise ParserException("days should be int")
    if -1 < days < 32:
        return days
    else:
        raise ParserException("days in out of range")


# проверка попадания в дипазон минут или секунд
def check_minutes_or_seconds(min_or_sec: int):
    if not isinstance(min_or_sec, int): raise ParserException("minutes or seconds should be int")
    if -1 < min_or_sec < 60:
        return min_or_sec
    else:
        raise ParserException("minutes or seconds in out of range")


# проверка попадания в дипазон часов
def check_hours(hours: int):
    if not isinstance(hours, int): raise ParserException("hours should be int")
    if -1 < hours < 24:
        return hours
    else:
        raise ParserException("hours in out of range")