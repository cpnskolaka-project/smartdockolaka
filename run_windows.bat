@echo off
echo ==============================================
echo SmartDoc Kolaka - Local Startup Server
echo ==============================================

cd /d "%~dp0"

IF NOT EXIST venv (
    echo [INFO] Membangun lingkungan virtual...
    python -m venv venv
)

echo [INFO] Mengaktifkan lingkungan virtual...
call venv\Scripts\activate

echo [INFO] Memeriksa dan menginstal paket yang dibutuhkan...
pip install -r requirements.txt
pip install "rembg[cpu]"

echo ==============================================
echo [BERHASIL] Menjalankan Server SmartDoc Kolaka
echo Silakan buka browser Anda dan akses:
echo http://127.0.0.1:5000
echo ==============================================

python app.py

pause
