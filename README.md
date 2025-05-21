# 🏙️ Scyscraper - Telkom Data ETL Automation

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Repo Size](https://img.shields.io/github/repo-size/Ersaoktaviannn/Scyscraper)](https://github.com/Ersaoktaviannn/Scyscraper)
[![Last Commit](https://img.shields.io/github/last-commit/Ersaoktaviannn/Scyscraper)](https://github.com/Ersaoktaviannn/Scyscraper/commits/main)
[![Issues](https://img.shields.io/github/issues/Ersaoktaviannn/Scyscraper)](https://github.com/Ersaoktaviannn/Scyscraper/issues)
[![Stars](https://img.shields.io/github/stars/Ersaoktaviannn/Scyscraper?style=social)](https://github.com/Ersaoktaviannn/Scyscraper/stargazers)

Scyscraper adalah proyek otomatisasi ETL berbasis Python yang mengekstraksi data dari portal internal Telkom (MyTens GoBeyond), melakukan transformasi data, dan memuatnya ke dalam database PostgreSQL atau SQLite. Proyek ini sepenuhnya dikontrol melalui script Python menggunakan Selenium, pandas, dan SQLAlchemy.

---
## 🔧 Fitur Utama

- ✅ **Login otomatis** ke portal Telkom MyTens GoBeyond
- 🔄 **Navigasi dashboard** dan tab dinamis (Bintang 1–5)
- 📥 **Ekstraksi file CSV otomatis** melalui antarmuka web dinamis
- 🧹 **Transformasi data**: normalisasi nama kolom, pengisian nilai kosong, penambahan metadata
- 🗃️ **Loading ke database** PostgreSQL / SQLite
- 📊 **Laporan hasil ETL** secara otomatis dalam bentuk log dan teks
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

2. Jalankan Program
python scraper.py

3. Analisis Log
telkom_etl.log



