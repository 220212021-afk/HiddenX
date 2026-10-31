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
