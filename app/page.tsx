import { AppShell } from '@/components/app-shell';
import { SummaryCard } from '@/components/summary-card';
import { recentActivity, recentModels, summaryCards } from '@/lib/mock-data';

const stageStyles = {
  production: 'bg-emerald-100 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-200',
  staging: 'bg-amber-100 text-amber-700 dark:bg-amber-500/10 dark:text-amber-200',
  candidate: 'bg-sky-100 text-sky-700 dark:bg-sky-500/10 dark:text-sky-200',
};

export default function HomePage() {
  return (
    <AppShell>
      <div className="space-y-6">
        <section className="panel p-6 sm:p-7">
          <div className="flex flex-col gap-6 lg:flex-row lg:items-end lg:justify-between">
            <div>
              <p className="section-label">Welcome</p>
              <h1 className="mt-3 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white sm:text-4xl">
                Build and operate a healthy machine learning platform.
              </h1>
              <p className="mt-3 max-w-2xl text-sm text-slate-600 dark:text-slate-300 sm:text-base">
                ModelOps Lab gives teams a single place to manage models, review experiments, and keep deployment workflows
                clear as the platform grows.
              </p>
            </div>

            <div className="flex flex-wrap gap-3">
              <button
                type="button"
                className="rounded-xl bg-brand-600 px-4 py-2.5 text-sm font-medium text-white shadow-lg shadow-brand-500/20 transition hover:bg-brand-500 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 focus-visible:ring-offset-2 dark:focus-visible:ring-offset-slate-950"
              >
                New model request
              </button>
              <button
                type="button"
                className="rounded-xl border border-slate-200 bg-white px-4 py-2.5 text-sm font-medium text-slate-700 transition hover:bg-slate-100 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-100 dark:hover:bg-slate-700"
              >
                Review workspace
              </button>
            </div>
          </div>
        </section>

        <section className="grid gap-4 md:grid-cols-2 xl:grid-cols-4">
          {summaryCards.map((card) => (
            <SummaryCard key={card.label} {...card} />
          ))}
        </section>

        <section className="grid gap-6 xl:grid-cols-[1.1fr_0.9fr]">
          <div className="panel p-5 sm:p-6">
            <div className="mb-5 flex items-center justify-between">
              <div>
                <p className="section-label">Inventory</p>
                <h2 className="mt-2 text-xl font-semibold text-slate-900 dark:text-white">Recent models</h2>
              </div>
              <a href="/models" className="text-sm font-medium text-brand-600 hover:text-brand-500 dark:text-brand-300 dark:hover:text-brand-200">
                View all
              </a>
            </div>

            <div className="overflow-x-auto">
              <table className="min-w-full text-left text-sm">
                <thead>
                  <tr className="border-b border-slate-200 text-slate-500 dark:border-slate-700 dark:text-slate-400">
                    <th className="pb-3 pr-4 font-medium">Name</th>
                    <th className="pb-3 pr-4 font-medium">Version</th>
                    <th className="pb-3 pr-4 font-medium">Stage</th>
                    <th className="pb-3 pr-4 font-medium">Owner</th>
                    <th className="pb-3 font-medium">Updated</th>
                  </tr>
                </thead>
                <tbody>
                  {recentModels.map((model) => (
                    <tr key={`${model.name}-${model.version}`} className="border-b border-slate-200 last:border-0 dark:border-slate-800">
                      <td className="py-3 pr-4 font-medium text-slate-800 dark:text-slate-100">{model.name}</td>
                      <td className="py-3 pr-4 text-slate-600 dark:text-slate-300">{model.version}</td>
                      <td className="py-3 pr-4">
                        <span className={`rounded-full px-2 py-1 text-xs font-medium ${stageStyles[model.stage]}`}>
                          {model.stage}
                        </span>
                      </td>
                      <td className="py-3 pr-4 text-slate-600 dark:text-slate-300">{model.owner}</td>
                      <td className="py-3 text-slate-600 dark:text-slate-300">{model.updated}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="panel p-5 sm:p-6">
            <div className="mb-5">
              <p className="section-label">Activity</p>
              <h2 className="mt-2 text-xl font-semibold text-slate-900 dark:text-white">Recent activity</h2>
            </div>
            <ul className="space-y-4">
              {recentActivity.map((item) => (
                <li key={item.id} className="flex gap-3 rounded-xl border border-slate-200 bg-slate-50 p-3 dark:border-slate-800 dark:bg-slate-800/60">
                  <div className="mt-1 flex h-2.5 w-2.5 shrink-0 rounded-full bg-brand-500" />
                  <div className="min-w-0 flex-1">
                    <p className="font-medium text-slate-800 dark:text-slate-100">{item.title}</p>
                    <p className="mt-1 text-sm text-slate-600 dark:text-slate-300">{item.detail}</p>
                    <p className="mt-2 text-[11px] font-medium uppercase tracking-[0.12em] text-slate-500 dark:text-slate-400">
                      {item.time}
                    </p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </section>
      </div>
    </AppShell>
  );
}
