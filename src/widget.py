# Импортируем функции get_mask_card_number и get_mask_account из модуля masks.py

from masks import get_mask_card_number
from masks import get_mask_account


# Импорт модуля re
import re

def mask_account_card(account_card: str) -> str:
    """
    Принимает один аргумент — строку, содержащую тип и номер карты или счета,
     и возвращает строку с замаскированным номером.
    """

    if "Счет" in account_card:
        letters_count = "".join(re.findall(r"\D+", account_card))
        numbers_count =  "".join(re.findall(r"\d+", account_card))
        return f"{letters_count} {get_mask_account(numbers_count)}"
    else:
        letters_card = "".join(re.findall(r"\D+", account_card))
        numbers_card = "".join(re.findall(r"\d+", account_card))
        return f"{letters_card} {get_mask_card_number(numbers_card)}"


# Импорт модуля datetime
from datetime import datetime

def get_date(date: str) -> str:
    """
    Преобразует строку даты в формат "ДД.ММ.ГГГГ"
    '"""
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return date.strftime("%d.%m.%Y")

