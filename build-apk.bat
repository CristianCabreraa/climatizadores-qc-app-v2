@echo off
echo ====================================================================
echo  COMPILADOR AUTOMATICO DE APK ANDROID - GREENAIR QC v1
echo ====================================================================
echo.
echo 1. Sincronizando archivos web con el proyecto nativo de Android...

xcopy /E /Y /I "css" "android\app\src\main\assets\public\css" >nul
xcopy /E /Y /I "js" "android\app\src\main\assets\public\js" >nul
xcopy /E /Y /I "assets" "android\app\src\main\assets\public\assets" >nul
copy /Y "index.html" "android\app\src\main\assets\public\" >nul
copy /Y "manifest.json" "android\app\src\main\assets\public\" >nul
copy /Y "sw.js" "android\app\src\main\assets\public\" >nul

echo [OK] Archivos sincronizados en android\app\src\main\assets\public.
echo.

cd android
if exist gradlew.bat (
    echo 2. Compilando APK con Gradle Wrapper...
    call gradlew.bat assembleDebug
) else (
    where gradle >nul 2>&1
    if %errorlevel% equ 0 (
        echo 2. Compilando APK con Gradle del sistema...
        call gradle assembleDebug
    ) else (
        echo [INFO] No se encontro Gradle instalado en el PATH.
        echo Para compilar el APK:
        echo   - Abre la carpeta 'android' en Android Studio y selecciona:
        echo     Build ^> Build Bundle(s) / APK(s) ^> Build APK(s)
        echo   - O sube el repositorio a GitHub para que GitHub Actions compile el APK v1 automaticamente.
        pause
        exit /b 0
    )
)

if exist "app\build\outputs\apk\debug\app-debug.apk" (
    copy /Y "app\build\outputs\apk\debug\app-debug.apk" "..\GreenAir-QC-v1.apk" >nul
    echo.
    echo ====================================================================
    echo  [EXITO] APK v1 generado con exito: GreenAir-QC-v1.apk
    echo ====================================================================
    echo Ubicacion: %~dp0GreenAir-QC-v1.apk
)

pause
