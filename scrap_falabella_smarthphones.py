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
    # id del producto en la web del scrapping(falabella)
    data["id"] = data["url"].split("/")[-1]
    # crear el objeto bs4 a partir del código HTML
    soup = BeautifulSoup(req.text, "html.parser")
    # nombre del producto
    data["productName"] = soup.find("div", class_="product-name").text.strip()
    # precio del producto
    data["productPrice"] = float(soup.find("span", class_="copy12").text.replace(
        "S/", "").strip().replace(",", ""))
    # descuento del producto
    try:
        data["productDiscount"] = int(soup.find(
            "div", class_="discount-badge").text.replace("-", "").replace("%", "").strip())
    except:  # pylint: disable=W0702
        data["productDiscount"] = None
    # precio sin descuento
    try:
        data["productPriceOld"] = float(soup.find(
            "span", class_="copy1").text.replace("S/", "").strip().replace(",", ""))
    except:  # pylint: disable=W0702
        data["productPriceOld"] = None
    # vendedor del producto
    data["productSeller"] = soup.find(
        id="testId-SellerInfo-sellerName").text.strip()
    # nombre de propiedades del producto
    # data["propertyName"] = []
    property_name = []
    list_names = soup.find(
        "table", class_="specification-table").find_all("td", class_="property-name")
    for name in list_names:
        # data["propertyName"].append(name.text.strip())
        property_name.append(name.text.strip())
    # valor de propiedades del producto
    # data["propertyValue"] = []
    property_value = []
    list_values = soup.find(
        "table", class_="specification-table").find_all("td", class_="property-value")
    for value in list_values:
        # data["propertyValue"].append(value.text.strip())
        property_value.append(value.text.strip())
    data["properties"] = dict(zip(property_name, property_value))
    return data


if __name__ == '__main__':
    URL = "https://www.falabella.com.pe/falabella-pe/product/"
    "119684620/Reacondicionado-apple-iphone-11-128gb-a2111-purpura/119684621"

    datos = datos_smarphones(URL)
    for clave, valor in datos.items():
        print(f'{AZUL}{clave.upper()}: {BLANCO}{valor}{GRIS}')
