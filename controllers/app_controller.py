from analysis.market_scanner import scan_markets


class AppController:

    def __init__(self):
        self.last_scan = []

    def scan(self):

        self.last_scan = scan_markets()

        print("\nDEBUG RESULTS:")
        print(self.last_scan)

        return self.last_scan
        