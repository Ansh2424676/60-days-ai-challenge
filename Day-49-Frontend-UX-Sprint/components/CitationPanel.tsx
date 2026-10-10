"use client";

import { useState } from "react";

export type ResearchCitation = {
  documentName: string;
  excerpt: string;
  similarityScore?: number;
};

type CitationPanelProps = {
  citations: ResearchCitation[];
};

export default function CitationPanel({
  citations,
}: CitationPanelProps) {
  const [isOpen, setIsOpen] = useState(false);

  if (citations.length === 0) {
    return (
      <p className="text-sm text-slate-500">
        No citations available for this response.
      </p>
    );
  }

  return (
    <section className="overflow-hidden rounded-xl border border-slate-200 bg-white">
      <button
        type="button"
        aria-expanded={isOpen}
        onClick={() => setIsOpen((previous) => !previous)}
        className="flex w-full items-center justify-between gap-3 p-4 text-left hover:bg-slate-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
      >
        <span className="font-semibold text-slate-800">
          Sources ({citations.length})
        </span>
        <span aria-hidden="true" className="text-slate-500">
          {isOpen ? "−" : "+"}
        </span>
      </button>

      {isOpen && (
        <div className="space-y-3 border-t border-slate-200 p-4">
          {citations.map((citation, index) => (
            <article
              key={`${citation.documentName}-${index}`}
              className="rounded-lg border border-slate-100 bg-slate-50 p-3"
            >
              <h3 className="font-medium text-slate-900">
                {citation.documentName}
              </h3>

              <p className="mt-2 whitespace-pre-wrap text-sm leading-6 text-slate-700">
                {citation.excerpt}
              </p>

              {typeof citation.similarityScore === "number" && (
                <p className="mt-2 text-xs text-slate-500">
                  Similarity score:{" "}
                  {citation.similarityScore.toFixed(3)}
                </p>
              )}
            </article>
          ))}
        </div>
      )}
    </section>
  );
}
