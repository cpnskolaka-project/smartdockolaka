```markdown
# Panduan Instalasi Aplikasi SmartDoc Kolaka
**(Khusus Komputer / Laptop Windows)**

Panduan ini akan membantu Anda menginstal dan menjalankan aplikasi **SmartDoc Kolaka** di komputer operasional KPP Pratama Kolaka. Setelah terinstal, aplikasi ini dapat digunakan secara penuh tanpa memerlukan koneksi internet (*Offline*).

**Beberapa hal yang perlu diketahui:**
- Aplikasi berjalan secara lokal di komputer (pada alamat `127.0.0.1`) dan tidak memerlukan akses internet untuk pemakaian sehari-hari.
- Keamanan data terjamin: Riwayat aktivitas disimpan dalam mode privasi. Nama file dan isi teks di dalamnya tidak akan dicatat oleh sistem.
- Agar kinerja komputer tetap ringan dan stabil, aplikasi ini membatasi ukuran file, jumlah halaman PDF, resolusi (DPI) OCR, dan ukuran gambar yang diproses.
- **Penting:** Komputer harus tersambung ke internet *hanya* pada saat instalasi pertama untuk mengunduh komponen pendukung. Setelah selesai, aplikasi siap dipakai *offline*.

---

## Tahap 1: Menginstal Python (Wajib)
Aplikasi ini membutuhkan bahasa pemrograman Python untuk bisa berjalan. Jika komputer belum pernah dipasangi Python, ikuti langkah instalasi otomatis (*Silent Install*) berikut:

1. Buka folder instalasi yang berisi file *installer* bernama `python-3.12.10-amd64.exe`.
2. **Jangan diklik ganda (*Double Click*)!** Arahkan kursor ke kolom alamat folder (*address bar*) di bagian atas, ketik **`cmd`**, lalu tekan `[ENTER]`. Jendela Terminal hitam (Command Prompt) akan terbuka.
3. *Copy* dan *paste* perintah di bawah ini ke dalam jendela hitam tersebut, lalu tekan `[ENTER]`:
   ```bash
   python-3.12.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
   ```
   *(Catatan: Perintah ini akan menginstal Python di latar belakang tanpa harus repot menekan 'Next', berlaku untuk semua pengguna di PC tersebut, dan otomatis mendaftarkannya ke sistem).*

## Tahap 2: Cek Hasil Instalasi Python
Setelah menjalankan perintah di atas, tunggu sekitar 1-2 menit (memang tidak akan ada notifikasi apa-apa di layar). Setelah itu:

1. Di jendela Terminal hitam yang sama *(atau jika sudah tertutup, buka CMD baru)*, ketik perintah ini dan tekan `[ENTER]`:
   ```bash
   python --version
   ```
2. Jika muncul tulisan `Python 3.12.10`, instalasi berhasil. Silakan tutup jendela Terminal hitam tersebut.

## Tahap 3: Menjalankan Aplikasi SmartDoc
Setelah Python terinstal, saatnya menjalankan aplikasinya!

1. Cari file bernama **`run_windows.bat`** (biasanya berlogo ikon gir/gear atau bertipe *Windows Batch File*) di dalam folder aplikasi ini.
2. **Klik Ganda (*Double Click*)** pada file tersebut. Untuk PC baru, cukup gunakan file ini untuk semua keperluan.
3. Sistem akan memproses secara otomatis, meliputi:
   - Membuat ruang khusus aplikasi (*virtual environment*).
   - Mengunduh dan menginstal komponen dari internet (hanya pada instalasi pertama).
   - Menawarkan opsi *autostart* (agar aplikasi jalan otomatis saat PC dinyalakan).
   - Membuka aplikasi secara otomatis di browser Anda.
4. **Perhatian:** Jangan menutup jendela Terminal hitam yang muncul selama aplikasi digunakan. Jika jendela itu ditutup (klik tanda silang [X]), maka aplikasi akan ikut berhenti.
5. Anda bisa langsung menggunakan aplikasi melalui browser (Chrome/Edge) dengan membuka alamat: **`http://127.0.0.1:5050`**

### Menu Pilihan saat Menjalankan Aplikasi

Saat Anda mengklik `run_windows.bat`, Anda akan disuguhkan beberapa menu:

1. **Jalankan aplikasi:** Pilih opsi ini untuk pemakaian sehari-hari.
2. **Install dependency sekarang:** Mengecek dan menginstal komponen yang kurang (membutuhkan internet).
3. **Reinstall dependency:** Menginstal ulang seluruh komponen pendukung (membutuhkan internet).
4. **Repair instalasi:** Opsi perbaikan jika aplikasi mendadak *error*. Sistem akan mereset ulang pengaturan aplikasi dari awal (membutuhkan internet).
5. **Atur ulang autostart:** Memunculkan kembali opsi pengaturan untuk menyalakan aplikasi secara otomatis.

*(Tips: Gunakan opsi **Repair instalasi** jika aplikasi tiba-tiba gagal berjalan di PC tertentu, asalkan file di dalam foldernya masih utuh).*

## Tahap 4: Mengatur Autostart (Aplikasi Jalan Otomatis)
Jika aplikasi ini diinstal pada komputer di area pelayanan terpadu yang rutin dimatikan setiap jam pulang, sangat disarankan untuk mengaktifkan fitur *Autostart*. Dengan begitu, saat komputer dinyalakan keesokan paginya, aplikasi sudah otomatis siap digunakan.

1. Saat pertama kali menjalankan **`run_windows.bat`**, ketik `Y` saat ditanya apakah ingin mengaktifkan *autostart*.
2. Sistem akan otomatis membuat *shortcut* agar aplikasi langsung berjalan saat Windows mulai menyala.
3. Jika pada awalnya Anda memilih `N` (Tidak), fitur ini masih bisa diaktifkan kapan saja. Caranya: hapus file bernama `.autostart_windows` yang ada di dalam folder, lalu jalankan lagi file **`run_windows.bat`**.

---
*Dibuat khusus untuk optimalisasi alat kerja di Lingkungan Direktorat Jenderal Pajak RI.*
```