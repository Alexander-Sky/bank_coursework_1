from src.processing import filter_by_state, sort_by_date


def test_filter_by_state(sample_operations):
    # Убедитесь, что функция используется
    filtered = filter_by_state(sample_operations, "EXECUTED")
    assert len(filtered) > 0
    # Добавьте проверки


def test_sort_by_date(sample_operations):
    sorted_ops = sort_by_date(sample_operations)
    # Добавьте проверки, например:
    assert sorted_ops[0]["date"] >= sorted_ops[-1]["date"]
