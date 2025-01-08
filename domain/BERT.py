import re
from transformers import BertTokenizer, BertModel
import torch
from scikit_learn.metrics.pairwise import cosine_similarity
import numpy as np

# Inicializar el modelo BERT y el tokenizer
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased')
model = BertModel.from_pretrained('bert-base-uncased')

# Lista ampliada y normalizada de nombres de productos estandarizados
standard_products = [
    "jbl tune 115 blanco",
    "jbl tune 115bt azul",
    "jbl tune 115bt blanco",
    "jbl tune 115bt gris",
    "jbl tune 115bt negro",
    "jbl tune 720 negro",
    "jbl tune 510bt blanco",
    "jbl tune 520bt",
    "jbl vibe 200tws azul",
    # Añadir más productos según tu lista
]

# Normalización de texto
def normalize_text(text):
    return re.sub(r'\W+', ' ', text).strip().lower()

# Extraer color del título
def extract_color(title):
    colors = ["blanco", "azul", "gris", "negro", "rojo", "verde", "rosa"]
    for color in colors:
        if color in title.lower():
            return color.capitalize()
    return "No especificado"

# Tokenización y obtención de embeddings BERT
def get_bert_embeddings(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True, max_length=128)
    outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).detach().numpy()
    return embeddings

# Encontrar la mejor coincidencia para el producto
def find_best_match(title, products):
    title_embedding = get_bert_embeddings(normalize_text(title))
    best_match = None
    best_score = -1

    for product in products:
        product_embedding = get_bert_embeddings(normalize_text(product))
        score = cosine_similarity(title_embedding, product_embedding)[0][0]
        if score > best_score:
            best_score = score
            best_match = product

    return best_match, best_score

def main():
    # Lista de títulos de productos obtenidos mediante scraping
    scraped_titles = [
        "AUDIFONOS BLUETOOTH JBL VIBE 200 TWS PURE BASS 20HRS - AZUL",
        "JBL TUNE 510BT: AUDIFONOS INALAMBRICOS CON SONIDO PUREBASS, COLOR BLANCO",
        "AUDIFONO JBL OVER EAR BLUETOOTH TUNE 720 NEGRO",
    ]

    # Procesar los títulos obtenidos
    for title in scraped_titles:
        best_match, score = find_best_match(title, standard_products)
        color = extract_color(title)
        print(f"Título: {title}")
        print(f"Coincidencia: {best_match}")
        print(f"Color: {color}")
        print(f"Score: {score}\n")

if __name__ == "__main__":
    main()
