import customtkinter as ctk

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        for i in range(8):
            self.columnconfigure(i, weight=1)
        
        for i in range(6):
            self.rowconfigure(i, weight=1)
        
        self.btn_back = ctk.CTkButton(
            self, text="Back to Main", 
            command=lambda: controller.show_frame("MainScreen")
        )
        self.btn_back.grid(row=0, column=0)

        self.settings_label = ctk.CTkLabel(self, text="Settings", font=("Helvetica", 20))
        self.settings_label.grid(row=0, column=3)

        self.keep_name_label = ctk.CTkLabel(self, text="Keep name after submission", font=("Helvetica", 20))
        self.keep_name_label.grid(row=1, column=2)