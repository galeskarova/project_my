import csv
import logging
from pathlib import Path
from typing import List, Dict, Any

try:
    import pandas as pd
except ImportError:
    pd = None

logger = logging.getLogger(__name__)

log_dir = Path(__file__).parent.parent / "logs"
log_dir.mkdir(exist_ok=True)
log_file = log_dir / "file_reader.log"
file_handler = logging.FileHandler(log_file, mode="w", encoding="utf-8")
file_handler.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
if not logger.handlers:
    logger.addHandler(file_handler)


def read_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает транзакции из CSV-файла и возвращает список словарей.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            transactions = [row for row in reader]
        logger.info(f"Успешно загружено {len(transactions)} транзакций из CSV: {file_path}")
        return transactions
    except FileNotFoundError:
        logger.error(f"CSV файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении CSV файла {file_path}: {e}")
        return []


def read_excel_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Считывает транзакции из Excel-файла (XLSX) и возвращает список словарей.
    """
    if pd is None:
        logger.error("Библиотека pandas не установлена")
        return []

    try:
        df = pd.read_excel(file_path, dtype=str, keep_default_na=False)
        df = df.fillna("")
        transactions = df.to_dict(orient="records")
        logger.info(f"Успешно загружено {len(transactions)} транзакций из Excel: {file_path}")
        return transactions
    except FileNotFoundError:
        logger.error(f"Excel файл не найден: {file_path}")
        return []
    except Exception as e:
        logger.error(f"Ошибка при чтении Excel файла {file_path}: {e}")
        return []
