"""
IKA AI Brain
Version 0.3
"""

def analyse_market(rsi, ema20, ema50, current_price):

    score = 0
    reasons = []

    # EMA Trend
    if current_price > ema20:
        score += 20
        reasons.append("Price above EMA20")
    else:
        reasons.append("Price below EMA20")

    if current_price > ema50:
        score += 20
        reasons.append("Price above EMA50")
    else:
        reasons.append("Price below EMA50")

    # RSI
    if 45 <= rsi <= 65:
        score += 20
        reasons.append("Healthy RSI")
    elif rsi < 30:
        score += 15
        reasons.append("Oversold")
    elif rsi > 70:
        reasons.append("Overbought")

    # Rating
    if score >= 60:
        rating = "BUY"
    elif score >= 40:
        rating = "HOLD"
    else:
        rating = "SELL"

    stop_loss = round(current_price * 0.99, 2)
    take_profit = round(current_price * 1.02, 2)

    return {
        "score": score,
        "rating": rating,
        "reasons": reasons,
        "stop_loss": stop_loss,
        "take_profit": take_profit
    }