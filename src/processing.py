from datetime import datetime

def filter_by_state(list_of_dicts, state='EXECUTED'):
    """
    Фильтрует список словарей по значению ключа 'state'.

    Args:
        list_of_dicts (list of dict): Исходный список словарей.
        state (str): Значение state для фильтрации. По умолчанию 'EXECUTED'.

    Returns:
        list of dict: Новый список, содержащий только словари с указанным state.
    """
    return [d for d in list_of_dicts if d.get('state') == state]



def sort_by_date(list_of_dicts, reverse=True):
    def safe_date(item):
        try:
            return datetime.fromisoformat(item['date'])
        except (KeyError, ValueError, TypeError):
            return datetime.min
    return sorted(list_of_dicts, key=safe_date, reverse=reverse)
