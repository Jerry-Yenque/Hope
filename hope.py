"""Welcome to HopeBot, this is the last hope project"""
import os
import time
# from webdriver_manager.chrome import ChromeDriverManager #para descargar por code el Driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait # para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as ec # para condiciones en selinium
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import finder
from variables import EMAIL, CLAVE, FILTRO_PAIS, FILTRO_RETAIL, FILTRO_AREA , FILTRO_DIVISION, FILTRO_CATEGORIA, FILTRO_MARCA # pylint: disable=C0301

AZUL = "\33[1;36m"  # texto azul claro
GRIS = "\33[0;37m"  # texto gris
BLANCO = "\33[1;37m"  # texto blanco
ROJO = "\33[1;31m"
VERDE = "\33[1;32m"

class Hope:
    """ Clase que representa el bot de 'The last hope project' """
    def __init__(self):
        os.system('cls')
        # print("\n\nBienvenido a The last Hope Project, un bot asistente"
            #   " que puede ser tu ultima esperanza...", end='\n\n')
        # VARIABLES
        self.retails = FILTRO_RETAIL
        self.categorias = FILTRO_CATEGORIA
        self.marcas = FILTRO_MARCA
        self.divisiones = FILTRO_DIVISION
        self.areas = FILTRO_AREA

        self.finder = finder.Finder()
        # end VARIABLES
        ruta_driver = r'C:\Program Files (x86)\chromedriver.exe'
        # Instalación de ChromeDriver, devuelve la ruta completa
        # (si ya esta instalado solo devuelve la ruta)
        # ruta_driver = ChromeDriverManager(path="./chromedriver").install()
        # Creamos y asignamos la variable a un objeto Service que contiene la ruta del webdriver
        driver_service = Service(ruta_driver)
        # Establecer las opciones del navegador
        options = Options()
        user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/"
        "537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36"
        options.add_argument(f"user_agent={user_agent}")
        # options.add_argument("--headless") # ejecutar chrome sin abrir la ventana
        # options.add_argument("--window-size=1000,1000")  # width and height
        options.add_argument("--start-maximized")  # ventana maximizada
        options.add_argument("--disable-web-security")
        options.add_argument("--disable-extensions")
        options.add_argument("--disable-notifications")
        # Sin aviso de "Su conexión no es privada"
        options.add_argument("--ignore-certificate-errors")
        options.add_argument("--no-sandbox")
        # ChromeDriver no muestra nd en terminal
        options.add_argument("--log-level=3")
        # contenido no seguro
        options.add_argument("--allow-running-insecure-content")
        options.add_argument("--no-default-browser-check")
        options.add_argument("--no-first-run")
        options.add_argument("--no-proxy-server")
        options.add_argument("--disabled-blink-features=AutomationControlled")
        # options.add_argument("--force-device-scale-factor=0.70") # esto controla el zoom

        # Parametros a omitir
        exp_opt = [
            # No muestra 'Un software automatizado de prueba...
            'enable-automation',
            'ignore-certificate-errors',  # Para ignorar errores de certificados
            'enable-logging'  # No muestra en terminal "DevTools listening on.."
        ]
        options.add_experimental_option("excludeSwitches", exp_opt
                                        )
        # Parametros de preferencias en chromedriver
        prefs = {
            # notificaciones: 0=preguntar | 1=permitir | 2=no permitir
            "profile.default_content_setting_values.notifications": 2,
            "intl.accept_languages": ["es-PE", "es"],  # idioma del navegador
            "credentials_enable_service": False  # no muestra "quiere guardar contraseña"
        }
        options.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(
            service=driver_service, options=options)
        # tiempo de espera hasta que el elemento esté disponible
        self.wait = WebDriverWait(self.driver, 10)
        print(f"{AZUL}HOPE: {BLANCO}Hola!, cómo puedo ayudarte?{GRIS}")
        print(f"{BLANCO}\tEl método .taxonomizar() te llevará a taxonomizar según tus filtros pre establecidos") # pylint: disable=C0301
        print(f"\tEl método .marketplace() te llevará a marketplacear según tus filtros pre establecidos{GRIS}\n") #pylint: disable=C0301
        self.login()
    # Getters and Setters
    def setRetail(self, retails): # pylint: disable=C0103
        """Se espera un arreglo de los retails para usar como filtro"""
        self.retails = retails
    def setCategoria(self, categorias): # pylint: disable=c0103
        """Se espera un arreglo de las categorias para usar como filtro"""
        self.categorias = categorias
    def setMarca(self, marcas): # pylint: disable=c0103
        """Se espera un arreglo de las marcas para usar como filtro"""
        self.marcas = marcas
    def addMarca(self, newMarca): # pylint: disable=c0103
        """Agregar un marca al arreglo de marcas para filtro"""
        self.marcas.append(newMarca)
    def setDivision(self, divisiones): # pylint: disable=c0103
        """Se espera un arreglo de las divisioens para usar como filtro"""
        self.divisiones = divisiones
    def setArea(self, areas): # pylint: disable=c0103
        """Se espera un arreglo de las áreas para usar como filtro"""
        self.areas = areas
    # end Getters and Setters

    def login(self, email=EMAIL, clave=CLAVE):
        """ Acceso automatico """
        self.driver.get("https://to-platform-v2-pd.lexartlabs.com/#/login")
        self.driver.find_element("css selector", "#login").send_keys(email)
        self.driver.find_element("css selector", "#password").send_keys(clave)
        self.driver.find_element("xpath", '//input[@value="Log In"]').send_keys(Keys.RETURN)

    def __nav_click(self, section, item):
        """ Dar click de acuerdo a la sección y a su item """
        try:
            self.wait.until(ec.presence_of_all_elements_located(('css selector', 'p[data-v-f95f071e]'))) # pylint: disable=C0301
        except TimeoutException:
            print(f"{AZUL}HOPE: {BLANCO}Tiempo de espera para click en pendiente agotado.{GRIS}")
        else:
            self.driver.get(f"https://to-platform-v2-pd.lexartlabs.com/#/{section}/{item}")

    def __filtro_pais(self, pais=FILTRO_PAIS):
        """ LLenado del filtro pais """
        self.driver.find_element(
            "css selector", "div.custom-dropdown").click()
        try:
            self.wait.until(ec.element_to_be_clickable(
                ("xpath", f"//li[@aria-label='{pais}']"))).click()
        except TimeoutException:
            print(f"{AZUL}Hope: {ROJO} No se puedo autocompletar el fitro = '{pais}'")
            return -1
        return 1

    def __filtro_retail(self, retails=None):
        """LLenado del filtro retail"""
        if retails is None:
            retails = self.retails
        self.driver.find_element("css selector", "div.p-multiselect-label").click()
        for retail in retails:
            try:
                self.wait.until(ec.element_to_be_clickable(
                    ("xpath", f"//li[@aria-label='{retail}']"))).click()
            except TimeoutException:
                print(f"{AZUL}Hope: {ROJO} No se puedo autocompletar el fitro = '{retail}'")
                return -1
        self.driver.find_element(
            "css selector", "div.p-multiselect-label").click()
        return 1

    def __filtro_categoria(self, categorias=None):
        """Llenado del filtro categorias"""
        if categorias is None:
            categorias = self.categorias
        self.driver.find_elements("css selector", "div.p-multiselect-label")[1].click()
        for categoria in categorias:
            try:
                self.wait.until(ec.element_to_be_clickable(
                    ("xpath", f"//li[@aria-label='{categoria}']"))).click()
            except TimeoutException:
                print(f"fitro {categoria} no cargó")
                return -1
        self.driver.find_elements("css selector", "div.p-multiselect-label")[1].click()
        return 1

    # def __filtro_marca(self, marcas = None):
    #     """Llenado del filtro marcas"""
    #     if marcas is None:
    #         marcas = self.marcas
    #     search = self.driver.find_elements("css selector", "div.p-multiselect-label")[2]
    #     search.click()
    #     for marca in marcas:
    #         try:
    #             search = self.wait.until(ec.element_to_be_clickable(
    #                 ("xpath", f"//li[@aria-label='{marca}']")))
    #             search.click()
    #         except TimeoutException:
    #             print(f"fitro {marca} no cargó")
    #             return -1
    #     search = self.driver.find_elements("css selector", "div.p-multiselect-label")[2]
    #     search.click()
    #     return 1

    def __filtro_area(self, areas=None):
        """LLenado del filtro areas"""
        if areas is None:
            areas = self.areas
        search = self.driver.find_element(
            "css selector", 'input[placeholder="Area"] + button')
        search.click()
        try:
            search = self.wait.until(ec.element_to_be_clickable(
                ("xpath", f"//li[contains(text(), '{areas}')]")))
        except TimeoutException:
            print(f"fitro {areas} no cargó")
            return -1
        search.click()
        return 1

    def __filtro_division(self, divisiones=None):
        """LLenado del filtro divisiones"""
        if divisiones is None:
            divisiones = self.divisiones
        search = self.driver.find_element(
            "css selector", 'input[placeholder="Division"] + button')
        search.click()
        try:
            search = self.wait.until(ec.element_to_be_clickable(
                ("xpath", f"//li[contains(text(), '{divisiones[0]}')]"
                 ))) #encerrar en un for el try para acceder al arreglo
        except TimeoutException:
            print(f"fitro {divisiones} no cargó")
            return -1
        search.click()
        return 1

    def set_fecha(self):
        """Seteamos fecha inicio y fecha final"""
        try:
            search = self.wait.until(ec.presence_of_element_located(
                ("css selector", 'input[placeholder="Visto por última vez"]')))
            search.click()
        except TimeoutException:
            print("fecha no cargo")
        try:
            search = self.wait.until(ec.element_to_be_clickable(
                ("xpath", "//table[@class='p-datepicker-calendar']//span[text()='1']")))
            search.click()
        except TimeoutException:
            print("no cargo el día")
        try:
            search = self.wait.until(ec.element_to_be_clickable(
                ("css selector", 'input[placeholder="Fecha hasta"]')))
            search.click()

        except TimeoutException:
            print("no cargo el selector de fecha final")

        #problema aquiii
        time.sleep(1)
        #intento 1
        # os.system('pause')
        # search = self.wait.until(ec.element_to_be_clickable(
        #     ("css selector", "div.p-datepicker-group")))
        # search = self.wait.until(ec.element_to_be_clickable(
        #     ("css selector", "p-datepicker-today"))) # fecha actual
        # print(search.get_attribute('innerHTML'))

        #intento original
        search = self.driver.find_element("css selector", "td.p-datepicker-today") # fecha actual
        search.click()

    def obtener_click(self):
        """Click en obtener"""
        search = self.driver.find_element("xpath", "//button[contains(., 'Obtener')]")
        search.click()

    def get_driver(self):
        """Obtenemos el driver"""
        return self.driver

    def taxonomizar(self, custom=None):
        """Get ready for action Smartphones samsung"""
        self.__nav_click('taxonomia', 'pendiente')
        self.__filtro_pais(FILTRO_PAIS)
        if custom is None:
            self.__filtro_retail(["plazavea", "tottus", "metro", "simple-ripley", "falabella-pe",
                    "lacuracao-pe", "oechsle-pe", "efe-pe", "hiraoka-pe", "sodimac-pe",
                    "carsa-pe", "lg", "tailoy-pe", "coolbox-pe"])
        elif custom is True:
            self.__filtro_retail()
        self.__filtro_categoria(self.categorias)
        self.set_fecha()
        self.obtener_click()
        print(f"{AZUL}HOPE: {BLANCO}Ahora estás listo para taxonomizar, te recomiendo el método .brand") # pylint: disable=C0301
        print(f"\tAutomaticamente te llenará los brand, sin mayor esfuerzo{GRIS}\n")

    def marketplace(self):
        """ Get ready for action marketplace """
        # self.__taxonomia_taxonomizado_click()
        self.__nav_click('taxonomia', 'taxonomizado')
        self.__filtro_pais(FILTRO_PAIS)
        self.__filtro_retail(self.retails)
        self.__filtro_area(FILTRO_AREA)
        self.__filtro_division()
        self.__filtro_categoria(self.categorias)
        self.obtener_click()
        print("HOPE: Ahora estás listo para Marketplacear, te recomiendo el método .fill_market()")


    def fill_market(self, nrow=None):
        """Hope empezará a trabajar el marketplace en la pagina actual"""
        wait = WebDriverWait(self.driver, 30)
        try:
            wait.until(ec.visibility_of_element_located(("css selector", "tbody"))) # pylint: disable=c0301
        except TimeoutException:
            print("Timeout: No cargó la tabla")
            return -1
        search = self.driver.find_elements('css selector', "tbody tr")
        if nrow is not None:
            search = list(search[nrow])
        for row in search:
            row.find_element("css selector", "div[tabindex='0']").click() #btn editar
            seller = row.find_element("css selector", 'input[placeholder="Feature 5"]')
            seller.click()
            seller.send_keys(Keys.CONTROL + 'a')
            name = seller.get_attribute("value") #pylint: disable=c0301
            # Boton editar
            if name != '':
                print(f"HOPE: Esta fila ya está hecha con Feature 5 = {name}\n")
                row.find_element("css selector", "div[tabindex='0']").click() # btn editar
            else:
                print('HOPE: Feature 5 sin completar. Se realizará la petición a The Finder')
                url = row.find_element("css selector", "a").get_attribute('href')
                if 'simple.ripley' in url:
                    data = self.finder.data_ripley(url)
                else:
                    data = self.finder.data_oechsle(url)
                if (data['status_code'] == 200) and (data['productSeller'] is not None):
                    print(f"THE FINDER: Encontré al vendedor = {data['productSeller']}")
                    seller.click()
                    seller.send_keys(data['productSeller'])
                    time.sleep(2)
                    try:
                        row.find_element("css selector", ".p-autocomplete-panel").click()
                    except NoSuchElementException: #pylint: disable=W0718
                        print(f"HOPE: Nombre '{data['productSeller']}'"
                              "no tiene autocompletar\n")
                        self.driver.execute_script("arguments[0].style.color = 'yellow';"
                                                   "arguments[0].style.fontWeight = '900';",
                                        row.find_element('css selector', 'td[field="nombre"]'))
                        if data['productSeller'] == 'Plazavea':
                            self.driver.execute_script("arguments[0].style.color = 'red';"
                                                   "arguments[0].style.fontWeight = '900';",
                                        row.find_element('css selector', 'td[field="nombre"]'))

                    else:
                        self.driver.execute_script("arguments[0].style.color = '#2bbd1c';"
                                                   "arguments[0].style.fontWeight = '900';",
                                        row.find_element('css selector', 'td[field="nombre"]'))
                        try:
                            time.sleep(2)
                            row.find_element('css selector', '.ml-1').click() # btn Descartar
                        except Exception as error: #pylint: disable=W0718
                            print('No se pudo dar click a confirmar', error)
                            self.driver.execute_script("arguments[0].style.color = 'yellow';"
                                                   "arguments[0].style.fontWeight = '900';",
                                        row.find_element('css selector', 'td[field="nombre"]'))
                        else:
                            print('Market done')

                elif data['status_code'] != 200:
                    print('404')
                    seller.click()
                    seller.send_keys('404')
                    self.driver.execute_script("arguments[0].style.color = 'red';"
                                                   "arguments[0].style.fontWeight = '900';",
                                        row.find_element('css selector', 'td[field="nombre"]'))
                    row.find_element("css selector", "div[tabindex='0']").click() #btn editar
                    time.sleep(2)
                    row.find_element('css selector', '.ml-1').click() # btn Descartar
                    # Ocultar el elemento utilizando JavaScript
                    self.driver.execute_script("arguments[0].style.display = 'none';", row)
                else:
                    seller.click()
                    seller.send_keys('Sin seller')
        return 1
    # Private Methods


    def brand(self):
        """ Llenar los brand automaticamente, para taxonomizado general """
        wait = WebDriverWait(self.driver, 30)
        try:
            # search = wait.until(ec.visibility_of_element_located(
            search = wait.until(ec.visibility_of_all_elements_located(
                ("css selector", 'td[field="brand"] input')))
        except TimeoutException:
            print(f"{AZUL}HOPE: {BLANCO}No ubico los campos brand, I can't see them{GRIS}")
        else:
            # brands = self.driver.find_elements("css selector", 'td[field="brand"] input')
            for valor, brand, row in zip(
                    self.driver.find_elements("css selector", 'td[field="brand"] div.p-chip-text'),
                    self.driver.find_elements("css selector", 'td[field="brand"] input'),
                    self.driver.find_elements('css selector', 'tbody tr')):
                brand.click()
                brand.send_keys(valor.text)
                try:
                    wait = WebDriverWait(self.driver, 3)
                    search = wait.until(ec.element_to_be_clickable(
                        ("xpath", f"//ul/li[contains(@class, 'p-autocomplete-item') and text() = ' {valor.text} ']"))) # pylint: disable=C0301
                except TimeoutException:
                    print(f"{AZUL}HOPE: {ROJO}'{valor.text}' no tiene automcopletar o no coincide con el de la web{GRIS}\n") # pylint: disable=C0301
                    self.driver.execute_script("arguments[0].style.color = 'red';"
                                                   "arguments[0].style.fontWeight = '900';",
                                    row.find_element('css selector', 'td[field="nombre"]'))
                else:
                    search.click()
                    self.driver.execute_script("arguments[0].style.color = 'green';"
                                                   "arguments[0].style.fontWeight = '900';",
                                    row.find_element('css selector', 'td[field="nombre"]'))
                    print(f"{AZUL}HOPE: {VERDE}Autocompletado con = {valor.text} {GRIS}\n") # pylint: disable=C0301
            print(f"{AZUL}HOPE: {BLANCO}Listo ahi tienes el brand hecho{GRIS}")

    def brand_marca(self, marcas=None):
        """ Llenar los brand automaticamente, para filtros especificos """
        if marcas is None:
            marcas = self.marcas
        wait = WebDriverWait(self.driver, 30)
        try:
            search = wait.until(ec.visibility_of_element_located(
                ("css selector", 'td[field="brand"] input')))
            # search.click()
        except TimeoutException:
            print("no cargo el selector")
        brands = self.driver.find_elements("css selector", 'td[field="brand"] input')
        for brand in brands:
            # code = 8 + i * 9
            # selector = '#pv_id_' + str(code) + '_list li'
            brand.click()
            brand.send_keys(marcas)
            # time.sleep(seconds)
            # search = self.driver.find_element("css selector", "ul li.p-autocomplete-item")
            # search = self.driver.find_element("css selector", selector)
            try:
                search = self.wait.until(ec.element_to_be_clickable(
                    ("css selector", 'ul li.p-autocomplete-item')))
                search.click()
            except TimeoutException:
                print("no cargo el selector de fecha final")
            search.click()
            # i += 1
        print("Listo ahi tienes el brand hecho")





# ------------------------Welcome-MAIN-----------------------------
if __name__ == '__main__':
    hope = Hope()
    hope.taxonomizar()
    hope.brand()
    os.system('pause')
