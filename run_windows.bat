@echo off
chcp 65001 >nul
echo ==============================================
echo SmartDoc Kolaka - Local Startup Server
echo ==============================================

:: Masuk ke direktori skrip ini berada
cd /d "%~dp0"

:: Buat virtual environment jika belum ada
if not exist "venv" (
    echo [INFO] Membangun lingkungan virtual...
    python -m venv venv
)

echo [INFO] Mengaktifkan lingkungan virtual...
call venv\Scripts\activate.bat

:: Hanya install jika requirements berubah atau belum pernah install
set "MARKER=venv\.requirements_installed"
set "NEEDS_INSTALL=0"

if not exist "%MARKER%" (
    set "NEEDS_INSTALL=1"
) else (
    :: Bandingkan hash requirements.txt dengan marker
    for /f "tokens=*" %%H in ('certutil -hashfile requirements.txt MD5 2^>nul ^| findstr /v "hash certutil"') do (
        for /f "tokens=*" %%M in ('type "%MARKER%" 2^>nul') do (
            if not "%%H"=="%%M" set "NEEDS_INSTALL=1"
        )
    )
)

if "%NEEDS_INSTALL%"=="1" (
    echo [INFO] Menginstal/memperbarui paket yang dibutuhkan...
    pip install -q -r requirements.txt
    certutil -hashfile requirements.txt MD5 2>nul | findstr /v "hash certutil" > "%MARKER%"
    echo [INFO] Paket berhasil diinstal.
) else (
    echo [INFO] Paket sudah terinstal (skip install).
)

echo ==============================================
echo [BERHASIL] Menjalankan Server SmartDoc Kolaka
echo Silakan buka browser Anda dan akses:
echo http://127.0.0.1:5000
echo ==============================================

:: Buka browser otomatis
start "" "http://127.0.0.1:5000"

python app.py
pause
