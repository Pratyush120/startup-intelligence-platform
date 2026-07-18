export default function LoginPage() {
  return (
    <div className="w-full max-w-md p-8 bg-surface-1 border border-border-default rounded-lg elevation-2">
      <h1 className="heading-xl text-primary mb-2">SDIP Login</h1>
      <p className="body-md text-secondary mb-6">Enter your credentials to access the Strategic Decision Intelligence Platform.</p>
      {/* Form would go here */}
      <button className="w-full h-11 bg-primary text-inverted caption-md uppercase tracking-[0.06em]">
        Sign In
      </button>
    </div>
  );
}
