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
