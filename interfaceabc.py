from abc import ABC, abstractmethod

class AbstractClassExample(ABC):

    @abstractmethod
    def do_something(self):
        pass

class InterfaceExample(ABC):

    @abstractmethod
    def method1(self):
        pass

    @abstractmethod
    def method2(self):
        pass

