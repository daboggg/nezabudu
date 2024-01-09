import moment

from perser.errors import ParserException
from perser.utils import intervals


def check_in_intervals(interval: str) -> str | None:
    interval = interval.strip().lower()
    for key, value in intervals.items():
        for item in value:
            if item == interval or item + ',' == interval:
                return key

    return None


def after(remind_cmd: list[str]):
    arg = dict()
    result = dict()

    for idx, item in enumerate(remind_cmd):
        if interval := check_in_intervals(item):
            if idx > 0 and (val := remind_cmd[idx - 1]).isdigit():
                arg[interval] = int(val)
            else:
                arg[interval] = 1

    if not arg:
        raise ParserException(f"remind cmd is wrong")

    result["date"] = moment.now().add(**arg).date

    return result
