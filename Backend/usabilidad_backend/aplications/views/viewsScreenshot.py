import time, os
from django.conf import settings
from django.apps import apps
from rest_framework.response import Response
from rest_framework.views import APIView
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from django.http import FileResponse
from selenium.webdriver.common.by import By


# Vista para capturar una captura de pantalla de una URL utilizando Selenium
class CaptureScreenshotView(APIView):
    """
    Vista para capturar una captura de pantalla de una URL proporcionada utilizando Selenium y devolverla como respuesta.
    """

    def capture_screenshot(self, url, output_path):
        """
        Función para capturar la captura de pantalla de la URL proporcionada y guardarla en una ruta específica.
        """
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Ejecutar en modo sin interfaz gráfica
        chrome_options.add_argument('--no-sandbox')  # Para servidores
        chrome_options.add_argument('--disable-dev-shm-usage')  # Optimización en entornos con poca memoria
        chrome_options.add_argument('--disable-gpu')  # Evitar el uso de la GPU

        service = ChromeService(executable_path=ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)

        try:
            # Acceder a la URL y esperar hasta que se cargue completamente
            driver.get(url)
            
            # Esperar que el iframe de Figma se cargue (esto puede necesitar ajustes)
            time.sleep(10)  # Aumentar el tiempo de espera si es necesario
            
            # Verificar que el iframe de Figma está presente (puedes ajustar el selector si es necesario)
            iframe = driver.find_element(By.TAG_NAME, 'iframe')

            if iframe:
                driver.switch_to.frame(iframe)  # Cambiar al contexto del iframe si es necesario
                time.sleep(5)  # Esperar más tiempo dentro del iframe

            # Tomar la captura
            driver.save_screenshot(output_path)
        
        except Exception as e:
            print(f"Error capturando la pantalla: {e}")
        
        finally:
            driver.quit()  # Cerrar el navegador

    def post(self, request):
        """
        POST: Recibe una URL y captura una captura de pantalla de la página web, devolviéndola como respuesta.
        """
        url = request.data.get('url')
        if not url:
            return Response({'error': 'URL is required'}, status=400)

        app_dir = apps.get_app_config('aplications').path
        output_path = os.path.join(app_dir, 'screenshots', 'capture.png')

        # Crear la carpeta 'screenshots' si no existe
        if not os.path.exists(os.path.dirname(output_path)):
            os.makedirs(os.path.dirname(output_path))

        # Capturar la pantalla
        self.capture_screenshot(url, output_path)

        # Devolver la captura como respuesta
        if os.path.exists(output_path):
            return FileResponse(open(output_path, 'rb'), content_type='image/png')
        else:
            return Response({'error': 'Screenshot failed'}, status=500)