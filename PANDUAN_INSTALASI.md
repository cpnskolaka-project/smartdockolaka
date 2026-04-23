# PANDUAN INSTALASI APLIKASI SMARTDOC KOLAKA
**(Khusus Komputer / Laptop Windows)**

Dokumen ini berisi panduan lengkap langkah demi langkah untuk menginstal dan menjalankan aplikasi **SmartDoc Kolaka** di komputer operasional KPP Pratama Kolaka secara lokal tanpa memerlukan akses internet (*Offline*).

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
2. Klik Ganda *(Double Click)* pada berkas tersebut.
3. Kumpulan tulisan skrip otomatis akan berlarian menata perpustakaan berkas dan memasang jubah AI tambahan yang dibutuhkan *(Hanya memakan waktu pada pertama kali dibuka)*.
4. Jangan pernah menekan tanda silang merah `[X]` pada terminal ini! Jika ditutup, maka *Web Server* akan mati seketika. Biarkan terminal terminimize ke *Taskbar* bawah.
5. Anda bisa langsung menikmati aplikasi di peramban internet (*Browser* Chrome/Edge) melalui alamat: **`http://127.0.0.1:5000`**

## TAHAP 4: Menata Menjadi Autostart (Berjalan Otomatis Saat PC Dinyalakan)
Jika Anda menggunakan PC stasioner / pelayanan terpadu yang sering dimatikan *(Shutdown)* pada jam pulang, lebih baik aplikasi ini menyala sendiri secara otomatis ketika satpam atau pegawai menyalakan PC keesokan paginya.

1. Beralih ke folder aplikasi dan temukan berkas **`run_windows.bat`** tadi.
2. Klik Kanan berkas tersebut -> Klik **`Create shortcut`** (atau ketuk tombol Alt/Option sembari menarik file). Berkas salinan bernama *run_windows.bat - Shortcut* akan terbentuk.
3. Sekarang, tekan tahan bendera sakti **`Tombol Windows` + `[R]`** di _Keyboard_ Anda secara bersamaan. Jendela kecil *Run* akan meloncat keluar.
4. Ketik teks sandi berikut ini dan tekan Enter:
   ```text
   shell:startup
   ```
5. Jendela folder kosong bernama _Startup_ akan terbuka. 
6. Pindahkan *(Cut)* atau seret berkas **Shortcut** yang Anda buat pada langkah ke-2 tadi ke dalam folder _Startup_ ini.
7. Selesai! Harta karun telah tersimpan rapi. Kini setiap kali PC di-*Restart* maupun baru pertama kali dihidupkan, ia akan otomatis menjalankan tugas tanpa Anda perintah!

---
*Dibuat khusus untuk optimalisasi alat tempur di Lingkungan Direktorat Jenderal Pajak RI.*
