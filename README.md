# AI PDF Chatbot (Document Q&A System)

## AI Overview

This project is a Retrieval-Augmented Generation (RAG) based AI system that allows users to upload PDF documents and ask questions strictly based on the document content.

The system ensures that responses are grounded only in the uploaded PDF and prevents hallucinations using similarity-based retrieval and strict prompt engineering.


## Objective

To build an AI-powered document Q&A system that:
- Extracts text from PDF files
- Processes and chunks the content
- Converts text into embeddings for semantic search
- Retrieves relevant context using cosine similarity
- Generates answers using an LLM (Ollama - Llama3)
- Ensures responses are strictly based on document content only


### Backend
- FastAPI
- Uvicorn
- pdfplumber
- NumPy

### AI / Machine Learning
- SentenceTransformers (all-MiniLM-L6-v2)
- scikit-learn (Cosine Similarity)
- Ollama (Llama3)

### Frontend
- HTML
- CSS
- JavaScript (Fetch API)


## Architecture

PDF Upload  
→ Text Extraction (pdfplumber)  
→ Text Cleaning  
→ Chunking  
→ Embedding Generation  
→ Cosine Similarity Search  
→ Top-K Relevant Chunks  
→ LLM (Ollama - Llama3)  
→ Final Answer Generation


## AI Approach (RAG System)

This project uses a Retrieval-Augmented Generation pipeline:

- PDF is split into small text chunks
- Each chunk is converted into embeddings
- User question is also converted into embeddings
- Cosine similarity finds most relevant chunks
- Only top matching chunks are passed to the LLM
- LLM generates answer strictly from provided context


## Prompt Design

```text
You are a strict document-based AI assistant.

Answer ONLY using the provided context.

If the answer is not present in the context, respond exactly:
"Not available in document"

Do not use external knowledge.

Context:
{context}

Question:
{question}

```

## Hallucination Handling

To ensure the system does not generate incorrect or fake answers, multiple safety layers are implemented:

- Cosine similarity threshold filtering (0.2–0.3)
  → Ensures only relevant document chunks are used

- Top-K relevant chunk selection
  → Only the most relevant sections of the PDF are sent to the LLM

- Strict system prompt control
  → Forces the AI to answer ONLY from provided context

- Forced fallback response
  → If information is not available, system returns:
  "Not available in document"

- Empty PDF validation
  → Prevents asking questions before uploading a document