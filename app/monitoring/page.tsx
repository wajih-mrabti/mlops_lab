import { AppShell } from '@/components/app-shell';

export default function MonitoringPage() {
  return (
    <AppShell>
      <div className="panel p-8">
        <p className="section-label">Monitoring</p>
        <h1 className="mt-3 text-3xl font-semibold text-slate-900 dark:text-white">Platform observability</h1>
        <p className="mt-3 max-w-2xl text-slate-600 dark:text-slate-300">
          Monitoring will summarize model health and service performance when the platform grows.
        </p>
      </div>
    </AppShell>
  );
}
