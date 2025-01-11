import hope
import importlib
import os  # undetected_chromedriver
import threading
import time
from dotenv import load_dotenv
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as ec  # para condiciones en selinium
from selenium.webdriver.support.ui import WebDriverWait  # para esperar por elementos en selenium
from domain.Procesor import getPosibleNames
from infrastructure.WebDriverManager import WebDriverManager
import presentation
from presentation.theme import AZUL, VERDE, BLANCO, ROJO, GRIS, AMARILLO
from src.config import FILTRO_PAIS, FILTRO_RETAIL, FILTRO_AREA, FILTRO_DIVISION, FILTRO_CATEGORIA, FILTRO_MARCA, \
    FILTRO_RETAIL_MARKETPLACE  # pylint: disable=C0301
from src.data.finder import Finder
from src.helpers import DropdownConstant

load_dotenv()
PROJECT = "Hope"


# Dropdown Superior
DROPDOWN_PAIS = DropdownConstant("DROPDOWN_PAIS", "1")
DROPDOWN_RETAIL = DropdownConstant("DROPDOWN_RETAIL", "2")
DROPDOWN_CATEGORIA = DropdownConstant("DROPDOWN_CATEGORIA", "3")
DROPDOWN_MARCAS = DropdownConstant("DROPDOWN_CATEGORIA", "4")

# Dropdown bottom
DROPDOWN_FILTRO = DropdownConstant("DROPDOWN_FILTRO", "1")
DROPDOWN_TIMEPICKER_START = DropdownConstant("DROPDOWN_TIMEPICKER_START", "2")
DROPDOWN_TIMEPICKER_END = DropdownConstant("DROPDOWN_TIMEPICKER_END", "3")



ABM_ON_SIDE_BAR = "1"
TAXONOMIA_ON_SIDE_BAR = "2"

PENDIENTE_ON_TAXONOMIA_SIDE_BAR = "1"

# To activate the virtual enviroment type this: .\env\Scripts\activate or only activate can work

class Hope:
    """ Clase que representa el bot de 'The last hope project' """
    def __init__(self):
        os.system('cls')
        # VARIABLES
        self.driver_manager = WebDriverManager()
        self.driver = self.driver_manager.create_driver()
        self.retails = FILTRO_RETAIL
        self.categorias = FILTRO_CATEGORIA
        self.marcas = FILTRO_MARCA
        self.divisiones = FILTRO_DIVISION
        self.areas = FILTRO_AREA
        self.pais = FILTRO_PAIS
        self.retailsMarketplace = FILTRO_RETAIL_MARKETPLACE
        self.categoriaMarketplace = ["audifono"]
        self.token = ""
        self.finder = Finder()
        # End VARIABLES
        self.welcome()

        # tiempo de espera hasta que el elemento esté disponible
        self._time: float = 10
        self.wait = WebDriverWait(self.driver, self.time)
        self.login()
        # self.audifonos()

    def welcome(self):
        print(f"{AZUL}{PROJECT}: {BLANCO}Bienvenido")
        print(f"\tEl método .taxonomizar() te llevará a taxonomizar según tus filtros pre establecidos")
        print(f"\tEl método .marketplace() te llevará a marketplacear según tus filtros pre establecidos{GRIS}\n") #pylint: disable=C0301

    @property
    def time(self):
        return self._time
    
    @time.setter
    def time(self):
        raise AttributeError("La variable es de solo lectura y no se puede modificar")
    

    def reload(self):
        load_dotenv(override=True)
        # import presentation.theme
        importlib.reload(hope)
        importlib.reload(presentation.theme)
        for name, method in hope.Hope.__dict__.items():
            if callable(method):
                setattr(self, name, method.__get__(self, self.__class__))
        print("Métodos recargados")

    def loadNames(self):
        thread = threading.Thread(target=self._load_names_task, daemon=True)
        thread.start()
        print("Cargando nombres en segundo plano...")
        # self.names = getPosibleNames(self.token)

    def _load_names_task(self):
        # Esta tarea se ejecuta en un hilo separado
        self.names = getPosibleNames(self.token)

    def login(self, email=os.getenv("EMAIL"), clave=os.getenv("PASSWORD")):
        """ Acceso automatico """
        self.driver.get(f"{os.getenv("HOST_V2")}/login")
        self.wait.until(ec.element_to_be_clickable(("css selector", "#login"))).send_keys(email)
        self.wait.until(ec.element_to_be_clickable(("css selector", "#password"))).send_keys(clave)
        self.wait.until(ec.element_to_be_clickable(("xpath", '//input[@value="Log In"]'))).send_keys(Keys.RETURN)

        # tablaSelector= "body > div > div.wrapper > div.main-panel > div > div > div:nth-child(1) > div"
        # self.wait.until(ec.presence_of_element_located(("css selector", tablaSelector)))


        # self.wait.until(ec.url_changes(f"{os.getenv("LOGIN")}/abm/area"))
        tableSelector = "body > div > div.wrapper > div.main-panel > div > div > div:nth-child(1) > div"
        self.wait.until(ec.presence_of_element_located(("css selector", tableSelector)))
        # Captura el token desde el localStorage (si se guarda ahí)
        self.token = self.driver.execute_script("return localStorage.getItem('http_token');")
        # print(f'Token: {self.token}')
        self.speak(f"Este es tu token {self.token}")

    def speak(self, msg: str):
        print(f"{AZUL}{PROJECT}: {BLANCO}{msg}{GRIS}")

    def getToken(self):
        return self.driver.execute_script("return localStorage.getItem('http_token');")
    def cls(self):
        os.system('cls')

    def audifonos(self): # it was called taxonomizar()
        """Get ready for action Smartphones samsung"""
        self.goTaxonomiaPendiente()
        self.fillCountry(self.pais)
        self.fillRetails(self.retails)
        self.fillCategoria(self.categorias)
        self.fillMarcas(self.marcas)
        self.setFecha()
        self.btnObtenerClick()
        tableSelector = "body > div > div.wrapper > div.main-panel > div > div > div:nth-child(2) > div > table"
        self.changeWait(40)
        self.wait.until(ec.presence_of_element_located(("css selector", tableSelector)))
        print(f"{AZUL}{PROJECT}: {BLANCO}Ahora estás listo para taxonomizar, te recomiendo el método .brand") # pylint: disable=C0301
        print(f"\tAutomaticamente te llenará los brand, sin mayor esfuerzo{GRIS}\n")
        self.resetWait()

    def goTaxonomiaPendiente(self):
        """ Just navigates to Taxonomia pendiente """
        self.__navWithUrl('taxonomia', 'pendiente')
        # try:
        #     self.clickCategoryOnSideBar(TAXONOMIA_ON_SIDE_BAR)
        #     self.clickElementOfTaxonomiaOnSideBar(PENDIENTE_ON_TAXONOMIA_SIDE_BAR)
        # except TimeoutException as error:
        #     print(f"{AZUL}{PROJECT}: {BLANCO}No apareció el elemento Pendiente en las opciones 'Taxonomia' de la barra izquierda de navegación.")
        #     print(f"\tNavegando de manera directa a través del link.")
        #     print(f"{GRIS}\tTimeoutError: {error}.")
        #     self.__navWithUrl('taxonomia', 'pendiente')

    def clickCategoryOnSideBar(self, dropdown: str):
        """ Aqui se da click a ABM, TAXONOMIA, COMPARATIVA DE PRECIOS o HISTORICOS DE PRECIOS de las categorias en el side bar """
        """ No se considera a AREA ya que se selecciona por defecto"""

        categoryOnSideBar = F"#style-3 > ul > div:nth-child(1) > div:nth-child({dropdown}) > div.p-panel-header"
        self.wait.until(ec.element_to_be_clickable(('css selector', categoryOnSideBar))).click()

    def clickElementOfTaxonomiaOnSideBar(self, dropdown: str):
        if(dropdown == 'pendiente'):
            dropdown = PENDIENTE_ON_TAXONOMIA_SIDE_BAR
        elementToClickOnTaxonomizaSideBar = f'#pv_id_2_content > div > div:nth-child({dropdown}) > li > a'
        self.changeWait(3)
        self.wait.until(ec.element_to_be_clickable(('css selector', elementToClickOnTaxonomizaSideBar))).click()
        self.resetWait()

    def __navWithUrl(self, section, item):
        """ Navegar a través de url de acuerdo a la sección y a su item """

        self.driver.get(f"{os.getenv("HOST_V2")}/{section}/{item}")


    def fillCountry(self, pais=FILTRO_PAIS):
        """ LLenado del filtro pais """
        self.changeWait(4)
        try:
            # self.clickDropdown(DROPDOWN_PAIS)
            self.clickDropdownCountry()
            self.clickDropdownElement(pais)
        except Exception as e:
            self.wait.until(ec.element_to_be_clickable(("css selector", "div.custom-dropdown"))).click()
            try:
                self.wait.until(ec.element_to_be_clickable(
                    ("xpath", f"//li[@aria-label='{pais}']"))).click()
            except TimeoutException:
                print(f"{AZUL}Hope: {ROJO} No se puedo autocompletar el fitro = '{pais}'{GRIS}")
        self.resetWait()

    def fillArea(self, area=FILTRO_AREA):
        """ Llenado del filtro area """
        self.changeWait(4)
        try:    
            self.clickDropdownArea()
            print(f"Dando click area {area}")
            self.clickDropdownElement(area)
        except TimeoutException:
            print(f"fitro {area} no cargó")
            

    
    ### DROPDOWNS SECTION-------------------------------------------------------------
    
    def clickDropdownRetail(self): 
        # retailDropdownSelector = "//div[@class='p-multiselect-label-container']/div[@class='p-multiselect-label p-placeholder' and text()='Retail']"
        retailDropdownSelector = "div.p-multiselect-label"
        self.wait.until(ec.element_to_be_clickable(("css selector", retailDropdownSelector))).click()

    def clickDropdownCountry(self):
        countryDropdownSelector = "//span[@class='p-dropdown-label p-inputtext p-placeholder' and normalize-space(text())='País']"
        self.wait.until(ec.element_to_be_clickable(("xpath", countryDropdownSelector))).click()
    
    def clickDropdownArea(self):
        areaDropdownSelector = 'input[placeholder="Area"] + button'
        self.wait.until(ec.element_to_be_clickable(("css selector", areaDropdownSelector))).click()

    def clickDropdownCategory(self):
        categoryDropdownSelector = "//div[contains(@class, 'p-multiselect-label') and text()='Categoria']"
        self.wait.until(ec.element_to_be_clickable(("xpath", categoryDropdownSelector))).click()


    def clickDropdown(self, dropdown: str):
        """ Da click a los dropdown en taxonomia pendiente:

        ### Dropdown Superior
        * DROPDOWN_PAIS
        * DROPDOWN_RETAIL
        * DROPDOWN_CATEGORIA
        * DROPDOWN_MARCAS 

        ### Dropdown bottom
        * DROPDOWN_FILTRO
        * DROPDOWN_TIMEPICKER_START
        * DROPDOWN_TIMEPICKER_END

        """
        dropdownSuperior = [
            DROPDOWN_PAIS,
            DROPDOWN_RETAIL,
            DROPDOWN_CATEGORIA,
            DROPDOWN_MARCAS
        ]

        if (dropdown in dropdownSuperior):
            self.clickDropdownSuperior(dropdown.value)
        else:
            self.clickDropdownBottom(dropdown.value)


    def clickDropdownSuperior(self, dropdown: str):
        # dropDownCountry = "div.custom-dropdown" #Antiguo
        dropdownSelector: str =  f"body > div > div.wrapper > div.main-panel > div > div > div.content-query > div > div.p-mt-4.container-flex.mb-2 > div:nth-child({dropdown})"
        try:
            self.wait.until(ec.element_to_be_clickable(("css selector", dropdownSelector))).click()
        except:
            print(f"DropdownSuperior no encontrado {dropdown}")

    def SendDropdownMarcas(self, text: str):
        """ To send keys in dropdown marcas input"""
        # dropDownCountry = "div.custom-dropdown" # Deprecated

        inputTextSelector: str =  "body > div > div.wrapper > div.main-panel > div > div > div.content-query > div > div.p-mt-4.container-flex.mb-2 > div.custom-multiselect.custom-input-max-min-300.filter.p-mr-2.p-multiselect.p-component.p-inputwrapper.p-multiselect-chip.p-inputwrapper-focus > div.p-multiselect-panel.p-component > div.p-multiselect-header > div.p-multiselect-filter-container > input"
        inputText = self.wait.until(ec.element_to_be_clickable(("css selector", inputTextSelector)))
        if (text == "" or text == " "):
            # time.sleep(0.8)
            # print(f"{BLANCO}      Limpiando el input.{GRIS}")
            inputText.click()
            inputText.send_keys(Keys.CONTROL + "a")  # Seleccionar todo el texto
            inputText.send_keys(Keys.DELETE)
            self.wait.until(ec.text_to_be_present_in_element_value(("css selector", inputTextSelector), ''))
        else:
            self.wait.until(ec.text_to_be_present_in_element_value(("css selector", inputTextSelector), ''))
            inputText.send_keys(text)
    
    def clickDropdownBottom(self, dropdown: str):
        dropdownSelector: str = f"body > div > div.wrapper > div.main-panel > div > div > div.content-query > div > div:nth-child(2) > span:nth-child({dropdown}) > input"
        self.wait.until(ec.element_to_be_clickable(("css selector", dropdownSelector))).click()
        
    # @DEPRECATED 80/01/2025
    # def clickDropdownElement(self, key: str):
    #     """ Clickea cualquier elemento de algún dropdown que tenga diga key, la funcion maneja el wait """
    #     dropdownElementSelector = f"//*[normalize-space(text())='{key}']"
    #     #//*[translate(normalize-space(text()), 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz') = 'peru']
    #     try:
    #         # self.wait.until(ec.element_to_be_clickable(
    #         #     ("xpath", f"//li[@aria-label='{key}']"))).click()
    #         self.wait.until(ec.element_to_be_clickable(
    #             ("xpath", dropdownElementSelector))).click()
            
    #     except TimeoutException:
    #         print(f"{AZUL}{ROJO}      Tiempo para encontrar al elemento del dropdown con texto= '{key}' agotado{GRIS} ")
    #         raise RuntimeError(f"El elemento {key} no cargó.")

    #     except StaleElementReferenceException:
    #         print(f"{AZUL}{ROJO}      El elemento {key} se ocultó antes de poder clickearlo{GRIS}")
    #         raise RuntimeError(f"El elemento {key} se ocultó antes de poder clickearlo")
    

    def clickDropdownElement(self, key: str, max_attempts=3, wait_time=4):
        """ Clickea cualquier elemento de algún dropdown que diga key, manejando reintentos internos """
        dropdownElementSelector = f"//*[normalize-space(text())='{key}']"
        attempt = 0
        self.changeWait(wait_time)
        while attempt < max_attempts:
            try:
                self.wait.until(ec.element_to_be_clickable(("xpath", dropdownElementSelector))).click()
                self.resetWait()
                return  # Salir si el clic fue exitoso
            except TimeoutException:
                # print(f"{AZUL}{ROJO}      Tiempo para encontrar al elemento del dropdown con texto= '{key}' agotado{AMARILLO} (intento {attempt+1}/{max_attempts}).{GRIS}")
                print(f"{AZUL}{ROJO}      Tiempo para encontrar la marca = '{key}' agotado{AMARILLO} (intento {attempt+1}/{max_attempts}).{GRIS}")
            except StaleElementReferenceException:
                print(f"{AZUL}{ROJO}      El elemento {key} se ocultó antes de poder clickearlo{AMARILLO} (intento {attempt+1}/{max_attempts}).")
            
            attempt += 1
            if attempt < max_attempts:
                print(f"{AZUL}{BLANCO}      Intentando una vez más para {key}{GRIS}")
            else:
                self.resetWait()
                raise RuntimeError(f"{ROJO}No se pudo clickear el elemento {key} después de {max_attempts} intentos.{GRIS}")

    

    def fillMarcas(self, marcas=None):
        """ Rellena marcas en el dropdown """
        if marcas is None:
            marcas = self.marcas
        self.clickDropdown(DROPDOWN_MARCAS)
        self.changeWait(4)
        listNoProcessed = []
        for key, value in marcas.items():
            self.SendDropdownMarcas(str(key))

            if isinstance(value, list):
                print(f"{AZUL}{PROJECT}: {VERDE}{key}{BLANCO} contiene versiones{GRIS}")
                all_processed = True  # Bandera para verificar si todos los elementos se procesaron
                for item in value:
                    try:
                        self.clickDropdownElement(item)
                    except RuntimeError:
                        listNoProcessed.append(item)
                        all_processed = False  # Indicar que hubo fallos
                        print(f"{AZUL}{ROJO}      No se pudo procesar {item} después de los intentos{GRIS}")

                if all_processed:
                    print(f"{AZUL}{VERDE}      Cargado sin problema.\n{GRIS}")
                self.SendDropdownMarcas("")  # Limpia el input después de las versiones
            else:
                print(f"{AZUL}{PROJECT}: {VERDE}{key}{BLANCO} es único")
                try:
                    self.clickDropdownElement(value)
                    print(f"{AZUL}{VERDE}      Cargado sin problema.\n{GRIS}")
                except RuntimeError:
                    listNoProcessed.append(value)
                    print(f"No se pudo procesar {value} después de los reintentos.")
                self.SendDropdownMarcas("")  # Limpia el input

        self.clickDropdown(DROPDOWN_MARCAS)
        self.resetWait()

    # @DEPRECATED 08/01/2025
    # def fillMarcas(self, marcas=None): #FILTRO_MARCA
    #     if marcas == None:
    #         marcas = self.marcas
    #     self.clickDropdown(DROPDOWN_MARCAS)
    #     # loop para las diferentes marcas
    #     # self.clickDropdownElement('SONY')
    #     self.changeWait(4)
    #     listNoProcessed = []
    #     max_attempts = 4
    #     for key, value in marcas.items():
    #         self.SendDropdownMarcas(str(key))
    #         if isinstance(value, list):
    #             print(f"{AZUL}{PROJECT}: {VERDE}{key}{BLANCO} contiene versiones{GRIS}")
    #             try:
    #                 for item in value:
    #                     attempt = 0
    #                     while attempt < max_attempts:
    #                         try:
    #                             self.clickDropdownElement(item)
    #                             # print(f"{VERDE}      {item}: logrado*.{GRIS}")
    #                             break
    #                         except Exception:
    #                             attempt += 1
    #                             print(f"{AZUL}{BLANCO}      Intentando una vez más para {item}{GRIS}")
    #                             if attempt < max_attempts:
    #                                 self.SendDropdownMarcas("")
    #                             else:
    #                                 listNoProcessed.append(item)
    #                                 print(f"{AZUL}{ROJO}      No se pudo procesar {item} después de {max_attempts} intentos{GRIS}")
    #                                 # self.clickDropdownElement(item)
    #                                 # print(f"{AZUL}{VERDE}      Logrado.{GRIS}")
                            
    #             except Exception:
    #                 print(f"{AZUL}{BLANCO}{ROJO}      Error procesando las versiones de {key}\n{GRIS}")
    #             else:
    #                 # Se ejecuta si no se produjo ninguna excepción durante la iteración interna
    #                 print(f"{AZUL}{VERDE}      Cargado sin problema.\n{GRIS}")
    #             finally:
    #                 self.SendDropdownMarcas("")

    #         else:
    #             print(f"{AZUL}{PROJECT}: {VERDE}{key}{BLANCO} es único")
    #             try:
    #                 self.clickDropdownElement(value)
    #                 print(f"{AZUL}{VERDE}      Cargado sin problema.\n{GRIS}")
    #             except Exception:
    #                 print(f"{AZUL}{BLANCO}      Intentando una vez más.{GRIS}")
    #                 self.SendDropdownMarcas("")
    #                 self.clickDropdownElement(value)
    #                 print(f"{AZUL}{VERDE}      Cargado sin problema.\n{GRIS}")
    #                 # print("se manda a limpiar input")
    #                 # self.SendDropdownMarcas("")
    #             else:
    #                 self.SendDropdownMarcas("")

    #     self.clickDropdown(DROPDOWN_MARCAS)
    #     self.resetWait()


    def brand(self):
        """ Llenar los brand automaticamente, para taxonomizado general """
        self.changeWait(30)

        # wait = WebDriverWait(self.driver, 30)
        try:
            # search = wait.until(ec.visibility_of_element_located(
            search = self.wait.until(ec.visibility_of_all_elements_located(
                ("css selector", 'td[field="brand"] input')))
        except TimeoutException:
            print(f"{AZUL}HOPE: {BLANCO}No ubico los campos brand, I can't see them{GRIS}")
        else:
            # brands = self.driver.find_elements("css selector", 'td[field="brand"] input')
            i = 1
            for valor, brand, row in zip(
                    self.driver.find_elements("css selector", 'td[field="brand"] div.p-chip-text'),
                    self.driver.find_elements("css selector", 'td[field="brand"] input'),
                    self.driver.find_elements('css selector', 'tbody tr')):
                text = str(valor.text)
                brand.click()
                brand.send_keys(text)
                try:
                    # wait = WebDriverWait(self.driver, 3)  
                    self.changeWait(3)
                    if (text == "BEATS"):
                        text = "BEATS BY DR.DRE"
                    search = self.wait.until(ec.element_to_be_clickable(
                        ("xpath", f"//ul/li[contains(@class, 'p-autocomplete-item') and text() = ' {text} ']"))) # pylint: disable=C0301
                except TimeoutException:
                    print(f"{AZUL}HOPE: {ROJO}'{valor.text}' no tiene automcopletar o no coincide con el de la web{GRIS}\n") # pylint: disable=C0301
                    self.driver.execute_script("arguments[0].style.color = 'red';"
                                                "arguments[0].style.fontWeight = '900';",
                                    row.find_element('css selector', f'body > div > div.wrapper > div.main-panel > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child({i}) > td.sticky-2.sticky-2-moved'))
                                    # row.find_element('css selector', 'td[field="nombre"]'))
                else:
                    search.click()
                    self.driver.execute_script("arguments[0].style.color = 'green';"
                                                "arguments[0].style.fontWeight = '900';",
                                    row.find_element('css selector', 'td[field="nombre"]'))
                    print(f"{AZUL}HOPE: {VERDE}Autocompletado con = {valor.text} {GRIS}\n") # pylint: disable=C0301
                i += 1
            print(f"{AZUL}HOPE: {BLANCO}Listo ahi tienes el brand hecho{GRIS}")
        self.resetWait()

    def name(self):
        """ Llenar los name automaticamente, para taxonomizado general """
        self.changeWait(30)

        nameInputTextSelectors = 'td[field="nombre"] input[type="text"]'

        # wait = WebDriverWait(self.driver, 30)
        try:
            # search = wait.until(ec.visibility_of_element_located(
            search = self.wait.until(ec.visibility_of_all_elements_located(
                ("css selector", nameInputTextSelectors)))
        except TimeoutException:
            print(f"{AZUL}HOPE: {BLANCO}No ubico los campos brand, I can't see them{GRIS}")
        else:
            # brands = self.driver.find_elements("css selector", 'td[field="brand"] input')
            i = 0
            rowSelectors = 'tbody tr' # Every row in the table: 20 rows
            for row in self.driver.find_elements('css selector', rowSelectors):  # -> zip = (element1, element2, element3 )
                # brand.click()
                # brand.send_keys(valor.text)
                try:
                    # wait = WebDriverWait(self.driver, 3)  
                    self.changeWait(3)
                    name_input = row.find_element("css selector", nameInputTextSelectors)
                    # search = self.wait.until(ec.element_to_be_clickable(
                    #     ("xpath", f"//ul/li[contains(@class, 'p-autocomplete-item') and text() = ' {valor.text} ']"))) # pylint: disable=C0301
                    search = self.wait.until(ec.element_to_be_clickable(
                        name_input))
                    # search.click()
                    search.send_keys(self.names[i])
                    row.click()
                    
                except TimeoutException:
                    print(f"{AZUL}HOPE: {ROJO}'valor.text' no tiene automcopletar o no coincide con el de la web{GRIS}\n") # pylint: disable=C0301
                    raise RuntimeError("plop")
                    # self.driver.execute_script("arguments[0].style.color = 'red';"
                    #                             "arguments[0].style.fontWeight = '900';",
                    #                 row.find_element('css selector', f'body > div > div.wrapper > div.main-panel > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child({i}) > td.sticky-2.sticky-2-moved'))
                                    # row.find_element('css selector', 'td[field="nombre"]'))
                else:
                    # search.click()
                    # self.driver.execute_script("arguments[0].style.color = 'green';"
                    #                             "arguments[0].style.fontWeight = '900';",
                    #                 row.find_element('css selector', 'td[field="nombre"]'))
                    print(f"{AZUL}HOPE: {VERDE}Autocompletado con = 'valor.text' {GRIS}\n") # pylint: disable=C0301
                i += 1
            self.names = self.names[20:]
            print(f"{AZUL}HOPE: {BLANCO}Quedan {len(self.names)} audífonos  .{GRIS}")
        self.resetWait()

    def changeWait(self, time: float):
        """ Change the wait on self.wait """
        self.wait = WebDriverWait(self.driver, time)
    
    def resetWait(self):
        self.wait = WebDriverWait(self.driver, self.time)

    def fillRetails(self, retails=FILTRO_RETAIL):
        """ LLenado del filtro de retail """

        # self.driver.find_element("css selector", "div.p-multiselect-label").click()
        self.changeWait(4)
        # self.clickDropdown(DROPDOWN_RETAIL)
        print("click retail dropdown")
        self.clickDropdownRetail()

        for retail in retails:
            try:
                # wait = WebDriverWait(self.driver, 4)
                #la funcion de abajo ya maneja el reloj
                print(f"click elemento {retail} en retail")
                self.clickDropdownElement(retail)
                # self.wait.until(ec.element_to_be_clickable(
                #     ("xpath", f"//li[@aria-label='{retail}']"))).click()
            except TimeoutException:
                print(f"{AZUL}{PROJECT}: {ROJO} Tiempo para encontrar el elemento del dropdown retail = '{retail} alcanzado{GRIS}'")
        
        print("Click para cerrar retails")
        # self.driver.find_element(
        #     "css selector", 'input[placeholder="Area"] + button').click()
        self.clickDropdownRetail()
        self.resetWait()

        # self.driver.find_element(
            # "css selector", "div.p-multiselect-label").click()
    def retailTaxonomizados(self, retails=None):
        """LLenado del filtro retail"""
        if retails is None:
            retails = self.retails
        self.wait.until(ec.element_to_be_clickable(("css selector", "div.p-multiselect-label"))).click()
        for retail in retails:
            try:
                self.wait.until(ec.element_to_be_clickable(
                    ("xpath", f"//li[@aria-label='{retail}']"))).click()
            except TimeoutException:
                print(f"{AZUL}Hope: {ROJO} No se puedo autocompletar el fitro = '{retail}'")
        self.driver.find_element(
            "css selector", "div.p-multiselect-label").click()
    
    def fillCategoria(self, categorias=FILTRO_CATEGORIA):
        """Llenado del filtro categorias"""
        if categorias is None:
            categorias = self.categorias
        # self.driver.find_elements("css selector", "div.p-multiselect-label")[1].click()
        self.changeWait(4)
        # self.clickDropdown(DROPDOWN_CATEGORIA)
        self.clickDropdownCategory()
        for categoria in categorias:
            try:
                self.clickDropdownElement(categoria)
                # self.wait.until(ec.element_to_be_clickable(
                #     ("xpath", f"//li[@aria-label='{categoria}']"))).click()
            except TimeoutException:
                print(f"{AZUL}{PROJECT}: {ROJO} Tiempo para encontrar el elemento del dropdown categoria = '{categoria} alcanzado{GRIS}'")
                return -1
        # self.driver.find_elements("css selector", "div.p-multiselect-label")[1].click()
        self.resetWait()
    
    def __fillArea(self, areas=FILTRO_AREA):
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

    
    def __fillDivision(self, divisiones=FILTRO_DIVISION):
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
    
    
    def setFecha(self):
        """Seteamos fecha inicio y fecha final"""
        self.changeWait(4)
        try:
            self.clickDropdown(DROPDOWN_TIMEPICKER_START)

            # @Deprecated
            # self.wait.until(ec.presence_of_element_located(("css selector", 'input[placeholder="Visto por última vez"]'))).click()
        except TimeoutException:
            print(f"{AZUL}{PROJECT}: {ROJO} Tiempo para encontrar time picker inicio{GRIS}")
        try:

            firstOfMonthXpath = "//table[@class='p-datepicker-calendar']//span[text()='1']"
            self.wait.until(ec.element_to_be_clickable(("xpath", firstOfMonthXpath))).click()
        except TimeoutException:
            print(f"{AZUL}{PROJECT}: {ROJO} Tiempo para encontrar el primero del mes alcanzado{GRIS}")
        try:
            self.clickDropdown(DROPDOWN_TIMEPICKER_END)

            # @Deprecated
            # self.wait.until(ec.element_to_be_clickable(
            #     ("css selector", 'input[placeholder="Fecha hasta"]'))).click()

        except TimeoutException:
            print(f"{AZUL}{PROJECT}: {ROJO} Tiempo para encontrar time picker final.{GRIS}")

        today_in_the_month_selector = "//td[contains(@class, 'p-datepicker-today')]"  #"td.p-datepicker-today"
        max_attempts = 5
        attempt = 0 

        while attempt < max_attempts:
            try:
                time.sleep(1)
                today_element = self.wait.until(ec.element_to_be_clickable(("xpath", today_in_the_month_selector)))
                today_element.click()
                # Asegurarse de que el elemento esté visible y en el viewport
                self.driver.execute_script("arguments[0].scrollIntoView(true);", today_element)
                return
            except StaleElementReferenceException:
                attempt += 1
                print(f"{AZUL}{PROJECT}: {ROJO}El elemento día actual se ocultó antes de poder clickearlo. Reintentando {attempt}{GRIS}")
                
            except TimeoutException:
                print("Tiempo de espera agotado al intentar encontrar el elemento.")
                break
            except Exception as e:
                print(f"Se produjo una excepción: {e}")
                break

        print(f"{AZUL}{PROJECT}: {ROJO} Tiempo para encontrar el dia actual del mes alcanzado{GRIS}")


        self.resetWait()


    def btnObtenerClick(self):
        """Click en obtener"""
        btnObtenerSelector = "//button[contains(., 'Obtener')]"
        self.driver.find_element("xpath", btnObtenerSelector).click()

    def extractTitle(self, number):
        """ Para extraer los titulos de cada una de las filas en la tabla """
        titleInRowNSelector = f"body > div > div.wrapper > div.main-panel > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child({number}) > td.sticky-2.sticky-2-moved"

        try: 
            title = self.wait.until(ec.presence_of_element_located(("css selector", titleInRowNSelector)))
            self.titlesTemp.append(title.text + "\n")

        except Exception as e:
            print(f"error: {e}")
        

    def reportTitles(self):
        print(f"{BLANCO} {self.titlesTemp}{GRIS}")
        print(f"{VERDE}Total: {self.titlesTemp.__len__()}{GRIS}")

    def getRowsMarketplace(self):
        rowsSelector = "tbody tr"
        return self.driver.find_elements('css selector', rowsSelector)


    def btnEditarRowClick(self, row):
        """ Dale un objeto fila y le dará click a su btnEditar """
        btnEditarSelector = "div[tabindex='0']"
        row.find_element("css selector", btnEditarSelector).click()

    def getInputMarketText(self, index):
        """ Dale el indice de una fila y le dará click a su input para el vendedor y te dará el texto """
        # inputMarketSelector = 'input[placeholder="Feature 5"]'
        inputMarketSelector = f"body > div > div.wrapper > div.main-panel > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child({index+1}) > td:nth-child(14) input"

        # inputMarket = row.find_element("css selector", inputMarketSelector)
        inputMarket = self.driver.find_element("css selector", inputMarketSelector)
        inputMarket.click()
        inputMarket.send_keys(Keys.CONTROL + 'a')
        print("enviando value")
        return inputMarket.get_attribute("value")
    
    def getRowLink(self, row):
        return row.find_element("css selector", "a").get_attribute('href')

    def sendInputMarketText(self, index, input):
        inputMarketSelector = f"body > div > div.wrapper > div.main-panel > div > div > div:nth-child(2) > div > table > tbody > tr:nth-child({index+1}) > td:nth-child(14) input"

        # inputMarket = row.find_element("css selector", inputMarketSelector)
        inputMarket = self.driver.find_element("css selector", inputMarketSelector)
        inputMarket.click()
        inputMarket.send_keys(input)

    def fill_market(self, nrow=None):
        """ Hope empezará a trabajar el marketplace en la pagina actual """

        self.changeWait(60)
        try:
            self.wait.until(ec.visibility_of_element_located(("css selector", "tbody"))) # pylint: disable=c0301
        except TimeoutException:
            print("Timeout: No cargó la tabla de productos taxonomizados")
            return
    
        self.changeWait(4)    
        filasSelector = "tbody tr"
        search = self.driver.find_elements('css selector', filasSelector)

        if nrow is not None:
            search = list(search[nrow])
        for index, row in enumerate(search):
            self.btnEditarRowClick(row)
            name = self.getInputMarketText(index)

            if name != '':
                print(f"{AZUL}{PROJECT}: {BLANCO}Esta fila ya está hecha con Feature 5 = {name}\n{GRIS}")
                self.btnEditarRowClick(row)
            else:
                print(f'{AZUL}{PROJECT}: {BLANCO}Vendedor sin completar. Se realizará la petición a The Finder{GRIS}')
                url = self.getRowLink(row)
                if 'simple.ripley' in url:
                    print("ripley")
                    data = self.finder.data_ripley(url)
                else:
                    print("ochele")
                    data = self.finder.data_oechsle(url)
                if (data['status_code'] == 200) and (data['productSeller'] is not None):
                    print(f"THE FINDER: Encontré al vendedor = {data['productSeller']}")
                    self.sendInputMarketText(data["productSeller"])
                    # seller.click()
                    # seller.send_keys(data['productSeller'])
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
                    print(data['status_code'])
                    self.sendInputMarketText(index, data["status_code"])
                    # seller.click()
                    # seller.send_keys(data['status_code'])
                    self.driver.execute_script("arguments[0].style.color = 'red';"
                                                   "arguments[0].style.fontWeight = '900';",
                                        row.find_element('css selector', 'td[field="nombre"]'))
                    



                    row.find_element("css selector", "div[tabindex='0']").click() #btn editar
                    time.sleep(2)
                    row.find_element('css selector', '.ml-1').click() # btn Descartar
                    # Ocultar el elemento utilizando JavaScript
                    self.driver.execute_script("arguments[0].style.display = 'none';", row)
                else:
                    self.sendInputMarketText(index, "Sin seller")
                    # seller.click()
                    # seller.send_keys('Sin seller')
        return 1


    

    def marketplace(self):
        """ Get ready for action marketplace """
        self.__navWithUrl('taxonomia', 'taxonomizado')
        self.fillCountry(self.pais)
        self.fillRetails(self.retailsMarketplace)
        self.fillArea(self.areas)
        self.__fillDivision(self.divisiones)
        self.fillCategoria(self.categoriaMarketplace)
        self.btnObtenerClick()
        print(f"{PROJECT}: Ahora estás listo para Marketplacear, te recomiendo el método .fill_market()")
        

# ------------------------Welcome-MAIN-----------------------------
if __name__ == '__main__':
    hope: Hope
    try:
        hope = Hope()
    except Exception as e:
        print(f"error: {e}")
    finally:
        os.system('pause')
        hope.driver.close()

    # hope.taxonomizar()
