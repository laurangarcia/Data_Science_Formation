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

class HentaiScraper:
    def __init__(self, driver_path):
        self.driver_path = driver_path
        self.driver = None
        self.downloaded_count = 0
        self.target_count = 540
        self.processed_urls = set()  # Para evitar duplicados
        
        # Definir paths dentro de results\drawing
        self.base_dir = "results\\hentai"
        self.download_folder = os.path.join(self.base_dir, "hentai_images")
        self.urls_file = os.path.join(self.base_dir, "hentai_urls.txt")
        self.metadata_file = os.path.join(self.base_dir, "hentai_metadata.json")
        
        # Crear directorios si no existen
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)
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
    
    def infinite_scroll(self):
        """Scroll infinito hasta alcanzar el número objetivo de imágenes"""
        print("Iniciando scroll infinito...")
        
        last_height = self.driver.execute_script("return document.body.scrollHeight")
        scroll_attempts = 0
        max_scroll_attempts = 50  # Límite para evitar bucle infinito
        no_new_images_count = 0
        max_no_new_images = 5  # Máximo de intentos sin nuevas imágenes
        
        while (self.downloaded_count < self.target_count and 
               scroll_attempts < max_scroll_attempts and
               no_new_images_count < max_no_new_images):
            
            # Scroll al fondo de la página
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(2.5)  # Esperar a que carguen nuevas imágenes
            
            # Verificar si hay nuevas imágenes
            current_images = self.driver.find_elements(By.CSS_SELECTOR, "img[src*='.jpg'], img[src*='.jpeg'], img[src*='.png']")
            print(f"Imágenes encontradas después del scroll: {len(current_images)}")
            
            # Extraer y procesar imágenes
            new_images_processed = self.process_visible_images()
            
            if new_images_processed > 0:
                no_new_images_count = 0  # Resetear contador si encontramos nuevas imágenes
                print(f"Procesadas {new_images_processed} nuevas imágenes")
            else:
                no_new_images_count += 1
                print(f"No se encontraron nuevas imágenes ({no_new_images_count}/{max_no_new_images})")
            
            # Verificar si la altura de la página cambió
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                scroll_attempts += 1
                print(f"Sin cambio de altura ({scroll_attempts}/{max_scroll_attempts})")
                
                # Intentar hacer scroll incremental si no hay cambio
                current_position = self.driver.execute_script("return window.pageYOffset")
                self.driver.execute_script(f"window.scrollTo(0, {current_position + 500});")
                time.sleep(1)
            else:
                scroll_attempts = 0
                last_height = new_height
            
            # Mostrar progreso
            print(f"Progreso: {self.downloaded_count}/{self.target_count} imágenes descargadas")
            
            # Pequeña pausa entre ciclos
            time.sleep(1)
        
        print("Scroll infinito completado")
    
    def process_visible_images(self):
        """Procesar todas las imágenes visibles en la página"""
        new_images_processed = 0
        
        # Buscar elementos de imagen
        selectors = [
            "img[src*='.jpg']",
            "img[src*='.jpeg']", 
            "img[src*='.png']",
            "[data-testid='gallery-items-container'] img",
            "figure img",
            ".gallery-asset__thumb img",
            ".MosaicAsset-module__image___jbMhr"  # Selector común en iStock
        ]
        
        for selector in selectors:
            if self.downloaded_count >= self.target_count:
                break
                
            try:
                img_elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                
                for img in img_elements:
                    if self.downloaded_count >= self.target_count:
                        break
                        
                    try:
                        src = img.get_attribute('src')
                        if not src or src in self.processed_urls:
                            continue
                            
                        # Verificar si es una URL de imagen válida
                        if any(ext in src.lower() for ext in ['.jpg', '.jpeg', '.png']):
                            # Intentar obtener la versión de alta resolución
                            high_res_src = self.get_high_resolution_url(src)
                            
                            if high_res_src in self.processed_urls:
                                continue
                                
                            # Intentar obtener atributo alt para la descripción
                            alt_text = img.get_attribute('alt') or "Imagen de drawing"
                            
                            # Crear datos de la imagen
                            image_info = {
                                'url': high_res_src,
                                'alt': alt_text,
                                'page_url': self.driver.current_url
                            }
                            
                            # Descargar imagen
                            if self.download_image(image_info):
                                self.processed_urls.add(high_res_src)
                                self.processed_urls.add(src)  # También marcar la URL original
                                new_images_processed += 1
                                
                    except StaleElementReferenceException:
                        continue
                    except Exception as e:
                        print(f"Error procesando elemento: {e}")
                        continue
                        
            except Exception as e:
                print(f"Error con selector {selector}: {e}")
                continue
        
        return new_images_processed
    
    def get_high_resolution_url(self, url):
        """Convertir URL a versión de alta resolución"""
        high_res_url = url
        # Patrones comunes de iStock para diferentes tamaños
        size_replacements = [
            ('_s.jpg', '_l.jpg'),
            ('_m.jpg', '_l.jpg'),
            ('_s.jpeg', '_l.jpeg'),
            ('_m.jpeg', '_l.jpeg'),
            ('-s.jpg', '-l.jpg'),
            ('-m.jpg', '-l.jpg'),
            ('_360.jpg', '_l.jpg'),
            ('_480.jpg', '_l.jpg'),
            ('_100.jpg', '_l.jpg'),
            ('_200.jpg', '_l.jpg')
        ]
        
        for old, new in size_replacements:
            if old in high_res_url:
                high_res_url = high_res_url.replace(old, new)
                break
        
        return high_res_url
    
    def download_image(self, image_info):
        """Descargar una imagen individual y guardar su metadata"""
        url = image_info['url']
        alt_text = image_info['alt']
        page_url = image_info['page_url']
        
        if '1px.png' in url:
            return False

        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
                'Referer': 'https://www.pornpics.com/es/hentai/',
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
                    
                    # Verificar tamaño mínimo (evitar iconos/thumbnails pequeños)
                    if width < 200 or height < 200:
                        print(f"Imagen demasiado pequeña: {width}x{height} - {url}")
                        return False
                        
                except:
                    print(f"Imagen no válida: {url}")
                    return False
                
                # Generar nombre de archivo único
                filename = f"hentai_{uuid.uuid4().hex[:8]}.jpg"
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
                    'category': 'hentai'
                }
                
                # Guardar metadata
                self.save_image_metadata(metadata)
                
                self.downloaded_count += 1
                
                print(f"Descargada imagen {self.downloaded_count}/{self.target_count}: {filename}")
                return True
                
        except Exception as e:
            print(f"Error descargando {url}: {e}")
            return False
    
    def scrape_images(self):
        """Función principal para scrapear imágenes con scroll infinito"""
        try:
            print("Iniciando scraping con scroll infinito...")
            self.driver.get("https://www.pornpics.com/es/hentai/")
            
            # Esperar a que cargue la página
            WebDriverWait(self.driver, 15).until(
                EC.presence_of_element_located((By.TAG_NAME, "img"))
            )
            
            self.accept_cookies()
            time.sleep(3)
            
            # Procesar imágenes iniciales
            print("Procesando imágenes iniciales...")
            self.process_visible_images()
            
            # Scroll infinito hasta alcanzar el objetivo
            self.infinite_scroll()
            
            # Si aún no hemos alcanzado el objetivo, intentar scroll adicional
            if self.downloaded_count < self.target_count:
                print("Intentando scroll adicional...")
                for _ in range(3):  # Intentar 3 veces más
                    self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(3)
                    self.process_visible_images()
                    if self.downloaded_count >= self.target_count:
                        break
            
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
    driver_path = r"C:\\Users\\Admin\\Documents\\python_ciencia_datos\\Data_Science_Formation\\Scraping_python\\selenium\\chromedriver.exe"
    
    scraper = HentaiScraper(driver_path)
    scraper.scrape_images()
