/* ══════════════════════════════════════════════════════════════
   SmartDoc Kolaka — DJP Enterprise Theme JavaScript
   ══════════════════════════════════════════════════════════════ */

/* ── Sidebar ──────────────────────────────────── */
function toggleCategory(btn) {
    const items = btn.nextElementSibling;
    const isOpen = btn.classList.contains("open");

    if (isOpen) {
        // Smooth close
        items.style.maxHeight = items.scrollHeight + "px";
        requestAnimationFrame(() => {
            items.style.maxHeight = "0";
            items.style.opacity = "0";
        });
        setTimeout(() => {
            items.classList.remove("open");
            items.style.maxHeight = "";
            items.style.opacity = "";
        }, 250);
        btn.classList.remove("open");
    } else {
        // Smooth open
        btn.classList.add("open");
        items.classList.add("open");
        items.style.maxHeight = "0";
        items.style.opacity = "0";
        requestAnimationFrame(() => {
            items.style.maxHeight = items.scrollHeight + "px";
            items.style.opacity = "1";
            items.style.transition = "max-height 0.3s ease, opacity 0.25s ease";
        });
        setTimeout(() => {
            items.style.maxHeight = "";
            items.style.opacity = "";
            items.style.transition = "";
        }, 300);
    }
}

function openSidebar() {
    document.getElementById("sidebar").classList.add("open");
    document.getElementById("overlay").classList.add("open");
    document.body.style.overflow = "hidden";
}

function closeSidebar() {
    document.getElementById("sidebar").classList.remove("open");
    document.getElementById("overlay").classList.remove("open");
    document.body.style.overflow = "";
}

/* ── Theme Toggle ─────────────────────────────── */
function toggleTheme() {
    const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
    const newTheme = isDark ? 'light' : 'dark';

    // Smooth transition
    document.documentElement.style.transition = 'background-color 0.3s ease, color 0.3s ease';
    document.documentElement.setAttribute('data-theme', newTheme);
    localStorage.setItem('theme', newTheme);
    updateThemeIcon(newTheme);

    setTimeout(() => {
        document.documentElement.style.transition = '';
    }, 400);
}

function updateThemeIcon(theme) {
    const icon = document.getElementById('theme-icon');
    if (!icon) return;
    icon.className = theme === 'dark' ? 'bi bi-sun-fill' : 'bi bi-moon-fill';
}

// Highlight active nav item & auto-open its category
document.addEventListener("DOMContentLoaded", () => {
    const path = window.location.pathname;
    document.querySelectorAll(".nav-item").forEach(a => {
        if (a.getAttribute("href") === path) {
            a.classList.add("active");
            const items = a.closest(".nav-items");
            if (items) {
                items.classList.add("open");
                const btn = items.previousElementSibling;
                if (btn) btn.classList.add("open");
            }
        }
    });

    initUploadZone();
    initToolForm();
    initDependentOptions();
    initCardAnimations();

    const savedTheme = localStorage.getItem('theme') || (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light');
    updateThemeIcon(savedTheme);
});


/* ── Card Entrance Animations ─────────────────── */
function initCardAnimations() {
    // Only run on pages with tool cards
    const cards = document.querySelectorAll('.tool-card');
    if (cards.length === 0) return;

    // Check for reduced motion preference
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;

    const observer = new IntersectionObserver((entries) => {
        entries.forEach((entry, idx) => {
            if (entry.isIntersecting) {
                // Stagger the animation based on position in viewport
                const card = entry.target;
                const delay = Array.from(cards).indexOf(card) % 4 * 50;
                card.style.transitionDelay = delay + 'ms';
                card.classList.add('card-visible');
                observer.unobserve(card);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -30px 0px'
    });

    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(12px)';
        card.style.transition = 'opacity 0.4s ease, transform 0.4s ease';
        observer.observe(card);
    });
}

// Add style for visible cards
const cardStyle = document.createElement('style');
cardStyle.textContent = `.tool-card.card-visible { opacity: 1 !important; transform: translateY(0) !important; }`;
document.head.appendChild(cardStyle);


/* ── Upload Zone ──────────────────────────────── */
let selectedFiles = [];

function initUploadZone() {
    const zone = document.getElementById("upload-zone");
    const input = document.getElementById("file-input");
    if (!zone || !input) return;

    zone.addEventListener("dragover", e => { e.preventDefault(); zone.classList.add("dragover"); });
    zone.addEventListener("dragleave", () => zone.classList.remove("dragover"));
    zone.addEventListener("drop", e => {
        e.preventDefault();
        zone.classList.remove("dragover");
        addFiles(e.dataTransfer.files);
    });

    input.addEventListener("change", () => {
        addFiles(input.files);
        input.value = "";
    });
}

function addFiles(fileList) {
    const input = document.getElementById("file-input");
    const isMultiple = input && input.hasAttribute("multiple");

    if (isMultiple) {
        selectedFiles.push(...Array.from(fileList));
    } else {
        selectedFiles = [fileList[0]];
    }
    renderFileList();
}

function removeFile(idx) {
    selectedFiles.splice(idx, 1);
    renderFileList();
}

function renderFileList() {
    const list = document.getElementById("file-list");
    const prompt = document.getElementById("upload-prompt");
    if (!list) return;

    if (selectedFiles.length === 0) {
        list.innerHTML = "";
        if (prompt) prompt.style.display = "";
        return;
    }
    if (prompt) prompt.style.display = "none";

    list.innerHTML = selectedFiles.map((f, i) => `
        <div class="file-item">
            <span><i class="bi bi-file-earmark"></i> ${f.name}
            <small>(${formatSize(f.size)})</small></span>
            <button type="button" class="remove-file" onclick="removeFile(${i})">&times;</button>
        </div>
    `).join("");
}

function formatSize(bytes) {
    if (bytes < 1024) return bytes + " B";
    if (bytes < 1048576) return (bytes / 1024).toFixed(1) + " KB";
    return (bytes / 1048576).toFixed(1) + " MB";
}


/* ── Form Submission ──────────────────────────── */
function initToolForm() {
    const form = document.getElementById("tool-form");
    if (!form) return;

    form.addEventListener("submit", async (e) => {
        e.preventDefault();
        const endpoint = form.dataset.endpoint;
        if (!endpoint) return;

        const btnText = document.querySelector(".btn-text");
        const btnLoad = document.querySelector(".btn-loading");
        const submitBtn = document.getElementById("submit-btn");
        const resultArea = document.getElementById("result-area");

        // Validate: either files or text input required
        const textInput = form.querySelector("textarea[name='text']");
        if (!textInput && selectedFiles.length === 0) {
            showError(t("error.no_file"));
            return;
        }
        if (textInput && !textInput.value.trim()) {
            showError(t("error.no_text"));
            return;
        }

        // Show loading
        if (btnText) btnText.style.display = "none";
        if (btnLoad) btnLoad.style.display = "inline-flex";
        submitBtn.disabled = true;
        resultArea.style.display = "none";

        const formData = new FormData(form);

        // Remove the empty file input and add our tracked files
        formData.delete("files");
        selectedFiles.forEach(f => formData.append("files", f));

        try {
            const resp = await fetch(endpoint, { method: "POST", body: formData });

            if (!resp.ok) {
                let msg = t("error.processing_failed");
                try {
                    const json = await resp.json();
                    msg = json.error || msg;
                } catch (_) {}
                showError(msg);
                return;
            }

            const ct = resp.headers.get("Content-Type") || "";

            if (ct.includes("application/json")) {
                const json = await resp.json();
                if (json.error) {
                    showError(json.error);
                } else if (json.text !== undefined) {
                    showTextResult(json.text);
                } else if (json.data !== undefined) {
                    showTextResult(typeof json.data === "string" ? json.data : JSON.stringify(json.data, null, 2));
                }
            } else {
                // Binary file download
                const blob = await resp.blob();
                const cd = resp.headers.get("Content-Disposition") || "";
                let filename = "download";
                const match = cd.match(/filename="?([^";\n]+)"?/);
                if (match) filename = match[1];

                const url = URL.createObjectURL(blob);

                // If image, show preview
                if (ct.startsWith("image/")) {
                    showFileResult(url, filename, true);
                } else {
                    showFileResult(url, filename, false);
                }
            }
        } catch (err) {
            showError(t("error.network") + err.message);
        } finally {
            if (btnText) btnText.style.display = "";
            if (btnLoad) btnLoad.style.display = "none";
            submitBtn.disabled = false;
        }
    });
}

function showError(msg) {
    const area = document.getElementById("result-area");
    area.style.display = "block";
    document.getElementById("result-success").style.display = "none";
    document.getElementById("result-text")?.style.setProperty("display", "none");
    const errEl = document.getElementById("result-error");
    errEl.style.display = "flex";
    document.getElementById("error-message").textContent = msg;
}

function showFileResult(url, filename, isImage) {
    const area = document.getElementById("result-area");
    area.style.display = "block";
    document.getElementById("result-error").style.display = "none";
    document.getElementById("result-text")?.style.setProperty("display", "none");

    const success = document.getElementById("result-success");
    success.style.display = "flex";
    document.getElementById("result-message").textContent = t("result.file_ready");

    const btn = document.getElementById("download-btn");
    btn.href = url;
    btn.download = filename;
    btn.textContent = "";
    btn.innerHTML = '<i class="bi bi-download"></i> ' + t("result.download") + ' ' + filename;

    const preview = document.getElementById("result-preview");
    if (isImage) {
        preview.style.display = "block";
        preview.innerHTML = `<img src="${url}" alt="Preview">`;
    } else {
        preview.style.display = "none";
    }
}

function showTextResult(text) {
    const area = document.getElementById("result-area");
    area.style.display = "block";
    document.getElementById("result-error").style.display = "none";
    document.getElementById("result-success").style.display = "none";

    const textBox = document.getElementById("result-text");
    if (textBox) {
        textBox.style.display = "block";
        document.getElementById("result-text-content").textContent = text;
    }
}

function copyResult() {
    const text = document.getElementById("result-text-content")?.textContent;
    if (text) {
        navigator.clipboard.writeText(text);
        // Visual feedback
        const btn = event.target.closest('.btn');
        if (btn) {
            const original = btn.innerHTML;
            btn.innerHTML = '<i class="bi bi-check2"></i> ' + t("result.copied");
            btn.style.color = 'var(--success)';
            setTimeout(() => {
                btn.innerHTML = original;
                btn.style.color = '';
            }, 1500);
        }
    }
}


/* ── Dependent Options ────────────────────────── */
function initDependentOptions() {
    document.querySelectorAll("[data-depends-on]").forEach(el => {
        const parentName = el.dataset.dependsOn;
        const requiredVal = el.dataset.dependsValue;
        const parentInput = document.querySelector(`[name="${parentName}"]`);
        if (!parentInput) return;

        const check = () => {
            // Support comma-separated values
            const vals = requiredVal.split(",");
            el.style.display = vals.includes(parentInput.value) ? "" : "none";
        };
        parentInput.addEventListener("change", check);
        check();
    });
}
