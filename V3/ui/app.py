import customtkinter as ctk

from app_config import (
    APP_NAME,
    VERSION,
    WINDOW_WIDTH,
    WINDOW_HEIGHT,
    MIN_WIDTH,
    MIN_HEIGHT,
)

from ui.theme import load_theme

from ui.pages.dashboard_page import DashboardPage
from ui.pages.scanner_page import ScannerPage
from ui.pages.portfolio_page import PortfolioPage


class IKAApp(ctk.CTk):

    def __init__(self):

        super().__init__()

        load_theme()

        self.title(
            f"{APP_NAME} {VERSION}"
        )

        self.geometry(
            f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}"
        )

        self.minsize(
            MIN_WIDTH,
            MIN_HEIGHT
        )

        # -----------------------------------------
        # Main window layout
        # -----------------------------------------

        self.grid_columnconfigure(
            1,
            weight=1
        )

        self.grid_rowconfigure(
            0,
            weight=1
        )

        # -----------------------------------------
        # Sidebar
        # -----------------------------------------

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.sidebar.grid(
            row=0,
            column=0,
            sticky="ns"
        )

        logo = ctk.CTkLabel(
            self.sidebar,
            text="IKA AI",
            font=("Segoe UI", 28, "bold")
        )

        logo.pack(
            pady=(30, 5)
        )

        subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Trading Platform",
            font=("Segoe UI", 14)
        )

        subtitle.pack(
            pady=(0, 30)
        )

        # -----------------------------------------
        # Navigation
        # -----------------------------------------

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="🏠 Dashboard",
            command=self.show_dashboard
        )

        self.dashboard_button.pack(
            fill="x",
            padx=15,
            pady=6
        )

        self.scanner_button = ctk.CTkButton(
            self.sidebar,
            text="📈 Scanner",
            command=self.show_scanner
        )

        self.scanner_button.pack(
            fill="x",
            padx=15,
            pady=6
        )

        self.portfolio_button = ctk.CTkButton(
            self.sidebar,
            text="💼 Portfolio",
            command=self.show_portfolio
        )

        self.portfolio_button.pack(
            fill="x",
            padx=15,
            pady=6
        )

        self.history_button = ctk.CTkButton(
            self.sidebar,
            text="📜 History",
            state="disabled"
        )

        self.history_button.pack(
            fill="x",
            padx=15,
            pady=6
        )

        self.watchlist_button = ctk.CTkButton(
            self.sidebar,
            text="⭐ Watchlist",
            state="disabled"
        )

        self.watchlist_button.pack(
            fill="x",
            padx=15,
            pady=6
        )

        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="⚙ Settings",
            state="disabled"
        )

        self.settings_button.pack(
            fill="x",
            padx=15,
            pady=6
        )

        # -----------------------------------------
        # Main content
        # -----------------------------------------

        self.main = ctk.CTkFrame(
            self
        )

        self.main.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=15,
            pady=15
        )

        self.main.grid_rowconfigure(
            0,
            weight=1
        )

        self.main.grid_columnconfigure(
            0,
            weight=1
        )

        # -----------------------------------------
        # Pages
        # -----------------------------------------

        self.dashboard_page = DashboardPage(
            self.main
        )

        self.scanner_page = ScannerPage(
            self.main
        )

        self.portfolio_page = PortfolioPage(
            self.main
        )

        # -----------------------------------------
        # Status bar
        # -----------------------------------------

        self.status = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            height=28
        )

        self.status.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="ew",
            padx=10,
            pady=(0, 5)
        )

        # Start on dashboard
        self.show_dashboard()

    # =============================================
    # Page management
    # =============================================

    def clear_pages(self):

        for widget in self.main.winfo_children():

            widget.grid_forget()

    # =============================================
    # Dashboard
    # =============================================

    def show_dashboard(self):

        self.clear_pages()

        self.dashboard_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.status.configure(
            text="Dashboard loaded"
        )

    # =============================================
    # Scanner
    # =============================================

    def show_scanner(self):

        self.clear_pages()

        self.scanner_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.status.configure(
            text="Scanner loaded"
        )

    # =============================================
    # Portfolio
    # =============================================

    def show_portfolio(self):

        self.clear_pages()

        self.portfolio_page.refresh()

        self.portfolio_page.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.status.configure(
            text="Portfolio loaded"
        )
        