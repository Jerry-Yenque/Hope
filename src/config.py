""" Configure your settings """

# País por defecto
FILTRO_PAIS = "Peru"

# Retail(s) por defecto"
FILTRO_RETAIL = ["plazavea", "tottus", "metro", "simple-ripley", "falabella-pe",
                    "lacuracao-pe", "oechsle-pe", "efe-pe", "hiraoka-pe", "sodimac-pe",
                    "carsa-pe", "lg", "tailoy-pe", "coolbox-pe"]

FILTRO_RETAIL_MARKETPLACE = ["simple-ripley", "oechsle-pe"]

FILTRO_AREA = "electro"

# Categorias para aspiradoras: 'aspiradoras', 'aspiradoras de robot', 'aspiradoras robot', 'aspiradoras verticales', # pylint: disable=C0301
#       'aspiradoras de tambor', 'aspiradoras portátiles'
# Categorias para celulares: 'celulares'
# Categorias para computo: 'tablets'
# Categorias para audio: 'audifonos', 'audífonos gamer', 'audifonos y manos libres'
# Categorias para video: 'tv', 'monitores'
FILTRO_CATEGORIA = ['audifonos', 'audífonos gamer']
# FILTRO_CATEGORIA = ['celulares']

# divisiones : 'telefonia', 'computo', 'audio', 'video'
# FILTRO_DIVISION = ['celulares']
FILTRO_DIVISION = ['audio']

# Marcas para tablets = 'samsung'
# Marcas para aspiradoras, 'DEERMA', 'irobot', 'karcher', 'electrolux'
# Marcas audifonos : 'samsung', 'sony', 'xiaomi', 'lenovo'
# Marcas para monitores : 'lg', 'hp'
FILTRO_MARCA = {
    "SONY": "SONY",
    "JBL": "JBL",  # Lista de valores
    "SKULL": ["SKULL CANDY", "SKULLCANDY"],
    "XIAOMI": ["XIAOMI", "XIAOMI REDMI"],
    "LENOVO": ["LENOVO", "LENOVO / LEMFO"],
    "PHILIPS": ["PHILIPS", "PHILIPS."],
    "APPLE": "APPLE",
    "HAVIT": "HAVIT",
    "BEATS": ["BEATS", "BEATS BY DR DRE", "BEATS BY DR. DRE", "BEATS SOLO3", "BEATS STUDIO BUDS", "BEATS STUDIO3"],
    "SAMSUNG": ["SAMSUNG", "SAMSUNG (AKG)"]
}

FILTRO_MARCA_2 = {
    "BOSE": "BOSE",
    "BANG": ["BANG & OLUFSEN", "BANG &AMP; OLUFSEN"],
    "DENON": "DENON",
    "JABRA": "JABRA",
    "TIMEKETTLE": "TIMEKETTLE",
    "PIONEER": ["PIONEER", "PIONEER DJ"],
    "SENNHEISER": ["SENNHEISER", "SENNHEISER PRO AUDIO"],
    "TECHNICS": "TECHNICS",
    "SHOKZ": "SHOKZ",
    "SHURE": "SHURE"
}

