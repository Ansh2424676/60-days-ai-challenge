\# Day 18 — Hallucination Evaluation Criteria



\## Classification



\### 1. Correct

Response ground truth ke fact se match karta hai.

Minor wording differences allowed hain.



\### 2. Partially Correct

Response mein main fact sahi hai, lekin:

\- incomplete information hai

\- unnecessary incorrect detail hai

\- answer partially matches ground truth



\### 3. Hallucinated

Response ground truth se factually wrong hai, ya model ne unsupported/fabricated information confidently provide ki hai.



\## Hallucination Categories



\### 1. fabricated\_specific\_fact

Model ne koi specific fact, number, name, date, location ya statistic invent kiya.



\### 2. outdated\_information

Model ne purani information ko current information ke roop mein present kiya.



\### 3. confident\_wrong\_answer

Model ne confidently factually incorrect answer diya.



\### 4. plausible\_unverifiable\_claim

Answer believable lagta hai, lekin provided evidence/ground truth se verify nahi hota.



\## Scoring Rule



Har response ko exactly ek classification diya jayega:



\- correct

\- partially\_correct

\- hallucinated



Agar classification `hallucinated` hai, to ek hallucination category assign ki jayegi.

