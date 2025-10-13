import threading
import time
import re
from random import uniform
import serial # pip install pyserial

def get_serial(ser: serial.Serial | None, lock: threading.Lock, StringToSend: str):
    """
    Sends a command and reads the response from an *already-open* serial port.
    """
    # 1. Check if the connection is valid
    if not ser or not ser.is_open:
        # This is not an error, just means the scale is not connected.
        return None

    with lock: # Acquire the lock to ensure exclusive access
        try:
            # 2. Send the command
            command_to_send = StringToSend + '\r\n'
            ser.reset_input_buffer() # Clear old data
            ser.write(command_to_send.encode('utf-8'))
            ser.flush()

            # 3. Read the response
            deadline = time.time() + 2.0 # 2-second timeout

            while time.time() < deadline:
                input_line = ser.readline().decode('utf-8', errors='ignore').strip()
                if not input_line:
                    continue # Ignore empty lines

                print(f"Serial line from scale: {input_line}")

                if re.match(r"^-?\d+(\.\d+)?,lbs,", input_line):
                    parts = input_line.split(",")
                    try:
                        weight = float(parts[0])
                        print("Weight =", weight)
                        return weight
                    except (ValueError, IndexError):
                        continue
            
            print("Timeout: No valid weight line received.")
            return None

        except serial.SerialException as e:
            print(f"Serial Error during read/write: {e}")
            return None

# Simulated scale data for testing
def get_serial_dummy(serialport, buadrate, stringToSend):
    weight = uniform(0, 200)
    #weight = 50
    return weight