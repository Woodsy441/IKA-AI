"""
IKA AI Configuration
Version 1.0
"""

# ==========================================
# ACCOUNT SETTINGS
# ==========================================

ACCOUNT_SIZE = 10000
RISK_PERCENT = 1

# ==========================================
# PORTFOLIO
# ==========================================

MAX_OPEN_TRADES = 10

# ==========================================
# TRADING
# ==========================================

PAPER_TRADING = True

# ==========================================
# SCANNER
# ==========================================

SCAN_INTERVAL = 300

# ==========================================
# FILES
# ==========================================

PORTFOLIO_FILE = "history/portfolio.json"
TRADE_HISTORY_FILE = "history/trade_history.csv"

# ==========================================
# MARKET TICKERS
# ==========================================

ASSETS = {
    "Gold": "GC=F",
    "Apple": "AAPL",
    "Microsoft": "MSFT",
    "NVIDIA": "NVDA",
    "Amazon": "AMZN",
    "Meta": "META",
    "Google": "GOOGL",
    "Tesla": "TSLA"
}
