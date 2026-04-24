import io
import zipfile
import json
from pathlib import Path

import fitz
from PIL import Image, UnidentifiedImageError


IMAGE_EXTENSIONS = {"jpg", "jpeg", "png", "bmp", "tiff", "webp", "gif"}
TEXT_EXTENSIONS = {"txt", "csv", "json", "html", "htm", "dxf"}
OFFICE_COMPATIBILITY = {
    "jpg": {"jpg", "jpeg"},
    "jpeg": {"jpg", "jpeg"},
    "xlsx": {"xlsx", "xlsm"},
    "xlsm": {"xlsx", "xlsm"},
}


def make_zip(files: list[tuple[str, bytes]]) -> io.BytesIO:
    """Create a ZIP file in memory from a list of (filename, data) tuples."""
    buf = io.BytesIO()
    with zipfile.ZipFile(buf, "w", zipfile.ZIP_DEFLATED) as zf:
        for name, data in files:
            zf.writestr(name, data)
    buf.seek(0)
    return buf


def allowed_file(filename: str, extensions: set[str]) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in extensions


def get_extension(filename: str) -> str:
    return Path(filename or "").suffix.lower().lstrip(".")


def parse_accept_string(accept: str) -> set[str]:
    items = set()
    for part in (accept or "").split(","):
        value = part.strip().lower().lstrip(".")
        if value:
            items.add(value)
    return items


def _is_text_like(data: bytes) -> bool:
    if not data:
        return True

    sample = data[:4096]
    if b"\x00" in sample:
        return False

    text_bytes = sum(32 <= b <= 126 or b in (9, 10, 13) for b in sample)
    return (text_bytes / len(sample)) >= 0.85


def _detect_zip_office_type(data: bytes) -> str | None:
    if not data.startswith(b"PK\x03\x04"):
        return None

    try:
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            names = set(zf.namelist())
    except zipfile.BadZipFile:
        return None

    if "word/document.xml" in names:
        return "docx"
    if "xl/workbook.xml" in names:
        return "xlsm" if "xl/vbaProject.bin" in names else "xlsx"
    return "zip"


def sniff_file_type(data: bytes, filename: str = "") -> str | None:
    ext = get_extension(filename)

    if data.startswith(b"%PDF"):
        return "pdf"
    if data.startswith(b"\x89PNG\r\n\x1a\n"):
        return "png"
    if data[:3] == b"\xff\xd8\xff":
        return "jpg"
    if data.startswith((b"GIF87a", b"GIF89a")):
        return "gif"
    if data.startswith(b"BM"):
        return "bmp"
    if data.startswith((b"II*\x00", b"MM\x00*")):
        return "tiff"
    if len(data) >= 12 and data[:4] == b"RIFF" and data[8:12] == b"WEBP":
        return "webp"
    if data.startswith(b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1"):
        return "xls"

    office_type = _detect_zip_office_type(data)
    if office_type:
        return office_type

    if _is_text_like(data):
        stripped = data.lstrip()
        if stripped.startswith((b"{", b"[", b'"')):
            try:
                json.loads(data.decode("utf-8", errors="strict"))
                return "json"
            except Exception:
                pass
        if ext in TEXT_EXTENSIONS:
            return ext
        return "txt"

    return None


def extensions_match(expected_ext: str, detected_ext: str | None) -> bool:
    if not detected_ext:
        return True
    if expected_ext == detected_ext:
        return True
    if expected_ext in OFFICE_COMPATIBILITY:
        return detected_ext in OFFICE_COMPATIBILITY[expected_ext]
    return False


def describe_files(files) -> str:
    names = [getattr(f, "filename", "") for f in files if getattr(f, "filename", "")]
    count = len(names)
    if count == 0:
        return "0 file"
    if count == 1:
        return "1 file"
    return f"{count} files"


def summarize_file_sizes(files) -> str:
    total = 0
    for file_storage in files:
        stream = getattr(file_storage, "stream", None)
        if not stream:
            continue
        current = stream.tell()
        stream.seek(0, 2)
        total += stream.tell()
        stream.seek(current)

    if total < 1024:
        return f"{total} B"
    if total < 1024 * 1024:
        return f"{total / 1024:.1f} KB"
    return f"{total / (1024 * 1024):.1f} MB"


def validate_uploaded_files(
    files,
    allowed_extensions: set[str],
    *,
    max_file_count: int | None = None,
    max_pdf_pages: int | None = None,
    max_image_pixels: int | None = None,
    max_single_size: int | None = None,
):
    valid_files = [f for f in files if getattr(f, "filename", "")]
    if max_file_count is not None and len(valid_files) > max_file_count:
        raise ValueError(f"Too many files uploaded. Maximum allowed is {max_file_count}.")

    for file_storage in valid_files:
        filename = file_storage.filename or "upload"
        ext = get_extension(filename)
        if allowed_extensions and ext not in allowed_extensions:
            raise ValueError(f"{filename}: unsupported file type '.{ext or 'unknown'}'.")

        data = file_storage.read()
        file_storage.stream.seek(0)

        if max_single_size is not None and len(data) > max_single_size:
            raise ValueError(f"{filename}: file is too large for this tool.")

        detected = sniff_file_type(data, filename)
        if allowed_extensions and detected:
            if not any(extensions_match(allowed_ext, detected) for allowed_ext in allowed_extensions):
                raise ValueError(f"{filename}: file content does not match the expected format.")
        elif not extensions_match(ext, detected):
            raise ValueError(f"{filename}: file content does not match the '.{ext}' extension.")

        if max_pdf_pages is not None and (ext == "pdf" or detected == "pdf"):
            try:
                with fitz.open(stream=data, filetype="pdf") as doc:
                    if len(doc) > max_pdf_pages:
                        raise ValueError(
                            f"{filename}: PDF has {len(doc)} pages. Maximum allowed is {max_pdf_pages} pages."
                        )
            except ValueError:
                raise
            except Exception as exc:
                raise ValueError(f"{filename}: invalid PDF file ({exc}).") from exc

        if max_image_pixels is not None and (ext in IMAGE_EXTENSIONS or detected in IMAGE_EXTENSIONS):
            try:
                with Image.open(io.BytesIO(data)) as img:
                    pixels = img.width * img.height
                    if pixels > max_image_pixels:
                        raise ValueError(
                            f"{filename}: image is too large ({pixels:,} pixels). Maximum allowed is {max_image_pixels:,} pixels."
                        )
            except ValueError:
                raise
            except (UnidentifiedImageError, OSError) as exc:
                raise ValueError(f"{filename}: invalid image file ({exc}).") from exc
