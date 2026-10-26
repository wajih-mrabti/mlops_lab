import { AppShell } from '@/components/app-shell';

export default function HomePage() {
  return (
    <AppShell>
      <div className="space-y-6">
        <section className="panel p-6 sm:p-7">
          <p className="section-label">Welcome</p>
          <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
            Build and operate a healthy machine learning platform.
          </h1>
          <p className="mt-3 max-w-2xl text-sm text-slate-600 dark:text-slate-300 sm:text-base">
            ModelOps Lab gives teams a single place to manage models, review experiments, and keep deployment workflows clear as the platform grows.
          </p>
        </section>
      </div>
    </AppShell>
  );
}
