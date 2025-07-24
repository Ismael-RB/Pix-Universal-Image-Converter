# Pix - Universal Image Converter

A modern and efficient cross-platform application for converting images between multiple formats with an intuitive graphical interface and professional dark theme.

## Features

- **Multi-format Support**: JPG, PNG, WebP, BMP, TIFF, GIF, ICO, HEIC
- **Modern Interface**: Professional dark theme with intuitive design
- **Drag & Drop**: Direct file import with visual feedback
- **Batch Processing**: Convert multiple files simultaneously with threading support
- **Image Preview**: Preview images before conversion
- **Quality Control**: Advanced compression and quality settings
- **Conversion History**: Complete log of all conversion operations
- **Internationalization**: Support for Spanish and English
- **Cross-platform**: Windows, Linux, and macOS compatibility

## System Requirements

**Minimum Requirements:**
- Windows 7+ / Linux (modern distributions) / macOS 10.14+
- 512 MB RAM
- 100 MB free disk space
- Display resolution: 1024x768 or higher

**Recommended:**
- 1 GB RAM for large batch operations
- SSD storage for optimal performance

## Installation

### Option 1: Pre-compiled Executable

$$ **Recommended for end users** $$

1. Download the latest release from the releases section
2. **Windows**: Run `Pix.exe`
3. **Linux**: Execute `./Pix` (ensure executable permissions)
4. **macOS**: Open `Pix.app`

### Option 2: Source Installation

$$ **Recommended for developers or customization** $$

**Prerequisites:**
- Python 3.8 or higher
- pip package manager

**Installation Steps:**
```bash
# Clone repository
git clone https://github.com/username/pix-converter.git
cd pix-converter

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run application
python main.py
```

## Building Executable

To create a standalone executable:

### Windows
```batch
build.bat
```

### Linux/macOS
```bash
chmod +x build.sh
./build.sh
```

The executable will be generated in the `dist/` directory.

## Usage

### Basic Workflow

1. **Select Input Format**: Choose the format of your source files
2. **Select Output Format**: Choose the desired conversion format
3. **Add Files**: 
   - Drag files directly into the application window
   - Click the drop zone to open file selection dialog
4. **Configure Settings**: Access advanced options through the settings panel
5. **Convert**: Execute the conversion process

### Advanced Configuration

#### General Settings
- **Language**: Interface language selection (Spanish/English)
- **Processing Mode**: 
  - Concurrent: Multi-threaded processing for faster batch operations
  - Sequential: Single-threaded processing for system resource conservation
- **Output Directory**: Custom destination folder for converted files
- **File Management**: Options for handling original files

#### Quality Settings
- **JPEG Quality**: Compression level control (1-100%)
- **WebP Quality**: Compression optimization (1-100%)
- **PNG Compression**: Compression level adjustment (0-9)

### Conversion History

The application maintains a comprehensive log of all conversion operations, including:
- Timestamp and file information
- Conversion success status
- Input/output format details
- File size information

## Supported Formats

| Format | Input | Output | Features |
|--------|-------|--------|----------|
| JPEG/JPG | ✓ | ✓ | Quality control, optimization |
| PNG | ✓ | ✓ | Transparency support, compression levels |
| WebP | ✓ | ✓ | Modern format, excellent compression |
| BMP | ✓ | ✓ | Uncompressed bitmap format |
| TIFF | ✓ | ✓ | Professional format with LZW compression |
| GIF | ✓ | ✓ | Animation support |
| ICO | ✓ | ✓ | Multi-size icon format |
| HEIC | ✓ | ✓ | Apple format (requires pillow-heif) |

$$ **Note**: HEIC support requires additional pillow-heif installation for full functionality $$

## Technical Architecture

### Core Technologies
- **Python 3.8+**: Primary development language
- **PyQt6**: Cross-platform GUI framework
- **Pillow (PIL)**: Image processing library
- **PyInstaller**: Executable packaging

### Project Structure
```
pix-converter/
├── main.py                 # Application entry point
├── ui.py                   # User interface implementation
├── converter.py            # Image conversion engine
├── settings_manager.py     # Configuration management
├── requirements.txt        # Python dependencies
├── build.bat              # Windows build script
├── build.sh               # Unix build script
├── assets/                # Application resources
│   ├── icon.png
│   ├── configuracion.png
│   ├── historial.png
│   └── calidad.png
├── settings.json          # User configuration storage
└── conversion_history.json # Conversion history data
```

### Key Components

**ImageConverter Class**: Core conversion engine with support for:
- Multi-threaded batch processing
- Format-specific optimization
- Progress tracking and error handling
- Conversion history management

**SettingsManager Class**: Configuration system providing:
- Persistent settings storage
- Quality profile management
- Internationalization support
- Default value handling

**User Interface**: Modern Qt6-based interface featuring:
- Responsive drag-and-drop functionality
- Real-time preview capabilities
- Progress indication and status reporting
- Tabbed configuration panels

## Development

### Contributing

Contributions are welcome. Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/enhancement-name`)
3. Implement changes with appropriate testing
4. Commit with descriptive messages (`git commit -m 'Add feature: description'`)
5. Push to branch (`git push origin feature/enhancement-name`)
6. Submit a pull request

### Development Areas

$$ **High Priority**: Performance optimization, additional format support $$
$$ **Medium Priority**: UI/UX improvements, accessibility features $$
$$ **Low Priority**: Additional language translations, theme customization $$

### Code Standards
- Follow PEP 8 Python style guidelines
- Include docstrings for all public methods
- Implement proper error handling and logging
- Maintain backward compatibility where possible

## Troubleshooting

### Common Issues

**Application won't start:**
- Verify Python version compatibility (3.8+)
- Check all dependencies are installed
- Ensure sufficient system permissions

**Conversion failures:**
- Verify input file integrity
- Check available disk space
- Confirm format compatibility

**Performance issues:**
- Adjust thread count in settings
- Monitor system resource usage
- Consider sequential processing for large files

### Reporting Issues

When reporting bugs, please include:
- Detailed problem description
- Steps to reproduce the issue
- Operating system and version
- Application version and installation method
- Relevant error messages or logs

## Contributors

This project is developed and maintained by:

- **Ismael** ([@Ismael-RB](https://github.com/Ismael-RB)) - Project Creator & Core Developer
- **Alvaro** ([@AlvaroAR100](https://github.com/AlvaroAR100)) - Core Developer  
- **Alan** ([@Alancius98](https://github.com/Alancius98)) - Core Developer

All contributors have equal involvement in the development and decision-making process of this project.

## License

This project is licensed under the MIT License. See the LICENSE file for complete terms and conditions.

## Changelog

### Version 2.0
- Complete interface redesign with modern dark theme
- Multi-language support implementation
- Enhanced batch processing capabilities
- Advanced configuration system
- Comprehensive conversion history tracking
- Cross-platform compatibility improvements

### Version 1.0
- Initial release
- Basic JPG to PNG conversion functionality
- Simple user interface

## Support

For technical support, feature requests, or general inquiries:

- **Issues**: Use the GitHub issue tracker for bug reports and feature requests
- **Documentation**: Refer to this README and inline code documentation
- **Community**: Participate in discussions through GitHub Discussions

---

**Pix Universal Image Converter** - Professional image conversion made simple.
