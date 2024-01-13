import re

from parser.errors import ParserException
from parser.utils import check_variants


# обработка команд начиноющихся на "каждый", "каждое" и т.д
def every(remind_cmd: list[str]):
    # итоговый словарь с параметрами
    params = dict()
    cmd = ' '.join(remind_cmd)

    # регулярное выражение для поиска
    pattern = re.compile("""
    (?P<num>\d+)*
    \s*
    (?P<date>[а-я]{3,})
    \D*
    (?P<time>
        (?P<hour>\d{1,2})
        [-:.]
        (?P<minute>\d\d)
    |\d+)?
    """, re.VERBOSE)

    # результат регулярного выражения
    result = pattern.search(cmd)

    # выбор и добавление параметров
    if result.group("date") == "день":
        set_time(params, result)
    elif result.group("date") in ["число", "числа"]:
        set_day(params, result)
        set_time(params, result)
    elif found := check_variants(result.group("date")):
        params[found[0]] = found[1]
        set_time(params, result)

    if not len(params):
        raise ParserException("incorrect date")

    return params


# установить параметы дня
def set_day(params, result):
    if result.group("num"):
        params["day"] = check_days(int(result.group("num")))


# установить параметы времени
def set_time(params, result):
    if not result.group("time"):
        params["hour"] = 8
        # params["minute"] = 0
    elif result.group("time").isdigit():
        params["hour"] = check_hours(int(result.group("time")))
    else:
        params['hour'] = check_hours(int(result.group("hour")))
        params['minute'] = check_minutes_or_seconds(int(result.group("minute")))


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


# print(every("день в 8:44".split(" ")))
# print(every("пятницу в 23.02".split(" ")))
# print(every("22 число в 13".split(" ")))
# print(every("28 сентября 10".split(" ")))
# every("30 мая".split(" "))
