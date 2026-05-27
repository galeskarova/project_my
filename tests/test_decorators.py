from pathlib import Path
from typing import Any, Callable

import pytest

from src.decorators import log


def test_log_success_to_console(capsys: pytest.CaptureFixture[str]) -> None:
    """При успешном выполнении функции в консоль выводится 'func ok'"""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    result: int = add(3, 5)
    captured = capsys.readouterr()
    assert result == 8
    assert captured.out == "add ok\n"


def test_log_error_to_console(capsys: pytest.CaptureFixture[str]) -> None:
    """При возникновении исключения в консоль выводится информация об ошибке и аргументах"""

    @log()
    def divide(a: float, b: float) -> float:
        return a / b

    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

    captured = capsys.readouterr()
    expected_error_message: str = "divide error: ZeroDivisionError. Inputs: (10, 0), {}\n"
    assert captured.out == expected_error_message


def test_log_with_kwargs_to_console(capsys: pytest.CaptureFixture[str]) -> None:
    """Проверка логирования с именованными аргументами"""

    @log()
    def greet(name: str, greeting: str = "Hello") -> str:
        return f"{greeting}, {name}!"

    result: str = greet("Alice", greeting="Hi")
    captured = capsys.readouterr()
    assert result == "Hi, Alice!"
    assert captured.out == "greet ok\n"


def test_log_success_to_file(tmp_path: Path) -> None:
    """При успешном выполнении лог пишется в файл"""
    log_file: Path = tmp_path / "test.log"

    @log(filename=str(log_file))
    def multiply(x: int, y: int) -> int:
        return x * y

    result: int = multiply(4, 5)
    assert result == 20

    content: str = log_file.read_text(encoding="utf-8")
    assert content == "multiply ok\n"


def test_log_error_to_file(tmp_path: Path) -> None:
    """При ошибке лог с исключением и аргументами пишется в файл"""
    log_file: Path = tmp_path / "error.log"

    @log(filename=str(log_file))
    def faulty_func(val: int) -> None:
        raise ValueError("Invalid value")

    with pytest.raises(ValueError):
        faulty_func(42)

    content: str = log_file.read_text(encoding="utf-8")
    assert "faulty_func error: ValueError. Inputs: (42,), {}\n" == content


def test_log_append_to_existing_file(tmp_path: Path) -> None:
    """Проверка, что новые логи дописываются в конец файла"""
    log_file: Path = tmp_path / "append.log"

    @log(filename=str(log_file))
    def first_func() -> str:
        return "first"

    @log(filename=str(log_file))
    def second_func() -> str:
        return "second"

    first_func()
    second_func()

    content: str = log_file.read_text(encoding="utf-8")
    assert content == "first_func ok\nsecond_func ok\n"


def test_log_with_multiple_arguments_to_file(tmp_path: Path) -> None:
    """Проверка логирования с несколькими аргументами и kwargs"""
    log_file: Path = tmp_path / "args.log"

    @log(filename=str(log_file))
    def process(a: int, b: int, c: int = 10, d: int = 20) -> int:
        return a + b + c + d

    process(1, 2, c=30, d=40)
    content: str = log_file.read_text(encoding="utf-8")
    assert content == "process ok\n"


def test_return_value_preserved() -> None:
    """Декоратор должен возвращать исходное значение функции"""

    @log()
    def add(a: int, b: int) -> int:
        return a + b

    assert add(1, 2) == 3

    @log(filename="dummy.log")
    def multiply(a: int, b: int) -> int:
        return a * b

    assert multiply(3, 4) == 12