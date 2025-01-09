import re
from fuzzywuzzy import fuzz, process
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from src.data.api.taxonomyApi import TaxonomyApi
import csv
from pymongo import MongoClient
import requests
from dotenv import load_dotenv
from src.data.model.Product import Product
from src.data.model.Feature import Feature
from nltk.corpus import stopwords
import nltk
from nltk.tokenize import word_tokenize
from presentation.theme import AZUL, ROJO, VERDE, BLANCO, GRIS
from datetime import datetime
load_dotenv()

try:
    stopwords.words('spanish')
except LookupError:
    nltk.download('stopwords')

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


client = MongoClient(os.getenv("MONGO_HOST"))

# Seleccionar la base de datos y la colección
db = client['ThirdEye']  # Reemplaza con el nombre de tu base de datos
collection = db['headphones']

def getHeadphonesNames():
    # Consultar los datos necesarios
    cursor = collection.find({}, {'name': 1, 'brand_id': 1, 'category_id': 1, 'feature_1': 1, 'feature_2': 1, 'feature_3': 1, 'feature_4': 1, 'feature_5': 1, '_id': 0})

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
                standard_products.add(name)
            if name != '' and feature_1 in features_1.values() and feature_2 in features_2.values() and feature_3 in features_3.values() and feature_4 == None and feature_5 == None:
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

def get_key_from_value(dictionary, value):
    """ Obten el nombre del Feature/1/2/3 dándole el código, none si no está"""
    for key, val in dictionary.items():
        if val == value:
            return key
    return None

def find_product_by_name(best_match, headphones):
    clean_dict = {}
    for product in headphones:
        if product.name == best_match:
            print(f'{VERDE}{product.name} {BLANCO}| {get_key_from_value(features_1, product.feature_1.id)} |  {get_key_from_value(features_2, product.feature_2.id)} | {get_key_from_value(features_3, product.feature_3.id)}\n')
            clean_dict = product.to_dict()
            print(clean_dict, end='\n')
    return clean_dict

def normalize_text(text):
    # nltk.download('stopwords')
    # return re.sub(r'\W+', ' ', text).strip().lower()  # this line was the unique in this function 
    spanish_stopwords = set(stopwords.words('spanish'))

    custom_stopwords = set([
        "audifonos", "auriculares", "para", "con", "sin", "de", "la", "el", "los", "las",
        "series", "true", "micrófono", "control", "voz", "alexa", "deportivo", "cancelacion", "ruido", "microfono", "max", "llamadas",
        "agua", "horas", "musica"
    ])
    
    all_stopwords = spanish_stopwords.union(custom_stopwords)
    text = re.sub(r'[^\w\s\+\-]', ' ', text)

    tokens = word_tokenize(text)
    tokens = [word for word in tokens if word.lower() not in all_stopwords]
    
    # Convertir a minúsculas y unir de nuevo en una cadena
    return ' '.join(tokens).lower()

# Extraer color del título
def extract_color(title):
    colors = ["blanco", "azul", "gris", "negro", "rojo", "verde", "rosa", "amarillo", "celeste"] # Añadir más colores según tu lista
    for color in colors:
        if color in title.lower():
            return color.capitalize()
    return "No especificado"

# Encontrar la mejor coincidencia para el producto
def find_best_match(title, products):
    normalized_title = normalize_text(title)
    best_match = process.extractOne(normalized_title, products, scorer=fuzz.token_set_ratio)
    return best_match[0] if best_match else "No encontrado"


def getProductCardNames(token: str, toPage: int):
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

    outputData = []


    for i in range(1, toPage + 1):
        print(f'Page {i}')
        body["page"] = i
        try:
            # print(i)
            outputData.extend(api.getPendingProducts(body)["productCards"])
            # print("Response:", result["brands"])
        except requests.exceptions.RequestException as e:
            print("Error:", e)

    print(f'len : {len(outputData)}')
    scraped_titles = []
    for productCard in outputData:
        scraped_titles.append(productCard.product_name)
        # print(f'"{productCard.product_name}",')
    return scraped_titles


def paintOutput(productCardTitle, bestMatch):
    title1_lower = productCardTitle.lower()
    title2_words = bestMatch.split()

    # Resaltar las coincidencias en productCardTitle
    highlighted_title1 = productCardTitle
    for word in title2_words:
        if word.lower() in title1_lower:
            highlighted_title1 = highlighted_title1.replace(word, f"{VERDE}{word}{GRIS}")

    # Inicializar una lista para almacenar las palabras con colores para productTitle
    highlighted_words_title2 = []

    # Dividir el segundo título en palabras y comprobar cada una en el primer título
    for word in title2_words:
        if word.lower() in title1_lower:
            highlighted_words_title2.append(f"{VERDE}{word}{GRIS}")
        else:
            highlighted_words_title2.append(f"{ROJO}{word}{GRIS}")

    # Unir las palabras resaltadas en una cadena para productTitle
    highlighted_title2 = " ".join(highlighted_words_title2)
    # print(f"Título: {highlighted_title1}{GRIS}")
    # print(f"{highlighted_title2}{GRIS}")
    return highlighted_title1, highlighted_title2


def getPosibleNames(token: str):
    standard_products, headphones = getHeadphonesNames()
    scraped_titles = getProductCardNames(token=token, toPage=1)

    df = []
    # i = 1
    # Procesar los títulos obtenidos
    for title in scraped_titles:
        best_match = find_best_match(title, standard_products)
        df.append(best_match)

        # color = extract_color(title)
        # if((i-1)%20 == 0):
        #     print(f"{AZUL}Página: {(i+20)//20}{GRIS}")
        
        # if color != "No especificado":
        #     print(f'{BLANCO}{i} - {AZUL}Contiene color {color}{GRIS}')
        # else:
        #     print(f'{BLANCO}{i} - {ROJO}No contiene color{GRIS}')

        # title, product_match = paintOutput(title, best_match)
        # print(f"{BLANCO}Título: {title}{GRIS}")
        # if (i%2 == 1):
        #     print(f"{AZUL}{product_match}{GRIS}")
        # else:
        #     print(f"{BLANCO}{product_match}{GRIS}")
        # print(f"Color: {color}")
        # # product_to_taxonomy =  find_product_by_name(best_match, headphones)
        # i +=1

    return df




if __name__ == "__main__":
    standard_products, headphones = getHeadphonesNames()
    scraped_titles = getProductCardNames("", toPage=1)

    df = []
    i = 1
    # Procesar los títulos obtenidos
    for title in scraped_titles:
        best_match = find_best_match(title, standard_products)
        df.append(best_match)

        color = extract_color(title)
        if((i-1)%20 == 0):
            print(f"{AZUL}Página: {(i+20)//20}{GRIS}")
        
        if color != "No especificado":
            print(f'{BLANCO}{i} - {AZUL}Contiene color {color}{GRIS}')
        else:
            print(f'{BLANCO}{i} - {ROJO}No contiene color{GRIS}')

        title, product_match = paintOutput(title, best_match)
        print(f"{BLANCO}Título: {title}{GRIS}")
        if (i%2 == 1):
            print(f"{AZUL}{product_match}{GRIS}")
        else:
            print(f"{BLANCO}{product_match}{GRIS}")
        print(f"Color: {color}")
        # product_to_taxonomy =  find_product_by_name(best_match, headphones)
        i +=1

    df
