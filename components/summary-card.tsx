type Tone = 'positive' | 'neutral' | 'warning';

type SummaryCardProps = {
  label: string;
  value: string;
  delta: string;
  tone: Tone;
};

const toneClasses: Record<Tone, string> = {
  positive: 'bg-emerald-50 text-emerald-700 dark:bg-emerald-500/10 dark:text-emerald-200',
  neutral: 'bg-sky-50 text-sky-700 dark:bg-sky-500/10 dark:text-sky-200',
  warning: 'bg-amber-50 text-amber-700 dark:bg-amber-500/10 dark:text-amber-200',
};

export function SummaryCard({ label, value, delta, tone }: SummaryCardProps) {
  return (
    <div className="panel p-5">
      <div className="flex items-start justify-between gap-3">
        <div>
          <p className="section-label">{label}</p>
          <p className="mt-3 text-3xl font-semibold tracking-tight text-slate-900 dark:text-white">{value}</p>
        </div>
        <span className={`rounded-full px-2.5 py-1 text-xs font-medium ${toneClasses[tone]}`}>{delta}</span>
      </div>
    </div>
  );
}
