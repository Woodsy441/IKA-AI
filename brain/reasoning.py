"""
IKA AI Brain
Version 0.3
"""

def analyse_market(rsi, ema20, ema50, current_price):
    score = 0
    reasons = []

    # Trend
    if current_price > ema20:
        score += 20
        reasons.append("Price is above the 20 EMA")

    if current_price > ema50:
        score += 20
        reasons.append("Price is above the 50 EMA")

    # Momentum
    if 45 <= rsi <= 65:
        score += 20
        reasons.append("RSI is healthy")

    elif rsi < 30:
        reasons.append("RSI indicates oversold conditions")

    elif rsi > 70:
        reasons.append("RSI indicates overbought conditions")

    # Rating
    if score >= 60:
        rating = "Bullish"
    elif score >= 40:
        rating = "Neutral"
    else:
        rating = "Weak"

    return {
        "score": score,
        "rating": rating,
        "reasons": reasons
    }
    