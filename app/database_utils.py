import datetime
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import requests

FILENAME="./weighly_backup.csv"

# Write donation data to a file
def save_to_file(filename: str, name: str, weight: float, person_type: str):
    """
    Saves name, weight, and type to local CSV.
    """
    clean_name = name.strip().title()
    ScoutTypeDisplay = person_type.strip()
    weight_to_file = weight

    if clean_name != "":
        with open(filename, "a") as hs:
            current_time = datetime.now()

            hs.write(f"{clean_name},{ScoutTypeDisplay},{weight_to_file},{current_time}\n")

        CTkMessagebox(
            title="Saved", message=f"Saved {weight_to_file} lbs. from {clean_name}"
        )
    else:
        CTkMessagebox(
            title="Error",
            message=f"Please Name The {ScoutTypeDisplay}",
            icon="cancel",
        )

def save_to_database(name: str, weight: float, person_type: str):
    """
    Saves name, weight, and type to weighly backend.
    """
    url = "http://127.0.0.1:8000/1/add_weight" # This is for local testing

    payload = {
    "name": name,
    "weight": weight,
    "type": person_type,
    "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)

def save_weight(name: str, weight: float, person_type: str):
    """
    Calls both save to database and file at the same time. 
    """

    save_to_file(FILENAME, name, weight, person_type) # Uses filename defined at top of file
    save_to_database(name, weight, person_type)