export type StreamEvent =
  | { type: "metadata"; request_id?: string; sources?: unknown[] }
  | { type: "token"; content: string }
  | { type: "done"; [key: string]: unknown }
  | { type: "error"; code?: string; message?: string };

export async function readResearchStream(
  response: Response,
  onEvent: (event: StreamEvent) => void,
  signal?: AbortSignal
): Promise<void> {
  if (!response.ok) {
    throw new Error(`HTTP_${response.status}`);
  }

  if (!response.body) {
    throw new Error("STREAM_BODY_MISSING");
  }

  const reader = response.body.getReader();
  const decoder = new TextDecoder();
  let buffer = "";

  try {
    while (true) {
      if (signal?.aborted) {
        await reader.cancel();
        throw new DOMException("Request aborted", "AbortError");
      }

      const { value, done } = await reader.read();

      if (done) break;

      buffer += decoder.decode(value, { stream: true });
      const lines = buffer.split("\n");
      buffer = lines.pop() ?? "";

      for (const line of lines) {
        if (!line.trim()) continue;
        onEvent(JSON.parse(line) as StreamEvent);
      }
    }

    buffer += decoder.decode();

    if (buffer.trim()) {
      onEvent(JSON.parse(buffer) as StreamEvent);
    }
  } finally {
    reader.releaseLock();
  }
}
