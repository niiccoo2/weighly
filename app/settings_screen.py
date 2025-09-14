import customtkinter as ctk
from json_utils import save_settings, load_settings

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        for i in range(8):
            self.columnconfigure(i, weight=1)
        
        for i in range(8):
            self.rowconfigure(i, weight=1)
        
        self.btn_back = ctk.CTkButton(
            self, text="Back to Main", 
            command=lambda: controller.show_frame("MainScreen")
        )
        self.btn_back.grid(row=0, column=0, columnspan=1, sticky="nw", pady=10, padx=10) # Change pady and padx to change with window size

        self.settings_label = ctk.CTkLabel(self, text="Settings", font=("Helvetica", 20))
        self.settings_label.grid(row=0, column=0, columnspan=8, sticky="n", pady=10)

        # Settings
        self.settings = load_settings()

        self.keep_name_label = ctk.CTkLabel(self, text="Keep name after submission:", font=("Helvetica", 20))
        self.keep_name_label.grid(row=1, column=1)

        def _update_keep_name_setting():
            print("keep_name_switch toggled, current value:", self.switch_var.get())
            self.settings["keep_name"] = self.switch_var.get()
            save_settings(self.settings)


        self.switch_var = ctk.BooleanVar(value=self.settings["keep_name"]) #init ctk var
        self.keep_name_switch = ctk.CTkSwitch(self, text="", command=_update_keep_name_setting,
                                 variable=self.switch_var, onvalue=True, offvalue=False)
        self.keep_name_switch.grid(row=1, column=2)