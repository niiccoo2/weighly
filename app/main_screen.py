import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from scale_utils import get_serial, get_serial_dummy
from database_utils import save_weight
from json_utils import load_settings
from threads import update_weight_thread
from typing import Any

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.settings = load_settings()

        self.current_font_size = 0
        self.use_dummy_scale = True # Remove this once the ability to enter weight is added

        if self.use_dummy_scale:
            self.get_serial = get_serial_dummy
        else:
            self.get_serial = get_serial

        for i in range(3):
            self.columnconfigure(i, weight=1)
        
        for i in range(6):
            self.rowconfigure(i, weight=1)
        

        #self.name = ctk.StringVar(self)
        #self.weight_TKvar = ctk.StringVar(self)
        #self.saved_weight = ctk.DoubleVar(self) # Might be able to remove this
        self.person_type = ctk.StringVar(self, "Scout")
        self.running_total = ctk.StringVar(self)

        # Buttons

        self.btnSettings = ctk.CTkButton(
            self, 
            text="Settings", 
            font=("Helvetica", 20), 
            command=lambda: controller.show_frame("SettingsScreen"))
        self.btnSettings.grid(row=0, column=2, columnspan=1, rowspan=1)

        self.btnSaveToFile = ctk.CTkButton(
            self, 
            text="Save To File", 
            font=("Helvetica", 60), 
            command=lambda: save_weight(1, # Might want to change this to first run a function that makes sure all the inputs are correct
                                        self.NameEntry.get() if self.settings["keep_name"] else self._clear_name_input(),
                                        self.get_current_weight(),
                                        self.person_type.get()))
            # self.name.get() will NOT clear the name
        self.btnSaveToFile.grid(row=4, column=2, columnspan=1, rowspan=3)

        self.btnTare = ctk.CTkButton(
            self, 
            text="Tare", 
            font=("Helvetica", 20),
            command=self.tare_scale)
        self.btnTare.grid(row=3, column=2, columnspan=1, rowspan=3)

        if self.settings["scale_mode"] == True:
            self.weight = ctk.CTkLabel(
                self, 
                text="",
                font=("Helvetica", 200))
            self.weight.grid(row=1, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10, pady=10)
        else:
            vcmd = self.register(self._only_numbers)
            self.weight = ctk.CTkEntry(
                self, 
                font=("Helvetica", 60), 
                width=300, 
                height=60,
                placeholder_text="Weight",
                validate="key",
                validatecommand=(vcmd, "%P"))
            self.weight.grid(row=2, column=1, columnspan=1, rowspan=3)

        self.running_total_label = ctk.CTkLabel(
            self, 
            textvariable=self.running_total, 
            font=("Helvetica", 60))
        self.running_total_label.grid(row=3, column=2, columnspan=1, rowspan=1)

        # self.max_on_scale = ctk.CTkLabel( # Don't need this because this should be a warning on the scale itself...
        #     self,                         # If we want to add it tho you need to use .grid to give it a spot to show
        #     text=("200 lbs. maximum on scale."), 
        #     font=("Helvetica", 40))
        
        self.NameEntry = ctk.CTkEntry(
            self, 
            font=("Helvetica", 60), 
            width=300, 
            height=60,
            placeholder_text="Name")
        self.NameEntry.grid(row=4, column=1, columnspan=1, rowspan=3)

        self.r1 = ctk.CTkRadioButton(
            self, 
            text="Scout", 
            font=("Helvetica", 20), 
            value="Scout", 
            variable=self.person_type)
        self.r1.grid(row=3, column=0, rowspan=1)

        self.r2 = ctk.CTkRadioButton(
            self, 
            text="Webelo", 
            font=("Helvetica", 20), 
            value="Webelo", 
            variable=self.person_type)
        self.r2.grid(row=4, column=0, rowspan=1)

        self.r3 = ctk.CTkRadioButton(
            self, 
            text="Other", 
            font=("Helvetica", 20), 
            value="Other", 
            variable=self.person_type)
        self.r3.grid(row=5, column=0, rowspan=1)
    
    def adjust_font_size(self, event=None):
        new_font_size = max(20, min(int((self.winfo_width() + self.winfo_height()) // 50), 100))

        if new_font_size != self.current_font_size:
            self.btnSaveToFile.configure(font=("Helvetica", new_font_size // 1.5))
            self.btnTare.configure(font=("Helvetica", new_font_size // 1.5))
            self.btnSettings.configure(font=("Helvetica", new_font_size // 1.5))
            self.weight.configure(font=("Helvetica", new_font_size))
            self.running_total_label.configure(font=("Helvetica", new_font_size))
            #self.max_on_scale.configure(font=("Helvetica", int(new_font_size // 1.3)))
            self.NameEntry.configure(font=("Helvetica", new_font_size))
            self.r1.configure(font=("Helvetica", new_font_size // 2))
            self.r2.configure(font=("Helvetica", new_font_size // 2))
            self.r3.configure(font=("Helvetica", new_font_size // 2))
        
    def tare_scale(self):
        self.get_serial(self.settings["SERIALPORT"], self.settings["BAUDRATE"], "x")
        
        self.get_serial(self.settings["SERIALPORT"], self.settings["BAUDRATE"], "1")
        
        self.get_serial(self.settings["SERIALPORT"], self.settings["BAUDRATE"], "x")
    
    def _clear_name_input(self):
        name = self.NameEntry.get()
        self.NameEntry.delete(0, "end")
        return name
    
    
    def _only_numbers(self, new_value):
        # Allow empty string so user can delete everything
        if new_value == "":
            return True
        # Return True only if new_value is digits
        return new_value.isdigit()
    
    def reload(self):
        self.settings = load_settings()
        print("Reloaded settings:", self.settings)

        if hasattr(self, "weight"):
            self.weight.destroy()
        
        # Make correct weight element
        if self.settings["scale_mode"]:
            self.weight = ctk.CTkLabel(
                self, 
                text="",
                font=("Helvetica", 200))
            self.weight.grid(row=1, column=0, columnspan=3, rowspan=2, sticky="nsew", padx=10, pady=10)
        else:
            vcmd = self.register(self._only_numbers)
            self.weight = ctk.CTkEntry(
                self, 
                font=("Helvetica", 60), 
                width=300, 
                height=60,
                placeholder_text="Weight",
                validate="key",
                validatecommand=(vcmd, "%P"))
            self.weight.grid(row=2, column=1, columnspan=1, rowspan=3)
        
        # Clear current weight element
        if isinstance(self.weight, ctk.CTkLabel):
            self.weight.configure(text="")
        else:  # fallback if somehow it's an Entry
            self.weight.delete(0, "end")
            self.weight.insert(0, "")
        
        # Make sure everything is correct size
        self.adjust_font_size()

        # Restart scale update thread if scale_mode
        if self.settings["scale_mode"]:
            threading.Thread(target= lambda: update_weight_thread(self.controller), daemon=True).start()
    
    def get_current_weight(self):
        self.weight: Any
        if self.settings["scale_mode"]:
            return float(self.weight.cget("text").replace(" lbs.", ""))
        else:
            if not self.weight.get().replace(" lbs.", "").isdigit():
                CTkMessagebox(
                    title="Error", 
                    message="Error, weight must be a number. Saved as 0.",
                    icon="cancel"
                )
                return 0
            else:
                weight = float(self.weight.get().replace(" lbs.", ""))
                self.NameEntry.delete(0, "end")
                return weight

