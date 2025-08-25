import tkinter as tk
import customtkinter
from scale_utils import get_serial, get_serial_dummy
from database_utils import write_to_file

use_dummy_scale = True # Remove this once the ability to enter weight is added

if use_dummy_scale:
    get_serial = get_serial_dummy

SERIALPORT = "/dev/ttyUSB0"  #Real Sparfun Open Scale
#SERIALPORT = "/dev/ttyACM0"  #Dummy Sparfun Open Scale on Arduino
BAUDRATE = 9600
FILENAME="./weighly_backup.csv"


open(FILENAME, "a")

ctk = customtkinter.CTk()
customtkinter.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
customtkinter.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"
ctk.geometry('1000x500')
ctk.resizable(True, True)
ctk.title('Weighly')

ctk.columnconfigure(0, weight=1)
ctk.columnconfigure(1, weight=1)
ctk.columnconfigure(2, weight=1)
ctk.rowconfigure(0, weight=1)
ctk.rowconfigure(1, weight=1)
ctk.rowconfigure(2, weight=1)
ctk.rowconfigure(3, weight=1)
ctk.rowconfigure(4, weight=1)
ctk.rowconfigure(5, weight=1)

name = tk.StringVar(ctk)
weight_to_display = tk.StringVar(ctk)
person_type = tk.StringVar(ctk)
person_type.set("Scout")
running_total = tk.StringVar(ctk)
with open(FILENAME, "r") as file:
    file=file.read().split(",")
    try:
        running_total.set(str(file[-3]))
    except:
        running_total.set("0")


def Tare_The_Scale():
    get_serial(SERIALPORT, BAUDRATE, "x")
    
    get_serial(SERIALPORT, BAUDRATE, "1")
    
    get_serial(SERIALPORT, BAUDRATE, "x")


# Buttons and labels
btnSaveToFile = customtkinter.CTkButton(
    ctk, text="Save To File", font=("Helvetica", 60), command=lambda: write_to_file(FILENAME, name, person_type, weight_to_display, running_total)
)
btnSaveToFile.grid(row=4, column=2, columnspan=1, rowspan=3)

btnTare = customtkinter.CTkButton(
    ctk, text="Tare", font=("Helvetica", 20), command=Tare_The_Scale
)
btnTare.grid(row=3, column=2, columnspan=1, rowspan=3)

label1 = customtkinter.CTkLabel(
    ctk, textvariable=weight_to_display, font=("Helvetica", 200), width=100
)
label1.grid(row=0, column=0, columnspan=3, rowspan=3)

label2 = customtkinter.CTkLabel(ctk, textvariable=running_total, font=("Helvetica", 60))
label2.grid(row=3, column=2, columnspan=1, rowspan=1)

label3 = customtkinter.CTkLabel(
    ctk, text=("200 lbs. maximum on scale."), font=("Helvetica", 40)
)

NameEntry = customtkinter.CTkEntry(
    ctk, textvariable=name, font=("Helvetica", 60), width=300, height=60
)
NameEntry.grid(row=4, column=1, columnspan=1, rowspan=3)

r1 = customtkinter.CTkRadioButton(
    ctk, text="Scout", font=("Helvetica", 20), value="Scout", variable=person_type
)
r1.grid(row=3, column=0, rowspan=1)

r2 = customtkinter.CTkRadioButton(
    ctk, text="Webelo", font=("Helvetica", 20), value="Webelo", variable=person_type
)
r2.grid(row=4, column=0, rowspan=1)

r3 = customtkinter.CTkRadioButton(
    ctk, text="Other", font=("Helvetica", 20), value="Other", variable=person_type
)
r3.grid(row=5, column=0, rowspan=1)

current_font_size = 0  # Store the current font size

def adjust_font_size(event=None):
    global current_font_size
    new_font_size = int((ctk.winfo_width() + ctk.winfo_height()) // 50)

    if new_font_size != current_font_size:
        current_font_size = new_font_size
        btnSaveToFile.configure(font=("Helvetica", int(new_font_size // 1.5)))
        btnTare.configure(font=("Helvetica", new_font_size // 1.5))
        label1.configure(font=("Helvetica", new_font_size))
        label2.configure(font=("Helvetica", new_font_size))
        label3.configure(font=("Helvetica", int(new_font_size // 1.3)))
        NameEntry.configure(font=("Helvetica", new_font_size))
        r1.configure(font=("Helvetica", new_font_size // 2))
        r2.configure(font=("Helvetica", new_font_size // 2))
        r3.configure(font=("Helvetica", new_font_size // 2))

#NameEntry.bind("<Return>", write_to_file) # This makes it so you can press enter to save the weight, but when uncommented
                                           # it makes it so you can only save with enter

last_weight = None

def my_mainloop():
    global last_weight
    weight = get_serial(SERIALPORT, BAUDRATE, "W")
    if weight != last_weight:
        last_weight = weight
        weight_to_display.set(f"{weight} lbs.")
    ctk.after(500, my_mainloop)

ctk.after(500, my_mainloop)
adjust_font_size(0)
ctk.bind("<Configure>", adjust_font_size)

ctk.mainloop()