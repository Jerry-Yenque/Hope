"""Welcome to HopeBot, this is the last hope project"""
import os
import time
from webdriver_manager.chrome import ChromeDriverManager #para descar por code el manager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait # para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as ec # para condiciones en selinium
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import finder
from variables import EMAIL, CLAVE, FILTRO_PAIS, FILTRO_RETAIL, FILTRO_AREA , FILTRO_DIVISION, FILTRO_CATEGORIA, FILTRO_MARCA # pylint: disable=C0301

class Hope:
    """ Clase que representa el bot de 'The last hope project' """

    def __init__(self):
        os.system('cls')
        print("\n\nBienvenido a The last Hope Project, un bot asistente"
              " que puede ser tu ultima esperanza...", end='\n\n')
        # VARIABLES
        self.retails = FILTRO_RETAIL
        self.categorias = FILTRO_CATEGORIA
        self.marcas = FILTRO_MARCA
        self.divisiones = FILTRO_DIVISION
        self.areas = FILTRO_AREA

        self.finder = finder.Finder()
        # end VARIABLES

        # ruta_driver = r'C:\Program Files (x86)\chromedriver.exe'
        # Instalación de ChromeDriver, devuelve la ruta completa
        # (si ya esta instalado solo devuelve la ruta)
        ruta_driver = ChromeDriverManager(path="./chromedriver").install()
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
        print("HOPE: Hola!, cómo puedo ayudarte?\n")
        print("El método .taxonomizar() te llevará a taxonomizar según tus filtros pre establecidos") # pylint: disable=C0301
        print("El método .marketplace() te llevará a marketplacear según tus filtros pre establecidos") #pylint: disable=C0301
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
        search = self.driver.find_element("css selector", "#login")
        search.send_keys(email)
        search = self.driver.find_element("css selector", "#password")
        search.send_keys(clave)
        search = self.driver.find_element("xpath", '//input[@value="Log In"]')
        search.send_keys(Keys.RETURN)

    def taxonomia_pendiente_click(self):
        """ Click para ir a la tabla de pendientes a taxonomizar """
        # Puede mejorar a esperar que cargue el boton y darle click
        time.sleep(1)
        self.driver.get(
            "https://to-platform-v2-pd.lexartlabs.com/#/taxonomia/pendiente")
    def taxonomia_taxonomizado_click(self):
        """ Click para ir a la tabla de pendientes a taxonomizar """
        # Puede mejorar a esperar que cargue el boton y darle click
        time.sleep(1)
        self.driver.get(
            "https://to-platform-v2-pd.lexartlabs.com/#/taxonomia/taxonomizado")

    def __filtro_pais(self, pais=FILTRO_PAIS):
        """LLenado del filtro pais"""
        search = self.driver.find_element(
            "css selector", "div.custom-dropdown")
        search.click()
        try:
            search = self.wait.until(ec.element_to_be_clickable(
                ("xpath", f"//li[@aria-label='{pais}']")))
        except TimeoutException:
            print(f"fitro {pais} no cargó")
            return -1
        search.click()
        return 1

    def filtro_area(self, areas=None):
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

    def filtro_division(self, divisiones=None):
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

    def __filtro_retail(self, retails=None):
        """LLenado del filtro retail"""
        if retails is None:
            retails = self.retails
        self.driver.find_element("css selector", "div.p-multiselect-label").click()
        for retail in retails:
            try:
                search = self.wait.until(ec.element_to_be_clickable(
                    ("xpath", f"//li[@aria-label='{retail}']")))
                # search = self.driver.find_element(
                #     "xpath", f"//li[@aria-label='{retail}']")
                search.click()
            except TimeoutException:
                print(f"fitro {retail} no cargó")
                return -1
        search = self.driver.find_element(
            "css selector", "div.p-multiselect-label")
        search.click()
        return 1

    def filtro_categoria(self, categorias=None):
        """Llenado del filtro categorias"""
        if categorias is None:
            categorias = self.categorias
        search = self.driver.find_elements("css selector", "div.p-multiselect-label")[1]
        search.click()
        for categoria in categorias:
            try:
                search = self.wait.until(ec.element_to_be_clickable(
                    ("xpath", f"//li[@aria-label='{categoria}']")))
                search.click()
            except TimeoutException:
                print(f"fitro {categoria} no cargó")
                return -1
        search = self.driver.find_elements("css selector", "div.p-multiselect-label")[1]
        search.click()
        return 1

    def filtro_marca(self, marcas = None):
        """Llenado del filtro marcas"""
        if marcas is None:
            marcas = self.marcas
        search = self.driver.find_elements("css selector", "div.p-multiselect-label")[2]
        search.click()
        for marca in marcas:
            try:
                search = self.wait.until(ec.element_to_be_clickable(
                    ("xpath", f"//li[@aria-label='{marca}']")))
                search.click()
            except TimeoutException:
                print(f"fitro {marca} no cargó")
                return -1
        search = self.driver.find_elements("css selector", "div.p-multiselect-label")[2]
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

    def taxonomizar(self):
        """Get ready for action Smartphones samsung"""
        self.taxonomia_pendiente_click()
        self.__filtro_pais(FILTRO_PAIS)
        self.__filtro_retail(self.retails)
        self.filtro_categoria(self.categorias)
        self.filtro_marca(self.marcas)
        self.set_fecha()
        self.obtener_click()
        print("Ahora estás listo para taxonomizar, te recomiendo el método .brand")
        print("Automaticamente te llenará los brand, sin mayor esfuerzo")

    def marketplace(self):
        """Get ready for action marketplace"""
        self.taxonomia_taxonomizado_click()
        self.__filtro_pais(FILTRO_PAIS)
        self.__filtro_retail(self.retails)
        self.filtro_area(FILTRO_AREA)
        self.filtro_division()
        self.filtro_categoria(self.categorias)
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


    def brand(self, marcas=None):
        """Llenar los brand automaticamente, para filtros especificos"""
        if marcas is None:
            marcas = self.marcas
        # brands = self.driver.find_elements("css selector", 'td[field="brand"] input')
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
    #approach 2
    hope.marketplace()
    os.system('pause')
    hope.fill_market()
    os.system('pause')
    #para los botones editar
    #search = d.find_element('css selector', "div[tabindex='0']")
    #feature 5 seleccionar
    #search = d.find_element("css selector", 'input[placeholder="Feature 5"]')
    #search.click()
    #search.send_keys(Keys.CONTROL + 'a') #seleccionar todo
    #texto = search.get_attribute("value") #obtenemos el valor de la seleccion
