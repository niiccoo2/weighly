import customtkinter as ctk

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        for i in range(4):
            self.columnconfigure(i, weight=1)
        
        for i in range(6):
            self.rowconfigure(i, weight=1)
        

        self.label = ctk.CTkLabel(self, text="Settings Screen", font=("Helvetica", 40))
        

        self.btn_to_main = ctk.CTkButton(
            self, text="Back to Main", 
            command=lambda: controller.show_frame("MainScreen")
        )
        