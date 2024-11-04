import serial
import time
from time import sleep
from grovepi import *
import grovepi
from grove_rgb_lcd import *
import RPi.GPIO as GPIO
from pyrebase import pyrebase

# Set up pin 32 (GPIO12) for PWM
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
p = GPIO.PWM(32, 50)
p.start(0)

buzzer = 2
grovepi.pinMode(buzzer, "OUTPUT")

# Set up button
button = 3
pinMode(button, "INPUT")

# Set up DHT11 sensor
dhtsensor = 8
pinMode(dhtsensor, "INPUT")

#Firebase
config={
    "apiKey": "AIzaSyDSVKWrU1Eqn0-C8BoJOXIKZGm11UcuFsQ",
    "authDomain": "iot-firebase-df0be.firebaseapp.com",
    "databaseURL": "https://iot-firebase-df0be-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "iot-firebase-df0be.appspot.com"
    }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("youngjuin1234@gmail.com", "Youngjuin_123")
db = firebase.database()


mypet=db.child("MyPet").get()
            
#rpiser1=serial.Serial('/dev/ttyAMA0',
rpiser1 = serial.Serial('/dev/ttyS0',
                        baudrate=9600, timeout=1,
                        bytesize=serial.EIGHTBITS, parity=serial.PARITY_NONE,
                        stopbits=serial.STOPBITS_ONE,
                        xonxoff=False, rtscts=False, dsrdtr=False)
rpiser1.flushInput()
rpiser1.flushOutput()


try:
    print("Start")
    while True:
        # Read data from DHT11 sensor
        [temp, hum] = dht(dhtsensor, 0)
        # Display data on LCD
        setRGB(218, 247, 166)
        t = str(temp)
        h = str(hum)
        setText("Temp: " + t + '\337' + "C    Humidity: "+ h +" %")
        
        bStatus = digitalRead(button)
        # Read data from serial port
        if bStatus:
            grovepi.digitalWrite(buzzer, 1)
            time.sleep(0.08)
            grovepi.digitalWrite(buzzer, 0)
            p.ChangeDutyCycle(3)
            time.sleep(3)
            p.ChangeDutyCycle(12)
            grovepi.digitalWrite(buzzer, 1)
            time.sleep(0.08)
            grovepi.digitalWrite(buzzer, 0)
        

        
        
#         mypet=db.child("MyPet").get()
#         for pet in mypet.each():
#              a = pet.val()
#              x = a['ID']
#              print(x)
#        s = rpiser1.read(14)     
#        if len(s) != 0:
        s = rpiser1.read(14)
        for pet in mypet.each():
            time.sleep(2)
            a = pet.val()
            x = a['ID']
            print(x)
            
        if str(s.hex())== x: 
#             print(mypet.val())
            print(s.hex(), "Authorised access")
            grovepi.digitalWrite(buzzer, 1)
            time.sleep(0.08)
            grovepi.digitalWrite(buzzer, 0)
            p.ChangeDutyCycle(3)
            time.sleep(3)
            p.ChangeDutyCycle(15)
            grovepi.digitalWrite(buzzer, 1)
            time.sleep(0.08)
            grovepi.digitalWrite(buzzer, 0)
            time.sleep(5)
            
        
except KeyboardInterrupt:
    print("Program ended")
finally:
    p.stop()
    GPIO.cleanup()
    grovepi.digitalWrite(buzzer, 0)