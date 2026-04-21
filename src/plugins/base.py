from abc import ABC, abstractmethod

class BasePlugin(ABC):
    @abstractmethod
    def execute(self, task_manager):
        pass
