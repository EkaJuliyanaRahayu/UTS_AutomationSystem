

```markdown
# Online Book Catalog Organizer (Automation System)

Aplikasi berbasis Python Command Line Interface (CLI) untuk mengotomatisasi pengambilan data katalog buku secara *online* dari **Open Library API**, memproses data menggunakan **Regular Expressions (Regex)**, mengelola file laporan terstruktur, serta menyediakan fitur **pencarian *offline*** dan **pembuatan cadangan (*backup*) otomatis**.

Proyek ini disusun untuk memenuhi evaluasi Ujian Tengah Semester (UTS) mata kuliah **Automation System / Otomasi Sistem**.

---

## 🚀 Fitur Utama Program

1. **Web Scraping & API Integration**: Mengambil data buku secara dinamis dari Open Library API berdasarkan kata kunci (*keyword*) dan batas jumlah data (*limit*).
2. **Pembersihan Data dengan Regex**:
   - Pembersihan karakter khusus pada judul buku (`re.sub`).
   - Ekstraksi 4 digit tahun terbit secara spesifik (`re.search`).
3. **Manajemen File & Direktori Terstruktur (`pathlib`)**:
   - `data/raw_data.txt`: Format data mentah (*raw text*).
   - `output/hasil_scraping.csv`: Format data terstruktur (*Comma-Separated Values*).
   - `output/laporan.txt`: Ringkasan statistik eksekusi program.
4. **Offline Search Engine**: Pencarian data lokal cepat dari file CSV tanpa koneksi internet.
5. **Automated Backup System (`zipfile`)**: Kompresi otomatis folder `data` dan `output` menjadi file `.zip`.
6. **Error Handling & Retry Mechanism**: Menangani kegagalan jaringan (*network timeout/connection error*) dan file hilang tanpa membuat aplikasi *crash*.

---

## 🛠️ Persyaratan Sistem & Instalasi

- **Python**: Versi 3.8 atau yang lebih baru.
- **Library Dependensi**: `requests`

Instalasi library dependensi melalui terminal:
```bash
pip install requests

```

---

## 📂 Struktur Direktori Proyek

```text
UTS_AutomationSystem/
│
├── main.py              # Skrip utama aplikasi (CLI & Logika Otomasi)
├── README.md            # Dokumentasi proyek & panduan pengujian
│
├── data/                # Folder penyimpanan data mentah
│   └── raw_data.txt
│
├── output/              # Folder penyimpanan hasil pemrosesan
│   ├── hasil_scraping.csv
│   └── laporan.txt
│
└── backup/              # Folder penyimpanan arsip backup
    └── backup_data.zip

```

---

## 📖 Panduan Pengujian & Demonstrasi CLI Lengkap (Demo Flow)

Berikut adalah urutan 7 langkah skenario pengujian dari awal hingga akhir beserta perintah terminal dan teks penjelasannya saat presentasi demo UTS:

### 1. Cek Daftar Argumen CLI

Perintah ini digunakan untuk menampilkan menu bantuan CLI dan membuktikan fleksibilitas argumen program:

```bash
python main.py --help

```

> *"Perintah ini menampilkan menu bantuan CLI untuk membuktikan bahwa program mendukung 7 argumen konfigurasi dinamis tanpa perlu mengubah kode program secara manual."*

---

### 2. Scraping Data Utama & Backup Otomatis

Mengambil 50 data buku dengan kata kunci `programming` serta membuat backup format `.zip`:

```bash
python main.py --keyword "programming" --limit 50 --backup

```

> **Penjelasan Demo saat Presentasi:** *"Program melakukan scraping 50 data dari Open Library API, membersihkan data dengan Regex, menyimpan file CSV/TXT, dan otomatis mengarsipkannya ke `backup/backup_data.zip`."*

---

### 3. Scraping Kustom Berdasarkan Kata Kunci

Menguji kemampuan pengambilan data dengan topik berbeda (misalnya: `python` sebanyak 30 record):

```bash
python main.py --keyword "python" --limit 30

```

> *"Perintah ini membuktikan program dapat memproses kata kunci pencarian lain dengan batas record yang disesuaikan secara dinamis."*

---

### 4. Pencarian Offline (Tanpa Internet)

Melakukan pencarian spesifik berdasarkan nama penulis (`austen`) dari file CSV lokal yang sudah tersimpan sebelumnya:

```bash
python main.py --search-only --keyword austen --field penulis

```

> *"Fitur pencarian offline ini mencari data secara cepat dari `hasil_scraping.csv` tanpa melakukan HTTP request ulang ke internet."*

---

### 5. Pengujian Error Handling (Koneksi Jaringan Gagal)

Simulasi penanganan kesalahan saat program mencoba mengakses URL yang tidak dapat dijangkau/down:

```bash
python main.py --url http://localhost:1/x

```

> *"Perintah ini menguji ketahanan sistem. Program akan mencoba melakukan retry hingga 3 kali, lalu berhenti secara aman dengan pesan peringatan rapi tanpa crash."*

---

### 6. Pengujian Error Handling (File / Folder Tidak Ditemukan)

Simulasi penanganan kesalahan ketika target folder pencarian offline tidak ada di direktori lokal:

```bash
python main.py --search-only --output folder_kosong

```

> *"Membuktikan exception handling berjalan baik saat file CSV tidak ditemukan, sehingga program menampilkan pesan kesalahan yang rapi dan tidak memunculkan traceback error."*

---

### 7. Pembersihan Folder Percobaan

Membersihkan folder `folder_kosong` yang otomatis terbentuk dari pengujian Langkah 6 agar proyek tetap bersih sebelum dikumpulkan:

```bash
rmdir /s /q folder_kosong

```

> "Langkah terakhir ini dilakukan untuk menghapus folder temporary hasil pengujian error handling agar struktur folder utama tetap bersih saat dikumpulkan."*



