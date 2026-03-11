import ollama
from typing import List, Dict, Optional
from app.config import OLLAMA_MODEL, OLLAMA_FALLBACK_MODEL
from app.retrieval.retriever import retrieve_and_format


# ─── System Prompt ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = """You are RepoMind, an expert AI assistant that helps developers understand codebases.

You are given relevant code snippets retrieved from a GitHub repository, along with a user question.
Your job is to:
1. Analyze the provided code context carefully
2. Answer the question clearly and accurately
3. Reference specific files and functions when relevant
4. If the context doesn't contain enough information, say so honestly

Always structure your answers with:
- A direct answer to the question
- Code references (file path + function/class name)
- A brief explanation of how the code works
- Any important notes or caveats

Be concise but thorough. Use markdown formatting for clarity."""


# ─── Core LLM Call ───────────────────────────────────────────────────────────
def call_ollama(prompt: str, model: str = None) -> str:
    """
    Send a prompt to Ollama and return the response.
    Falls back to mistral if deepseek-coder fails.
    """
    model = model or OLLAMA_MODEL

    try:
        response = ollama.chat(
            model=model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ]
        )
        return response["message"]["content"]

    except Exception as e:
        print(f"⚠️ {model} failed: {e}")
        print(f"🔄 Falling back to {OLLAMA_FALLBACK_MODEL}...")

        response = ollama.chat(
            model=OLLAMA_FALLBACK_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user",   "content": prompt},
            ]
        )
        return response["message"]["content"]


# ─── RAG Query ────────────────────────────────────────────────────────────────
def query_repo(
    question: str,
    repo_name: str,
    k: int = 5,
    language_filter: Optional[str] = None,
    chunk_type_filter: Optional[str] = None,
    model: str = None,
) -> Dict:
    """
    Full RAG pipeline:
    1. Retrieve relevant chunks from vector store
    2. Format them as context
    3. Send to LLM with the question
    4. Return answer + sources
    """
    print(f"🔍 Retrieving context for: '{question}'")

    # Step 1 & 2 — Retrieve + Format
    chunks, context = retrieve_and_format(
        query=question,
        repo_name=repo_name,
        k=k,
        language_filter=language_filter,
        chunk_type_filter=chunk_type_filter,
    )

    if not chunks:
        return {
            "answer": "I couldn't find relevant code for your question. Try rephrasing.",
            "sources": [],
            "context": "",
        }

    # Step 3 — Build prompt
    prompt = f"""The user is asking about the '{repo_name}' GitHub repository.

Here are the most relevant code snippets I found:

{context}

---

User Question: {question}

Please answer based on the code context above."""

    # Step 4 — Call LLM
    print(f"🤖 Sending to {model or OLLAMA_MODEL}...")
    answer = call_ollama(prompt, model=model)

    # Step 5 — Return result
    sources = [{
        "file":     c["relative_path"],
        "type":     c["chunk_type"],
        "language": c["language"],
        "score":    c["score"],
        "preview":  c["content"][:150] + "..." if len(c["content"]) > 150 else c["content"],
    } for c in chunks]

    return {
        "answer":  answer,
        "sources": sources,
        "context": context,
    }


# ─── Streaming Version ────────────────────────────────────────────────────────
def query_repo_stream(
    question: str,
    repo_name: str,
    k: int = 5,
    model: str = None,
):
    """
    Streaming version — yields text tokens as LLM generates them.
    Used by Streamlit frontend for live typing effect.
    """
    model = model or OLLAMA_MODEL

    print(f"🔍 Retrieving context for: '{question}'")
    chunks, context = retrieve_and_format(query=question, repo_name=repo_name, k=k)

    if not chunks:
        yield "I couldn't find relevant code for your question."
        return

    prompt = f"""The user is asking about the '{repo_name}' GitHub repository.

Here are the most relevant code snippets I found:

{context}

---

User Question: {question}

Please answer based on the code context above."""

    stream = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user",   "content": prompt},
        ],
        stream=True,
    )

    for chunk in stream:
        token = chunk["message"]["content"]
        if token:
            yield token