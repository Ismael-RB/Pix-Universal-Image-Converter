@echo off
title JPG to PNG Converter - Instalador
color 0B

echo ===============================================
echo    JPG to PNG Converter - Instalador
echo ===============================================
echo.

echo Este script instalará JPG to PNG Converter en tu sistema.
echo.
echo Requisitos:
echo - Windows 7 o superior
echo - 100 MB de espacio libre
echo.
echo ¿Deseas continuar? (S/N)
set /p choice=
if /i not "%choice%"=="S" (
    echo Instalación cancelada.
    pause
    exit /b 0
)

echo.
echo [1/4] Creando directorio de instalación...
set "INSTALL_DIR=%PROGRAMFILES%\JPG-to-PNG-Converter"
if not exist "%INSTALL_DIR%" (
    mkdir "%INSTALL_DIR%"
    if %errorlevel% neq 0 (
        echo ERROR: No se pudo crear el directorio de instalación
        echo Intenta ejecutar como administrador
        pause
        exit /b 1
    )
)
echo ✓ Directorio creado: %INSTALL_DIR%

echo.
echo [2/4] Copiando archivos...
copy "JPG-to-PNG-Converter.exe" "%INSTALL_DIR%\" >nul
if %errorlevel% neq 0 (
    echo ERROR: No se pudo copiar el ejecutable
    pause
    exit /b 1
)
echo ✓ Ejecutable copiado

echo.
echo [3/4] Creando acceso directo en el escritorio...
set "DESKTOP=%USERPROFILE%\Desktop"
echo Set oWS = WScript.CreateObject("WScript.Shell") > "%TEMP%\shortcut.vbs"
echo sLinkFile = "%DESKTOP%\JPG to PNG Converter.lnk" >> "%TEMP%\shortcut.vbs"
echo Set oLink = oWS.CreateShortcut(sLinkFile) >> "%TEMP%\shortcut.vbs"
echo oLink.TargetPath = "%INSTALL_DIR%\JPG-to-PNG-Converter.exe" >> "%TEMP%\shortcut.vbs"
echo oLink.WorkingDirectory = "%INSTALL_DIR%" >> "%TEMP%\shortcut.vbs"
echo oLink.Description = "Convertidor de imágenes JPG a PNG" >> "%TEMP%\shortcut.vbs"
echo oLink.Save >> "%TEMP%\shortcut.vbs"
cscript "%TEMP%\shortcut.vbs" >nul
del "%TEMP%\shortcut.vbs"
echo ✓ Acceso directo creado en el escritorio

echo.
echo [4/4] Registrando en el menú inicio...
set "START_MENU=%APPDATA%\Microsoft\Windows\Start Menu\Programs"
copy "%DESKTOP%\JPG to PNG Converter.lnk" "%START_MENU%\" >nul
echo ✓ Acceso directo agregado al menú inicio

echo.
echo ===============================================
echo            ¡INSTALACIÓN COMPLETADA!
echo ===============================================
echo.
echo JPG to PNG Converter ha sido instalado exitosamente.
echo.
echo Ubicación: %INSTALL_DIR%
echo.
echo Puedes ejecutarlo desde:
echo - Acceso directo en el escritorio
echo - Menú inicio
echo - Directamente desde: %INSTALL_DIR%\JPG-to-PNG-Converter.exe
echo.
echo ¿Deseas ejecutar la aplicación ahora? (S/N)
set /p choice=
if /i "%choice%"=="S" (
    start "" "%INSTALL_DIR%\JPG-to-PNG-Converter.exe"
)

pause