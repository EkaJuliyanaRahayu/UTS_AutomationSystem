import argparse
import csv
from pathlib import Path
import re
import sys
import zipfile
import requests


# ==========================================
# 1. INTEGRASI CHAPTER 13 & API WEB SCRAPING
# ==========================================
def scrape_books_openlibrary(query="programming", limit=50, custom_url=None):
    """Mengambil data buku dari API Open Library secara stabil atau menguji custom URL."""
    data_buku = []
    page = 1

    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
    }

    # Jika argumen --url digunakan untuk simulasi koneksi gagal
    if custom_url:
        print(f"[+] Mengakses URL khusus: '{custom_url}'...")
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                print(f"[+] Percobaan koneksi ke-{attempt}...")
                response = requests.get(custom_url, headers=headers, timeout=5)
                if response.status_code == 200:
                    print("[+] Koneksi berhasil!")
                    return data_buku
            except requests.exceptions.RequestException as e:
                print(f"[!] Gagal terhubung: {e}")
        print("[!] Mencapai batas maksimum percobaan retry. Operasi dibatalkan secara aman.")
        return data_buku

    print(f"[+] Mengambil data dari Open Library (Keyword: '{query}')...")

    while len(data_buku) < limit:
        url = f"https://openlibrary.org/search.json?q={query}&page={page}"
        try:
            response = requests.get(url, headers=headers, timeout=10)
            if response.status_code != 200:
                print(f"[!] Gagal mengakses API page {page}. HTTP {response.status_code}")
                break

            json_data = response.json()
            docs = json_data.get("docs", [])

            if not docs:
                print(f"[!] Tidak ada lagi data yang ditemukan pada halaman {page}.")
                break

            for doc in docs:
                if len(data_buku) >= limit:
                    break

                judul_raw = doc.get("title", "Untitled")
                authors = doc.get("author_name", ["Unknown Author"])
                penulis_raw = authors[0] if authors else "Unknown Author"
                tahun_raw = str(doc.get("first_publish_year", "N/A"))

                key = doc.get("key", "")
                link = f"https://openlibrary.org{key}" if key else "-"

                # Regular Expressions (Regex)
                judul_clean = re.sub(r"[^\w\s\-\:]", "", judul_raw)
                match_tahun = re.search(r"\b(19|20)\d{2}\b", tahun_raw)
                tahun_terbit = (
                    match_tahun.group(0) if match_tahun else "Tidak diketahui"
                )

                data_buku.append(
                    {
                        "judul": judul_clean,
                        "penulis": penulis_raw,
                        "tahun_terbit": tahun_terbit,
                        "tautan": link,
                    }
                )

            page += 1

        except Exception as e:
            print(f"[!] Terjadi kesalahan koneksi: {e}")
            break

    return data_buku


# ==========================================
# 2. PENCARIAN OFFLINE (CHAPTER 10)
# ==========================================
def search_offline(keyword, field="penulis", folder_output="output"):
    """Mencari data pada file CSV lokal secara offline."""
    csv_path = Path(folder_output) / "hasil_scraping.csv"

    if not csv_path.exists():
        print(f"[!] Error: File '{csv_path}' tidak ditemukan!")
        print(f"[!] Pastikan folder '{folder_output}' dan file CSV hasil scraping sudah ada.")
        return

    print(f"[+] Melakukan pencarian offline pada file: {csv_path}")
    print(f"[+] Kata kunci: '{keyword}' | Kolom: '{field}'")
    
    hasil = []
    with csv_path.open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            target_value = row.get(field, "")
            if keyword.lower() in target_value.lower():
                hasil.append(row)

    print(f"\n[+] Ditemukan {len(hasil)} record yang cocok:")
    print("-" * 50)
    for idx, item in enumerate(hasil, 1):
        print(f"{idx}. {item.get('judul', '-')} | Penulis: {item.get('penulis', '-')} ({item.get('tahun_terbit', '-')})")
    print("-" * 50)


# ==========================================
# 3. FILE & DIRECTORY MANAGEMENT
# ==========================================
def process_and_save_files(data_buku, keyword, folder_output="output"):
    dir_data = Path("data")
    dir_output = Path(folder_output)
    dir_backup = Path("backup")

    for folder in [dir_data, dir_output, dir_backup]:
        folder.mkdir(parents=True, exist_ok=True)

    # 1. Simpan Raw Data (.txt)
    raw_file = dir_data / "raw_data.txt"
    with raw_file.open("w", encoding="utf-8") as f:
        for b in data_buku:
            f.write(
                f"{b['judul']} | {b['penulis']} | {b['tahun_terbit']} | {b['tautan']}\n"
            )

    # 2. Simpan Output Hasil Scraping (.csv)
    csv_file = dir_output / "hasil_scraping.csv"
    keys = ["judul", "penulis", "tahun_terbit", "tautan"]
    with csv_file.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=keys)
        writer.writeheader()
        writer.writerows(data_buku)

    # 3. Simpan Ringkasan Laporan (.txt)
    laporan_file = dir_output / "laporan.txt"
    with laporan_file.open("w", encoding="utf-8") as f:
        f.write("=== LAPORAN RINGKASAN AUTOMASI ONLINE BOOK CATALOG ORGANIZER ===\n")
        f.write(f"Kata Kunci Pencarian : {keyword}\n")
        f.write(f"Total Record Berhasil: {len(data_buku)}\n")
        f.write("--------------------------------------------------\n")
        for idx, b in enumerate(data_buku[:10], 1):
            f.write(f"{idx}. {b['judul']} ({b['tahun_terbit']}) - {b['penulis']}\n")

    print(f"[+] Raw data tersimpan di: {raw_file.resolve()}")
    print(f"[+] Hasil scraping tersimpan di: {csv_file.resolve()}")
    print(f"[+] Laporan tersimpan di: {laporan_file.resolve()}")


def create_backup_zip():
    dir_backup = Path("backup")
    zip_path = dir_backup / "backup_data.zip"

    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zipf:
        for folder_target in [Path("data"), Path("output")]:
            if folder_target.exists():
                for file in folder_target.iterdir():
                    if file.is_file():
                        zipf.write(
                            file, arcname=Path(folder_target.name) / file.name
                        )

    print(f"[+] Backup berhasil dibuat di: {zip_path.resolve()}")


# ==========================================
# 4. COMMAND LINE INTERFACE (CLI)
# ==========================================
def main():
    parser = argparse.ArgumentParser(
        description="Aplikasi Automasi Online Book Catalog Organizer (UTS)"
    )

    parser.add_argument(
        "--keyword",
        type=str,
        default="programming",
        help="Kata kunci pencarian buku",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=50,
        help="Jumlah minimal record data yang diambil",
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        help="Sertakan opsi ini untuk otomatis membuat backup .zip",
    )
    parser.add_argument(
        "--search-only",
        action="store_true",
        help="Melakukan pencarian offline dari file CSV lokal",
    )
    parser.add_argument(
        "--field",
        type=str,
        default="penulis",
        help="Kolom target pencarian (penulis/judul)",
    )
    parser.add_argument(
        "--url",
        type=str,
        default=None,
        help="URL kustom untuk pengujian koneksi error",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="output",
        help="Folder tempat menyimpan atau mencari file output",
    )

    args = parser.parse_args()

    # Mode 1: Pencarian Offline
    if args.search_only:
        search_offline(keyword=args.keyword, field=args.field, folder_output=args.output)
        sys.exit(0)

    # Mode 2: Scraping Online / Pengujian Custom URL
    data = scrape_books_openlibrary(query=args.keyword, limit=args.limit, custom_url=args.url)

    if not data:
        if not args.url:
            print("[!] Data kosong atau scraping gagal. Program dihentikan.")
        sys.exit(1)

    process_and_save_files(data, args.keyword, folder_output=args.output)

    if args.backup:
        create_backup_zip()

    print("\n==================================================")
    print("           RINGKASAN PEMROSESAN AUTOMASI          ")
    print("==================================================")
    print(f"Kata Kunci  : {args.keyword}")
    print(f"Total Data  : {len(data)} record")
    print("--------------------------------------------------")
    print("Contoh 3 Data Teratas:")
    for i, b in enumerate(data[:3], 1):
        print(f"{i}. {b['judul']} | Penulis: {b['penulis']} ({b['tahun_terbit']})")
    print("==================================================\n")


if __name__ == "__main__":
    main()