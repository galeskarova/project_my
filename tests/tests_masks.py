import pytest
from masks import get_mask_account, get_mask_card_number

def test_improved_normal():
    assert get_mask_account("1234567890") == "**7890"

def test_improved_short_raises():
    with pytest.raises(ValueError, match="слишком короткий"):
        get_mask_account("123")

def test_improved_none_returns_none():
    assert get_mask_account(None) is None

def test_improved_empty_returns_none():
    assert get_mask_account("   ") is None


def test_improved():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"
    assert get_mask_card_number("1234 5678 9012 3456") == "1234 56** **** 3456"
    assert get_mask_card_number("1234-5678-9012-3456") == "1234 56** **** 3456"
    assert get_mask_card_number("378282246310005") == "3782 82** **** 0005"   # 15 цифр
    assert get_mask_card_number("123456789012345678") == "1234 56** **** 5678" # 18 цифр
    assert get_mask_card_number("") is None
    assert get_mask_card_number(None) is None
    assert get_mask_card_number("   ") is None
    assert get_mask_card_number("12345") is None   # слишком короткий