"""Finder para scrapear, el aliado de Hope"""
from scrap_oechsle_smarthphones import datos_smarphones

class Finder:
    """Mr. Finder te ayudará a scrapear datos de distintos retails"""
    def __init__(self):
        self.data_oechsle = datos_smarphones

if __name__ == '__main__':
    URL = "https://www.oechsle.pe/realme-c11-6-5-2gb-ram-32gb-iron-grey-1914008/p"
    f = Finder()
    datos = f.data_oechsle(URL)
    for clave, valor in datos.items():
        print(f'{clave.upper()}: {valor}')
