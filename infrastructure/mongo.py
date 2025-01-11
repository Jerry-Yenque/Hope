import mongo
from pymongo import MongoClient
from dotenv import load_dotenv
import importlib
from presentation.theme import VERDE, GRIS, AMARILLO, ROJO, AZUL, BLANCO
import os
load_dotenv()
A = 3

class MongoConnection:
    def __init__(self, uri):
        self.client = MongoClient(uri)

    # def reload(self):
    #     """ A beaty method to reload the instance """
    #     os.system('cls')
    #     importlib.reload(mongoConnection)
    #     for name, method in mongoConnection.MongoConnection.__dict__.items():
    #         if callable(method):
    #             setattr(self, name, method.__get__(self, self.__class__))
    #     print(f"{AMARILLO}MongoConnection Reloaded!{GRIS}")

    def reload(self):
        """ A beauty method to reload the instance """
        os.system('cls')
        importlib.reload(mongo)

        # Limpiar métodos antiguos
        existing_methods = list(self.__dict__.keys())
        # print(f"{BLANCO}Methods of current instance: {existing_methods}{GRIS}")
        # print(f"{AZUL}Methods of updated version: {list(mongoConnection.MongoConnection.__dict__.keys())}{GRIS}")
        for method_name in existing_methods:
            if method_name not in mongo.MongoConnection.__dict__.keys():
                print(f"{ROJO}Deleting method: {method_name}(){GRIS}")
                delattr(self, method_name)

        # Actualizar métodos de la clase
        for name, method in mongo.MongoConnection.__dict__.items():
            if callable(method):
                if name not in existing_methods:
                    print(f"{VERDE}Adding method: {name}(){GRIS}")
                setattr(self, name, method.__get__(self, self.__class__))
        print(f"{AMARILLO}MongoConnection Reloaded!{GRIS}")


    def hola7(self):
        print(A)
