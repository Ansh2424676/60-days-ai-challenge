"use client";

import { useState } from "react";

type FeedbackButtonsProps = {
  onSubmit: (rating: "positive" | "negative") => Promise<void>;
};

export default function FeedbackButtons({
  onSubmit,
}: FeedbackButtonsProps) {
  const [submitted, setSubmitted] = useState<"positive" | "negative" | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(rating: "positive" | "negative") {
    setLoading(true);
    setError("");

    try {
      await onSubmit(rating);
      setSubmitted(rating);
    } catch {
      setError("Feedback could not be saved. Please try again.");
    } finally {
      setLoading(false);
    }
  }

  if (submitted) {
    return (
      <p className="text-sm text-slate-600" role="status">
        Thanks! Your feedback has been recorded.
      </p>
    );
  }

  return (
    <div className="flex flex-wrap items-center gap-3">
      <span className="text-sm text-slate-600">Was this helpful?</span>

      <button
        type="button"
        disabled={loading}
        onClick={() => handleSubmit("positive")}
        className="rounded-lg border border-slate-300 px-3 py-2 text-sm hover:bg-slate-100 disabled:opacity-50"
        aria-label="Mark response helpful"
      >
        👍 Helpful
      </button>

      <button
        type="button"
        disabled={loading}
        onClick={() => handleSubmit("negative")}
        className="rounded-lg border border-slate-300 px-3 py-2 text-sm hover:bg-slate-100 disabled:opacity-50"
        aria-label="Mark response not helpful"
      >
        👎 Not helpful
      </button>

      {error && (
        <p className="w-full text-sm text-red-700" role="alert">
          {error}
        </p>
      )}
    </div>
  );
}
