# API

Base URL: `https://api.hiddenx.app/api/v1` (lokal: `http://localhost:8000/api/v1`).
Format: JSON. Endpoint bertanda 🔒 memerlukan header `Authorization: Bearer <access_token>`.
Format error dan kode status: lihat `CONVENTIONS.md`.

Kolom **Sumber**: *SRS* = tersurat di SRS, *Usulan* = usulan yang perlu dikonfirmasi tim.

## 1. Daftar Endpoint

### Autentikasi (FR-01 s.d. FR-04)
| Metode | Path | Fungsi | Sukses | Sumber |
| --- | --- | --- | --- | --- |
| POST | `/auth/register` | Registrasi, menerbitkan Anon-ID | 201 | Usulan |
| POST | `/auth/login` | Login, menerbitkan access + refresh token | 200 | SRS |
| POST | `/auth/refresh` | Tukar refresh token dengan access token baru | 200 | SRS |
| POST | `/auth/logout` 🔒 | Cabut refresh token | 204 | Usulan |

### Konten (FR-05 s.d. FR-09)
| Metode | Path | Fungsi | Sukses | Sumber |
| --- | --- | --- | --- | --- |
| POST | `/posts` 🔒 | Buat post (maks. 280 karakter) | 201 | SRS |
| DELETE | `/posts/{post_id}` 🔒 | Hapus post sendiri | 204 | Usulan |
| GET | `/posts/{post_id}` | Detail post dan thread reply | 200 | Usulan |
| POST | `/posts/{post_id}/like` 🔒 | Like | 200 | SRS |
| DELETE | `/posts/{post_id}/like` 🔒 | Unlike | 204 | Usulan |
| POST | `/posts/{post_id}/reply` 🔒 | Balas post | 201 | Usulan |
| POST | `/posts/{post_id}/repost` 🔒 | Repost / quote (komentar opsional) | 201 | Usulan |

### Sosial (FR-10 s.d. FR-14)
| Metode | Path | Fungsi | Sukses | Sumber |
| --- | --- | --- | --- | --- |
| GET | `/posts/feed` 🔒 | Feed dari akun yang di-follow | 200 | SRS |
| GET | `/users/{anon_id}` | Profil publik + post (bisa diakses Guest) | 200 | Usulan |
| POST | `/users/{anon_id}/follow` 🔒 | Follow | 204 | Usulan |
| DELETE | `/users/{anon_id}/follow` 🔒 | Unfollow | 204 | Usulan |
| GET | `/trending` | Hashtag trending 24 jam terakhir | 200 | Usulan |
| GET | `/search?q=` | Cari post/Anon-ID/hashtag | 200 | Usulan |

### Moderasi dan Notifikasi (FR-15 s.d. FR-17)
| Metode | Path | Fungsi | Sukses | Sumber |
| --- | --- | --- | --- | --- |
| POST | `/reports` 🔒 | Laporkan post/akun dengan kategori | 201 | Usulan |
| GET | `/admin/reports` 🔒 | Antrean laporan (Moderator/Admin) | 200 | SRS |
| PATCH | `/admin/reports/{report_id}` 🔒 | Ubah status / tindak lanjut | 200 | Usulan |
| POST | `/admin/users/{anon_id}/suspend` 🔒 | Suspend akun (Admin) | 204 | Usulan |
| GET | `/notifications` 🔒 | Daftar notifikasi | 200 | Usulan |
| POST | `/notifications/read` 🔒 | Tandai sudah dibaca | 204 | Usulan |

## 2. Contoh Kontrak

### POST `/auth/login`
Request:
```json
{ "email": "user@example.com", "password": "********" }
```
Response 200:
```json
{
  "access_token": "<jwt>",
  "refresh_token": "<opaque>",
  "token_type": "bearer",
  "expires_in": 1800
}
```
Gagal: 401 dengan pesan generik. Akun suspend: 403 `ACCOUNT_SUSPENDED`.

### POST `/posts` 🔒
Request:
```json
{ "content": "Hari ini aku akhirnya berani bilang jujur. #HiddenX", "image_url": null }
```
Response 201:
```json
{
  "id": 101,
  "anon_id": "kabut_senja92",
  "content": "Hari ini aku akhirnya berani bilang jujur. #HiddenX",
  "image_url": null,
  "like_count": 0,
  "reply_count": 0,
  "repost_count": 0,
  "created_at": "2026-10-20T09:15:00Z"
}
```
`content` > 280 karakter → 422. Response tidak pernah memuat `user_id` internal atau identitas asli.

### GET `/posts/feed` 🔒
Query: `limit` (default 20, maks. 50), `cursor`.
```json
{ "items": [ { "...": "PostOut" } ], "next_cursor": "eyJ0IjoiLi4uIn0" }
```

### POST `/reports` 🔒
```json
{ "target_post_id": 101, "category": "hate_speech", "note": "opsional" }
```
Status awal laporan: `pending` (menunggu tinjauan). Satu user tidak boleh melaporkan target
yang sama dua kali (409).

## 3. Aturan Perubahan Kontrak

- Menambah field opsional di response: boleh di `v1`.
- Menghapus/mengganti nama field, atau mengubah arti: wajib versi baru.
- Setiap endpoint baru atau perubahan kontrak harus memperbarui dokumen ini dan test integrasi.
- OpenAPI otomatis FastAPI adalah cerminan; dokumen ini adalah sumber kesepakatan dengan
  tim frontend.
