from src.inventory import load_stock, check_stock, decrement, get_stock


def test_check_stock():
    load_stock({"prod-1": 10})
    assert check_stock("prod-1", 5) is True
    assert check_stock("prod-1", 15) is False


def test_decrement():
    load_stock({"prod-1": 10})
    decrement("prod-1", 3)
    assert get_stock("prod-1") == 7
