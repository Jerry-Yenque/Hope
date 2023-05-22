"""Welcome to HopeBot, this is the last hope project"""
import os
import time
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait # para esperar por elementos en selenium
from selenium.webdriver.support import expected_conditions as ec # para condiciones en selinium
from selenium.common.exceptions import TimeoutException # excepcion de timeout en selenium

from variables import EMAIL, CLAVE, FILTRO_PAIS, FILTRO_RETAIL, FILTRO_CATEGORIA, FILTRO_MARCA

class Hope:
    """ Clase que representa el bot de 'The last hope project' """

    def __init__(self):
        os.system('cls')
        print("\n\nBienvenido a The last Hope Project, un bot asistente"
              " que puede ser tu ultima esperanza...", end='\n\n')
        # RUTA_DRIVER = r'C:\Program Files (x86)\chromedriver.exe'
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
        # self.driver.execute_script("document.body.style.zoom = '0.33'")
        # tiempo de espera hasta que el elemento esté disponible
        self.wait = WebDriverWait(self.driver, 10)
        print("Estás seteado, ingresa el comando a realizar, por ejemplo")
        print("El metodo .ready() te llevará a taxonomizar segun tus parametros pre establecidos"
        " a la brevedad posible")

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

    def filtro_pais(self, pais):
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

    def filtro_retail(self, retails):
        """LLenado del filtro retail"""
        search = self.driver.find_element("css selector", "div.p-multiselect-label")
        search.click()
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

    def filtro_categoria(self, categorias):
        """Llenado del filtro categoria"""
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

    def filtro_marca(self, marcas):
        """Llenado del filtro marcas"""
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
        # search = self.driver.find_elements("css selector", "input.p-inputtext")[1]
        # search.click()
        #primero del mes
        # search = self.driver.find_element("xpath", "//table[@class='p-datepicker-calendar']"
        #                                   "//span[text()='1']")
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

    def ready(self, email=EMAIL, clave=CLAVE):
        """Get ready for action Smartphones samsung"""
        # filtro_pais = "Peru"
        # filtro_retail = ["plazavea", "tottus", "metro", "simple-ripley", "falabella-pe",
        #                 "lacuracao-pe", "oechsle-pe", "efe-pe", "hiraoka-pe", "sodimac-pe",
        #                 "carsa-pe", "lg", "tailoy-pe", "coolbox-pe"]
        # filtro_categoria = ['celulares']
        # filtro_marca = ["samsung"]
        self.login(email, clave)
        self.taxonomia_pendiente_click()
        self.filtro_pais(FILTRO_PAIS)
        self.filtro_retail(FILTRO_RETAIL)
        self.filtro_categoria(FILTRO_CATEGORIA)
        self.filtro_marca(FILTRO_MARCA)
        self.set_fecha()
        self.obtener_click()
        print("Ahora estás listo para taxonomizar, te recomiendo el método .brand")
        print("Automaticamente te llenará los brand, sin mayor esfuerzo")

    def brand(self):
        """Llenar los brand automaticamente, para filtros especificos"""
        brands = self.driver.find_elements("css selector", 'td[field="brand"] input')
        # i = 0
        for brand in brands:
            # code = 8 + i * 9
            # selector = '#pv_id_' + str(code) + '_list li'
            brand.click()
            brand.send_keys("samsung")
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
    hope.login(EMAIL, CLAVE)
    hope.taxonomia_pendiente_click()
    hope.filtro_pais(FILTRO_PAIS)
    hope.filtro_retail(FILTRO_RETAIL)
    hope.filtro_categoria(FILTRO_CATEGORIA)
    hope.filtro_marca(FILTRO_MARCA)
    hope.set_fecha()
    hope.obtener_click()
    hope.llenar_brand()
    os.system('pause')
    # hope.fill_brand()

# input[placeholder="Visto por última vez"]
