from datetime import datetime

from perser.after import after
from perser.errors import ParserException


def starts_digits(remind: list[str]):
    print("digit")


def starts_alpha(remind_cmd: list[str]):
    if remind_cmd[0] == "через":
        return  after(remind_cmd[1:])

def start(remind: str):
    remind = remind.split("@")
    remind_cmd = [item.strip().lower() for item in remind[0].split(' ') if item]
    remind_msg = "@".join(remind[1:]).strip()

    if len(remind_cmd) < 2:
        raise ParserException(f"remind is wrong: the length must be at least two arguments")
    if not remind_msg:
        raise ParserException(f"remind is wrong: the message is missing")

    if remind_cmd[0].isdigit():
        starts_digits(remind_cmd)
    else:
        result = starts_alpha(remind_cmd)
        result["msg"] = remind_msg
        return result

if __name__ == '__main__':
    # remind = "через 1 год 1 месяц 1 день 1 час 1 минуту 1 секунду@"
    # remind = "через 1 месяц и 1 день и 1 минуту@ надо купить билет"
    remind = "Через неделю@ надо купить косилку"
    # remind = "   ЧереЗ   l  год @ Lkdjj @ lkdf Df@kjh"
    print(datetime.now())
    print(start(remind))



