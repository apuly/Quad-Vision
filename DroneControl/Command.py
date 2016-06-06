from Item import Item

class Command(Item):
    def __init__(self, actionHandler, camera, height):
        self.camera = camera
        self.action = actionHandler
        self.height = height
        self.runningFlag = True
        
    def stop(self):
        self.runningFlag = False

    def binder(self):
        pass

    def execute(self):
        pass

    def exit(self):
        pass