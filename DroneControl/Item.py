from abc import ABCMeta, abstractmethod, abstractproperty

class Item(object):
    __metaclass__ = ABCMeta

    @abstractmethod
    def execute(self, *args):
        pass

    @abstractproperty
    def binder(self):
        pass