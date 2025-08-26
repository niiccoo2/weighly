import datetime
from CTkMessagebox import CTkMessagebox
from datetime import datetime
import requests

FILENAME="./weighly_backup.csv"

# Write donation data to a file
def save_to_file(filename: str, name: str, weight: float, person_type: str):
    """
    Saves name, weight, and type to local CSV.
    Returns 0 for success, otherwise returns the error message.
    """
    try:
        clean_name = name.strip().title()
        type_display = person_type.strip() # idk why we have this
        weight_to_file = weight

        if name != "":
            with open(filename, "a") as hs:
                current_time = datetime.now()
                hs.write(f"{clean_name},{type_display},{weight_to_file},{current_time}\n")
        else:
            return "Name cannot be blank"
        return 0
    except Exception as e:
        return str(e)


def save_to_database(name: str, weight: float, person_type: str):
    """
    Saves name, weight, and type to weighly backend.
    Returns 0 for success, otherwise the error message.
    """
    if name != "":
        try:
            url = "http://127.0.0.1:8000/1/add_weight"  # This is for local testing

            payload = {
                "name": name,
                "weight": weight,
                "type": person_type,
                "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            headers = {"Content-Type": "application/json"}

            response = requests.post(url, json=payload, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses
            return 0
        except Exception as e:
            return str(e)
    else:
        return "Name cannot be blank"

def save_weight(name: str, weight: float, person_type: str):
    """
    Calls both save to database and file at the same time and gives saved or error message.
    """

    database = "Not attempted"

    file = save_to_file(FILENAME, name, weight, person_type)

    if file == 0: # Only save to db if it saves to file
        database = save_to_database(name, weight, person_type)

    if file == 0 and database == 0: # If they both return 0 for no error
        CTkMessagebox(
            title="Saved", message=f"Saved {weight} lbs from {name}!"
        )
    else:
        if file != 0: # Means file is not ok
            CTkMessagebox(
                title="Error", 
                message=f"Error: {str(file)}",
                icon="cancel"
            )
        if database != 0 and database != "Not attempted": # Means db is not ok
            CTkMessagebox(
                title="Error", 
                message=f"Error: {str(database)}",
                icon="cancel"
            )