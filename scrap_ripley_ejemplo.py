""" Scrapping para falabella en smartphones(Celulares y telefonos) """
import requests
from bs4 import BeautifulSoup

# COLORES
AZUL = "\33[1;36m"  # texto azul claro
GRIS = "\33[0;37m"  # texto gris
BLANCO = "\33[1;37m"  # texto blanco


def datos_smarphones(url):
    """Devuelve los datos para smartphone en las web de falabella"""

    # inicialización del diccionario de salida
    data = {}
    # cabeceras de la petición HTTP
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
        "537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"}
    # realizar la petición
    print(f'{AZUL}Realizando la petición: {BLANCO}{url}{GRIS}')
    req = requests.get(url, headers=headers, timeout=10)
    # si petición no fue correcta, devolver error
    if req.status_code != 200:
        return {"Error": f"{req.reason}", "status_code": f"{req.status_code}"}

    # obteniendo datos
    # url del producto
    data["url"] = req.url
    # crear el objeto bs4 a partir del código HTML
    soup = BeautifulSoup(req.text, "html.parser")
    # nombre del producto
    data["productName"] = soup.find("section", class_="product-header").find("h1").text.strip()

    # precio del producto
    data["productPrice"] = soup.find("dt", class_="product-price").text.replace("S/", "").strip().replace(",", "")

    prices_section = soup.find("dl", class_="prices-list")
    price_elements = prices_section.find_all("dt", class_="product-price")

    normal_price = price_elements[0].text.strip()
    discounted_price = price_elements[1].text.strip()

    data["normalPrice"] = normal_price
    data["discountedPrice"] = discounted_price
    try:
       data["marketplace"] = soup.find("a", class_="product-information-shop-name").text.strip()
    except:  # pylint: disable=W0702
       data["marketplace"] = None




    
    # data["Caracteristicas"] = soup.find("a", class_="product-information-shop-name").text.strip()

    return data


if __name__ == '__main__':
    URL = "https://simple.ripley.com.pe/televisor-hisense-32-smart-tv-hd-led-32a4gsv-pmp00002088326?color_80=negro&s=mdco"


    datos = datos_smarphones(URL)
    for clave, valor in datos.items():
        print(f'{AZUL}{clave.upper()}: {BLANCO}{valor}{GRIS}')
