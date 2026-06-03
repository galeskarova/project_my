import re
import logging
from pathlib import Path


logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)

log_file = log_dir / 'masks.log'
file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
file_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def get_mask_account(account):
    logger.info(f"Вызвана функция get_mask_account с аргументом: {account}")
    if account is None or not str(account).strip():
        return None  # или raise ValueError("Номер счёта не может быть пустым")
    account_str = str(account).strip()
    # Дополнительно: можно проверить, что строка состоит только из цифр, если это требуется
    if len(account_str) < 4:
        # Либо маскировать всё: "**" + "*" * (len...), либо выбросить ошибку
        raise ValueError("Номер счёта слишком короткий для маскирования")
    return "**" + account_str[-4:]


def get_mask_card_number(card_number):
    """Возвращает маску номера карты или None при ошибке."""
    logger.info(f"Вызвана функция get_mask_card_number с аргументом: {card_number}")
    if card_number is None:
        return None
    # Удаляем всё, кроме цифр
    digits = re.sub(r"\D", "", str(card_number))
    if len(digits) < 12 or len(digits) > 19:
        return None  # или raise ValueError
    first6 = digits[:6]
    last4 = digits[-4:]
    # Формируем маску: первые 6, затем "**", затем "****", затем последние 4
    masked = f"{first6[:4]} {first6[4:6]}** **** {last4}"
    return masked
