from abc import ABC, abstractmethod

class ICommand(ABC):
    @abstractmethod
    def execute(self):
        """
        Encapsulated command logic
        """
        pass
