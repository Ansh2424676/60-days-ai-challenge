# Day 49 — API Error Handling

## Purpose
Explain API failures in plain language and provide a useful recovery action.

## Error Mapping

| Error Code / Status | User Message | Suggested Action |
|---|---|---|
| LLM_TIMEOUT | The AI took too long to respond. | Retry the research request. |
| RETRIEVAL_FAILURE | Research sources could not be retrieved. | Retry; if repeated, check source availability. |
| HTTP 400 | The request is invalid. | Review the research question. |
| HTTP 422 | Required input could not be processed. | Check the request fields. |
| HTTP 429 | Too many requests were sent. | Wait before retrying. |
| HTTP 500 | The server encountered an error. | Retry after a short wait. |
| HTTP 502 | The AI service returned an invalid response. | Retry; check backend logs if repeated. |
| HTTP 503 | The service is temporarily unavailable. | Try again later. |
| HTTP 504 | The request timed out. | Retry the request. |

## Implementation Requirements
- Prefer structured error codes returned by the backend.
- Use HTTP status as a fallback when no structured code is available.
- Do not expose stack traces, secrets, or internal server details.
- Keep the user's research question available for retry.
- Disable duplicate submissions while a request is running.
- Display an accessible error message using role="alert".
- Verify each mapping with a controlled test before marking it complete.

## Verification
- [ ] Structured backend errors are parsed correctly.
- [ ] HTTP errors display the expected message.
- [ ] Retry sends the request again.
- [ ] Errors are accessible to screen readers.
