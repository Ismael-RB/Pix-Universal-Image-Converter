@echo off
title Pix - Build Script
color 0A
echo ==================================================
echo                 Pix - Build
echo ==================================================
echo.

echo [1/3] Limpiando builds anteriores...
if exist "dist" rmdir /s /q "dist"
if exist "build" rmdir /s /q "build"
if exist "*.spec" del /q "*.spec"
echo ✓ Limpieza completada
echo.

echo [2/3] Creando ejecutable con PyInstaller...
REM --noconfirm: Sobrescribe archivos existentes sin pedir confirmacion.
REM --onefile: Empaqueta todo en un solo archivo ejecutable.
REM --windowed: Crea una aplicacion de GUI que no muestra la ventana de la consola.
REM --icon: Especifica el icono para el ejecutable.
REM --name: Establece el nombre del ejecutable.
REM --add-data "origen;destino": Incluye archivos/carpetas adicionales.
REM --hidden-import: Incluye módulos que PyInstaller podría no detectar automáticamente.
REM --debug=all: Para depuración, muestra más información si falla. (Quitar para la versión final)
pyinstaller --noconfirm --onefile --windowed ^
            --icon="assets/icon.png" ^
            --name="Pix" ^
            --add-data="assets;assets" ^
            --add-data="settings.json;." ^
            --add-data="conversion_history.json;." ^
            --hidden-import="PyQt6.QtWebEngineWidgets" ^
            --hidden-import="PyQt6.QtPrintSupport" ^
            --hidden-import="PIL._tkinter_finder" ^
            main.py

IF %ERRORLEVEL% NEQ 0 (
    echo.
    echo ERROR: Falló la creación del ejecutable.
    echo.
    echo Revisa los mensajes anteriores para mas detalles.
    echo.
    PAUSE
    EXIT /B %errorlevel%
)

echo ✓ Ejecutable creado exitosamente
echo.

echo [3/3] Verificando y finalizando...
if exist "dist\Pix.exe" (
    echo ===============================================
    echo               ¡BUILD EXITOSO!
    echo ===============================================
    echo.
    echo El ejecutable se encuentra en: dist\Pix.exe
    explorer dist
) else (
    echo ERROR: No se pudo crear el ejecutable
    echo Por favor, revisa si hay errores en la salida de PyInstaller.
)

pause
