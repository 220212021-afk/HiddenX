# CONVENTIONS

## 1. Gaya Kode Python

- Type hints wajib pada semua fungsi publik. `mypy` harus lolos.
- Formatter dan linter: `ruff` (panjang baris 100). Jangan menambah aturan ignore tanpa alasan.
- Impor absolut dari `app.`, urutan dirapikan ruff.
- Fungsi pendek dan satu tanggung jawab. Service dipecah bila melebihi sekitar 150 baris.
- Komentar menjelaskan **mengapa**, bukan **apa**. Docstring service mencantumkan kode SRS.
- Tidak ada `print()`; gunakan `logging` (lihat `SECURITY.md` bagian log).
- Tidak ada `except:` kosong atau menelan exception diam-diam.

## 2. Penamaan

| Hal | Aturan | Contoh |
| --- | --- | --- |
| File/modul | `snake_case` | `post_service.py` |
| Kelas | `PascalCase` | `PostCreate`, `User` |
| Fungsi/variabel | `snake_case` | `create_post` |
| Konstanta | `UPPER_SNAKE` | `MAX_POST_LENGTH = 280` |
| Tabel DB | jamak, `snake_case` | `posts`, `follows` |
| Kolom FK | `<entitas>_id` | `user_id`, `post_id` |
| Skema Pydantic | `<Entitas><Tujuan>` | `PostCreate`, `PostOut`, `LoginIn`, `TokenOut` |
| Endpoint URL | kebab/jamak, huruf kecil | `/posts/{post_id}/like` |
| Branch | `<tipe>/<singkat>` | `feat/post-create` |

Konstanta yang dipakai lintas modul (mis. 280) didefinisikan sekali di `app/core/constants.py`.

## 3. Pola Endpoint

```python
@router.post("", response_model=PostOut, status_code=status.HTTP_201_CREATED)
async def create_post(
    data: PostCreate,
    db: AsyncSession = Depends(get_db),
    user: User = Depends(get_current_user),
) -> PostOut:
    """FR-05: membuat post baru."""
    post = await post_service.create_post(db, user, data)
    return PostOut.model_validate(post)
```

Aturan: selalu set `response_model` dan `status_code`, tidak ada logika bisnis di badan fungsi.

## 4. Pola Skema Pydantic

- Skema input dan output dipisah. Jangan memakai satu skema untuk keduanya.
- Skema output publik hanya memuat field yang secara sengaja dibuka (`anon_id`, `content`, ...).
- Gunakan `model_config = ConfigDict(from_attributes=True)` untuk skema output.
- Validasi di skema: `Field(min_length=..., max_length=...)`, `EmailStr`, enum untuk nilai terbatas.

## 5. Format Error Seragam

Semua error dikembalikan dengan bentuk:

```json
{
  "error": {
    "code": "POST_TOO_LONG",
    "message": "Post melebihi 280 karakter.",
    "details": null
  }
}
```

- `code`: `UPPER_SNAKE`, stabil, dipakai frontend. `message`: bahasa Indonesia, aman ditampilkan.
- Service melempar exception domain (`NotFoundError`, `ForbiddenError`, `ConflictError`,
  `ValidationDomainError`) dari `core/exceptions.py`; handler di `main.py` memetakannya.
- Jangan bocorkan detail internal (stack trace, query SQL, nama kolom identitas).
- Pesan login gagal selalu generik ("Email atau kata sandi salah") agar tidak membuka
  keberadaan akun.

## 6. Kode Status HTTP

| Situasi | Status |
| --- | --- |
| Berhasil membaca/mengubah | 200 |
| Berhasil membuat resource | 201 |
| Berhasil tanpa isi (mis. hapus) | 204 |
| Validasi gagal (Pydantic) | 422 |
| Token hilang/tidak valid/kedaluwarsa | 401 |
| Login valid tapi tidak berhak / akun suspend | 403 |
| Resource tidak ada | 404 |
| Konflik (email atau Anon-ID sudah dipakai, sudah follow) | 409 |
| Terkena rate limit | 429 |

## 7. Pagination

- Endpoint daftar (feed, profil, notifikasi, laporan) memakai **cursor-based pagination**
  berdasarkan `(created_at, id)` agar stabil saat data baru masuk.
- Parameter: `limit` (default 20, maks. 50) dan `cursor` (opsional).
- Response: `{ "items": [...], "next_cursor": "..." | null }`.

## 8. Waktu dan ID

- Simpan waktu dalam UTC (`TIMESTAMPTZ`/`DateTime(timezone=True)`); format ISO 8601 di API.
- ID internal integer auto-increment. Jangan membuka `users.id` ke publik; identifikasi
  pengguna di API selalu lewat `anon_id`.

## 9. Penulisan Test

- Nama: `test_<kode_srs>_<perilaku>`, mis. `test_fr05_post_over_280_chars_rejected`.
- Pola Arrange-Act-Assert. Satu perilaku per test.
- Unit test untuk service dan utilitas; integration test untuk endpoint dengan DB uji.
- Test tidak boleh bergantung pada urutan eksekusi atau data dari test lain.
- Wajib ada test negatif: tanpa token, token kedaluwarsa, peran salah, input tidak valid.
