import { AppShell } from '@/components/app-shell';

export default function MonitoringPage() {
  return (
    <AppShell>
      <div className="panel p-8">
        <p className="section-label">Monitoring</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900 dark:text-white">Platform observability</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
          Monitoring will eventually summarize model health, deployment drift, and performance signals across services.
        </p>
        <div className="mt-8 rounded-2xl border border-dashed border-slate-300 bg-slate-50 p-8 text-center dark:border-slate-700 dark:bg-slate-800/50">
          <p className="text-lg font-medium text-slate-700 dark:text-slate-200">Monitoring views not implemented yet</p>
          <p className="mt-2 text-sm text-slate-500 dark:text-slate-400">This is a placeholder for dashboards, alerts, and drift monitoring.</p>
        </div>
      </div>
    </AppShell>
  );
}
