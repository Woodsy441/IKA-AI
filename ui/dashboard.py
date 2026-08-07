import customtkinter as ctk

from controllers.app_controller import AppController
from ui.account_frame import AccountFrame
from ui.scanner_frame import ScannerFrame


class IKADashboard(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("IKA AI")
        self.geometry("1400x850")

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # --------------------------
        # Controller
        # --------------------------

        self.controller = AppController()

        # --------------------------
        # Header
        # --------------------------

        title = ctk.CTkLabel(
            self,
            text="IKA AI",
            font=("Arial", 34, "bold")
        )
        title.pack(pady=(20, 5))

        subtitle = ctk.CTkLabel(
            self,
            text="Intelligent Trading Assistant",
            font=("Arial", 18)
        )
        subtitle.pack(pady=(0, 20))

        # --------------------------
        # Main Frame
        # --------------------------

        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # --------------------------
        # Sidebar
        # --------------------------

        self.menu_frame = ctk.CTkFrame(
            self.main_frame,
            width=220
        )

        self.menu_frame.pack(
            side="left",
            fill="y",
            padx=(15, 10),
            pady=15
        )

        menu_title = ctk.CTkLabel(
            self.menu_frame,
            text="Navigation",
            font=("Arial", 22, "bold")
        )

        menu_title.pack(pady=(20, 25))

        ctk.CTkButton(
            self.menu_frame,
            text="🏠 Dashboard"
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            self.menu_frame,
            text="📈 Scan Markets"
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            self.menu_frame,
            text="💼 Portfolio"
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            self.menu_frame,
            text="📜 Trade History"
        ).pack(fill="x", padx=20, pady=8)

        ctk.CTkButton(
            self.menu_frame,
            text="⚙ Settings"
        ).pack(fill="x", padx=20, pady=8)

        # --------------------------
        # Right Side
        # --------------------------

        self.content_frame = ctk.CTkFrame(self.main_frame)

        self.content_frame.pack(
            side="left",
            fill="both",
            expand=True,
            padx=(10, 15),
            pady=15
        )

        # --------------------------
        # Account
        # --------------------------

        self.account = AccountFrame(self.content_frame)

        self.account.pack(
            fill="x",
            padx=20,
            pady=20
        )

        # --------------------------
        # Scanner
        # --------------------------

        self.scanner = ScannerFrame(
            self.content_frame,
            self.controller
        )

        self.scanner.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )
        