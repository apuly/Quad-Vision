from Command import Command
from time import sleep

class Follow(Command):
    def __init__(self, camera, distance):
        super(Follow, self).__init__(camera, distance)
        self._binder = 'follow'
    
    @property
    def binder(self):
        return self._binder

    def execute(self):
        while self.runningFlag:
            print("Following")
            sleep(0.5)

    def exit(self):
        print("that was quick")

class Stop(Command):
    def __init__(self, camera, distance):
        super(Stop, self).__init__(camera, distance)
        self._binder = 'stop'

    @property
    def binder(self):
        return self._binder

    def execute(self):
        print("Stopping")
        
