'use client'

export default function ResultGridSkeleton() {
  return (
    <section>
      <header className="mb-4 flex items-end justify-between">
        <h3 className="text-sm font-semibold uppercase tracking-wider text-text-primary dark:text-dark-text-primary">6-SIEVE RESULT GRID</h3>
        <span className="text-xs uppercase tracking-[0.2em] text-stone-500 dark:text-stone-400">2 x 3 Forensic Matrix</span>
      </header>

      <div className="grid gap-4 md:grid-cols-2 xl:grid-cols-3">
        {Array.from({ length: 6 }).map((_, index) => (
          <article
            key={index}
            className="rounded-2xl border border-subtle-border dark:border-slate-700 bg-background dark:bg-dark-panel p-5 animate-pulse"
          >
            <div className="mb-3 flex items-start justify-between gap-2">
              <div className="space-y-2">
                <div className="h-5 w-24 rounded bg-stone-200 dark:bg-slate-700" />
                <div className="h-3 w-36 rounded bg-stone-100 dark:bg-slate-800" />
              </div>
              <div className="h-5 w-14 rounded-full bg-stone-200 dark:bg-slate-700" />
            </div>

            <div className="mt-4 space-y-2">
              <div className="h-4 w-full rounded bg-stone-200 dark:bg-slate-700" />
              <div className="h-4 w-3/4 rounded bg-stone-100 dark:bg-slate-800" />
            </div>
          </article>
        ))}
      </div>
    </section>
  )
}
