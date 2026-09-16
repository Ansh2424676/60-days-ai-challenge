"use client";

import { FormEvent, useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

type Source = {
  id: string;
};

type Message = {
  role: "user" | "assistant";
  content: string;
  sources?: Source[];
};

export default function Home() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event: FormEvent) {
    event.preventDefault();

    const query = input.trim();

    if (!query || loading) {
      return;
    }

    setError("");
    setInput("");

    setMessages((previous) => [
      ...previous,
      {
        role: "user",
        content: query,
      },
    ]);

    setLoading(true);

    try {
      const response = await fetch("http://127.0.0.1:8000/chat/stream", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          query,
          stream: true,
        }),
      });

      if (!response.ok) {
        const errorData = await response.json();

        throw new Error(
          errorData.message || "Unable to get a response from the AI."
        );
      }

      if (!response.body) {
        throw new Error("Streaming response is not available.");
      }

      setMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: "",
        },
      ]);

      const reader = response.body.getReader();
      const decoder = new TextDecoder();

      let assistantResponse = "";

      while (true) {
        const { value, done } = await reader.read();

        if (done) {
          break;
        }

        const chunk = decoder.decode(value, { stream: true });

        assistantResponse += chunk;

        setMessages((previous) => {
          const updated = [...previous];

          updated[updated.length - 1] = {
            role: "assistant",
            content: assistantResponse,
          };

          return updated;
        });
      }
    } catch (err) {
      const message =
        err instanceof Error
          ? err.message
          : "Unable to connect to the AI backend.";

      setError(message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto flex min-h-screen max-w-4xl flex-col px-4 py-6 sm:px-6">
        <header className="border-b border-slate-800 pb-5">
          <h1 className="text-2xl font-bold sm:text-3xl">
            AI Knowledge Assistant
          </h1>

          <p className="mt-2 text-sm text-slate-400">
            Ask questions and get AI-powered answers.
          </p>
        </header>

        <section className="flex-1 space-y-5 overflow-y-auto py-6">
          {messages.length === 0 && (
            <div className="rounded-2xl border border-slate-800 bg-slate-900 p-6 text-center">
              <h2 className="text-lg font-semibold">
                Welcome 👋
              </h2>

              <p className="mt-2 text-sm text-slate-400">
                Ask me anything about your knowledge base.
              </p>
            </div>
          )}

          {messages.map((message, index) => (
            <div
              key={index}
              className={
                message.role === "user"
                  ? "ml-auto max-w-[90%] rounded-2xl bg-blue-600 p-4 sm:max-w-[75%]"
                  : "mr-auto max-w-[95%] rounded-2xl border border-slate-800 bg-slate-900 p-4 sm:max-w-[85%]"
              }
            >
              <div className="mb-2 text-xs font-semibold uppercase tracking-wide text-slate-400">
                {message.role === "user" ? "You" : "AI Assistant"}
              </div>

              {message.role === "assistant" ? (
                <div className="prose prose-invert max-w-none text-sm">
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {message.content}
                  </ReactMarkdown>
                </div>
              ) : (
                <p className="whitespace-pre-wrap break-words text-sm">
                  {message.content}
                </p>
              )}

              {message.role === "assistant" &&
                message.sources &&
                message.sources.length > 0 && (
                  <details className="mt-4 rounded-lg bg-slate-800 p-3">
                    <summary className="cursor-pointer text-sm font-medium">
                      Sources
                    </summary>

                    <ul className="mt-2 list-disc pl-5 text-sm text-slate-300">
                      {message.sources.map((source) => (
                        <li key={source.id}>{source.id}</li>
                      ))}
                    </ul>
                  </details>
                )}
            </div>
          ))}

          {loading && (
            <div className="mr-auto rounded-2xl border border-slate-800 bg-slate-900 px-4 py-3 text-sm text-slate-400">
              <span className="animate-pulse">
                AI is thinking...
              </span>
            </div>
          )}
        </section>

        {error && (
          <div className="mb-4 rounded-xl border border-red-800 bg-red-950/40 p-4 text-sm text-red-300">
            <strong>Error:</strong> {error}
          </div>
        )}

        <form
          onSubmit={handleSubmit}
          className="sticky bottom-0 border-t border-slate-800 bg-slate-950 pt-4"
        >
          <div className="flex gap-2">
            <input
              value={input}
              onChange={(event) => setInput(event.target.value)}
              placeholder="Ask a question..."
              disabled={loading}
              className="min-w-0 flex-1 rounded-xl border border-slate-700 bg-slate-900 px-4 py-3 text-sm outline-none placeholder:text-slate-500 focus:border-blue-500"
            />

            <button
              type="submit"
              disabled={loading || !input.trim()}
              className="rounded-xl bg-blue-600 px-5 py-3 text-sm font-semibold transition hover:bg-blue-500 disabled:cursor-not-allowed disabled:opacity-50"
            >
              Send
            </button>
          </div>
        </form>
      </div>
    </main>
  );
}