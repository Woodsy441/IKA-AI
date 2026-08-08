import customtkinter as ctk

from ui.market_table import MarketTable


class ScannerFrame(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.configure(corner_radius=10)

        # ---------------- Header ---------------- #

        header = ctk.CTkFrame(self)
        header.pack(fill="x", padx=15, pady=15)

        title = ctk.CTkLabel(
            header,
            text="Market Scanner",
            font=("Segoe UI", 22, "bold")
        )
        title.pack(side="left")

        self.scan_button = ctk.CTkButton(
            header,
            text="🔄 Scan Markets",
            width=150,
            command=self.scan_markets
        )
        self.scan_button.pack(side="right")

        # ---------------- Table ---------------- #

        self.table = MarketTable(self)
        self.table.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=(0, 15)
        )

    def scan_markets(self):

        self.scan_button.configure(state="disabled")

        try:
            results = self.controller.scan()

            if results:
                self.table.populate(results)

        finally:
            self.scan_button.configure(state="normal")
            