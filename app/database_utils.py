import datetime
from CTkMessagebox import CTkMessagebox

# Write donation data to a file
def write_to_file(filename, name, person_type, weight, running_total):
    ScoutName = name.get().strip().title()
    ScoutTypeDisplay = person_type.get().strip()
    weight_to_file = weight.get().rstrip(" lbs.")

    if ScoutName != "":
        with open(filename, "a") as hs:
            ct = datetime.datetime.now()
            bt = float(running_total.get())
            bt = round(bt + float(weight_to_file), 2)
            running_total.set(str(bt))

            hs.write(f"{ScoutName},{ScoutTypeDisplay},{weight_to_file},lbs,{bt},lbs,{ct}\n")

        CTkMessagebox(
            title="Saved", message=f"{ScoutName}, thank you for your {weight_to_file} lbs. donation!"
        )
    else:
        CTkMessagebox(
            title="Error",
            message=f"Please Name The {ScoutTypeDisplay}",
            icon="cancel",
        )