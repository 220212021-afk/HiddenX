# SECURITY

Hidden X menjanjikan privasi identitas. Pelanggaran aturan di dokumen ini adalah bug kritis.

## 1. Model Identitas (Pseudonimitas Terkelola)

- Publik hanya melihat `anon_id`. Identitas asli tersimpan terenkripsi untuk kebutuhan moderasi
  dan hukum (NFR-01, NFR-08).
- Penelusuran identitas asli **hanya** lewat jalur terpisah khusus Admin, dicatat di audit log,
  dan tidak tersedia di endpoint publik maupun endpoint Moderator.

## 2. Data Sensitif

| Data | Perlakuan |
| --- | --- |
| Email, username asli | Enkripsi Fernet di kolom `*_enc`; lookup lewat `email_hash` (HMAC) |
| Kata sandi | Hash argon2; tidak pernah disimpan atau di-log dalam bentuk asli |
| Access/refresh token | Tidak di-log; refresh token disimpan sebagai hash |
| `SECRET_KEY`, `ENCRYPTION_KEY`, `HMAC_KEY` | Hanya dari environment; rotasi didokumentasikan |

Normalisasi email (lowercase, trim) dilakukan **sebelum** hash dan enkripsi.

## 3. Autentikasi JWT (NFR-02)

- Access token: HS256, masa berlaku dari `ACCESS_TOKEN_EXPIRE_MINUTES` (rentang SRS 15–60 menit).
- Payload minimal: `sub` (ID internal sebagai string), `anon_id`, `role`, `iat`, `exp`, `type=access`.
  **Jangan** memasukkan email atau identitas asli ke payload (payload JWT hanya di-encode,
  tidak terenkripsi).
- Refresh token: nilai acak panjang, disimpan hash-nya di `refresh_tokens`, dirotasi setiap
  dipakai (token lama dicabut). Logout mencabut refresh token.
- Verifikasi wajib mengecek: tanda tangan, `exp`, `type`, dan bahwa user masih `active`.
- Peran dicek di server lewat `require_role(...)`; jangan percaya klaim `role` dari klien
  tanpa memeriksa ulang status akun bila operasinya sensitif.

## 4. Otorisasi

| Operasi | Syarat |
| --- | --- |
| Hapus post | Pemilik post, atau Moderator/Admin lewat jalur moderasi |
| Lihat/ubah laporan | Moderator atau Admin |
| Suspend akun, kelola pengguna | Admin (Moderator hanya bila SRS menetapkan) |
| Like, reply, repost, follow, report | User aktif |

Selalu cek kepemilikan resource di service, bukan hanya di UI.

## 5. Validasi dan Serangan Umum

- Validasi semua input di skema Pydantic; tolak field tak dikenal pada skema input sensitif
  (`extra="forbid"`).
- Cegah SQL injection: hanya query terparameter/ORM.
- Sanitasi konten post terhadap XSS di sisi tampilan (frontend) dan jangan menganggap konten
  aman; backend menyimpan teks apa adanya dan tidak mengeksekusinya.
- `image_url`: validasi skema (hanya https) dan domain yang diizinkan; jangan fetch URL
  tersebut dari server (cegah SSRF).
- CORS: hanya origin di `CORS_ORIGINS`, bukan `*`, terutama bila memakai kredensial.
- Aktifkan header keamanan dasar dan nonaktifkan dokumentasi interaktif (`/docs`) di produksi
  bila tidak diperlukan.

## 6. Rate Limiting

| Endpoint | Saran awal |
| --- | --- |
| `/auth/login` | 5/menit per IP dan per akun |
| `/auth/register` | 3/jam per IP |
| `POST /posts`, reply, repost | 30/menit per user |
| `POST /reports` | 10/jam per user |

Nilai bersifat usulan; sesuaikan setelah uji.

## 7. Logging

- Boleh: ID internal, `anon_id`, method, path, status, durasi, request ID.
- **Dilarang:** email, username asli, kata sandi, token, isi header `Authorization`,
  body request auth.
- Error yang dikirim ke klien bersifat generik; detail teknis hanya di log server.
- Tindakan moderasi (suspend, hapus post, penelusuran identitas) dicatat dengan siapa, kapan,
  dan alasannya.

## 8. Checklist Review Keamanan (untuk setiap PR)

- [ ] Tidak ada field identitas asli di skema output atau log
- [ ] Endpoint baru punya dependensi auth yang benar dan cek peran/kepemilikan
- [ ] Input divalidasi; tidak ada SQL mentah
- [ ] Ada test negatif (tanpa token, peran salah, bukan pemilik)
- [ ] Tidak ada rahasia di kode atau `.env.example`
