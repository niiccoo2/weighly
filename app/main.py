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

    # label
    self.label = ctk.CTkLabel(self, text='Hello, Tkinter!')
    self.label.pack()

    # button
    self.button = ctk.CTkButton(self, text='Click Me')
    self.button['command'] = self.button_clicked
    self.button.pack()

  def button_clicked(self):
    print("Clicked")

if __name__ == "__main__":
  weighly = Weighly()
  weighly.mainloop()