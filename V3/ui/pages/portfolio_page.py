import customtkinter as ctk

from controllers.dashboard_controller import DashboardController


class PortfolioPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.controller = DashboardController()

        self.grid_columnconfigure(
            0,
            weight=1
        )

        self.grid_rowconfigure(
            2,
            weight=1
        )

        # ==================================================
        # Header
        # ==================================================

        header = ctk.CTkFrame(self)

        header.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=20,
            pady=(20, 10)
        )

        header.grid_columnconfigure(
            0,
            weight=1
        )

        title = ctk.CTkLabel(
            header,
            text="Portfolio",
            font=("Segoe UI", 30, "bold")
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=15
        )

        self.refresh_button = ctk.CTkButton(
            header,
            text="🔄 Refresh",
            width=130,
            command=self.refresh
        )

        self.refresh_button.grid(
            row=0,
            column=1,
            padx=15
        )

        # ==================================================
        # Summary
        # ==================================================

        self.summary = ctk.CTkFrame(self)

        self.summary.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=20,
            pady=10
        )

        self.summary.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.balance_label = self.create_summary_card(
            0,
            "Balance",
            "£0.00"
        )

        self.pnl_label = self.create_summary_card(
            1,
            "Open P/L",
            "£0.00"
        )

        self.trades_label = self.create_summary_card(
            2,
            "Open Trades",
            "0"
        )

        # ==================================================
        # Positions
        # ==================================================

        self.positions_frame = ctk.CTkScrollableFrame(
            self
        )

        self.positions_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(10, 20)
        )

        for column in range(8):

            self.positions_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.refresh()

    # ======================================================
    # Summary Card
    # ======================================================

    def create_summary_card(
        self,
        column,
        title,
        value
    ):

        frame = ctk.CTkFrame(
            self.summary
        )

        frame.grid(
            row=0,
            column=column,
            padx=8,
            pady=8,
            sticky="ew"
        )

        ctk.CTkLabel(
            frame,
            text=title,
            font=("Segoe UI", 14)
        ).pack(
            pady=(15, 5)
        )

        value_label = ctk.CTkLabel(
            frame,
            text=value,
            font=("Segoe UI", 24, "bold")
        )

        value_label.pack(
            pady=(0, 15)
        )

        return value_label

    # ======================================================
    # Refresh
    # ======================================================

    def refresh(self):

        try:

            self.controller.refresh()

            self.balance_label.configure(
                text=(
                    f"£{self.controller.get_balance():,.2f}"
                )
            )

            self.pnl_label.configure(
                text=(
                    f"£{self.controller.get_open_profit():,.2f}"
                )
            )

            self.trades_label.configure(
                text=str(
                    self.controller.get_open_trades()
                )
            )

            self.display_positions()

        except Exception as error:

            print(
                "Portfolio refresh error:",
                error
            )

    # ======================================================
    # Display Positions
    # ======================================================

    def display_positions(self):

        for widget in self.positions_frame.winfo_children():

            widget.destroy()

        positions = (
            self.controller.get_open_positions()
        )

        if not positions:

            label = ctk.CTkLabel(
                self.positions_frame,
                text="No open positions",
                font=("Segoe UI", 18)
            )

            label.pack(
                pady=50
            )

            return

        # ==================================================
        # Headers
        # ==================================================

        headers = [
            "Asset",
            "Action",
            "Entry",
            "Current",
            "P/L",
            "Stop Loss",
            "Take Profit",
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
                padx=8,
                pady=12,
                sticky="ew"
            )

        # ==================================================
        # Positions
        # ==================================================

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

            stop_loss = trade.get(
                "stop_loss"
            )

            take_profit = trade.get(
                "take_profit"
            )

            status = trade.get(
                "status",
                "-"
            )

            values = [
                asset,
                action,
                self.format_price(entry),
                self.format_price(current),
                self.format_pnl(profit_loss),
                self.format_price(stop_loss),
                self.format_price(take_profit),
                status
            ]

            for column, value in enumerate(values):

                label = ctk.CTkLabel(
                    self.positions_frame,
                    text=value,
                    font=("Segoe UI", 13)
                )

                label.grid(
                    row=row,
                    column=column,
                    padx=8,
                    pady=10,
                    sticky="ew"
                )

                # ------------------------------------------
                # P/L colour
                # ------------------------------------------

                if column == 4:

                    try:

                        pnl = float(
                            profit_loss
                        )

                        if pnl > 0:

                            label.configure(
                                text_color="green"
                            )

                        elif pnl < 0:

                            label.configure(
                                text_color="red"
                            )

                    except (
                        ValueError,
                        TypeError
                    ):

                        pass

    # ======================================================
    # Formatting
    # ======================================================

    def format_price(
        self,
        value
    ):

        if value is None:

            return "—"

        try:

            return f"£{float(value):,.2f}"

        except (
            ValueError,
            TypeError
        ):

            return "—"

    def format_pnl(
        self,
        value
    ):

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
            