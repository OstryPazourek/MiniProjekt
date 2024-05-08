from machine import Timer, Pin, WDT
import time
from time import sleep
import motor

led = machine.Pin("LED", machine.Pin.OUT) 

def blink():
    led.on()
    time.sleep(0.5)
    led.off()
    time.sleep(0.5)

for _ in range(3):  # Blikne 10x při startu
    blink()
    #wdt = WDT(timeout = 8000)
    
import WifiConn
from simple import MQTTClient
import temData

    
WifiConn.Conncect()
MQTT_BROKER = "test.mosquitto.org"
MQTT_PORT = 1883

client = MQTTClient(
    client_id="RaspberryPiPicoGeorge",
    server=MQTT_BROKER,
    port=MQTT_PORT)
client.connect()
#wdt.feed()

# MQTT Callback funkce
def mqtt_callback(topic, msg):
    print(f"Received `{msg}` from `{topic}`")
    blink()
    blink()
    if msg == b'1':
        motor.opendoor()
    elif msg == b'0':
        motor.closedoor()
# Nastavení callbacku pro MQTT klienta
client.set_callback(mqtt_callback)
client.subscribe("KURNIK/DVERE")


def TimerEvent(t):
    try:
        client.publish(
        "KURNIK/DHT11",
        temData.GetData()
        )
        led.on()
        time.sleep(0.1)
        led.off()
        time.sleep(0.1)
        #wdt.feed()
    except:
        client.connect()
        
Timer(mode=Timer.ONE_SHOT, period=1, callback=TimerEvent)
Timer(mode=Timer.PERIODIC, period=600000, callback=TimerEvent)

while True:
    client.check_msg()
    time.sleep(1)  # Krátká pauza pro stabilizaci smyčky
    
    
    
    