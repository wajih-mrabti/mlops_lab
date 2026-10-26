'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import { useTheme } from '@/components/theme-provider';
import { navItems } from '@/lib/navigation';

const iconMap = {
  overview: '◫',
  models: '◎',
  experiments: '▣',
  deployments: '◌',
  monitoring: '◍',
  team: '◐',
};

export function AppShell({ children }: { children: React.ReactNode }) {
  const pathname = usePathname();
  const { theme, toggleTheme } = useTheme();
  const currentItem = navItems.find((item) => item.href === pathname) ?? navItems[0];

  const buttonLabel = theme === 'light' ? 'Dark mode' : 'Light mode';

  return (
    <div className="min-h-screen bg-slate-100 text-slate-900 dark:bg-slate-950 dark:text-slate-100">
      <div className="mx-auto flex min-h-screen max-w-[1800px]">
        <aside className="w-full max-w-[280px] border-r border-slate-200 bg-slate-50/90 p-5 dark:border-slate-800 dark:bg-slate-900/90">
          <div className="mb-8 flex items-center gap-3 px-2">
            <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-600 text-sm font-bold text-white shadow-lg shadow-brand-500/30">
              M
            </div>
            <div>
              <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">
                Platform
              </p>
              <h1 className="text-lg font-semibold text-slate-900 dark:text-white">ModelOps Lab</h1>
            </div>
          </div>

          <nav aria-label="Sidebar navigation" className="space-y-1">
            {navItems.map((item) => {
              const isActive = pathname === item.href;

              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={[
                    'group flex items-center gap-3 rounded-xl px-3 py-2.5 text-sm font-medium transition-colors',
                    isActive
                      ? 'bg-brand-50 text-brand-700 ring-1 ring-brand-200 dark:bg-brand-500/10 dark:text-brand-100 dark:ring-brand-400/30'
                      : 'text-slate-600 hover:bg-slate-200/80 hover:text-slate-900 dark:text-slate-300 dark:hover:bg-slate-800 dark:hover:text-white',
                  ].join(' ')}
                >
                  <span className="flex h-7 w-7 items-center justify-center rounded-lg bg-slate-200 text-xs text-slate-600 dark:bg-slate-800 dark:text-slate-300">
                    {iconMap[item.id as keyof typeof iconMap]}
                  </span>
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </nav>

          <div className="mt-10 rounded-2xl border border-dashed border-slate-300 bg-slate-100 p-4 text-sm text-slate-600 dark:border-slate-700 dark:bg-slate-800/70 dark:text-slate-300">
            <p className="font-semibold text-slate-700 dark:text-slate-200">Portfolio note</p>
            <p className="mt-1">The platform shell is intentionally model-agnostic and prepared for future API integration.</p>
          </div>
        </aside>

        <div className="flex min-w-0 flex-1 flex-col">
          <header className="border-b border-slate-200 bg-white/80 px-4 py-4 backdrop-blur-sm dark:border-slate-800 dark:bg-slate-950/80 sm:px-6 lg:px-8">
            <div className="flex items-center justify-between gap-4">
              <div>
                <p className="text-xs font-semibold uppercase tracking-[0.2em] text-slate-500 dark:text-slate-400">Workspace / {currentItem.label}</p>
                <h2 className="mt-1 text-xl font-semibold text-slate-900 dark:text-white">{currentItem.label}</h2>
              </div>

              <div className="flex items-center gap-3">
                <button
                  type="button"
                  onClick={toggleTheme}
                  aria-label="Toggle color theme"
                  className="inline-flex items-center justify-center rounded-xl border border-slate-200 bg-slate-100 px-3 py-2 text-sm font-medium text-slate-700 transition hover:bg-slate-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-brand-500 dark:border-slate-700 dark:bg-slate-800 dark:text-slate-200 dark:hover:bg-slate-700"
                >
                  {buttonLabel}
                </button>
                <div className="flex items-center gap-3 rounded-xl border border-slate-200 bg-slate-100 px-3 py-2 dark:border-slate-700 dark:bg-slate-800">
                  <div className="flex h-8 w-8 items-center justify-center rounded-full bg-brand-100 text-xs font-semibold text-brand-700 dark:bg-brand-500/20 dark:text-brand-100">
                    WM
                  </div>
                  <div className="hidden text-left sm:block">
                    <p className="text-sm font-medium text-slate-900 dark:text-white">Wajih Mrabti</p>
                    <p className="text-[11px] uppercase tracking-[0.15em] text-slate-500 dark:text-slate-400">Admin</p>
                  </div>
                </div>
              </div>
            </div>
          </header>

          <main className="flex-1 p-4 sm:p-6 lg:p-8">{children}</main>
        </div>
      </div>
    </div>
  );
}
