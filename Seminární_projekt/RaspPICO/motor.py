import machine 
import PicoMotorDriver
import utime
led = machine.Pin("LED", machine.Pin.OUT)

speed = 10
step = 400 #400=15mm = 1,5cm

board = PicoMotorDriver.KitronikPicoMotor()

def opendoor():
    direction = "r" #r = otevřít
    led.on()
    board.step(direction,step,speed)
    led.off()
    print("Oteviram")
    
def closedoor():
    direction = "f" #f=zavřít
    led.on()
    board.step(direction,step,speed)
    led.off()
    print("Zaviram")


opendoor()
closedoor()