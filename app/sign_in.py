import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from typing import Any
from database_utils import sign_in_supabase

class SignInScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        for i in range(3):
            self.rowconfigure(i, weight=1)

        self.label = ctk.CTkLabel(self, text="Sign in to Weighly", font=("Helvetica", 30))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.sign_in_button = ctk.CTkButton(self, text="Sign In", font=("Helvetica", 30), command=sign_in_supabase)
        self.sign_in_button.grid(row=1, column=0, padx=20, pady=20)