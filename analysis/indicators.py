from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator


def calculate_rsi(close_prices):
    """Return the latest RSI value."""
    rsi = RSIIndicator(close_prices).rsi()
    return round(rsi.iloc[-1], 2)


def calculate_ema(close_prices, period):
    """Return the latest EMA value."""
    ema = EMAIndicator(close_prices, window=period).ema_indicator()
    return round(ema.iloc[-1], 2)
    