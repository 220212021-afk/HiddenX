# Status dan Alur Project Hidden X

Dokumen ini merangkum kondisi repository pada 21 Oktober 2026. Isinya membedakan kode yang benar-benar ada dari rancangan pada SRS dan dokumentasi. Keberadaan nama dependensi atau rancangan endpoint tidak berarti fitur tersebut sudah berfungsi.

## Ringkasan

Hidden X dirancang sebagai platform microblogging anonim: pengguna tampil dengan Anon-ID, sedangkan identitas asli dilindungi di backend. Repository saat ini baru berisi fondasi backend Python dan sebagian konfigurasi proyek. Aplikasi belum dapat melayani alur pengguna karena entry point FastAPI masih kosong dan belum ada endpoint, service, model, migrasi, ataupun test.

| Area | Status nyata |
| --- | --- |
| Konfigurasi package, dependensi, Ruff, mypy, pytest | Ada di `backend/pyproject.toml` |
| Template konfigurasi aplikasi | Ada di `backend/.env.example` |
| Pengaturan environment | Ada di `backend/app/core/config.py` |
| Base SQLAlchemy, mixin waktu, dan sesi async | Ada di `backend/app/db/` |
| Entry point aplikasi | `backend/app/main.py` ada, tetapi kosong |
| Model, schema API, service, endpoint | Belum ada |
| Alembic dan migrasi | Belum ada file konfigurasi atau migrasi yang terlacak |
| Test | Folder tersedia, tetapi belum ada test |
| Frontend | Belum ada |
| PostgreSQL lokal | Rancangan Compose ada di `compose.yaml`, tetapi file ini diabaikan Git |
| Fitur produk: auth, post, feed, sosial, moderasi, notifikasi | Masih rancangan; belum diimplementasikan |

## Yang Sudah Tercapai

1. **Fondasi project backend:** package Python menggunakan setuptools, versi project `0.1.0`, dan Python minimum 3.11.
2. **Konfigurasi aplikasi:** `Settings` membaca environment dan file `backend/.env`, memvalidasi pilihan environment, durasi token, asal CORS, serta format kunci Fernet.
3. **Fondasi database:** tersedia `DeclarativeBase` dengan aturan penamaan constraint, kolom waktu bersama, serta SQLAlchemy async engine dan pembuat `AsyncSession`.
4. **Konfigurasi kerja tim:** root `Makefile` mendefinisikan perintah install, run, migrate, revision, test, lint, format, dan hooks. Perintah migrasi belum bisa berjalan karena konfigurasi Alembic belum ada.
5. **Rancangan kebutuhan dan arsitektur:** SRS draf menguraikan aktor, FR-01–FR-17, NFR, use case, skema data, dan rancangan API. Dokumen `docs/agent/` menjabarkan arsitektur target, keputusan database, keamanan, konvensi, roadmap, dan workflow.

Roadmap masih perlu diselaraskan dengan kode. Contohnya, Roadmap Fase 0 menandai konfigurasi selesai, tetapi mencentang `db/base.py`, `db/session.py`, `db/mixins.py`, dan `main.py` sebagai belum selesai, walau tiga modul database sudah ada. Sebaliknya, file `main.py` memang ada, tetapi kosong. Gunakan pemeriksaan kode sebagai sumber status implementasi.

## Alur Program yang Direncanakan

Rancangan memakai arsitektur tiga lapis:

```text
Next.js (frontend) --REST/JSON--> FastAPI (backend) --SQLAlchemy async--> PostgreSQL
```

Frontend belum ada. PostgreSQL merupakan pilihan default dalam `docs/agent/DATABASE.md`; MySQL masih disebut sebagai opsi umum pada SRS.

Alur request yang direncanakan:

1. Client mengirim request JSON ke endpoint versi `/api/v1`.
2. Endpoint memvalidasi input dengan schema Pydantic dan, untuk endpoint privat, memeriksa token serta akses pengguna.
3. Endpoint memanggil service; service menjalankan aturan bisnis dan query database melalui `AsyncSession`.
4. Model SQLAlchemy memetakan data ke tabel. Migrasi Alembic mengelola perubahan skema.
5. Endpoint membentuk response memakai schema output eksplisit. Data identitas asli dan ID internal tidak boleh bocor.

Contoh `POST /posts` (FR-05): Pydantic menolak isi di atas 280 karakter; autentikasi memverifikasi pengguna aktif; service membuat post dan, bila tersedia, memproses hashtag; database menyimpan transaksi; API mengembalikan response post dengan status `201`.

Roadmap membagi fitur menjadi fase:

- **Fase 0 — Fondasi:** konfigurasi, database async, Alembic, entry point, dan test.
- **Fase 1 — Autentikasi:** registrasi, login, JWT, refresh/logout, penyimpanan identitas aman, dan otorisasi.
- **Fase 2 — Konten:** post, reply, repost, like, hashtag, batas 280 karakter, dan penghapusan.
- **Fase 3 — Sosial:** follow, feed berhalaman cursor, profil publik, trending, dan pencarian.
- **Fase 4 — Moderasi/notifikasi:** laporan, alur status, tindakan moderator/admin, audit, dan notifikasi.
- **Fase 5 — Rilis:** penguatan keamanan/performa, seed/admin tools, Docker produksi, dokumentasi, dan deploy.

Rincian fitur di SRS tidak semuanya kebutuhan final: beberapa butir secara eksplisit berlabel **Asumsi**. Tim perlu mengonfirmasi asumsi dan keputusan terbuka database sebelum implementasi fitur terkait.

## Alur Program yang Sudah Ada

Belum ada alur request HTTP yang dapat dijalankan. `backend/app/main.py` berukuran 0 byte; belum ada objek `FastAPI`, router, atau endpoint. Alur kode yang tersedia terbatas pada fondasi konfigurasi dan database:

1. `get_settings()` di `core/config.py` membuat `Settings` sekali lalu menyimpan hasilnya lewat `lru_cache`.
2. Saat `db/session.py` diimpor, modul memanggil `get_settings()` untuk membaca `DATABASE_URL`, lalu membuat async engine dan `async_sessionmaker`.
3. Pemanggil `get_db()` dapat membuka `AsyncSession` dalam context manager dan menutupnya saat generator selesai.
4. `db/base.py` menyediakan metadata untuk model SQLAlchemy yang akan ditambahkan. `db/mixins.py` menyediakan kolom waktu yang dapat digunakan model.

Belum ada pemanggil `get_db()` dari endpoint, model yang memakai `Base` atau `TimestampMixin`, maupun konfigurasi Alembic. Karena itu fondasi ini belum menyimpan atau membaca data aplikasi dengan sendirinya.

## Fungsi File yang Sudah Ada

| File | Fungsi | Hubungan |
| --- | --- | --- |
| `backend/app/main.py` | Direncanakan sebagai entry point FastAPI. | Kosong; belum menghubungkan config, middleware, router, atau error handler. |
| `backend/app/core/config.py` | Mendefinisikan `Settings`, validasi environment dan kunci, parsing CORS, serta `get_settings()`. | Memakai Pydantic, `pydantic-settings`, dan `cryptography.Fernet`; `db/session.py` mengambil pengaturan dari sini. |
| `backend/app/db/base.py` | Menyediakan `Base` SQLAlchemy dan `NAMING_CONVENTION` untuk constraint/index. | Model ORM dan Alembic nantinya perlu memakai metadata ini; model belum ada. |
| `backend/app/db/mixins.py` | Menyediakan `created_at` dan `updated_at` dengan waktu dari database. | Dirancang untuk dipakai bersama oleh model ORM; saat ini belum dipakai model. |
| `backend/app/db/session.py` | Membuat async engine, `async_sessionmaker`, dan dependency generator `get_db()`. | Bergantung pada URL dari config dan `AsyncSession` SQLAlchemy; belum digunakan endpoint. |
| `backend/pyproject.toml` | Menetapkan metadata package, dependency, dan konfigurasi pytest/Ruff/mypy. | Sumber deklarasi dependency aplikasi dan tooling developer. |
| `backend/requirements.txt` | Memasang project lokal beserta dependency development lewat `-e ./backend[dev]`. | Mengacu ke dependency group dalam `pyproject.toml`. |
| `backend/.env.example` | Contoh nama variabel konfigurasi aplikasi dan database lokal, tanpa kunci produksi. | Menjadi acuan untuk file `backend/.env` lokal yang diabaikan Git. |
| `Makefile` | Menyediakan shortcut perintah untuk install, server, migrasi, test, lint, dan format. | Memanggil modul Python dengan working directory backend; beberapa target belum bisa berhasil sebelum komponen dibuat. |
| `compose.yaml` | Mendefinisikan service PostgreSQL lokal, health check, port localhost, dan volume data. | Dimaksudkan untuk database development. File ini diabaikan Git menurut `.gitignore`. |
| `SRS Hidden X (Draf Rekonstruksi).md` | Menyimpan kebutuhan dan rancangan produk. | Sumber rencana; bukan bukti fitur sudah tersedia. |
| `docs/agent/*.md` | Berisi arsitektur, kontrak API, konvensi, database, keamanan, roadmap, dan workflow. | Panduan perencanaan. Folder `docs/agent` diabaikan Git, sehingga berkas di dalamnya tidak terlacak pada repository. |
| `README.md` | Hanya menyebut HiddenX sebagai project mata kuliah Full Stack Web Framework. | Belum berisi petunjuk setup atau gambaran implementasi. |

## Dependency dan Hubungan dengan Kode

Dependency runtime yang tercantum di `backend/pyproject.toml`:

| Dependency | Peran yang direncanakan | Status penggunaan di kode yang ada |
| --- | --- | --- |
| `fastapi`, `uvicorn[standard]` | Framework API dan server ASGI. | Belum dipakai; `main.py` kosong. |
| `pydantic`, `pydantic-settings`, `email-validator` | Validasi schema dan pembacaan konfigurasi. | Pydantic dan pydantic-settings dipakai config; validasi email belum ada. |
| `sqlalchemy[asyncio]` | ORM async, engine, session, dan model. | Dipakai `base.py`, `mixins.py`, dan `session.py`; model belum ada. |
| `asyncpg`, `aiomysql` | Driver async PostgreSQL dan MySQL. | Dicantumkan; koneksi nyata belum diuji atau digunakan oleh endpoint. |
| `alembic` | Migrasi skema database. | Dicantumkan; belum ada konfigurasi atau migrasi. |
| `PyJWT` | Pembuatan/verifikasi JWT. | Belum dipakai. |
| `argon2-cffi` | Hash kata sandi. | Belum dipakai. |
| `cryptography` | Enkripsi identitas dengan Fernet. | Fernet baru dipakai untuk memvalidasi format `ENCRYPTION_KEY`; belum ada enkripsi data. |
| `slowapi` | Rate limit endpoint. | Belum dipakai. |

Dependency development opsional: `pytest`, `pytest-asyncio`, `httpx`, dan `faker` ditujukan untuk test; `ruff`, `mypy`, dan `pre-commit` untuk kualitas kode dan hook. Saat ini tidak ada test maupun hook yang mengimplementasikan alur produk.

## Kondisi Pemeriksaan

- Ruff lint: lulus.
- Ruff format check: lulus untuk 5 file Python.
- mypy: belum lulus. Pemanggilan dari root gagal menemukan modul `app.core.config`; pemanggilan dari folder backend menemukan modul yang sama dengan dua nama (`config` dan `app.core.config`).
- pytest: tidak menemukan test (`0 items`, exit code 5).
- Target `make` tidak dapat dijalankan di lingkungan pemeriksaan karena executable `make` tidak tersedia. Pemeriksaan Ruff, mypy, dan pytest dijalankan langsung melalui interpreter virtualenv backend.

## Langkah Lanjut yang Disarankan

1. Tetapkan status roadmap dan keputusan terbuka SRS/database agar rancangan yang masih asumsi tidak dianggap kontrak final.
2. Lengkapi konfigurasi package Python (termasuk struktur package dan pemetaan mypy), lalu buat entry point FastAPI yang sehat.
3. Tambahkan konfigurasi Alembic async dan migrasi awal; verifikasi dengan database development.
4. Implementasikan satu vertikal fitur secara bertahap: model/schema, service, endpoint, lalu test unit dan integrasi.
5. Buat frontend dan integrasikan melalui kontrak API yang disepakati.
6. Pastikan dokumentasi lokal yang perlu dibagikan tidak berada di folder yang diabaikan Git.
