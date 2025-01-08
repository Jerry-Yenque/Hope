""" Scrapping para oechsle en smartphones(Celulares y telefonos) """
import requests
from bs4 import BeautifulSoup

# COLORES
AZUL = "\33[1;36m"  # texto azul claro
GRIS = "\33[0;37m"  # texto gris
BLANCO = "\33[1;37m"  # texto blanco


def datos_smarphones(url):
    """Devuelve los datos para smartphone en las web de oechsle"""

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

    # crear el objeto bs4 a partir del código HTML
    soup = BeautifulSoup(req.text, "html.parser")
    # Obteniendo datos
    # url del producto
    data["url"] = req.url
    # código de respuesta
    data ['status_code'] = req.status_code
    seller, codigo = None, None
    try:
        seller, codigo = soup.find("div", class_="skuReference").text.split("-")
        data["id"] = codigo
        # vendedor del producto
        data["productSeller"] = seller
    except ValueError:
        data['idPosible'] = soup.find("div", class_="skuReference").text
        data['productSeller'] = None

    if data['productSeller'] is None:
        try:
            data['productSeller'] = soup.find('div', {'data-js': 'marketplace-2'}).find('img')['alt'] #pylint: disable=c0301
        except Exception as e: #pylint: disable=c0103, w0718
            print('no img', e)

    # nombre del producto
    data["productName"] = soup.find("h1", attrs={"itemprop": "name"}).text.strip()
    # precio del producto
    try:
        data["productPrice"] = float(soup.find("strong", class_="skuBestPrice").text
                                    .replace("S/.", "").strip().replace(",", ""))
    except Exception as error: # pylint: disable=W0718
        print("-Hope: No encontré el precio del producto\n", error)
    # descuento del producto
    try:
        data["productDiscount"] = float(soup.find(
            "span", class_="economy").text.replace("S/.", "").strip())
    except:  # pylint: disable=W0702
        data["productDiscount"] = None
    # precio sin descuento
    try:
        data["productPriceOld"] = float(soup.find(
            "strong", class_="skuListPrice").text.replace("S/.", "").strip().replace(",", ""))
    except:  # pylint: disable=W0702
        data["productPriceOld"] = None
    # nombre de propiedades del producto
    property_name = []
    list_names = soup.find("div", id="caracteristicas").find_all("th")
    for name in list_names:
        property_name.append(name.text.strip())
    # valor de propiedades del producto
    # data["propertyValue"] = []
    property_value = []
    list_values = soup.find("div", id="caracteristicas").find_all("td")
    for value in list_values:
        property_value.append(value.text.strip())
    data["properties"] = dict(zip(property_name, property_value))
    return data


if __name__ == '__main__':
    URL = "https://www.oechsle.pe/auriculares-intrauditivos-inalambricos-wfc700n-b-sony-unisex-en-negro-1000619282/p"

    datos = datos_smarphones(URL)
    for clave, valor in datos.items():
        print(f'{AZUL}{clave.upper()}: {BLANCO}{valor}{GRIS}')
