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
        self.events = get_allowed_events()

        formatted = {int(e.get('event_id')): e.get('name', '') for e in self.events}
        print(f"Formatted events: {formatted}")

        self.event_var = ctk.StringVar(value="") #init ctk var
        self.event_dropdown = ctk.CTkOptionMenu(self,
            values=list(formatted.values()),
            command= lambda item: self._load_event(item),
            variable=self.event_var)
        self.event_dropdown.grid(row=1, column=0)
        # Build safe dict {id: name} and list of (id, name) pairs
        pairs = []
        allowed = {}
        for e in (self.events or []):
            eid = e.get('event_id')
            if eid is None:
                continue
            try:
                eid = int(eid)
            except (TypeError, ValueError):
                continue
            name = e.get('name') or ""
            allowed[eid] = name
            pairs.append((eid, name))

        self.allowed_events = allowed  # {id: name}
        print(f"Formatted events: {self.allowed_events}")

        # Build display names for dropdown; disambiguate duplicates by appending (id)
        from collections import Counter
        name_counts = Counter(name for _, name in pairs)
        display_names = []
        id_list = []
        for eid, name in pairs:
            display = f"{name} ({eid})" if name_counts[name] > 1 else name
            display_names.append(display)
            id_list.append(eid)

        # Store mapping arrays for lookup
        self.display_names = display_names
        self.event_id_list = id_list

        # Create / update OptionMenu
        self.event_var = ctk.StringVar(value=display_names[0] if display_names else "No events")
        self.event_dropdown = ctk.CTkOptionMenu(self,
            values=display_names or ["No events"],
            command=lambda item: self._load_event(item),
            variable=self.event_var)
        self.event_dropdown.grid(row=1, column=0)
    
    def _load_event(self, event):
        pass