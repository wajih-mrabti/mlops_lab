import { AppShell } from '@/components/app-shell';

export default function ModelsPage() {
  return (
    <AppShell>
      <div className="panel p-8">
        <p className="section-label">Models</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900 dark:text-white">Model registry</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
          This section is reserved for model catalog, version history, and lifecycle management.
        </p>
      </div>
    </AppShell>
  );
}
