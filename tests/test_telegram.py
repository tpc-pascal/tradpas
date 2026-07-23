from src.telegram.parser import parse_message


def test_parse_long_market():
    msg = """
    BTCUSDT LONG
    Entry: 65000
    TP: 67000
    SL: 64000
    """
    order = parse_message(msg)
    assert order is not None
    assert order.symbol == "BTCUSDT"
    assert order.direction == "LONG"
    assert order.entry == 65000.0
    assert order.tp == 67000.0
    assert order.sl == 64000.0


def test_parse_short():
    msg = """
    ETHUSDT SHORT
    Entry: 3500
    TP: 3400
    SL: 3600
    """
    order = parse_message(msg)
    assert order is not None
    assert order.symbol == "ETHUSDT"
    assert order.direction == "SHORT"
    assert order.entry == 3500.0


def test_parse_with_limit():
    msg = """
    SOLUSDT LONG LIMIT
    Entry: 150
    TP: 160
    SL: 145
    """
    order = parse_message(msg)
    assert order is not None
    assert order.symbol == "SOLUSDT"
    assert order.order_type == "LIMIT"


def test_parse_invalid():
    msg = "Hello world"
    order = parse_message(msg)
    assert order is None


def test_parse_empty():
    order = parse_message("")
    assert order is None


def test_parse_buy_as_long():
    msg = """
    BTCUSDT BUY
    Entry: 65000
    TP: 67000
    SL: 64000
    """
    order = parse_message(msg)
    assert order is not None
    assert order.direction == "LONG"
