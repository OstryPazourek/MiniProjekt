import serial
import json
 
try:
    ser = serial.Serial('COM5', 115200)
    ser.flushInput()
except Exception as e:
    print(e)
    print("unable to open COM port")
    exit(-1)

while True:
    data = ser.readline().decode()
    print(data)
    temp = json.loads(data)
    print(temp["Temp"])
'''
while True:
    I = input("ON/OFF: ")
    I = I+"\r\n"
    I = I.encode()
    print(I)
    ser.write(I)

'''