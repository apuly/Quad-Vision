from Sensor import Sensor
import time
import RPi.GPIO as GPIO

class DistanceSensor(Sensor):
    def __init__(self, triggerPin, echoPin):
        self.trigPin = triggerPin
        self.echoPin = echoPin
        GPIO.setwarngins(False)

        GPIO.setup(self.trigPin, GPIO.OUT)
        GPIO.setup(self.echoPin, GPIO.IN)
        GPIO.output(self.trigPin, GPIO.LOW)
        time.sleep(0.3) #needed to prevent sensor from crashing
        

    def read(self):     #reads value from sensor
        GPIO.output(self.trigPin, True) #sends a 10Us pulse to the trigger pin of the sensor to start reading
        time.sleep(0.00001)                 
        GPIO.output(self.trigPin, False)

        while GPIO.input(self.echoPin) == 0:        #wait till the sensor starts reading
            pass
        startPulseTime = time.time()                #get start time when it does

        while GPIO.input(self.echoPin) == 1:        #wait for the sensor to stop reading
            pass
        endPulseTime = time.time()                  #get end time when it does

        timepassed = endPulseTime - startPulseTime  #calculate the time between trigger and echo

        distance = timepassed * 17000               #convert time to (somewhat) centimeters
        return distance

   