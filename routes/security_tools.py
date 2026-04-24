import importlib.util
import os
import platform
import shutil
import sqlite3
import sys
from importlib import metadata
from pathlib import Path

from flask import Blueprint, current_app, render_template

bp = Blueprint("security", __name__)


@bp.route("/password-generator")
def password_generator():
    return render_template("tools/password_generator.html")


@bp.route("/hash-generator")
def hash_generator():
    return render_template("tools/hash_generator.html")


def _module_installed(module_name: str) -> bool:
    return importlib.util.find_spec(module_name) is not None


def _installed_version(*names: str) -> str:
    for name in names:
        if not name:
            continue
        try:
            return metadata.version(name)
        except metadata.PackageNotFoundError:
            continue
    return ""


def _windows_autostart_path() -> Path:
    startup_dir = os.environ.get("APPDATA", "")
    return Path(startup_dir) / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" / "SmartDoc Kolaka Launcher.lnk"


def _mac_launch_agent_path() -> Path:
    return Path.home() / "Library" / "LaunchAgents" / "id.kppkolaka.smartdockolaka.plist"


@bp.route("/system-check")
def system_check():
    project_root = Path(current_app.root_path)
    db_path = project_root / "app_history.db"
    venv_path = project_root / "venv"
    marker_path = venv_path / ".requirements_installed"

    module_checks = [
        {"name": "Flask", "import_name": "flask", "required": True, "version_names": ("Flask", "flask")},
        {"name": "Pillow", "import_name": "PIL", "required": True, "version_names": ("Pillow",)},
        {"name": "PyMuPDF", "import_name": "fitz", "required": True, "version_names": ("PyMuPDF", "pymupdf")},
        {"name": "qrcode", "import_name": "qrcode", "required": True, "version_names": ("qrcode",)},
        {"name": "markdown", "import_name": "markdown", "required": True, "version_names": ("Markdown", "markdown")},
        {"name": "reportlab", "import_name": "reportlab", "required": True, "version_names": ("reportlab",)},
        {"name": "img2pdf", "import_name": "img2pdf", "required": True, "version_names": ("img2pdf",)},
        {"name": "python-docx", "import_name": "docx", "required": True, "version_names": ("python-docx", "python_docx")},
        {"name": "openpyxl", "import_name": "openpyxl", "required": True, "version_names": ("openpyxl",)},
        {"name": "xlrd", "import_name": "xlrd", "required": False, "version_names": ("xlrd",)},
        {"name": "pdf2docx", "import_name": "pdf2docx", "required": False, "version_names": ("pdf2docx",)},
        {"name": "pytesseract", "import_name": "pytesseract", "required": False, "version_names": ("pytesseract",)},
        {"name": "rembg", "import_name": "rembg", "required": False, "version_names": ("rembg",)},
        {"name": "pyzbar", "import_name": "pyzbar", "required": False, "version_names": ("pyzbar",)},
        {"name": "ezdxf", "import_name": "ezdxf", "required": False, "version_names": ("ezdxf",)},
        {"name": "matplotlib", "import_name": "matplotlib", "required": False, "version_names": ("matplotlib",)},
    ]
    for item in module_checks:
        item["installed"] = _module_installed(item["import_name"])
        item["installed_version"] = _installed_version(*item["version_names"])

    binaries = [
        {"name": "python", "path": shutil.which("python") or shutil.which("python3")},
        {"name": "tesseract", "path": shutil.which("tesseract")},
        {"name": "ping", "path": shutil.which("ping")},
        {"name": "ODAFileConverter", "path": shutil.which("ODAFileConverter") or shutil.which("oda_file_converter")},
    ]

    system_name = platform.system()
    if system_name == "Windows":
        autostart_path = _windows_autostart_path()
    elif system_name == "Darwin":
        autostart_path = _mac_launch_agent_path()
    else:
        autostart_path = None

    stats = {
        "python_version": sys.version.split()[0],
        "platform": f"{platform.system()} {platform.release()}",
        "host": current_app.config["HOST"],
        "port": current_app.config["PORT"],
        "privacy_mode": current_app.config["PRIVACY_MODE"],
        "debug": current_app.config["DEBUG"],
        "max_upload_mb": current_app.config["MAX_CONTENT_LENGTH"] // (1024 * 1024),
        "max_pdf_pages": current_app.config["MAX_PDF_PAGES"],
        "max_ocr_pdf_pages": current_app.config["MAX_OCR_PDF_PAGES"],
        "max_image_pixels": current_app.config["MAX_IMAGE_PIXELS"],
        "autostart_enabled": autostart_path.exists() if autostart_path else False,
        "autostart_path": str(autostart_path) if autostart_path else "Belum didukung untuk OS ini",
        "history_db_exists": db_path.exists(),
        "history_db_size_kb": round(db_path.stat().st_size / 1024, 1) if db_path.exists() else 0,
        "venv_exists": venv_path.exists(),
        "requirements_marker_exists": marker_path.exists(),
        "initial_install_ready": all(item["installed"] for item in module_checks if item["required"]),
    }

    db_ok = False
    db_error = ""
    if db_path.exists():
        try:
            with sqlite3.connect(db_path) as conn:
                conn.execute("SELECT 1 FROM activity_logs LIMIT 1")
            db_ok = True
        except sqlite3.Error as exc:
            db_error = str(exc)

    return render_template(
        "tools/system_check.html",
        module_checks=module_checks,
        binaries=binaries,
        stats=stats,
        db_ok=db_ok,
        db_error=db_error,
    )
