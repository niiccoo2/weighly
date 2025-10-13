import serial
import time
import re
import threading
from random import uniform

# This lock prevents two threads from trying to use the scale at the exact same time,
# which is the cause of the "PermissionError: Access is denied" error.
_serial_lock = threading.Lock()

def get_serial(port: str, baud: int, command: str = "W", timeout: float = 2.0) -> float | None:
    """
    Sends a character to the scale and reads the weight response.
    This is designed to be robust for your specific SparkFun scale.
    """
    # 1. ACQUIRE THE PORT
    # We use a lock to ensure only one part of your app can talk to the scale at a time.
    with _serial_lock:
        try:
            # This opens the port and guarantees it closes, even if errors happen.
            with serial.Serial(port, baud, timeout=0.1) as ser:

                # 2. IGNORE THE STARTUP BANNER
                # Your scale sends a banner ("Serial Load Cell Converter...") on connection.
                # We must read and discard these lines first, just like you see in PuTTY.
                time.sleep(0.1)  # Give the banner time to start sending
                while ser.in_waiting:
                    ser.readline() # Read and throw away one line of the banner

                # 3. SEND THE COMMAND
                # Now that the banner is gone, we send the 'W' character.
                # Your old code didn't use a newline, so we won't either.
                ser.write(command.encode('ascii'))
                ser.flush() # Ensure the command is sent immediately

                # 4. READ THE RESPONSE
                # We now listen for the answer, which looks like "-0.47,lbs,0,".
                # We loop until we find a line with a valid number or we time out.
                deadline = time.monotonic() + timeout
                while time.monotonic() < deadline:
                    response_bytes = ser.readline()
                    if not response_bytes:
                        time.sleep(0.05) # Wait a moment for the response
                        continue

                    # Decode bytes to text, ignoring any weird characters.
                    response_text = response_bytes.decode('latin-1', errors='ignore').strip()
                    print(f"Scale Read: '{response_text}'") # Debug print

                    # Find the first number in the response text.
                    match = re.search(r"-?\d+\.?\d*", response_text)
                    if match:
                        try:
                            # If we found a number, convert it to a float and return it.
                            return float(match.group(0))
                        except (ValueError, TypeError):
                            # If conversion fails, keep trying.
                            continue
                
                # If the loop finishes without returning, we timed out.
                print("Scale timeout: No valid weight received.")
                return None

        except serial.SerialException as e:
            # This handles errors like "port not found" or "access denied".
            print(f"Serial communication error: {e}")
            return None

# Simulated scale data for testing
def get_serial_dummy(serialport, buadrate, stringToSend):
    weight = uniform(0, 200)
    #weight = 50
    return weight