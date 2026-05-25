import os

import requests
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

API_KEY = os.getenv("EXCHANGE_API_KEY")
BASE_URL = "https://api.apilayer.com/exchangerates_data"


def get_currency_rate(currency: str) -> float:
    """
    Возвращает курс заданной валюты к рублю (RUB) через внешнее API.
    Если API недоступен или нет ключа, возвращает 0.0.
    """
    if not API_KEY:
        print("API key not found. Set EXCHANGE_API_KEY in .env")
        return 0.0

    url = f"{BASE_URL}/convert"
    params = {"from": currency, "to": "RUB", "amount": 1}
    headers = {"apikey": API_KEY}

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        # Успешный ответ содержит "result" – сконвертированная сумма
        return float(data["result"])
    except (requests.RequestException, KeyError, ValueError) as e:
        print(f"Error fetching rate for {currency}: {e}")
        return 0.0


def convert_to_rub(transaction: dict) -> float:
    """
    Принимает транзакцию (словарь) и возвращает сумму в рублях (float).
    Если транзакция уже в рублях, возвращает исходную сумму.
    Если валюта USD или EUR – конвертирует по курсу API.
    В случае ошибки или неизвестной валюты возвращает 0.0.
    """
    # Извлекаем сумму и валюту из транзакции
    # Предполагается структура из примера:
    # {"operationAmount": {"amount": "100.00", "currency": {"code": "USD"}}}
    try:
        amount_str = transaction["operationAmount"]["amount"]
        currency = transaction["operationAmount"]["currency"]["code"]
        amount = float(amount_str)
    except (KeyError, ValueError, TypeError):
        return 0.0

    if currency == "RUB":
        return amount

    if currency in ("USD", "EUR"):
        rate = get_currency_rate(currency)
        return amount * rate

    # Если валюта не поддерживается или неизвестна
    return 0.0
