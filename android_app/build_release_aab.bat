@echo off
echo ====================================================================
echo VYAS ASTRA - Production AAB Build Script (Google Play Store Release)
echo ====================================================================
echo.

cd /d "%~dp0"

if not exist "vyas_astra_release.keystore" (
    echo [WARNING] Release keystore not found. Generating now...
    call generate_keystore.bat
)

echo.
echo Building Release Android App Bundle (.aab) with Gradle...
gradle bundleRelease

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================================
    echo [SUCCESS] Android App Bundle created successfully!
    echo Location: app\build\outputs\bundle\release\app-release.aab
    echo ====================================================================
    echo You can now upload this .aab file directly to Google Play Console!
) else (
    echo.
    echo [ERROR] Gradle build failed. Ensure Android SDK and JDK 17 are installed.
)

pause
