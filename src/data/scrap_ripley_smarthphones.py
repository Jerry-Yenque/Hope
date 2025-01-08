""" Scrapping para ripley en smartphones(Celulares y telefonos) """
import requests
from bs4 import BeautifulSoup

# session = requests.Session()

# COLORES
AZUL = "\33[1;36m"  # texto azul claro
GRIS = "\33[0;37m"  # texto gris
BLANCO = "\33[1;37m"  # texto blanco


def datos_ripley(url):
    """Devuelve los datos para smartphone en las web de ripley"""

    # inicialización del diccionario de salida
    data = {}
    # cabeceras de la petición HTTP
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36",
        "Accept-Language": "es-ES,es;q=0.9",
        "Accept-Encoding": "gzip, deflate, br, zstd",
        "Referer": "https://simple.ripley.com.pe",
        "authority": "simple.ripley.com.pe",
        "Upgrade-Insecure-Requests": "1"
    }
    # realizar la petición
    print(f'{AZUL}Realizando la petición: {BLANCO}{url}{GRIS}')
    req = requests.get(url, timeout=10)
    # si petición no fue correcta, devolver error
    if req.status_code != 200:
        return {"Error": f"{req.reason}", "status_code": f"{req.status_code}"}
    print("Status code:", req.status_code)
    # with open("archivo.html", "w", encoding="utf-8") as f:
    #     f.write(req.text)
    # crear el objeto bs4 a partir del código HTML
    soup = BeautifulSoup(req.text, "html.parser")
    # Obteniendo datos
    # url del producto
    data["url"] = req.url
    # código de respuesta
    data['status_code'] = req.status_code
    # id-sku
    data['id'] = soup.find_all('span', class_='sku-value')[1].text.strip()
    # vende-door
    try:
        data["productSeller"] = soup.find("a", class_="product-information-shop-name").text.strip()
    except:  # pylint: disable=W0702
        data["productSeller"] = None
    # nombre del producto
    data["productName"] = soup.find("section", class_="product-header").find("h1").text.strip()
    # precio del producto
    try:
        prices_section = soup.find("dl", class_="prices-list")
        price_elements = prices_section.find_all("dt", class_="product-price")
    except Exception: # pylint: disable=W0718
        print('price table error')

    try:
        data["productPrice"] = float(price_elements[1].text.replace("S/", "").strip()
                                     .replace(",", ""))
        data["productPriceOld"] = float(price_elements[0].text.replace("S/", "").strip()
                                    .replace(",", ""))
        data["productDiscount"] = data["productPriceOld"] - data["productPrice"]
    except IndexError:
        print('Price Error')
    except Exception:
        print("Some error with price")
    return data


if __name__ == '__main__':
    #https://simple.ripley.com.pe/audifonos-jbl-c50hi-azul-pmp20000010526?sein=todo_audifonos&color_80=azul&s=mdco
    #https://simple.ripley.com.pe/audifonos-samsung-handsfree-akg-s10s10e-jack-35mm-blanco-pmp20000048938?sein=todo_audifonos&color_80=blanco&s=mdco
    #https://simple.ripley.com.pe/audifonos-bluetooth-skullcandy-jib-true-wireless-gris-lentes-de-regalo-pmp20000056008?sein=todo_audifonos&s=mdco
    
    URL = "https://simple.ripley.com.pe/auriculares-sony-inalambricos-wh-ch520-pmp20000331578?sein=todo_audifonos"
    datos = datos_ripley(URL)
    for clave, valor in datos.items():
        print(f'{AZUL}{clave.upper()}: {BLANCO}{valor}{GRIS}')
