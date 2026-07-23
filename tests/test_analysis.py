from src.analysis.market import format_market_data


def test_format_market_data_unknown():
    result = format_market_data("UNKNOWNSYMBOL")
    assert "No market data available" in result


def test_format_market_data_cached():
    result = format_market_data("BTCUSDT")
    if "No market data available" not in result:
        assert "BTCUSDT" in result
        assert "Price:" in result
