from typing import Dict, List


def filter_by_state(operations: List[Dict], state: str = "EXECUTED") -> List[Dict]:
    """
    Фильтрует список операций по состоянию

    Args:
        operations (List[Dict]): список операций
        state (str): состояние для фильтрации (по умолчанию 'EXECUTED')

    Returns:
        List[Dict]: отфильтрованный список операций
    """
    return [op for op in operations if op.get("state") == state]


def sort_by_date(operations: List[Dict], descending: bool = True) -> List[Dict]:
    """
    Сортирует список операций по дате

    Args:
        operations (List[Dict]): список операций
        descending (bool): порядок сортировки (True - убывание, False - возрастание)

    Returns:
        List[Dict]: отсортированный список операций
    """
    return sorted(operations, key=lambda x: x["date"], reverse=descending)
