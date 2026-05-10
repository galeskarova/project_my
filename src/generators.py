def filter_by_currency(transactions, currency_code):
    """
    Возвращает итератор, который поочередно выдает транзакции
    """
    for transaction in transactions:
        # Безопасно получаем код валюты из вложенного словаря
        if transaction.get("operationAmount", {}).get("currency", {}).get("code") == currency_code:
            yield transaction


def transaction_descriptions(transactions):
    """
    Принимает список словарей с транзакциями.
    """
    for transaction in transactions:
        # Безопасно получаем описание, если ключа нет – возвращаем пустую строку или None
        yield transaction.get("description", "")


def card_number_generator(start, end):
    """
    Генерирует номера банковских карт в формате 'XXXX XXXX XXXX XXXX'
    """
    for number in range(start, end + 1):
        # Преобразуем число в 16-значную строку с ведущими нулями
        number_str = f"{number:016d}"
        # Разбиваем на группы по 4 цифры и объединяем через пробел
        formatted = " ".join(number_str[i:i+4] for i in range(0, 16, 4))
        yield formatted