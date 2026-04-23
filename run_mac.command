#!/bin/bash
echo "=============================================="
echo "SmartDoc Kolaka - Local Startup Server"
echo "=============================================="

# Masuk ke direktori skrip ini berada
cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "[INFO] Membangun lingkungan virtual..."
    python3 -m venv venv
fi

echo "[INFO] Mengaktifkan lingkungan virtual..."
source venv/bin/activate

echo "[INFO] Memeriksa dan menginstal paket yang dibutuhkan..."
pip3 install -r requirements.txt
pip3 install "rembg[cpu]"

echo "=============================================="
echo "[BERHASIL] Menjalankan Server SmartDoc Kolaka"
echo "Silakan buka browser Anda dan akses:"
echo "http://127.0.0.1:5000"
echo "=============================================="

exec python3 app.py
