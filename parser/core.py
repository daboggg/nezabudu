from datetime import datetime

from parser.after import after
from parser.errors import ParserException
from parser.every import every

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




