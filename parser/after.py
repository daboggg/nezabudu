import moment

from parser.errors import ParserException
from parser.utils import check_in_intervals


# обработка команд начиноющихся на "через"
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

    result["run_date"] = moment.now().add(**arg).date

    return result
