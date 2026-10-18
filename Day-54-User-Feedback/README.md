\# Day 54 — Collect and Analyse Real User Feedback



\## Objective

Collect user feedback, analyse ratings and queries, identify recurring problems, and prioritise product improvements.



\## Product description

This AI assistant helps users find answers to their questions. User feedback helps identify unclear answers, inaccurate responses, and areas where the experience can improve.



\## Implementation

\- SQLite feedback storage

\- Query, rating (1–5), optional comment, and timestamp

\- Keyword-based topic clustering

\- Positive-rating percentage

\- Low-rating-based failure proxy

\- Prioritised improvement recommendations



\## Real-world feedback collection

\- Product URL: \[Add your live product URL]

\- People contacted outside the ABTalks community: \[Enter actual count]

\- Feedback collection start/end time: \[Enter actual times]

\- Total genuine responses: \[Enter measured count]

\- Positive rating percentage: \[Enter measured result]



\## Negative feedback interviews

Record two real interviews here. Obtain permission before quoting participants.



1\. Exact quote: \[Add participant's actual words]

2\. Exact quote: \[Add participant's actual words]



\## Findings

Run `python Day-54-User-Feedback/feedback\_analytics.py` to generate the current local analytics.



\## Prioritised improvements

1\. Address the highest observed low-rating topic.

2\. Investigate recurring negative comments.

3\. Re-evaluate quality after implementing fixes.



\## Limitations

Keyword-based topics are approximate. Ratings of 1–2 are treated as a failure proxy, not proof of a technical failure. A complete 24-hour report requires real feedback collected over 24 hours.



\## Submission

\- Repository: \[Add repository URL]

\- LinkedIn post: \[Add post URL]

