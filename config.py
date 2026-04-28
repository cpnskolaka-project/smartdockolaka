import os


class Config:
    APP_NAME = "SmartDoc Kolaka"

    # Runtime
    HOST = os.getenv("SMARTDOC_HOST", "127.0.0.1")
    PORT = int(os.getenv("SMARTDOC_PORT", "5050"))
    DEBUG = os.getenv("SMARTDOC_DEBUG", "").strip().lower() in {"1", "true", "yes"}
    TEMPLATES_AUTO_RELOAD = True

    # Upload and processing limits
    MAX_CONTENT_LENGTH = 250 * 1024 * 1024  # 250 MB
    MAX_UPLOAD_FILES = 50
    MAX_PDF_PAGES = 250
    MAX_OCR_PDF_PAGES = 75
    MAX_IMAGE_PIXELS = 40_000_000
    MAX_RENDER_DPI = 300
    MAX_CAD_FILE_SIZE = 25 * 1024 * 1024
    MAX_CAD_DPI = 300

    # Timeouts
    PROCESS_TIMEOUT_SECONDS = 60
    CAD_TIMEOUT_SECONDS = 60
    NETWORK_TIMEOUT_SECONDS = 10
    PING_COUNT = 4

    # Logging and privacy
    PRIVACY_MODE = os.getenv("SMARTDOC_PRIVACY_MODE", "1").strip().lower() not in {"0", "false", "no"}
