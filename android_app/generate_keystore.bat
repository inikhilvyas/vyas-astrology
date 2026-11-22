@echo off
echo ====================================================================
echo VYAS ASTRA - Production Release Keystore Generator (Google Play Store)
echo ====================================================================
echo.

set KEYSTORE_NAME=vyas_astra_release.keystore
set ALIAS=vyasastra
set VALIDITY_DAYS=10000

if exist "%KEYSTORE_NAME%" (
    echo [INFO] Keystore %KEYSTORE_NAME% already exists. Skipping creation.
    goto end
)

echo Generating 2048-bit RSA Release Keystore...
keytool -genkey -v -keystore "%KEYSTORE_NAME%" -alias "%ALIAS%" -keyalg RSA -keysize 2048 -validity %VALIDITY_DAYS% -storepass vyasastro2026 -keypass vyasastro2026 -dname "CN=VYAS ASTRA, OU=Vedic Research, O=VYAS ASTRA FOUNDATION, L=Jaipur, ST=Rajasthan, C=IN"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo [SUCCESS] Release Keystore created: %KEYSTORE_NAME%
    echo Alias: %ALIAS%
    echo Validity: %VALIDITY_DAYS% days (until year 2053)
    echo Keystore Password: vyasastro2026
    echo Key Password: vyasastro2026
    echo.
    echo IMPORTANT: Keep this keystore safe! Never lose it, or you cannot update the app on Google Play Store!
) else (
    echo [ERROR] Failed to generate keystore. Ensure Java keytool is in your PATH.
)

:end
echo.
pause
