import functools
from typing import Any, Callable, Optional


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызовов функции.
    Записывает результат выполнения или ошибку в файл или в консоль.

    Args:
        filename (str, optional): Имя файла для записи логов.
            Если None, логи выводятся в консоль (stdout).

    Returns:
        Callable: Декорированная функция.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                # Логируем ошибку и затем пробрасываем её
                if filename is None:
                    print(log_message)
                else:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message + '\n')
                raise
            else:
                # Если успешно – записываем лог
                if filename is None:
                    print(log_message)
                else:
                    with open(filename, 'a', encoding='utf-8') as f:
                        f.write(log_message + '\n')
                return result

        return wrapper

    return decorator
