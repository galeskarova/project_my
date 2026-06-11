import sys
from src.utils import load_transactions
from src.file_reader import read_csv_transactions, read_excel_transactions
from src.processing import sort_by_date
from src.widget import get_date, mask_account_card
from src.search import search_transactions

def get_user_choice(prompt: str, options: list) -> str:
    """Запрашивает у пользователя выбор из допустимых вариантов."""
    while True:
        choice = input(prompt).strip()
        if choice in options:
            return choice
        print(f"Неверный ввод. Пожалуйста, выберите из {options}")

def get_yes_no(prompt: str) -> bool:
    """Запрашивает ответ Да/Нет, возвращает True/False."""
    while True:
        answer = input(prompt + " (Да/Нет): ").strip().lower()
        if answer in ("да", "yes", "y"):
            return True
        if answer in ("нет", "no", "n"):
            return False
        print("Пожалуйста, ответьте 'Да' или 'Нет'.")

def display_transactions(transactions):
    """Выводит транзакции в отформатированном виде, аналогичном примеру."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return
    print(f"\nВсего банковских операций в выборке: {len(transactions)}")
    for t in transactions:
        date = get_date(t["date"])
        desc = t["description"]
        from_str = mask_account_card(t.get("from", "")) if "from" in t else ""
        to_str = mask_account_card(t.get("to", "")) if "to" in t else ""
        amount = float(t["operationAmount"]["amount"])
        currency = t["operationAmount"]["currency"]["code"]
        if currency == "RUB":
            amount_str = f"{amount:.2f} руб."
        else:
            amount_str = f"{amount:.2f} {currency}"
        print(f"\n{date} {desc}")
        if from_str and to_str:
            print(f"{from_str} -> {to_str}")
        elif to_str:
            print(to_str)
        print(f"Сумма: {amount_str}")

def main():
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")
    source = get_user_choice("Ваш выбор: ", ["1", "2", "3"])
    if source == "1":
        file_path = "data/operations.json"
        print("Для обработки выбран JSON-файл.")
        transactions = load_transactions(file_path)
    elif source == "2":
        file_path = "data/transactions.csv"
        print("Для обработки выбран CSV-файл.")
        transactions = read_csv_transactions(file_path)
    else:
        file_path = "data/transactions_excel.xlsx"
        print("Для обработки выбран XLSX-файл.")
        transactions = read_excel_transactions(file_path)

    if not transactions:
        print("Не удалось загрузить транзакции. Проверьте файл.")
        return

    # Фильтрация по статусу
    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    while True:
        status_input = input("Введите статус, по которому необходимо выполнить фильтрацию. Доступные статусы: EXECUTED, CANCELED, PENDING\n").strip().upper()
        if status_input in valid_statuses:
            break
        print(f"Статус операции \"{status_input}\" недоступен.")
    transactions = [t for t in transactions if t.get("state", "").upper() == status_input]
    print(f"Операции отфильтрованы по статусу \"{status_input}\"")

    # Сортировка по дате
    if get_yes_no("Отсортировать операции по дате?"):
        order = get_user_choice(
            "Отсортировать по возрастанию или по убыванию? (введите 'по возрастанию' или 'по убыванию'): ",
            ["по возрастанию", "по убыванию"]
        )
        reverse = (order == "по убыванию")
        transactions = sort_by_date(transactions, reverse=reverse)

    # Фильтрация по рублевым транзакциям
    if get_yes_no("Выводить только рублевые транзакции?"):
        transactions = [t for t in transactions
                        if t.get("operationAmount", {}).get("currency", {}).get("code") == "RUB"]

    # Поиск по слову в описании
    if get_yes_no("Отфильтровать список транзакций по определенному слову в описании?"):
        search_word = input("Введите слово для поиска: ").strip()
        if search_word:
            transactions = search_transactions(transactions, search_word)

    print("\nРаспечатываю итоговый список транзакций...")
    display_transactions(transactions)

if __name__ == "__main__":
    main()