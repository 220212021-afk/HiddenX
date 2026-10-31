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
