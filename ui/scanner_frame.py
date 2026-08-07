import customtkinter as ctk


class ScannerFrame(ctk.CTkFrame):

    def __init__(self, master, controller):
        super().__init__(master)

        self.controller = controller

        self.configure(corner_radius=10)

        title = ctk.CTkLabel(
            self,
            text="Market Scanner",
            font=("Arial", 22, "bold")
        )
        title.pack(pady=(15, 10))

        self.scan_button = ctk.CTkButton(
            self,
            text="📈 Scan Markets",
            command=self.scan_markets
        )
        self.scan_button.pack(pady=10)

        self.results_box = ctk.CTkTextbox(
            self,
            width=800,
            height=400
        )
        self.results_box.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def scan_markets(self):

        self.results_box.delete("1.0", "end")

        self.results_box.insert(
            "end",
            "Scanning markets...\n\n"
        )

        results = self.controller.scan()

        for result in results:

            line = (
                f"{result['asset']:12}"
                f"{result['rating']:8}"
                f"{result['score']}%\n"
            )

            self.results_box.insert("end", line)
            