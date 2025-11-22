import time
from scale_utils import get_serial
import serial
from database_utils import read_running_total
import customtkinter as ctk

def update_weight_thread(weighly):
    main_screen = weighly.frames["MainScreen"]
    
    while True:
        # --- Solution: Wait for the activation signal ---
        weighly.weight_thread_active.wait()

        scale_mode = weighly.settings.get("scale_mode")
        if not scale_mode:
            time.sleep(1)
            continue

        raw_weight = get_serial(weighly.serial_connection, weighly.serial_lock, "W")

        # --- Gracefully handle no data without setting to 0 ---
        if not isinstance(raw_weight, float):
            # If we get None, just loop again without updating the UI
            time.sleep(0.5)
            continue
        
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
            # Also check if the widget still exists before configuring it
            if w.winfo_exists() and isinstance(w, ctk.CTkLabel):
                w.configure(text=f"{wt} {unit}")

        # Schedule the UI update on the main thread
        main_screen.after(0, update_widget)
        time.sleep(.4)

def update_running_total_thread(weighly):
    while True:
        # --- Solution: Wait for the activation signal ---
        weighly.total_thread_active.wait()
        
        try:
            if weighly.event_id is not None:
                total = read_running_total(weighly.event_id)
                # Check if the frame and its variable still exist before updating
                if weighly.frames["MainScreen"].winfo_exists():
                    weighly.frames["MainScreen"].after(0, lambda: weighly.frames["MainScreen"].running_total.set(str(round(total, 2))))
        except Exception as e:
            print("Error updating total:", e)
        time.sleep(5)