import pytest
@pytest.fixture(params={
    ("1234567890123456", "1234 56** **** 3456"),
    (1234567890123456, "1234 56** **** 3456"),
    ("0000111122223333", "0000 11** **** 3333"),
    ("123456789012", "1234 56** **** 9012"),
    ("123", "123 ** **** "),
    ("", " ** **** "),
})
def card_test_data(request):
    return request.param

# Фикстура для номеров счетов
@pytest.fixture(params=[
    ("12345678901234567890", "**7890"),
    (12345678901234567890,   "**7890"),
    ("1234",                 "**1234"),
    ("12",                   "**12"),
    ("",                     "**"),
    ("abc",                  "**abc"),
])
def account_test_data(request):
    return request.param

@pytest.fixture
def sample_transactions():
    return [
        {"id": 1, "state": "EXECUTED", "amount": 100},
        {"id": 2, "state": "PENDING", "amount": 200},
        {"id": 3, "state": "EXECUTED", "amount": 150},
        {"id": 4, "state": "CANCELED", "amount": 50},
        {"id": 5, "amount": 300},                     # нет ключа 'state'
        {"id": 6, "state": "EXECUTED", "amount": 75},
    ]

@pytest.fixture
def unsorted_transactions():
    return [
        {"id": 1, "date": "2023-12-01"},
        {"id": 2, "date": "2023-10-15"},
        {"id": 3, "date": "2023-11-20"},
        {"id": 4, "date": "2023-12-01"},  # одинаковая дата с id=1
        {"id": 5, "date": "2023-09-10"},
    ]
