@echo off
set "JAVA_HOME=G:\software\simpa\jdk-17.0.21+9"
set "PATH=%JAVA_HOME%\bin;G:\software\simpa\androidsdk\platform-tools;%PATH%"
set "ANDROID_HOME=G:\software\simpa\androidsdk"

echo ====================================================================
echo VYAS ASTRA - Android APK Build
echo ====================================================================
echo JAVA_HOME: %JAVA_HOME%
echo ANDROID_HOME: %ANDROID_HOME%
echo.

cd /d "G:\software\simpa\VYAS\android_app"

echo Building APK with Gradle...
call gradle assembleDebug

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ====================================================================
    echo [SUCCESS] APK built successfully!
    echo ====================================================================
) else (
    echo.
    echo [ERROR] Build failed with exit code %ERRORLEVEL%
)

