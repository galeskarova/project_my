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
    """
    Сортирует список словарей по дате (ключ 'date').

    Args:
        list_of_dicts (list of dict): Исходный список словарей.
        reverse (bool): Порядок сортировки.
                        True — убывание (сначала новые), False — возрастание.
                        По умолчанию True.

    Returns:
        list of dict: Новый отсортированный список.
    """
    return sorted(list_of_dicts, key=lambda x: x['date'], reverse=reverse)
