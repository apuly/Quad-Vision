from Item import Item

class Action(Item):
    def __init__(self, binder, data):
        self._binder = binder
        self._data = data

    def binder(self):           #returns the binder
        return self._binder

    def execute(self, *args):   #TODO send data to the drone
        pass
