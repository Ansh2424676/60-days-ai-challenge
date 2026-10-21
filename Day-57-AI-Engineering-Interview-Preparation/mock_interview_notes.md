# Day 57 — Mock Interview Notes

## Interview details
Date:
Peer name:
Duration: 30 minutes

## Question 1: RAG system design
My answer summary:
Peer feedback on clarity:
Peer feedback on technical depth:
Trade-offs explained:
One improvement:

## Question 2: Debugging incorrect RAG answers
My answer summary:
Peer feedback on clarity:
Peer feedback on technical depth:
Trade-offs explained:
One improvement:

## Question 3: FAISS vs managed vector database
My answer summary:
Peer feedback on clarity:
Peer feedback on technical depth:
Trade-offs explained:
One improvement:

## Three moments I struggled to explain
1. Topic:
   What I said:
   Clearer version:

2. Topic:
   What I said:
   Clearer version:

3. Topic:
   What I said:
   Clearer version:

## Role swap
Questions I asked my peer:
Feedback I gave my peer:

## Action items
1.
2.
3.

## Step 3 — Three Clearer Interview Answers

### 1. Explain RAG architecture

RAG combines information retrieval with language generation. First, documents are cleaned, chunked, converted into embeddings, and indexed. At query time, the system retrieves relevant passages and supplies them to the LLM as context. The model generates an answer grounded in that context. I would evaluate retrieval quality, answer correctness, and citation accuracy to verify the system.

### 2. Debug incorrect RAG answers

I would reproduce the failure using a fixed evaluation dataset. Then I would determine whether the correct evidence is missing from retrieval or whether the model fails to use evidence that was retrieved. I would inspect document processing, chunking, ranking, metadata filters, and the generation prompt. After testing a targeted fix, I would compare results against the baseline and run regression tests.

### 3. FAISS vs. managed vector database

I would choose FAISS when I need efficient similarity search, greater control, and can manage indexing, persistence, deployment, and scaling myself. I would consider a managed vector database when I need operational support, availability features, access controls, or easier scaling. The decision depends on dataset size, query load, latency, security, budget, and team expertise. I would benchmark both against the actual workload before deciding.

