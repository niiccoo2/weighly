import serial
import time
import re
import threading
from random import uniform

def get_serial(serialport, baudrate, StringToSend):
    print("StringToSend =", StringToSend)
    ser = serial.Serial(serialport, baudrate, timeout=1)
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    ser.write(StringToSend.encode('utf-8'))

    start_time = time.time()

    while True:
        if ser.in_waiting > 0:
            input_line = ser.readline().decode('utf-8', errors='ignore').strip()
            print(f"Serial line from scale: {input_line}")

            # Match something like "-2.14,lbs,0,"
            if re.match(r"^-?\d+(\.\d+)?,lbs,", input_line):
                parts = input_line.split(",")
                try:
                    weight = float(parts[0])
                    print("Weight =", weight)
                    ser.close()
                    return weight
                except ValueError:
                    print("Couldn't parse weight number:", parts[0])
        
        # prevent infinite loop if no data
        if time.time() - start_time > 5:
            print("Timeout waiting for valid data")
            ser.close()
            return None

# Simulated scale data for testing
def get_serial_dummy(serialport, buadrate, stringToSend):
    weight = uniform(0, 200)
    #weight = 50
    return weight