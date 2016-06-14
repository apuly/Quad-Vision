from CommandManager import CommandManager
from Command import Command
from ActionManager import ActionManager
from Action import Action
import json
import cv2

#class voor de load
class Load(object):
    actionManager = ActionManager()
    def loadActions(self):                                                  #loads actions into actionmanager   
        with open('actions.json') as data_file:    
            actionJson = json.load(data_file)                              #opens JSON file with action data
        for actions in actionJson['actions']:                               
            tempAction = Action(actions['binder'], actions['data'], self.rcData)         #creates actions using data
            actionManager.addItem(tempAction)                          #loads data into action manager
        return actionManager

    def loadCommands(self):
        cmdManager = CommandManager();
        commands = [cls for cls in vars()['Command'].__subclasses__()]      #gets all classes that extends command class
        for command in commands:
            cmdManager.addItem(command(self.actionManager, self.cam, self.heightController))       #initiallise commands and add them to command manager

    def loadSymbols(self):                                                  #loads symbols into symbol list
        symbolList = symbolList();
        with open('symbols.json') as data_file:    
            symbolsJson = json.load(data_file)                               #opens JSON file with symbol data
        for symbolData in symbolsJson['symbols']:
            _, image = cv2.threshold(cv2.imread(symbolData['path'], cv2.IMREAD_GRAYSCALE), 100, 255, 0)
            symbolList.append(Symbol(image, symbolData['command'])) #reads data from json, loads into symbol list