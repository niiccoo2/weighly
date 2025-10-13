import customtkinter as ctk
import threading
import serial
import time
from database_utils import FILENAME
from json_utils import load_settings
from main_screen import MainScreen
from settings_screen import SettingsScreen
from sign_in import EventPicker, SignInScreen
from threads import update_running_total_thread, update_weight_thread


class Weighly(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.settings = load_settings()
        self.serial_connection: serial.Serial | None = None
        self.serial_lock = threading.Lock()  # Lock to protect serial access
        self.event_id: int | None = None

        ctk.set_appearance_mode("System")
        ctk.set_default_color_theme(self.settings["theme"])
        self.title("Weighly")
        self.geometry("1000x500")
        self.resizable(True, True)
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

        open(FILENAME, "a")  # make sure file exists

        # Dictionary to store frames
        self.frames = {}

        for F in (MainScreen, SettingsScreen, SignInScreen, EventPicker):
            frame = F(self, self)
            name = F.__name__
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("SignInScreen")
        self.connect_to_scale()

    def connect_to_scale(self):
        """Opens or re-opens the serial port based on current settings."""
        with self.serial_lock:  # Use the lock to prevent race conditions
            if self.serial_connection and self.serial_connection.is_open:
                self.serial_connection.close()

            if not self.settings.get("scale_mode"):
                print("Scale mode is disabled.")
                self.serial_connection = None
                return

            port = self.settings.get("SERIALPORT")
            baud = self.settings.get("BAUDRATE", 9600)
            try:
                print(f"Attempting to connect to scale at {port}...")
                self.serial_connection = serial.Serial(port, int(baud), timeout=0.5)
                time.sleep(0.1)
                print("Scale connected successfully.")
            except (serial.SerialException, ValueError) as e:
                print(f"Failed to connect to scale: {e}")
                self.serial_connection = None

    def on_closing(self):
        """Cleanly close the serial port when the app exits."""
        if self.serial_connection and self.serial_connection.is_open:
            print("Closing serial port.")
            self.serial_connection.close()
        self.destroy()

    def show_frame(self, frame_name):
        frame = self.frames[frame_name]

        # reload settings if returning to MainScreen
        if frame_name == "MainScreen":
            frame.reload()
        elif frame_name == "EventPicker":
            # Refresh the event list when showing the picker
            frame.refresh()

        frame.tkraise()


if __name__ == "__main__":
    weighly = Weighly()
    weighly.protocol("WM_DELETE_WINDOW", weighly.on_closing)

    threading.Thread(target=lambda: update_weight_thread(weighly), daemon=True).start()
    threading.Thread(
        target=lambda: update_running_total_thread(weighly), daemon=True
    ).start()

    main_frame = weighly.frames["MainScreen"]
    main_frame.adjust_font_size(0)
    main_frame.bind("<Configure>", main_frame.adjust_font_size)

    weighly.mainloop()