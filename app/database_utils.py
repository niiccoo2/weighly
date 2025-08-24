import datetime
from CTkMessagebox import CTkMessagebox

# Write donation data to a file
def write_to_file(filename, scout, ScoutType, weight_to_display, Bigtotal):
    ScoutName = scout.get().strip().title()
    ScoutTypeDisplay = ScoutType.get().strip()
    weight_to_file = weight_to_display.get().rstrip(" lbs.")

    if ScoutName != "":
        with open(filename, "a") as hs:
            ct = datetime.datetime.now()
            bt = float(Bigtotal.get())
            bt = round(bt + float(weight_to_file), 2)
            Bigtotal.set(str(bt))

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