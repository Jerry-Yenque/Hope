import mongo
from pymongo import MongoClient
from dotenv import load_dotenv
import importlib
from presentation.theme import VERDE, GRIS, AMARILLO, ROJO, AZUL, BLANCO
import os
load_dotenv()

class MongoConnection:
    def __init__(self) -> None:
        load_dotenv()
        self.host = os.getenv("MONGO_HOST")  # Valor por defecto si no se encuentra
        # self.db_name = os.getenv("")       # Valor por defecto si no se encuentra
        # self.client = None
        self.db = None
        for name, method in mongo.MongoConnection.__dict__.items():
            if callable(method):
                setattr(self, name, method.__get__(self, self.__class__))
        # pprint(self.__dict__)

    def connect(self):
        try:
            # self.client = MongoClient(self.uri)
            self.db = MongoClient(self.host)
            # self.db = self.client[self.db_name]
            print(f"{VERDE}Conexión exitosa a MongoDB{GRIS}")
        except Exception as e:
            print(f"Error al conectar a MongoDB: {e}")

    def reload(self):
        """ A beauty method to reload the instance """
        os.system('cls')
        importlib.reload(mongo)

        methods_names = [name for name, value in self.__dict__.items() if callable(value)] #list(self.__dict__.keys())
        # Limpiar métodos antiguos
        print(methods_names)
        # print(f"{BLANCO}Methods of current instance: {existing_methods}{GRIS}")
        # print(f"{AZUL}Methods of updated version: {list(mongoConnection.MongoConnection.__dict__.keys())}{GRIS}")
        for method_name in methods_names:
            if method_name not in mongo.MongoConnection.__dict__.keys():
                print(f"{ROJO}Deleting method: {method_name}(){GRIS}")
                delattr(self, method_name)

        # Actualizar métodos de la clase
        for name, method in mongo.MongoConnection.__dict__.items():
            # print(name)
            if callable(method):
                if name not in methods_names:
                    print(f"{VERDE}Adding method: {name}(){GRIS}")
                    setattr(self, name, method.__get__(self, self.__class__))
        print(f"{AMARILLO}MongoConnection Reloaded!{GRIS}")
