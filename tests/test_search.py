import pytest
from src.search import search_transactions, count_transactions_by_category

@pytest.fixture
def sample_transactions():
    return [
        {"description": "Перевод организации", "id": 1},
        {"description": "Перевод со счета на счет", "id": 2},
        {"description": "Перевод с карты на карту", "id": 3},
        {"description": "Оплата услуг", "id": 4},
        {"description": "Перевод другу", "id": 5}
    ]

def test_search_transactions_found(sample_transactions):
    result = search_transactions(sample_transactions, "перевод")
    assert len(result) == 4   # все, кроме "Оплата услуг"
    assert all("перевод" in t["description"].lower() for t in result)

def test_search_transactions_not_found(sample_transactions):
    result = search_transactions(sample_transactions, "покупка")
    assert result == []

def test_search_transactions_empty_string(sample_transactions):
    result = search_transactions(sample_transactions, "")
    assert result == sample_transactions

def test_search_transactions_case_insensitive(sample_transactions):
    result = search_transactions(sample_transactions, "ПЕРЕВОД")
    assert len(result) == 4

def test_count_transactions_by_category():
    transactions = [
        {"description": "Перевод организации"},
        {"description": "Перевод со счета на счет"},
        {"description": "Перевод с карты на карту"},
        {"description": "Оплата услуг"},
        {"description": "Перевод другу"}
    ]
    categories = ["Перевод", "Оплата"]
    result = count_transactions_by_category(transactions, categories)
    assert result["Перевод"] == 4
    assert result["Оплата"] == 1

def test_count_transactions_by_category_case_insensitive():
    transactions = [{"description": "перевод организации"}]
    categories = ["Перевод"]
    result = count_transactions_by_category(transactions, categories)
    assert result["Перевод"] == 1

def test_count_transactions_by_category_no_match():
    transactions = [{"description": "Покупка"}]
    categories = ["Перевод"]
    result = count_transactions_by_category(transactions, categories)
    assert result == {}