import { AppShell } from '@/components/app-shell';

export default function ExperimentsPage() {
  return (
    <AppShell>
      <div className="panel p-8">
        <p className="section-label">Experiments</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900 dark:text-white">Experiment tracking</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
          This page will eventually contain run tracking and model comparison views.
        </p>
      </div>
    </AppShell>
  );
}
