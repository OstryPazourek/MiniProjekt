import json

from dht import DHT11
from machine import Pin

p = Pin(26)
d = DHT11(p)
 

def GetData():
    d.measure()
    D = {
    "Temp": d.temperature(),
    "Hum":d.humidity()
    }
    print(json.dumps(D))
    return json.dumps(D)

print(GetData())
