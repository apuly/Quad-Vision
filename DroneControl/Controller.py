from CommandManager import CommandManager
from pyMultiwii import MultiWii
from ActionManager import ActionManager
from Action import Action
from Camera import Camera
#from DistanceSensor import DistanceSensor
from Symbol import Symbol
from Command import Command
from Commands import *
from Recognition import Recognition
import json
import Load
import threading
import time
import cv2
import sys

class RCData(self):
    MIN = 1000
    MAX = 2000
    
    def __init__(self):
        self._yaw = 1500
        self._pitch = 1500
        self._roll = 1500
        self._throttle = 1000

    @property
    def yaw(self):
        return self._yaw
    @yaw.setter
    def yaw(self, x):
        if MIN > x > MAX:
            raise Exception("RC value not in range")
        else:
            self._yaw = x

    @property
    def pitch(self):
        return self._pitch
    @pitch.setter
    def pitch(self, x):
        if MIN > x > MAX:
            raise Exception("RC value not in range")
        else:
            self._pitch = x

    @property
    def roll(self):
        return self._roll
    @roll.setter
    def roll(self, x):
        if MIN > x > MAX:
            raise Exception("RC value not in range")
        else:
            self._roll = x

    @property
    def throttle(self):
        return self._throttle
    @throttle.setter
    def yaw(self, x):
        if MIN > x > MAX:
            raise Exception("RC value not in range")
        else:
            self._throttle = x

    def toArray(self):
        return [self._pitch, self._roll, self._yaw, self._throttle]


class CameraData(Camera):
    def __init__(self, *args):
        super(CameraData, self).__init__()
        self.image = None
        self.timeStamp = time.time()

    def updateImage(self):
        while True:
            self.image = self.read()[1]
            self.timeStamp = time.time()
            time.sleep(0.05)
    
    def start(self):
        self._updateImageThread = threading.Thread(target = self.updateImage)
        self._updateImageThread.start()


class heightControl(object):
    def __init__(self, rcData):
        self._distance = DistanceSensor(0,0,0)
        self._targetHeight = None
        self._rc = rcData

    def start(self):
        self._thread = threading.Thread(target = self.updateSpeed)
        self._thread.daemon = True
        self._thread.start()

    def updateSpeed(self):
        while self._targetHeight is None:
            pass
        while True:
            speed = (self._targetHeight - self._distance.read()) * 10
            if speed > 300:
                speed = 300
            elif speed < -300:
                speed = -300
            rcData.throttle = speed
            
    @property
    def target(self):
        return self._targetHeight

    @target.setter
    def target(self, x):
        self._targetHeight = x

class Controller(object):
    def __init__(self):
        self.rcData = RCData()
        self.cam = CameraData()
        self.cmdManager = CommandManager()
        self.actionManager = ActionManager()
        self.heightController = heightControl(self.rcData)
        #self.recog = Recognition(self.cam)
        self.symbolList = []
        self.currentCommand = None
        self.board = MultiWii('/dev/ttyUSB0')

        #self.loadActions()
        #self.loadCommands()
        #self.loadSymbols()
        self.Load.loadAction()
        self.Load.loadCommands()
        self.Load.loadSymbols()

        time.sleep(1)
    
    def start(self): #starten van de threading en processen
        self.commandThread = threading.Thread(target = self.commandHandler)
        self.symbolThread = threading.Thread(target = self.compareSymbols)
        self.symbolThread.start()
        self.commandThread.start()

        self.distance.start()
        self.cam.start()

        while True:
            self.board.sendCMD(8, MultiWii.SEND_RAW_RC, self.rcData.toArray())
            time.sleep(0.1)
            
        
    def compareSymbols(self): #vergelijken van images
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
            
    def commandHandler(self): #afhandeling van commando's. 
        while self.currentCommand is None: pass
        
        previousCommand = None
        commandThread = None
        while True:
            if self.currentCommand != previousCommand:
                previousCommand = self.currentCommand
                if commandThread is not None:
                    self.cmdManager.stopCommand()
                    while commandThread.isAlive():
                        pass
                commandThread = threading.Thread(target = self.cmdManager.execute, args = (self.currentCommand,))
                commandThread.start()

if __name__ == '__main__':
    control = Controller()