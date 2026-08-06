def calculate_position_size(account_size, risk_percent, entry_price, stop_loss):
    """
    Calculates the ideal position size based on risk.
    """

    risk_amount = account_size * (risk_percent / 100)

    stop_distance = abs(entry_price - stop_loss)

    if stop_distance == 0:
        return 0

    position_size = risk_amount / stop_distance

    return round(position_size, 2)
    