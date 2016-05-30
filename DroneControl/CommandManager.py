from AbstractManager import AbstractManager
from threading import Thread

class CommandManager(AbstractManager):
    def __init__(self):
        self._itemList = []                            #a list of all items
        self.currentCommand = None

    def addItem(self, newItem):                        #adds an item to the item list
        for existingItem in self._itemList:             #checks if binder already exists
            if newItem.binder == existingItem.binder:
                raise Exception()                      #if it does, raise exception
        self._itemList.append(newItem)                  #if it doesn't, add item to list
        
    def removeItem(self, item):                        #removes an item from the item list
        if item in self._itemList:                      #checks if item is in item list
            self._itemList.remove(item)                 #if it is, remove it
        else:
            raise Exception()                          #if it isn't, raise exception

    def stopCommand(self):
        if self.currentCommand is None:
            pass
        else:
            self.currentCommand.stop()

    def execute(self, binder):                         #executes function in item
        found = False
        for item in self._itemList:                          #checks if binder is in specifiecd
            if item.binder == binder:                  #if it is, execute it
                found = True
                self.currentCommand = item
                item.runningFlag = True
                item.execute()
                item.exit()
                item.stop()
                self.currentCommand = None
        if found == False:                             #if it isn't, raise exception
            raise Exception("Command %s not found!" % binder)
    @property
    def itemList(self):                                #returns the item list
        return self._itemList