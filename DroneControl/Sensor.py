from abc import ABCMeta, abstractmethod

class Sensor(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def read(self):
        pass