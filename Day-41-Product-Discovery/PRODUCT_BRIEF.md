# HireLens AI — Job Application Copilot

## 1. Problem Statement

Users currently manually compare their resume with each job description, identify missing skills, tailor resume content, and prepare application materials, which takes 20–40 minutes per application and can produce inconsistent or generic results. An AI system could reduce this to 5–10 minutes with more consistent, job-specific recommendations by analyzing the resume and job description, identifying skill gaps, generating evidence-based improvement suggestions, and helping prepare tailored application content.

## 2. Target User

HireLens AI is designed for final-year students, fresh graduates, and early-career professionals with 0–3 years of experience who are applying to multiple jobs.

The primary users are candidates targeting roles such as:

- Data Analyst
- Python Developer
- Software Developer
- Data Engineer
- Junior Machine Learning Engineer

These users typically have a resume and job descriptions but struggle to determine exactly how well their profile matches each role and what they should improve before applying.

## 3. Proposed Solution

HireLens AI will compare a candidate's resume with a specific job description and produce an explainable job-application analysis.

The system will:

1. Parse the candidate's resume.
2. Extract important requirements from the job description.
3. Identify matching skills and experience.
4. Identify missing or weak requirements.
5. Map recommendations to evidence found in the resume.
6. Suggest improvements to relevant resume content.
7. Identify interview preparation areas.
8. Clearly distinguish confirmed skills from missing skills.
9. Avoid fabricating experience, qualifications, or achievements.

The product will prioritize truthful, evidence-based recommendations over simply maximizing keyword matches.

## 4. Success Criteria

### Criterion 1 — Requirement Extraction

The system should correctly identify at least 90% of important skills, tools, and qualifications in a manually labelled set of 10 job descriptions.

### Criterion 2 — Resume-Job Analysis

For at least 8 out of 10 evaluation cases, the system should correctly identify the major alignment areas and important gaps between the resume and job description.

### Criterion 3 — Grounded Recommendations

At least 90% of generated recommendations should be supported by information present in either the user's resume or the job description, with zero fabricated work experience or qualifications.

## 5. Representative User Queries

1. Here is my resume and a Data Analyst job description. What are the top five skills I already match and which three important skills are missing?

2. Compare my resume with this Python Developer role and tell me whether my Python, Flask and SQL experience is relevant to the requirements.

3. I'm a fresher with internship experience but no full-time experience. Which parts of this job description can I realistically demonstrate from my resume?

4. The job requires Power BI, SQL and Excel. My resume contains SQL and Power BI but not Excel. Explain this gap without suggesting that I claim Excel experience.

5. Which three resume bullet points should I improve for this Data Analyst position, and why?

6. I have a Credit Card Fraud Detection project and a Power BI sales dashboard. Which project is more relevant to this Data Analyst job description, and what evidence supports that?

7. Extract the important technical keywords from this job description and show which ones are already supported by my resume.

8. Does my current profile have major gaps for this Software Developer role? Separate must-have gaps from nice-to-have gaps.

9. The job description asks for AWS and Docker, but neither appears in my resume. How should I handle these requirements without exaggerating my experience?

10. Based only on my resume and this job description, give me five interview topics I should prepare for and explain why each one is relevant.

## 6. Anti-Patterns the System Must Handle

### Anti-Pattern 1 — Fabricated Experience

The system must not add skills or experience that the candidate does not actually have.

### Anti-Pattern 2 — Guaranteed Outcomes

The system must not claim that a particular resume guarantees an interview or job offer.

### Anti-Pattern 3 — Unsupported Skill Insertion

The system must not recommend falsely adding a skill only because it appears in a job description.

## 7. Competitive Differentiation

### Jobscan

Jobscan compares resumes with job descriptions, identifies missing keywords, calculates a match rate, and performs resume checks.

**HireLens difference:** HireLens focuses on evidence-based skill-gap reasoning and explicitly avoids unsupported experience claims.

### Teal

Teal combines job tracking, job matching, keyword extraction, resume tailoring, application checklists, and related job-search workflows.

**HireLens difference:** HireLens focuses the MVP on deep resume-to-job reasoning and explainable recommendations rather than broad job-search management.

### Rezi

Rezi provides AI resume tailoring, keyword targeting, ATS analysis, job search, interview preparation, and an AI resume agent.

**HireLens difference:** HireLens emphasizes traceable recommendations grounded in evidence from the candidate's actual resume and the target job description.

## 8. Biggest Technical Risk and Mitigation

The biggest technical risk is hallucinated or unsupported recommendations. An LLM may generate recommendations that sound useful but are not supported by the user's resume or the job description. For example, it could incorrectly claim that a candidate has experience with AWS, Docker, Kubernetes, or a particular business domain simply because those terms appear in the job description. This could reduce user trust and encourage inaccurate application claims.

The mitigation strategy will be an evidence-first analysis pipeline. Resume facts and job requirements will be extracted separately before the LLM generates recommendations. Recommendations will be required to reference available evidence, while missing skills will be explicitly labelled as missing instead of being invented. Structured outputs, validation rules, logging, and dedicated evaluation cases for hallucination and unsupported claims will be used to detect failures.

## 9. Required Technical Components

- Next.js frontend
- FastAPI backend
- Resume parser
- Job description parser
- LLM reasoning layer
- Evidence extraction layer
- Skill-gap detection
- Structured JSON outputs
- Recommendation engine
- Evaluation dataset
- Evaluation pipeline
- Error handling
- Logging
- SQLite/PostgreSQL for application data
- Optional FAISS/vector store for future semantic retrieval

## 10. Rough User Flow

Resume Upload
→ Job Description Input
→ Resume Parsing
→ Job Requirement Extraction
→ Skill/Evidence Matching
→ Gap Analysis
→ LLM Reasoning
→ Structured Recommendations
→ Resume Improvement Suggestions
→ Interview Preparation Topics

## 11. Product Principle

HireLens AI should optimize for truthful and useful job-application guidance rather than blindly maximizing ATS keywords.

The system must never encourage a user to claim experience, skills, qualifications, or achievements that are not supported by their actual background.
