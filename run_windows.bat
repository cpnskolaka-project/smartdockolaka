@echo off
setlocal EnableExtensions EnableDelayedExpansion
chcp 65001 >nul

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%"

set "APP_NAME=SmartDoc Kolaka"
set "APP_URL=http://127.0.0.1:5050"
set "AUTOSTART_ARG=%~1"
set "IS_AUTOSTART=0"
if /I "%AUTOSTART_ARG%"=="--autostart" set "IS_AUTOSTART=1"
set "ACTION=start"

echo ==============================================
echo %APP_NAME% - Installer dan Local Runner
echo ==============================================

where python >nul 2>nul
if errorlevel 1 (
    echo [ERROR] Python tidak ditemukan di PATH.
    echo [INFO] Instal Python terlebih dahulu, lalu jalankan file ini lagi.
    pause
    exit /b 1
)

if "%IS_AUTOSTART%"=="0" call :choose_action
if /I "%ACTION%"=="exit" exit /b 0

if /I "%ACTION%"=="repair" (
    echo [INFO] Mode repair dipilih. Virtual environment lama akan dibuat ulang.
    if exist "venv" rmdir /s /q "venv"
)

if not exist "venv" (
    echo [INFO] Membuat virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Gagal membuat virtual environment.
        pause
        exit /b 1
    )
)

echo [INFO] Mengaktifkan virtual environment...
call venv\Scripts\activate.bat
if errorlevel 1 (
    echo [ERROR] Gagal mengaktifkan virtual environment.
    pause
    exit /b 1
)

set "MARKER=venv\.requirements_installed"
set "NEEDS_INSTALL=0"
set "REQ_HASH="

for /f "skip=1 delims=" %%H in ('certutil -hashfile requirements.txt MD5 ^| findstr /R /V /C:"hash of" /C:"CertUtil" /C:"^$"') do (
    if not defined REQ_HASH set "REQ_HASH=%%H"
)

if not exist "%MARKER%" (
    set "NEEDS_INSTALL=1"
) else (
    set /p INSTALLED_HASH=<"%MARKER%"
    if /I not "!INSTALLED_HASH!"=="!REQ_HASH!" set "NEEDS_INSTALL=1"
)

set "PIP_INSTALL_CMD=python -m pip install -r requirements.txt"
if "%NEEDS_INSTALL%"=="1" (
    echo [INFO] Instalasi awal atau perubahan dependency terdeteksi.
    echo [INFO] Komputer ini perlu terhubung ke internet untuk memasang dependency Python.
)

if /I "%ACTION%"=="reinstall" (
    set "NEEDS_INSTALL=1"
    set "PIP_INSTALL_CMD=python -m pip install --force-reinstall -r requirements.txt"
)

if /I "%ACTION%"=="install" set "NEEDS_INSTALL=1"
if /I "%ACTION%"=="repair" set "NEEDS_INSTALL=1"

if "%NEEDS_INSTALL%"=="1" (
    echo [INFO] Menginstal atau memperbarui dependency...
    call %PIP_INSTALL_CMD%
    if errorlevel 1 (
        echo [ERROR] Instalasi dependency gagal.
        echo [INFO] Pastikan koneksi internet tersedia saat instalasi pertama atau saat reinstall/repair.
        pause
        exit /b 1
    )
    > "%MARKER%" echo !REQ_HASH!
    echo [INFO] Dependency siap digunakan.
) else (
    echo [INFO] Dependency sudah sesuai. Lewati instalasi.
)

if "%IS_AUTOSTART%"=="0" (
    if /I "%ACTION%"=="autostart" (
        del /q ".autostart_windows" >nul 2>nul
    )
    call :ensure_autostart_choice
)

echo ==============================================
echo [BERHASIL] Menjalankan server %APP_NAME%
echo Akses lokal: %APP_URL%
echo ==============================================

if "%IS_AUTOSTART%"=="0" start "" "%APP_URL%"

set "SMARTDOC_HOST=127.0.0.1"
set "SMARTDOC_PORT=5050"
set "SMARTDOC_DEBUG=0"
set "SMARTDOC_PRIVACY_MODE=1"

python app.py
if "%IS_AUTOSTART%"=="1" exit /b %errorlevel%

echo.
echo [INFO] Server berhenti. Tekan tombol apa pun untuk menutup jendela ini.
pause >nul
exit /b %errorlevel%

:choose_action
echo.
echo Pilih aksi:
echo   1. Jalankan aplikasi
echo   2. Install dependency sekarang
echo   3. Reinstall dependency
echo   4. Repair instalasi ^(buat ulang venv + install^)
echo   5. Atur ulang autostart
echo   6. Keluar
set /p MENU_CHOICE=Masukkan pilihan [1-6, default 1]:
if "%MENU_CHOICE%"=="" set "MENU_CHOICE=1"

if "%MENU_CHOICE%"=="1" set "ACTION=start"
if "%MENU_CHOICE%"=="2" set "ACTION=install"
if "%MENU_CHOICE%"=="3" set "ACTION=reinstall"
if "%MENU_CHOICE%"=="4" set "ACTION=repair"
if "%MENU_CHOICE%"=="5" set "ACTION=autostart"
if "%MENU_CHOICE%"=="6" set "ACTION=exit"

if /I "%ACTION%"=="autostart" (
    echo [INFO] Konfigurasi autostart akan ditawarkan ulang.
    set "ACTION=start"
)
goto :eof

:ensure_autostart_choice
set "CHOICE_FILE=.autostart_windows"
set "STARTUP_SHORTCUT=%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup\SmartDoc Kolaka Launcher.lnk"

if exist "%CHOICE_FILE%" goto :eof

echo.
set /p ENABLE_AUTOSTART=Aktifkan autostart Windows untuk %APP_NAME% pada komputer ini? [Y/N]:
if /I "%ENABLE_AUTOSTART%"=="Y" (
    call :install_autostart
    > "%CHOICE_FILE%" echo enabled
    goto :eof
)

if /I "%ENABLE_AUTOSTART%"=="N" (
    > "%CHOICE_FILE%" echo skipped
    goto :eof
)

echo [WARN] Pilihan tidak dikenali. Autostart dilewati untuk saat ini.
> "%CHOICE_FILE%" echo skipped
goto :eof

:install_autostart
echo [INFO] Menyiapkan autostart Windows...
set "POWERSHELL_CMD=$ws = New-Object -ComObject WScript.Shell; $shortcut = $ws.CreateShortcut('%STARTUP_SHORTCUT%'); $shortcut.TargetPath = '%SCRIPT_DIR%run_windows.bat'; $shortcut.Arguments = '--autostart'; $shortcut.WorkingDirectory = '%SCRIPT_DIR%'; $shortcut.IconLocation = '%SystemRoot%\System32\SHELL32.dll,220'; $shortcut.Save()"
powershell -NoProfile -ExecutionPolicy Bypass -Command "%POWERSHELL_CMD%"
if errorlevel 1 (
    echo [WARN] Gagal membuat shortcut autostart. Anda masih bisa menjalankan file ini manual.
) else (
    echo [INFO] Autostart Windows berhasil dibuat di folder Startup.
)
goto :eof
