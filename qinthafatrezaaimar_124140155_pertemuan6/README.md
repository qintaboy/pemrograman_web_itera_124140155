# REST API Mahasiswa & Matakuliah - Pyramid + PostgreSQL

Tugas Praktikum Pengembangan Aplikasi Web - Pertemuan 6: Pyramid Framework dan PostgreSQL (CRUD REST API)

## Identitas

| | |
|---|---|
| **Nama Lengkap** | Qinthafa Treza Aimar |
| **NIM** | 124140155 |
| **Kelas Praktikum** | RA |

## Deskripsi

REST API sederhana yang dibuat dengan **Pyramid 2.x**, **SQLAlchemy**, dan **PostgreSQL**. Semua respons berbentuk JSON. API memiliki dua sumber daya:

- **Mahasiswa** (contoh dari materi): `id`, `nim`, `nama`, `jurusan`, `tanggal_lahir`, `alamat`.
- **Matakuliah** (tugas): `id`, `kode_mk`, `nama_mk`, `sks`, `semester`.

Skema database dikelola dengan **Alembic** (dua revisi: tabel `mahasiswa` dan tabel `matakuliah`). Transaksi database ditangani otomatis oleh `pyramid_tm`: bila view berhasil maka di-*commit*, bila terjadi galat maka di-*rollback*.

## Isi Folder

```
qinthafatrezaaimar_124140155_pertemuan6/
├── development.ini            # konfigurasi (URL database, server)
├── production.ini
├── setup.py                   # dependensi dan entry point
├── README.md
├── .gitignore
├── screenshots/               # bukti pengujian cURL
└── pyramid_mahasiswa/
    ├── __init__.py            # fungsi main(): membuat aplikasi
    ├── routes.py              # daftar route + request_method
    ├── tests.py               # tes otomatis (pytest + WebTest)
    ├── alembic/
    │   ├── env.py
    │   └── versions/          # 2 revisi migrasi
    ├── models/
    │   ├── meta.py            # Base SQLAlchemy
    │   ├── mahasiswa.py       # model Mahasiswa
    │   └── matakuliah.py      # model Matakuliah
    ├── scripts/
    │   └── initialize_db.py   # seed data awal
    └── views/
        ├── __init__.py        # fungsi bantu (galat JSON, baca body)
        ├── default.py         # halaman utama (peta endpoint)
        ├── mahasiswa.py       # CRUD Mahasiswa
        └── matakuliah.py      # CRUD Matakuliah
```

## Daftar Endpoint

### Mahasiswa

| Method | URL | Keterangan | Status |
|---|---|---|---|
| GET | `/api/mahasiswa` | Daftar semua mahasiswa | 200 |
| GET | `/api/mahasiswa/{id}` | Detail satu mahasiswa | 200 / 404 |
| POST | `/api/mahasiswa` | Tambah mahasiswa | 200 / 400 |
| PUT | `/api/mahasiswa/{id}` | Ubah mahasiswa | 200 / 400 / 404 |
| DELETE | `/api/mahasiswa/{id}` | Hapus mahasiswa | 200 / 404 |

### Matakuliah

| Method | URL | Keterangan | Status |
|---|---|---|---|
| GET | `/api/matakuliah` | Daftar semua matakuliah | 200 |
| GET | `/api/matakuliah/{id}` | Detail satu matakuliah | 200 / 404 |
| POST | `/api/matakuliah` | Tambah matakuliah | 200 / 400 |
| PUT | `/api/matakuliah/{id}` | Ubah matakuliah | 200 / 400 / 404 |
| DELETE | `/api/matakuliah/{id}` | Hapus matakuliah | 200 / 404 |

### Aturan validasi Matakuliah

- `kode_mk`, `nama_mk`, `sks`, `semester` **wajib** pada POST; field kosong atau hilang menghasilkan **400**.
- `sks` dan `semester` harus **bilangan bulat lebih dari 0** (`0`, negatif, desimal, teks, dan `true` ditolak dengan 400).
- `kode_mk` harus unik; kode yang sudah dipakai menghasilkan 400.
- PUT boleh mengirim sebagian field saja; body kosong menghasilkan 400.
- `id` yang tidak ada pada GET/PUT/DELETE menghasilkan **404**.
- Semua galat berbentuk `{"error": "pesan"}`.

## Cara Menjalankan

Prasyarat: **Python 3.10 atau 3.11** (disarankan, karena `psycopg2-binary` belum tentu punya paket siap pakai untuk Python yang terlalu baru) dan **PostgreSQL**.

### 1. Clone dan buat virtual environment

```bash
git clone https://github.com/qintaboy/pemrograman_web_itera_124140155.git
cd pemrograman_web_itera_124140155/qinthafatrezaaimar_124140155_pertemuan6

python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Linux / macOS

pip install --upgrade pip setuptools wheel
pip install -e ".[testing]"
```

### 2. Siapkan database PostgreSQL

Masuk ke `psql` sebagai superuser, lalu jalankan:

```sql
CREATE DATABASE pyramid_mahasiswa;
CREATE USER pyramid_user WITH PASSWORD 'pyramid_pass';
GRANT ALL PRIVILEGES ON DATABASE pyramid_mahasiswa TO pyramid_user;
\c pyramid_mahasiswa
GRANT ALL ON SCHEMA public TO pyramid_user;
```

URL koneksi ada di `development.ini`:

```
sqlalchemy.url = postgresql+psycopg2://pyramid_user:pyramid_pass@localhost:5432/pyramid_mahasiswa
```

> Memakai `postgresql+psycopg2://` (bukan `postgresql://`) agar SQLAlchemy versi terbaru tetap memakai driver `psycopg2`.

### 3. Migrasi database (Alembic)

```bash
alembic -c development.ini upgrade head
```

Perintah ini membuat tabel `mahasiswa` dan `matakuliah`. Cek posisi migrasi dengan `alembic -c development.ini current`.

Cara membuat revisi baru setelah mengubah model:

```bash
alembic -c development.ini revision --autogenerate -m "pesan revisi"
alembic -c development.ini upgrade head
```

### 4. Isi data awal (seed)

```bash
python -m pyramid_mahasiswa.scripts.initialize_db development.ini
```

Data awal: 2 mahasiswa dan 3 matakuliah (IF2110, IF3140, IF2210). Aman dijalankan berulang kali karena data yang sudah ada dilewati.

### 5. Jalankan server

```bash
pserve development.ini --reload
```

API aktif di `http://localhost:6543`. Buka `http://localhost:6543/` untuk melihat peta endpoint.

### 6. Jalankan tes otomatis

```bash
pytest
```

Tes memakai SQLite sementara sehingga tidak mengubah data PostgreSQL.

## Pengujian (cURL)

Contoh di bawah dijalankan di terminal; pada PowerShell Windows gunakan `curl.exe` dan tanda kutip ganda yang di-escape, atau pakai Postman.

### Mahasiswa

**GET daftar, GET detail, dan detail yang tidak ada (404)**

```bash
curl http://localhost:6543/api/mahasiswa
curl http://localhost:6543/api/mahasiswa/1
curl http://localhost:6543/api/mahasiswa/99
```

![Mahasiswa GET](screenshots/01-mahasiswa-get.png)

**POST data valid dan tidak valid (nama kosong, NIM kembar)**

```bash
curl -X POST http://localhost:6543/api/mahasiswa \
  -H "Content-Type: application/json" \
  -d '{"nim":"124140155","nama":"Qinthafa Treza Aimar","jurusan":"Teknik Informatika","tanggal_lahir":"1945-11-11","alamat":"Kost Mango"}'
```

![Mahasiswa POST](screenshots/02-mahasiswa-post.png)

**PUT dan DELETE (termasuk 404)**

```bash
curl -X PUT http://localhost:6543/api/mahasiswa/3 \
  -H "Content-Type: application/json" -d '{"alamat":"Bandar Lampung"}'
curl -X DELETE http://localhost:6543/api/mahasiswa/3
```

![Mahasiswa PUT dan DELETE](screenshots/03-mahasiswa-put-delete.png)

### Matakuliah

**GET daftar, GET detail, dan detail yang tidak ada (404)**

```bash
curl http://localhost:6543/api/matakuliah
curl http://localhost:6543/api/matakuliah/1
curl http://localhost:6543/api/matakuliah/99
```

![Matakuliah GET](screenshots/04-matakuliah-get.png)

**POST data valid dan validasi 400 (kode kosong, sks = 0, field hilang)**

```bash
curl -X POST http://localhost:6543/api/matakuliah \
  -H "Content-Type: application/json" \
  -d '{"kode_mk":"IF4110","nama_mk":"Kecerdasan Buatan","sks":3,"semester":6}'
```

![Matakuliah POST](screenshots/05-matakuliah-post.png)

**PUT dan DELETE (termasuk 404)**

```bash
curl -X PUT http://localhost:6543/api/matakuliah/4 \
  -H "Content-Type: application/json" -d '{"sks":4}'
curl -X DELETE http://localhost:6543/api/matakuliah/4
```

![Matakuliah PUT dan DELETE](screenshots/06-matakuliah-put-delete.png)

## Alur Satu Request

1. `routes.py` mencocokkan URL **dan** method (`request_method`) ke sebuah nama route.
2. `@view_config(route_name=..., request_method=..., renderer='json')` mengarahkan ke fungsi view.
3. View membaca `request.matchdict` (id di URL) atau `request.json_body` (data kiriman), memvalidasi, lalu memakai `request.dbsession` untuk query.
4. Hasil dict diubah menjadi JSON; `pyramid_tm` meng-*commit* transaksi, atau *rollback* bila ada galat.

Kode mengikuti PEP 8 (dicek dengan `pycodestyle`) dan setiap fungsi memiliki docstring.
