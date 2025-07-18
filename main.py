# main.py - Punto de entrada principal de la aplicación
from ui import ConverterWindow
from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon
import sys
import os

def resource_path(relative_path):
    """
    Obtener la ruta correcta de los recursos tanto en desarrollo como en ejecutable.
    PyInstaller crea un directorio temporal y almacena la ruta en _MEIPASS.
    """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Configurar icono de la aplicación para la taskbar (Windows)
    # Se busca primero 'app_icon.ico' y luego 'assets/icon.png'
    icon_paths = [
        resource_path("app_icon.ico"),
        resource_path("assets/icon.png")
    ]
    
    for icon_path in icon_paths:
        if os.path.exists(icon_path):
            app.setWindowIcon(QIcon(icon_path))
            break
    
    # Configurar información de la aplicación
    app.setApplicationName("Pix") # <-- CAMBIO AQUÍ: Cambia "Universal Image Converter" a "Pix"
    app.setApplicationVersion("2.0")
    app.setOrganizationName("ImageConverter") # Puedes mantener este o cambiarlo también si lo deseas
    
    window = ConverterWindow()
    window.show()
    sys.exit(app.exec())
