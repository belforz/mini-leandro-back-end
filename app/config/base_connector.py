from abc import ABC, abstractmethod

class BaseDatabaseConnector(ABC):

    def __init__(self, db_uri: str, db_name: str):
        self.db_uri = db_uri
        self.db_name = db_name
        self.connection = None

    @abstractmethod
    def connect(self):
        pass

    @abstractmethod
    def close(self):
        pass
