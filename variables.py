""" variables que usa el bot """
EMAIL = ""
CLAVE = "1234"
FILTRO_PAIS = "Peru"
# Retail por defecto"
FILTRO_RETAIL = ["oechsle-pe"]
# FILTRO_RETAIL = ["plazavea", "tottus", "metro", "simple-ripley", "falabella-pe",
#                     "lacuracao-pe", "oechsle-pe", "efe-pe", "hiraoka-pe", "sodimac-pe",
#                     "carsa-pe", "lg", "tailoy-pe", "coolbox-pe"]

FILTRO_AREA = "electro"

# Categorias para aspiradoras: 'aspiradoras', 'aspiradoras de robot', 'aspiradoras robot', 'aspiradoras verticales', # pylint: disable=C0301
#       'aspiradoras de tambor', 'aspiradoras portátiles'
# Categorias para celulares: 'celulares'
# Categorias para computo: 'tablets'
# Categorias para audio: 'audifono'
# Categorias para video: 'tv'
FILTRO_CATEGORIA = ['tablets']

# divisiones : 'telefonia', 'computo', 'audio'
FILTRO_DIVISION = ['computo']

# Marcas para tablets = 'samsung'
# Marcas para aspiradoras, 'DEERMA', 'irobot', 'karcher', 'electrolux'
# Marcas audifonos : 'samsung', 'sony', 'xiaomi', 'lenovo'
FILTRO_MARCA = ["lenovo"]


dictSeller = { 'ElectronicStore': 'ElectronicsStore',
              'ENVIOSUSAPERU': 'ENVIOSUSAPERU',
              'Umut': 'Umut'}
