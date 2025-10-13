import customtkinter as ctk
import threading
from database_utils import FILENAME
from main_screen import MainScreen
from settings_screen import SettingsScreen
from sign_in import SignInScreen, EventPicker
from json_utils import load_settings
from threads import update_running_total_thread, update_weight_thread

class Weighly(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme(self.settings["theme"])
        self.title('Weighly')
        self.geometry('1000x500')
        self.resizable(True, True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        self.event_id: int | None = None

        # Should delete this junk
        # self.SERIALPORT = "/dev/ttyUSB0"
        # self.BAUDRATE = 9600 # Not needed when reading from settings

        # self.SERIALPORT = self.settings["SERIALPORT"] # I don't think we ever use this
        # self.BAUDRATE = self.settings["BAUDRATE"]     # 90% sure we always read stright from settings


        open(FILENAME, "a")  # make sure file exists

        # Dictionary to store frames
        self.frames = {}

        for F in (MainScreen, SettingsScreen, SignInScreen, EventPicker):
            frame = F(self, self)
            name = F.__name__
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SignInScreen")
    
    def show_frame(self, frame_name):
        frame = self.frames[frame_name]
        
        # reload settings if returning to MainScreen
        if frame_name == "MainScreen":
            frame.reload()
        if frame_name == "EventPicker" and hasattr(frame, "refresh"):
            frame.refresh()

        frame.tkraise()


if __name__ == "__main__":
    weighly = Weighly()

    threading.Thread(target= lambda: update_weight_thread(weighly), daemon=True).start()
    threading.Thread(target= lambda: update_running_total_thread(weighly), daemon=True).start()

    main_frame = weighly.frames["MainScreen"]
    main_frame.adjust_font_size(0)
    main_frame.bind("<Configure>", main_frame.adjust_font_size)

    weighly.mainloop()