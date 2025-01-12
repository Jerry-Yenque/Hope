import importlib
import os
import re
from datetime import datetime

import nltk
import requests
from fuzzywuzzy import process, fuzz
from nltk import word_tokenize
from nltk.corpus import stopwords
from pymongo.synchronous.cursor import Cursor
from pymongo.synchronous.database import Database

import infrastructure.repository.headphoneRepository
from infrastructure.mongo import MongoConnection
from presentation.theme import VERDE, GRIS, AMARILLO
from src.data.api.taxonomyApi import TaxonomyApi
from src.data.model.Feature import Feature
from src.data.model.Product import Product
from dotenv import load_dotenv
try:
    stopwords.words('spanish')
except LookupError:
    nltk.download('stopwords')
load_dotenv()

# def getHeadphoneDbService() -> Database:
#     """ fuction to get the headphone db service, use it in unit tests """
#     mongo = MongoConnection()
#     return mongo.get_collection("headphones")


features_1 = {
    "ON EAR" : 626,
    "OVER EAR" : 628,
    "IN EAR" : 2551
}
features_2 = {
    "INALÁMBRICOS" : 2552,
    "POR CABLE" : 2553
}
features_3 = {
    "CON CANCELACIÓN DE RUIDO" : 2554,
    "SIN CANCELACIÓN DE RUIDO" : 2555
}


def get_key_from_value(dictionary, value):
    """ Obten el nombre del Feature/1/2/3 dándole el código, none si no está"""
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def normalize_text(text):
    # nltk.download('stopwords')
    # return re.sub(r'\W+', ' ', text).strip().lower()  # this line was the unique in this function
    spanish_stopwords = set(stopwords.words('spanish'))

    custom_stopwords = {"audifonos", "auriculares", "para", "con", "sin", "de", "la", "el", "los", "las", "series",
                        "true", "micrófono", "control", "voz", "alexa", "deportivo", "cancelacion", "ruido",
                        "microfono", "max", "llamadas", "agua", "horas", "musica"}
    all_stopwords = spanish_stopwords.union(custom_stopwords)
    text = re.sub(r'[^\w\s\+\-]', ' ', text)

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.lower() not in all_stopwords]

    # Convertir a minúsculas y unir de nuevo en una cadena
    return ' '.join(tokens).lower()

def find_best_match(title, products):
    normalized_title = normalize_text(title)
    best_match = process.extractOne(normalized_title, products, scorer=fuzz.token_set_ratio)
    return best_match[0] if best_match else "No encontrado"


class HeadphoneRepository:
    def __init__(self, headphoneDbService : Database ) -> None:
        print(f"✅ {VERDE}HeadphoneRepository{GRIS}")
        self.db: Database = headphoneDbService

        for name, method in infrastructure.repository.headphoneRepository.HeadphoneRepository.__dict__.items():
            if callable(method):
                setattr(self, name, method.__get__(self, self.__class__))

    def reload(self):
        """ A beauty method to reload the instance """
        os.system('cls')
        importlib.reload(infrastructure.repository.headphoneRepository)

        methods_names = [name for name, value in self.__dict__.items() if callable(value)] #list(self.__dict__.keys())
        # Limpiar métodos antiguos
        # print(methods_names)
        # # print(f"{BLANCO}Methods of current instance: {existing_methods}{GRIS}")
        # print(f"{AZUL}Methods of updated version: {list(infrastructure.repository.headphoneRepository.HeadphoneRepository.__dict__.keys())}{GRIS}")
        # for method_name in methods_names:
        #     if method_name not in infrastructure.repository.headphoneRepository.HeadphoneRepository.__dict__.keys():
        #         print(f"{ROJO}Deleting method: {method_name}(){GRIS}")
        #         delattr(self, method_name)

        # Actualizar métodos de la clase
        for name, method in infrastructure.repository.headphoneRepository.HeadphoneRepository.__dict__.items():
            # print(name)
            if callable(method):
                if name not in methods_names:
                    print(f"{VERDE}Adding method: {name}(){GRIS}")
                    setattr(self, name, method.__get__(self, self.__class__))
        print(f"{AMARILLO}HeadphoneRepository Reloaded!{GRIS}")

    def get_headphones(self) ->  Cursor:
        return self.db.find({}, {'name': 1, 'brand_id': 1, 'category_id': 1, 'feature_1': 1, 'feature_2': 1, 'feature_3': 1, 'feature_4': 1, 'feature_5': 1, '_id': 0})

    def get_headphones_names(self):
        # Consultar los datos necesarios
        cursor = self.get_headphones()
        standard_products = set()
        headphones = set()
        for document in cursor:
            name = document.get('name', '').strip()
            brand_id: int = document.get("brand_id")
            category_id: int = document.get("category_id")
            feature_1: int = document.get('feature_1')
            feature_2: int = document.get('feature_2')
            feature_3: int = document.get('feature_3')
            feature_4: int = document.get('feature_4')
            feature_5: int = document.get('feature_5')

            if name:
                standard_products.add(str(name))
            if name != '' and feature_1 in features_1.values() and feature_2 in features_2.values() and feature_3 in features_3.values() and feature_4 is None and feature_5 is None:
                product = Product(name = name, brand_id=brand_id, category_id=category_id, feature_1=Feature(feature_1), feature_2=Feature(feature_2), feature_3=Feature(feature_3))
                product.feature_1.name = get_key_from_value(features_1, feature_1)
                product.feature_2.name = get_key_from_value(features_2, feature_2)
                product.feature_3.name = get_key_from_value(features_3, feature_3)
                headphones.add(product)
        standard_products = list(standard_products)
        # for i in headphones:
        #     print(f'{i.name}')
        headphones = list(headphones)
        return standard_products, headphones

    def get_posible_names(self, token: str):
        standard_products, headphones = self.get_headphones_names()
        scraped_titles = self.get_product_card_names(token=token, toPage=1)

        df = []
        # i = 1
        # Procesar los títulos obtenidos
        for title in scraped_titles:
            best_match = find_best_match(title, standard_products)
            df.append(best_match)

        return df

    def get_product_card_names(self, token: str, toPage: int):
        base_url = os.getenv("HOST")
        api = TaxonomyApi(base_url, token)
        current_date = datetime.now().strftime("%Y-%m-%d")
        print(f"current day: {current_date}")
        # body = {
        # "order_by": "id",
        # #"name": "LENOVO",  # para buscar por nombre activa ese campo
        # "asc": 1,
        # "page": 1
        # }

        body = {
            "page": 1,
            "countries": [
                "PE"
            ],
            "retails": [
                "plazavea",
                "tottus",
                "metro",
                "simple-ripley",
                "falabella-pe",
                "lacuracao-pe",
                "oechsle-pe",
                "efe-pe",
                "hiraoka-pe",
                "sodimac-pe",
                "carsa-pe",
                "lg",
                "tailoy-pe",
                "coolbox-pe"
            ],
            "categories": [
                "audifonos",
                "audífonos gamer"
            ],
            "brands": [
                "SONY",
                "JBL",
                "SKULL CANDY",
                "SKULLCANDY",
                "XIAOMI",
                "XIAOMI REDMI",
                "LENOVO",
                "LENOVO / LEMFO",
                "PHILIPS",
                "PHILIPS.",
                "APPLE",
                "HAVIT",
                "BEATS",
                "BEATS BY DR DRE",
                "BEATS BY DR. DRE",
                "BEATS SOLO3",
                "BEATS STUDIO BUDS",
                "BEATS STUDIO3",
                "SAMSUNG",
                "SAMSUNG (AKG)"
            ],
            "start_date": "2025-01-01",
            "end_date": current_date,
            "name": None,
            "last_seen_products": False
        }

        output_data = []


        for i in range(1, toPage + 1):
            print(f'Page {i}')
            body["page"] = i
            try:
                # print(i)
                output_data.extend(api.getPendingProducts(body)["productCards"])
                # print("Response:", result["brands"])
            except requests.exceptions.RequestException as e:
                print("Error:", e)

        print(f'len : {len(output_data)}')
        scraped_titles = []
        for productCard in output_data:
            scraped_titles.append(productCard.product_name)
            # print(f'"{productCard.product_name}",')
        return scraped_titles

