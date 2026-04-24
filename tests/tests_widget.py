import pytest
from widget import mask_account_card, get_date
import re
from masks import get_mask_card_number
from masks import get_mask_account
from datetime import datetime

@pytest.mark.parametrize("input_str, expected", [
    # Стандарт 16 цифр
    ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
    ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
    ("MasterCard 1234567890123456", "MasterCard 1234 56** **** 3456"),
    ("МИР 1234567890123456", "МИР 1234 56** **** 3456"),
    # С пробелами внутри номера
    ("Visa 1234 5678 9012 3456", "Visa 1234 56** **** 3456"),
    # Без пробела после названия (вставится пробел)
    ("Visa1234567890123456", "Visa 1234 56** **** 3456"),
    # American Express (15 цифр) – get_mask_card_number формирует маску из первых 6 и последних 4
    ("Amex 378282246310005", "Amex 3782 82** **** 0005"),
])
def test_mask_account_card_card_types(input_str, expected):
    assert mask_account_card(input_str) == expected
@pytest.mark.parametrize("input_str, expected", [
    ("Счет 1234567890", "Счет **7890"),
    ("Счет 12345678901234567890", "Счет **7890"),
    ("Счет 1234", "Счет **1234"),
    ("Счет 12345", "Счет **2345"),
    ("Расчетный счет 1234567890", "Расчетный счет **7890"),
    ("счет 1234567890", "счет **7890"),          # нижний регистр
    ("СЧЕТ 1234567890", "СЧЕТ **7890"),          # верхний регистр
    # Символы №, -, / удаляются (не буквы и не пробелы)
    ("Счет № 1234567890", "Счет **7890"),
    ("Счет-1234567890", "Счет **7890"),
    # Буква "ё" не входит в диапазон [А-Яа-я] – будет потеряна
])
def test_mask_account_card_account_types(input_str, expected):
    assert mask_account_card(input_str) == expected

def test_mask_account_card_short_account_raises():
    with pytest.raises(ValueError, match="Номер счёта слишком короткий для маскирования"):
        mask_account_card("Счет 12")
    with pytest.raises(ValueError):
        mask_account_card("Счет 1")
    with pytest.raises(ValueError):
        mask_account_card("счет 123")

def test_mask_account_card_no_numbers():
    assert mask_account_card("Счет") == "Счет"
    assert mask_account_card("Visa Classic") == "Visa Classic"
    assert mask_account_card("") == ""
    assert mask_account_card("  ") == ""

def test_mask_account_card_none():
    assert mask_account_card(None) == ""

def test_mask_account_card_invalid_card_length():
    # 10 цифр -> None -> строка "None"
    assert mask_account_card("Visa 1234567890") == "Visa None"
    # 20 цифр -> None
    assert mask_account_card("MasterCard 12345678901234567890") == "MasterCard None"

def test_mask_account_card_prefix_only_letters_and_spaces():
    result = mask_account_card("Visa Classic (USA) 1234567890123456")
    assert result == "Visa Classic USA 1234 56** **** 3456"

