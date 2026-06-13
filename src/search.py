import re
from collections import Counter
from typing import Any, Dict, List


def search_transactions(transactions: List[Dict[str, Any]], search_string: str) -> List[Dict[str, Any]]:
    """
    Возвращает список транзакций, у которых в описании (description) содержится искомая строка.
    """
    if not search_string:
        return transactions.copy()
    pattern = re.compile(re.escape(search_string), re.IGNORECASE)
    return [t for t in transactions if pattern.search(t.get("description", ""))]


def count_transactions_by_category(transactions: List[Dict[str, Any]], categories: List[str]) -> Dict[str, int]:
    """
    Подсчитывает количество транзакций, попадающих в каждую категорию.
    """
    counter = Counter()
    for t in transactions:
        desc = t.get("description", "").lower()
        for cat in categories:
            if cat.lower() in desc:
                counter[cat] += 1
    return dict(counter)
