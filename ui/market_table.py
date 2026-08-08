import tkinter as tk
from tkinter import ttk


class MarketTable(ttk.Treeview):
    """
    Reusable table used throughout IKA AI.

    This table is shared by:
        • Market Scanner
        • Portfolio
        • Trade History
    """

    def __init__(self, master):

        columns = (
            "Asset",
            "Signal",
            "Score",
            "Price",
            "Stop Loss",
            "Take Profit",
        )

        super().__init__(
            master,
            columns=columns,
            show="headings",
            height=15
        )

        style = ttk.Style()

        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1f1f1f",
            foreground="white",
            fieldbackground="#1f1f1f",
            rowheight=30,
            borderwidth=0,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#2b2b2b",
            foreground="white",
            relief="flat",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#1f6aa5")]
        )

        headings = {
            "Asset": 140,
            "Signal": 90,
            "Score": 80,
            "Price": 110,
            "Stop Loss": 120,
            "Take Profit": 120,
        }

        for heading, width in headings.items():
            self.heading(heading, text=heading)
            self.column(
                heading,
                width=width,
                anchor="center",
                stretch=True
            )

        self.tag_configure("BUY", foreground="#4CAF50")
        self.tag_configure("HOLD", foreground="#FFC107")
        self.tag_configure("SELL", foreground="#F44336")

    def clear(self):
        """Remove every row."""
        for row in self.get_children():
            self.delete(row)

    def populate(self, trades):
        """Populate the table with scanner results."""

        self.clear()

        for trade in trades:

            signal = trade["rating"]

            self.insert(
                "",
                "end",
                values=(
                    trade["asset"],
                    signal,
                    f"{trade['score']}%",
                    f"£{trade['price']:,.2f}",
                    f"£{trade['stop_loss']:,.2f}",
                    f"£{trade['take_profit']:,.2f}",
                ),
                tags=(signal,)
            )
            