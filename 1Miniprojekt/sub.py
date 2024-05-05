import paho.mqtt.subscribe as subscribe
import json
 
def print_msg(client, userdata, message):
    
    MSG = json.loads(message.payload.decode("utf-8"))
    print("%s : %s" % (message.topic, MSG))
 
subscribe.callback(print_msg, "KURNIK/DHT11", hostname="test.mosquitto.org")
print("ahoj")