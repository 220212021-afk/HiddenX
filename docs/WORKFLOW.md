# WORKFLOW

## 1. Setup Lokal

```powershell
# Jalankan perintah dari root repo.
Copy-Item backend\.env.example backend\.env
docker compose -f backend\docker-compose.yml up -d db
make install
make migrate
python backend\scripts\create_admin.py
make run                      # http://localhost:8000/docs
```

Menghasilkan kunci:
```bash
python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"
python -c "import secrets; print(secrets.token_urlsafe(48))"
```

## 2. Git

- Branch dari `main`: `feat/...`, `fix/...`, `chore/...`, `docs/...`.
- Commit mengikuti Conventional Commits (bahasa Inggris):
  `feat(posts): add 280-char validation`, `fix(auth): revoke refresh token on logout`,
  `chore(db): add index on posts.created_at`.
- Satu commit = satu perubahan logis; migrasi dan model terkait boleh satu commit.
- Pull request kecil (idealnya < 400 baris diff), minimal satu reviewer anggota tim.
- Jangan push langsung ke `main`; jangan force push.
- Agent **tidak** melakukan `git push` atau membuka PR kecuali diminta.

## 3. Strategi Testing

| Jenis | Lokasi | Isi |
| --- | --- | --- |
| Unit | `backend/tests/unit/` | Service, util (anon_id, hashtag), keamanan (JWT, enkripsi) tanpa jaringan |
| Integrasi | `backend/tests/integration/` | Endpoint via `httpx.AsyncClient` + DB uji nyata |

- DB uji terpisah dari DB dev (`hiddenx_test`), dibuat bersih tiap sesi; gunakan transaksi
  rollback per test atau truncate.
- Fixture di `backend/tests/conftest.py`: `db`, `client`, `make_user`, `auth_headers`.
- Target awal: seluruh FR yang sudah diimplementasikan punya minimal satu test jalur normal
  dan satu jalur gagal.
- Test wajib untuk aturan inti:
  - post 281 karakter → 422; 280 karakter → 201 (FR-05)
  - response tidak memuat `email`, `email_enc`, `email_hash`, `password_hash` (NFR-08)
  - token kedaluwarsa → 401 (NFR-02)
  - User biasa mengakses `/admin/reports` → 403
  - akun suspend tidak bisa login/posting

## 4. Alur Mengerjakan Satu Fitur

1. Baca butir SRS (FR/UC) dan dokumen terkait; tulis rencana singkat bila tugas besar.
2. Skema/model → migrasi → schemas → service → endpoint → test (urutan ini).
3. Jalankan `make lint` dan `make test`.
4. Perbarui `docs/API.md` / `docs/DATABASE.md` bila perlu.
5. Commit, lalu ringkas: apa berubah, apa diuji, apa yang belum.

## 5. CI (disarankan)

Pipeline minimal pada setiap PR: install → `ruff` → `mypy` → `alembic upgrade head` pada DB
kosong → `pytest`. Gagal di salah satu langkah memblokir merge.

## 6. Pembagian Kerja (usulan, sesuaikan tim)

| Area | Modul |
| --- | --- |
| Anggota A | Fondasi (core, db, config), autentikasi |
| Anggota B | Konten dan sosial (posts, likes, follow, feed, trending, search) |
| Anggota C | Moderasi, notifikasi, admin, pengujian dan dokumentasi |

Kontrak `docs/API.md` disepakati dulu agar frontend bisa jalan dengan data tiruan.

## 7. Troubleshooting Umum

| Gejala | Kemungkinan penyebab |
| --- | --- |
| `MissingGreenlet` | Lazy loading di konteks async; muat relasi dengan `selectinload` |
| Autogenerate Alembic kosong | Model belum diimpor di `backend/app/db/base.py` |
| Login selalu gagal setelah ganti kunci | `HMAC_KEY` berubah sehingga `email_hash` lama tak cocok |
| 422 pada body valid | Cek skema `extra="forbid"` dan nama field |
