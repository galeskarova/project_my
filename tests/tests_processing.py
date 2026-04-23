import pytest
from processing import filter_by_state, sort_by_date

def test_no_matching_state(sample_transactions):
    """Ни один словарь не имеет статуса 'REJECTED'."""
    result = filter_by_state(sample_transactions, "REJECTED")
    assert result == []


def test_empty_list():
    """Тест на пустой входной список.
    Передан пустой список."""
    assert filter_by_state([], "EXECUTED") == []
    assert filter_by_state([], "ANY") == []


def test_default_state(sample_transactions):
    """Тест на значение по умолчанию (state='EXECUTED')
    Вызов без аргумента state должен использовать 'EXECUTED'."""
    filtered = filter_by_state(sample_transactions)
    result_ids = [item["id"] for item in filtered]
    assert result_ids == [1, 3, 6]


def test_missing_state_key():
    """Тест, когда некоторые словари не содержат ключа 'state' """
    data = [
        {"id": 1, "state": "EXECUTED"},
        {"id": 2},                # без state
        {"id": 3, "state": "EXECUTED"},
    ]
    filtered = filter_by_state(data, "EXECUTED")
    assert len(filtered) == 2
    assert all(item["id"] in (1, 3) for item in filtered)


def test_original_list_unchanged(sample_transactions):
    """Проверка, что исходный список не изменяется.
    Функция не должна мутировать исходный список."""
    original_copy = sample_transactions.copy()
    filter_by_state(sample_transactions, "EXECUTED")
    assert sample_transactions == original_copy

def test_sort_descending(unsorted_transactions):
    result = sort_by_date(unsorted_transactions)
    expected_order = [1, 4, 3, 2, 5]  # id в порядке убывания дат (новые -> старые)
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_order


def test_sort_ascending(unsorted_transactions):
    result = sort_by_date(unsorted_transactions, reverse=False)
    expected_order = [5, 2, 3, 1, 4]  # старые -> новые, среди одинаковых дат порядок сохранён
    result_ids = [item["id"] for item in result]
    assert result_ids == expected_order

# ----- 3.  -----
def test_stable_sort_same_dates():
    """Одинаковые даты: порядок должен сохраниться (устойчивость)"""
    data = [
        {"id": 1, "date": "2023-01-01"},
        {"id": 2, "date": "2023-01-01"},
        {"id": 3, "date": "2023-01-01"},
    ]
    result = sort_by_date(data, reverse=True)
    assert [item["id"] for item in result] == [1, 2, 3]


def test_empty_list():
    """Пустой список"""
    assert sort_by_date([]) == []
    assert sort_by_date([], reverse=False) == []


def test_single_element():
    """Список с одним элементом"""
    data = [{"id": 42, "date": "2024-01-01"}]
    assert sort_by_date(data) == data
    assert sort_by_date(data, reverse=False) == data

