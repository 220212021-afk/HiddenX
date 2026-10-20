# AGENTS.md — Hidden X Backend

Panduan utama untuk agent CLI (Claude Code, Codex, Gemini CLI, dll.) yang bekerja di repo ini.
Baca file ini sepenuhnya sebelum mengubah kode. Detail ada di folder `docs/`.

## 1. Tentang Proyek

Hidden X adalah platform microblogging anonim bergaya Twitter/X. Pengguna tampil ke publik
hanya sebagai **Anon-ID**; identitas asli (email, username asli) disimpan terenkripsi di server.

- **backend** dan **database** berada dalam `backend/`
- **frontend** berada dalam `frontend/`
- Stack: Python, FastAPI (async), SQLAlchemy 2.x (async), Alembic, PostgreSQL/MySQL, JWT.
- Mata kuliah Web Framework; tim 3 orang. Utamakan kode yang sederhana dan mudah dijelaskan.

## 2. Peta Dokumentasi

Baca dokumen yang relevan sebelum mengerjakan tugas terkait.

| Dokumen | Baca bila tugas menyangkut |
| --- | --- |
| `docs/ARCHITECTURE.md` | Struktur folder, pembagian layer, alur request |
| `docs/CONVENTIONS.md` | Gaya kode, penamaan, format error, pagination |
| `docs/DATABASE.md` | Model, relasi, migrasi Alembic, keputusan skema |
| `docs/SECURITY.md` | Auth, JWT, enkripsi, privasi identitas, logging |
| `docs/API.md` | Kontrak endpoint dan kode status |
| `docs/WORKFLOW.md` | Git, testing, definisi selesai, perintah harian |
| `docs/ROADMAP.md` | Urutan fase pengerjaan dan status |

## 3. Aturan Mutlak (jangan dilanggar)

1. **Identitas asli tidak boleh bocor.** Kolom `email_enc`, `email_hash`, `username_asli_enc`,
   `password_hash` tidak boleh muncul di response, log, pesan error, atau notifikasi.
   Response selalu lewat skema Pydantic eksplisit (whitelist), tidak pernah model ORM mentah.
2. **Layering wajib:** `endpoints → services → models`. Endpoint tidak berisi query SQL atau
   logika bisnis. Service tidak mengimpor apa pun dari `fastapi`.
3. **Semua I/O async.** Pakai `AsyncSession` dan driver async. Dilarang memanggil fungsi
   blocking (`requests`, `time.sleep`, driver sync) di dalam handler async.
4. **Perubahan skema hanya lewat migrasi Alembic.** Jangan `Base.metadata.create_all()` di
   luar test, jangan ubah tabel manual, dan **jangan edit file migrasi yang sudah ter-commit**.
5. **Batas 280 karakter ditegakkan di tiga tempat:** skema Pydantic, constraint DB, dan test.
6. **Jangan commit rahasia.** `.env`, kunci enkripsi, dan `SECRET_KEY` tidak pernah masuk git.
   Perbarui `.env.example` (tanpa nilai asli) bila menambah variabel baru.
7. **Jangan menjalankan perintah destruktif** (drop database, `alembic downgrade base`,
   `rm -rf`, `git push --force`, `git reset --hard`) tanpa persetujuan eksplisit dari pengguna.

## 4. Perilaku Agent

- **Mulai dengan membaca**, bukan menulis: lihat file terkait dan dokumen relevan dulu.
- **Rencanakan dulu untuk tugas besar** (menyentuh lebih dari 3 file atau mengubah skema):
  tulis rencana singkat dan minta konfirmasi sebelum mengeksekusi.
- **Diff kecil dan terfokus.** Satu tugas = satu perubahan logis. Jangan refactor di luar
  lingkup tugas; catat sebagai saran di akhir.
- **Jangan menambah dependensi** tanpa menyebutkan alasannya, lalu catat di `pyproject.toml`
  dan `docs/ARCHITECTURE.md` bagian dependensi.
- **Jangan menebak requirement.** Bila SRS atau dokumen ambigu, tanyakan. Bila butir bertanda
  *Asumsi* di SRS menghalangi pekerjaan, ajukan usulan, jangan putuskan diam-diam.
- **Jangan mengubah SRS atau keputusan di `docs/`** tanpa memberi tahu. Bila perlu menyimpang,
  jelaskan alasannya dan usulkan pembaruan dokumen.
- **Jujur soal hasil.** Laporkan test yang gagal, perintah yang tidak bisa dijalankan, dan
  hal yang belum diverifikasi. Jangan menyatakan "selesai" tanpa menjalankan test.
- **Perbarui dokumen** bila perubahan kode mengubah kontrak API, skema, atau perintah.

## 5. Perintah Harian

```bash
make install     # pasang dependensi
make run         # jalankan server dev (uvicorn --reload)
make migrate     # alembic upgrade head
make revision m="pesan"   # alembic revision --autogenerate -m "pesan"
make test        # pytest
make lint        # ruff check + ruff format --check + mypy
make format      # ruff format + ruff check --fix
```

Bila target `make` belum ada, buat di `Makefile` sesuai daftar di atas.

## 6. Definisi Selesai (Definition of Done)

Sebuah tugas baru dianggap selesai bila:

- [ ] Kode mengikuti `docs/CONVENTIONS.md` dan layering di atas
- [ ] `make lint` bersih
- [ ] Test baru ditulis untuk perilaku baru (unit dan/atau integrasi), `make test` hijau
- [ ] Migrasi dibuat dan sudah ditinjau jika skema berubah (upgrade dan downgrade jalan)
- [ ] Tidak ada data sensitif di response/log
- [ ] `docs/API.md` / `docs/DATABASE.md` diperbarui bila kontraknya berubah
- [ ] Ringkasan perubahan ditulis: apa yang diubah, apa yang diuji, apa yang belum

## 7. Referensi SRS

Kode kebutuhan dipakai untuk keterlacakan: `FR-xx` (fungsional), `NFR-xx` (non-fungsional),
`UC-xx` (use case). Cantumkan kode terkait di docstring service dan nama test, misalnya
`test_fr05_post_over_280_chars_rejected`.
