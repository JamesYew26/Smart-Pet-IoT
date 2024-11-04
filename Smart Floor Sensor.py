import grovepi
import time


ultrasonic_pin = 2
led_pin = 3
buzzer_pin = 4

grovepi.pinMode(ultrasonic_pin, "INPUT")
grovepi.pinMode(led_pin, "OUTPUT")
grovepi.pinMode(buzzer_pin, "OUTPUT")


def read_distance():
    return grovepi.ultrasonicRead(ultrasonic_pin)

def activate_alarm():
    grovepi.digitalWrite(buzzer_pin, 1)
    time.sleep(0.08)
    grovepi.digitalWrite(buzzer_pin, 0)
    time.sleep(0.08)
    grovepi.digitalWrite(buzzer_pin, 1)
    time.sleep(0.08)
    grovepi.digitalWrite(buzzer_pin, 0)
    grovepi.digitalWrite(led_pin, 1)
    
def deactivate_alarm():
    grovepi.digitalWrite(buzzer_pin, 0)
    grovepi.digitalWrite(led_pin, 0)
    
#main loop
try:
    threshold_distance = 0
    distance_counter = 0
    
    while True:
        distance = read_distance()
        
        if distance < 50:
            distance_counter += 1
        else:
            distance_counter = 0
            
        
        if distance_counter >= 3:
            print("Object detected")
            activate_alarm()
        else:
            deactivate_alarm()
            
        time.sleep(1)
        
except KeyboardInterrupt:
    print("Exiting...")
    deactivate_alarm()
    