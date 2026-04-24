const TRANSLATIONS = {
    en: {
        "nav.history": "Activity History",
        "nav.favorites": "Favorites & Recent",
        "nav.toggle_theme": "Toggle Theme",
        "nav.switch_lang": "Indonesia",
        
        "cat.convert": "Document Conversion",
        "cat.pdf": "PDF Tools",
        "cat.spreadsheet": "Spreadsheet",
        "cat.image": "Image Tools",
        "cat.text": "Text & Data",
        "cat.calc": "Calculators",
        "cat.qr": "QR Code",
        "cat.security": "Security",
        "cat.network": "Network Tools",
        
        "tool.convert.to-pdf": "Files to PDF",
        "tool.convert.pdf-to-word": "PDF to Word",
        "tool.convert.pdf-to-excel": "PDF to Excel",
        "tool.convert.pdf-to-images": "PDF to Images",
        "tool.convert.pdf-to-text": "PDF to Text",
        "tool.convert.html-to-pdf": "HTML to PDF",
        "tool.convert.ocr-pdf": "OCR PDF",
        "tool.convert.cad-to-pdf": "CAD to PDF/Image",
        
        "tool.pdf.merge": "Merge PDFs",
        "tool.pdf.split": "Split PDF",
        "tool.pdf.delete": "Delete Pages",
        "tool.pdf.compress": "Compress PDF",
        "tool.pdf.rotate": "Rotate PDF",
        "tool.pdf.resize": "Resize PDF",
        "tool.pdf.page-numbers": "Page Numbers",
        "tool.pdf.extract-images": "Extract Images",
        "tool.pdf.watermark": "PDF Watermark",
        "tool.pdf.protect": "Protect PDF",
        "tool.pdf.unlock": "Unlock PDF",
        
        "tool.spreadsheet.excel-to-csv": "Excel to CSV/JSON",
        "tool.spreadsheet.csv-to-excel": "CSV/JSON to Excel",
        "tool.spreadsheet.excel-to-pdf": "Excel to PDF",
        "tool.spreadsheet.merge": "Merge Workbooks",
        "tool.spreadsheet.split": "Split Sheets",
        "tool.spreadsheet.info": "Excel Info & Preview",
        
        "tool.image.resize": "Resize Image",
        "tool.image.compress": "Compress Image",
        "tool.image.convert": "Convert Format",
        "tool.image.remove-bg": "Remove Background",
        "tool.image.crop": "Crop Image",
        "tool.image.rotate": "Rotate / Flip",
        "tool.image.watermark": "Add Watermark",
        "tool.image.exif": "EXIF Viewer",
        "tool.image.favicon": "Favicon Generator",
        "tool.image.ocr": "Image to Text",
        "tool.image.animated": "Animated WebP/GIF",
        
        "tool.text.json-formatter": "JSON Formatter",
        "tool.text.csv-json": "CSV / JSON",
        "tool.text.base64": "Base64",
        "tool.text.url-encode": "URL Encode",
        "tool.text.word-counter": "Word Counter",
        "tool.text.markdown": "Markdown Preview",
        "tool.text.case-converter": "Case Converter",
        "tool.text.text-diff": "Text Diff",
        "tool.text.regex-tester": "Regex Tester",
        "tool.text.slug-generator": "Slug Generator",
        "tool.text.json-yaml": "JSON / YAML",
        "tool.text.lorem-ipsum": "Lorem Ipsum",
        
        "tool.calc.calculator": "Calculator",
        "tool.calc.unit-converter": "Unit Converter",
        "tool.calc.color-converter": "Color Converter",
        "tool.calc.percentage": "Percentage Calc",
        "tool.calc.date": "Date Calculator",
        "tool.calc.timestamp": "Timestamp",
        "tool.calc.number-base": "Number Base",
        "tool.calc.pomodoro": "Pomodoro Timer",
        
        "tool.qr.generate": "Generate QR",
        "tool.qr.read": "Read QR",
        
        "tool.security.password-generator": "Password Generator",
        "tool.security.hash-generator": "Hash Generator",
        "tool.security.system-check": "System Check",
        
        "tool.network.ping": "Ping Test",
        
        "desc.convert.to-pdf": "Convert images and text files to PDF",
        "desc.convert.pdf-to-word": "Convert PDF to Word document",
        "desc.convert.pdf-to-excel": "Extract PDF tabular data to Excel",
        "desc.convert.pdf-to-images": "Convert PDF pages to images",
        "desc.convert.pdf-to-text": "Extract text content from PDF",
        "desc.convert.html-to-pdf": "Convert HTML content to PDF",
        "desc.convert.ocr-pdf": "Make scanned PDFs searchable or extract text",
        "desc.convert.cad-to-pdf": "Convert DXF/DWG drawings to PDF or PNG",
        "desc.pdf.merge": "Combine multiple PDFs into one",
        "desc.pdf.split": "Split PDF into individual pages",
        "desc.pdf.delete": "Remove specific pages from PDF",
        "desc.pdf.compress": "Reduce PDF file size",
        "desc.pdf.rotate": "Rotate PDF pages",
        "desc.pdf.resize": "Change PDF page dimensions",
        "desc.pdf.page-numbers": "Add page numbers to PDF",
        "desc.pdf.extract-images": "Extract images from PDF",
        "desc.pdf.watermark": "Add text watermark to PDF documents",
        "desc.pdf.protect": "Add password protection to PDF",
        "desc.pdf.unlock": "Remove PDF password",
        "desc.spreadsheet.excel-to-csv": "Export sheets as CSV or JSON",
        "desc.spreadsheet.csv-to-excel": "Build .xlsx from CSV or JSON files",
        "desc.spreadsheet.excel-to-pdf": "Convert workbook to PDF (one section per sheet)",
        "desc.spreadsheet.merge": "Combine multiple Excel files into one",
        "desc.spreadsheet.split": "Export each sheet as its own .xlsx",
        "desc.spreadsheet.info": "List sheets, counts, and preview rows",
        "desc.image.resize": "Resize by percentage or dimensions",
        "desc.image.compress": "Reduce image file size",
        "desc.image.convert": "Convert between image formats",
        "desc.image.remove-bg": "Remove image background",
        "desc.image.crop": "Crop images to specific dimensions",
        "desc.image.rotate": "Rotate or flip images",
        "desc.image.watermark": "Add text watermark to images",
        "desc.image.exif": "View and strip image metadata",
        "desc.image.favicon": "Create .ico favicons from images",
        "desc.image.ocr": "Extract text from images (OCR)",
        "desc.image.animated": "Convert between animated WebP and GIF",
        "desc.text.json-formatter": "Format and validate JSON",
        "desc.text.csv-json": "Convert between CSV and JSON",
        "desc.text.base64": "Encode and decode Base64",
        "desc.text.url-encode": "Encode and decode URLs",
        "desc.text.word-counter": "Count words, characters, sentences",
        "desc.text.markdown": "Preview Markdown as HTML",
        "desc.text.case-converter": "Convert text between cases",
        "desc.text.text-diff": "Compare two texts side by side",
        "desc.text.regex-tester": "Test regular expressions live",
        "desc.text.slug-generator": "Create URL-friendly slugs",
        "desc.text.json-yaml": "Convert between JSON and YAML",
        "desc.text.lorem-ipsum": "Generate placeholder text",
        "desc.calc.calculator": "Basic and scientific calculator",
        "desc.calc.unit-converter": "Convert between units of measurement",
        "desc.calc.color-converter": "Convert HEX, RGB, HSL colors",
        "desc.calc.percentage": "Calculate percentages easily",
        "desc.calc.date": "Calculate date differences",
        "desc.calc.timestamp": "Convert Unix timestamps",
        "desc.calc.number-base": "Convert between number bases",
        "desc.calc.pomodoro": "Focus timer with breaks",
        "desc.qr.generate": "Create QR codes from text or URLs",
        "desc.qr.read": "Decode QR codes from images",
        "desc.security.password-generator": "Generate strong random passwords",
        "desc.security.hash-generator": "Generate MD5, SHA hashes",
        "desc.security.system-check": "Inspect local readiness, optional dependencies, and autostart status",
        "desc.network.ping": "Check network connectivity and latency",
        
        "home.title": "SmartDoc Kolaka",
        "home.subtitle": "Digital Utility System — KPP Pratama Kolaka",
        
        "upload.drag": "Drag & drop file(s) here",
        "upload.browse": "or click to browse",
        "upload.process": "Process",
        "upload.processing": "Processing...",
        
        "result.done": "Done!",
        "result.file_ready": "File ready!",
        "result.download": "Download",
        "result.copy": "Copy",
        "result.copied": "Copied!",
        "result.result": "Result",
        
        "history.title": "Activity History",
        "history.desc": "Live audit log of processed tasks and system utility usage.",
        "history.clear": "Clear All",
        "history.confirm": "Are you sure you want to clear all history? This cannot be undone.",
        "history.empty": "No activity recorded yet. Process a PDF or Image to see logs here!",
        "history.col.id": "ID",
        "history.col.time": "Timestamp",
        "history.col.tool": "Tool Endpoint",
        "history.col.status": "Status",
        
        "fav.title": "My Favorites",
        "fav.subtitle": "Quick access to your most frequently used utilities.",
        "fav.empty": "You don't have any favorite tools yet.",
        "fav.empty_hint": "Click the star icon (★) on any tool to add it here.",
        "fav.recent_title": "Recently Used",
        "fav.recent_empty": "No recent tool usage on this device yet.",
        
        "error.no_file": "Please select a file first.",
        "error.no_text": "Please enter some text.",
        "error.processing_failed": "Processing failed.",
        "error.network": "Network error: "
    },
    id: {
        "nav.history": "Riwayat Log",
        "nav.favorites": "Favorit & Recent",
        "nav.toggle_theme": "Ubah Tema",
        "nav.switch_lang": "English",
        
        "cat.convert": "Konversi Dokumen",
        "cat.pdf": "Alat PDF",
        "cat.spreadsheet": "Lembar Kerja",
        "cat.image": "Alat Gambar",
        "cat.text": "Teks & Data",
        "cat.calc": "Kalkulator",
        "cat.qr": "Kode QR",
        "cat.security": "Keamanan",
        "cat.network": "Alat Jaringan",
        
        "tool.convert.to-pdf": "File ke PDF",
        "tool.convert.pdf-to-word": "PDF ke Word",
        "tool.convert.pdf-to-excel": "PDF ke Excel",
        "tool.convert.pdf-to-images": "PDF ke Gambar",
        "tool.convert.pdf-to-text": "PDF ke Teks",
        "tool.convert.html-to-pdf": "HTML ke PDF",
        "tool.convert.ocr-pdf": "OCR PDF",
        "tool.convert.cad-to-pdf": "CAD ke PDF/Gambar",
        
        "tool.pdf.merge": "Gabung PDF",
        "tool.pdf.split": "Pisah PDF",
        "tool.pdf.delete": "Hapus Halaman",
        "tool.pdf.compress": "Kompres PDF",
        "tool.pdf.rotate": "Putar PDF",
        "tool.pdf.resize": "Ubah Ukuran PDF",
        "tool.pdf.page-numbers": "Nomor Halaman",
        "tool.pdf.extract-images": "Ekstrak Gambar",
        "tool.pdf.watermark": "Tanda Air PDF",
        "tool.pdf.protect": "Lindungi PDF",
        "tool.pdf.unlock": "Buka Kunci PDF",
        
        "tool.spreadsheet.excel-to-csv": "Excel ke CSV/JSON",
        "tool.spreadsheet.csv-to-excel": "CSV/JSON ke Excel",
        "tool.spreadsheet.excel-to-pdf": "Excel ke PDF",
        "tool.spreadsheet.merge": "Gabung Lembar Kerja",
        "tool.spreadsheet.split": "Pisah Lembar Kerja",
        "tool.spreadsheet.info": "Info & Pratinjau Excel",
        
        "tool.image.resize": "Ubah Ukuran Gambar",
        "tool.image.compress": "Kompres Gambar",
        "tool.image.convert": "Konversi Format",
        "tool.image.remove-bg": "Hapus Latar Belakang",
        "tool.image.crop": "Potong Gambar",
        "tool.image.rotate": "Putar / Balik",
        "tool.image.watermark": "Tambah Tanda Air",
        "tool.image.exif": "Penampil EXIF",
        "tool.image.favicon": "Pembuat Favicon",
        "tool.image.ocr": "Gambar ke Teks",
        "tool.image.animated": "Animasi WebP/GIF",
        
        "tool.text.json-formatter": "Pemformat JSON",
        "tool.text.csv-json": "CSV / JSON",
        "tool.text.base64": "Base64",
        "tool.text.url-encode": "URL Encode",
        "tool.text.word-counter": "Penghitung Kata",
        "tool.text.markdown": "Pratinjau Markdown",
        "tool.text.case-converter": "Pengubah Huruf",
        "tool.text.text-diff": "Bandingkan Teks",
        "tool.text.regex-tester": "Penguji Regex",
        "tool.text.slug-generator": "Pembuat Slug",
        "tool.text.json-yaml": "JSON / YAML",
        "tool.text.lorem-ipsum": "Lorem Ipsum",
        
        "tool.calc.calculator": "Kalkulator",
        "tool.calc.unit-converter": "Konversi Satuan",
        "tool.calc.color-converter": "Konversi Warna",
        "tool.calc.percentage": "Kalkulator Persen",
        "tool.calc.date": "Kalkulator Tanggal",
        "tool.calc.timestamp": "Stempel Waktu",
        "tool.calc.number-base": "Basis Angka",
        "tool.calc.pomodoro": "Pengatur Waktu Pomodoro",
        
        "tool.qr.generate": "Buat QR",
        "tool.qr.read": "Baca QR",
        
        "tool.security.password-generator": "Pembuat Kata Sandi",
        "tool.security.hash-generator": "Pembuat Hash",
        "tool.security.system-check": "Pemeriksaan Sistem",
        
        "tool.network.ping": "Cek Ping",
        
        "desc.convert.to-pdf": "Konversi gambar dan teks ke PDF",
        "desc.convert.pdf-to-word": "Konversi PDF ke dokumen Word",
        "desc.convert.pdf-to-excel": "Ekstrak data tabel PDF ke Excel",
        "desc.convert.pdf-to-images": "Konversi halaman PDF ke gambar",
        "desc.convert.pdf-to-text": "Ekstrak konten teks dari PDF",
        "desc.convert.html-to-pdf": "Konversi konten HTML ke PDF",
        "desc.convert.ocr-pdf": "Buat PDF pindaian dapat dicari atau ekstrak teks",
        "desc.convert.cad-to-pdf": "Konversi gambar DXF/DWG ke PDF atau PNG",
        "desc.pdf.merge": "Gabungkan beberapa PDF menjadi satu",
        "desc.pdf.split": "Pisahkan PDF menjadi halaman individu",
        "desc.pdf.delete": "Hapus halaman tertentu dari PDF",
        "desc.pdf.compress": "Kurangi ukuran file PDF",
        "desc.pdf.rotate": "Putar halaman PDF",
        "desc.pdf.resize": "Ubah dimensi halaman PDF",
        "desc.pdf.page-numbers": "Tambahkan nomor halaman ke PDF",
        "desc.pdf.extract-images": "Ekstrak gambar dari PDF",
        "desc.pdf.watermark": "Tambahkan tanda air teks ke dokumen PDF",
        "desc.pdf.protect": "Tambahkan perlindungan kata sandi ke PDF",
        "desc.pdf.unlock": "Hapus kata sandi PDF",
        "desc.spreadsheet.excel-to-csv": "Ekspor lembar sebagai CSV atau JSON",
        "desc.spreadsheet.csv-to-excel": "Buat .xlsx dari file CSV atau JSON",
        "desc.spreadsheet.excel-to-pdf": "Konversi buku kerja ke PDF (satu bagian per lembar)",
        "desc.spreadsheet.merge": "Gabungkan beberapa file Excel menjadi satu",
        "desc.spreadsheet.split": "Ekspor setiap lembar sebagai .xlsx tersendiri",
        "desc.spreadsheet.info": "Cantumkan lembar, hitung, dan pratinjau baris",
        "desc.image.resize": "Ubah ukuran berdasarkan persentase atau dimensi",
        "desc.image.compress": "Kurangi ukuran file gambar",
        "desc.image.convert": "Konversi antar format gambar",
        "desc.image.remove-bg": "Hapus latar belakang gambar",
        "desc.image.crop": "Potong gambar ke dimensi tertentu",
        "desc.image.rotate": "Putar atau balikkan gambar",
        "desc.image.watermark": "Tambahkan tanda air teks ke gambar",
        "desc.image.exif": "Lihat dan hapus metadata gambar",
        "desc.image.favicon": "Buat favicon .ico dari gambar",
        "desc.image.ocr": "Ekstrak teks dari gambar (OCR)",
        "desc.image.animated": "Konversi antara WebP animasi dan GIF",
        "desc.text.json-formatter": "Format dan validasi JSON",
        "desc.text.csv-json": "Konversi antara CSV dan JSON",
        "desc.text.base64": "Enkode dan dekode Base64",
        "desc.text.url-encode": "Enkode dan dekode URL",
        "desc.text.word-counter": "Hitung kata, karakter, kalimat",
        "desc.text.markdown": "Pratinjau Markdown sebagai HTML",
        "desc.text.case-converter": "Ubah huruf teks",
        "desc.text.text-diff": "Bandingkan dua teks berdampingan",
        "desc.text.regex-tester": "Uji ekspresi reguler secara langsung",
        "desc.text.slug-generator": "Buat slug ramah URL",
        "desc.text.json-yaml": "Konversi antara JSON dan YAML",
        "desc.text.lorem-ipsum": "Buat teks placeholder",
        "desc.calc.calculator": "Kalkulator dasar dan ilmiah",
        "desc.calc.unit-converter": "Konversi antar satuan ukuran",
        "desc.calc.color-converter": "Konversi warna HEX, RGB, HSL",
        "desc.calc.percentage": "Hitung persentase dengan mudah",
        "desc.calc.date": "Hitung perbedaan tanggal",
        "desc.calc.timestamp": "Konversi stempel waktu Unix",
        "desc.calc.number-base": "Konversi antar basis angka",
        "desc.calc.pomodoro": "Pengatur waktu fokus dengan istirahat",
        "desc.qr.generate": "Buat kode QR dari teks atau URL",
        "desc.qr.read": "Pecahkan kode QR dari gambar",
        "desc.security.password-generator": "Buat kata sandi acak yang kuat",
        "desc.security.hash-generator": "Buat hash MD5, SHA",
        "desc.security.system-check": "Periksa kesiapan lokal, dependency opsional, dan status autostart",
        "desc.network.ping": "Periksa konektivitas dan latensi jaringan",
        
        "home.title": "SmartDoc Kolaka",
        "home.subtitle": "Sistem Utilitas Digital — KPP Pratama Kolaka",
        
        "upload.drag": "Seret & lepas file di sini",
        "upload.browse": "atau klik untuk memilih",
        "upload.process": "Proses",
        "upload.processing": "Memproses...",
        
        "result.done": "Selesai!",
        "result.file_ready": "File siap!",
        "result.download": "Unduh",
        "result.copy": "Salin",
        "result.copied": "Tersalin!",
        "result.result": "Hasil",
        
        "history.title": "Riwayat Aktivitas",
        "history.desc": "Catatan audit langsung dari tugas yang diproses dan penggunaan utilitas sistem.",
        "history.clear": "Hapus Semua",
        "history.confirm": "Apakah Anda yakin ingin menghapus semua riwayat? Ini tidak dapat dibatalkan.",
        "history.empty": "Belum ada aktivitas tercatat. Proses PDF atau Gambar untuk melihat riwayat di sini!",
        "history.col.id": "ID",
        "history.col.time": "Waktu",
        "history.col.tool": "Endpoint Alat",
        "history.col.status": "Status",
        
        "fav.title": "Favorit Saya",
        "fav.subtitle": "Akses cepat ke utilitas yang paling sering Anda gunakan.",
        "fav.empty": "Anda belum memiliki tool favorit.",
        "fav.empty_hint": "Klik ikon bintang (★) pada tool mana saja untuk menambahkannya ke sini.",
        "fav.recent_title": "Terakhir Digunakan",
        "fav.recent_empty": "Belum ada riwayat penggunaan tool di perangkat ini.",
        
        "error.no_file": "Silakan pilih file terlebih dahulu.",
        "error.no_text": "Silakan masukkan teks.",
        "error.processing_failed": "Pemrosesan gagal.",
        "error.network": "Kesalahan jaringan: "
    }
};

let currentLang = localStorage.getItem("lang") || "en";

function t(key) {
    if (TRANSLATIONS[currentLang] && TRANSLATIONS[currentLang][key] !== undefined) {
        return TRANSLATIONS[currentLang][key];
    }
    if (TRANSLATIONS["en"] && TRANSLATIONS["en"][key] !== undefined) {
        return TRANSLATIONS["en"][key];
    }
    return key;
}

function applyLanguage() {
    document.querySelectorAll("[data-i18n]").forEach(el => {
        const key = el.getAttribute("data-i18n");
        const translation = t(key);
        if (translation !== key) {
            el.innerHTML = translation;
        }
    });
    
    // Also support data-i18n-text to only change text content safely
    document.querySelectorAll("[data-i18n-text]").forEach(el => {
        const key = el.getAttribute("data-i18n-text");
        const translation = t(key);
        if (translation !== key) {
            el.textContent = translation;
        }
    });

    document.querySelectorAll("[data-i18n-placeholder]").forEach(el => {
        const key = el.getAttribute("data-i18n-placeholder");
        const translation = t(key);
        if (translation !== key) {
            el.setAttribute("placeholder", translation);
        }
    });

    document.querySelectorAll("[data-i18n-title]").forEach(el => {
        const key = el.getAttribute("data-i18n-title");
        const translation = t(key);
        if (translation !== key) {
            el.setAttribute("title", translation);
        }
    });
    
    // Update the HTML lang attribute
    document.documentElement.lang = currentLang;
}

function toggleLanguage() {
    currentLang = currentLang === "en" ? "id" : "en";
    localStorage.setItem("lang", currentLang);
    applyLanguage();
}

document.addEventListener("DOMContentLoaded", () => {
    applyLanguage();
});
