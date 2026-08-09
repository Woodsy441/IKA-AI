import sys
from pathlib import Path

import customtkinter as ctk


# ==========================================================
# Make the original IKA_AI trading system available to v3
# ==========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from controllers.scanner_controller import ScannerController
from trading.paper_trader import open_trade
from trading.portfolio import trade_exists


class ScannerPage(ctk.CTkFrame):

    def __init__(self, master):

        super().__init__(master)

        self.controller = ScannerController()

        # ==================================================
        # Layout
        # ==================================================

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
            text="Market Scanner",
            font=("Segoe UI", 30, "bold")
        )

        title.grid(
            row=0,
            column=0,
            sticky="w",
            padx=15,
            pady=15
        )

        self.scan_button = ctk.CTkButton(
            header,
            text="🔄 Scan Markets",
            width=160,
            height=40,
            command=self.scan_markets
        )

        self.scan_button.grid(
            row=0,
            column=1,
            padx=15,
            pady=15
        )

        # ==================================================
        # Status
        # ==================================================

        self.status = ctk.CTkLabel(
            self,
            text="Ready to scan",
            anchor="w",
            font=("Segoe UI", 14)
        )

        self.status.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 10)
        )

        # ==================================================
        # Results
        # ==================================================

        self.results_frame = ctk.CTkScrollableFrame(
            self
        )

        self.results_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=20,
            pady=(0, 20)
        )

        for column in range(8):

            self.results_frame.grid_columnconfigure(
                column,
                weight=1
            )

        self.show_empty_state()

    # ======================================================
    # Scan Markets
    # ======================================================

    def scan_markets(self):

        self.scan_button.configure(
            state="disabled",
            text="Scanning..."
        )

        self.status.configure(
            text="Scanning markets..."
        )

        self.update_idletasks()

        try:

            results = self.controller.scan_markets()

            self.display_results(
                results
            )

            self.status.configure(
                text=f"Scan complete — {len(results)} results"
            )

        except Exception as error:

            self.status.configure(
                text="Scanner error"
            )

            self.show_error(
                error
            )

            print(
                "\nScanner error:"
            )

            print(error)

        finally:

            self.scan_button.configure(
                state="normal",
                text="🔄 Scan Markets"
            )

    # ======================================================
    # Display Results
    # ======================================================

    def display_results(self, results):

        for widget in self.results_frame.winfo_children():

            widget.destroy()

        if not results:

            self.show_empty_state()

            return

        headers = [
            "Asset",
            "Signal",
            "Score",
            "Price",
            "Stop Loss",
            "Take Profit",
            "Position Size",
            "Reasons"
        ]

        for column, header in enumerate(headers):

            label = ctk.CTkLabel(
                self.results_frame,
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

        for row, result in enumerate(
            results,
            start=1
        ):

            self.create_result_row(
                row,
                result
            )

    # ======================================================
    # Create Result Row
    # ======================================================

    def create_result_row(
        self,
        row,
        result
    ):

        asset = result.get(
            "asset",
            "Unknown"
        )

        rating = result.get(
            "rating",
            "UNKNOWN"
        )

        score = result.get(
            "score"
        )

        price = result.get(
            "price"
        )

        stop_loss = result.get(
            "stop_loss"
        )

        take_profit = result.get(
            "take_profit"
        )

        position_size = result.get(
            "position_size"
        )

        reasons = result.get(
            "reasons",
            []
        )

        if isinstance(
            reasons,
            list
        ):

            reasons_text = ", ".join(
                str(reason)
                for reason in reasons
            )

        else:

            reasons_text = str(
                reasons
            )

        if score is not None:

            score_text = f"{score}%"

        else:

            score_text = "—"

        values = [
            asset,
            rating,
            score_text,
            self.format_price(price),
            self.format_price(stop_loss),
            self.format_price(take_profit),
            self.format_number(position_size),
            reasons_text
        ]

        for column, value in enumerate(values):

            label = ctk.CTkLabel(
                self.results_frame,
                text=value,
                font=("Segoe UI", 13),
                wraplength=220,
                cursor="hand2"
            )

            label.grid(
                row=row,
                column=column,
                padx=8,
                pady=10,
                sticky="ew"
            )

            # ------------------------------------------
            # Signal colour
            # ------------------------------------------

            if column == 1:

                if rating == "BUY":

                    label.configure(
                        text_color="green"
                    )

                elif rating == "SELL":

                    label.configure(
                        text_color="red"
                    )

                elif rating == "HOLD":

                    label.configure(
                        text_color="orange"
                    )

            # ------------------------------------------
            # Clickable row
            # ------------------------------------------

            label.bind(
                "<Button-1>",
                lambda event, data=result:
                    self.open_trade_review(data)
            )

    # ======================================================
    # Trade Review
    # ======================================================

    def open_trade_review(
        self,
        result
    ):

        asset = result.get(
            "asset",
            "Unknown"
        )

        rating = result.get(
            "rating",
            "UNKNOWN"
        )

        price = result.get(
            "price"
        )

        stop_loss = result.get(
            "stop_loss"
        )

        take_profit = result.get(
            "take_profit"
        )

        position_size = result.get(
            "position_size"
        )

        reasons = result.get(
            "reasons",
            []
        )

        # ==================================================
        # Check existing trade
        # ==================================================

        already_open = False

        try:

            already_open = trade_exists(
                asset
            )

        except Exception as error:

            print(
                f"Could not check existing trade "
                f"for {asset}: {error}"
            )

        # ==================================================
        # Reasons
        # ==================================================

        reasons_text = "\n".join(
            f"• {reason}"
            for reason in reasons
        )

        # ==================================================
        # Review Window
        # ==================================================

        window = ctk.CTkToplevel(
            self
        )

        window.title(
            f"Trade Review — {asset}"
        )

        window.geometry(
            "600x700"
        )

        window.grab_set()

        # ==================================================
        # Title
        # ==================================================

        title = ctk.CTkLabel(
            window,
            text=asset,
            font=("Segoe UI", 32, "bold")
        )

        title.pack(
            pady=(30, 5)
        )

        # ==================================================
        # Signal
        # ==================================================

        signal = ctk.CTkLabel(
            window,
            text=rating,
            font=("Segoe UI", 26, "bold")
        )

        signal.pack(
            pady=10
        )

        if rating == "BUY":

            signal.configure(
                text_color="green"
            )

        elif rating == "SELL":

            signal.configure(
                text_color="red"
            )

        else:

            signal.configure(
                text_color="orange"
            )

        # ==================================================
        # Existing Trade Warning
        # ==================================================

        if already_open:

            warning = ctk.CTkLabel(
                window,
                text=(
                    "⚠ OPEN TRADE ALREADY EXISTS\n\n"
                    f"You already have an open {asset} position.\n"
                    "IKA AI will not create a duplicate trade."
                ),
                font=("Segoe UI", 15, "bold"),
                text_color="orange",
                justify="center"
            )

            warning.pack(
                padx=30,
                pady=15
            )

        # ==================================================
        # Trade Information
        # ==================================================

        info = ctk.CTkFrame(
            window
        )

        info.pack(
            fill="x",
            padx=40,
            pady=20
        )

        details = [
            (
                "Current Price",
                self.format_price(price)
            ),
            (
                "Stop Loss",
                self.format_price(stop_loss)
            ),
            (
                "Take Profit",
                self.format_price(take_profit)
            ),
            (
                "Position Size",
                self.format_number(position_size)
            )
        ]

        for name, value in details:

            row_frame = ctk.CTkFrame(
                info
            )

            row_frame.pack(
                fill="x",
                padx=15,
                pady=8
            )

            ctk.CTkLabel(
                row_frame,
                text=name,
                font=("Segoe UI", 15)
            ).pack(
                side="left"
            )

            ctk.CTkLabel(
                row_frame,
                text=value,
                font=("Segoe UI", 15, "bold")
            ).pack(
                side="right"
            )

        # ==================================================
        # Reasons
        # ==================================================

        reasons_title = ctk.CTkLabel(
            window,
            text="Why IKA AI likes this setup",
            font=("Segoe UI", 18, "bold")
        )

        reasons_title.pack(
            anchor="w",
            padx=40,
            pady=(10, 5)
        )

        reasons_label = ctk.CTkLabel(
            window,
            text=reasons_text or "No reasons supplied.",
            justify="left",
            anchor="w",
            font=("Segoe UI", 14)
        )

        reasons_label.pack(
            anchor="w",
            padx=50,
            pady=10
        )

        # ==================================================
        # Buttons
        # ==================================================

        button_frame = ctk.CTkFrame(
            window
        )

        button_frame.pack(
            fill="x",
            padx=40,
            pady=30
        )

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            command=window.destroy
        ).pack(
            side="left",
            expand=True,
            padx=10
        )

        # --------------------------------------------------
        # HOLD = no trade
        # --------------------------------------------------

        if rating == "HOLD":

            hold_button = ctk.CTkButton(
                button_frame,
                text="HOLD — No Trade",
                state="disabled"
            )

            hold_button.pack(
                side="right",
                expand=True,
                padx=10
            )

        # --------------------------------------------------
        # Existing trade = blocked
        # --------------------------------------------------

        elif already_open:

            blocked_button = ctk.CTkButton(
                button_frame,
                text="Trade Already Open",
                state="disabled"
            )

            blocked_button.pack(
                side="right",
                expand=True,
                padx=10
            )

        # --------------------------------------------------
        # New trade = allow paper trade
        # --------------------------------------------------

        else:

            paper_button = ctk.CTkButton(
                button_frame,
                text="Confirm Paper Trade",
                command=lambda:
                    self.confirm_paper_trade(
                        window,
                        result
                    )
            )

            paper_button.pack(
                side="right",
                expand=True,
                padx=10
            )

    # ======================================================
    # Confirm Paper Trade
    # ======================================================

    def confirm_paper_trade(
        self,
        window,
        result
    ):

        asset = result.get(
            "asset",
            "Unknown"
        )

        rating = result.get(
            "rating"
        )

        # ==================================================
        # Safety check
        # ==================================================

        if rating == "HOLD":

            self.show_trade_message(
                window,
                "No Trade",
                "IKA AI rated this asset HOLD."
            )

            return

        # ==================================================
        # Duplicate protection
        # ==================================================

        try:

            if trade_exists(asset):

                self.show_trade_message(
                    window,
                    "Trade Blocked",
                    (
                        f"{asset} already has "
                        "an open trade.\n\n"
                        "No duplicate position was created."
                    )
                )

                return

        except Exception as error:

            self.show_trade_message(
                window,
                "Trade Error",
                f"Could not verify portfolio:\n\n{error}"
            )

            return

        # ==================================================
        # Open Paper Trade
        # ==================================================

        try:

            trade = open_trade(
                result
            )

            if trade:

                print(
                    "\n=============================="
                )

                print(
                    "IKA AI PAPER TRADE OPENED"
                )

                print(
                    "=============================="
                )

                print(
                    f"Asset: {trade.get('asset')}"
                )

                print(
                    f"Action: {trade.get('action')}"
                )

                print(
                    f"Entry: {trade.get('entry')}"
                )

                print(
                    f"Stop Loss: {trade.get('stop_loss')}"
                )

                print(
                    f"Take Profit: {trade.get('take_profit')}"
                )

                print(
                    f"Position Size: "
                    f"{trade.get('position_size')}"
                )

                print(
                    "==============================\n"
                )

                self.show_trade_message(
                    window,
                    "Paper Trade Opened",
                    (
                        f"{asset} paper trade "
                        "has been successfully opened."
                    )
                )

                self.status.configure(
                    text=f"Paper trade opened — {asset}"
                )

            else:

                self.show_trade_message(
                    window,
                    "Trade Failed",
                    "The paper trader did not create a trade."
                )

        except Exception as error:

            print(
                "\nPaper trade error:"
            )

            print(error)

            self.show_trade_message(
                window,
                "Trade Error",
                f"Could not open paper trade:\n\n{error}"
            )

    # ======================================================
    # Trade Message
    # ======================================================

    def show_trade_message(
        self,
        window,
        title,
        message
    ):

        for widget in window.winfo_children():

            widget.destroy()

        window.title(
            title
        )

        label = ctk.CTkLabel(
            window,
            text=message,
            font=("Segoe UI", 17),
            justify="center",
            wraplength=500
        )

        label.pack(
            expand=True,
            padx=40,
            pady=40
        )

        button = ctk.CTkButton(
            window,
            text="Close",
            command=window.destroy
        )

        button.pack(
            pady=(0, 30)
        )

    # ======================================================
    # Empty State
    # ======================================================

    def show_empty_state(self):

        for widget in self.results_frame.winfo_children():

            widget.destroy()

        label = ctk.CTkLabel(
            self.results_frame,
            text=(
                "Click 'Scan Markets' "
                "to search for trading opportunities."
            ),
            font=("Segoe UI", 16)
        )

        label.grid(
            row=0,
            column=0,
            columnspan=8,
            pady=50
        )

    # ======================================================
    # Error
    # ======================================================

    def show_error(
        self,
        error
    ):

        for widget in self.results_frame.winfo_children():

            widget.destroy()

        label = ctk.CTkLabel(
            self.results_frame,
            text=f"Scanner error:\n{error}",
            font=("Segoe UI", 15),
            wraplength=800
        )

        label.grid(
            row=0,
            column=0,
            columnspan=8,
            pady=50
        )

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

    def format_number(
        self,
        value
    ):

        if value is None:

            return "—"

        try:

            return f"{float(value):,.2f}"

        except (
            ValueError,
            TypeError
        ):

            return "—"
            