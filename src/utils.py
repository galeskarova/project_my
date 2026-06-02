import json
from typing import Any, Dict, List
import logging
import json
from pathlib import Path
from typing import List, Dict, Any

# Настройка логгера для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

log_dir = Path(__file__).parent.parent / 'logs'
log_dir.mkdir(exist_ok=True)

log_file = log_dir / 'utils.log'
file_handler = logging.FileHandler(log_file, mode='w', encoding='utf-8')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    logger.info(f"Загрузка транзакций из файла: {file_path}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"Файл не найден: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Ошибка декодирования JSON в файле {file_path}: {e}")
        return []

    if not isinstance(data, list):
        logger.warning(f"Данные в файле {file_path} не являются списком, возвращён пустой список")
        return []

    logger.info(f"Успешно загружено {len(data)} транзакций из {file_path}")
    return data

def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список транзакций из JSON-файла.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

    if not isinstance(data, list):
        return []

    return data
