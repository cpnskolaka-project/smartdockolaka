import os
from flask import Flask, render_template, request, redirect, url_for
import logger

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 100 * 1024 * 1024  # 100 MB max upload

# Initialize DB
logger.init_db()

TOOL_CATEGORIES = [
    {
        "id": "convert",
        "name": "Document Conversion",
        "icon": "bi-files",
        "tools": [
            {"id": "to-pdf", "name": "Files to PDF", "desc": "Convert images and text files to PDF", "icon": "bi-file-pdf-fill"},
            {"id": "pdf-to-word", "name": "PDF to Word", "desc": "Convert PDF to Word document", "icon": "bi-file-word-fill"},
            {"id": "pdf-to-excel", "name": "PDF to Excel", "desc": "Extract PDF tabular data to Excel", "icon": "bi-file-earmark-spreadsheet-fill"},
            {"id": "pdf-to-images", "name": "PDF to Images", "desc": "Convert PDF pages to images", "icon": "bi-file-image-fill"},
            {"id": "pdf-to-text", "name": "PDF to Text", "desc": "Extract text content from PDF", "icon": "bi-file-text-fill"},
            {"id": "html-to-pdf", "name": "HTML to PDF", "desc": "Convert HTML content to PDF", "icon": "bi-filetype-html"},
            {"id": "ocr-pdf", "name": "OCR PDF", "desc": "Make scanned PDFs searchable or extract text", "icon": "bi-file-earmark-text-fill"},
            {"id": "cad-to-pdf", "name": "CAD to PDF/Image", "desc": "Convert DXF/DWG drawings to PDF or PNG", "icon": "bi-rulers"},
        ],
    },
    {
        "id": "pdf",
        "name": "PDF Tools",
        "icon": "bi-file-pdf-fill",
        "tools": [
            {"id": "merge", "name": "Merge PDFs", "desc": "Combine multiple PDFs into one", "icon": "bi-union"},
            {"id": "split", "name": "Split PDF", "desc": "Split PDF into individual pages", "icon": "bi-scissors"},
            {"id": "delete", "name": "Delete Pages", "desc": "Remove specific pages from PDF", "icon": "bi-file-earmark-x"},
            {"id": "compress", "name": "Compress PDF", "desc": "Reduce PDF file size", "icon": "bi-file-zip-fill"},
            {"id": "rotate", "name": "Rotate PDF", "desc": "Rotate PDF pages", "icon": "bi-arrow-clockwise"},
            {"id": "resize", "name": "Resize PDF", "desc": "Change PDF page dimensions", "icon": "bi-aspect-ratio-fill"},
            {"id": "page-numbers", "name": "Page Numbers", "desc": "Add page numbers to PDF", "icon": "bi-123"},
            {"id": "extract-images", "name": "Extract Images", "desc": "Extract images from PDF", "icon": "bi-images"},
            {"id": "watermark", "name": "PDF Watermark", "desc": "Add text watermark to PDF documents", "icon": "bi-water"},
            {"id": "protect", "name": "Protect PDF", "desc": "Add password protection to PDF", "icon": "bi-lock-fill"},
            {"id": "unlock", "name": "Unlock PDF", "desc": "Remove PDF password", "icon": "bi-unlock-fill"},
        ],
    },
    {
        "id": "spreadsheet",
        "name": "Spreadsheet",
        "icon": "bi-file-earmark-spreadsheet-fill",
        "tools": [
            {"id": "excel-to-csv", "name": "Excel to CSV/JSON", "desc": "Export sheets as CSV or JSON", "icon": "bi-table"},
            {"id": "csv-to-excel", "name": "CSV/JSON to Excel", "desc": "Build .xlsx from CSV or JSON files", "icon": "bi-file-earmark-spreadsheet"},
            {"id": "excel-to-pdf", "name": "Excel to PDF", "desc": "Convert workbook to PDF (one section per sheet)", "icon": "bi-file-pdf"},
            {"id": "merge", "name": "Merge Workbooks", "desc": "Combine multiple Excel files into one", "icon": "bi-union"},
            {"id": "split", "name": "Split Sheets", "desc": "Export each sheet as its own .xlsx", "icon": "bi-scissors"},
            {"id": "info", "name": "Excel Info & Preview", "desc": "List sheets, counts, and preview rows", "icon": "bi-info-circle-fill"},
        ],
    },
    {
        "id": "image",
        "name": "Image Tools",
        "icon": "bi-image-fill",
        "tools": [
            {"id": "resize", "name": "Resize Image", "desc": "Resize by percentage or dimensions", "icon": "bi-arrows-angle-expand"},
            {"id": "compress", "name": "Compress Image", "desc": "Reduce image file size", "icon": "bi-file-zip-fill"},
            {"id": "convert", "name": "Convert Format", "desc": "Convert between image formats", "icon": "bi-arrow-left-right"},
            {"id": "remove-bg", "name": "Remove Background", "desc": "Remove image background", "icon": "bi-eraser-fill"},
            {"id": "crop", "name": "Crop Image", "desc": "Crop images to specific dimensions", "icon": "bi-crop"},
            {"id": "rotate", "name": "Rotate / Flip", "desc": "Rotate or flip images", "icon": "bi-arrow-repeat"},
            {"id": "watermark", "name": "Add Watermark", "desc": "Add text watermark to images", "icon": "bi-water"},
            {"id": "exif", "name": "EXIF Viewer", "desc": "View and strip image metadata", "icon": "bi-info-circle-fill"},
            {"id": "favicon", "name": "Favicon Generator", "desc": "Create .ico favicons from images", "icon": "bi-app-indicator"},
            {"id": "ocr", "name": "Image to Text", "desc": "Extract text from images (OCR)", "icon": "bi-card-text"},
            {"id": "animated", "name": "Animated WebP/GIF", "desc": "Convert between animated WebP and GIF", "icon": "bi-film"},
        ],
    },
    {
        "id": "text",
        "name": "Text & Data",
        "icon": "bi-braces",
        "tools": [
            {"id": "json-formatter", "name": "JSON Formatter", "desc": "Format and validate JSON", "icon": "bi-braces"},
            {"id": "csv-json", "name": "CSV / JSON", "desc": "Convert between CSV and JSON", "icon": "bi-table"},
            {"id": "base64", "name": "Base64", "desc": "Encode and decode Base64", "icon": "bi-hash"},
            {"id": "url-encode", "name": "URL Encode", "desc": "Encode and decode URLs", "icon": "bi-link-45deg"},
            {"id": "word-counter", "name": "Word Counter", "desc": "Count words, characters, sentences", "icon": "bi-type"},
            {"id": "markdown", "name": "Markdown Preview", "desc": "Preview Markdown as HTML", "icon": "bi-markdown-fill"},
            {"id": "case-converter", "name": "Case Converter", "desc": "Convert text between cases", "icon": "bi-type-bold"},
            {"id": "text-diff", "name": "Text Diff", "desc": "Compare two texts side by side", "icon": "bi-file-diff-fill"},
            {"id": "regex-tester", "name": "Regex Tester", "desc": "Test regular expressions live", "icon": "bi-search"},
            {"id": "slug-generator", "name": "Slug Generator", "desc": "Create URL-friendly slugs", "icon": "bi-link"},
            {"id": "json-yaml", "name": "JSON / YAML", "desc": "Convert between JSON and YAML", "icon": "bi-filetype-yml"},
            {"id": "lorem-ipsum", "name": "Lorem Ipsum", "desc": "Generate placeholder text", "icon": "bi-text-paragraph"},
        ],
    },
    {
        "id": "calc",
        "name": "Calculators",
        "icon": "bi-calculator-fill",
        "tools": [
            {"id": "calculator", "name": "Calculator", "desc": "Basic and scientific calculator", "icon": "bi-calculator"},
            {"id": "unit-converter", "name": "Unit Converter", "desc": "Convert between units of measurement", "icon": "bi-arrow-left-right"},
            {"id": "color-converter", "name": "Color Converter", "desc": "Convert HEX, RGB, HSL colors", "icon": "bi-palette-fill"},
            {"id": "percentage", "name": "Percentage Calc", "desc": "Calculate percentages easily", "icon": "bi-percent"},
            {"id": "date", "name": "Date Calculator", "desc": "Calculate date differences", "icon": "bi-calendar-date-fill"},
            {"id": "timestamp", "name": "Timestamp", "desc": "Convert Unix timestamps", "icon": "bi-clock-fill"},
            {"id": "number-base", "name": "Number Base", "desc": "Convert between number bases", "icon": "bi-123"},
            {"id": "pomodoro", "name": "Pomodoro Timer", "desc": "Focus timer with breaks", "icon": "bi-stopwatch-fill"},
        ],
    },
    {
        "id": "qr",
        "name": "QR Code",
        "icon": "bi-qr-code",
        "tools": [
            {"id": "generate", "name": "Generate QR", "desc": "Create QR codes from text or URLs", "icon": "bi-qr-code"},
            {"id": "read", "name": "Read QR", "desc": "Decode QR codes from images", "icon": "bi-qr-code-scan"},
        ],
    },
    {
        "id": "security",
        "name": "Security",
        "icon": "bi-shield-lock-fill",
        "tools": [
            {"id": "password-generator", "name": "Password Generator", "desc": "Generate strong random passwords", "icon": "bi-key-fill"},
            {"id": "hash-generator", "name": "Hash Generator", "desc": "Generate MD5, SHA hashes", "icon": "bi-fingerprint"},
        ],
    },
    {
        "id": "network",
        "name": "Alat Jaringan",
        "icon": "bi-hdd-network-fill",
        "tools": [
            {"id": "ping", "name": "Cek Ping", "desc": "Periksa konektivitas dan latensi jaringan", "icon": "bi-activity"},
        ],
    },
]


# Build endpoint → human-readable name mapping from TOOL_CATEGORIES
ENDPOINT_NAMES = {}
ENDPOINT_CATEGORIES = {}
for _cat in TOOL_CATEGORIES:
    for _tool in _cat["tools"]:
        # Blueprint endpoints use format: "blueprint.function_name"
        # Function names replace hyphens with underscores
        _fn = _tool["id"].replace("-", "_")
        _ep = f"{_cat['id']}.{_fn}"
        ENDPOINT_NAMES[_ep] = _tool["name"]
        ENDPOINT_CATEGORIES[_ep] = _cat["name"]
    # Also map POST processing endpoints (some differ from page route names)
    # e.g., convert.to_pdf (page) → convert.to_pdf (POST) share the same endpoint
# Special overrides for endpoints whose function names differ from tool IDs
ENDPOINT_NAMES.update({
    "pdf.process_delete": "Delete Pages",
    "pdf.process_watermark": "PDF Watermark",
    "convert.process_pdf_excel": "PDF to Excel",
    "network.process_ping": "Cek Ping",
})
ENDPOINT_CATEGORIES.update({
    "pdf.process_delete": "PDF Tools",
    "pdf.process_watermark": "PDF Tools",
    "convert.process_pdf_excel": "Document Conversion",
    "network.process_ping": "Alat Jaringan",
})


@app.context_processor
def inject_tools():
    return {"tool_categories": TOOL_CATEGORIES}


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/history")
def history():
    logs = logger.get_logs()
    stats = logger.get_stats()
    return render_template("history.html", logs=logs, stats=stats)

@app.route("/clear_history", methods=["POST"])
def clear_history():
    logger.clear_logs()
    return redirect(url_for("history"))

import time as _time

@app.before_request
def before_request_timer():
    request._start_time = _time.time()

@app.after_request
def after_request_logger(response):
    if request.method == "POST" and request.endpoint:
        # Skip static files and internal endpoints
        if request.endpoint not in ("static", "clear_history"):
            # Calculate duration
            duration_ms = 0
            if hasattr(request, "_start_time"):
                duration_ms = int((_time.time() - request._start_time) * 1000)

            # Resolve human-readable names
            ep = request.endpoint
            tool_name = ENDPOINT_NAMES.get(ep, ep.replace(".", " › ").replace("_", " ").title())
            category = ENDPOINT_CATEGORIES.get(ep, ep.split(".")[0].title() if "." in ep else "")

            # Extract detail info
            detail = ""
            if response.status_code >= 400:
                # Try to get error message from JSON response
                try:
                    data = response.get_json(silent=True)
                    if data and "error" in data:
                        detail = f"Error: {data['error'][:250]}"
                except Exception:
                    detail = f"HTTP {response.status_code}"
            else:
                # For success, note file info if available
                files = request.files.getlist("files")
                if files and files[0].filename:
                    fnames = ", ".join(f.filename for f in files if f.filename)
                    detail = f"File: {fnames[:200]}"
                elif request.form.get("text"):
                    text_preview = request.form["text"][:80]
                    detail = f'Input: "{text_preview}..."' if len(request.form["text"]) > 80 else f'Input: "{text_preview}"'

            logger.log_activity(
                tool_endpoint=ep,
                status_code=response.status_code,
                user_agent=request.headers.get('User-Agent', ''),
                tool_name=tool_name,
                category=category,
                detail=detail,
                duration_ms=duration_ms,
            )
    return response


@app.errorhandler(413)
def too_large(e):
    return {"error": "File terlalu besar. Maksimum ukuran file adalah 100 MB."}, 413


@app.errorhandler(500)
def server_error(e):
    return {"error": f"Terjadi kesalahan internal server: {str(e)}"}, 500


# Register blueprints
from routes.convert_tools import bp as convert_bp
from routes.pdf_tools import bp as pdf_bp
from routes.image_tools import bp as image_bp
from routes.text_tools import bp as text_bp
from routes.calculator_tools import bp as calc_bp
from routes.qr_tools import bp as qr_bp
from routes.security_tools import bp as security_bp
from routes.spreadsheet_tools import bp as spreadsheet_bp
from routes.network_tools import bp as network_bp

app.register_blueprint(convert_bp, url_prefix="/convert")
app.register_blueprint(pdf_bp, url_prefix="/pdf")
app.register_blueprint(image_bp, url_prefix="/image")
app.register_blueprint(text_bp, url_prefix="/text")
app.register_blueprint(calc_bp, url_prefix="/calc")
app.register_blueprint(qr_bp, url_prefix="/qr")
app.register_blueprint(security_bp, url_prefix="/security")
app.register_blueprint(spreadsheet_bp, url_prefix="/spreadsheet")
app.register_blueprint(network_bp, url_prefix="/network")

if __name__ == "__main__":
    app.run(debug=True, port=5000)
