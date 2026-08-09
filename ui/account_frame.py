import customtkinter as ctk


class AccountFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(fg_color="transparent")

        # -----------------------------
        # Title
        # -----------------------------

        title = ctk.CTkLabel(
            self,
            text="Account Overview",
            font=("Segoe UI", 24, "bold")
        )

        title.pack(anchor="w", padx=20, pady=(15, 20))

        # -----------------------------
        # Cards
        # -----------------------------

        cards = ctk.CTkFrame(self)
        cards.pack(fill="x", padx=20)

        cards.grid_columnconfigure((0, 1, 2, 3), weight=1)

        self.balance_card = self.create_card(cards, "Balance", "£10,000.00")
        self.balance_card.grid(row=0, column=0, padx=10, sticky="nsew")

        self.equity_card = self.create_card(cards, "Equity", "£10,000.00")
        self.equity_card.grid(row=0, column=1, padx=10, sticky="nsew")

        self.pnl_card = self.create_card(cards, "Open P/L", "£0.00")
        self.pnl_card.grid(row=0, column=2, padx=10, sticky="nsew")

        self.trades_card = self.create_card(cards, "Open Trades", "0")
        self.trades_card.grid(row=0, column=3, padx=10, sticky="nsew")

    def create_card(self, parent, title, value):

        frame = ctk.CTkFrame(parent, corner_radius=12)

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 15)
        )
        label.pack(pady=(15, 5))

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Segoe UI", 24, "bold")
        )
        value_label.pack(pady=(0, 15))

        frame.value_label = value_label

        return frame

    def update_account(self, account, open_trades=0):

        self.balance_card.value_label.configure(
            text=f"£{account.balance:,.2f}"
        )

        self.equity_card.value_label.configure(
            text=f"£{account.balance + account.open_profit:,.2f}"
        )

        pnl_colour = "green"

        if account.open_profit < 0:
            pnl_colour = "red"

        self.pnl_card.value_label.configure(
            text=f"£{account.open_profit:,.2f}",
            text_color=pnl_colour
        )

        self.trades_card.value_label.configure(
            text=str(open_trades)
        )
        