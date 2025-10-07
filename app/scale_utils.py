import serial # pip install pyserial
from random import uniform

def get_serial(serialport, buadrate, stringToSend):
    ser = serial.Serial(serialport, buadrate, timeout =1) #Real scale

    print("StringToSend = "+stringToSend)
    weight_string = ""
    weight = 00.0
    miliseconds = 0
    Data_Ready = 0
    
    ser.reset_input_buffer()
    ser.reset_output_buffer()
    
    #ser.write(bytearray("W",'ascii'))
    ser.write(stringToSend.encode('utf-8'))
    i=0
    #time.sleep(.1)
    while (Data_Ready == 0):
        Data_Ready = ser.in_waiting
        i=i+1
        if i>10:
            print("Scale timeout. [scale_utils.py, line 24 ish]")
            break
    
    input_string =""
    
    input_string = ser.readline().decode('utf-8')
    print (input_string)
    
    try:
        split_input_string = input_string.split(",")
        print("weight splitting")
        print (split_input_string[0])
        print (split_input_string[1])
        weight_string = split_input_string[0]
        weight_string = weight_string.rstrip()
        weight_string = weight_string.rstrip('lbs')
        
        print("weight_string = "+ weight_string)
        weight = float(weight_string)
        
        print("weight = "+ str(weight))
        
        #miliseconds_string = split_input_string[0].strip()
        #miliseconds = int(miliseconds_string)
        
        print("milliseconds = " + str(miliseconds))
              
        return weight
        
    except:
        print("Not Weight Data")
        print (split_input_string[0])

# Simulated scale data for testing
def get_serial_dummy(serialport, buadrate, stringToSend):
    weight = uniform(0, 200)
    #weight = 50
    return weight