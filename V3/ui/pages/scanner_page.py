import customtkinter as ctk


class ScannerPage(ctk.CTkFrame):

    def __init__(self, master):
        super().__init__(master)

        title = ctk.CTkLabel(
            self,
            text="Market Scanner",
            font=("Segoe UI", 30, "bold")
        )

        title.pack(anchor="w", padx=20, pady=20)

        button = ctk.CTkButton(
            self,
            text="Scan Markets"
        )

        button.pack(pady=20)

        textbox = ctk.CTkTextbox(self)

        textbox.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        textbox.insert(
            "1.0",
            "Scanner output will appear here..."
        )
        