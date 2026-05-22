import pytest
import json
from pathlib import Path
from src.utils import load_transactions


def test_load_transactions_success(tmp_path):
    """Корректный JSON-файл со списком транзакций"""
    test_data = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200}
    ]
    file_path = tmp_path / "operations.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    result = load_transactions(str(file_path))
    assert result == test_data


def test_load_transactions_file_not_found():
    """Файл не существует -> пустой список"""
    result = load_transactions("non_existent_file.json")
    assert result == []


def test_load_transactions_empty_file(tmp_path):
    """Пустой файл -> пустой список"""
    file_path = tmp_path / "empty.json"
    file_path.touch()
    result = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_not_list(tmp_path):
    """JSON-файл содержит не список (например, объект) -> пустой список"""
    test_data = {"key": "value"}
    file_path = tmp_path / "object.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    result = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_invalid_json(tmp_path):
    """Повреждённый JSON -> пустой список"""
    file_path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")

    result = load_transactions(str(file_path))
    assert result == []