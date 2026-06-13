from unittest.mock import patch


def test_main_json_flow():
    with patch(
        "main.load_transactions",
        return_value=[
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T00:00:00",
                "description": "Test",
                "operationAmount": {"amount": "100", "currency": {"code": "RUB"}},
            }
        ],
    ):
        with patch("builtins.input", side_effect=["1", "EXECUTED", "нет", "нет", "нет"]):
            with patch("builtins.print") as mock_print:
                # Импортируем main только после настройки моков
                from main import main

                main()

    # Проверяем, что в выводе есть нужная строка
    calls = [call[0][0] for call in mock_print.call_args_list]
    assert any("Всего банковских операций в выборке: 1" in str(c) for c in calls)
