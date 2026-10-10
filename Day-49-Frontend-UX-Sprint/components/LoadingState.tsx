"use client";

export function ResearchSkeleton() {
  return (
    <div
      role="status"
      aria-label="Preparing research response"
      className="animate-pulse space-y-4 rounded-xl border border-slate-200 bg-white p-5"
    >
      <div className="h-4 w-1/3 rounded bg-slate-200" />
      <div className="h-3 w-full rounded bg-slate-200" />
      <div className="h-3 w-11/12 rounded bg-slate-200" />
      <div className="h-3 w-4/5 rounded bg-slate-200" />
      <div className="h-20 rounded-lg bg-slate-100" />
      <span className="sr-only">Preparing your research response...</span>
    </div>
  );
}

export function TypingIndicator() {
  return (
    <div
      role="status"
      aria-label="Research response is streaming"
      className="flex items-center gap-2 text-sm text-slate-600"
    >
      <span className="flex gap-1" aria-hidden="true">
        <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500 [animation-delay:-0.2s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500 [animation-delay:-0.1s]" />
        <span className="h-2 w-2 animate-bounce rounded-full bg-blue-500" />
      </span>
      <span>ResearchMate is researching...</span>
    </div>
  );
}
