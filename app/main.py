import customtkinter as ctk
from scale_utils import get_serial, get_serial_dummy
from database_utils import save_weight, read_running_total, FILENAME

class Weighly(ctk.CTk):
    def __init__(self):
        super().__init__()

        # configure the root window
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("dark-blue")  # Themes: "blue", "green", "dark-blue"
        self.title('Weighly')
        self.geometry('1000x500')
        self.resizable(True, True)

        self.use_dummy_scale = True # Remove this once the ability to enter weight is added

        if self.use_dummy_scale:
            get_serial = get_serial_dummy

        self.SERIALPORT = "/dev/ttyUSB0"  #Real Sparfun Open Scale
        #self.SERIALPORT = "/dev/ttyACM0"  #Dummy Sparfun Open Scale on Arduino
        self.BAUDRATE = 9600
        self.current_font_size = 0

        open(FILENAME, "a") # Creates the file if non existent

        self.main_screen()


    def tare_scale(self):
        get_serial(self.SERIALPORT, self.BAUDRATE, "x")
        
        get_serial(self.SERIALPORT, self.BAUDRATE, "1")
        
        get_serial(self.SERIALPORT, self.BAUDRATE, "x")
    
    def main_screen(self):
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
        self.btnSaveToFile = ctk.CTkButton(
            self, 
            text="Save To File", 
            font=("Helvetica", 60), 
            command=lambda: save_weight(1, self.name.get(), float(self.weight_TKvar.get()), self.person_type.get()))
        self.btnSaveToFile.grid(row=4, column=2, columnspan=1, rowspan=3)

        self.btnTare = ctk.CTkButton(
            self, 
            text="Tare", 
            font=("Helvetica", 20), 
            command=self.tare_scale)
        self.btnTare.grid(row=3, column=2, columnspan=1, rowspan=3)

        self.label1 = ctk.CTkLabel(
            self, 
            textvariable=f"{self.weight_TKvar} lbs.",
            font=("Helvetica", 200), 
            width=100)
        self.label1.grid(row=0, column=0, columnspan=3, rowspan=3)

        self.label2 = ctk.CTkLabel(
            self, 
            textvariable=self.running_total, 
            font=("Helvetica", 60))
        self.label2.grid(row=3, column=2, columnspan=1, rowspan=1)

        self.label3 = ctk.CTkLabel(
            self, 
            text=("200 lbs. maximum on scale."), 
            font=("Helvetica", 40))
        
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
        global current_font_size
        new_font_size = int((self.winfo_width() + self.winfo_height()) // 50)

        if new_font_size != self.current_font_size:
            current_font_size = new_font_size
            self.btnSaveToFile.configure(font=("Helvetica", int(new_font_size // 1.5)))
            self.btnTare.configure(font=("Helvetica", new_font_size // 1.5))
            self.label1.configure(font=("Helvetica", new_font_size))
            self.label2.configure(font=("Helvetica", new_font_size))
            self.label3.configure(font=("Helvetica", int(new_font_size // 1.3)))
            self.NameEntry.configure(font=("Helvetica", new_font_size))
            self.r1.configure(font=("Helvetica", new_font_size // 2))
            self.r2.configure(font=("Helvetica", new_font_size // 2))
            self.r3.configure(font=("Helvetica", new_font_size // 2))


  

if __name__ == "__main__":
    weighly = Weighly()

    def my_mainloop():
        # initialize the attribute on first call
        if not hasattr(my_mainloop, "last_weight"):
            my_mainloop.last_weight = None

        weighly.running_total.set(str(read_running_total(1)))
        weight = get_serial(weighly.SERIALPORT, weighly.BAUDRATE, "W")

        if weight != my_mainloop.last_weight:
            my_mainloop.last_weight = weight
            weighly.weight_TKvar.set(f"{weight}")

        weighly.after(500, my_mainloop)

    weighly.after(500, my_mainloop)
    weighly.adjust_font_size(0)
    weighly.bind("<Configure>", weighly.adjust_font_size)

    weighly.mainloop()