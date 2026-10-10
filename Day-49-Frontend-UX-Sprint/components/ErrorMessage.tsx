"use client";

type ErrorMessageProps = {
  code?: string;
  message?: string;
  onRetry?: () => void;
};

const ERROR_DETAILS: Record<string, { title: string; description: string }> = {
  LLM_TIMEOUT: {
    title: "Research is taking too long",
    description: "The AI service did not respond in time. Please try again.",
  },
  RETRIEVAL_FAILURE: {
    title: "Could not retrieve research sources",
    description: "The source search failed. Please retry your research question.",
  },
  "400": {
    title: "Invalid request",
    description: "Check your research question and try again.",
  },
  "422": {
    title: "Request could not be processed",
    description: "Some required information may be missing or invalid.",
  },
  "429": {
    title: "Too many requests",
    description: "Please wait a little before trying again.",
  },
  "500": {
    title: "Server error",
    description: "Something went wrong on the server. Please try again.",
  },
  "502": {
    title: "Research service unavailable",
    description: "The AI service returned an invalid response.",
  },
  "503": {
    title: "Service temporarily unavailable",
    description: "The service is temporarily unavailable. Try again shortly.",
  },
  "504": {
    title: "Request timed out",
    description: "The server took too long to respond. Please retry.",
  },
};

export default function ErrorMessage({
  code,
  message,
  onRetry,
}: ErrorMessageProps) {
  const details = ERROR_DETAILS[code ?? ""] ?? {
    title: "Unable to complete research",
    description:
      message || "An unexpected error occurred. Please try again.",
  };

  return (
    <section
      role="alert"
      className="rounded-xl border border-red-200 bg-red-50 p-4 text-red-900"
    >
      <h3 className="font-semibold">{details.title}</h3>
      <p className="mt-1 text-sm">{details.description}</p>

      {code && (
        <p className="mt-2 text-xs text-red-700">
          Error code: {code}
        </p>
      )}

      {onRetry && (
        <button
          type="button"
          onClick={onRetry}
          className="mt-3 rounded-lg bg-red-700 px-4 py-2 text-sm font-medium text-white hover:bg-red-800 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2"
        >
          Try again
        </button>
      )}
    </section>
  );
}
