from machine import WDT
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
        print("AllreadyConnect")
        return
    
    wlan.active(True)

    ssid = "Zyxel_24"
    password = "4U4D8MEX7R"

    wlan.connect(ssid, password)
    Waiting = 0
    while wlan.isconnected() == False:
        print('Waiting for connection...')
        blink()
        
        sleep(1)
        Waiting = Waiting+1
        if Waiting >= 12:
            print("moc dlouho cekam na pripojení")
            #wdt = WDT(timeout = 1000)

    print(wlan.ifconfig())
    return True
