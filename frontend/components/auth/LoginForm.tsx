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
