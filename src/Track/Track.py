from abc import ABC, abstractmethod

class Track(ABC):

    @abstractmethod
    def rotate(self, angle):
        pass

    @abstractmethod
    def move(self, distance):
        pass