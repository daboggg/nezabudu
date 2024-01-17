import re
from datetime import datetime, timedelta
from re import Match

from parser.errors import ParserException
from parser.utils import check_hours, check_minutes_or_seconds, check_variants


def in_date(remind_cmd: list[str]) -> dict[str, datetime]:
    # итоговый словарь с параметрами
    params = dict()
    cmd = ' '.join(remind_cmd)

    # регулярное выражение для поиска
    # pattern = re.compile("""
    # (?P<num>\d+)*
    # \s*
    # (?P<date>[а-я]{3,}|\d\d[.:-]\d\d[.:-]\d{2,4})?
    # \D*
    # (?P<time>
    #     (?P<hour>\d{1,2})
    #     [-:.]
    #     (?P<minute>\d\d)
    # |\d+)?
    #     """, re.VERBOSE)

    #  pattern = re.compile("""
    #  (?P<num>\d+)*
    #  \W*
    #  (?P<q>(?P<date>[а-я]{3,}|\d\d[.:-]\d\d[.:-]\d{2,4}))?
    #  \D*
    #  (?(q)
    #  (?P<time>
    #      (?P<hour>\d{1,2})
    #      [-:.]
    #      (?P<minute>\d\d)
    #  |\d+)?
    #  |
    #  (?P<only_time>
    # [^.:-]\d\d[.:-]\d\d
    #  )
    #  )
    #      """, re.VERBOSE)

    # pattern = re.compile("""
    #     (?P<num>\d+)*
    #     (?:\w*\s*)
    #     (?P<date>[а-я]{3,}|\d\d[.:-]\d\d[.:-]\d{2,4})?
    #     \D*
    #     (?(date)
    #         (?P<time>
    #             (?P<hour>\d{1,2})
    #             [-:.]
    #             (?P<minute>\d\d)
    #         |\d+)?
    #     |
    #     [^.:-](?P<only_time>
    #     \d\d[.:-]\d\d
    #     )
    #     )
    #         """, re.VERBOSE)

    # pattern = re.compile("""
    #     (?P<num>\d+)*
    #     \s*
    #     (?P<date>[а-я]{3,}|\d\d[.:-]\d\d[.:-]\d{2,4})?
    #     \D*
    #     (?(date)
    #         (?P<time>
    #             (?P<hour>\d{1,2})
    #             [-:.]
    #             (?P<minute>\d\d)
    #         |\d+)?
    #     |
    #     [^.:-](?P<only_time>
    #     \d\d[.:-]\d\d
    #     )
    #     )
    #         """, re.VERBOSE)

    pattern = re.compile("""
            (?P<num>\d+)?
            (?(num)\s*)
            (?:\w*\s)?
            (?P<date>[а-я]{3,}|\d\d[.:-]\d\d[.:-]\d{2,4})?
            (?(date)\s*)
            (?:\w*\s)?
            (?(date)
                (?P<time>
                    (?P<hour>\d{1,2})
                    [-:.]
                    (?P<minute>\d\d)
                |\d+)?
            |
            [^.:-](?P<only_time>
            \d\d[.:-]\d\d
            |
            \d\d
            )
            )
                """, re.VERBOSE)

    # результат применения   регулярного выражения
    result = pattern.search(cmd)
    # print(result[0])
    print(pattern.findall(cmd))

    # выбор и добавление параметров
    if result.group("date") == "завтра":
        set_date_tomorrow_or_after_tomorrow(1, result, params)
    elif result.group("date") == "послезавтра":
        set_date_tomorrow_or_after_tomorrow(2, result, params)
    elif re.search(r"\d\d[.:-]\d\d[.:-]\d\d\d?\d?", result.group("date")):
        day, month, year = re.split(r":|-|\.", result.group("date"))
        set_date(int(year), int(month), int(day), result, params)
    elif result.group("date") and (found := check_variants(result.group("date"))):
        set_date_on_month_or_day_of_week(found[1], result, params, found[0])

    if not len(params):
        raise ParserException("incorrect date")

    return params


# установка времени
def get_time(result: Match):
    if not result.group("time"):
        hour = 8
        minute = 0
    elif result.group("time").isdigit():
        hour = check_hours(int(result.group("time")))
        minute = 0
    else:
        hour = check_hours(int(result.group("hour")))
        minute = check_minutes_or_seconds(int(result.group("minute")))
    return [hour, minute]


# установка даты (dd:mm:YYYY)
def set_date(year: int, month: int, day: int, result: Match, params: dict):
    if year < 100: year = year + 2000
    hour, minute = get_time(result)
    now = datetime.now()
    date_for_checking = datetime(year=year, month=month, day=day, hour=hour, minute=minute)

    if now < date_for_checking:
        params["run_date"] = date_for_checking
    else:
        raise ParserException("the date is earlier than the current one")


# установка даты (завтра, послезавтра)
def set_date_tomorrow_or_after_tomorrow(days: int, result: Match, params: dict):
    hour, minute = get_time(result)
    now = datetime.now()
    date_for_checking = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    params["run_date"] = date_for_checking + timedelta(days=days)


# установка даты (понедельник вторник и тд)
def set_date_on_month_or_day_of_week(numb: int, result: Match, params: dict, period: str) -> None:
    hour, minute = get_time(result)

    now = datetime.now()

    if period == "day_of_week":
        date_for_checking = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
        if numb == now.weekday():
            if now < date_for_checking - timedelta(minutes=1):
                params["run_date"] = date_for_checking
            else:
                params["run_date"] = date_for_checking + timedelta(days=7)
        else:
            add_days = numb - now.weekday()
            if add_days < 0:
                add_days += 7
            params["run_date"] = date_for_checking + timedelta(days=add_days)
    elif period == "month" and result.group("num"):
        day_of_month = int(result.group("num"))
        date_for_checking = datetime(year=now.year, month=numb, day=day_of_month, hour=hour, minute=minute)
        if now > date_for_checking:
            params["run_date"] = date_for_checking.replace(year=now.year + 1)
        else:
            params["run_date"] = date_for_checking


# print(in_date("22 f понедельник в 18.41".split(" ")))    ###
# in_date("завтра в 14.23".split(" "))                     ###
# in_date("послезавтра в 14".split(" "))                    ###
# in_date("18 апреля в 14".split(" ")) #                    ###
# in_date("16 сентября в 10-20".split(" "))                 ###
# in_date("17.04.2024 в 9-15".split(" "))                   ###
# in_date("в 13-30".split(" "))


print(in_date("17 февраля в 02.32".split(" ")))
print(in_date("17 во марта в 02.32".split(" ")))
print(in_date(" понедельник".split(" ")))
print(in_date("d понедельник 20.36".split(" ")))
print(in_date("d понедельник f 20.36".split(" ")))
print(in_date("20  среду f 14.26".split(" ")))
print(in_date("20 jd понедельник f 20".split(" ")))
print(in_date("20 jd 12.12.26 f 20.36".split(" ")))
print(in_date("20 ffjd 12.12.24 fff 23".split(" ")))
print(in_date("12.12.24 fff 07".split(" ")))
print(in_date("d 12.12.24 df".split(" ")))
# print(in_date("в dfffdsdf dfffdsdf dfffdsdf 20".split(" ")))
# print(in_date("в 20".split(" ")))
# print(in_date("в 07".split(" ")))
# print(in_date("в 20.25".split(" ")))


print(in_date(" завтра".split(" ")))
print(in_date("завтра".split(" ")))
print(in_date("завтра в 2.11".split(" ")))
print(in_date("d завтра 20.36".split(" ")))
print(in_date("d завтра f 20.36".split(" ")))
print(in_date("20 jd послезавтра f 20.36".split(" ")))
print(in_date("20 jd завтра f 20".split(" ")))
