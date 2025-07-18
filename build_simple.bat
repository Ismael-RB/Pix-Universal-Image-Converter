@echo off
title Universal Image Converter - Build Script
color 0A
echo ==================================================
echo         Universal Image Converter - Build
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
pyinstaller --noconfirm --onefile --windowed ^
            --icon="assets/icon.png" ^
            --name="Universal Image Converter" ^
            --add-data="assets;assets" ^
            --add-data="settings.json;." ^
            --add-data="conversion_history.json;." ^
            main.py

if %errorlevel% neq 0 (
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
if exist "dist\Universal Image Converter.exe" (
    echo ===============================================
    echo               ¡BUILD EXITOSO!
    echo ===============================================
    echo.
    echo El ejecutable se encuentra en: dist\Universal Image Converter.exe
    explorer dist
) else (
    echo ERROR: No se pudo crear el ejecutable.
    echo Por favor, revisa si hay errores en la salida de PyInstaller.
)

pause