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
        weight = main_screen.get_serial(main_screen.settings["SERIALPORT"], main_screen.settings["BAUDRATE"], "W")

        # Capture the current widget reference and weight in the lambda
        weight_widget = main_screen.weight

        # convert to kg if in kg mode
        if main_screen.settings["unit"] == "kg":
            weight = weight*0.45359237
        
        weight = round(weight, 2)

        def update_widget(w=weight_widget, wt=weight):
            if isinstance(w, ctk.CTkLabel):
                w.configure(text=f"{wt} lbs.")
            else:  # fallback if somehow it's an Entry
                w.delete(0, "end")
                w.insert(0, f"{wt} lbs.")

        # Schedule the update on the main thread
        main_screen.after(0, update_widget)

        time.sleep(1)

def update_running_total_thread(weighly):
    while True:
        try:
            total = read_running_total(1)
            weighly.frames["MainScreen"].after(0, lambda: weighly.frames["MainScreen"].running_total.set(str(total)))
        except Exception as e:
            print("Error updating total:", e)
        time.sleep(10)