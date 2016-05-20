from abc import ABCMeta, abstractmethod, abstractproperty

class AbstractManager(object):
    __metaclass__ = ABCMeta

    @abstractproperty
    def itemList(self):
        pass

    def addItem(self, item):
        pass

    def removeItem(self, item):
        pass

    @abstractmethod
    def execute(self, binder):
        pass

