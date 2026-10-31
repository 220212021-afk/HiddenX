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
