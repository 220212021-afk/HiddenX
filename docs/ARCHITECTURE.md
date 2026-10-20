# ARCHITECTURE

## 1. Gambaran

Arsitektur three-tier. Repo ini mencakup application layer dan data layer.

```
Next.js (repo lain)  --REST/JSON-->  FastAPI (repo ini)  --SQLAlchemy async-->  PostgreSQL/MySQL
```

## 2. Struktur Folder

```
app/
├── main.py            # entry point, CORS, router, exception handler
├── core/              # config, security (JWT/hash), crypto (enkripsi), exceptions, rate_limit, logging
├── db/                # base, session, mixins
├── models/            # SQLAlchemy ORM, satu file per tabel
├── schemas/           # Pydantic: request dan response
├── services/          # logika bisnis
├── api/
│   ├── deps.py        # get_current_user, require_role
│   └── v1/
│       ├── router.py
│       └── endpoints/ # auth, posts, users, trending, search, reports, notifications, admin
└── utils/             # anon_id, hashtag
alembic/               # migrasi
tests/                 # unit/ dan integration/
scripts/               # create_admin.py, seed_data.py
```

## 3. Aturan Dependensi Antar-Layer

```
endpoints  →  services  →  models
    ↓            ↓
 schemas      schemas
```

| Layer | Boleh | Tidak boleh |
| --- | --- | --- |
| `endpoints` | Parse request, panggil service, kembalikan schema, atur status code | Query SQL, logika bisnis, akses `models` langsung |
| `services` | Logika bisnis, query lewat `AsyncSession`, melempar exception domain | Impor `fastapi`, mengembalikan objek `Response` |
| `models` | Definisi tabel, relasi, constraint | Logika bisnis, impor `services` |
| `schemas` | Validasi dan bentuk data | Akses DB |
| `core` | Dipakai semua layer | Impor `services` atau `endpoints` |

## 4. Alur Request (contoh `POST /posts`, FR-05)

1. Endpoint menerima body, Pydantic memvalidasi `PostCreate` (maks. 280 karakter, otomatis 422).
2. `deps.get_current_user` memverifikasi JWT dan memuat user aktif.
3. Endpoint memanggil `post_service.create_post(db, user, data)`.
4. Service menyimpan post, mengekstrak hashtag (`utils/hashtag.py`), lalu `commit`.
5. Endpoint mengembalikan `PostOut` dengan status `201`. Identitas asli tidak ikut.

## 5. Manajemen Sesi Database

- Satu `AsyncSession` per request lewat dependency `get_db`.
- **Transaksi dikontrol di service**, bukan endpoint. `get_db` hanya membuka dan menutup sesi.
- Gunakan `selectinload`/`joinedload` eksplisit untuk relasi. Hindari lazy loading di konteks
  async (akan error) dan hindari pola N+1 pada feed.

## 6. Konfigurasi

Semua konfigurasi lewat `app/core/config.py` (pydantic-settings) dari environment variable.
Jangan memanggil `os.environ` langsung di tempat lain.

Variabel minimum di `.env.example`:

```
APP_ENV=development
DATABASE_URL=postgresql+asyncpg://user:pass@localhost:5432/hiddenx
SECRET_KEY=ganti-dengan-nilai-acak-panjang
ENCRYPTION_KEY=ganti-dengan-kunci-fernet
HMAC_KEY=ganti-dengan-kunci-hmac
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
CORS_ORIGINS=http://localhost:3000
```

## 7. Daftar Dependensi

Setiap dependensi baru dicatat di sini beserta alasannya.

| Library | Alasan |
| --- | --- |
| fastapi, uvicorn | Framework dan server ASGI |
| pydantic, pydantic-settings, email-validator | Validasi dan konfigurasi |
| sqlalchemy (2.x async), asyncpg / aiomysql | ORM dan driver |
| alembic | Migrasi |
| pyjwt | JWT (NFR-02) |
| argon2-cffi | Hash kata sandi |
| cryptography | Enkripsi identitas (NFR-01) |
| slowapi | Rate limiting |
| pytest, pytest-asyncio, httpx, faker | Pengujian |
| ruff, mypy, pre-commit | Kualitas kode |

Versi dipin di `pyproject.toml`; cek rilis terbaru saat menginstal.

## 8. Versioning API

Semua endpoint di bawah prefix `/api/v1`. Perubahan yang merusak kompatibilitas
(menghapus/mengubah field) memerlukan `v2`, bukan modifikasi `v1`.
