from Sensor import Sensor

class DistanceSensor(Sensor):
    def __init__(self, triggerPin, echoPin):
        self.trigPin = triggerPin
        self.echoPin = echoPin
        

    def read(self):     #reads value from sensor
        pass            #TODO: implement this shit