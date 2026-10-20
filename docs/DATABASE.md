# DATABASE

## 1. Keputusan Terbuka (perlu konfirmasi tim)

| ID | Isu | Usulan default (dipakai agent sampai dikonfirmasi) |
| --- | --- | --- |
| DEC-01 | SRS memakai `posts.anon_id` sebagai FK integer ke `users.id`, tetapi di JWT `anon_id` berupa string | Kolom FK bernama `user_id` (integer). `users.anon_id` (string unik) hanya untuk tampilan publik dan JWT |
| DEC-02 | PostgreSQL atau MySQL | **PostgreSQL** + driver `asyncpg`. Kode harus tetap netral dialek lewat ORM |
| DEC-03 | Soft delete atau hard delete untuk post | Soft delete (`deleted_at`) agar laporan moderasi tetap bisa ditinjau |

Setelah tim memutuskan, perbarui tabel ini dan SRS (Bab 8).

## 2. Skema

Atribut bertanda (*) adalah usulan di luar SRS yang tersurat.

### users
| Kolom | Tipe | Catatan |
| --- | --- | --- |
| id | integer PK | internal, tidak dibuka ke publik |
| anon_id | varchar(30) UNIQUE NOT NULL | alias publik |
| email_enc | text NOT NULL | email terenkripsi (Fernet) |
| email_hash | varchar(64) UNIQUE NOT NULL | HMAC-SHA256 email ternormalisasi, untuk lookup login (*) |
| username_asli_enc | text | identitas asli terenkripsi |
| password_hash | text NOT NULL | argon2 |
| role | enum(user, moderator, admin) | default `user` |
| status | enum(active, suspended) | default `active` |
| created_at, updated_at | timestamptz | |

### posts
| Kolom | Tipe | Catatan |
| --- | --- | --- |
| id | integer PK | |
| user_id | integer FK → users.id NOT NULL | lihat DEC-01 |
| content | varchar(280) NOT NULL | CHECK `char_length(content) <= 280` |
| image_url | text NULL | |
| parent_id | integer FK → posts.id NULL | reply (FR-08) (*) |
| repost_of_id | integer FK → posts.id NULL | repost/quote (FR-09) (*) |
| deleted_at | timestamptz NULL | soft delete (DEC-03) |
| created_at | timestamptz | |

### follows
`follower_id` FK, `followed_id` FK, `created_at`. PK gabungan `(follower_id, followed_id)`,
CHECK `follower_id <> followed_id`.

### likes
`user_id` FK, `post_id` FK, `created_at`. PK gabungan `(user_id, post_id)`.

### hashtags dan post_hashtags (*)
`hashtags(id, tag UNIQUE lowercase)`; `post_hashtags(post_id, hashtag_id, created_at)` PK gabungan.
Dipakai FR-13 (trending 24 jam: hitung `post_hashtags` dengan `created_at` dalam 24 jam terakhir).

### reports
| Kolom | Tipe | Catatan |
| --- | --- | --- |
| id | integer PK | |
| reporter_id | integer FK → users.id | |
| target_post_id | integer FK NULL | |
| target_user_id | integer FK NULL | CHECK minimal salah satu target terisi |
| category | enum(spam, hate_speech, harassment, other) | kategori final menunggu SRS |
| status | enum(pending, reviewing, actioned, rejected) | memetakan: menunggu tinjauan, sedang ditinjau, ditindaklanjuti, ditolak |
| handled_by | integer FK → users.id NULL | |
| created_at, updated_at | timestamptz | |

### notifications (*)
`id`, `user_id` (penerima), `type`, `actor_id` NULL, `post_id` NULL, `is_read`, `created_at`.

### refresh_tokens (*)
`id`, `user_id`, `token_hash` (SHA-256, jangan simpan token mentah), `expires_at`,
`revoked_at` NULL, `created_at`.

## 3. Index yang Diharapkan

- `users(anon_id)`, `users(email_hash)` — unik
- `posts(user_id, created_at DESC)` — profil dan feed
- `posts(created_at DESC, id DESC)` — cursor pagination
- `posts(parent_id)` — thread reply
- `follows(followed_id)` — hitung follower
- `post_hashtags(hashtag_id, created_at)` — trending
- `reports(status, created_at)` — antrean moderator
- `notifications(user_id, is_read, created_at DESC)`

## 4. Naming Convention Constraint

Set `naming_convention` di `MetaData` pada `backend/app/db/base.py` agar Alembic menghasilkan nama
constraint yang konsisten dan bisa di-drop:

```python
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}
```

## 5. Aturan Migrasi (Alembic)

1. Setiap perubahan model diikuti `make revision m="..."`; **tinjau hasil autogenerate** karena
   tidak selalu menangkap perubahan enum, constraint, atau rename.
2. Satu migrasi = satu perubahan logis, pesan singkat dan deskriptif (bahasa Inggris).
3. Migrasi harus punya `downgrade()` yang berfungsi. Uji `upgrade head` lalu `downgrade -1`
   lalu `upgrade head` di DB lokal sebelum commit.
4. **Jangan edit migrasi yang sudah di-commit/dibagikan.** Buat migrasi baru untuk koreksi.
5. Jangan menaruh logika aplikasi atau impor `services` di dalam migrasi.
6. Perubahan data (data migration) dipisah dari perubahan skema.
7. `backend/alembic/env.py` membaca URL dari `settings`, bukan dari `alembic.ini`.
8. Semua model harus diimpor di `backend/app/db/base.py` agar terdeteksi autogenerate.
9. Jangan menjalankan migrasi ke database selain lokal/dev tanpa persetujuan pengguna.

## 6. Aturan Query

- Selalu gunakan parameter bind SQLAlchemy; dilarang menyusun SQL dengan f-string.
- Query feed dan daftar wajib memakai pagination dan memuat relasi secara eksplisit.
- Post `deleted_at IS NOT NULL` tidak boleh muncul di endpoint publik.
- Akun `suspended` tidak muncul di pencarian dan tidak bisa login.
- Operasi multi-langkah (mis. buat post + hashtag + notifikasi) berada dalam satu transaksi.

## 7. Seed dan Data Uji

- `backend/scripts/seed_data.py` membuat data contoh untuk pengembangan frontend; hanya jalan bila
  `APP_ENV=development`.
- Data uji tidak boleh berisi email atau identitas orang sungguhan.
