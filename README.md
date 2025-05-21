# 🏙️ Scyscraper - Telkom ETL Automation

Scyscraper adalah proyek otomatisasi ETL berbasis Python yang mengekstraksi data dari portal internal Telkom (GoBeyond), melakukan transformasi data, dan memuatnya ke dalam database PostgreSQL atau SQLite. Proyek ini sepenuhnya dikontrol melalui script Python menggunakan Selenium, pandas, dan SQLAlchemy.

---

## 🔧 Fitur Utama

- ✅ **Login otomatis** ke portal internal Telkom
- 🔄 **Navigasi dashboard interaktif** dan tab dinamis (Bintang 1–5)
- 📥 **Ekstraksi file CSV otomatis** melalui antarmuka web dinamis
- 🧹 **Transformasi data**: normalisasi nama kolom, pengisian nilai kosong, penambahan metadata
- 🗃️ **Loading ke database** PostgreSQL / SQLite
- 📊 **Laporan hasil ETL** secara otomatis dalam bentuk log dan teks

---

## 📁 Struktur Proyek

├── chromedriver-win64/ # Folder chromedriver lokal
├── downloads/ # Folder download file mentah
├── processed/ # Hasil transformasi data
├── output/ # Hasil gabungan + laporan
├── data/
│ ├── telkom_data.db # SQLite DB (opsional)
│ └── metadata.json # Metadata ekstraksi
├── scraper.py # File utama pipeline ETL
├── scy.py # Versi entry point alternatif
├── README.md



---

## 🛠️ Prasyarat

- Python 3.8+
- Google Chrome
- [ChromeDriver](https://chromedriver.chromium.org/downloads) (sudah disediakan di folder `chromedriver-win64`)

### 📦 Instalasi Dependensi

```bash
pip install -r requirements.txt

pip install selenium pandas sqlalchemy psycopg2



🚀 Menjalankan Pipeline
1. Konfigurasi
Edit konfigurasi di dalam file scraper.py (bagian CONFIG):

"username": "isi sesuai kebutuhan",
"password": "isi sesuai kebutuhan",
"base_url": "https://newgobeyond.mytens.co.id",
...
"db_type": "postgresql",
"db_user": "isi sesuai kebutuhan",
"db_password": "isi sesuai kebutuhan",
...

. Jalankan Program
python scraper.py

