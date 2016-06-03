from Item import Item

class Action(Item):
    def __init__(self, binder, data):
        self._binder = binder
        self._data = data
        pass

    def binder(self):           #returns the binder
        return self._binder

    def execute(self, *args):  
        pass
