import re
from datetime import datetime, timedelta
from re import Match

from parser.errors import ParserException
from parser.utils import check_hours, check_minutes_or_seconds, check_variants


def in_date(remind_cmd: list[str]):
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
            \D*
            (?(date)
                (?P<time>
                    (?P<hour>\d{1,2})
                    [-:.]
                    (?P<minute>\d\d)
                |\d+)?
            |
            (?:
            [^.:-](?P<only_time>
            \d\d[.:-]\d\d
            |
            \d\d
            )
            )
            )
                """, re.VERBOSE)

    # результат применения   регулярного выражения
    result = pattern.search(cmd)
    # print(result[0])
    # print(pattern.findall(cmd))

    # выбор и добавление параметров
    if result.group("date") == "завтра":
        set_date_tomorrow_or_after_tomorrow(1, result, params)
    elif result.group("date") == "послезавтра":
        set_date_tomorrow_or_after_tomorrow(2, result, params)
    elif found := check_variants(result.group("date")):
        set_date_on_day_of_week(found[1], result, params)

    if not len(params):
        raise ParserException("incorrect date")

    return params


def get_time(result: Match):
    hour = 0
    minute = 0

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


def set_date_tomorrow_or_after_tomorrow(days: int, result: Match, params: dict):
    hour, minute = get_time(result)
    now = datetime.now()
    date_for_checking = datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute)
    params["run_date"] = date_for_checking + timedelta(days=days)


def set_date_on_day_of_week(day_of_week: int, result: Match, params: dict) -> None:
    hour, minute = get_time(result)

    now = datetime.now()
    date_for_checking = datetime(year=now.year, month=now.month, day=now.day, hour=hour, minute=minute, second=0)

    if day_of_week == now.weekday():
        if now < date_for_checking - timedelta(minutes=1):
            params["run_date"] = date_for_checking
        else:
            params["run_date"] = date_for_checking + timedelta(days=7)
    else:
        add_days = day_of_week - now.weekday()
        if add_days < 0:
            add_days += 7
        params["run_date"] = date_for_checking + timedelta(days=add_days)

# print(in_date("22 f понедельник в 18.41".split(" ")))
# in_date("в 13-30".split(" "))
# in_date("завтра в 14.23".split(" "))
# in_date("18 апреля в 14".split(" "))
# in_date("послезавтра в 14".split(" "))
# in_date("16 сентября в 10-20".split(" "))
# in_date("17.04.2024 в 9-15".split(" "))


# print(in_date(" понедельник".split(" ")))
# print(in_date("d понедельник 20.36".split(" ")))
# print(in_date("d понедельник f 20.36".split(" ")))
# print(in_date("20 jd понедельник f 20.36".split(" ")))
# print(in_date("20 jd понедельник f 20".split(" ")))
# print(in_date("20 jd 12.12.24 f 20.36".split(" ")))
# print(in_date("20 ffjd 12.12.24 fff 23".split(" ")))
# print(in_date("в dfffdsdf dfffdsdf dfffdsdf 20".split(" ")))
# print(in_date("в 20".split(" ")))
# print(in_date("в 20.25".split(" ")))


print(in_date(" завтра".split(" ")))
print(in_date("завтра".split(" ")))
print(in_date("d завтра 20.36".split(" ")))
print(in_date("d завтра f 20.36".split(" ")))
print(in_date("20 jd послезавтра f 20.36".split(" ")))
print(in_date("20 jd завтра f 20".split(" ")))
