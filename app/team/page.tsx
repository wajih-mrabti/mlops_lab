import { AppShell } from '@/components/app-shell';

export default function TeamPage() {
  return (
    <AppShell>
      <div className="panel p-8">
        <p className="section-label">Team</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900 dark:text-white">Collaboration workspace</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
          This page is intended for roles, permissions, and team ownership later on.
        </p>
      </div>
    </AppShell>
  );
}
