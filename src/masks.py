def get_mask_account(account):
    """
    Функция маскировки банковского счета
    """
    account = str(account)
    mask = "**"
    part = account[-4:]
    return mask + part


def get_mask_card_number(card_number: str) -> str:
    """
    Принимает номер карты и возвращает его маску
    """
    # Преобразуем в строку, если вдруг передан не строковый тип
    card_number = str(card_number)
    # Формируем маску: первые 4, пробел, следующие 2, **, пробел, ****, пробел, последние 4
    masked = f"{card_number[:4]} {card_number[4:6]}** **** {card_number[-4:]}"
    return masked

