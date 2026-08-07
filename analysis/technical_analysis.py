import yfinance as yf
from ta.momentum import RSIIndicator
from ta.trend import EMAIndicator

from config import ACCOUNT_SIZE, RISK_PERCENT
from brain.reasoning import analyse_market
from analysis.risk_management import calculate_risk
from analysis.position_sizing import calculate_position_size


def analyse_asset(name, ticker):

    data = yf.download(
        ticker,
        period="6mo",
        interval="1d",
        progress=False
    )

    if data.empty:
        return None

    close = data["Close"]

    if hasattr(close, "columns"):
        close = close.iloc[:, 0]

    rsi = RSIIndicator(close).rsi().iloc[-1]

    ema20 = EMAIndicator(
        close,
        window=20
    ).ema_indicator().iloc[-1]

    ema50 = EMAIndicator(
        close,
        window=50
    ).ema_indicator().iloc[-1]

    current_price = float(close.iloc[-1])

    risk = calculate_risk(
        data,
        current_price
    )

    result = analyse_market(
        rsi=rsi,
        ema20=ema20,
        ema50=ema50,
        current_price=current_price
    )

    result["asset"] = name
    result["ticker"] = ticker
    result["price"] = round(current_price, 2)

    result["atr"] = risk["atr"]
    result["stop_loss"] = risk["stop_loss"]
    result["take_profit"] = risk["take_profit"]

    result["position_size"] = calculate_position_size(
        ACCOUNT_SIZE,
        RISK_PERCENT,
        current_price,
        risk["stop_loss"]
    )

    return result
    