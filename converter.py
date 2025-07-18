# converter.py - Módulo para convertir imágenes entre múltiples formatos

from PIL import Image
import os
import time
import json
from datetime import datetime
import threading
import queue

class ImageConverter:
    """
    Clase principal para conversión de imágenes con soporte para múltiples formatos
    """
    SUPPORTED_FORMATS = {
        'JPG': ['jpg', 'jpeg'],
        'PNG': ['png'],
        'WEBP': ['webp'],
        'BMP': ['bmp'],
        'TIFF': ['tiff', 'tif'],
        'GIF': ['gif'],
        'ICO': ['ico'],
        'HEIC': ['heic', 'heif']  # Requiere pillow-heif si quieres HEIC
    }

    QUALITY_SETTINGS = {
        'JPG': {'quality': 95, 'optimize': True},
        'WEBP': {'quality': 90, 'method': 6},
        'PNG': {'optimize': True, 'compress_level': 6},
        'TIFF': {'compression': 'tiff_lzw'},
    }

    def __init__(self, history_file="conversion_history.json"):
        self.history_file = history_file
        self._load_history()

    def _load_history(self):
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
            else:
                self.history = []
        except Exception:
            self.history = []

    def _save_history(self):
        try:
            with open(self.history_file, 'w', encoding='utf-8') as f:
                # Guardar solo las últimas 100 entradas
                json.dump(self.history[-100:], f, indent=2, ensure_ascii=False)
        except Exception:
            pass

    def _add_to_history(self, input_path, output_path, in_fmt, out_fmt, success):
        entry = {
            'timestamp': datetime.now().isoformat(),
            'input_file': os.path.basename(input_path),
            'output_file': os.path.basename(output_path),
            'input_format': in_fmt,
            'output_format': out_fmt,
            'success': success,
            'input_size': os.path.getsize(input_path) if os.path.exists(input_path) else 0,
            'output_size': os.path.getsize(output_path) if success and os.path.exists(output_path) else 0
        }
        self.history.append(entry)
        self._save_history()

    def get_format_from_extension(self, file_path):
        ext = os.path.splitext(file_path)[1].lower().lstrip('.')
        for fmt, exts in self.SUPPORTED_FORMATS.items():
            if ext in exts:
                return fmt
        return None

    def convert_image(self, input_path, output_path, output_format,
                      quality_settings=None, progress_callback=None):
        """
        Convierte una sola imagen.
        """
        try:
            if progress_callback: progress_callback(10)
            in_fmt = self.get_format_from_extension(input_path)
            if not in_fmt:
                return False, "Formato de entrada no soportado"

            if progress_callback: progress_callback(25)
            with Image.open(input_path) as img:
                if progress_callback: progress_callback(50)
                img = self._process_for_format(img, output_format)
                if progress_callback: progress_callback(75)

                save_kwargs = quality_settings or self.QUALITY_SETTINGS.get(output_format, {})
                time.sleep(0.1)  # pequeña pausa para animación de progreso

                fmt = 'JPEG' if output_format == 'JPG' else output_format
                if output_format == 'ICO':
                    # ICO necesita RGBA en varios tamaños
                    if img.mode != 'RGBA': img = img.convert('RGBA')
                    img.save(output_path, format='ICO', sizes=[(16,16),(32,32),(48,48)])
                else:
                    img.save(output_path, format=fmt, **save_kwargs)

                if progress_callback: progress_callback(100)
                self._add_to_history(input_path, output_path, in_fmt, output_format, True)
                return True, f"Convertido a {output_format}"

        except FileNotFoundError:
            self._add_to_history(input_path, output_path, None, output_format, False)
            return False, "Archivo no encontrado."
        except PermissionError:
            self._add_to_history(input_path, output_path, None, output_format, False)
            return False, "Sin permisos para acceder."
        except Exception as e:
            self._add_to_history(input_path, output_path, None, output_format, False)
            return False, f"Error: {e}"

    def _process_for_format(self, img, output_format):
        """
        Ajusta modo de color/transparencia según formato de salida.
        """
        if output_format == 'JPG':
            # Si hay canal alfa, compón sobre blanco
            if img.mode in ('RGBA','LA') or (img.mode=='P' and 'transparency' in img.info):
                img = img.convert('RGBA')
                fondo = Image.new('RGB', img.size, (255,255,255))
                fondo.paste(img, mask=img.split()[-1])
                return fondo
            return img.convert('RGB')

        if output_format in ('PNG','WEBP'):
            # Asegurar modo que soporte alfa
            if 'A' not in img.mode:
                return img.convert('RGBA')
            return img

        if output_format in ('BMP','TIFF'):
            # No soportan alfa
            if 'A' in img.mode:
                fondo = Image.new('RGB', img.size, (255,255,255))
                img = img.convert('RGBA')
                fondo.paste(img, mask=img.split()[-1])
                return fondo
            return img.convert('RGB')

        if output_format == 'ICO':
            return img.convert('RGBA')

        return img

    def batch_convert(self, files, output_dir, output_format,
                      use_threading=True, max_threads=4, progress_callback=None,
                      quality_settings=None):
        """
        Convierte múltiples archivos, retorno lista de tuplas (success,msg,path).
        """
        os.makedirs(output_dir, exist_ok=True)
        total = len(files)
        completed = 0
        results = []

        if use_threading and total > 1:
            q = queue.Queue()
            lock = threading.Lock()

            def worker(path):
                nonlocal completed
                name = os.path.splitext(os.path.basename(path))[0]
                out = os.path.join(output_dir, f"{name}.{output_format.lower()}")
                success, msg = self.convert_image(path, out, output_format, quality_settings)
                q.put((success, msg, path))
                with lock:
                    completed += 1
                    if progress_callback:
                        progress_callback(int(completed/total*100))

            threads = []
            idx = 0
            while idx < total or threads:
                while idx < total and len(threads) < max_threads:
                    t = threading.Thread(target=worker, args=(files[idx],))
                    t.start()
                    threads.append(t)
                    idx += 1
                threads = [t for t in threads if t.is_alive()]
                time.sleep(0.01)

            for t in threads: t.join()
            while not q.empty():
                results.append(q.get())

        else:
            for i,path in enumerate(files):
                name = os.path.splitext(os.path.basename(path))[0]
                out = os.path.join(output_dir, f"{name}.{output_format.lower()}")
                success, msg = self.convert_image(path, out, output_format, quality_settings)
                results.append((success, msg, path))
                if progress_callback:
                    progress_callback(int((i+1)/total*100))

        return results


# ——————————————————————————————
# Wrappers para compatibilidad con ui.py
# ——————————————————————————————

def convert_jpg_to_png(input_path, output_path):
    conv = ImageConverter()
    return conv.convert_image(input_path, output_path, 'PNG')

def convert_png_to_webp(input_path, output_path):
    conv = ImageConverter()
    return conv.convert_image(input_path, output_path, 'WEBP')

def convert_webp_to_jpg(input_path, output_path):
    conv = ImageConverter()
    return conv.convert_image(input_path, output_path, 'JPG')
