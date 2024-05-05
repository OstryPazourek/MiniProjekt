import network
from time import sleep
import machine 
import time

led = machine.Pin("LED", machine.Pin.OUT) 
def blink():
    
    led.on()
    time.sleep(0.1)
    led.off()
    time.sleep(0.1)


    

def Conncect():

    wlan = network.WLAN(network.STA_IF)
    if wlan.isconnected():
        return
    
    wlan.active(True)

    ssid = "Vodafone-ACAE"
    password = "Qt6hdjh5wceA6rsw"

    wlan.connect(ssid, password)

    while wlan.isconnected() == False:
        print('Waiting for connection...')
        blink()
        
        sleep(1)


    print(wlan.ifconfig())
    return True
