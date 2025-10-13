import time
from scale_utils import get_serial
import serial
from database_utils import read_running_total
import customtkinter as ctk

def update_weight_thread(weighly):
    main_screen = weighly.frames["MainScreen"]
    
    while True:
        scale_mode = weighly.settings.get("scale_mode")
        if not scale_mode:
            time.sleep(1)
            continue

        raw_weight = get_serial(weighly.serial_connection, "W")

        if not isinstance(raw_weight, float):
            raw_weight = 0.0
        
        main_screen.raw_weight = raw_weight

        weight_widget = main_screen.weight
        display_weight = raw_weight
        if main_screen.settings["unit"] == "kg":
            display_weight = display_weight * 0.45359237
        
        display_weight = round(display_weight, 2)

        if main_screen.settings["unit"] == "kg":
            unit = "kgs."
        else:
            unit = "lbs."

        def update_widget(w=weight_widget, wt=display_weight):
            if isinstance(w, ctk.CTkLabel):
                w.configure(text=f"{wt} {unit}")
            else:
                w.delete(0, "end")
                w.insert(0, f"{wt} {unit}")

        main_screen.after(0, update_widget)
        time.sleep(1)

def update_running_total_thread(weighly):
    while True:
        try:
            total = read_running_total(weighly.event_id)  # Use the event_id from the main application
            weighly.frames["MainScreen"].after(0, lambda: weighly.frames["MainScreen"].running_total.set(str(round(total, 2))))
        except Exception as e:
            print("Error updating total:", e)
        time.sleep(5)