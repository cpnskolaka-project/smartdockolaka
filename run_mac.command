#!/bin/bash
echo "=============================================="
echo "SmartDoc Kolaka - Local Startup Server"
echo "=============================================="

# Masuk ke direktori skrip ini berada
cd "$(dirname "$0")"

# Buat virtual environment jika belum ada
if [ ! -d "venv" ]; then
    echo "[INFO] Membangun lingkungan virtual..."
    python3 -m venv venv
fi

echo "[INFO] Mengaktifkan lingkungan virtual..."
source venv/bin/activate

# Hanya install jika requirements berubah atau belum pernah install
MARKER="venv/.requirements_installed"
REQ_HASH=$(md5 -q requirements.txt 2>/dev/null || md5sum requirements.txt | cut -d' ' -f1)

if [ ! -f "$MARKER" ] || [ "$(cat "$MARKER")" != "$REQ_HASH" ]; then
    echo "[INFO] Menginstal/memperbarui paket yang dibutuhkan..."
    pip3 install -q -r requirements.txt
    echo "$REQ_HASH" > "$MARKER"
    echo "[INFO] Paket berhasil diinstal."
else
    echo "[INFO] Paket sudah terinstal (skip install)."
fi

echo "=============================================="
echo "[BERHASIL] Menjalankan Server SmartDoc Kolaka"
echo "Silakan buka browser Anda dan akses:"
echo "http://127.0.0.1:5000"
echo "=============================================="

# Buka browser otomatis (macOS)
open "http://127.0.0.1:5000" 2>/dev/null &

# Export Homebrew lib path for pyzbar (Apple Silicon Macs)
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH

exec python3 app.py
