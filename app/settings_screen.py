import customtkinter as ctk

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Settings Screen", font=("Helvetica", 40))
        self.label.pack(pady=50)

        self.btn_to_main = ctk.CTkButton(
            self, text="Back to Main", 
            command=lambda: controller.show_frame("MainScreen")
        )
        self.btn_to_main.pack()