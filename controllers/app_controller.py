from analysis.market_scanner import scan_markets


class AppController:
    """
    Main controller connecting the GUI to the trading engine.
    """

    def __init__(self):
        self.last_scan = []

    def scan(self):
        """
        Run a market scan and store the results.
        """
        self.last_scan = scan_markets()
        return self.last_scan

    def get_last_scan(self):
        """
        Return the most recent scan results.
        """
        return self.last_scan