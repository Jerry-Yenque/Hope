from webdriver_manager.chrome import ChromeDriverManager # to download by code the driver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from seleniumwire import webdriver
from presentation.theme import AZUL, BLANCO, GRIS


class WebDriverManager:
    """Clase encargada de configurar y manejar el WebDriver."""
    def __init__(self):
        self.tag = "WebDriverManager"
        self.driver = None

    def create_driver(self):
        print(f"{AZUL}{self.tag}:{BLANCO} Creating driver.{GRIS}")
        # ruta_driver = r'C:\Program Files (x86)\chromedriver.exe'
        # Instalación de ChromeDriver, devuelve la ruta completa
        # (si ya esta instalado solo devuelve la ruta)
        ruta_driver = ChromeDriverManager(driver_version="131.0.6778.204").install()
        # print(ruta_driver)
        # ruta_driver = ChromeDriverManager(path="./chromedriver").install()
        # Creamos y asignamos la variable a un objeto Service que contiene la ruta del webdriver
        driver_service = Service(ruta_driver)
        # Establecer las opciones del navegador
        options = Options()
        options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"
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
        # options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})
        self.driver = webdriver.Chrome(
            service=driver_service, options=options)
        
        return self.driver
    
if __name__ == "__main__":
    # ========= This is like an unit test! =============== #
    import os
    driver_manager = WebDriverManager()
    driver = driver_manager.create_driver()
    driver.get("https://github.com/Jerry-Yenque")
    os.system("PAUSE")