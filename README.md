# Online Book Catalog Organizer (Automations System)

Aplikasi berbasis Python Command Line Interface (CLI) untuk mengotomatisasi pengambilan data katalog buku secara *online* dari **Open Library API**, memproses data menggunakan **Regular Expressions (Regex)**, mengelola file laporan, serta menyediakan fitur **pencarian *offline*** dan **pembuatan cadangan (*backup*) otomatis**.

Project ini dibuat untuk memenuhi tugas mata kuliah **Automation System / Otomasi Sistem**.

---

## 🚀 Fitur Utama

1. **Web Scraping & API Integration**: Mengambil data buku secara otomatis dari Open Library API berdasarkan kata kunci dan batas jumlah data (*limit*).
2. **Data Cleaning dengan Regex**: Membersihkan karakter khusus pada judul buku dan mengekstrak 4 digit tahun terbit secara presisi.
3. **Penyimpanan File Terstruktur**:
   - `data/raw_data.txt`: Data mentah hasil ekstraksi.
   - `output/hasil_scraping.csv`: Data terstruktur format CSV.
   - `output/laporan.txt`: Ringkasan hasil pemrosesan data.
4. **Offline Search**: Fitur pencarian cepat langsung dari file CSV lokal tanpa koneksi internet.
5. **Automatic Backup**: Membuat arsip kompresi `.zip` dari folder `data` dan `output`.
6. **Error Handling & Retry Mechanism**: Menangani kegagalan koneksi jaringan secara aman tanpa membuat program *crash*.

---

## 🛠️ Persyaratan Sistem

- **Python**: versi 3.8 atau lebih baru.
- **Library Tambahan**: `requests`

Instalasi library yang dibutuhkan:
```bash
pip install requests
