from typing import Any, Dict
from unittest.mock import MagicMock, patch

import pytest
import requests

from src.external_api import convert_to_rub, get_currency_rate


# Фикстура с примером транзакции в USD
@pytest.fixture
def usd_transaction() -> Dict[str, Any]:
    return {"id": 1, "operationAmount": {"amount": "100.00", "currency": {"name": "USD", "code": "USD"}}}


@pytest.fixture
def eur_transaction() -> Dict[str, Any]:
    return {"id": 2, "operationAmount": {"amount": "50.00", "currency": {"name": "EUR", "code": "EUR"}}}


@pytest.fixture
def rub_transaction() -> Dict[str, Any]:
    return {"id": 3, "operationAmount": {"amount": "1000.00", "currency": {"name": "RUB", "code": "RUB"}}}


def test_convert_to_rub_rub_transaction(rub_transaction: Dict[str, Any]) -> None:
    """Рублёвая транзакция не требует конвертации"""
    result = convert_to_rub(rub_transaction)
    assert result == 1000.0


@patch("src.external_api.get_currency_rate")
def test_convert_to_rub_usd_transaction(mock_get_rate: MagicMock, usd_transaction: Dict[str, Any]) -> None:
    """Конвертация USD в RUB по фиктивному курсу"""
    mock_get_rate.return_value = 75.5
    result = convert_to_rub(usd_transaction)
    assert result == 100.0 * 75.5
    mock_get_rate.assert_called_once_with("USD")


@patch("src.external_api.get_currency_rate")
def test_convert_to_rub_eur_transaction(mock_get_rate: MagicMock, eur_transaction: Dict[str, Any]) -> None:
    """Конвертация EUR в RUB"""
    mock_get_rate.return_value = 90.0
    result = convert_to_rub(eur_transaction)
    assert result == 50.0 * 90.0
    mock_get_rate.assert_called_once_with("EUR")


def test_convert_to_rub_invalid_transaction() -> None:
    """Ошибочная структура транзакции -> 0.0"""
    result = convert_to_rub({"no_amount": 123})
    assert result == 0.0


@patch("src.external_api.requests.get")
@patch("src.external_api.API_KEY", "fake_key")  # подменяем ключ на фиктивный
def test_get_currency_rate_success(mock_get: MagicMock) -> None:
    """Успешный вызов API возвращает курс"""
    mock_response = MagicMock()
    mock_response.json.return_value = {"result": 75.5}
    mock_response.raise_for_status.return_value = None
    mock_get.return_value = mock_response

    rate = get_currency_rate("USD")
    assert rate == 75.5

    mock_get.assert_called_once()
    args, kwargs = mock_get.call_args
    assert kwargs["params"]["from"] == "USD"
    assert kwargs["params"]["to"] == "RUB"
    assert kwargs["headers"]["apikey"] == "fake_key"


@patch("src.external_api.requests.get")
@patch("src.external_api.API_KEY", "fake_key")  # подменяем ключ на фиктивный
def test_get_currency_rate_failure(mock_get: MagicMock) -> None:
    """Сбой API (ошибка соединения) -> возвращает 0.0"""
    # Выбрасываем исключение, которое перехватывается в функции
    mock_get.side_effect = requests.ConnectionError("Connection error")
    rate = get_currency_rate("USD")
    assert rate == 0.0


@patch("src.external_api.API_KEY", None)  # отключаем ключ
def test_get_currency_rate_no_api_key() -> None:
    """Отсутствие API ключа -> 0.0"""
    rate = get_currency_rate("USD")
    assert rate == 0.0
