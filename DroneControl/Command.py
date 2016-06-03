﻿from Item import Item

class Command(Item):
    def __init__(self, actionHandler, camera, distance):
        self.camera = camera
        self.distance = distance
        self.action = actionHandler
        self.runningFlag = False
        
    def stop(self):
        self.runningFlag = False

    def binder(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass