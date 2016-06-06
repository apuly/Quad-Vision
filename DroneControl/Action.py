from Item import Item

class Action(Item):
    def __init__(self, binder, data, rcdata):
        if len(data) != 3:
            raise Exception("fault in actions.json")
        self._binder = binder
        self._data = data
        self._rcdata = rcdata
        pass

    def binder(self):           #returns the binder
        return self._binder

    def execute(self, *args):  
        self._rcdata.pitch = data[0]
        self._rcdata.roll = data[1]
        self._rcdata.yaw = data[2]
