# ui.py - Interfaz gráfica mejorada para conversor universal de imágenes
from PyQt6.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout,
                            QHBoxLayout, QPushButton, QLabel, QFileDialog,
                            QProgressBar, QComboBox, QDialog, QGridLayout,
                            QCheckBox, QSpinBox, QSlider, QTextEdit, QTabWidget,
                            QListWidget, QListWidgetItem, QMessageBox, QFrame,
                            QScrollArea, QButtonGroup, QRadioButton, QGroupBox)
from PyQt6.QtGui import QIcon, QPixmap, QAction, QFont, QPainter, QColor
from PyQt6.QtCore import Qt, QTimer, QThread, pyqtSignal, QMimeData, QSize
import os
import sys
from datetime import datetime
from converter import ImageConverter
from settings_manager import SettingsManager
from PIL import Image, ImageQt

def resource_path(relative_path):
    """Obtener la ruta correcta de los recursos"""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    full_path = os.path.join(base_path, relative_path)
    print(f"Intentando cargar recurso: {full_path}")  # Depuración
    return full_path

class ConversionThread(QThread):
    """
    Hilo para conversión de imágenes, soporta tanto archivos individuales como lotes.
    Emite progreso general.
    """
    finished = pyqtSignal(bool, str)
    progress = pyqtSignal(int)

    def __init__(self, converter, files_to_convert, output_format, quality_settings, default_output_dir):
        super().__init__()
        self.converter = converter
        self.files_to_convert = files_to_convert
        self.output_format = output_format
        self.quality_settings = quality_settings
        self.default_output_dir = default_output_dir

    def run(self):
        total_files = len(self.files_to_convert)
        if total_files == 0:
            self.finished.emit(False, "No files to convert.")
            return

        success_count = 0
        results = []

        if total_files == 1:
            # Single file conversion
            input_path = self.files_to_convert[0]
            output_dir = self.default_output_dir or os.path.dirname(input_path)
            output_name = os.path.splitext(os.path.basename(input_path))[0]
            output_path = os.path.join(output_dir, f"{output_name}.{self.output_format.lower()}")

            def single_progress_callback(value):
                self.progress.emit(value)

            success, message = self.converter.convert_image(
                input_path,
                output_path,
                self.output_format,
                self.quality_settings,
                single_progress_callback
            )
            self.finished.emit(success, message)
        else:
            # Batch conversion
            results = self.converter.batch_convert(
                self.files_to_convert,
                self.default_output_dir,
                self.output_format,
                progress_callback=self.progress.emit,
                quality_settings=self.quality_settings
            )

            for success, message, _ in results:
                if success:
                    success_count += 1

            if success_count == total_files:
                message = "Conversion completed." + f" ({success_count}/{total_files})"
                self.finished.emit(True, message)
            else:
                message = "Partial conversion." + f" {success_count}/{total_files} files converted."
                self.finished.emit(False, message)

class SettingsDialog(QDialog):
    """Diálogo de configuraciones"""

    def __init__(self, settings_manager, parent=None):
        super().__init__(parent)
        self.settings_manager = settings_manager
        self.translations = self.settings_manager.get_translations()
        self.original_language = self.settings_manager.settings.language
        self.init_ui()
        self.apply_theme()

    def apply_theme(self):
        """Aplicar tema oscuro al diálogo"""
        dark_style = """
        QDialog {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QLabel {
            color: #FFFFFF;
            background-color: transparent;
        }
        QPushButton {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: 1px solid #666666;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #5A5A5A;
        }
        QPushButton:pressed {
            background-color: #3A3A3A;
        }
        QComboBox {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: 1px solid #666666;
            padding: 5px;
            border-radius: 4px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #FFFFFF;
        }
        QSpinBox, QSlider {
            background-color: #3A3A3A;
            color: #FFFFFF;
            border: 1px solid #666666;
            border-radius: 4px;
            padding: 2px;
        }
        QGroupBox {
            font-weight: bold;
            color: #FFFFFF;
            margin-top: 10px;
            border: 1px solid #555555;
            border-radius: 5px;
            padding-top: 15px;
        }
        QGroupBox::title {
            subcontrol-origin: margin;
            subcontrol-position: top center;
            padding: 0 3px;
            background-color: #2E2E2E;
        }
        QCheckBox {
            color: #FFFFFF;
        }
        QRadioButton {
            color: #FFFFFF;
        }
        """
        self.setStyleSheet(dark_style)

    def init_ui(self):
        self.setWindowTitle(self.translations['settings'])
        icon = QIcon(resource_path("assets/configuracion.png"))
        if icon.isNull():
            print("Error: No se pudo cargar el icono configuracion.png para la ventana de configuraciones")
        self.setWindowIcon(icon)
        self.setFixedSize(500, 600)
        layout = QVBoxLayout()

        # Crear tabs
        self.tabs = QTabWidget()

        # Tab General
        self.general_tab = QWidget()
        general_layout = QVBoxLayout()

        # Idioma
        self.lang_group = QGroupBox(self.translations['language'])
        lang_layout = QHBoxLayout()
        self.lang_combo = QComboBox()
        self.lang_combo.addItem(self.translations['language_es'], "es")
        self.lang_combo.addItem(self.translations['language_en'], "en")
        current_lang_index = self.lang_combo.findData(self.settings_manager.settings.language)
        if current_lang_index != -1:
            self.lang_combo.setCurrentIndex(current_lang_index)
        lang_layout.addWidget(self.lang_combo)
        self.lang_group.setLayout(lang_layout)
        general_layout.addWidget(self.lang_group)

        # Modo de procesamiento
        self.proc_group = QGroupBox(self.translations['processing_mode'])
        proc_layout = QVBoxLayout()
        self.threading_radio = QRadioButton(self.translations['concurrent'])
        self.sequential_radio = QRadioButton(self.translations['sequential'])
        if self.settings_manager.settings.use_threading:
            self.threading_radio.setChecked(True)
        else:
            self.sequential_radio.setChecked(True)
        proc_layout.addWidget(self.threading_radio)
        proc_layout.addWidget(self.sequential_radio)
        threads_layout = QHBoxLayout()
        self.threads_label = QLabel(self.translations['threads_max'])
        threads_layout.addWidget(self.threads_label)
        self.threads_spin = QSpinBox()
        self.threads_spin.setRange(1, 8)
        self.threads_spin.setValue(self.settings_manager.settings.max_threads)
        threads_layout.addWidget(self.threads_spin)
        proc_layout.addLayout(threads_layout)
        self.proc_group.setLayout(proc_layout)
        general_layout.addWidget(self.proc_group)

        # Directorio de salida
        self.output_group = QGroupBox(self.translations['output_directory'])
        output_layout = QVBoxLayout()
        self.output_dir_label = QLabel(self.settings_manager.settings.default_output_dir or self.translations['same_as_original_dir'])
        self.output_dir_button = QPushButton(self.translations['select_output_dir_dialog'])
        self.output_dir_button.clicked.connect(self.select_output_dir)
        output_layout.addWidget(self.output_dir_label)
        output_layout.addWidget(self.output_dir_button)
        self.output_group.setLayout(output_layout)
        general_layout.addWidget(self.output_group)

        # Opciones adicionales
        self.options_group = QGroupBox(self.translations['options'])
        options_layout = QVBoxLayout()
        self.keep_original_check = QCheckBox(self.translations['maintain_original_files'])
        self.keep_original_check.setChecked(self.settings_manager.settings.keep_original_files)
        self.show_notifications_check = QCheckBox(self.translations['show_notifications'])
        self.show_notifications_check.setChecked(self.settings_manager.settings.show_notifications)
        self.drag_drop_check = QCheckBox(self.translations['enable_drag_drop'])
        self.drag_drop_check.setChecked(self.settings_manager.settings.enable_drag_drop)
        options_layout.addWidget(self.keep_original_check)
        options_layout.addWidget(self.show_notifications_check)
        options_layout.addWidget(self.drag_drop_check)
        self.options_group.setLayout(options_layout)
        general_layout.addWidget(self.options_group)

        self.general_tab.setLayout(general_layout)
        icon = QIcon(resource_path("assets/configuracion.png"))
        if icon.isNull():
            print("Error: No se pudo cargar el icono configuracion.png para la pestaña General")
        self.tabs.addTab(self.general_tab, icon, self.translations['general_tab_name'])

        # Tab Calidad
        self.quality_tab = QWidget()
        quality_layout = QVBoxLayout()

        # JPG Quality
        self.jpg_group = QGroupBox("JPG " + self.translations['quality'])
        jpg_layout = QVBoxLayout()
        self.jpg_quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.jpg_quality_slider.setRange(1, 100)
        self.jpg_quality_slider.setValue(self.settings_manager.settings.jpg_quality)
        self.jpg_quality_label = QLabel(f"{self.translations['quality']}: {self.settings_manager.settings.jpg_quality}%")
        self.jpg_quality_slider.valueChanged.connect(lambda v: self.jpg_quality_label.setText(f"{self.translations['quality']}: {v}%"))
        jpg_layout.addWidget(self.jpg_quality_label)
        jpg_layout.addWidget(self.jpg_quality_slider)
        self.jpg_group.setLayout(jpg_layout)
        quality_layout.addWidget(self.jpg_group)

        # WebP Quality
        self.webp_group = QGroupBox("WebP " + self.translations['quality'])
        webp_layout = QVBoxLayout()
        self.webp_quality_slider = QSlider(Qt.Orientation.Horizontal)
        self.webp_quality_slider.setRange(1, 100)
        self.webp_quality_slider.setValue(self.settings_manager.settings.webp_quality)
        self.webp_quality_label = QLabel(f"{self.translations['quality']}: {self.settings_manager.settings.webp_quality}%")
        self.webp_quality_slider.valueChanged.connect(lambda v: self.webp_quality_label.setText(f"{self.translations['quality']}: {v}%"))
        webp_layout.addWidget(self.webp_quality_label)
        webp_layout.addWidget(self.webp_quality_slider)
        self.webp_group.setLayout(webp_layout)
        quality_layout.addWidget(self.webp_group)

        # PNG Compression
        self.png_group = QGroupBox(self.translations['png_compression'])
        png_layout = QVBoxLayout()
        self.png_compression_slider = QSlider(Qt.Orientation.Horizontal)
        self.png_compression_slider.setRange(0, 9)
        self.png_compression_slider.setValue(self.settings_manager.settings.png_compression)
        self.png_compression_label = QLabel(f"{self.translations['png_compression']}: {self.settings_manager.settings.png_compression}")
        self.png_compression_slider.valueChanged.connect(lambda v: self.png_compression_label.setText(f"{self.translations['png_compression']}: {v}"))
        png_layout.addWidget(self.png_compression_label)
        png_layout.addWidget(self.png_compression_slider)
        self.png_group.setLayout(png_layout)
        quality_layout.addWidget(self.png_group)

        self.quality_tab.setLayout(quality_layout)
        icon = QIcon(resource_path("assets/calidad.png"))
        if icon.isNull():
            print("Error: No se pudo cargar el icono calidad.png para la pestaña Calidad")
        self.tabs.addTab(self.quality_tab, icon, self.translations['quality_tab_name'])

        layout.addWidget(self.tabs)

        # Botones
        buttons_layout = QHBoxLayout()
        self.save_button = QPushButton(self.translations['save'])
        self.save_button.clicked.connect(self.save_settings)
        self.cancel_button = QPushButton(self.translations['cancel'])
        self.cancel_button.clicked.connect(self.reject)
        self.reset_button = QPushButton(self.translations['reset'])
        self.reset_button.clicked.connect(self.reset_settings)
        buttons_layout.addWidget(self.save_button)
        buttons_layout.addWidget(self.cancel_button)
        buttons_layout.addWidget(self.reset_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def select_output_dir(self):
        """Seleccionar directorio de salida"""
        directory = QFileDialog.getExistingDirectory(self, self.translations['select_output_dir_dialog'])
        if directory:
            self.output_dir_label.setText(directory)

    def save_settings(self):
        """Guardar configuraciones"""
        new_language_code = self.lang_combo.currentData()
        language_changed = (new_language_code != self.original_language)

        self.settings_manager.set_setting('language', new_language_code)
        self.settings_manager.set_setting('use_threading', self.threading_radio.isChecked())
        self.settings_manager.set_setting('max_threads', self.threads_spin.value())
        output_dir = self.output_dir_label.text()
        if output_dir != self.translations['same_as_original_dir']:
            self.settings_manager.set_setting('default_output_dir', output_dir)
        else:
            self.settings_manager.set_setting('default_output_dir', "")
        self.settings_manager.set_setting('keep_original_files', self.keep_original_check.isChecked())
        self.settings_manager.set_setting('show_notifications', self.show_notifications_check.isChecked())
        self.settings_manager.set_setting('enable_drag_drop', self.drag_drop_check.isChecked())
        self.settings_manager.set_setting('jpg_quality', self.jpg_quality_slider.value())
        self.settings_manager.set_setting('webp_quality', self.webp_quality_slider.value())
        self.settings_manager.set_setting('png_compression', self.png_compression_slider.value())

        if language_changed:
            self.translations = self.settings_manager.get_translations()
            self.update_ui_text()
            QMessageBox.information(self, self.translations['settings'],
                                    self.translations['language_change_restart_info'])
        self.accept()

    def reset_settings(self):
        """Restablecer configuraciones a valores por defecto"""
        reply = QMessageBox.question(self, self.translations['reset'],
                                   self.translations['reset_settings_confirm'],
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.settings_manager.reset_to_defaults()
            self.translations = self.settings_manager.get_translations()
            self.update_ui_text()
            QMessageBox.information(self, self.translations['settings'],
                                    self.translations['language_change_restart_info'])
            self.reject()

    def update_ui_text(self):
        """Actualiza todos los textos de la interfaz del diálogo de configuraciones."""
        self.setWindowTitle(self.translations['settings'])
        self.tabs.setTabText(self.tabs.indexOf(self.general_tab), self.translations['general_tab_name'])
        icon = QIcon(resource_path("assets/configuracion.png"))
        if icon.isNull():
            print("Error: No se pudo cargar el icono configuracion.png para la pestaña General (update_ui_text)")
        self.tabs.setTabIcon(self.tabs.indexOf(self.general_tab), icon)
        self.tabs.setTabText(self.tabs.indexOf(self.quality_tab), self.translations['quality_tab_name'])
        icon = QIcon(resource_path("assets/calidad.png"))
        if icon.isNull():
            print("Error: No se pudo cargar el icono calidad.png para la pestaña Calidad (update_ui_text)")
        self.tabs.setTabIcon(self.tabs.indexOf(self.quality_tab), icon)

        self.lang_group.setTitle(self.translations['language'])
        self.lang_combo.setItemText(0, self.translations['language_es'])
        self.lang_combo.setItemText(1, self.translations['language_en'])

        self.proc_group.setTitle(self.translations['processing_mode'])
        self.threading_radio.setText(self.translations['concurrent'])
        self.sequential_radio.setText(self.translations['sequential'])
        self.threads_label.setText(self.translations['threads_max'])

        self.output_group.setTitle(self.translations['output_directory'])
        if self.output_dir_label.text() == self.settings_manager.get_translations(self.original_language).get('same_as_original_dir', 'Same as original directory'):
            self.output_dir_label.setText(self.translations['same_as_original_dir'])
        self.output_dir_button.setText(self.translations['select_output_dir_dialog'])

        self.options_group.setTitle(self.translations['options'])
        self.keep_original_check.setText(self.translations['maintain_original_files'])
        self.show_notifications_check.setText(self.translations['show_notifications'])
        self.drag_drop_check.setText(self.translations['enable_drag_drop'])

        self.jpg_group.setTitle("JPG " + self.translations['quality'])
        self.jpg_quality_label.setText(f"{self.translations['quality']}: {self.settings_manager.settings.jpg_quality}%")

        self.webp_group.setTitle("WebP " + self.translations['quality'])
        self.webp_quality_label.setText(f"{self.translations['quality']}: {self.settings_manager.settings.webp_quality}%")

        self.png_group.setTitle(self.translations['png_compression'])
        self.png_compression_label.setText(f"{self.translations['png_compression']}: {self.settings_manager.settings.png_compression}")

        self.save_button.setText(self.translations['save'])
        self.cancel_button.setText(self.translations['cancel'])
        self.reset_button.setText(self.translations['reset'])

        self.original_language = self.settings_manager.settings.language

class HistoryDialog(QDialog):
    """Diálogo de historial de conversiones"""

    def __init__(self, converter, settings_manager, parent=None):
        super().__init__(parent)
        self.converter = converter
        self.settings_manager = settings_manager
        self.translations = settings_manager.get_translations()
        self.init_ui()
        self.apply_theme()

    def apply_theme(self):
        """Aplicar tema oscuro al diálogo"""
        dark_style = """
        QDialog {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QLabel {
            color: #FFFFFF;
            background-color: transparent;
        }
        QPushButton {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: 1px solid #666666;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #5A5A5A;
        }
        QPushButton:pressed {
            background-color: #3A3A3A;
        }
        QListWidget {
            background-color: #3A3A3A;
            color: #CCCCCC;
            border: 1px solid #555555;
            border-radius: 4px;
        }
        QListWidget::item {
            padding: 5px;
        }
        QListWidget::item:selected {
            background-color: #4CAF50;
            color: #FFFFFF;
        }
        """
        self.setStyleSheet(dark_style)

    def init_ui(self):
        self.setWindowTitle(self.translations['history_title'])
        icon = QIcon(resource_path("assets/historial.png"))
        if icon.isNull():
            print("Error: No se pudo cargar el icono historial.png para la ventana de historial")
        self.setWindowIcon(icon)
        self.setFixedSize(600, 400)

        layout = QVBoxLayout()

        # Lista de historial
        self.history_list = QListWidget()
        self.load_history()

        layout.addWidget(self.history_list)

        # Botones
        buttons_layout = QHBoxLayout()

        self.clear_button = QPushButton(self.translations['clear_history'])
        self.clear_button.clicked.connect(self.clear_history)

        self.close_button = QPushButton(self.translations['close'])
        self.close_button.clicked.connect(self.close)

        buttons_layout.addWidget(self.clear_button)
        buttons_layout.addWidget(self.close_button)

        layout.addLayout(buttons_layout)
        self.setLayout(layout)

    def load_history(self):
        """Cargar historial en la lista"""
        self.history_list.clear()

        for entry in reversed(self.converter.history):
            timestamp = datetime.fromisoformat(entry['timestamp']).strftime("%Y-%m-%d %H:%M:%S")
            status = "✓" if entry['success'] else "✗"

            item_text = f"{status} {timestamp} - {entry['input_file']} → {entry['output_file']} ({entry['input_format']} → {entry['output_format']})"

            item = QListWidgetItem(item_text)
            if entry['success']:
                item.setForeground(QColor("#4CAF50"))
            else:
                item.setForeground(QColor("#F44336"))

            self.history_list.addItem(item)

    def clear_history(self):
        """Limpiar historial"""
        reply = QMessageBox.question(self, self.translations['clear_history'],
                                   self.translations['clear_history_confirm'],
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.converter.history.clear()
            self.converter.save_history()
            self.load_history()

class DragDropLabel(QLabel):
    """Label que acepta drag and drop"""

    filesDropped = pyqtSignal(list)

    def __init__(self, text=""):
        super().__init__(text)
        self.setAcceptDrops(True)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #666;
                border-radius: 8px;
                padding: 20px;
                background-color: #3A3A3A;
                color: #CCCCCC;
                font-size: 14px;
            }
            QLabel:hover {
                border-color: #4CAF50;
                background-color: #404040;
            }
        """)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls() and self.parent().settings_manager.settings.enable_drag_drop:
            event.acceptProposedAction()
            self.setStyleSheet("""
                QLabel {
                    border: 2px dashed #4CAF50;
                    border-radius: 8px;
                    padding: 20px;
                    background-color: #404040;
                    color: #4CAF50;
                    font-size: 14px;
                }
            """)
        else:
            event.ignore()

    def dragLeaveEvent(self, event):
        self.setStyleSheet("""
            QLabel {
                border: 2px dashed #666;
                border-radius: 8px;
                padding: 20px;
                background-color: #3A3A3A;
                color: #CCCCCC;
                font-size: 14px;
            }
            QLabel:hover {
                border-color: #4CAF50;
                background-color: #404040;
            }
        """)

    def dropEvent(self, event):
        if self.parent().settings_manager.settings.enable_drag_drop:
            files = [url.toLocalFile() for url in event.mimeData().urls()]
            self.filesDropped.emit(files)
            self.dragLeaveEvent(event)
        else:
            event.ignore()

class ConverterWindow(QMainWindow):
    """Ventana principal mejorada"""

    def __init__(self):
        super().__init__()
        self.settings_manager = SettingsManager()
        self.converter = ImageConverter()
        self.translations = self.settings_manager.get_translations()
        self.current_files = []
        self.current_format = None
        self.conversion_thread = None
        self.init_ui()
        self.apply_theme()

    def init_ui(self):
        self.setWindowTitle(self.translations['app_title'])
        self.setFixedSize(450, 500)
        self._set_window_icon()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        header_layout = QHBoxLayout()
        self.settings_button = QPushButton("⚙")
        self.settings_button.setFixedSize(30, 30)
        self.settings_button.setToolTip(self.translations['settings'])
        self.settings_button.clicked.connect(self.open_settings)
        self.history_button = QPushButton("📋")
        self.history_button.setFixedSize(30, 30)
        self.history_button.setToolTip(self.translations['history'])
        self.history_button.clicked.connect(self.open_history)
        header_layout.addStretch()
        header_layout.addWidget(self.settings_button)
        header_layout.addWidget(self.history_button)
        self.layout.addLayout(header_layout)

        format_layout = QVBoxLayout()
        self.format_label = QLabel(self.translations['select_conversion'])
        self.format_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        format_layout.addWidget(self.format_label)
        input_layout = QHBoxLayout()
        self.from_label = QLabel(self.translations['from'])
        input_layout.addWidget(self.from_label)
        self.input_format_combo = QComboBox()
        self.input_format_combo.addItems(list(self.converter.SUPPORTED_FORMATS.keys()))
        input_layout.addWidget(self.input_format_combo)
        format_layout.addLayout(input_layout)
        output_layout = QHBoxLayout()
        self.to_label = QLabel(self.translations['to'])
        output_layout.addWidget(self.to_label)
        self.output_format_combo = QComboBox()
        self.output_format_combo.addItems(list(self.converter.SUPPORTED_FORMATS.keys()))
        output_layout.addWidget(self.output_format_combo)
        format_layout.addLayout(output_layout)
        self.layout.addLayout(format_layout)

        self.drop_label = DragDropLabel(self.translations['drag_drop_files'] + "\n" + self.translations['or_click_to_select'])
        self.drop_label.setFixedHeight(150)
        self.drop_label.filesDropped.connect(self.handle_dropped_files)
        self.drop_label.mousePressEvent = self.select_files
        self.layout.addWidget(self.drop_label)

        self.preview_label = QLabel()
        self.preview_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_label.setFixedHeight(200)
        self.preview_label.setStyleSheet("border: 1px solid #666; background-color: #3A3A3A;")
        self.preview_label.hide()
        self.layout.addWidget(self.preview_label)

        self.file_info_label = QLabel("")
        self.file_info_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_info_label.hide()
        self.layout.addWidget(self.file_info_label)

        self.convert_button = QPushButton(self.translations['convert'])
        self.convert_button.setFixedHeight(40)
        self.convert_button.clicked.connect(self.start_conversion)
        self.convert_button.hide()
        self.layout.addWidget(self.convert_button)

        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.hide()
        self.layout.addWidget(self.progress_bar)

        self.back_button = QPushButton(self.translations['back'])
        self.back_button.clicked.connect(self.reset_interface)
        self.back_button.hide()
        self.layout.addWidget(self.back_button)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.status_label)

        self.reset_timer = QTimer()
        self.reset_timer.timeout.connect(self.reset_interface)

    def _set_window_icon(self):
        """Método auxiliar para establecer el icono de la ventana."""
        icon_paths = [
            resource_path("app_icon.ico"),
            resource_path("assets/icon.png")
        ]
        for icon_path in icon_paths:
            if os.path.exists(icon_path):
                icon = QIcon(icon_path)
                if not icon.isNull():
                    self.setWindowIcon(icon)
                    print(f"Icono de ventana cargado: {icon_path}")
                    return
                else:
                    print(f"Error: No se pudo cargar el icono de ventana: {icon_path}")

    def apply_theme(self):
        """Aplicar tema oscuro"""
        dark_style = """
        QMainWindow {
            background-color: #2E2E2E;
            color: #FFFFFF;
        }
        QLabel {
            color: #FFFFFF;
            background-color: transparent;
        }
        QPushButton {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: 1px solid #666666;
            padding: 8px 16px;
            border-radius: 6px;
            font-size: 12px;
        }
        QPushButton:hover {
            background-color: #5A5A5A;
        }
        QPushButton:pressed {
            background-color: #3A3A3A;
        }
        QComboBox {
            background-color: #4A4A4A;
            color: #FFFFFF;
            border: 1px solid #666666;
            padding: 5px;
            border-radius: 4px;
        }
        QComboBox::drop-down {
            border: none;
        }
        QComboBox::down-arrow {
            image: none;
            border-left: 5px solid transparent;
            border-right: 5px solid transparent;
            border-top: 5px solid #FFFFFF;
        }
        QProgressBar {
            border: 1px solid #666666;
            border-radius: 4px;
            text-align: center;
            color: #FFFFFF;
            background-color: #3A3A3A;
        }
        QProgressBar::chunk {
            background-color: #4CAF50;
            border-radius: 3px;
        }
        """
        self.setStyleSheet(dark_style)

    def select_files(self, event):
        """Seleccionar archivos manualmente"""
        if not self.settings_manager.settings.enable_drag_drop:
            return
        input_format = self.input_format_combo.currentText()
        extensions = self.converter.SUPPORTED_FORMATS.get(input_format.upper(), [])
        filter_text = f"{input_format} Files (*.{' *.'.join(extensions)})"
        files, _ = QFileDialog.getOpenFileNames(
            self, f"{self.translations['select_file']} {input_format}", "", filter_text
        )
        if files:
            self.handle_dropped_files(files)

    def handle_dropped_files(self, files):
        """Manejar archivos arrastrados o seleccionados"""
        valid_files = []
        input_format = self.input_format_combo.currentText()
        valid_extensions = self.converter.SUPPORTED_FORMATS.get(input_format.upper(), [])
        for file in files:
            ext = os.path.splitext(file)[1].lower()[1:]
            if ext in valid_extensions:
                valid_files.append(file)
        if not valid_files:
            self.status_label.setText(self.translations['no_valid_files'])
            self.status_label.setStyleSheet("color: #F44336;")
            return
        self.current_files = valid_files
        self.show_file_info()
        self.show_conversion_interface()

    def show_file_info(self):
        """Mostrar información del archivo seleccionado"""
        if len(self.current_files) == 1:
            file_path = self.current_files[0]
            file_name = os.path.basename(file_path)
            file_size = os.path.getsize(file_path)
            file_size_mb = file_size / (1024 * 1024)
            self.file_info_label.setText(f"{self.translations['file']}: {file_name}\n{self.translations['size']}: {file_size_mb:.2f} MB")
            try:
                img = Image.open(file_path)
                if img.mode not in ('RGB', 'RGBA', 'L'):
                    img = img.convert('RGBA')
                elif img.mode == 'P':
                    if 'transparency' in img.info or img.format == 'GIF':
                        img = img.convert('RGBA')
                    else:
                        img = img.convert('RGB')
                elif img.mode == 'L':
                    img = img.convert('RGB')
                qim = ImageQt.ImageQt(img)
                pixmap = QPixmap.fromImage(qim)
                scaled_pixmap = pixmap.scaled(180, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
                self.preview_label.setPixmap(scaled_pixmap)
                self.preview_label.show()
            except Exception as e:
                print(f"Error al cargar la vista previa de la imagen: {e}")
                self.preview_label.hide()
        else:
            self.file_info_label.setText(f"{self.translations['selected_files']} {len(self.current_files)}")
            self.preview_label.hide()
        self.file_info_label.show()

    def show_conversion_interface(self):
        """Mostrar interfaz de conversión"""
        self.drop_label.hide()
        self.convert_button.show()
        self.back_button.show()
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: #FFFFFF;")

    def start_conversion(self):
        """Iniciar conversión"""
        if not self.current_files:
            return
        self.convert_button.hide()
        self.progress_bar.show()
        self.progress_bar.setValue(0)
        output_format = self.output_format_combo.currentText()
        quality_settings = self.settings_manager.get_quality_settings(output_format)
        default_output_dir = self.settings_manager.settings.default_output_dir
        self.conversion_thread = ConversionThread(
            self.converter,
            self.current_files,
            output_format,
            quality_settings,
            default_output_dir
        )
        self.conversion_thread.finished.connect(self.conversion_finished)
        self.conversion_thread.progress.connect(self.progress_bar.setValue)
        self.conversion_thread.start()

    def conversion_finished(self, success, message):
        """Manejar finalización de conversión"""
        self.progress_bar.hide()
        self.status_label.setText(message)
        if success:
            self.status_label.setStyleSheet("color: #4CAF50;")
            self.reset_timer.start(3000)
        else:
            self.status_label.setStyleSheet("color: #F44336;")
            self.convert_button.show()

    def reset_interface(self):
        """Resetear interfaz para nueva conversión"""
        if self.conversion_thread and self.conversion_thread.isRunning():
            self.conversion_thread.requestInterruption()
            self.conversion_thread.wait(5000)
            if self.conversion_thread.isRunning():
                print("Advertencia: El hilo de conversión no terminó limpiamente.")
        self.current_files = []
        self.drop_label.show()
        self.preview_label.hide()
        self.file_info_label.hide()
        self.convert_button.hide()
        self.back_button.hide()
        self.progress_bar.hide()
        self.status_label.setText("")
        self.status_label.setStyleSheet("color: #FFFFFF;")
        self.reset_timer.stop()

    def open_settings(self):
        """Abrir diálogo de configuraciones"""
        dialog = SettingsDialog(self.settings_manager, self)
        original_ui_language = self.settings_manager.settings.language
        if dialog.exec() == QDialog.DialogCode.Accepted:
            new_translations = self.settings_manager.get_translations()
            if new_translations != self.translations:
                self.translations = new_translations
                self.update_ui_text()
                if self.settings_manager.settings.language != original_ui_language:
                    QMessageBox.information(self, self.translations['settings'],
                                            self.translations['language_change_restart_info'])

    def open_history(self):
        """Abrir diálogo de historial"""
        dialog = HistoryDialog(self.converter, self.settings_manager, self)
        dialog.exec()

    def update_ui_text(self):
        """Actualizar textos de la interfaz y el icono de la ventana"""
        try:
            app_instance = QApplication.instance()
            if app_instance:
                app_instance.setApplicationName(self.translations['app_title'])
            self.setWindowTitle(self.translations['app_title'])
            self.convert_button.setText(self.translations['convert'])
            self.settings_button.setToolTip(self.translations['settings'])
            self.history_button.setToolTip(self.translations['history'])
            self.format_label.setText(self.translations['select_conversion'])
            self.drop_label.setText(self.translations['drag_drop_files'] + "\n" + self.translations['or_click_to_select'])
            self.back_button.setText(self.translations['back'])
            if hasattr(self, 'from_label') and self.from_label is not None:
                self.from_label.setText(self.translations['from'])
            if hasattr(self, 'to_label') and self.to_label is not None:
                self.to_label.setText(self.translations['to'])
            self._set_window_icon()
            if self.file_info_label.isVisible():
                self.show_file_info()
        except Exception as e:
            print(f"Error al actualizar los textos de la UI o el icono: {e}")