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

        # keep_name
        self.keep_name_label = ctk.CTkLabel(self, text="Keep name after submission:", font=("Helvetica", 20))
        self.keep_name_label.grid(row=1, column=1)

        self.keep_name_switch_var = ctk.BooleanVar(value=self.settings["keep_name"]) #init ctk var
        self.keep_name_switch = ctk.CTkSwitch(self,
                                               text="",
                                               command= lambda: self._update_setting(self.settings,
                                                                                     "keep_name",
                                                                                     self.keep_name_switch_var),
                                               variable=self.keep_name_switch_var,
                                               onvalue=True, 
                                               offvalue=False)
        self.keep_name_switch.grid(row=1, column=2)

        # scale_mode
        self.scale_mode_label = ctk.CTkLabel(self, text="Use USB scale:", font=("Helvetica", 20))
        self.scale_mode_label.grid(row=2, column=1)

        self.scale_mode_switch_var = ctk.BooleanVar(value=self.settings["scale_mode"]) #init ctk var
        self.scale_mode_switch = ctk.CTkSwitch(self,
                                               text="",
                                               command= lambda: self._update_setting(self.settings,
                                                                                     "scale_mode",
                                                                                     self.scale_mode_switch_var),
                                               variable=self.scale_mode_switch_var,
                                               onvalue=True, 
                                               offvalue=False)
        self.scale_mode_switch.grid(row=2, column=2)

        # port

        self.port_label = ctk.CTkLabel(self, text="Scale port:", font=("Helvetica", 20))
        self.port_label.grid(row=3, column=1)

        self.port_var = ctk.StringVar(value=self.settings["SERIALPORT"]) #init ctk var
        self.port_dropdown = ctk.CTkOptionMenu(self,
                                               values=["/dev/ttyUSB0", "/dev/ttyUSB1", "COM1", "COM2"],
                                               command= lambda _: self._update_setting(self.settings,
                                                                                         "SERIALPORT",
                                                                                         self.port_var),
                                               # the _ above is because when it runs the cmd, it passes a var,
                                               # in this case thats the selected item, but we dont need that,
                                               # but we still need to do something with it, or else it gets mad
                                               # so we assign it to _ and do nothing with it
                                               variable=self.port_var)
        self.port_dropdown.grid(row=3, column=2)

        # baud rate
        # stuff goes here

    def _update_setting(self, settings, setting_to_change: str, value_to_change_to):
            print(f"{setting_to_change} toggled, current value:", value_to_change_to.get())
            settings[setting_to_change] = value_to_change_to.get()
            save_settings(self.settings)