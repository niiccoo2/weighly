import customtkinter as ctk
import threading
import time
from database_utils import read_running_total, FILENAME
from main_screen import MainScreen
from settings_screen import SettingsScreen
from json_utils import load_settings, save_settings

class Weighly(ctk.CTk):
    def __init__(self):
        super().__init__()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme("dark-blue")
        self.title('Weighly')
        self.geometry('1000x500')
        self.resizable(True, True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        # self.SERIALPORT = "/dev/ttyUSB0"
        # self.BAUDRATE = 9600 # Not needed when reading from settings

        self.settings = load_settings()
        self.SERIALPORT = self.settings["SERIALPORT"]
        self.BAUDRATE = self.settings["BAUDRATE"]


        open(FILENAME, "a")  # make sure file exists

        # Dictionary to store frames
        self.frames = {}

        for F in (MainScreen, SettingsScreen):
            frame = F(self, self)
            name = F.__name__
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("MainScreen")
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        
        # reload settings if returning to MainScreen
        if frame_name == "MainScreen":
            frame.reload()

        frame.tkraise()

def update_scale_thread():
    scale_mode = weighly.frames["MainScreen"].settings["scale_mode"]
    if scale_mode:
        while True:
            
            weight = weighly.frames["MainScreen"].get_serial(weighly.SERIALPORT, weighly.BAUDRATE, "W")

            weighly.frames["MainScreen"].after(0, lambda: weighly.frames["MainScreen"].weight.configure(text=f"{weight} lbs."))
            # Was trying to get the weight to be centered ^^^

            time.sleep(1)
    return

def update_running_total_thread():
    while True:
        try:
            total = read_running_total(1)
            weighly.frames["MainScreen"].after(0, lambda: weighly.frames["MainScreen"].running_total.set(str(total)))
        except Exception as e:
            print("Error updating total:", e)
        time.sleep(10)




if __name__ == "__main__":
    weighly = Weighly()

    threading.Thread(target=update_scale_thread, daemon=True).start()
    threading.Thread(target=update_running_total_thread, daemon=True).start()

    main_frame = weighly.frames["MainScreen"]
    main_frame.adjust_font_size(0)
    main_frame.bind("<Configure>", main_frame.adjust_font_size)

    weighly.mainloop()