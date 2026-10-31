# Panduan Frontend Hidden X untuk Pemula

**Target:** menyelesaikan halaman **Register** dan **Login** pada proyek `hiddenx/frontend`
**Teknologi:** Next.js 16 · App Router · TypeScript · Tailwind CSS
**Backend:** FastAPI (masih dikembangkan), jadi kita pakai **data tiruan (mock)** dulu

---

## Baca ini dulu

### Cara memakai panduan ini

- Kerjakan **berurutan**, satu tahap sampai selesai. Jangan loncat.
- Setiap tahap diakhiri blok **⏸️ Jeda**. Pastikan semua centang terpenuhi sebelum lanjut.
- Kalau ada error, **jangan panik**. Salin pesan error-nya (teks merahnya) dan tanyakan ke saya. Itu hal normal dalam belajar ngoding.
- Library hanya dipasang **satu per satu**, tepat saat dibutuhkan.

### Kabar baik: kamu tidak perlu Python

SRS menyebut backend memakai **FastAPI (Python)**, tapi itu pekerjaan tim backend. Sebagai **developer frontend** kamu memakai **JavaScript/TypeScript** lewat Next.js. Python tidak perlu dipasang.

### Catatan versi

Panduan ini saya cocokkan dengan dokumentasi resmi Next.js 16.x (halaman yang saya baca menampilkan versi 16.2.x). Konsep di sini (App Router, `proxy.ts`, `await cookies()`, Server Actions) sama untuk 16.4.3. Kalau ada perbedaan kecil, dokumentasi resmi di <https://nextjs.org/docs> yang menang.

### Peta perjalanan

| Tahap | Yang dikerjakan | Yang dipasang |
| --- | --- | --- |
| 1 | Kenalan dengan terminal, pasang Node.js | Node.js |
| 2 | Pasang editor kode | VS Code |
| 3 | Buat proyek `hiddenx/frontend` | Paket starter Next.js |
| 4 | Jalankan proyek, kenali isinya | tidak ada |
| 5 | Layout dasar | tidak ada |
| 6 | Halaman Login (tampilan saja) | tidak ada |
| 7 | Halaman Register (tampilan saja) | tidak ada |
| 8 | Pengaturan `.env` dan "jembatan" ke API | tidak ada |
| 9 | Validasi isian form | `zod` |
| 10 | Menyimpan token login di cookie | tidak ada |
| 11 | Login benar-benar berfungsi | tidak ada |
| 12 | Register benar-benar berfungsi | tidak ada |
| 13 | Beranda sementara, logout, penjaga halaman | tidak ada |
| 14 | Uji coba manual | tidak ada |
| 15 | Sambung ke backend asli | tidak ada |

### Kontrak API yang kita pakai

Sesuai arahanmu, semua endpoint berada di bawah prefix `/api/v1`:

| Fungsi | Metode | Endpoint |
| --- | --- | --- |
| Registrasi (FR-01) | POST | `/api/v1/auth/register` |
| Login (FR-02) | POST | `/api/v1/auth/login` |

> ⚠️ **Perbedaan di dokumen:** SRS Bab 10 menulis endpoint tanpa prefix (`/auth/login`), sedangkan rancangan struktur backend memakai prefix `/api/v1` pada `router.py`. Kita ikut `/api/v1`. Konfirmasikan ke tim backend.

Isi permintaan (*request*) dan balasan (*response*) **belum tertulis di SRS**, jadi saya buat asumsi yang wajar. Asumsi ini dikumpulkan di [Lampiran A](#lampiran-a--asumsi-kontrak-api-wajib-dicocokkan-dengan-tim-backend).

---

## Tahap 1: Kenalan dengan Terminal dan Pasang Node.js

### 1.1 Apa itu terminal?

Terminal adalah jendela tempat kamu **mengetik perintah teks** ke komputer, sebagai pengganti klik-klik. Dunia pemrograman memakainya terus. Kamu akan sering membukanya.

- **Windows:** cari "PowerShell" atau "Terminal" di menu Start.
- **macOS:** cari "Terminal" di Spotlight (`⌘ + Space`).
- **Linux:** biasanya `Ctrl + Alt + T`.

Tiga perintah dasar yang akan sering kamu pakai:

| Perintah | Artinya | Contoh |
| --- | --- | --- |
| `cd nama-folder` | **c**hange **d**irectory: masuk ke folder | `cd Documents` |
| `cd ..` | naik satu folder ke atas | |
| `mkdir nama` | **m**a**k**e **dir**ectory: membuat folder baru | `mkdir hiddenx` |

Cara melihat "sekarang saya ada di folder mana?": ketik `pwd` (macOS/Linux) atau `cd` saja tanpa nama (Windows CMD). Di PowerShell, `pwd` juga bisa.

### 1.2 Apa itu Node.js dan npm?

- **Node.js** adalah mesin yang menjalankan JavaScript **di luar browser**. Next.js membutuhkannya untuk berjalan di komputermu.
- **npm** (*Node Package Manager*) ikut terpasang bersama Node.js. Fungsinya seperti "toko aplikasi" untuk library kode. Perintah `npm install nama-library` berarti "unduh library itu ke proyekku".

### 1.3 Pasang Node.js

1. Buka <https://nodejs.org>.
2. Unduh versi **LTS** (*Long Term Support*, versi yang stabil).
3. Jalankan installer, klik *Next* sampai selesai (biarkan pengaturan bawaan).
4. **Tutup terminal lalu buka lagi.** Ini penting agar komputer mengenali Node.js yang baru dipasang.

### 1.4 Cek hasil pemasangan

Ketik di terminal:

```bash
node -v
```

```bash
npm -v
```

**Makna perintah:** `-v` adalah singkatan dari *version*. Kamu meminta komputer menyebutkan nomor versi program tersebut.

**Hasil yang diharapkan:** angka seperti `v22.11.0` dan `10.9.0`. Yang penting, Node.js **minimal versi 20.9** (syarat Next.js 16).

> ⏸️ **Jeda 1**
> - [ ] `node -v` menampilkan versi **20.9 atau lebih tinggi**
> - [ ] `npm -v` menampilkan angka versi
>
> Kalau muncul "command not found" atau "tidak dikenali", tutup semua terminal, buka lagi, coba ulang. Kalau masih gagal, kabari saya.

---

## Tahap 2: Pasang VS Code

**Visual Studio Code (VS Code)** adalah editor tempat kamu menulis kode. Ia gratis dan paling populer.

1. Unduh dari <https://code.visualstudio.com> lalu pasang.
2. Buka VS Code.

Dua fitur yang akan kamu pakai terus:

- **Terminal bawaan:** tekan `` Ctrl + ` `` (tombol di atas Tab). Terminal terbuka di bagian bawah, dan otomatis berada di folder proyekmu.
- **Membuat file bersarang:** klik kanan di panel kiri → *New File*, lalu ketik path lengkap seperti `app/(auth)/login/page.tsx`. VS Code **otomatis membuat folder-foldernya**.

> ⏸️ **Jeda 2**
> - [ ] VS Code terbuka dan terminal bawaan (`` Ctrl + ` ``) bisa dibuka

---

## Tahap 3: Membuat Proyek `hiddenx/frontend`

### 3.1 Buat folder induk

Pilih tempat menyimpan proyek, misalnya folder Documents. Di terminal:

```bash
cd Documents
mkdir hiddenx
cd hiddenx
```

**Makna:**
- `cd Documents`: masuk ke folder Documents.
- `mkdir hiddenx`: buat folder bernama `hiddenx`.
- `cd hiddenx`: masuk ke dalamnya.

Folder `hiddenx` ini nanti bisa berisi `frontend` (punyamu) dan `backend` (punya tim backend).

### 3.2 Buat proyek Next.js

```bash
npx create-next-app@latest frontend
```

**Makna perintah ini, per kata:**

| Bagian | Artinya |
| --- | --- |
| `npx` | menjalankan sebuah program dari npm **tanpa memasangnya permanen** |
| `create-next-app` | program resmi yang membuatkan kerangka proyek Next.js |
| `@latest` | pakai versi terbaru |
| `frontend` | nama folder proyek yang akan dibuat, sehingga hasilnya `hiddenx/frontend` |

Kalau muncul pertanyaan *"Ok to proceed? (y)"*, ketik `y` lalu Enter.

### 3.3 Jawab pertanyaan instalasi

Pertanyaan pertama biasanya berbunyi:

```
Would you like to use the recommended Next.js defaults?
```

Pilih opsi pertama, **"Yes, use recommended defaults"**, dengan menekan **Enter**. Itu sudah berisi pilihan yang kita butuhkan:

| Pilihan | Nilai | Artinya |
| --- | --- | --- |
| TypeScript | Ya | JavaScript dengan "pengecek kesalahan" bawaan |
| ESLint | Ya | alat yang menegur gaya/penulisan kode yang janggal |
| Tailwind CSS | Ya | cara menata tampilan dengan class pendek |
| App Router | Ya | sistem routing modern Next.js (**wajib** sesuai tugasmu) |
| Folder `src/` | Tidak | file `app/` langsung di akar proyek, jalur lebih pendek |
| Import alias | `@/*` | `@/` berarti "mulai dari akar proyek" |

Kalau yang muncul justru pertanyaan satu per satu, jawab seperti tabel di atas. Untuk **React Compiler**, jawab **No**, karena belum kita butuhkan.

Tunggu sampai selesai. Prosesnya mengunduh banyak file (bisa beberapa menit tergantung internet).

### 3.4 Apa saja yang baru saja terpasang?

`create-next-app` memasang satu paket starter. Jangan dihafal, cukup kenali namanya dulu. Kita bahas tiap bagian **saat dipakai**.

| Library | Fungsi singkat | Kita bahas di |
| --- | --- | --- |
| `next` | kerangka utama (routing, server, dll.) | Tahap 4-5 |
| `react`, `react-dom` | pustaka untuk membangun tampilan dari "komponen" | Tahap 5-6 |
| `typescript` | pemeriksa tipe data | Tahap 6 |
| `tailwindcss` | penata tampilan lewat class | Tahap 5 |
| `eslint` | penegur penulisan kode | Tahap 14 |

> ⏸️ **Jeda 3**
> - [ ] Folder `hiddenx/frontend` sudah ada
> - [ ] Terminal kembali menampilkan prompt tanpa error merah

---

## Tahap 4: Jalankan dan Kenali Proyekmu

### 4.1 Buka di VS Code

```bash
cd frontend
code .
```

**Makna:** masuk ke folder `frontend`, lalu `code .` berarti "buka folder ini (`.` = folder saat ini) di VS Code". Kalau perintah `code` tidak dikenali, buka VS Code manual: *File → Open Folder* → pilih `hiddenx/frontend`.

Mulai sekarang, **gunakan terminal bawaan VS Code** (`` Ctrl + ` ``). Pastikan path-nya berakhir di `frontend`.

### 4.2 Jalankan server pengembangan

```bash
npm run dev
```

**Makna:** `npm run dev` menjalankan skrip bernama `dev` yang tertulis di `package.json`. Skrip itu mengeksekusi `next dev`, yaitu **server lokal untuk pengembangan**. Setiap kali kamu menyimpan file, halaman di browser **otomatis ter-update**.

Buka browser ke <http://localhost:3000>. Kamu akan melihat halaman bawaan Next.js.

- `localhost` = "komputer saya sendiri"
- `3000` = nomor "pintu" tempat server mendengarkan

Untuk **menghentikan** server: tekan `Ctrl + C` di terminal. Untuk menjalankan lagi, ketik `npm run dev`.

> 💡 Biarkan `npm run dev` menyala sepanjang kamu mengerjakan. Buka **terminal kedua** (ikon `+` di panel terminal) kalau perlu mengetik perintah lain.

### 4.3 Kenali isi folder

```
frontend/
├── app/                  ← JANTUNG proyek: halaman-halamanmu ada di sini
│   ├── layout.tsx        ← "bingkai" yang membungkus semua halaman
│   ├── page.tsx          ← halaman untuk alamat "/"
│   └── globals.css       ← gaya global (Tailwind masuk dari sini)
├── public/               ← gambar/ikon statis
├── node_modules/         ← tempat semua library terunduh (JANGAN diedit, JANGAN di-commit)
├── package.json          ← daftar library + skrip perintah proyek
├── next.config.ts        ← pengaturan Next.js
└── tsconfig.json         ← pengaturan TypeScript
```

**Konsep terpenting: routing berbasis folder.** Di App Router, **folder = alamat URL**, dan file bernama `page.tsx` di dalamnya = halaman.

| File | Alamat di browser |
| --- | --- |
| `app/page.tsx` | `/` |
| `app/login/page.tsx` | `/login` |
| `app/register/page.tsx` | `/register` |

### 4.4 Cek versi Next.js

Di terminal kedua:

```bash
npm ls next
```

**Makna:** `ls` = *list*. Perintah ini menampilkan versi `next` yang terpasang di proyekmu. Harusnya tertulis `next@16.x.x`.

Kalau tugas mewajibkan tepat 16.4.3 dan versi yang tampil berbeda, kunci dengan:

```bash
npm install next@16.4.3
```

(Kalau muncul error "No matching version found", artinya versi itu belum tersedia di npm. Pakai versi yang sudah terpasang.)

### 4.5 Bersihkan halaman bawaan

Ganti seluruh isi `app/page.tsx` dengan:

```tsx
export default function HomePage() {
  return (
    <main className="p-8">
      <h1 className="text-2xl font-bold">Beranda Hidden X</h1>
    </main>
  );
}
```

**Cara kerja kode ini:**
- `export default function HomePage()` membuat sebuah **komponen**, yaitu potongan tampilan yang bisa dipakai ulang. `export default` artinya "inilah isi utama file ini". Next.js mencarinya untuk dijadikan halaman.
- Kode yang mirip HTML di dalam `return (...)` disebut **JSX**.
- `className="..."` adalah cara menulis `class` HTML di React. Isinya class Tailwind (dijelaskan di Tahap 5).

Simpan (`Ctrl + S`). Browser langsung berubah.

> ⏸️ **Jeda 4**
> - [ ] <http://localhost:3000> menampilkan tulisan "Beranda Hidden X"
> - [ ] `npm ls next` menampilkan versi 16.x
> - [ ] Kamu paham: **folder = URL**, `page.tsx` = isi halaman

---

## Tahap 5: Layout Dasar

### 5.1 Ganti `app/layout.tsx`

`layout.tsx` yang di akar `app/` adalah **Root Layout**: bingkai yang membungkus **setiap halaman**. Ganti seluruh isinya:

```tsx
import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Hidden X",
  description: "Platform microblogging anonim",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="id">
      <body className="min-h-screen bg-gray-50 text-gray-900 antialiased">
        {children}
      </body>
    </html>
  );
}
```

**Cara kerja:**
- `import "./globals.css"` memuat gaya global agar Tailwind aktif.
- `metadata` menentukan judul tab browser.
- `children` adalah **isi halaman yang sedang dibuka**. Next.js menyisipkannya di sini. Jadi `<html>` dan `<body>` cukup ditulis sekali.
- `{ children }: { children: React.ReactNode }` adalah penulisan TypeScript: bagian kiri mengambil `children`, bagian kanan menjelaskan **tipenya** ("apa pun yang boleh dirender React").

### 5.2 Ganti `app/globals.css`

Ganti seluruh isinya dengan satu baris:

```css
@import "tailwindcss";
```

**Makna:** baris ini mengaktifkan Tailwind CSS. Tailwind menyediakan ratusan class siap pakai.

### 5.3 Kamus Tailwind mini

| Class | Efek |
| --- | --- |
| `p-8` | padding (jarak dalam) 2rem |
| `mt-1` | margin atas (jarak luar) kecil |
| `text-2xl` | ukuran huruf besar |
| `font-bold` | huruf tebal |
| `bg-indigo-600` | warna latar indigo |
| `text-white` | warna huruf putih |
| `rounded-lg` | sudut membulat |
| `w-full` | lebar 100% |
| `flex items-center justify-center` | susun isi dan taruh di tengah |
| `hover:bg-indigo-700` | berubah warna saat kursor di atasnya |

Kamu tidak perlu menghafal. Cukup baca dan tebak, lama-lama terbiasa.

> ⏸️ **Jeda 5**
> - [ ] Halaman `/` masih tampil (sekarang latar abu-abu muda)
> - [ ] Tidak ada tulisan error merah di terminal

---

## Tahap 6: Halaman Login (Tampilan Dulu)

Kita buat **tampilannya dulu**, belum berfungsi. Satu hal dalam satu waktu.

### 6.1 Route group `(auth)`

Buat folder **dengan tanda kurung**: `app/(auth)/`. Folder berkurung disebut **route group**. Ia hanya untuk **mengelompokkan** file, dan namanya **tidak muncul di URL**. Jadi `app/(auth)/login/page.tsx` tetap beralamat `/login`.

Gunanya: halaman login dan register berbagi layout yang sama (kartu di tengah layar).

### 6.2 Layout khusus auth

Buat file `app/(auth)/layout.tsx`:

```tsx
export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <main className="flex min-h-screen items-center justify-center px-4 py-10">
      <div className="w-full max-w-md rounded-2xl bg-white p-8 shadow-lg">
        <div className="mb-6 text-center">
          <h1 className="text-3xl font-bold text-indigo-600">Hidden X</h1>
          <p className="mt-1 text-sm text-gray-500">
            Bersuara tanpa membuka identitasmu
          </p>
        </div>
        {children}
      </div>
    </main>
  );
}
```

**Cara kerja:** layout ini dibungkus **di dalam** Root Layout, lalu membungkus halaman login/register dengan kartu putih berukuran maksimal `max-w-md`.

### 6.3 Komponen input yang bisa dipakai ulang

Login dan Register sama-sama punya banyak kolom isian. Daripada menulis ulang, kita buat **satu komponen**. Buat file `components/auth/TextField.tsx` (folder `components` di akar proyek, sejajar dengan `app`):

```tsx
type TextFieldProps = {
  label: string;
  name: string;
  type?: string;
  placeholder?: string;
  autoComplete?: string;
  defaultValue?: string;
  hint?: string;
  error?: string[];
};

export default function TextField({
  label,
  name,
  type = "text",
  placeholder,
  autoComplete,
  defaultValue,
  hint,
  error,
}: TextFieldProps) {
  const hasError = error !== undefined && error.length > 0;

  return (
    <div>
      <label
        htmlFor={name}
        className="mb-1 block text-sm font-medium text-gray-700"
      >
        {label}
      </label>
      <input
        id={name}
        name={name}
        type={type}
        placeholder={placeholder}
        autoComplete={autoComplete}
        defaultValue={defaultValue}
        aria-invalid={hasError}
        className={`w-full rounded-lg border px-3 py-2 text-sm outline-none focus:ring-2 focus:ring-indigo-500 ${
          hasError ? "border-red-500" : "border-gray-300"
        }`}
      />
      {hint && !hasError && (
        <p className="mt-1 text-xs text-gray-500">{hint}</p>
      )}
      {hasError && <p className="mt-1 text-sm text-red-600">{error[0]}</p>}
    </div>
  );
}
```

**Cara kerja, pelan-pelan:**
- `type TextFieldProps = {...}` mendefinisikan **props** (parameter komponen). Tanda `?` berarti **opsional**.
- `label` dan `name` wajib. Sisanya boleh kosong.
- `type = "text"` memberi **nilai bawaan** kalau tidak diisi.
- `name` penting: nama inilah yang nanti dibaca saat form dikirim (`formData.get("email")`).
- `{hasError && <p>...</p>}` artinya "tampilkan paragraf ini **hanya kalau** ada error".
- `error` bertipe daftar teks (`string[]`) karena library validasi nanti mengembalikan daftar pesan.

### 6.4 Form login (versi statis)

Buat `components/auth/LoginForm.tsx`:

```tsx
import Link from "next/link";
import TextField from "./TextField";

export default function LoginForm() {
  return (
    <form className="space-y-4">
      <TextField
        label="Email"
        name="email"
        type="email"
        autoComplete="email"
        placeholder="kamu@contoh.com"
      />
      <TextField
        label="Kata sandi"
        name="password"
        type="password"
        autoComplete="current-password"
      />
      <button
        type="submit"
        className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
      >
        Masuk
      </button>
      <p className="text-center text-sm text-gray-600">
        Belum punya akun?{" "}
        <Link href="/register" className="font-medium text-indigo-600 hover:underline">
          Daftar
        </Link>
      </p>
    </form>
  );
}
```

**Cara kerja:**
- `Link` dari `next/link` adalah pengganti `<a>`. Pindah halaman terasa instan karena tidak memuat ulang seluruh halaman.
- `import TextField from "./TextField"` berarti "ambil komponen dari file tetangga". `./` artinya folder yang sama.
- `space-y-4` memberi jarak vertikal antar anak form.

### 6.5 Halaman `/login`

Buat `app/(auth)/login/page.tsx`:

```tsx
import LoginForm from "@/components/auth/LoginForm";

export const metadata = { title: "Masuk | Hidden X" };

export default function LoginPage() {
  return (
    <>
      <h2 className="mb-4 text-xl font-semibold">Masuk ke akunmu</h2>
      <LoginForm />
    </>
  );
}
```

**Cara kerja:** `@/components/auth/LoginForm` memakai alias `@/` (akar proyek). `<>...</>` disebut **Fragment**, pembungkus tak terlihat karena React mewajibkan satu pembungkus.

Buka <http://localhost:3000/login>.

> 🚫 **Jangan klik tombol "Masuk" dulu.** Form belum punya aksi, jadi klik hanya memuat ulang halaman.

> ⏸️ **Jeda 6**
> - [ ] `/login` menampilkan kartu putih berisi Email, Kata sandi, tombol Masuk
> - [ ] Link "Daftar" mengarah ke `/register` (halamannya belum ada, itu wajar: 404)
> - [ ] Kamu paham fungsi **komponen** dan **props** (`label`, `name`, ...)

---

## Tahap 7: Halaman Register (Tampilan Dulu)

### 7.1 Form register (statis)

Buat `components/auth/RegisterForm.tsx`:

```tsx
import Link from "next/link";
import TextField from "./TextField";

export default function RegisterForm() {
  return (
    <form className="space-y-4">
      <TextField
        label="Email"
        name="email"
        type="email"
        autoComplete="email"
        placeholder="kamu@contoh.com"
      />
      <TextField
        label="Username"
        name="username"
        autoComplete="username"
        placeholder="nama_aslimu"
        hint="Disimpan terenkripsi dan tidak pernah tampil ke publik. Nama tampilanmu (Anon-ID) dibuat otomatis oleh sistem."
      />
      <TextField
        label="Kata sandi"
        name="password"
        type="password"
        autoComplete="new-password"
        hint="Minimal 8 karakter, mengandung huruf dan angka."
      />
      <TextField
        label="Ulangi kata sandi"
        name="confirmPassword"
        type="password"
        autoComplete="new-password"
      />
      <button
        type="submit"
        className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700"
      >
        Daftar
      </button>
      <p className="text-center text-sm text-gray-600">
        Sudah punya akun?{" "}
        <Link href="/login" className="font-medium text-indigo-600 hover:underline">
          Masuk
        </Link>
      </p>
    </form>
  );
}
```

**Kenapa ada hint tentang Anon-ID?** SRS (NFR-01, NFR-08) menegaskan identitas asli tidak boleh tampil ke pengguna lain, dan Anon-ID diterbitkan sistem (FR-01). Pesan ini menenangkan pengguna dan sesuai konsep produk.

### 7.2 Halaman `/register`

Buat `app/(auth)/register/page.tsx`:

```tsx
import RegisterForm from "@/components/auth/RegisterForm";

export const metadata = { title: "Daftar | Hidden X" };

export default function RegisterPage() {
  return (
    <>
      <h2 className="mb-4 text-xl font-semibold">Buat akun baru</h2>
      <RegisterForm />
    </>
  );
}
```

> ⏸️ **Jeda 7**
> - [ ] `/register` tampil dengan 4 kolom + tombol Daftar
> - [ ] Link "Masuk" dan "Daftar" saling berpindah halaman dengan mulus
>
> Tampilan selesai. Mulai tahap berikutnya kita menghidupkannya.

---

## Tahap 8: Pengaturan `.env` dan "Jembatan" ke API

### 8.1 Apa itu variabel lingkungan?

Alamat backend akan berubah-ubah (lokal vs server asli). Jangan ditulis permanen di kode. Simpan di file **`.env.local`**, yang tidak ikut ke Git.

Buat file `.env.local` di **akar** `frontend/` (sejajar `package.json`):

```env
API_BASE_URL=http://localhost:8000/api/v1
USE_MOCK=true
```

**Makna:**
- `API_BASE_URL`: alamat dasar API. `http://localhost:8000` adalah port bawaan FastAPI saat dijalankan lokal. Ini **asumsi**, tanyakan ke tim backend. `/api/v1` adalah prefix yang kamu sebut.
- `USE_MOCK=true`: nyalakan **mode data tiruan**, karena backend belum siap.

> ⚠️ Setiap kali `.env.local` diubah, **hentikan server (`Ctrl + C`) lalu `npm run dev` lagi**. Next.js hanya membaca file ini saat start.

Nama variabel **tanpa** awalan `NEXT_PUBLIC_` artinya **hanya bisa dibaca di sisi server**, jadi aman dan tidak terlihat di browser pengguna.

### 8.2 Buat "jembatan" ke API

Semua komunikasi ke backend kita pusatkan di satu file. Keuntungannya: kalau backend berubah, cukup edit di sini. Buat `lib/api.ts`:

```ts
const API_BASE_URL = process.env.API_BASE_URL ?? "http://localhost:8000/api/v1";
const USE_MOCK = process.env.USE_MOCK === "true";

// ---------- Tipe data (asumsi, cocokkan dengan backend) ----------
export type LoginInput = { email: string; password: string };
export type RegisterInput = { email: string; username: string; password: string };

export type TokenOut = {
  access_token: string;
  refresh_token: string;
  token_type: string;
};
export type RegisterOut = { anon_id?: string };

// Hasil panggilan API selalu "berhasil" atau "gagal", tidak ada kemungkinan lain.
export type ApiResult<T> =
  | { ok: true; data: T }
  | { ok: false; status: number; message: string };

// ---------- Fungsi bantu ----------
function getDetail(data: unknown): string | null {
  if (typeof data === "object" && data !== null && "detail" in data) {
    const detail = (data as { detail: unknown }).detail;
    if (typeof detail === "string") return detail;
  }
  return null;
}

function errorMessage(status: number, data: unknown): string {
  if (status === 422) return "Data yang dikirim tidak valid. Periksa kembali isianmu.";
  const detail = getDetail(data);
  if (detail) return detail;
  if (status === 401) return "Email atau kata sandi salah.";
  if (status === 409) return "Email atau username sudah terdaftar.";
  return "Terjadi kesalahan pada server. Coba lagi nanti.";
}

async function post<T>(path: string, body: unknown): Promise<ApiResult<T>> {
  try {
    const res = await fetch(`${API_BASE_URL}${path}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    const data: unknown = await res.json().catch(() => null);

    if (res.ok) return { ok: true, data: data as T };
    return { ok: false, status: res.status, message: errorMessage(res.status, data) };
  } catch {
    return {
      ok: false,
      status: 0,
      message: "Tidak dapat terhubung ke server. Coba lagi nanti.",
    };
  }
}

// ---------- Data tiruan (dipakai saat USE_MOCK=true) ----------
const sleep = (ms: number) => new Promise((resolve) => setTimeout(resolve, ms));

async function mockLogin(input: LoginInput): Promise<ApiResult<TokenOut>> {
  await sleep(600); // pura-pura menunggu jaringan
  if (input.email === "test@hiddenx.app" && input.password === "Password123") {
    return {
      ok: true,
      data: {
        access_token: "mock-access-token",
        refresh_token: "mock-refresh-token",
        token_type: "bearer",
      },
    };
  }
  return { ok: false, status: 401, message: "Email atau kata sandi salah." };
}

async function mockRegister(input: RegisterInput): Promise<ApiResult<RegisterOut>> {
  await sleep(600);
  if (input.email === "sudah@hiddenx.app") {
    return { ok: false, status: 409, message: "Email sudah terdaftar." };
  }
  return { ok: true, data: { anon_id: "kabut_senja92" } };
}

// ---------- Fungsi yang dipakai aplikasi ----------
export function loginRequest(input: LoginInput) {
  return USE_MOCK ? mockLogin(input) : post<TokenOut>("/auth/login", input);
}

export function registerRequest(input: RegisterInput) {
  return USE_MOCK ? mockRegister(input) : post<RegisterOut>("/auth/register", input);
}
```

**Cara kerja, per bagian:**

- `process.env.API_BASE_URL` membaca nilai dari `.env.local`. `??` artinya "kalau kosong, pakai nilai cadangan".
- `type ApiResult<T>` adalah "kotak hasil". Hasilnya **hanya dua kemungkinan**: `{ ok: true, data }` atau `{ ok: false, message }`. Dengan begitu kode pemanggil selalu mengecek `ok` dulu.
- `fetch(...)` adalah perintah bawaan untuk **memanggil API**. `method: "POST"` artinya mengirim data. `JSON.stringify(body)` mengubah objek menjadi teks JSON (format yang dimengerti FastAPI, sesuai SRS 6.2).
- `await` artinya "tunggu sampai selesai". Fungsi yang memakainya harus ditandai `async`.
- `try { ... } catch { ... }`: coba jalankan; kalau gagal total (misalnya backend mati), jalankan blok `catch`, dan aplikasi tidak crash.
- `res.ok` bernilai `true` untuk status 200-299. Status lain (401, 409, 422, ...) dianggap gagal.
- **Mode mock:** `USE_MOCK ? mockLogin(...) : post(...)` berarti "kalau mock aktif pakai data tiruan, kalau tidak panggil backend sungguhan". Akun uji tiruan: **`test@hiddenx.app` / `Password123`**.
- Endpoint asli yang dipanggil: `${API_BASE_URL}/auth/login`, yaitu `http://localhost:8000/api/v1/auth/login`.

> ⏸️ **Jeda 8**
> - [ ] `.env.local` ada di akar `frontend/`
> - [ ] `lib/api.ts` tersimpan dan tidak ada garis bawah merah di VS Code
> - [ ] Kamu paham: `USE_MOCK=true` → data tiruan; nanti diubah `false` saat backend siap
> - [ ] Server sudah di-restart setelah membuat `.env.local`

---

## Tahap 9: Validasi Form dengan `zod` (Library Pertama yang Kita Pasang)

### 9.1 Kenapa perlu validasi?

Kita harus memastikan isian benar **sebelum** dikirim ke backend (email berformat benar, kata sandi cukup kuat, dsb.). Memang backend juga memvalidasi (SRS menyebut 422 untuk validasi gagal), tapi validasi di frontend memberi pesan yang cepat dan ramah.

**`zod`** adalah library untuk menulis aturan validasi secara rapi.

### 9.2 Pasang

```bash
npm install zod
```

**Makna:**
- `npm install` = unduh library ke proyek.
- `zod` = nama library.
- Hasilnya: folder `node_modules` bertambah, dan `package.json` bagian `dependencies` kini mencatat `zod`. Catatan itu yang membuat rekan setimmu cukup mengetik `npm install` untuk mendapatkan library yang sama.

> ⏸️ **Jeda 9a**
> - [ ] Install selesai tanpa error merah
> - [ ] Buka `package.json`: di `"dependencies"` ada baris `"zod": ...`

### 9.3 Tulis aturan validasi

Buat `lib/definitions.ts`:

```ts
import { z } from "zod";

// ---------- Aturan validasi ----------
export const loginSchema = z.object({
  email: z.email("Format email tidak valid"),
  password: z.string().min(1, "Kata sandi wajib diisi"),
});

export const registerSchema = z
  .object({
    email: z.email("Format email tidak valid"),
    username: z
      .string()
      .min(3, "Username minimal 3 karakter")
      .max(30, "Username maksimal 30 karakter")
      .regex(/^[a-zA-Z0-9_]+$/, "Hanya boleh huruf, angka, dan underscore"),
    password: z
      .string()
      .min(8, "Kata sandi minimal 8 karakter")
      .regex(/[A-Za-z]/, "Kata sandi harus mengandung huruf")
      .regex(/[0-9]/, "Kata sandi harus mengandung angka"),
    confirmPassword: z.string(),
  })
  .refine((data) => data.password === data.confirmPassword, {
    message: "Konfirmasi kata sandi tidak cocok",
    path: ["confirmPassword"],
  });

// ---------- Bentuk "state" yang dikembalikan ke form ----------
export type FormState = {
  message?: string;
  errors?: Record<string, string[] | undefined>;
  values?: { email?: string; username?: string };
};
```

**Cara kerja:**
- `z.object({...})` mendefinisikan **bentuk** data yang valid. Tiap kolom punya aturan berantai: `.min(8, "pesan")` artinya minimal 8 karakter, kalau gagal tampilkan pesan itu.
- `.regex(/[0-9]/, ...)` memastikan ada minimal satu angka. `/.../` adalah pola pencocokan teks.
- `.refine(...)` adalah aturan **kustom** yang membandingkan dua kolom. `path: ["confirmPassword"]` menentukan pesan error muncul di kolom konfirmasi.
- `FormState` adalah "kotak balasan" dari server ke form: pesan umum (`message`), error per kolom (`errors`), dan nilai yang tadi diketik (`values`) agar pengguna tidak mengetik ulang.

> ⚠️ Aturan kata sandi (minimal 8, huruf + angka) dan aturan username adalah **asumsi saya**. SRS belum menetapkannya. Samakan dengan backend agar pesan error tidak bertabrakan.

> ⏸️ **Jeda 9b**
> - [ ] `lib/definitions.ts` tidak ada garis merah
> - [ ] Kamu paham: schema = "aturan main" bentuk data yang valid

---

## Tahap 10: Menyimpan Token Login di Cookie

Saat login berhasil, backend memberi **access token** dan **refresh token** (JWT, FR-02). Kita harus menyimpannya agar pengguna tetap "masuk" saat berpindah halaman.

**Kita simpan di cookie `httpOnly`.** Artinya cookie **tidak bisa dibaca oleh JavaScript di browser**, jadi lebih aman dari pencurian lewat skrip jahat (mendukung NFR-02 tentang keamanan sesi).

Buat `lib/session.ts`:

```ts
import { cookies } from "next/headers";

export const ACCESS_COOKIE = "hx_access_token";
export const REFRESH_COOKIE = "hx_refresh_token";

const baseOptions = {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax" as const,
  path: "/",
};

export async function createSession(tokens: {
  access_token: string;
  refresh_token: string;
}) {
  const cookieStore = await cookies();

  // SRS NFR-02: access token berlaku 15-60 menit. Di sini 30 menit.
  cookieStore.set(ACCESS_COOKIE, tokens.access_token, {
    ...baseOptions,
    maxAge: 60 * 30,
  });

  // Refresh token umur lebih panjang: 7 hari.
  cookieStore.set(REFRESH_COOKIE, tokens.refresh_token, {
    ...baseOptions,
    maxAge: 60 * 60 * 24 * 7,
  });
}

export async function deleteSession() {
  const cookieStore = await cookies();
  cookieStore.delete(ACCESS_COOKIE);
  cookieStore.delete(REFRESH_COOKIE);
}
```

**Cara kerja:**
- `cookies()` dari `next/headers` adalah alat membaca/menulis cookie di sisi server. Di Next.js 16 fungsinya **wajib** dipanggil dengan `await cookies()`.
- `httpOnly: true` → tidak bisa dibaca JavaScript browser.
- `secure` → pada produksi, cookie hanya dikirim lewat HTTPS.
- `sameSite: "lax"` → perlindungan dasar terhadap serangan CSRF.
- `path: "/"` → cookie berlaku di seluruh situs.
- `maxAge` dalam **detik**. `60 * 30` = 30 menit.

> ⚠️ **Catatan jujur:** kita belum membuat alur *refresh* otomatis (`/auth/refresh`, FR-04). Untuk saat ini, setelah 30 menit pengguna diminta login ulang. Itu cukup untuk tugas login/register. Refresh token kita simpan agar siap dipakai nanti.

> ⏸️ **Jeda 10**
> - [ ] `lib/session.ts` tersimpan tanpa garis merah
> - [ ] Kamu paham: token disimpan di cookie `httpOnly`, bukan di `localStorage`

---

## Tahap 11: Login Benar-Benar Berfungsi

### 11.1 Konsep kunci: Server Action

Selama ini komponen kita hanya "menampilkan". Sekarang kita butuh **kode yang jalan di server** saat form dikirim. Di Next.js ini disebut **Server Action**:

- Ditandai dengan `"use server"` di baris pertama file.
- Dipasang ke form lewat atribut `action`.
- Isinya berjalan di **server**, sehingga aman memegang token dan memanggil backend.

**Alur login kita:**

```
Pengguna isi form → klik Masuk
   ↓
Server Action (loginAction) menerima data form
   ↓
Validasi dengan zod ── gagal → kembalikan pesan error ke form
   ↓ lulus
Panggil POST /api/v1/auth/login (lewat lib/api.ts)
   ↓ gagal → kembalikan pesan error
   ↓ berhasil
Simpan token ke cookie → pindah ke halaman "/"
```

### 11.2 Tulis Server Action

Buat `actions/auth.ts` (folder `actions` di akar proyek):

```ts
"use server";

import { redirect } from "next/navigation";
import { z } from "zod";
import { loginRequest } from "@/lib/api";
import { loginSchema, type FormState } from "@/lib/definitions";
import { createSession, deleteSession } from "@/lib/session";

export async function loginAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  // 1. Ambil nilai dari form
  const raw = {
    email: String(formData.get("email") ?? "").trim(),
    password: String(formData.get("password") ?? ""),
  };

  // 2. Validasi
  const parsed = loginSchema.safeParse(raw);
  if (!parsed.success) {
    return {
      errors: z.flattenError(parsed.error).fieldErrors,
      values: { email: raw.email },
    };
  }

  // 3. Panggil backend (atau data tiruan)
  const result = await loginRequest(parsed.data);
  if (!result.ok) {
    return { message: result.message, values: { email: raw.email } };
  }

  // 4. Simpan token, lalu pindah halaman
  await createSession(result.data);
  redirect("/");
}

export async function logoutAction() {
  await deleteSession();
  redirect("/login");
}
```

**Cara kerja, baris penting:**
- `formData: FormData` adalah paket isi form. `formData.get("email")` membaca kolom yang `name`-nya `email` (ingat Tahap 6.3).
- `_prevState`: parameter pertama berisi hasil panggilan sebelumnya. Kita tidak memakainya, awalan `_` menandakan "sengaja tidak dipakai".
- `safeParse` mengecek data terhadap aturan zod **tanpa melempar error**. Hasilnya `success: true/false`.
- `z.flattenError(parsed.error).fieldErrors` mengubah error zod menjadi bentuk `{ email: ["pesan"], password: [...] }`, siap ditampilkan per kolom.
- `redirect("/")` memindahkan pengguna. Ia **harus** dipanggil di luar blok `try/catch`, karena cara kerjanya memang "melempar" sinyal khusus.
- `logoutAction` kita tulis sekalian untuk dipakai di Tahap 13.

### 11.3 Hidupkan form login

Sekarang ganti seluruh isi `components/auth/LoginForm.tsx`:

```tsx
"use client";

import Link from "next/link";
import { useActionState } from "react";
import { loginAction } from "@/actions/auth";
import type { FormState } from "@/lib/definitions";
import TextField from "./TextField";

const initialState: FormState = {};

export default function LoginForm() {
  const [state, formAction, pending] = useActionState(loginAction, initialState);

  return (
    <form action={formAction} noValidate className="space-y-4">
      {state.message && (
        <div
          role="alert"
          className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {state.message}
        </div>
      )}

      <TextField
        label="Email"
        name="email"
        type="email"
        autoComplete="email"
        placeholder="kamu@contoh.com"
        defaultValue={state.values?.email}
        error={state.errors?.email}
      />
      <TextField
        label="Kata sandi"
        name="password"
        type="password"
        autoComplete="current-password"
        error={state.errors?.password}
      />

      <button
        type="submit"
        disabled={pending}
        className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {pending ? "Memproses..." : "Masuk"}
      </button>

      <p className="text-center text-sm text-gray-600">
        Belum punya akun?{" "}
        <Link href="/register" className="font-medium text-indigo-600 hover:underline">
          Daftar
        </Link>
      </p>
    </form>
  );
}
```

**Yang berubah dan kenapa:**
- `"use client"` di baris pertama: komponen ini kini **Client Component**, yaitu berjalan di browser, karena memakai *hook* `useActionState` yang butuh interaksi. Komponen tanpa tanda ini adalah **Server Component** (bawaan App Router).
- `useActionState(loginAction, initialState)` menghubungkan form dengan Server Action dan mengembalikan tiga hal:
  - `state`: balasan terakhir dari server (pesan/error/nilai).
  - `formAction`: pengganti `action` untuk dipasang ke `<form>`.
  - `pending`: `true` selama server memproses. Kita pakai untuk menonaktifkan tombol dan mengganti tulisannya.
- `noValidate` mematikan validasi bawaan browser, supaya pesan zod kita yang tampil dan konsisten.
- `defaultValue={state.values?.email}`: setelah submit, React mengosongkan form. Kita isi ulang email agar pengguna tidak mengetik ulang (kata sandi sengaja tidak dikembalikan demi keamanan).
- `state.errors?.email`: tanda `?.` artinya "kalau ada, ambil; kalau tidak, abaikan".

### 11.4 Tampilkan banner "berhasil daftar" di halaman login

Setelah register nanti, pengguna dialihkan ke `/login?registered=1`. Kita tampilkan pesan hijau. Ganti isi `app/(auth)/login/page.tsx`:

```tsx
import LoginForm from "@/components/auth/LoginForm";

export const metadata = { title: "Masuk | Hidden X" };

export default async function LoginPage({
  searchParams,
}: {
  searchParams: Promise<{ registered?: string }>;
}) {
  const { registered } = await searchParams;

  return (
    <>
      <h2 className="mb-4 text-xl font-semibold">Masuk ke akunmu</h2>
      {registered === "1" && (
        <div className="mb-4 rounded-lg bg-green-50 px-3 py-2 text-sm text-green-700">
          Pendaftaran berhasil. Silakan masuk.
        </div>
      )}
      <LoginForm />
    </>
  );
}
```

**Cara kerja:** `searchParams` berisi bagian URL setelah tanda `?`. Di Next.js 16 ia berupa **Promise**, jadi wajib `await`, dan fungsi halamannya ditandai `async`.

> ⏸️ **Jeda 11** (belum bisa diuji penuh karena halaman `/` belum dijaga; tetap coba)
> - [ ] Buka `/login`, klik **Masuk** dengan kolom kosong → muncul pesan merah di bawah kolom
> - [ ] Isi `test@hiddenx.app` + `salah` → muncul kotak merah "Email atau kata sandi salah."
> - [ ] Isi `test@hiddenx.app` + `Password123` → tombol berubah "Memproses...", lalu pindah ke `/`
> - [ ] DevTools (F12) → tab *Application* → *Cookies*: ada `hx_access_token`

---

## Tahap 12: Register Benar-Benar Berfungsi

### 12.1 Tambah Server Action register

Di `actions/auth.ts`, ubah **baris import** bagian atas menjadi:

```ts
import { loginRequest, registerRequest } from "@/lib/api";
import { loginSchema, registerSchema, type FormState } from "@/lib/definitions";
```

Lalu tambahkan fungsi ini **di bawah `loginAction`** (sebelum `logoutAction`):

```ts
export async function registerAction(
  _prevState: FormState,
  formData: FormData,
): Promise<FormState> {
  const raw = {
    email: String(formData.get("email") ?? "").trim(),
    username: String(formData.get("username") ?? "").trim(),
    password: String(formData.get("password") ?? ""),
    confirmPassword: String(formData.get("confirmPassword") ?? ""),
  };
  const keepValues = { email: raw.email, username: raw.username };

  const parsed = registerSchema.safeParse(raw);
  if (!parsed.success) {
    return {
      errors: z.flattenError(parsed.error).fieldErrors,
      values: keepValues,
    };
  }

  // confirmPassword hanya untuk pengecekan di frontend, tidak dikirim ke backend
  const { email, username, password } = parsed.data;
  const result = await registerRequest({ email, username, password });
  if (!result.ok) {
    return { message: result.message, values: keepValues };
  }

  redirect("/login?registered=1");
}
```

**Cara kerja:** mirip login. Bedanya, `confirmPassword` kita **buang** sebelum dikirim, karena itu hanya untuk memastikan pengguna tidak salah ketik. Setelah sukses, pengguna dialihkan ke login dengan banner hijau.

### 12.2 Hidupkan form register

Ganti seluruh isi `components/auth/RegisterForm.tsx`:

```tsx
"use client";

import Link from "next/link";
import { useActionState } from "react";
import { registerAction } from "@/actions/auth";
import type { FormState } from "@/lib/definitions";
import TextField from "./TextField";

const initialState: FormState = {};

export default function RegisterForm() {
  const [state, formAction, pending] = useActionState(registerAction, initialState);

  return (
    <form action={formAction} noValidate className="space-y-4">
      {state.message && (
        <div
          role="alert"
          className="rounded-lg bg-red-50 px-3 py-2 text-sm text-red-700"
        >
          {state.message}
        </div>
      )}

      <TextField
        label="Email"
        name="email"
        type="email"
        autoComplete="email"
        placeholder="kamu@contoh.com"
        defaultValue={state.values?.email}
        error={state.errors?.email}
      />
      <TextField
        label="Username"
        name="username"
        autoComplete="username"
        placeholder="nama_aslimu"
        hint="Disimpan terenkripsi dan tidak pernah tampil ke publik. Nama tampilanmu (Anon-ID) dibuat otomatis oleh sistem."
        defaultValue={state.values?.username}
        error={state.errors?.username}
      />
      <TextField
        label="Kata sandi"
        name="password"
        type="password"
        autoComplete="new-password"
        hint="Minimal 8 karakter, mengandung huruf dan angka."
        error={state.errors?.password}
      />
      <TextField
        label="Ulangi kata sandi"
        name="confirmPassword"
        type="password"
        autoComplete="new-password"
        error={state.errors?.confirmPassword}
      />

      <button
        type="submit"
        disabled={pending}
        className="w-full rounded-lg bg-indigo-600 px-4 py-2 text-sm font-semibold text-white hover:bg-indigo-700 disabled:cursor-not-allowed disabled:opacity-60"
      >
        {pending ? "Memproses..." : "Daftar"}
      </button>

      <p className="text-center text-sm text-gray-600">
        Sudah punya akun?{" "}
        <Link href="/login" className="font-medium text-indigo-600 hover:underline">
          Masuk
        </Link>
      </p>
    </form>
  );
}
```

> ⏸️ **Jeda 12**
> - [ ] Daftar dengan kolom kosong → muncul pesan error di tiap kolom
> - [ ] Kata sandi `abc` → "minimal 8 karakter"
> - [ ] Konfirmasi tidak sama → "Konfirmasi kata sandi tidak cocok" (muncul setelah kolom lain valid)
> - [ ] Email `sudah@hiddenx.app` (data valid) → kotak merah "Email sudah terdaftar."
> - [ ] Email lain yang valid → pindah ke `/login` dengan banner hijau

---

## Tahap 13: Beranda Sementara, Logout, dan Penjaga Halaman

### 13.1 Beranda sementara

Ganti `app/page.tsx`:

```tsx
import { logoutAction } from "@/actions/auth";

export default function HomePage() {
  return (
    <main className="mx-auto max-w-xl p-8">
      <h1 className="text-2xl font-bold">Beranda Hidden X</h1>
      <p className="mt-2 text-gray-600">
        Kamu berhasil masuk 🎉 (halaman sementara, feed akan dibuat nanti).
      </p>
      <form action={logoutAction} className="mt-6">
        <button
          type="submit"
          className="rounded-lg border border-gray-300 px-4 py-2 text-sm hover:bg-gray-100"
        >
          Keluar
        </button>
      </form>
    </main>
  );
}
```

**Cara kerja:** `<form action={logoutAction}>` langsung memanggil Server Action tanpa komponen client, karena tidak butuh state. Logout kita baru menghapus cookie. Memanggil `POST /auth/logout` (FR-03) ke backend bisa ditambahkan nanti.

### 13.2 Penjaga halaman: `proxy.ts`

Kita ingin: belum login → tidak boleh membuka `/`; sudah login → tidak perlu melihat `/login` dan `/register`. Buat `proxy.ts` **di akar `frontend/`** (sejajar `package.json`, **bukan** di dalam `app/`):

```ts
import { NextResponse, type NextRequest } from "next/server";

const ACCESS_COOKIE = "hx_access_token";

export function proxy(request: NextRequest) {
  const { pathname } = request.nextUrl;
  const isLoggedIn = request.cookies.has(ACCESS_COOKIE);
  const isAuthPage = pathname === "/login" || pathname === "/register";

  if (!isLoggedIn && !isAuthPage) {
    return NextResponse.redirect(new URL("/login", request.url));
  }
  if (isLoggedIn && isAuthPage) {
    return NextResponse.redirect(new URL("/", request.url));
  }
  return NextResponse.next();
}

export const config = {
  matcher: ["/", "/login", "/register"],
};
```

**Cara kerja:**
- Di Next.js 16, file yang dulu bernama `middleware.ts` **diganti nama menjadi `proxy.ts`**, dan fungsinya bernama `proxy`. Kalau kamu membaca tutorial lama yang memakai `middleware.ts`, itu gaya versi lama.
- `proxy` berjalan **sebelum** halaman dirender, seperti satpam di pintu gerbang.
- `matcher` menentukan alamat mana yang dijaga: hanya `/`, `/login`, `/register`. Nanti tambahkan halaman lain (mis. `/notifications`) ke daftar ini.
- Penjaga ini cuma memeriksa **ada tidaknya** cookie, bukan keabsahan token. Keamanan sebenarnya tetap tugas backend yang memverifikasi JWT di setiap endpoint terproteksi. Penjaga ini hanya urusan kenyamanan tampilan.

> Setelah membuat `proxy.ts`, kalau perilakunya aneh, hentikan server lalu `npm run dev` lagi.

> ⏸️ **Jeda 13**
> - [ ] Belum login, buka `/` → otomatis ke `/login`
> - [ ] Sudah login, buka `/login` → otomatis ke `/`
> - [ ] Klik **Keluar** → kembali ke `/login`, cookie hilang

---

## Tahap 14: Uji Coba Manual

Jalankan semua skenario berikut (mode mock):

| # | Skenario | Hasil yang benar |
| --- | --- | --- |
| 1 | Login kolom kosong | Pesan error di bawah kolom |
| 2 | Login email salah format | "Format email tidak valid" |
| 3 | Login `test@hiddenx.app` / `salah` | Kotak merah "Email atau kata sandi salah." |
| 4 | Login `test@hiddenx.app` / `Password123` | Masuk ke `/`, cookie ada |
| 5 | Buka `/` tanpa login | Diarahkan ke `/login` |
| 6 | Register username `a!` | Pesan username tidak valid |
| 7 | Register email `sudah@hiddenx.app` | "Email sudah terdaftar." |
| 8 | Register data valid | Pindah ke `/login` + banner hijau |
| 9 | Refresh browser saat sudah login | Tetap login |

Lalu cek kualitas kode:

```bash
npm run build
```

**Makna:** `build` membuat versi produksi dan **memeriksa kesalahan TypeScript** di seluruh proyek. Kalau lolos tanpa error merah, kodemu sehat. Kalau ada error, kirim ke saya. Di Next.js 16 perintah ini tidak lagi menjalankan linter otomatis. Untuk linter, jalankan `npm run lint` (jika skrip itu ada di `package.json`).

> ⏸️ **Jeda 14**
> - [ ] Sembilan skenario berhasil
> - [ ] `npm run build` selesai tanpa error

---

## Tahap 15: Sambung ke Backend Asli

Kerjakan ini **saat tim backend memberi tahu endpoint sudah siap**.

1. **Konfirmasi kontrak** dengan tim backend (lihat [Lampiran A](#lampiran-a--asumsi-kontrak-api-wajib-dicocokkan-dengan-tim-backend)).
2. Pastikan backend FastAPI berjalan, misalnya di `http://localhost:8000`. Cek lewat dokumentasi Swagger bawaan FastAPI di `http://localhost:8000/docs` (NFR-07).
3. Ubah `.env.local`:

   ```env
   API_BASE_URL=http://localhost:8000/api/v1
   USE_MOCK=false
   ```

4. Hentikan server (`Ctrl + C`), jalankan lagi `npm run dev`.
5. Ulangi skenario di Tahap 14 dengan akun sungguhan.

**Kenapa tidak ada urusan CORS?** CORS adalah aturan browser saat halaman web memanggil API di alamat lain. Panggilan kita dilakukan oleh **Server Action di server Next.js**, bukan oleh browser, jadi aman dari masalah itu.

Kalau gagal, bacalah pesan di kotak merah form, lalu cek terminal tempat `npm run dev` berjalan. Pesan error server tampil di sana.

---

## Lampiran A: Asumsi Kontrak API (WAJIB dicocokkan dengan tim backend)

SRS hanya menyebut endpoint dan perilaku umum, bukan isi JSON. Berikut asumsi saya:

| Hal | Asumsi di panduan ini | Sumber | Jika berbeda, ubah di |
| --- | --- | --- | --- |
| Base URL | `http://localhost:8000/api/v1` | prefix dari kamu; port bawaan FastAPI | `.env.local` |
| Register: body | `{ "email", "username", "password" }` | FR-01 + tabel `users` (`username_asli`) | `RegisterInput` di `lib/api.ts` |
| Register: sukses | 201/200 dengan `{ "anon_id": "..." }` | FR-01 (sistem menerbitkan Anon-ID) | `RegisterOut` |
| Login: body | `{ "email", "password" }` | FR-02 | `LoginInput` |
| Login: sukses | `{ "access_token", "refresh_token", "token_type" }` | skema `TokenOut`, FR-02 | `TokenOut`, `createSession` |
| Error umum | `{ "detail": "pesan" }`; 401 login salah, 409 duplikat, 422 validasi | format bawaan FastAPI; 422 disebut SRS 6.2 | fungsi `errorMessage` |
| Aturan kata sandi | min. 8 karakter, huruf + angka | tidak ada di SRS | `lib/definitions.ts` |
| Masa access token | cookie 30 menit | NFR-02 (15-60 menit) | `lib/session.ts` |

Pertanyaan untuk tim backend: *nama field register apa saja? Apakah login memakai email atau username? Bentuk error persisnya bagaimana? Port dan alamat backend?*

---

## Lampiran B: Struktur Akhir `hiddenx/frontend`

```
hiddenx/
└── frontend/
    ├── app/
    │   ├── (auth)/
    │   │   ├── layout.tsx
    │   │   ├── login/page.tsx
    │   │   └── register/page.tsx
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx
    ├── actions/
    │   └── auth.ts                 ← loginAction, registerAction, logoutAction
    ├── components/
    │   └── auth/
    │       ├── TextField.tsx
    │       ├── LoginForm.tsx
    │       └── RegisterForm.tsx
    ├── lib/
    │   ├── api.ts                  ← jembatan ke backend + mock
    │   ├── definitions.ts          ← aturan zod + tipe FormState
    │   └── session.ts              ← cookie token
    ├── proxy.ts                    ← penjaga halaman
    ├── .env.local                  ← tidak ikut Git
    ├── package.json
    └── next.config.ts
```

---

## Lampiran C: Daftar Perintah Terminal

| Perintah | Makna |
| --- | --- |
| `node -v` / `npm -v` | cek versi Node.js / npm |
| `mkdir nama` | buat folder |
| `cd nama` / `cd ..` | masuk folder / naik satu tingkat |
| `npx create-next-app@latest frontend` | buat proyek Next.js baru bernama `frontend` |
| `npm run dev` | jalankan server pengembangan (http://localhost:3000) |
| `npm install zod` | pasang library `zod` ke proyek |
| `npm ls next` | tampilkan versi `next` yang terpasang |
| `npm run build` | buat versi produksi + cek error TypeScript |
| `Ctrl + C` | hentikan program yang sedang berjalan di terminal |

---

## Lampiran D: Pemecahan Masalah Umum

| Gejala | Penyebab / solusi |
| --- | --- |
| `npm` / `node` "not recognized" | Tutup semua terminal lalu buka lagi. Kalau masih, pasang ulang Node.js |
| Windows PowerShell: "running scripts is disabled" | Pakai Command Prompt, atau jalankan di PowerShell: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `Port 3000 is in use` | Ada server lain di port itu. Tutup, atau Next.js akan menawarkan port lain (3001) |
| `Module not found: @/...` | Cek ejaan nama file/folder (huruf besar-kecil berpengaruh) dan lokasi di akar `frontend/`, bukan di dalam `app/` |
| Error tentang `useActionState` / "use client" | Pastikan `"use client";` ada di **baris pertama** form |
| Perubahan `.env.local` tidak terbaca | Restart `npm run dev` |
| Halaman `/login` 404 | Pastikan path-nya `app/(auth)/login/page.tsx` dan nama file persis `page.tsx` |
| Pengalihan berulang (redirect loop) | Cek `matcher` dan logika di `proxy.ts`; hapus cookie lewat DevTools lalu coba lagi |
| Garis bawah merah di VS Code tapi halaman jalan | Biasanya salah tipe TypeScript. Baca pesannya saat diarahkan kursor, atau tanyakan ke saya |

---

## Setelah ini

Urutan yang masuk akal berdasarkan SRS:

1. Sambungkan ke backend asli (Tahap 15).
2. Tambah alur **refresh token** (FR-04, `POST /auth/refresh`).
3. Panggil `POST /auth/logout` ke backend (FR-03).
4. Halaman **Feed** (FR-11) dan **Buat Post** (FR-05, validasi maksimal 280 karakter).
5. **Profil publik Anon-ID** (FR-12) yang bisa dilihat Guest.

Saat kamu siap, beri tahu saya tahap mana yang sedang dikerjakan, atau tempel pesan error-nya. Kita selesaikan bersama.
