import infrastructure.mongo
from pymongo.synchronous.database import Database
from typing import Optional
from pymongo import MongoClient
from dotenv import load_dotenv
import importlib
from presentation.theme import VERDE, GRIS, AMARILLO, ROJO
import os
import threading
load_dotenv()

class MongoConnection:
    def __init__(self) -> None:
        self.db: Optional[Database] = None
        self.connection_string: str = os.getenv("MONGO_HOST")
        self.client: Optional[MongoClient] = None

        if not self.connection_string:
            raise ValueError("La variable de entorno 'MONGO_HOST' no está configurada.")
        self.client = MongoClient(self.connection_string)
        # self.connect()
        try:
            self.client.admin.command("ping")
            self.db = self.client.get_database()
            print(f"✅ {VERDE}Conexión exitosa a MongoDB.{GRIS}")
        except Exception as e:
            print(f"❌ {ROJO}Algo sucedió al conectar a MongoDB.{GRIS}")
        for name, method in infrastructure.mongo.MongoConnection.__dict__.items():
            if callable(method):
                setattr(self, name, method.__get__(self, self.__class__))

    def connect(self):
        """
        Verifica la conexión a MongoDB en un hilo separado.
        """
        def _check():
            try:
                self.client.admin.command("ping")
                self.db = self.client.get_database()
                print(f"✅ {VERDE}Conexión exitosa a MongoDB.{GRIS}")
            except Exception as e:
                print(f"❌ {ROJO}Algo sucedió al conectar a MongoDB.{GRIS}")
                # print(e)

        # Ejecutar la verificación en un hilo
        threading.Thread(target=_check, daemon=True).start()

    def get_collection(self, collection_name: str):
        """ Devuelve una colección específica de la base de datos. """
        return self.db[collection_name]

    def reload(self):
        """ A beauty method to reload the instance """
        os.system('cls')
        importlib.reload(infrastructure.mongo)

        methods_names = [name for name, value in self.__dict__.items() if callable(value)] #list(self.__dict__.keys())
        # Limpiar métodos antiguos
        print(methods_names)
        # print(f"{BLANCO}Methods of current instance: {existing_methods}{GRIS}")
        # print(f"{AZUL}Methods of updated version: {list(mongoConnection.MongoConnection.__dict__.keys())}{GRIS}")
        for method_name in methods_names:
            if method_name not in infrastructure.mongo.MongoConnection.__dict__.keys():
                print(f"{ROJO}Deleting method: {method_name}(){GRIS}")
                delattr(self, method_name)

        # Actualizar métodos de la clase
        for name, method in infrastructure.mongo.MongoConnection.__dict__.items():
            # print(name)
            if callable(method):
                if name not in methods_names:
                    print(f"{VERDE}Adding method: {name}(){GRIS}")
                    setattr(self, name, method.__get__(self, self.__class__))
        print(f"{AMARILLO}MongoConnection Reloaded!{GRIS}")

    def close(self):
        """ Cierra la conexión con MongoDB. """
        if self.client:
            self.client.close()