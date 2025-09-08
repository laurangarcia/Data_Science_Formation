import os
import time
import requests
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from urllib.parse import urljoin, urlparse
import uuid
from PIL import Image
import io
from datetime import datetime

class iStockNeutralScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None
        self.downloaded_count = 0
        self.target_count = 540
        self.download_folder = "neutral_images"
        self.urls_file = "neutral_image_urls.txt"  # Archivo de texto para URLs
        self.metadata_file = "neutral_metadata.json"  # Archivo JSON para metadata

        # Crear carpeta de descarga si no existe
        if not os.path.exists(self.download_folder):
            os.makedirs(self.download_folder)
        
        # Inicializar archivos
        self.initialize_files()
        
        self.setup_driver()
    
    def initialize_files(self):
        """Inicializar los archivos de URLs y metadata"""
        # Inicializar archivo de URLs (vacío)
        with open(self.urls_file, 'w', encoding='utf-8') as f:
            f.write("")
        
        # Inicializar archivo de metadata con array vacío
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump([], f)
    
    def save_image_url(self, url):
        """Guardar URL en el archivo de texto (una por línea)"""
        with open(self.urls_file, 'a', encoding='utf-8') as f:
            f.write(url + '\n')
    
    def save_image_metadata(self, metadata):
        """Guardar metadata en el archivo JSON"""
        # Leer metadata existente
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                try:
                    existing_metadata = json.load(f)
                except:
                    existing_metadata = []
        else:
            existing_metadata = []
        
        # Agregar nueva metadata
        existing_metadata.append(metadata)
        
        # Guardar metadata actualizada
        with open(self.metadata_file, 'w', encoding='utf-8') as f:
            json.dump(existing_metadata, f, indent=2, ensure_ascii=False)
    
    def setup_driver(self):
        """Configurar el driver de Chrome"""
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Comentado para ver el proceso
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
        chrome_options.add_experimental_option('useAutomationExtension', False)
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Configurar para evitar detección como bot
        chrome_options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
        
        service = Service(self.driver_path)
        self.driver = webdriver.Chrome(service=service, options=chrome_options)
        self.driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    
    def accept_cookies(self):
        """Aceptar cookies si es necesario"""
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Aceptar') or contains(text(), 'Accept') or contains(@aria-label, 'Accept')]"))
            )
            cookie_button.click()
            print("Cookies aceptadas")
            time.sleep(2)
        except:
            print("No se encontró botón de cookies o ya estaba aceptado")
    
    def scroll_page(self):
        """Hacer scroll suave para cargar todas las imágenes"""
        print("Haciendo scroll para cargar imágenes...")
        
        # Obtener altura inicial
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_pause_time = 1.5
        scroll_increment = 800  # Scroll suave en incrementos
        
        # Empezar desde la parte superior
        self.driver.execute_script("window.scrollTo(0, 0);")
        time.sleep(1)
        
        current_position = 0
        max_scroll_attempts = 20
        scroll_attempts = 0
        
        while scroll_attempts < max_scroll_attempts:
            # Scroll incremental
            current_position += scroll_increment
            self.driver.execute_script(f"window.scrollTo(0, {current_position});")
            time.sleep(scroll_pause_time / 3)
            
            # Obtener nueva altura después del scroll
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Si hemos llegado al final
            if current_position >= new_height:
                break
                
            # Si no hay cambio después de varios intentos, salir
            if new_height == last_height:
                scroll_attempts += 1
            else:
                scroll_attempts = 0
                last_height = new_height
                
            # Si ya tenemos suficientes imágenes, podemos terminar antes
            images = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='.jpg'], img[src*='.jpeg'], img[src*='.png']")
            if len(images) > self.target_count * 1.5:  # Margen para asegurar calidad
                break
        
        # Scroll final al fondo para asegurar
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
    
    def extract_image_data(self):
        """Extraer URLs de imágenes de alta calidad y sus metadatos"""
        image_data = []
        
        # Buscar elementos de imagen - patrones específicos de iStock
        selectors = [
            "img[src*='.jpg']",
            "img[src*='.jpeg']", 
            "img[src*='.png']",
            "[data-testid='gallery-items-container'] img",
            "figure img",
            ".gallery-asset__thumb img"
        ]
        
        for selector in selectors:
            if self.downloaded_count >= self.target_count:
                break
                
            try:
                img_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                print(f"Encontrados {len(img_elements)} elementos con selector {selector}")
                
                for img in img_elements:
                    if self.downloaded_count >= self.target_count:
                        break
                        
                    try:
                        src = img.get_attribute('src')
                        if not src:
                            continue
                            
                        # Verificar si es una URL de imagen válida
                        if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png']):
                            # Intentar obtener la versión de alta resolución
                            high_res_src = src
                            for size in ['s', 'm', '360', '480']:
                                high_res_src = high_res_src.replace(f'_{size}.', '_l.').replace(f'-{size}.', '-l.')
                            
                            # Intentar obtener atributo alt para la descripción
                            alt_text = img.get_attribute('alt') or "Imagen de cosplay"
                            
                            # Crear datos de la imagen
                            image_data.append({
                                'url': high_res_src,
                                'alt': alt_text,
                                'page_url': self.driver.current_url
                            })
                                
                    except StaleElementReferenceException:
                        continue
                    except Exception as e:
                        print(f"Error procesando elemento: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error con selector {selector}: {e}")
                continue
        
        return image_data
    
    def download_image(self, image_info):
        """Descargar una imagen individual y guardar su metadata"""
        url = image_info['url']
        alt_text = image_info['alt']
        page_url = image_info['page_url']
        
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.istockphoto.com/es/collaboration/boards/AwxaA_jHWUyul-5RWiY4UA',
                'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8'
            }
            
            response = requests.get(url, headers=headers, stream=True, timeout=30)
            
            if response.status_code == 200:
                # Verificar que sea una imagen válida
                image_data = response.content
                try:
                    img = Image.open(io.BytesIO(image_data))
                    img.verify()  # Verificar que es una imagen válida
                    
                    # Obtener dimensiones de la imagen
                    img = Image.open(io.BytesIO(image_data))
                    width, height = img.size
                except:
                    print(f"Imagen no válida: {url}")
                    return False
                
                # Generar nombre de archivo único
                filename = f"cosplay_{uuid.uuid4().hex[:8]}.jpg"
                filepath = os.path.join(self.download_folder, filename)
                
                with open(filepath, 'wb') as f:
                    f.write(image_data)
                
                # Guardar URL en el archivo de texto (una por línea)
                self.save_image_url(url)
                
                # Crear metadata
                metadata = {
                    'id': str(uuid.uuid4()),
                    'filename': filename,
                    'download_date': datetime.now().isoformat(),
                    'url': url,
                    'source_page': page_url,
                    'description': alt_text,
                    'dimensions': {
                        'width': width,
                        'height': height
                    },
                    'file_size': len(image_data),
                    'category': 'cosplay'
                }
                
                # Guardar metadata
                self.save_image_metadata(metadata)
                
                self.downloaded_count += 1
                
                print(f"Descargada imagen {self.downloaded_count}/{self.target_count}: {filename}")
                return True
                
        except Exception as e:
            print(f"Error descargando {url}: {e}")
            return False
    
    def go_to_next_page(self, current_page):
        """Navegar a la siguiente página"""
        try:
            next_page = current_page + 1
            next_url = f"https://www.istockphoto.com/es/collaboration/boards/AwxaA_jHWUyul-5RWiY4UA?page={next_page}"
            print(f"Navegando a la página {next_page}: {next_url}")
            
            self.driver.get(next_url)
            
            # Esperar a que cargue la página
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            
            time.sleep(3)
            return True
            
        except Exception as e:
            print(f"Error navegando a la página {next_page}: {e}")
            return False
    
    def scrape_images(self):
        """Función principal para scrapear imágenes"""
        try:
            current_page = 1
            
            while self.downloaded_count < self.target_count and current_page <= 100:
                print(f"\n=== Procesando página {current_page} ===")
                
                if current_page == 1:
                    self.driver.get("https://www.istockphoto.com/es/collaboration/boards/AwxaA_jHWUyul-5RWiY4UA")
                else:
                    if not self.go_to_next_page(current_page - 1):
                        print("No se pudo navegar a la siguiente página")
                        break
                
                # Esperar a que cargue la página
                WebDriverWait(self.driver, 15).until(
                    EC.presence_of_element_located((By.TAG_NAME, "img"))
                )
                
                self.accept_cookies()
                time.sleep(3)
                
                # Hacer scroll para cargar más imágenes
                self.scroll_page()
                
                # Extraer URLs de imágenes y sus metadatos
                print("Extrayendo URLs de imágenes y metadatos...")
                image_data = self.extract_image_data()
                
                print(f"Encontradas {len(image_data)} imágenes potenciales en la página {current_page}")
                
                # Descargar imágenes
                for i, img_info in enumerate(image_data):
                    if self.downloaded_count >= self.target_count:
                        break
                    
                    if self.download_image(img_info):
                        time.sleep(1)  # Espera entre descargas para evitar bloqueos
                    
                    # Mostrar progreso cada 10 imágenes
                    if (i + 1) % 10 == 0:
                        print(f"Procesadas {i + 1} URLs, descargadas {self.downloaded_count} imágenes")
                
                current_page += 1
                
                # Pausa entre páginas
                time.sleep(2)
            
        except Exception as e:
            print(f"Error durante el scraping: {e}")
        
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Limpiar y cerrar el driver"""
        if self.driver:
            self.driver.quit()
        print(f"Scraping completado. Descargadas {self.downloaded_count} imágenes en la carpeta '{self.download_folder}'")
        print(f"URLs guardadas en: {self.urls_file}")
        print(f"Metadatos guardados en: {self.metadata_file}")

# Configuración y ejecución
if __name__ == "__main__":
    driver_path = r"C:\Users\Admin\Documents\python_ciencia_datos\Data_Science_Formation\Scraping_python\selenium\chromedriver.exe"
    
    scraper = iStockNeutralScraper(driver_path)
    scraper.scrape_images()