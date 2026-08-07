import customtkinter as ctk


class AccountFrame(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.configure(corner_radius=10)

        title = ctk.CTkLabel(
            self,
            text="Account",
            font=("Arial", 22, "bold")
        )
        title.pack(anchor="w", padx=20, pady=(15, 10))

        self.balance = ctk.CTkLabel(
            self,
            text="Balance: £10,000.00",
            font=("Arial", 18)
        )
        self.balance.pack(anchor="w", padx=20, pady=5)

        self.equity = ctk.CTkLabel(
            self,
            text="Equity: £10,000.00",
            font=("Arial", 18)
        )
        self.equity.pack(anchor="w", padx=20, pady=5)

        self.pnl = ctk.CTkLabel(
            self,
            text="Open P/L: £0.00",
            font=("Arial", 18)
        )
        self.pnl.pack(anchor="w", padx=20, pady=5)

    def update_account(self, account):

        self.balance.configure(
            text=f"Balance: £{account.balance:,.2f}"
        )

        self.equity.configure(
            text=f"Equity: £{account.balance + account.open_profit:,.2f}"
        )

        self.pnl.configure(
            text=f"Open P/L: £{account.open_profit:,.2f}"
        )
        