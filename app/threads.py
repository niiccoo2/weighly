import time
from database_utils import read_running_total
import customtkinter as ctk

def update_weight_thread(weighly):
    main_screen = weighly.frames["MainScreen"]
    scale_mode: bool = main_screen.settings["scale_mode"]
    
    if not scale_mode:
        return

    while scale_mode:
        scale_mode = main_screen.settings["scale_mode"]
        # Get the weight from the scale
        raw_weight = main_screen.get_serial(main_screen.settings["SERIALPORT"], main_screen.settings["BAUDRATE"], "W")

        # Store raw weight for precision (before any rounding or unit conversion)
        main_screen.raw_weight = raw_weight

        # Capture the current widget reference and weight in the lambda
        weight_widget = main_screen.weight

        # convert to kg if in kg mode and round for display
        display_weight = raw_weight
        if main_screen.settings["unit"] == "kg":
            display_weight = display_weight*0.45359237
        
        display_weight = round(display_weight, 2)

        if main_screen.settings["unit"] == "kg":
            unit = "kgs."
        else:
            unit = "lbs."

        # Need to find a way to make this say kg if it is kg
        def update_widget(w=weight_widget, wt=display_weight):
            if isinstance(w, ctk.CTkLabel):
                w.configure(text=f"{wt} {unit}")
            else:  # fallback if somehow it's an Entry
                w.delete(0, "end")
                w.insert(0, f"{wt} {unit}")

        # Schedule the update on the main thread
        main_screen.after(0, update_widget)

        time.sleep(1)

def update_running_total_thread(weighly):
    while True:
        try:
            total = read_running_total(1)
            weighly.frames["MainScreen"].after(0, lambda: weighly.frames["MainScreen"].running_total.set(str(round(total, 2))))
        except Exception as e:
            print("Error updating total:", e)
        time.sleep(10)