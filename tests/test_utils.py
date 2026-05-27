import pytest
import json
from pathlib import Path
from typing import Any, List, Dict

from src.utils import load_transactions


def test_load_transactions_success(tmp_path: Path) -> None:
    """Корректный JSON-файл со списком транзакций"""
    test_data: List[Dict[str, int]] = [
        {"id": 1, "amount": 100},
        {"id": 2, "amount": 200}
    ]
    file_path: Path = tmp_path / "operations.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    result: List[Dict[str, Any]] = load_transactions(str(file_path))
    assert result == test_data


def test_load_transactions_file_not_found() -> None:
    """Файл не существует -> пустой список"""
    result: List[Dict[str, Any]] = load_transactions("non_existent_file.json")
    assert result == []


def test_load_transactions_empty_file(tmp_path: Path) -> None:
    """Пустой файл -> пустой список"""
    file_path: Path = tmp_path / "empty.json"
    file_path.touch()
    result: List[Dict[str, Any]] = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_not_list(tmp_path: Path) -> None:
    """JSON-файл содержит не список (например, объект) -> пустой список"""
    test_data: Dict[str, str] = {"key": "value"}
    file_path: Path = tmp_path / "object.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(test_data, f)

    result: List[Dict[str, Any]] = load_transactions(str(file_path))
    assert result == []


def test_load_transactions_invalid_json(tmp_path: Path) -> None:
    """Повреждённый JSON -> пустой список"""
    file_path: Path = tmp_path / "invalid.json"
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write("{invalid json}")

    result: List[Dict[str, Any]] = load_transactions(str(file_path))
    assert result == []