import { AppShell } from '@/components/app-shell';

export default function TeamPage() {
  return (
    <AppShell>
      <div className="panel p-8">
        <p className="section-label">Team</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900 dark:text-white">Collaboration workspace</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
          This page is intended for roles, permissions, project ownership, and cross-functional collaboration later on.
        </p>
        <div className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center dark:border-slate-700 dark:bg-slate-800/50">
          <p className="text-lg font-medium text-slate-700 dark:text-slate-200">No team data yet</p>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">Team directory and access management will be added when the platform matures.</p>
        </div>
      </div>
    </AppShell>
  );
}
