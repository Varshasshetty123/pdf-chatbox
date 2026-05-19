from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pdfplumber
import ollama
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


embedding_model = SentenceTransformer("all-MiniLM-L6-v2")


pdf_chunks = []
chunk_embeddings = []

chat_history = []


def extract_text_from_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + "\n"
    return text


def clean_text(text):
    text = text.replace("\n", " ")
    text = " ".join(text.split())
    return text

def split_into_chunks(text, chunk_size=300):
    sentences = text.split(". ")
    chunks = []
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk.split()) + len(sentence.split()) < chunk_size:
            current_chunk += sentence + ". "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    global pdf_chunks, chunk_embeddings

    # extract
    text = extract_text_from_pdf(file.file)

    # clean
    cleaned = clean_text(text)

    # chunk
    pdf_chunks = split_into_chunks(cleaned, chunk_size=300)

    # DEBUG PRINTS GO HERE (ADD HERE)
    print("TOTAL CHUNKS:", len(pdf_chunks))
    print("FIRST CHUNK:", pdf_chunks[0])

    # embeddings
    chunk_embeddings = embedding_model.encode(pdf_chunks)
    chunk_embeddings = np.array(chunk_embeddings)

    return {
        "message": "PDF processed successfully",
        "total_chunks": len(pdf_chunks)
    }


@app.get("/ask")
async def ask(question: str):
    global pdf_chunks, chunk_embeddings

    if len(pdf_chunks) == 0:
        return {"answer": "Please upload a PDF first."}

    # question embedding
    question_embedding = embedding_model.encode([question])
    question_embedding = np.array(question_embedding)

    # similarity
    scores = cosine_similarity(question_embedding, chunk_embeddings)[0]

    # DEBUG (IMPORTANT)
    print("TOP SCORES:", sorted(scores, reverse=True)[:5])

    top_indices = scores.argsort()[-3:][::-1]
    top_score = scores[top_indices[0]]

    # threshold fix
    if top_score < 0.2:
        return {"answer": "Not available in document"}

    # context
    context = "\n\n".join([pdf_chunks[i] for i in top_indices])

    messages = [
        {
            "role": "system",
            "content": "You are a strict document QA assistant. Answer ONLY from context. If not found, say: Not available in document"
        },
        {
            "role": "user",
            "content": f"CONTEXT:\n{context}\n\nQUESTION:\n{question}"
        }
    ]

    response = ollama.chat(
        model="llama3",
        messages=messages
    )

    return {"answer": response["message"]["content"]}