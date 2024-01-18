from datetime import datetime

from parser.after import after
from parser.errors import ParserException
from parser.every import every
from parser.in_date import in_date


# выбирает как обрабатывать remind
def start_formatter(remind_cmd: list[str]):
    if remind_cmd[0] == "через":
        result = after(remind_cmd[1:])
        result["trigger"] = "date"
        return  result
    elif  remind_cmd[0] in ["каждый","каждую","каждое",]:
        result = every(remind_cmd[1:])
        result["trigger"] = "cron"
        return result
    else:
        result = in_date(remind_cmd)
        result["trigger"] = "date"
        return result

def remind_formatter(remind_tmp: str):
    remind_tmp = remind_tmp.split("@")
    remind_cmd = [item.strip().lower() for item in remind_tmp[0].split(' ') if item]
    remind_msg = "@".join(remind_tmp[1:]).strip()

    if len(remind_cmd) < 2:
        raise ParserException(f"remind is wrong: the length must be at least two arguments")
    if not remind_msg:
        raise ParserException(f"remind is wrong: the message is missing")

    result = start_formatter(remind_cmd)
    return {"args": result, "msg": remind_msg}

if __name__ == '__main__':
    # remind = "через 1 год 1 месяц 1 день 1 час 1 минуту 1 секунду@ dffgg"
    # remind = "через 3 минуты@]что то где то"
    # remind = "через 1 месяц и 1 день и 1 минуту@ надо купить билет"
    # remind = "   ЧереЗ   l  год @ Lkdjj @ lkdf Df@kjh"
    # remind = "Каждый денЬ@     d"
    remind = "Каждый СрЕду в 20.32 @ блядство разное @@ aflfk "
    print(remind_formatter(remind))
    print(remind_formatter("17 февраля в 3 @ тру ля ля"))
    print(remind_formatter("через 2 часа @ dlfkj"))

    # print(in_date("17 февраля в 3".split(" ")))
    # print(in_date("17 февраля в 02.32".split(" ")))
    # print(in_date("17 во марта в 02.32".split(" ")))
    # print(in_date(" понедельник".split(" ")))
    # print(in_date("d понедельник 20.36".split(" ")))
    # print(in_date("d понедельник f 20.36".split(" ")))
    # print(in_date("20  среду f 14.26".split(" ")))
    # print(in_date("20 jd понедельник f 20".split(" ")))
    # print(in_date("20 jd 12.12.26 f 20.36".split(" ")))
    # print(in_date("20 ffjd 12.12.24 fff 23".split(" ")))
    # print(in_date("12.12.24 fff 07".split(" ")))
    # print(in_date("d 12.12.24 df".split(" ")))
    # print(in_date("в dfffdsdf dfffdsdf dfffdsdf 20".split(" ")))
    # print(in_date("в 20".split(" ")))
    # print(in_date("в 7".split(" ")))
    # print(in_date("в 13".split(" ")))
    #
    # print(in_date(" завтра".split(" ")))
    # print(in_date("завтра".split(" ")))
    # print(in_date("завтра в 2.11".split(" ")))
    # print(in_date("d завтра 20.36".split(" ")))
    # print(in_date("d завтра f 20.36".split(" ")))
    # print(in_date("20 jd послезавтра f 20.36".split(" ")))
    # print(in_date("20 jd завтра f 20".split(" ")))




