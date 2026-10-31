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
