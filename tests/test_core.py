from src.core.order import Order


def test_order_long():
    order = Order(
        symbol="BTCUSDT",
        direction="LONG",
        entry=65000.0,
        tp=67000.0,
        sl=64000.0,
    )
    assert order.symbol == "BTCUSDT"
    assert order.direction == "LONG"
    assert order.risk_reward_ratio == 2.0
    assert order.tp_pct == 3.08
    assert order.sl_pct == -1.54


def test_order_short():
    order = Order(
        symbol="ETHUSDT",
        direction="SHORT",
        entry=3500.0,
        tp=3400.0,
        sl=3600.0,
    )
    assert order.direction == "SHORT"
    assert order.risk_reward_ratio == 1.0
    assert order.tp_pct == -2.86
    assert order.sl_pct == 2.86


def test_order_defaults():
    order = Order(
        symbol="SOLUSDT",
        direction="LONG",
        entry=150.0,
        tp=160.0,
        sl=145.0,
    )
    assert order.order_type == "MARKET"
    assert order.confidence == 0.0
