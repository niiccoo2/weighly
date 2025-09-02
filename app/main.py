import customtkinter as ctk
import threading
import time
from scale_utils import get_serial, get_serial_dummy
from database_utils import save_weight, read_running_total, FILENAME

class Weighly(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        self.title('Weighly')
        self.geometry('1000x500')
        self.resizable(True, True)

        self.SERIALPORT = "/dev/ttyUSB0"
        self.BAUDRATE = 9600

        open(FILENAME, "a")  # make sure file exists

        # Dictionary to store frames
        self.frames = {}

        for F in (MainScreen, SettingsScreen):
            frame = F(self, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(MainScreen)
    
    def show_frame(self, frame_class):
        frame = self.frames[frame_class]
        frame.tkraise()

def update_scale_thread():
    while True:
        weight = weighly.frames[MainScreen].get_serial(weighly.SERIALPORT, weighly.BAUDRATE, "W")
        weighly.frames[MainScreen].after(0, lambda: weighly.frames[MainScreen].weight_TKvar.set(f"{weight:>4} lbs."))
        time.sleep(1)

def update_running_total_thread():
    while True:
        try:
            total = read_running_total(1)
            weighly.frames[MainScreen].after(0, lambda: weighly.frames[MainScreen].running_total.set(str(total)))
        except Exception as e:
            print("Error updating total:", e)
        time.sleep(10)

class MainScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.current_font_size = 0
        self.use_dummy_scale = True # Remove this once the ability to enter weight is added

        if self.use_dummy_scale:
            self.get_serial = get_serial_dummy
        else:
            self.get_serial = get_serial

        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)
        self.rowconfigure(4, weight=1)
        self.rowconfigure(5, weight=1)

        self.name = ctk.StringVar(self)
        self.weight_TKvar = ctk.StringVar(self)
        self.saved_weight = ctk.DoubleVar(self) # Might be able to remove this
        self.person_type = ctk.StringVar(self, "Scout")
        self.running_total = ctk.StringVar(self)

        # Buttons

        self.btnSettings = ctk.CTkButton(
            self, 
            text="Settings", 
            font=("Helvetica", 20), 
            command=lambda: controller.show_frame(SettingsScreen))
        self.btnSettings.grid(row=0, column=2, columnspan=1, rowspan=1)

        self.btnSaveToFile = ctk.CTkButton(
            self, 
            text="Save To File", 
            font=("Helvetica", 60), 
            command=lambda: save_weight(1, self.name.get(), float(self.weight_TKvar.get().replace(" lbs.", "")), self.person_type.get()))
        self.btnSaveToFile.grid(row=4, column=2, columnspan=1, rowspan=3)

        self.btnTare = ctk.CTkButton(
            self, 
            text="Tare", 
            font=("Helvetica", 20), 
            command=self.tare_scale)
        self.btnTare.grid(row=3, column=2, columnspan=1, rowspan=3)

        self.weight_label = ctk.CTkLabel(
            self, 
            textvariable=self.weight_TKvar,
            font=("Helvetica", 200))
        self.weight_label.grid(row=0, column=0, columnspan=3, rowspan=3, sticky="nsew", padx=10, pady=10)

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
            textvariable=self.name, 
            font=("Helvetica", 60), 
            width=300, 
            height=60)
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
            self.btnSaveToFile.configure(font=("Helvetica", int(new_font_size // 1.5)))
            self.btnTare.configure(font=("Helvetica", new_font_size // 1.5))
            self.weight_label.configure(font=("Helvetica", new_font_size))
            self.running_total_label.configure(font=("Helvetica", new_font_size))
            #self.max_on_scale.configure(font=("Helvetica", int(new_font_size // 1.3)))
            self.NameEntry.configure(font=("Helvetica", new_font_size))
            self.r1.configure(font=("Helvetica", new_font_size // 2))
            self.r2.configure(font=("Helvetica", new_font_size // 2))
            self.r3.configure(font=("Helvetica", new_font_size // 2))
        
    def tare_scale(self):
        self.get_serial(self.controller.SERIALPORT, self.controller.BAUDRATE, "x")
        
        self.get_serial(self.controller.SERIALPORT, self.controller.BAUDRATE, "1")
        
        self.get_serial(self.controller.SERIALPORT, self.controller.BAUDRATE, "x")

class SettingsScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.label = ctk.CTkLabel(self, text="Settings Screen", font=("Helvetica", 40))
        self.label.pack(pady=50)

        self.btn_to_main = ctk.CTkButton(
            self, text="Back to Main", 
            command=lambda: controller.show_frame(MainScreen)
        )
        self.btn_to_main.pack()


if __name__ == "__main__":
    weighly = Weighly()

    threading.Thread(target=update_scale_thread, daemon=True).start()
    threading.Thread(target=update_running_total_thread, daemon=True).start()

    main_frame = weighly.frames[MainScreen]
    main_frame.adjust_font_size(0)
    main_frame.bind("<Configure>", main_frame.adjust_font_size)

    weighly.mainloop()