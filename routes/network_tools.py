import subprocess
import platform
from flask import Blueprint, current_app, render_template, request, jsonify

bp = Blueprint("network", __name__)


@bp.route("/ping")
def ping_page():
    return render_template(
        "upload_tool.html",
        title="Cek Ping",
        description="Periksa konektivitas dan latensi jaringan ke nama host atau alamat IP tertentu.",
        endpoint="/network/ping",
        text_input=True,
        text_label="Nama Host atau Alamat IP",
        text_placeholder="misal: google.com atau 8.8.8.8",
        button_text="Jalankan Ping"
    )


@bp.route("/ping", methods=["POST"])
def process_ping():
    hostname = request.form.get("text", "").strip()
    if not hostname:
        return jsonify(error="Please enter a valid hostname or IP address."), 400
    
    # Basic sanitization: refuse command injection characters
    if any(c in hostname for c in [";", "&", "|", "`", "$", "(", ")", ">", "<"]):
        return jsonify(error="Invalid characters in hostname."), 400

    # Determine command based on OS
    param = "-n" if platform.system().lower() == "windows" else "-c"
    
    try:
        # Run ping with 4 packets
        result = subprocess.run(
            ["ping", param, str(current_app.config["PING_COUNT"]), hostname],
            capture_output=True,
            text=True,
            timeout=current_app.config["NETWORK_TIMEOUT_SECONDS"],
        )
        
        # Combine stdout and stderr
        output = result.stdout
        if result.stderr:
            output += "\n" + result.stderr
            
        if not output.strip():
            output = "Command executed but no output was returned."
            
        return jsonify(text=output)
    except subprocess.TimeoutExpired:
        return jsonify(error=f"Ping melebihi batas waktu {current_app.config['NETWORK_TIMEOUT_SECONDS']} detik."), 408
    except Exception as e:
        return jsonify(error=f"Error executing ping: {str(e)}"), 500
