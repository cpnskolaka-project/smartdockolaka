#!/bin/bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

APP_NAME="SmartDoc Kolaka"
APP_URL="http://127.0.0.1:5050"
AUTOSTART_ARG="${1:-}"
IS_AUTOSTART=0
ACTION="start"
if [[ "$AUTOSTART_ARG" == "--autostart" ]]; then
    IS_AUTOSTART=1
fi

choose_action() {
    echo
    echo "Pilih aksi:"
    echo "  1. Jalankan aplikasi"
    echo "  2. Install dependency sekarang"
    echo "  3. Reinstall dependency"
    echo "  4. Repair instalasi (buat ulang venv + install)"
    echo "  5. Atur ulang autostart"
    echo "  6. Keluar"
    read -r -p "Masukkan pilihan [1-6, default 1]: " menu_choice
    case "${menu_choice:-1}" in
        1) ACTION="start" ;;
        2) ACTION="install" ;;
        3) ACTION="reinstall" ;;
        4) ACTION="repair" ;;
        5) ACTION="autostart" ;;
        6) ACTION="exit" ;;
        *) ACTION="start" ;;
    esac
}

ensure_autostart_choice() {
    local choice_file=".autostart_macos"
    if [[ -f "$choice_file" ]]; then
        return
    fi

    echo
    read -r -p "Aktifkan autostart macOS untuk $APP_NAME pada komputer ini? [y/N]: " answer
    case "${answer:-N}" in
        y|Y)
            install_autostart
            printf "enabled" > "$choice_file"
            ;;
        *)
            printf "skipped" > "$choice_file"
            ;;
    esac
}

install_autostart() {
    local plist_dir="$HOME/Library/LaunchAgents"
    local plist_path="$plist_dir/id.kppkolaka.smartdockolaka.plist"
    mkdir -p "$plist_dir"

    cat > "$plist_path" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>id.kppkolaka.smartdockolaka</string>
    <key>ProgramArguments</key>
    <array>
        <string>/bin/bash</string>
        <string>$SCRIPT_DIR/run_mac.command</string>
        <string>--autostart</string>
    </array>
    <key>WorkingDirectory</key>
    <string>$SCRIPT_DIR</string>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <false/>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>/usr/local/bin:/opt/homebrew/bin:/usr/bin:/bin:/usr/sbin:/sbin</string>
        <key>DYLD_LIBRARY_PATH</key>
        <string>/opt/homebrew/lib</string>
    </dict>
</dict>
</plist>
PLIST

    launchctl unload "$plist_path" >/dev/null 2>&1 || true
    if launchctl load "$plist_path" >/dev/null 2>&1; then
        echo "[INFO] Autostart macOS berhasil diaktifkan."
    else
        echo "[WARN] LaunchAgent dibuat, tetapi gagal diload otomatis. Coba login ulang atau cek System Check."
    fi
}

echo "=============================================="
echo "$APP_NAME - Installer dan Local Runner"
echo "=============================================="

if ! command -v python3 >/dev/null 2>&1; then
    echo "[ERROR] python3 tidak ditemukan."
    echo "[INFO] Instal Python 3 terlebih dahulu, lalu jalankan file ini lagi."
    read -r -p "Tekan Enter untuk menutup..."
    exit 1
fi

if [[ "$IS_AUTOSTART" -eq 0 ]]; then
    choose_action
fi

if [[ "$ACTION" == "exit" ]]; then
    exit 0
fi

if [[ "$ACTION" == "repair" ]]; then
    echo "[INFO] Mode repair dipilih. Virtual environment lama akan dibuat ulang."
    rm -rf venv
fi

if [[ ! -d "venv" ]]; then
    echo "[INFO] Membuat virtual environment..."
    python3 -m venv venv
fi

echo "[INFO] Mengaktifkan virtual environment..."
source venv/bin/activate

MARKER="venv/.requirements_installed"
if command -v md5 >/dev/null 2>&1; then
    REQ_HASH="$(md5 -q requirements.txt)"
else
    REQ_HASH="$(md5sum requirements.txt | awk '{print $1}')"
fi

NEEDS_INSTALL=0
if [[ ! -f "$MARKER" ]]; then
    NEEDS_INSTALL=1
elif [[ "$(cat "$MARKER")" != "$REQ_HASH" ]]; then
    NEEDS_INSTALL=1
fi

PIP_INSTALL=(python -m pip install -r requirements.txt)
if [[ "$NEEDS_INSTALL" -eq 1 ]]; then
    echo "[INFO] Instalasi awal atau perubahan dependency terdeteksi."
    echo "[INFO] Komputer ini perlu terhubung ke internet untuk memasang dependency Python."
fi

if [[ "$ACTION" == "reinstall" ]]; then
    NEEDS_INSTALL=1
    PIP_INSTALL=(python -m pip install --force-reinstall -r requirements.txt)
fi

if [[ "$ACTION" == "install" || "$ACTION" == "repair" ]]; then
    NEEDS_INSTALL=1
fi

if [[ "$NEEDS_INSTALL" -eq 1 ]]; then
    echo "[INFO] Menginstal atau memperbarui dependency..."
    if ! "${PIP_INSTALL[@]}"; then
        echo "[ERROR] Instalasi dependency gagal."
        echo "[INFO] Pastikan koneksi internet tersedia saat instalasi pertama atau saat reinstall/repair."
        read -r -p "Tekan Enter untuk menutup..."
        exit 1
    fi
    printf "%s" "$REQ_HASH" > "$MARKER"
    echo "[INFO] Dependency siap digunakan."
else
    echo "[INFO] Dependency sudah sesuai. Lewati instalasi."
fi

if [[ "$IS_AUTOSTART" -eq 0 ]]; then
    if [[ "$ACTION" == "autostart" ]]; then
        rm -f .autostart_macos
    fi
    ensure_autostart_choice
fi

echo "=============================================="
echo "[BERHASIL] Menjalankan server $APP_NAME"
echo "Akses lokal: $APP_URL"
echo "=============================================="

if [[ "$IS_AUTOSTART" -eq 0 ]]; then
    open "$APP_URL" >/dev/null 2>&1 &
fi

export SMARTDOC_HOST=127.0.0.1
export SMARTDOC_PORT=5050
export SMARTDOC_DEBUG=0
export SMARTDOC_PRIVACY_MODE=1
export DYLD_LIBRARY_PATH="/opt/homebrew/lib:${DYLD_LIBRARY_PATH:-}"

exec python3 app.py
