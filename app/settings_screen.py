import customtkinter as ctk

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

        self.keep_name_label = ctk.CTkLabel(self, text="Keep name after submission", font=("Helvetica", 20))
        self.keep_name_label.grid(row=1, column=1)

        def switch_event():
            print("switch toggled, current value:", self.switch_var.get())

        self.switch_var = ctk.StringVar(value="on")
        self.keep_name_switch = ctk.CTkSwitch(self, text="CTkSwitch", command=switch_event,
                                 variable=self.switch_var, onvalue="on", offvalue="off")
        self.keep_name_switch.grid(row=1, column=2)