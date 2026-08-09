import customtkinter as ctk

from controllers.dashboard_controller import DashboardController


class DashboardPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.controller = DashboardController()

        # ==================================================
        # Main layout
        # ==================================================

        self.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.grid_rowconfigure(
            3,
            weight=1
        )

        # ==================================================
        # Title
        # ==================================================

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
            pady=(20, 20)
        )

        # ==================================================
        # Account cards
        # ==================================================

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

        # ==================================================
        # Open positions section
        # ==================================================

        positions_title = ctk.CTkLabel(
            self,
            text="Open Positions",
            font=("Segoe UI", 22, "bold")
        )

        positions_title.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="w",
            padx=20,
            pady=(20, 10)
        )

        # ==================================================
        # Positions container
        # ==================================================

        self.positions_frame = ctk.CTkScrollableFrame(
            self
        )

        self.positions_frame.grid(
            row=4,
            column=0,
            columnspan=3,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

        self.positions_frame.grid_columnconfigure(
            (0, 1, 2, 3, 4, 5),
            weight=1
        )

        # Draw initial table
        self.update_positions()

        # ==================================================
        # Auto refresh
        # ==================================================

        self.after(
            5000,
            self.auto_refresh
        )

    # ======================================================
    # Create dashboard card
    # ======================================================

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
            pady=10,
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

    # ======================================================
    # Update account cards
    # ======================================================

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

        self.update_positions()

    # ======================================================
    # Auto refresh
    # ======================================================

    def auto_refresh(self):

        try:

            self.refresh()

        except Exception as error:

            print(
                "Dashboard refresh error:",
                error
            )

        self.after(
            5000,
            self.auto_refresh
        )

    # ======================================================
    # Update positions table
    # ======================================================

    def update_positions(self):

        # Remove old rows
        for widget in self.positions_frame.winfo_children():

            widget.destroy()

        # --------------------------------------------------
        # Table headers
        # --------------------------------------------------

        headers = [
            "Asset",
            "Action",
            "Entry",
            "Current",
            "P/L",
            "Status"
        ]

        for column, header in enumerate(headers):

            label = ctk.CTkLabel(
                self.positions_frame,
                text=header,
                font=("Segoe UI", 14, "bold")
            )

            label.grid(
                row=0,
                column=column,
                padx=10,
                pady=10,
                sticky="ew"
            )

        # --------------------------------------------------
        # Get open trades
        # --------------------------------------------------

        positions = self.controller.get_open_positions()

        # --------------------------------------------------
        # Empty portfolio
        # --------------------------------------------------

        if not positions:

            empty = ctk.CTkLabel(
                self.positions_frame,
                text="No open positions",
                font=("Segoe UI", 15)
            )

            empty.grid(
                row=1,
                column=0,
                columnspan=6,
                pady=30
            )

            return

        # --------------------------------------------------
        # Add positions
        # --------------------------------------------------

        for row, trade in enumerate(
            positions,
            start=1
        ):

            asset = trade.get(
                "asset",
                "Unknown"
            )

            action = trade.get(
                "action",
                "-"
            )

            entry = trade.get(
                "entry"
            )

            current = trade.get(
                "current_price"
            )

            profit_loss = trade.get(
                "profit_loss"
            )

            status = trade.get(
                "status",
                "-"
            )

            # ----------------------------------------------
            # Format values
            # ----------------------------------------------

            entry_text = self.format_price(
                entry
            )

            current_text = self.format_price(
                current
            )

            pnl_text = self.format_pnl(
                profit_loss
            )

            # ----------------------------------------------
            # Create row
            # ----------------------------------------------

            values = [
                asset,
                action,
                entry_text,
                current_text,
                pnl_text,
                status
            ]

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.positions_frame,
                    text=value,
                    font=("Segoe UI", 14)
                )

                label.grid(
                    row=row,
                    column=column,
                    padx=10,
                    pady=8,
                    sticky="ew"
                )

    # ======================================================
    # Format price
    # ======================================================

    def format_price(self, value):

        if value is None:

            return "—"

        try:

            return f"£{float(value):,.2f}"

        except (
            ValueError,
            TypeError
        ):

            return "—"

    # ======================================================
    # Format P/L
    # ======================================================

    def format_pnl(self, value):

        if value is None:

            return "—"

        try:

            value = float(value)

            if value > 0:

                return f"+£{value:,.2f}"

            return f"£{value:,.2f}"

        except (
            ValueError,
            TypeError
        ):

            return "—"
            