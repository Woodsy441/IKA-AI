import customtkinter as ctk

from controllers.dashboard_controller import DashboardController


class DashboardPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        self.controller = DashboardController()

        self.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        # -----------------------------------------
        # Title
        # -----------------------------------------

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
            font=("Segoe UI", 30, "bold")
        )

        title.grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(20, 30)
        )

        # -----------------------------------------
        # Account cards
        # -----------------------------------------

        self.balance_value = self.create_card(
            1,
            0,
            "Balance",
            f"£{self.controller.get_balance():,.2f}"
        )

        self.equity_value = self.create_card(
            1,
            1,
            "Equity",
            f"£{self.controller.get_equity():,.2f}"
        )

        self.pnl_value = self.create_card(
            1,
            2,
            "Open P/L",
            f"£{self.controller.get_open_profit():,.2f}"
        )

        self.trades_value = self.create_card(
            2,
            0,
            "Open Trades",
            str(self.controller.get_open_trades())
        )

        self.winrate_value = self.create_card(
            2,
            1,
            "Win Rate",
            "0%"
        )

        self.daily_value = self.create_card(
            2,
            2,
            "Today's P/L",
            "£0.00"
        )

    # -----------------------------------------
    # Create card
    # -----------------------------------------

    def create_card(
        self,
        row,
        column,
        title,
        value
    ):

        frame = ctk.CTkFrame(
            self,
            height=120
        )

        frame.grid(
            row=row,
            column=column,
            padx=15,
            pady=15,
            sticky="nsew"
        )

        label = ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 16)
        )

        label.pack(
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Segoe UI", 28, "bold")
        )

        value_label.pack()

        return value_label

    # -----------------------------------------
    # Refresh
    # -----------------------------------------

    def refresh(self):

        self.controller.refresh()

        self.balance_value.configure(
            text=f"£{self.controller.get_balance():,.2f}"
        )

        self.equity_value.configure(
            text=f"£{self.controller.get_equity():,.2f}"
        )

        self.pnl_value.configure(
            text=f"£{self.controller.get_open_profit():,.2f}"
        )

        self.trades_value.configure(
            text=str(
                self.controller.get_open_trades()
            )
        )
        