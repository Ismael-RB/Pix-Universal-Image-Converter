# Pix - Image Converter

Pix is a powerful and intuitive image converter application built with Python and PyQt6. [cite\_start]It allows users to convert images between various popular formats with ease, offering both single-file and batch conversion capabilities. [cite: 1] [cite\_start]The application also includes customizable quality settings for output formats, a conversion history, and drag-and-drop functionality for a seamless user experience. [cite: 1]

## Features

  * [cite\_start]**Multi-Format Support**: Convert images to and from a wide range of formats, including JPG, PNG, WEBP, BMP, TIFF, GIF, ICO, and HEIC (HEIC requires `pillow-heif`). [cite: 1]
  * [cite\_start]**Single and Batch Conversion**: Convert individual image files or process multiple images simultaneously. [cite: 1]
  * [cite\_start]**Customizable Quality Settings**: Adjust quality parameters for output formats like JPG, WebP, and PNG compression levels. [cite: 1]
  * [cite\_start]**Conversion History**: Keep a record of all your past conversions for easy tracking. [cite: 1]
  * [cite\_start]**Drag-and-Drop Interface**: Easily add files for conversion by dragging and dropping them into the application window. [cite: 1]
  * [cite\_start]**Configurable Settings**: Customize various application settings, including language, processing mode (concurrent or sequential), default output directory, and notification preferences. [cite: 1]
  * [cite\_start]**Dark Theme**: The application features a dark theme for a comfortable viewing experience. [cite: 1]

## Supported Formats

[cite\_start]Pix supports conversion for the following image formats: [cite: 1]

  * [cite\_start]JPG (JPEG) [cite: 1]
  * [cite\_start]PNG [cite: 1]
  * [cite\_start]WEBP [cite: 1]
  * [cite\_start]BMP [cite: 1]
  * [cite\_start]TIFF (TIF) [cite: 1]
  * [cite\_start]GIF [cite: 1]
  * [cite\_start]ICO [cite: 1]
  * [cite\_start]HEIC (HEIF) [cite: 1]

## Installation

To run Pix, you need to have Python installed. It's recommended to use a virtual environment.

1.  **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/pix.git
    cd pix
    ```

2.  **Create a virtual environment** (optional but recommended):

    ```bash
    python -m venv venv
    .\venv\Scripts\activate   # On Windows
    source venv/bin/activate # On macOS/Linux
    ```

3.  **Install dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

    (Note: A `requirements.txt` file is assumed to exist with `Pillow` and `PyQt6` listed.)

## Usage

To start the Pix application, run the `main.py` file:

```bash
python main.py
```

### Converting Images

1.  [cite\_start]**Select Input and Output Formats**: Choose the desired input and output image formats from the dropdown menus. [cite: 1]
2.  [cite\_start]**Add Files**: Drag and drop your image files onto the designated area, or click the area to browse and select files. [cite: 1]
3.  [cite\_start]**Convert**: Click the "Convert" button to start the conversion process. [cite: 1]
4.  [cite\_start]**Output**: Converted images will be saved to the specified output directory (default is the original directory). [cite: 1]

### Settings

Access the settings dialog by clicking the "⚙" button. [cite\_start]Here you can configure: [cite: 1]

  * [cite\_start]**Language**: Change the application's language. [cite: 1]
  * [cite\_start]**Processing Mode**: Choose between concurrent (threaded) or sequential processing for conversions. [cite: 1]
  * [cite\_start]**Output Directory**: Set a default directory for saving converted images. [cite: 1]
  * [cite\_start]**Quality Settings**: Adjust quality for JPG, WebP, and compression level for PNG. [cite: 1]
  * [cite\_start]**Other Options**: Enable/disable drag-and-drop, show notifications, and choose to keep original files. [cite: 1]

### Conversion History

View a list of your past conversions by clicking the "📋" button. [cite\_start]You can also clear the history from this dialog. [cite: 1]

## Building an Executable

You can create a standalone executable for Pix using PyInstaller. A `build.bat` script is provided for Windows.

To build the executable:

1.  **Run the build script**:

    ```bash
    build.bat
    ```

    [cite\_start]This script will clean previous builds, then use PyInstaller to create a single-file, windowed executable named "Pix" with the appropriate assets and hidden imports. [cite: 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

2.  **Find the executable**:
    [cite\_start]The executable will be located in the `dist` directory. [cite: 20]

## Project Structure

  * [cite\_start]`main.py`: The entry point of the application. [cite: 3]
  * [cite\_start]`ui.py`: Contains the PyQt6 graphical user interface (GUI) elements and logic. [cite: 2]
  * [cite\_start]`converter.py`: Handles the core image conversion logic using the Pillow library. [cite: 1]
  * `settings_manager.py`: (Assumed) Manages application settings and translations.
  * [cite\_start]`assets/`: Directory for application icons and other resources. [cite: 17]
  * [cite\_start]`conversion_history.json`: Stores the history of image conversions. [cite: 18]
  * [cite\_start]`settings.json`: Stores user-configurable application settings. [cite: 17]
  * [cite\_start]`build.bat`: Script for building the executable using PyInstaller (Windows). [cite: 11]
