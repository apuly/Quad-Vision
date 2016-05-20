from CommandManager import CommandManager
from ActionManager import ActionManager
from Action import Action
from Camera import Camera
from DistanceSensor import DistanceSensor
from Symbol import Symbol
import json
import threading
from time import sleep

class Controller(object):
    def __init__(self):
        self.cam = Camera()
        self.distance = DistanceSensor()
        self.cmdManager = CommandManager()
        self.actionManager = ActionManager()
        self.heightCm = None
        self.symbolList = []

        self.loadActions()
        self.loadCommands()
        self.loadSymbols()
        

        heightThread = threading.Thread(target = self.updateDistance)
        heightThread.start()


    def loadActions(self):                                                  #loads actions into actionmanager   
        actionJson = json.load('actions.json')                              #opens JSON file with action data
        for actions in actionJson['actions']:                               
            tempAction = Action(actions['binder'], actions['data'])         #creates actions using data
            self.actionManager.addItem(tempAction)                          #loads data into action manager

    def loadCommands(self):
        commands = [cls for cls in vars()['Command'].__subclasses__()]      #gets all classes that extends command class
        for command in commands:
            self.cmdManager.addItem(command())                              #initiallise commands and add them to command manager

    def loadSymbols(self):                                                  #loads symbols into symbol list
        symbolsJson = json.load('symbols.json')                             #opens JSON file with symbol data
        for symbolData in symbolsJson['symbols']:
            self.symbolList.append(Symbol(symbol['path'], symbol['command']) #reads data from json, loads into symbol list

    def updateDistance(self):                           #constantly updates the drones height to the ground
        while True:
            self.heightCm = self.distance.read()        #read sensor
            sleep(0.01)                                 #wait 0.01 seconds

if __name__ == '__main__':
    control = Controller()