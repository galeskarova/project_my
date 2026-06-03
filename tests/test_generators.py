from typing import Any, Dict, Iterator, List

import pytest

from src.generators import card_number_generator, filter_by_currency, transaction_descriptions


@pytest.fixture
def sample_transactions_1() -> List[Dict[str, Any]]:
    return [
        {
            "id": 1,
            "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "USD transaction 1",
        },
        {
            "id": 2,
            "operationAmount": {"amount": "200.00", "currency": {"name": "EUR", "code": "EUR"}},
            "description": "EUR transaction",
        },
        {
            "id": 3,
            "operationAmount": {"amount": "300.00", "currency": {"name": "USD", "code": "USD"}},
            "description": "USD transaction 2",
        },
        {
            "id": 4,
            "operationAmount": {"amount": "400.00", "currency": {"name": "GBP", "code": "GBP"}},
            "description": "GBP transaction",
        },
    ]


def test_filter_by_currency_returns_correct_transactions(sample_transactions_1: List[Dict[str, Any]]) -> None:
    """Проверяет, что фильтр возвращает только транзакции с заданной валютой"""
    usd_filter: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions_1, "USD")

    transactions_usd: List[Dict[str, Any]] = list(usd_filter)

    assert len(transactions_usd) == 2
    assert all(t["operationAmount"]["currency"]["code"] == "USD" for t in transactions_usd)
    assert transactions_usd[0]["id"] == 1
    assert transactions_usd[1]["id"] == 3


def test_filter_by_currency_no_matching_currency(sample_transactions_1: List[Dict[str, Any]]) -> None:
    """Если нет транзакций с указанной валютой, итератор должен быть пустым"""
    filter_rub: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions_1, "RUB")

    transactions_rub: List[Dict[str, Any]] = list(filter_rub)

    assert transactions_rub == []


def test_filter_by_currency_empty_list() -> None:
    """Пустой список транзакций не должен вызывать ошибок, итератор пуст"""
    empty_filter: Iterator[Dict[str, Any]] = filter_by_currency([], "USD")

    assert list(empty_filter) == []


def test_filter_by_currency_missing_currency_field() -> None:
    """Транзакции без поля 'currency' или с некорректной структурой игнорируются без ошибок"""
    transactions_with_bad_data: List[Dict[str, Any]] = [
        {"id": 5, "operationAmount": {"amount": "500"}},  # нет currency
        {"id": 6, "operationAmount": {}},  # пустой operationAmount
        {"id": 7},  # нет operationAmount
        {"id": 8, "operationAmount": {"currency": {"code": "USD"}}},  # корректная USD
    ]

    usd_filter: Iterator[Dict[str, Any]] = filter_by_currency(transactions_with_bad_data, "USD")

    result: List[Dict[str, Any]] = list(usd_filter)
    assert len(result) == 1
    assert result[0]["id"] == 8


def test_filter_by_currency_generator_lazy_evaluation(sample_transactions_1: List[Dict[str, Any]]) -> None:
    """Проверяет, что генератор работает лениво (не вычисляет все сразу)"""
    usd_filter: Iterator[Dict[str, Any]] = filter_by_currency(sample_transactions_1, "USD")

    # Поэлементное извлечение
    first: Dict[str, Any] = next(usd_filter)
    assert first["id"] == 1

    second: Dict[str, Any] = next(usd_filter)
    assert second["id"] == 3

    # Дальше должно быть StopIteration
    with pytest.raises(StopIteration):
        next(usd_filter)


@pytest.fixture
def sample_transactions_2() -> List[Dict[str, Any]]:
    return [
        {"id": 1, "description": "Перевод организации"},
        {"id": 2, "description": "Перевод со счета на счет"},
        {"id": 3, "description": "Перевод со счета на счет"},
        {"id": 4, "description": "Перевод с карты на карту"},
        {"id": 5, "description": "Перевод организации"},
    ]


def test_transaction_descriptions_returns_descriptions(sample_transactions_2: List[Dict[str, Any]]) -> None:
    """Проверяет, что генератор возвращает правильные описания для всех транзакций"""
    descriptions: Iterator[str] = transaction_descriptions(sample_transactions_2)
    expected: List[str] = [
        "Перевод организации",
        "Перевод со счета на счет",
        "Перевод со счета на счет",
        "Перевод с карты на карту",
        "Перевод организации",
    ]
    assert list(descriptions) == expected


def test_transaction_descriptions_empty_list() -> None:
    """Пустой список транзакций -> генератор не выдает ни одного описания"""
    descriptions: Iterator[str] = transaction_descriptions([])
    assert list(descriptions) == []


def test_transaction_descriptions_missing_description() -> None:
    """Если у транзакции нет ключа 'description', возвращается пустая строка (или None в зависимости от get)"""
    transactions_without_desc: List[Dict[str, Any]] = [
        {"id": 1, "description": "Нормальная транзакция"},
        {"id": 2, "amount": 100},  # нет description
        {"id": 3, "description": None},  # description = None
    ]
    descriptions: Iterator[str] = transaction_descriptions(transactions_without_desc)
    # По умолчанию .get возвращает None, но по условию задачи лучше вернуть пустую строку
    # Если хотим пустую строку, можно использовать .get("description", "")
    # В текущей реализации yield transaction.get("description", "") -> пустая строка
    assert list(descriptions) == ["Нормальная транзакция", "", ""]


def test_transaction_descriptions_generator_lazy_evaluation(sample_transactions_2: List[Dict[str, Any]]) -> None:
    """Проверка, что генератор работает лениво (пошаговый next)"""
    desc_gen: Iterator[str] = transaction_descriptions(sample_transactions_2)
    assert next(desc_gen) == "Перевод организации"
    assert next(desc_gen) == "Перевод со счета на счет"
    assert next(desc_gen) == "Перевод со счета на счет"
    assert next(desc_gen) == "Перевод с карты на карту"
    assert next(desc_gen) == "Перевод организации"
    with pytest.raises(StopIteration):
        next(desc_gen)


def test_transaction_descriptions_single_transaction() -> None:
    """Одна транзакция -> один элемент"""
    single: List[Dict[str, str]] = [{"description": "Тестовый перевод"}]
    gen: Iterator[str] = transaction_descriptions(single)
    assert next(gen) == "Тестовый перевод"
    with pytest.raises(StopIteration):
        next(gen)


def test_card_number_generator_range_1_to_5() -> None:
    """Проверяет правильность генерации для диапазона 1-5"""
    expected: List[str] = [
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
        "0000 0000 0000 0003",
        "0000 0000 0000 0004",
        "0000 0000 0000 0005",
    ]
    result: List[str] = list(card_number_generator(1, 5))
    assert result == expected


def test_card_number_generator_single_value() -> None:
    """Диапазон из одного значения"""
    result: List[str] = list(card_number_generator(42, 42))
    assert result == ["0000 0000 0000 0042"]


def test_card_number_generator_large_numbers() -> None:
    """Проверка форматирования чисел с разным количеством цифр"""
    result: List[str] = list(card_number_generator(9999, 10001))
    expected: List[str] = [
        "0000 0000 0000 9999",
        "0000 0000 0001 0000",
        "0000 0000 0001 0001",
    ]
    assert result == expected


def test_card_number_generator_max_range() -> None:
    """Проверка максимально допустимого номера"""
    result: List[str] = list(card_number_generator(9999999999999999, 9999999999999999))
    assert result == ["9999 9999 9999 9999"]


def test_card_number_generator_start_greater_than_end() -> None:
    """Если start > end, генератор не должен выдавать ни одного номера"""
    result: List[str] = list(card_number_generator(10, 5))
    assert result == []


def test_card_number_generator_zero_start() -> None:
    """Диапазон, включающий 0 (принимаем, что 0 даст 16 нулей)"""
    result: List[str] = list(card_number_generator(0, 2))
    expected: List[str] = [
        "0000 0000 0000 0000",
        "0000 0000 0000 0001",
        "0000 0000 0000 0002",
    ]
    assert result == expected


def test_card_number_generator_formatting() -> None:
    """Проверка правильности форматирования: ровно 4 группы по 4 цифры"""
    gen: Iterator[str] = card_number_generator(1234567890123456, 1234567890123456)
    card: str = next(gen)
    parts: List[str] = card.split()
    assert len(parts) == 4
    assert all(len(part) == 4 for part in parts)
    assert card == "1234 5678 9012 3456"


def test_card_number_generator_lazy_evaluation() -> None:
    """Генератор должен быть ленивым (пошаговый next)"""
    gen: Iterator[str] = card_number_generator(1, 3)
    assert next(gen) == "0000 0000 0000 0001"
    assert next(gen) == "0000 0000 0000 0002"
    assert next(gen) == "0000 0000 0000 0003"
    with pytest.raises(StopIteration):
        next(gen)
