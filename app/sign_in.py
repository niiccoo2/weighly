import customtkinter as ctk
import threading
from CTkMessagebox import CTkMessagebox
from typing import Any
from database_utils import sign_in_supabase, get_allowed_events

class SignInScreen(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.columnconfigure(0, weight=1)
        for i in range(3):
            self.rowconfigure(i, weight=1)

        self.label = ctk.CTkLabel(self, text="Sign in to Weighly", font=("Helvetica", 30))
        self.label.grid(row=0, column=0, padx=20, pady=20)

        self.sign_in_button = ctk.CTkButton(self, text="Sign In", font=("Helvetica", 30), command=self._sign_in_button)
        self.sign_in_button.grid(row=1, column=0, padx=20, pady=20)
    
    def _sign_in_button(self):
        if sign_in_supabase() == 0: # If successful
            self.controller.show_frame("EventPicker")
        else:
            CTkMessagebox(title="Error", message="Sign in failed. Please try again.", icon="cancel")

class EventPicker(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.events = []

        self.columnconfigure(0, weight=1)
        for i in range(3):
            self.rowconfigure(i, weight=1)

        self.label = ctk.CTkLabel(self, text="Pick Event:", font=("Helvetica", 30))
        self.label.grid(row=0, column=0, padx=20, pady=20)

    def refresh(self):

        self.formatted = self._create_formatted_events(get_allowed_events())
        print(f"\nFormatted events: {self.formatted}")

        # Build a list of names from the formatted event dicts.
        # Use a list comprehension (not a generator) so `names` is a list of strings.
        names: list[str] = [str(e.get("name", "")) for e in self.formatted]
        print(f"\nNames: {names}")

        self.event_var = ctk.StringVar(value="") #init ctk var
        self.event_dropdown = ctk.CTkOptionMenu(self,
            values=names,
            command= lambda item: self._load_event(item),
            variable=self.event_var)
        self.event_dropdown.grid(row=1, column=0)
        
    
    def _load_event(self, event):
        # Find event id from name
        for e in self.formatted:
            if e.get("name") == event:
                event_id = int(e.get("event_id", 0))
                break

        self.controller.event_id = event_id
        self.controller.show_frame("MainScreen")

    def _create_formatted_events(self, events) -> list[dict[str, str|int]]:
        # list[dict[str, Any]]

        formatted = []

        for e in events:
            event_id = int(e.get('event_id', 0))
            name = e.get('name', '')

            if any(name.lower() in (i.get('name') or "").lower() for i in formatted): # If name already exists
                name = name + f" ({event_id})"
                formatted.append({'event_id': event_id, 'name': name})
            else:
                formatted.append({'event_id': event_id, 'name': name})

        return formatted