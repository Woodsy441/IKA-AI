import customtkinter as ctk


class IKADashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("IKA AI")
        self.geometry("1100x700")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # ==========================
        # Title
        # ==========================

        title = ctk.CTkLabel(
            self,
            text="IKA AI",
            font=("Arial", 34, "bold")
        )

        title.pack(pady=20)

        subtitle = ctk.CTkLabel(
            self,
            text="Intelligent Trading Assistant",
            font=("Arial", 18)
        )

        subtitle.pack()

        # ==========================
        # Account Frame
        # ==========================

        self.account_frame = ctk.CTkFrame(self)

        self.account_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.balance_label = ctk.CTkLabel(
            self.account_frame,
            text="Balance: £10,000",
            font=("Arial", 20)
        )

        self.balance_label.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        self.equity_label = ctk.CTkLabel(
            self.account_frame,
            text="Equity: £10,000",
            font=("Arial", 20)
        )

        self.equity_label.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        self.pnl_label = ctk.CTkLabel(
            self.account_frame,
            text="Open P/L: £0.00",
            font=("Arial", 20)
        )

        self.pnl_label.pack(
            anchor="w",
            padx=20,
            pady=10
        )

        # ==========================
        # Buttons
        # ==========================

        self.button_frame = ctk.CTkFrame(self)

        self.button_frame.pack(
            fill="x",
            padx=20,
            pady=20
        )

        self.scan_button = ctk.CTkButton(
            self.button_frame,
            text="Scan Markets"
        )

        self.scan_button.pack(
            side="left",
            padx=10,
            pady=15
        )

        self.refresh_button = ctk.CTkButton(
            self.button_frame,
            text="Refresh"
        )

        self.refresh_button.pack(
            side="left",
            padx=10,
            pady=15
        )

        self.history_button = ctk.CTkButton(
            self.button_frame,
            text="Trade History"
        )

        self.history_button.pack(
            side="left",
            padx=10,
            pady=15
        )
        