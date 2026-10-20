# Software Requirements Specification (SRS) “Hidden X”

Platform Microblogging Anonim Bergaya Twitter/X

Mata Kuliah: Web Framework · Dosen Pengampu: Abdul Fikri B.Sc

Disusun oleh: Fadhlun (220212021), Alifi Luthfir Rahman (240212009), Anta Nisa Pratama (230212126)

Status: **Draf rekonstruksi** dari serpihan pada dokumen “Materi dan Teori Tambahan SRS Hidden X” (v3.0, 3 Oktober 2026), mengikuti struktur IEEE Std 830-1998.

> **Catatan penting.** Dokumen ini bukan SRS asli. Butir yang disebut langsung di dokumen sumber ditandai **Dokumen**, sedangkan butir yang saya lengkapi sendiri agar struktur SRS utuh ditandai **Asumsi** dan perlu dicocokkan dengan SRS asli kelompok. Nomor bab mengikuti rujukan silang di dokumen sumber (Bagian 3.3, 6.2, 7.1, 7.2.3, BAB 8, 9, 10, Lampiran 13.2).

## 1. Pendahuluan

### 1.1 Tujuan

Dokumen ini mendeskripsikan kebutuhan fungsional dan non-fungsional Hidden X, platform *microblogging* anonim, sebagai acuan bersama pengembang, dosen, dan penguji.

### 1.2 Ruang Lingkup

Hidden X adalah aplikasi web yang mempertahankan pola interaksi *microblogging* klasik (post, reply, repost, like, follow, hashtag) dengan tambahan lapisan identitas **Anon-ID**. Pengguna tampil ke publik hanya sebagai Anon-ID, sementara identitas asli (email, *username* asli) tersimpan terenkripsi di server dan hanya dapat ditelusuri secara internal untuk kepentingan moderasi dan hukum (pseudonimitas terkelola). Sistem terdiri atas *frontend* Next.js, *backend* FastAPI, dan basis data PostgreSQL/MySQL.

### 1.3 Definisi dan Singkatan

| Istilah | Arti |
| --- | --- |
| Anon-ID | Alias publik pengguna yang menggantikan identitas asli |
| Post | Unggahan teks maksimal 280 karakter |
| Repost / Quote Post | Penyebaran ulang post, tanpa atau dengan komentar |
| Feed | Daftar post dari akun yang di-follow |
| JWT | JSON Web Token (RFC 7519) |
| FR / NFR / UC | Functional Requirement / Non-Functional Requirement / Use Case |

### 1.4 Gambaran Isi Dokumen

Bab 2 memuat referensi, Bab 3 deskripsi umum, Bab 4 dan 5 kebutuhan fungsional dan non-fungsional, Bab 6 antarmuka, Bab 7 arsitektur, Bab 8 model data, Bab 9 use case, Bab 10 rancangan API, Bab 11 batasan dan asumsi, Bab 12 keterlacakan dan pengujian, Bab 13 lampiran.

## 2. Referensi

IEEE Std 830-1998; RFC 7519 (JWT); Fielding (2000) tentang REST; dokumentasi Next.js, FastAPI, dan SQLAlchemy; Suler (2004) dan Christopherson (2007) tentang anonimitas; Gillespie (2018) tentang moderasi konten.

## 3. Deskripsi Umum

### 3.1 Perspektif Produk

Hidden X adalah sistem mandiri berbasis web dengan arsitektur *three-tier*. Pembedanya dari Twitter/X adalah lapisan Anon-ID di antara identitas asli dan tampilan publik. *(Dokumen)*

### 3.2 Fungsi Produk

Fungsi utama dikelompokkan dalam empat modul: Autentikasi, Konten, Sosial, dan Notifikasi, ditambah fungsi moderasi untuk Moderator dan Admin. *(Dokumen, pengelompokan modul; rincian Asumsi)*

### 3.3 Karakteristik Pengguna

| Aktor | Deskripsi | Hak Akses | Sumber |
| --- | --- | --- | --- |
| Guest | Pengunjung belum login | Melihat halaman publik (profil publik Anon-ID), registrasi, login | Dokumen |
| User | Pengguna terdaftar | Membuat post, reply, repost, like, follow, melaporkan konten, menerima notifikasi | Dokumen |
| Moderator | Peninjau laporan | Meninjau dan menindak laporan (hapus post, suspend akun) | Dokumen |
| Admin | Pengelola sistem | Seluruh hak Moderator ditambah pengelolaan pengguna | Dokumen; cakupan tambahan Asumsi |

### 3.4 Batasan Umum

Batas 280 karakter per post; identitas asli tidak boleh tampil ke pengguna lain; komunikasi *client-server* hanya melalui REST API berformat JSON; autentikasi menggunakan JWT.

### 3.5 Asumsi dan Ketergantungan

Pengguna mengakses melalui peramban modern dengan koneksi internet. *(Asumsi)*

## 4. Kebutuhan Fungsional

### 4.1 Modul Autentikasi

| Kode | Nama | Deskripsi | Sumber |
| --- | --- | --- | --- |
| FR-01 | Registrasi | Guest mendaftar dengan email dan data identitas; sistem menerbitkan Anon-ID unik dan menyimpan identitas asli secara terenkripsi | Asumsi |
| FR-02 | Login | Pengguna login dan menerima JWT (access token dan refresh token) | Dokumen |
| FR-03 | Logout | Pengguna mengakhiri sesi dan token tidak lagi dipakai | Asumsi |
| FR-04 | Pembaruan Token | Pengguna menukarkan refresh token dengan access token baru | Dokumen (endpoint /auth/refresh) |

### 4.2 Modul Konten

| Kode | Nama | Deskripsi | Sumber |
| --- | --- | --- | --- |
| FR-05 | Membuat Post Baru | User membuat post teks maksimal 280 karakter, opsional dengan gambar; divalidasi di backend | Dokumen |
| FR-06 | Menghapus Post | User menghapus post miliknya sendiri | Asumsi |
| FR-07 | Like / Unlike | User menyukai atau membatalkan suka pada post | Dokumen (endpoint like) |
| FR-08 | Reply | User membalas post sehingga membentuk percakapan berulir (*thread*) | Dokumen |
| FR-09 | Repost / Quote Post | User menyebarkan ulang post, dengan atau tanpa komentar | Dokumen |

### 4.3 Modul Sosial

| Kode | Nama | Deskripsi | Sumber |
| --- | --- | --- | --- |
| FR-10 | Follow / Unfollow | User mengikuti atau berhenti mengikuti Anon-ID lain | Asumsi (tabel follows tersurat) |
| FR-11 | Feed Following | Menampilkan post terbaru dari akun yang di-follow | Dokumen (halaman beranda) |
| FR-12 | Profil Publik Anon-ID | Menampilkan profil dan post suatu Anon-ID, dapat dilihat Guest | Dokumen |
| FR-13 | Trending Hashtag | Menampilkan hashtag berdasarkan frekuensi penggunaan dalam 24 jam terakhir | Dokumen |
| FR-14 | Pencarian | Mencari post atau Anon-ID berdasarkan kata kunci atau hashtag | Asumsi |

### 4.4 Modul Moderasi dan Notifikasi

| Kode | Nama | Deskripsi | Sumber |
| --- | --- | --- | --- |
| FR-15 | Melaporkan Post/Akun | User melaporkan konten dengan memilih kategori alasan (spam, ujaran kebencian, dan lainnya) | Dokumen |
| FR-16 | Meninjau dan Menindak Laporan | Moderator/Admin meninjau antrean laporan, lalu menghapus post, menangguhkan akun, atau menolak laporan | Dokumen |
| FR-17 | Notifikasi | Sistem memberi tahu User atas like, reply, repost, follower baru, dan hasil laporan | Asumsi |

Alur status laporan *(Dokumen)*: **menunggu tinjauan** → **sedang ditinjau** → **ditindaklanjuti** atau **ditolak**.

## 5. Kebutuhan Non-Fungsional

| Kode | Kategori | Deskripsi | Sumber |
| --- | --- | --- | --- |
| NFR-01 | Keamanan data | Identitas asli (email, username asli) disimpan terenkripsi; kata sandi disimpan sebagai *hash* | Dokumen; hash Asumsi |
| NFR-02 | Keamanan sesi | Access token JWT berlaku 15–60 menit; perpanjangan lewat refresh token | Dokumen |
| NFR-03 | Kinerja | Halaman feed dimuat dalam ≤ 3 detik pada kondisi normal | Asumsi |
| NFR-04 | Ketersediaan | Layanan tersedia selama jam operasional uji tanpa gangguan berarti | Asumsi |
| NFR-05 | Skalabilitas | Lapisan frontend, backend, dan data dapat dikembangkan dan di-*deploy* terpisah | Asumsi (dari pola three-tier) |
| NFR-06 | Kegunaan | Antarmuka responsif pada peramban modern desktop dan seluler | Asumsi |
| NFR-07 | Keterpeliharaan | API terdokumentasi otomatis (Swagger/OpenAPI) dan kode memakai ORM sehingga mesin basis data mudah diganti | Asumsi (dari tech stack) |
| NFR-08 | Privasi | Identitas asli tidak pernah dikirim atau ditampilkan kepada pengguna lain; publik hanya melihat Anon-ID | Dokumen |

## 6. Kebutuhan Antarmuka

### 6.1 Antarmuka Pengguna

Aplikasi web Next.js (App Router). Halaman utama: beranda/feed, profil Anon-ID, detail post dan thread, pencarian dan trending, notifikasi, serta panel Moderator/Admin. Beranda memakai SSR agar data selalu terbaru; profil publik dapat memakai SSG. *(Dokumen; daftar halaman sebagian Asumsi)*

### 6.2 Antarmuka Komunikasi

Seluruh komunikasi Next.js dan FastAPI memakai REST API berformat JSON melalui HTTP, dengan header `Authorization: Bearer <access_token>` untuk *endpoint* terproteksi. Contoh: `POST /posts` dijawab `201 Created`, sedangkan validasi gagal dijawab `422 Unprocessable Entity`. *(Dokumen)*

### 6.3 Antarmuka Perangkat Lunak

FastAPI berinteraksi dengan PostgreSQL/MySQL melalui SQLAlchemy (ORM). *(Dokumen)*

## 7. Arsitektur dan Teknologi

### 7.1 Arsitektur Sistem

Arsitektur *three-tier*: *presentation layer* (Next.js di sisi klien), *application layer* (FastAPI: autentikasi, validasi post, moderasi), dan *data layer* (PostgreSQL/MySQL). Pemisahan ini memungkinkan tim frontend bekerja dengan data tiruan sambil menunggu *endpoint* backend selesai. *(Dokumen)*

### 7.2 Tech Stack

#### 7.2.1 Frontend

Next.js (React) dengan strategi rendering SSR/SSG.

#### 7.2.2 Backend

FastAPI (ASGI) dengan validasi Pydantic, SQLAlchemy sebagai ORM, dan JWT untuk autentikasi.

#### 7.2.3 Basis Data

PostgreSQL/MySQL dipilih karena data relasional yang saling berkaitan (users, posts, follows, likes, reports) dan dukungan transaksi ACID. *(Dokumen)*

## 8. Model Data

### 8.1 Entitas dan Atribut

Atribut yang tidak disebut di dokumen sumber adalah **Asumsi**.

| Tabel | Atribut utama |
| --- | --- |
| users | id (PK), anon\_id, email (terenkripsi), username\_asli (terenkripsi), password\_hash, role (user/moderator/admin), status (aktif/suspend), created\_at |
| posts | id (PK), anon\_id (FK → users.id), content (VARCHAR 280, wajib), image\_url, parent\_id (untuk reply, Asumsi), created\_at |
| follows | follower\_id (FK), followed\_id (FK) |
| likes | user\_id (FK), post\_id (FK), created\_at |
| reports | id (PK), reporter\_id (FK), target\_post\_id / target\_user\_id, kategori, status, handled\_by (FK), created\_at |

### 8.2 Relasi dan Kardinalitas

User–Post: 1:N. User–Follow–User: N:M melalui tabel follows. Post–Like–User: N:M melalui tabel likes. User–Report: 1:N (satu pengguna dapat membuat banyak laporan). *(User–Post, Follow, Like: Dokumen; Report: Asumsi)*

Catatan konsistensi: dokumen sumber memakai `anon_id` sebagai kolom integer FK ke `users.id` pada tabel, tetapi sebagai string (mis. “kabut\_senja92”) pada payload JWT. Kelompok perlu menetapkan satu representasi (misalnya `users.id` untuk FK dan `users.anon_id` untuk tampilan).

## 9. Use Case

Aktor: Guest, User, Moderator, Admin. Dua belas use case:

| Kode | Use Case | Aktor | Sumber |
| --- | --- | --- | --- |
| UC-01 | Registrasi | Guest | Asumsi |
| UC-02 | Login | Guest | Asumsi |
| UC-03 | Melihat Profil Publik dan Trending | Guest, User | Asumsi |
| UC-04 | Membuat Post | User | Asumsi |
| UC-05 | Like / Unlike Post | User | Asumsi |
| UC-06 | Reply Post | User | Asumsi |
| UC-07 | Repost / Quote Post | User | Asumsi |
| UC-08 | Follow / Unfollow | User | Asumsi |
| UC-09 | Melihat Feed dan Notifikasi | User | Asumsi |
| UC-10 | Melaporkan Post/Akun | User | Dokumen |
| UC-11 | Meninjau dan Menindak Laporan | Moderator, Admin | Dokumen |
| UC-12 | Mengelola Pengguna | Admin | Asumsi |

UC-10 memiliki relasi *include* ke use case “Memilih Kategori Pelanggaran”. *(Dokumen)*

## 10. Rancangan API

Base URL: `https://api.hiddenx.app`. Semua *endpoint* bertanda 🔒 memerlukan header Bearer token.

| Metode | Endpoint | Fungsi | FR | Sumber |
| --- | --- | --- | --- | --- |
| POST | /auth/register | Registrasi | FR-01 | Asumsi |
| POST | /auth/login | Login, menerbitkan JWT | FR-02 | Dokumen |
| POST | /auth/logout 🔒 | Logout | FR-03 | Asumsi |
| POST | /auth/refresh | Menukar refresh token | FR-04 | Dokumen |
| POST | /posts 🔒 | Membuat post (201 Created) | FR-05 | Dokumen |
| DELETE | /posts/{id} 🔒 | Menghapus post sendiri | FR-06 | Asumsi |
| POST | /posts/{id}/like 🔒 | Like post | FR-07 | Dokumen |
| POST | /posts/{id}/reply 🔒 | Membalas post | FR-08 | Asumsi |
| POST | /posts/{id}/repost 🔒 | Repost / quote | FR-09 | Asumsi |
| POST | /users/{anon\_id}/follow 🔒 | Follow / unfollow | FR-10 | Asumsi |
| GET | /posts/feed 🔒 | Feed following | FR-11 | Dokumen |
| GET | /users/{anon\_id} | Profil publik | FR-12 | Asumsi |
| GET | /trending | Hashtag trending 24 jam | FR-13 | Asumsi |
| GET | /search | Pencarian | FR-14 | Asumsi |
| POST | /reports 🔒 | Membuat laporan | FR-15 | Asumsi |
| GET / PATCH | /admin/reports 🔒 | Antrean dan tindak lanjut laporan | FR-16 | Dokumen |
| GET | /notifications 🔒 | Daftar notifikasi | FR-17 | Asumsi |

Contoh permintaan `POST /posts` (Dokumen): isi JSON berupa `content` (maks. 280 karakter) dan `image_url` (boleh kosong); balasan memuat `id`, `anon_id`, `content`, dan `created_at`.

## 11. Batasan, Asumsi, dan Risiko

Pseudonimitas terkelola menuntut pemisahan ketat antara tabel identitas asli dan data publik. Risiko utama: penyalahgunaan akibat anonimitas (*toxic disinhibition*), yang dimitigasi lewat pelaporan komunitas dan moderasi manusia (FR-15, FR-16). Kebocoran identitas asli dimitigasi oleh NFR-01 dan NFR-08. Akses penelusuran identitas asli hanya untuk kebutuhan hukum dan perlu dibatasi pada peran tertentu *(Asumsi)*.

## 12. Keterlacakan dan Pengujian

Setiap FR ditelusuri ke *endpoint* (Bab 10), use case (Bab 9), dan kasus uji. Contoh dari dokumen sumber: FR-05 → POST /posts → uji unit validasi 280 karakter (harus ditolak 422) dan uji integrasi pembuatan post (201 Created). Kasus uji lain disusun kelompok pada tahap pengujian.

## 13. Lampiran

### 13.1 Daftar Pustaka

Mengacu pada daftar pustaka dokumen “Materi dan Teori Tambahan SRS Hidden X”.

### 13.2 Saran Pengembangan ERD

Sempurnakan ERD menjadi notasi *Crow’s Foot* formal menggunakan draw.io atau dbdiagram.io sebelum implementasi skema fisik di PostgreSQL/MySQL. *(Dokumen)*

backend planned structure
hiddenx-backend/
├── app/
│   ├── main.py                    # Entry point FastAPI, CORS, include router, exception handler
│   │
│   ├── core/                      # Konfigurasi dan komponen lintas modul
│   │   ├── config.py              # Settings (pydantic-settings), baca dari .env
│   │   ├── security.py            # Buat/verifikasi JWT, hash kata sandi (NFR-02)
│   │   ├── crypto.py              # Enkripsi identitas asli (Fernet) + HMAC untuk lookup (NFR-01)
│   │   ├── exceptions.py          # Custom exception dan handler error seragam
│   │   ├── rate_limit.py          # Pembatasan laju request (login, post, report)
│   │   └── logging.py
│   │
│   ├── db/
│   │   ├── base.py                # DeclarativeBase + import semua model (untuk Alembic)
│   │   ├── session.py             # Async engine, sessionmaker, dependency get_db
│   │   └── mixins.py              # TimestampMixin (created_at, updated_at)
│   │
│   ├── models/                    # SQLAlchemy ORM (satu file per tabel)
│   │   ├── user.py                # users: anon_id, email_enc, email_hash, role, status
│   │   ├── post.py                # posts: content(280), image_url, parent_id, repost_of_id
│   │   ├── follow.py              # follows (junction N:M)
│   │   ├── like.py                # likes (junction N:M)
│   │   ├── hashtag.py             # hashtags + post_hashtags (untuk FR-13 trending)
│   │   ├── report.py              # reports + enum status laporan
│   │   ├── notification.py        # notifications (FR-17)
│   │   └── refresh_token.py       # refresh_tokens (FR-03, FR-04)
│   │
│   ├── schemas/                   # Pydantic: validasi request dan bentuk response
│   │   ├── auth.py                # RegisterIn, LoginIn, TokenOut
│   │   ├── user.py                # PublicProfileOut (tanpa identitas asli)
│   │   ├── post.py                # PostCreate (max_length=280), PostOut
│   │   ├── report.py
│   │   ├── notification.py
│   │   └── common.py              # Pagination, ErrorResponse
│   │
│   ├── services/                  # Logika bisnis (router tipis, logika di sini)
│   │   ├── auth_service.py        # Register, login, refresh, logout, generate Anon-ID
│   │   ├── post_service.py        # Buat/hapus post, reply, repost, ekstrak hashtag
│   │   ├── social_service.py      # Follow, like, feed following
│   │   ├── trending_service.py    # Hashtag 24 jam terakhir
│   │   ├── search_service.py
│   │   ├── report_service.py      # Buat laporan, transisi status
│   │   ├── notification_service.py
│   │   └── admin_service.py       # Suspend akun, kelola pengguna
│   │
│   ├── api/
│   │   ├── deps.py                # get_current_user, require_role("moderator"/"admin")
│   │   └── v1/
│   │       ├── router.py          # Gabungkan semua endpoint di prefix /api/v1
│   │       └── endpoints/
│   │           ├── auth.py        # /auth/register, /login, /logout, /refresh
│   │           ├── posts.py       # /posts, /posts/feed, /posts/{id}/like|reply|repost
│   │           ├── users.py       # /users/{anon_id}, /users/{anon_id}/follow
│   │           ├── trending.py    # /trending
│   │           ├── search.py      # /search
│   │           ├── reports.py     # /reports
│   │           ├── notifications.py
│   │           └── admin.py       # /admin/reports, /admin/users
│   │
│   └── utils/
│       ├── anon_id.py             # Generator alias unik (mis. kabut_senja92)
│       └── hashtag.py             # Parser hashtag dari teks post
│
├── alembic/                       # Migrasi database
│   ├── env.py                     # Dikonfigurasi async + membaca URL dari settings
│   ├── script.py.mako
│   └── versions/                  # File migrasi hasil autogenerate
├── alembic.ini
│
├── tests/
│   ├── conftest.py                # Fixture: DB uji, AsyncClient, user/token contoh
│   ├── unit/                      # Uji service dan utilitas (validasi 280 karakter, JWT)
│   └── integration/               # Uji endpoint (POST /posts → 201, 422)
│
├── scripts/
│   ├── create_admin.py            # Buat akun Admin pertama
│   └── seed_data.py               # Data contoh untuk pengembangan frontend
│
├── .env.example                   # DATABASE_URL, SECRET_KEY, ENCRYPTION_KEY, dll.
├── .gitignore
├── .pre-commit-config.yaml
├── pyproject.toml                 # Dependensi + konfigurasi ruff, pytest, mypy
├── Dockerfile
├── docker-compose.yml             # Backend + PostgreSQL (+ Redis opsional)
├── Makefile                       # Shortcut: make run, migrate, test, lint
└── README.md
