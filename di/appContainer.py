from pymongo.synchronous.database import Database

from infrastructure.mongo import MongoConnection
from infrastructure.repository.headphoneRepository import HeadphoneRepository


class AppContainer:
    _instance = None
    def __init__(self) -> None:
        pass

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_dependencies()
        return cls._instance

    def _initialize_dependencies(self):
        # Aquí inicializas todas las dependencias necesarias
        self.mongo = MongoConnection()
        self.headphoneDbService: Database = self.mongo.get_collection("headphones")
        self.headphone_repository = HeadphoneRepository(self.headphoneDbService)
