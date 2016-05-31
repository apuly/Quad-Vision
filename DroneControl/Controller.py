from CommandManager import CommandManager
from ActionManager import ActionManager
from Action import Action
from Camera import Camera
#from DistanceSensor import DistanceSensor
from Symbol import Symbol
from Command import Command
from Commands import *
from Recognition import Recognition
import json
import threading
import time
import cv2
import sys

class DistanceSensorData(DistanceSensor):
    def __init__(self, trigPin, echoPin):
        super(DistanceSensorData, self).__init__(trigPin, echoPin)
        self.value = None
        self.dataUpdateThread = threading.Thread(target = self.updateData)
        self.dataUpdateThread.start()
    def updateData(self):
        while True:
            self.value = self.read()
            time.sleep(0.05)


class CameraData(Camera):
    def __init__(self, *args):
        super(CameraData, self).__init__()
        self.image = None
        self.timeStamp = time.time()
        self.updateImageThread = threading.Thread(target = self.updateImage)
        self.updateImageThread.start()

    def updateImage(self):
        while True:
            self.image = self.read()[1]
            self.timeStamp = time.time()
            time.sleep(0.05)

class Controller(object):
    def __init__(self):
        self.cam = CameraData()
        #self.distance = DistanceSensorData(trigpin, echopin)
        self.distance = 8
        self.cmdManager = CommandManager()
        self.actionManager = ActionManager()
        #self.recog = Recognition(self.cam)
        self.symbolList = []
        self.currentCommand = None

        self.loadActions()
        self.loadCommands()
        self.loadSymbols()

        time.sleep(1)

        self.commandThread = threading.Thread(target = self.commandHandler)
        self.commandThread.start()

        self.symbolThread = threading.Thread(target = self.compareSymbols)
        self.compareSymbols.start()
            
            
        
    def compareSymbols(self):
        while self.recog.processedImage is None:
            pass
        oldTimestamp = None
        while True:
            if oldTimestamp != self.recog.timestamp:
                oldTimestamp = self.recog.timestamp
                diffs = [self.recog.compareImage(self.recog.processedImage, symbol.image) for symbol in self.symbolList]
                filteredDiffs = [diff for diff in diffs if diff is not None]
                index = diffs.index(min(filteredDiffs))
                detectedSymbol = self.symbolList[index]
                self.currentCommand = detectedSymbol.command
            
    def commandHandler(self):
        while self.currentCommand is None: pass
        
        previousCommand = None
        commandThread = None
        while True:
            if self.currentCommand != previousCommand:
                previousCommand = self.currentCommand
                if commandThread is not None:
                    self.cmdManager.stopCommand()
                    while commandThread.isAlive():
                        #print commandThread.isAlive()
                        pass
                commandThread = threading.Thread(target = self.cmdManager.execute, args = (self.currentCommand,))
                commandThread.start()
                
 

    def loadActions(self):                                                  #loads actions into actionmanager   
        with open('actions.json') as data_file:    
            actionJson = json.load(data_file)                              #opens JSON file with action data
        for actions in actionJson['actions']:                               
            tempAction = Action(actions['binder'], actions['data'])         #creates actions using data
            self.actionManager.addItem(tempAction)                          #loads data into action manager

    def loadCommands(self):
        from Command import Command
        commands = [cls for cls in vars()['Command'].__subclasses__()]      #gets all classes that extends command class
        for command in commands:
            self.cmdManager.addItem(command(self.actionManager, self.cam, self.distance))       #initiallise commands and add them to command manager

    def loadSymbols(self):                                                  #loads symbols into symbol list
        with open('symbols.json') as data_file:    
            symbolsJson = json.load(data_file)                               #opens JSON file with symbol data
        for symbolData in symbolsJson['symbols']:
            _, image = cv2.threshold(cv2.imread(symbolData['path'], cv2.IMREAD_GRAYSCALE), 100, 255, 0)
            self.symbolList.append(Symbol(image, symbolData['command'])) #reads data from json, loads into symbol list
            

if __name__ == '__main__':
    control = Controller()