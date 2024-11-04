import serial
import grovepi
import time
from pyrebase import pyrebase

buzzer = 2
relay = 6
grovepi.pinMode(buzzer, "OUTPUT")
grovepi.pinMode (relay,"OUTPUT")


config={
    "apiKey": "AIzaSyDSVKWrU1Eqn0-C8BoJOXIKZGm11UcuFsQ",
    "authDomain": "iot-firebase-df0be.firebaseapp.com",
    "databaseURL": "https://iot-firebase-df0be-default-rtdb.asia-southeast1.firebasedatabase.app",
    "storageBucket": "iot-firebase-df0be.appspot.com"
    }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password("junchee0206@gmail.com", "JunChee26_")
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
        s = rpiser1.read(14)
        for pet in mypet.each():
            time.sleep(1)
            a = pet.val()
            x = a['ID']
            print(x)
        if str(s.hex())== x: 
            
            grovepi.digitalWrite(relay,1)
            grovepi.digitalWrite(buzzer,1)
            time.sleep(0.08)
            grovepi.digitalWrite(buzzer,0)
            time.sleep(0.08)
            grovepi.digitalWrite(buzzer,1)
            time.sleep(0.08)
            grovepi.digitalWrite(buzzer,0)
            print(pet.val())
        else:
            grovepi.digitalWrite(relay,0)
            
                
        #break 
except KeyboardInterrupt:
    print("Program ended")
finally:
    grovepi.digitalWrite(buzzer, 0)
    grovepi.digitalWrite(relay,0)