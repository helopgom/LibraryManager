from abc import ABC, abstractmethod


class BaseModel(ABC):

    def __init__(self):
        self.connection = None

    @abstractmethod
    def create(self):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def update(self):
        pass

    @abstractmethod
    def delete(self):
        pass
