# ROADMAP

Urutan pengerjaan backend dan database. Centang item saat selesai (agent boleh memperbarui
file ini setelah menyelesaikan tugas). Fase bersifat usulan; sesuaikan dengan jadwal tim.

## Fase 0 — Fondasi
- [ ] Inisialisasi proyek (`pyproject.toml`, ruff, mypy, pre-commit, Makefile)
- [ ] `core/config.py`, `.env.example`, `docker-compose.yml` (PostgreSQL)
- [ ] `db/base.py` (naming convention), `db/session.py` (async), `db/mixins.py`
- [ ] Setup Alembic async + migrasi kosong pertama
- [ ] `main.py`: CORS, router v1, exception handler seragam, endpoint `/health`
- [ ] Setup pytest: `conftest.py`, DB uji, fixture dasar

## Fase 1 — Autentikasi (FR-01 s.d. FR-04, NFR-01, NFR-02)
- [ ] Model `users`, `refresh_tokens` + migrasi
- [ ] `core/crypto.py` (Fernet + HMAC), `core/security.py` (argon2, JWT)
- [ ] `utils/anon_id.py` (generator alias unik)
- [ ] Register, login, refresh (rotasi), logout
- [ ] `api/deps.py`: `get_current_user`, `require_role`
- [ ] Rate limiting login/register
- [ ] Test: alur auth lengkap, token kedaluwarsa, akun suspend, kebocoran identitas

## Fase 2 — Konten (FR-05 s.d. FR-09)
- [ ] Model `posts`, `likes`, `hashtags`, `post_hashtags` + migrasi
- [ ] Buat post (280 karakter) + ekstraksi hashtag
- [ ] Hapus post (soft delete), detail post dan thread
- [ ] Like/unlike, reply, repost/quote
- [ ] Test: batas 280, kepemilikan, duplikat like

## Fase 3 — Sosial (FR-10 s.d. FR-14)
- [ ] Model `follows` + migrasi
- [ ] Follow/unfollow, feed following (cursor pagination)
- [ ] Profil publik Anon-ID (akses Guest)
- [ ] Trending hashtag 24 jam, pencarian
- [ ] Test: feed hanya berisi akun yang di-follow, pagination stabil

## Fase 4 — Moderasi dan Notifikasi (FR-15 s.d. FR-17)
- [ ] Model `reports`, `notifications` + migrasi
- [ ] Buat laporan, antrean laporan, transisi status (pending → reviewing → actioned/rejected)
- [ ] Tindak lanjut: hapus post, suspend akun; audit log
- [ ] Notifikasi untuk like, reply, repost, follower baru, hasil laporan
- [ ] Test: peran Moderator/Admin, transisi status valid dan tidak valid

## Fase 5 — Pengerasan dan Rilis
- [ ] Tinjau index dan performa query feed/trending (EXPLAIN)
- [ ] Review keamanan memakai checklist `SECURITY.md`
- [ ] `scripts/seed_data.py`, `scripts/create_admin.py`
- [ ] Dockerfile produksi, konfigurasi env produksi, matikan `/docs` bila perlu
- [ ] Sinkronkan SRS dengan hasil akhir (DEC-01 s.d. DEC-03, endpoint, tabel tambahan)
- [ ] Dokumentasi README dan panduan deploy

## Catatan Prioritas

Jika waktu terbatas, urutan minimum yang tetap memenuhi inti produk:
Fase 0 → 1 → 2 → 3 (tanpa pencarian) → 4 (laporan dan antrean saja).
