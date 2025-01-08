import csv
from pymongo import MongoClient

AZUL = "\33[1;36m"
GRIS = "\33[0;37m"
BLANCO = "\33[1;37m"
ROJO = "\33[1;31m"
VERDE = "\33[1;32m"

# Configuración de la conexión a MongoDB
uri = "mongodb://localhost:27017/ThirdEye"  # Reemplaza con tu cadena de conexión
client = MongoClient(uri)

# Seleccionar la base de datos y la colección
db = client['ThirdEye']  # Reemplaza con el nombre de tu base de datos
collection = db['headphones']

# Consultar los datos necesarios
cursor = collection.find({}, {'name': 1, 'taxonomy_product.product_name': 1, '_id': 0})

# Abrir un archivo CSV para escribir los datos
with open('headphones.csv', 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    
    # Escribir el encabezado
    csv_writer.writerow(['name', 'productName'])
    
        # Escribir los datos
    for document in cursor:
        name = document.get('name', '').strip()
        product_name = document.get('taxonomy_product', {}).get('product_name', '')
        print(f'{ROJO}{product_name} {AZUL}=====> {VERDE}"{name}"{GRIS}')
        csv_writer.writerow([name, product_name])

print("Datos exportados a headphones.csv")

# Cerrar la conexión a MongoDB
client.close()
