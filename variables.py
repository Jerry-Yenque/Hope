""" variables que usa el bot """
EMAIL = ""
CLAVE = "1234"
FILTRO_PAIS = "Peru"
# Retail por defecto"
# FILTRO_RETAIL = ["oechsle-pe"]
# FILTRO_RETAIL = ["simple-ripley"]
FILTRO_RETAIL = ["plazavea", "tottus", "metro", "simple-ripley", "falabella-pe",
                    "lacuracao-pe", "oechsle-pe", "efe-pe", "hiraoka-pe", "sodimac-pe",
                    "carsa-pe", "lg", "tailoy-pe", "coolbox-pe"]

FILTRO_AREA = "electro"

# Categorias para aspiradoras: 'aspiradoras', 'aspiradoras de robot', 'aspiradoras robot', 'aspiradoras verticales', # pylint: disable=C0301
#       'aspiradoras de tambor', 'aspiradoras portátiles'
# Categorias para celulares: 'celulares'
# Categorias para computo: 'tablets'
# Categorias para audio: 'audifonos', 'audífonos gamer', 'audifonos y manos libres'
# Categorias para video: 'tv', 'monitores'
# FILTRO_CATEGORIA = ['audifonos', 'audífonos gamer', 'audifonos y manos libres']
FILTRO_CATEGORIA = ['colchones']

# divisiones : 'telefonia', 'computo', 'audio', 'video'
FILTRO_DIVISION = ['celulares']
# FILTRO_DIVISION = ['peds']

# Marcas para tablets = 'samsung'
# Marcas para aspiradoras, 'DEERMA', 'irobot', 'karcher', 'electrolux'
# Marcas audifonos : 'samsung', 'sony', 'xiaomi', 'lenovo'
# Marcas para monitores : 'lg', 'hp'
FILTRO_MARCA = ["paraiso"]


dictSeller = { 'ElectronicStore': 'ElectronicsStore',
              'ENVIOSUSAPERU': 'ENVIOSUSAPERU',
              'Umut': 'Umut'}
