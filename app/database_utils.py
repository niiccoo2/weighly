import datetime
from CTkMessagebox import CTkMessagebox

# Write donation data to a file
def write_to_file(filename, name, person_type, weight, running_total):
    clean_name = name.get().strip().title()
    ScoutTypeDisplay = person_type.get().strip()
    weight_to_file = weight.get().rstrip(" lbs.")

    if clean_name != "":
        with open(filename, "a") as hs:
            ct = datetime.datetime.now()
            bt = float(running_total.get())
            bt = round(bt + float(weight_to_file), 2)
            running_total.set(str(bt))

            hs.write(f"{clean_name},{ScoutTypeDisplay},{weight_to_file},lbs,{bt},lbs,{ct}\n")

        CTkMessagebox(
            title="Saved", message=f"Saved {weight_to_file} lbs. from {clean_name}"
        )
    else:
        CTkMessagebox(
            title="Error",
            message=f"Please Name The {ScoutTypeDisplay}",
            icon="cancel",
        )