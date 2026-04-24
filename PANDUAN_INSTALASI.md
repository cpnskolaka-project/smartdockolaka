# PANDUAN INSTALASI APLIKASI SMARTDOC KOLAKA
**(Khusus Komputer / Laptop Windows)**

Dokumen ini berisi panduan lengkap langkah demi langkah untuk menginstal dan menjalankan aplikasi **SmartDoc Kolaka** di komputer operasional KPP Pratama Kolaka secara lokal tanpa memerlukan akses internet (*Offline*).

Catatan tahap 1:
- Aplikasi berjalan lokal pada `127.0.0.1` dan tidak membuka akses keluar secara default untuk aset antarmuka utama.
- Riwayat aktivitas disimpan dalam mode privasi, sehingga nama file dan isi teks mentah tidak dicatat secara default.
- Beberapa tool memiliki batas ukuran file, jumlah halaman PDF, DPI OCR, dan ukuran gambar agar aplikasi tetap stabil di komputer operasional.
- Instalasi pertama membutuhkan koneksi internet untuk memasang dependency Python. Setelah selesai, aplikasi dapat digunakan secara offline.

---

## TAHAP 1: Instalasi Mesin Python (Wajib)
Aplikasi ini diotaki oleh mesin *Python*. Jika komputer Anda belum pernah dipasangi *Python*, ikuti langkah hening (*Silent Install*) berikut agar terpasang mulus di seluruh sistem:

1. Buka folder instalasi yang memuat kaset digital (berkas instalator Windows installer) bernama `python-3.12.10-amd64.exe`.
2. Jangan melakukan *Double Click / Klik Ganda*! Arahkan krusor Anda ke bilah alamat folder di bagian atas, ketik **`cmd`** lalu tekan `[ENTER]`. Jendela Terminal Hitam akan terbuka.
3. Salin dan tempelkan mantera perintah gaib berikut ini ke dalam terminal hitam tersebut, lalu tekan `[ENTER]`:
   ```bash
   python-3.12.10-amd64.exe /quiet InstallAllUsers=1 PrependPath=1
   ```
   *(Penjelasan: Perintah ini menginstruksikan komputer untuk menginstal Python secara senyap tanpa repot menekan 'Next', berlaku untuk semua User PC, dan memasukkannya otomatis ke dalam Path Global).*

## TAHAP 2: Verifikasi Instalasi Mesin
Setelah proses instalasi senyap selesai (biasanya tidak ada notifikasi, hanya diam sejenak sekitar 1-2 menit):

1. Tetap berada di dalam jendela terminal hitam tadi *(atau buka CMD baru)*.
2. Ketik perintah berikut dan tekan `[ENTER]`:
   ```bash
   python --version
   ```
3. Jika pada layar muncul tulisan seperti `Python 3.12.10`, **Selamat!** Mesin berhasil ditanamkan ke dalam PC Anda. Anda boleh menutup terminal hitam tersebut.

## TAHAP 3: Menyalakan Mesin Aplikasi SmartDoc
Kini mesin telah siap, saatnya membangkitkan aplikasi utama!

1. Cari berkas pemicu berlogo gir gigi roda bernama **`run_windows.bat`** *(atau bernama "run_windows" jenis Windows Batch File)* yang terdapat di dalam tumpukan berkas sumber ini.
2. Klik Ganda *(Double Click)* pada berkas tersebut. Untuk instalasi PC baru, **cukup jalankan file ini saja**.
3. Skrip akan otomatis:
   - membuat lingkungan virtual Python jika belum ada
   - memasang seluruh dependency Python dari internet pada instalasi pertama
   - menawarkan pemasangan autostart Windows pada pemakaian pertama
   - membuka aplikasi lokal di browser
4. Jangan menekan tanda silang merah `[X]` pada terminal ini saat aplikasi sedang dipakai. Jika ditutup, maka *Web Server* akan berhenti.
5. Anda bisa langsung menikmati aplikasi di peramban internet (*Browser* Chrome/Edge) melalui alamat: **`http://127.0.0.1:5050`**

### Mode Perbaikan Cepat dari Launcher

Saat menjalankan **`run_windows.bat`**, Anda akan melihat menu singkat:

1. **Jalankan aplikasi**  
   Digunakan untuk pemakaian harian biasa.
2. **Install dependency sekarang**  
   Memaksa pengecekan dan pemasangan paket. Gunakan saat komputer terhubung internet.
3. **Reinstall dependency**  
   Memasang ulang seluruh dependency tanpa menghapus `venv`. Membutuhkan internet.
4. **Repair instalasi**  
   Menghapus `venv`, membuat ulang lingkungan virtual, lalu memasang ulang paket dari internet.
5. **Atur ulang autostart**  
   Menampilkan ulang pertanyaan aktivasi autostart.

Gunakan **Repair instalasi** jika aplikasi gagal berjalan di PC tertentu tetapi berkas project masih lengkap.

## TAHAP 4: Menata Menjadi Autostart (Berjalan Otomatis Saat PC Dinyalakan)
Jika Anda menggunakan PC stasioner / pelayanan terpadu yang sering dimatikan *(Shutdown)* pada jam pulang, lebih baik aplikasi ini menyala sendiri secara otomatis ketika satpam atau pegawai menyalakan PC keesokan paginya.

1. Saat pertama kali menjalankan **`run_windows.bat`**, jawab `Y` jika ingin autostart aktif.
2. Skrip akan otomatis membuat shortcut pada folder `Startup` Windows untuk user yang sedang login.
3. Jika sebelumnya menjawab `N`, autostart masih bisa diaktifkan ulang dengan menghapus berkas `.autostart_windows` lalu menjalankan **`run_windows.bat`** lagi.

---
*Dibuat khusus untuk optimalisasi alat tempur di Lingkungan Direktorat Jenderal Pajak RI.*
