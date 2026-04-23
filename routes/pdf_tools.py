import io
import fitz  # PyMuPDF
from flask import Blueprint, render_template, request, send_file, jsonify
from utils.file_utils import make_zip

bp = Blueprint("pdf", __name__)


# ── Page Routes ──────────────────────────────────

@bp.route("/merge")
def merge_page():
    return render_template("upload_tool.html",
        title="Merge PDFs",
        description="Combine multiple PDF files into one document",
        endpoint="/pdf/merge",
        accept=".pdf",
        multiple=True,
        options=[])


@bp.route("/split")
def split_page():
    return render_template("upload_tool.html",
        title="Split PDF",
        description="Split a PDF into individual pages or custom ranges",
        endpoint="/pdf/split",
        accept=".pdf",
        multiple=False,
        options=[
            {"type": "text", "name": "pages", "label": "Page ranges (leave empty for all pages)",
             "placeholder": "e.g. 1-3, 5, 7-10"},
        ])


@bp.route("/delete")
def delete_pages():
    return render_template(
        "upload_tool.html",
        title="Delete Pages",
        description="Remove specific pages from PDF",
        endpoint="/pdf/delete",
        accept=".pdf",
        multiple=False,
        options=[
            {"name": "pages", "label": "Pages to delete (e.g. 1, 3-5):", "type": "text", "placeholder": "1, 3-5", "required": True}
        ],
    )


@bp.route("/compress")
def compress_page():
    return render_template("upload_tool.html",
        title="Compress PDF",
        description="Reduce PDF file size by compressing images and cleaning up",
        endpoint="/pdf/compress",
        accept=".pdf",
        multiple=False,
        options=[
            {"type": "select", "name": "quality", "label": "Compression Level",
             "choices": [
                 {"value": "medium", "label": "Medium (good balance)"},
                 {"value": "low", "label": "Maximum compression"},
                 {"value": "high", "label": "Minimal compression"},
             ]},
        ])


@bp.route("/rotate")
def rotate_page():
    return render_template("upload_tool.html",
        title="Rotate PDF",
        description="Rotate all or specific pages of a PDF",
        endpoint="/pdf/rotate",
        accept=".pdf",
        multiple=False,
        options=[
            {"type": "select", "name": "angle", "label": "Rotation Angle",
             "choices": [
                 {"value": "90", "label": "90° Clockwise"},
                 {"value": "180", "label": "180°"},
                 {"value": "270", "label": "90° Counter-clockwise"},
             ]},
            {"type": "text", "name": "pages", "label": "Pages to rotate (leave empty for all)",
             "placeholder": "e.g. 1, 3, 5-7"},
        ])


@bp.route("/resize")
def resize_page():
    return render_template("upload_tool.html",
        title="Resize PDF",
        description="Change the page dimensions of a PDF",
        endpoint="/pdf/resize",
        accept=".pdf",
        multiple=False,
        options=[
            {"type": "select", "name": "mode", "label": "Resize Mode",
             "choices": [
                 {"value": "scale", "label": "Scale by percentage"},
                 {"value": "paper", "label": "Standard paper size"},
             ]},
            {"type": "number", "name": "scale", "label": "Scale (%)", "default": 100, "min": 10, "max": 500,
             "depends_on": {"mode": "scale"}},
            {"type": "select", "name": "paper", "label": "Paper Size",
             "choices": [
                 {"value": "a4", "label": "A4 (210 x 297 mm)"},
                 {"value": "letter", "label": "Letter (8.5 x 11 in)"},
                 {"value": "a3", "label": "A3 (297 x 420 mm)"},
                 {"value": "a5", "label": "A5 (148 x 210 mm)"},
                 {"value": "legal", "label": "Legal (8.5 x 14 in)"},
             ],
             "depends_on": {"mode": "paper"}},
        ])


@bp.route("/page-numbers")
def page_numbers_page():
    return render_template("upload_tool.html",
        title="Add Page Numbers",
        description="Add page numbers to each page of a PDF",
        endpoint="/pdf/page-numbers",
        accept=".pdf",
        multiple=False,
        options=[
            {"type": "select", "name": "position", "label": "Position",
             "choices": [
                 {"value": "bottom-center", "label": "Bottom Center"},
                 {"value": "bottom-right", "label": "Bottom Right"},
                 {"value": "bottom-left", "label": "Bottom Left"},
                 {"value": "top-center", "label": "Top Center"},
                 {"value": "top-right", "label": "Top Right"},
                 {"value": "top-left", "label": "Top Left"},
             ]},
            {"type": "number", "name": "start", "label": "Start number", "default": 1, "min": 0},
            {"type": "number", "name": "fontsize", "label": "Font size", "default": 11, "min": 6, "max": 30},
        ])


@bp.route("/extract-images")
def extract_images_page():
    return render_template(
        "upload_tool.html",
        title="Extract Images",
        description="Extract all images embedded in PDF",
        endpoint="/pdf/extract-images",
        accept=".pdf",
        multiple=False,
        options=[]
    )

@bp.route("/watermark")
def watermark():
    return render_template(
        "upload_tool.html",
        title="PDF Watermark",
        description="Add text watermark to PDF documents",
        endpoint="/pdf/watermark",
        accept=".pdf",
        multiple=False,
        options=[
            {"name": "text", "label": "Watermark Text:", "type": "text", "required": True, "placeholder": "CONFIDENTIAL"},
            {"name": "color", "label": "Text Color:", "type": "color", "value": "#ff0000"},
            {"name": "opacity", "label": "Opacity (10%-100%):", "type": "range", "min": 10, "max": 100, "step": 5, "value": "30"},
            {"name": "angle", "label": "Rotation Angle (°):", "type": "number", "value": "45"},
            {"name": "size", "label": "Font Size:", "type": "number", "value": "72"}
        ],
    )


@bp.route("/protect")
def protect_page():
    return render_template("upload_tool.html",
        title="Protect PDF",
        description="Add password protection to a PDF file",
        endpoint="/pdf/protect",
        accept=".pdf",
        multiple=False,
        options=[
            {"type": "password", "name": "user_password", "label": "User Password (to open)",
             "placeholder": "Enter password"},
            {"type": "password", "name": "owner_password", "label": "Owner Password (optional, for editing)",
             "placeholder": "Leave empty to use same password"},
        ])


@bp.route("/unlock")
def unlock_page():
    return render_template("upload_tool.html",
        title="Unlock PDF",
        description="Remove password protection from a PDF",
        endpoint="/pdf/unlock",
        accept=".pdf",
        multiple=False,
        options=[
            {"type": "password", "name": "password", "label": "PDF Password",
             "placeholder": "Enter the current password"},
        ])


# ── Processing Routes ────────────────────────────

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255 for i in (0, 2, 4))


def parse_page_ranges(spec: str, total: int) -> list[int]:
    """Parse '1-3, 5, 7-10' into a list of 0-based page indices."""
    if not spec.strip():
        return list(range(total))

    pages = set()
    for part in spec.split(","):
        part = part.strip()
        if "-" in part:
            start, end = part.split("-", 1)
            s = max(1, int(start.strip()))
            e = min(total, int(end.strip()))
            pages.update(range(s - 1, e))
        else:
            p = int(part.strip()) - 1
            if 0 <= p < total:
                pages.add(p)
    return sorted(pages)


def parse_page_groups(spec: str, total: int) -> list[tuple[str, int, int]]:
    """Parse '1-3, 5, 7-10' into list of (name, start_idx, end_idx)"""
    if not spec.strip():
        return [(str(i + 1), i, i) for i in range(total)]

    groups = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            start, end = part.split("-", 1)
            s = max(1, int(start.strip()))
            e = min(total, int(end.strip()))
            if s <= e:
                groups.append((f"{s}-{e}", s - 1, e - 1))
        else:
            p = int(part.strip()) - 1
            if 0 <= p < total:
                groups.append((str(p + 1), p, p))
    return groups


PAPER_SIZES = {
    "a4": (595.28, 841.89),
    "letter": (612, 792),
    "a3": (841.89, 1190.55),
    "a5": (419.53, 595.28),
    "legal": (612, 1008),
}


@bp.route("/merge", methods=["POST"])
def merge():
    files = request.files.getlist("files")
    if len(files) < 2:
        return jsonify(error="Please upload at least 2 PDF files."), 400

    result = fitz.open()
    for f in files:
        try:
            doc = fitz.open(stream=f.read(), filetype="pdf")
            result.insert_pdf(doc)
            doc.close()
        except Exception as e:
            return jsonify(error=str(e)), 500

    output = io.BytesIO()
    result.save(output)
    result.close()
    output.seek(0)
    return send_file(output, mimetype="application/pdf",
                     as_attachment=True, download_name="merged.pdf")


@bp.route("/split", methods=["POST"])
def split():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    page_spec = request.form.get("pages", "").strip()
    doc = fitz.open(stream=files[0].read(), filetype="pdf")

    try:
        groups = parse_page_groups(page_spec, len(doc))
    except ValueError:
        return jsonify(error="Invalid page range format."), 400

    if not groups:
        return jsonify(error="No valid pages selected."), 400

    if len(groups) == 1:
        name, start_idx, end_idx = groups[0]
        single = fitz.open()
        single.insert_pdf(doc, from_page=start_idx, to_page=end_idx)
        output = io.BytesIO()
        single.save(output)
        single.close()
        doc.close()
        output.seek(0)
        prefix = "page_" if "-" not in name and name != "all" else "pages_"
        return send_file(output, mimetype="application/pdf",
                         as_attachment=True, download_name=f"{prefix}{name}.pdf")

    parts = []
    for name, start_idx, end_idx in groups:
        part = fitz.open()
        part.insert_pdf(doc, from_page=start_idx, to_page=end_idx)
        buf = io.BytesIO()
        part.save(buf)
        part.close()
        prefix = "page_" if "-" not in name else "pages_"
        parts.append((f"{prefix}{name}.pdf", buf.getvalue()))

    doc.close()
    zip_buf = make_zip(parts)
    return send_file(zip_buf, mimetype="application/zip",
                     as_attachment=True, download_name="split_pages.zip")


@bp.route("/compress", methods=["POST"])
def compress():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    quality = request.form.get("quality", "medium")
    image_quality = {"low": 40, "medium": 65, "high": 85}.get(quality, 65)
    max_dim = {"low": 1000, "medium": 1600, "high": 2500}.get(quality, 1600)

    doc = fitz.open(stream=files[0].read(), filetype="pdf")
    compressed_streams = {}

    for page in doc:
        images = page.get_images(full=True)
        for img_info in images:
            xref = img_info[0]
            try:
                if xref in compressed_streams:
                    page.replace_image(xref, stream=compressed_streams[xref])
                    continue

                base_image = doc.extract_image(xref)
                if not base_image:
                    continue
                
                img_bytes = base_image["image"]
                from PIL import Image
                pil_img = Image.open(io.BytesIO(img_bytes))
                if pil_img.mode in ("RGBA", "P"):
                    pil_img = pil_img.convert("RGB")
                
                w, h = pil_img.size
                if w > max_dim or h > max_dim:
                    ratio = min(max_dim / w, max_dim / h)
                    new_w, new_h = int(w * ratio), int(h * ratio)
                    pil_img = pil_img.resize((new_w, new_h), Image.Resampling.LANCZOS)

                buf = io.BytesIO()
                pil_img.save(buf, format="JPEG", quality=image_quality, optimize=True)
                
                compressed_streams[xref] = buf.getvalue()
                page.replace_image(xref, stream=compressed_streams[xref])
            except Exception:
                continue

    output = io.BytesIO()
    doc.save(output, garbage=4, deflate=True, clean=True)
    doc.close()
    output.seek(0)

    name = files[0].filename.rsplit(".", 1)[0] + "_compressed.pdf"
    return send_file(output, mimetype="application/pdf",
                     as_attachment=True, download_name=name)


@bp.route("/rotate", methods=["POST"])
def rotate():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    angle = int(request.form.get("angle", 90))
    page_spec = request.form.get("pages", "").strip()

    doc = fitz.open(stream=files[0].read(), filetype="pdf")
    pages = parse_page_ranges(page_spec, len(doc))

    for p in pages:
        doc[p].set_rotation((doc[p].rotation + angle) % 360)

    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)

    name = files[0].filename.rsplit(".", 1)[0] + "_rotated.pdf"
    return send_file(output, mimetype="application/pdf",
                     as_attachment=True, download_name=name)


@bp.route("/resize", methods=["POST"])
def resize():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    mode = request.form.get("mode", "scale")
    doc = fitz.open(stream=files[0].read(), filetype="pdf")

    if mode == "scale":
        scale = float(request.form.get("scale", 100)) / 100.0
        for page in doc:
            r = page.rect
            new_rect = fitz.Rect(0, 0, r.width * scale, r.height * scale)
            page.set_mediabox(new_rect)
    elif mode == "paper":
        paper = request.form.get("paper", "a4")
        w, h = PAPER_SIZES.get(paper, PAPER_SIZES["a4"])
        for page in doc:
            page.set_mediabox(fitz.Rect(0, 0, w, h))

    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)

    name = files[0].filename.rsplit(".", 1)[0] + "_resized.pdf"
    return send_file(output, mimetype="application/pdf",
                     as_attachment=True, download_name=name)


@bp.route("/page-numbers", methods=["POST"])
def page_numbers():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    position = request.form.get("position", "bottom-center")
    start = int(request.form.get("start", 1))
    fontsize = int(request.form.get("fontsize", 11))

    doc = fitz.open(stream=files[0].read(), filetype="pdf")

    for i, page in enumerate(doc):
        num = start + i
        r = page.rect
        margin = 36  # 0.5 inch

        pos_map = {
            "bottom-center": fitz.Point(r.width / 2, r.height - margin),
            "bottom-right": fitz.Point(r.width - margin, r.height - margin),
            "bottom-left": fitz.Point(margin, r.height - margin),
            "top-center": fitz.Point(r.width / 2, margin + fontsize),
            "top-right": fitz.Point(r.width - margin, margin + fontsize),
            "top-left": fitz.Point(margin, margin + fontsize),
        }
        point = pos_map.get(position, pos_map["bottom-center"])

        align = 1 if "center" in position else (2 if "right" in position else 0)
        page.insert_text(point, str(num), fontsize=fontsize,
                         fontname="helv", color=(0.3, 0.3, 0.3))

    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)

    name = files[0].filename.rsplit(".", 1)[0] + "_numbered.pdf"
    return send_file(output, mimetype="application/pdf",
                     as_attachment=True, download_name=name)


@bp.route("/extract-images", methods=["POST"])
def extract_images():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    doc = fitz.open(stream=files[0].read(), filetype="pdf")
    images = []

    for i, page in enumerate(doc):
        for img_idx, img_info in enumerate(page.get_images(full=True)):
            xref = img_info[0]
            try:
                base_image = doc.extract_image(xref)
                if not base_image:
                    continue
                ext = base_image.get("ext", "png")
                images.append((f"page{i+1}_img{img_idx+1}.{ext}", base_image["image"]))
            except Exception:
                continue

    doc.close()

    if not images:
        return jsonify(error="No images found in the PDF."), 400

    if len(images) == 1:
        ext = images[0][0].rsplit(".", 1)[1]
        mime = f"image/{'jpeg' if ext in ('jpg','jpeg') else ext}"
        return send_file(io.BytesIO(images[0][1]), mimetype=mime,
                         as_attachment=True, download_name=images[0][0])

    zip_buf = make_zip(images)
    name = files[0].filename.rsplit(".", 1)[0] + "_images.zip"
    return send_file(zip_buf, mimetype="application/zip",
                     as_attachment=True, download_name=name)


@bp.route("/protect", methods=["POST"])
def protect():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    user_pw = request.form.get("user_password", "")
    owner_pw = request.form.get("owner_password", "") or user_pw

    if not user_pw:
        return jsonify(error="Please enter a password."), 400

    doc = fitz.open(stream=files[0].read(), filetype="pdf")
    perm = fitz.PDF_PERM_PRINT | fitz.PDF_PERM_COPY

    output = io.BytesIO()
    doc.save(output,
             encryption=fitz.PDF_ENCRYPT_AES_256,
             user_pw=user_pw,
             owner_pw=owner_pw,
             permissions=perm)
    doc.close()
    output.seek(0)

    name = files[0].filename.rsplit(".", 1)[0] + "_protected.pdf"
    return send_file(output, mimetype="application/pdf",
                     as_attachment=True, download_name=name)


@bp.route("/unlock", methods=["POST"])
def unlock():
    files = request.files.getlist("files")
    if not files or not files[0].filename:
        return jsonify(error="No file uploaded."), 400

    password = request.form.get("password", "")
    pdf_data = files[0].read()

    doc = fitz.open(stream=pdf_data, filetype="pdf")

    if doc.needs_pass:
        if not doc.authenticate(password):
            doc.close()
            return jsonify(error="Incorrect password."), 400

    output = io.BytesIO()
    doc.save(output)
    doc.close()
    output.seek(0)

    name = files[0].filename.rsplit(".", 1)[0] + "_unlocked.pdf"
    return send_file(output, mimetype="application/pdf",
                     as_attachment=True, download_name=name)

@bp.route("/delete", methods=["POST"])
def process_delete():
    f = request.files.get("files")
    pages_str = request.form.get("pages", "").strip()
    if not f or not f.filename or not pages_str:
        return jsonify(error="PDF file and pages to delete are required"), 400
    
    try:
        data = f.read()
        doc = fitz.open(stream=data, filetype="pdf")
        total = len(doc)
        
        groups = parse_page_groups(pages_str, total)
        delete_list = set()
        for g in groups:
            for p in g:
                delete_list.add(int(p))
                
        keep_list = [i for i in range(total) if i not in delete_list]
        if not keep_list:
            return jsonify(error="Cannot delete all pages uniformly, minimum 1 page must remain"), 400
            
        doc.select(keep_list)
        
        output = io.BytesIO()
        doc.save(output)
        doc.close()
        output.seek(0)
        
        return send_file(output, mimetype="application/pdf", as_attachment=True, download_name=f"deleted_{f.filename}")
    except Exception as e:
        return jsonify(error=str(e)), 500

@bp.route("/watermark", methods=["POST"])
def process_watermark():
    f = request.files.get("files")
    text = request.form.get("text", "")
    if not f or not f.filename or not text:
        return jsonify(error="PDF file and watermark text are required"), 400
    
    try:
        color = request.form.get("color", "#ff0000")
        opacity_val = request.form.get("opacity", 30)
        try:
            opacity = float(opacity_val) / 100.0
        except ValueError:
            opacity = 0.3
            
        angle = float(request.form.get("angle", 45))
        size = float(request.form.get("size", 72))
        
        rgb = hex_to_rgb(color)
        
        data = f.read()
        doc = fitz.open(stream=data, filetype="pdf")
        
        for page in doc:
            rect = page.rect
            center = fitz.Point(rect.width / 2, rect.height / 2)
            page.insert_text(center, text, fontsize=size, color=rgb, fill_opacity=opacity, rotate=angle, fontname="helv")
            
        output = io.BytesIO()
        doc.save(output)
        doc.close()
        output.seek(0)
        
        return send_file(output, mimetype="application/pdf", as_attachment=True, download_name=f"watermarked_{f.filename}")
    except Exception as e:
        return jsonify(error=str(e)), 500
