# settings_manager.py - Gestión de configuraciones y traducciones de la aplicación
import json
import os
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class AppSettings:
    """Configuraciones de la aplicación"""
    # Configuraciones generales
    language: str = "es"  # "es" o "en"
    theme: str = "dark"   # "dark" o "light"
    
    # Configuraciones de conversión
    use_threading: bool = True
    max_threads: int = 4
    default_output_dir: str = ""
    keep_original_files: bool = True
    
    # Configuraciones de calidad
    jpg_quality: int = 95
    webp_quality: int = 90
    png_compression: int = 6
    
    # Configuraciones de interfaz
    show_preview: bool = True
    auto_resize_preview: bool = True
    show_notifications: bool = True
    minimize_to_tray: bool = False
    
    # Configuraciones de historial
    max_history_items: int = 100
    auto_clear_history: bool = False
    
    # Configuraciones de drag & drop
    enable_drag_drop: bool = True
    auto_detect_format: bool = True

class SettingsManager:
    """Gestor de configuraciones de la aplicación"""
    
    def __init__(self, settings_file="settings.json"):
        self.settings_file = settings_file
        self.settings = AppSettings()
        self.load_settings()
    
    def load_settings(self):
        """Cargar configuraciones desde archivo"""
        try:
            if os.path.exists(self.settings_file):
                with open(self.settings_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                # Actualizar configuraciones existentes
                for key, value in data.items():
                    if hasattr(self.settings, key):
                        setattr(self.settings, key, value)
        except Exception as e:
            print(f"Error cargando configuraciones: {e}")
    
    def save_settings(self):
        """Guardar configuraciones a archivo"""
        try:
            # Convertir dataclass a diccionario
            settings_dict = {
                'language': self.settings.language,
                'theme': self.settings.theme,
                'use_threading': self.settings.use_threading,
                'max_threads': self.settings.max_threads,
                'default_output_dir': self.settings.default_output_dir,
                'keep_original_files': self.settings.keep_original_files,
                'jpg_quality': self.settings.jpg_quality,
                'webp_quality': self.settings.webp_quality,
                'png_compression': self.settings.png_compression,
                'show_preview': self.settings.show_preview,
                'auto_resize_preview': self.settings.auto_resize_preview,
                'show_notifications': self.settings.show_notifications,
                'minimize_to_tray': self.settings.minimize_to_tray,
                'max_history_items': self.settings.max_history_items,
                'auto_clear_history': self.settings.auto_clear_history,
                'enable_drag_drop': self.settings.enable_drag_drop,
                'auto_detect_format': self.settings.auto_detect_format
            }
            
            with open(self.settings_file, 'w', encoding='utf-8') as f:
                json.dump(settings_dict, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error guardando configuraciones: {e}")
    
    def get_setting(self, key: str, default=None):
        """Obtener una configuración específica"""
        return getattr(self.settings, key, default)
    
    def set_setting(self, key: str, value):
        """Establecer una configuración específica"""
        if hasattr(self.settings, key):
            setattr(self.settings, key, value)
            self.save_settings()
    
    def reset_to_defaults(self):
        """Resetear configuraciones a valores por defecto"""
        self.settings = AppSettings()
        self.save_settings()
    
    def get_quality_settings(self, format_type: str) -> Dict[str, Any]:
        """Obtener configuraciones de calidad para un formato específico"""
        quality_settings = {}
        
        if format_type == 'JPG':
            quality_settings = {
                'quality': self.settings.jpg_quality,
                'optimize': True
            }
        elif format_type == 'WEBP':
            quality_settings = {
                'quality': self.settings.webp_quality,
                'method': 6
            }
        elif format_type == 'PNG':
            quality_settings = {
                'optimize': True,
                'compress_level': self.settings.png_compression
            }
        
        return quality_settings
    
    def get_translations(self) -> Dict[str, str]:
        """Obtener traducciones según el idioma configurado"""
        translations = {
            'es': {
                'app_title': 'Pix', # <-- CAMBIO AQUÍ: Cambia 'Conversor Universal de Imágenes' a 'Pix'
                'select_file': 'Seleccionar Archivo',
                'convert': 'Convertir',
                'settings': 'Configuraciones',
                'history': 'Historial',
                'language': 'Idioma',
                'theme': 'Tema',
                'processing_mode': 'Modo de Procesamiento',
                'concurrent': 'Concurrente (Hilos)',
                'sequential': 'Secuencial',
                'quality': 'Calidad',
                'output_directory': 'Directorio de Salida',
                'conversion_completed': 'Conversión Completada',
                'error_occurred': 'Error Ocurrido',
                'file_not_found': 'Archivo no encontrado',
                'unsupported_format': 'Formato no soportado',
                'drag_drop_files': 'Arrastra archivos aquí',
                'clear_history': 'Limpiar Historial',
                'about': 'Acerca de',
                'exit': 'Salir',
                'select_output_dir_dialog': 'Seleccionar Directorio de Salida',
                'maintain_original_files': 'Mantener archivos originales',
                'show_notifications': 'Mostrar notificaciones',
                'enable_drag_drop': 'Habilitar arrastrar y soltar',
                'options': 'Opciones',
                'max_threads': 'Hilos máximos:',
                'png_compression': 'Compresión PNG',
                'reset_settings_confirm': '¿Está seguro de que desea restablecer todas las configuraciones?',
                'reset': 'Restablecer',
                'save': 'Guardar',
                'cancel': 'Cancelar',
                'history_title': 'Historial de Conversiones',
                'clear_history_confirm': '¿Está seguro de que desea limpiar el historial?',
                'close': 'Cerrar',
                'file': 'Archivo',
                'size': 'Tamaño',
                'selected_files': 'Archivos seleccionados:',
                'no_valid_files': 'No se encontraron archivos válidos para el formato de entrada seleccionado.',
                'success': 'Éxito',
                'partial_conversion': 'Conversión parcial:',
                'back': '← Regresar',
                'select_conversion': 'Seleccionar conversión:',
                'from': 'De:',
                'to': 'A:',
                'same_as_original_dir': 'Mismo directorio que el archivo original',
                'language_change_restart_prompt': 'El idioma ha cambiado. ¿Desea reiniciar la aplicación para aplicar los cambios?',
                'language_change_restart_info': 'Los cambios de idioma se aplicarán la próxima vez que inicie la aplicación.',
                'threads_max': 'Hilos máximos:',
                'language_es': 'Español',
                'language_en': 'English',
                'general_tab_name': 'General',
                'quality_tab_name': 'Calidad',
                'or_click_to_select': 'o haz clic para seleccionar'
            },
            'en': {
                'app_title': 'Pix', # <-- CAMBIO AQUÍ: Cambia 'Universal Image Converter' a 'Pix'
                'select_file': 'Select File',
                'convert': 'Convert',
                'settings': 'Settings',
                'history': 'History',
                'language': 'Language',
                'theme': 'Theme',
                'processing_mode': 'Processing Mode',
                'concurrent': 'Concurrent (Threads)',
                'sequential': 'Sequential',
                'quality': 'Quality',
                'output_directory': 'Output Directory',
                'conversion_completed': 'Conversion Completed',
                'error_occurred': 'Error Occurred',
                'file_not_found': 'File not found',
                'unsupported_format': 'Unsupported format',
                'drag_drop_files': 'Drag files here',
                'clear_history': 'Clear History',
                'about': 'About',
                'exit': 'Exit',
                'select_output_dir_dialog': 'Select Output Directory',
                'maintain_original_files': 'Keep original files',
                'show_notifications': 'Show notifications',
                'enable_drag_drop': 'Enable drag and drop',
                'options': 'Options',
                'max_threads': 'Max threads:',
                'png_compression': 'PNG Compression',
                'reset_settings_confirm': 'Are you sure you want to reset all settings?',
                'reset': 'Reset',
                'save': 'Save',
                'cancel': 'Cancel',
                'history_title': 'Conversion History',
                'clear_history_confirm': 'Are you sure you want to clear the history?',
                'close': 'Close',
                'file': 'File',
                'size': 'Size',
                'selected_files': 'Selected files:',
                'no_valid_files': 'No valid files found for the selected input format.',
                'success': 'Success',
                'partial_conversion': 'Partial Conversion:',
                'back': '← Back',
                'select_conversion': 'Select conversion:',
                'from': 'From:',
                'to': 'To:',
                'same_as_original_dir': 'Same directory as original file',
                'language_change_restart_prompt': 'Language has changed. Do you want to restart the application to apply the changes?',
                'language_change_restart_info': 'Language changes will apply the next time you start the application.',
                'threads_max': 'Max threads:',
                'language_es': 'Spanish',
                'language_en': 'English',
                'general_tab_name': 'General',
                'quality_tab_name': 'Quality',
                'or_click_to_select': 'or click to select'
            }
        }
        
        return translations.get(self.settings.language, translations['es'])
