import re
from masks import get_mask_card_number
from masks import get_mask_account
from datetime import datetime



def mask_account_card(account_card: str) -> str:
    if account_card is None:
        return ""
    account_card = str(account_card)
    # Улучшенное распознавание счёта (игнорируем регистр)
    is_account = "счет" in account_card.lower()
    letters = "".join(re.findall(r"[А-Яа-яA-Za-z\s]+", account_card)).strip()
    numbers = "".join(re.findall(r"\d+", account_card))
    if not numbers:
        return letters  # или вернуть только буквы
    if is_account:
        return f"{letters} {get_mask_account(numbers)}"
    else:
        return f"{letters} {get_mask_card_number(numbers)}"




def get_date(date: str) -> str:
    """
    Преобразует строку даты в формат "ДД.ММ.ГГГГ"
    '"""
    date = datetime.strptime(date, "%Y-%m-%dT%H:%M:%S.%f")
    return date.strftime("%d.%m.%Y")

