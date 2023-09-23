from abc import ABC, abstractmethod


class AFStrategy(ABC):

    @abstractmethod
    def af(self, theta, phi):
        pass
