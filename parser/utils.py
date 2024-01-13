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
def check_variants(interval: str) -> list[str, int] | None:
    interval = interval.strip().lower()
    for key, value in variants.items():
        for item in value:
            if item == interval or item + ',' == interval:
                return [key, value.index(item)]

    return None