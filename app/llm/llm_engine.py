from typing import List, Dict, Optional
from langchain_groq import ChatGroq
from app.config import GROQ_API_KEY
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


# ─── Core LLM ─────────────────────────────────────────────────────────────────
def get_llm():
    return ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0.1,
    )


# ─── RAG Query ────────────────────────────────────────────────────────────────
def query_repo(
    question: str,
    repo_name: str,
    k: int = 5,
    language_filter: Optional[str] = None,
    chunk_type_filter: Optional[str] = None,
    model: str = None,
) -> Dict:
    """Full RAG pipeline using Groq."""
    print(f"🔍 Retrieving context for: '{question}'")

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

    prompt = f"""You are RepoMind, an expert AI assistant analyzing the '{repo_name}' GitHub repository.

Here are the most relevant code snippets:

{context}

---

User Question: {question}

Please answer based on the code context above."""

    print(f"🤖 Sending to Groq...")
    llm = get_llm()
    from langchain_core.messages import HumanMessage, SystemMessage
    response = llm.invoke([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessage(content=prompt),
    ])
    answer = response.content

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
    """Streaming version for Streamlit frontend."""
    chunks, context = retrieve_and_format(query=question, repo_name=repo_name, k=k)

    if not chunks:
        yield "I couldn't find relevant code for your question."
        return

    prompt = f"""The user is asking about the '{repo_name}' GitHub repository.

Here are the most relevant code snippets:

{context}

---

User Question: {question}

Please answer based on the code context above."""

    llm = get_llm()
    for chunk in llm.stream(prompt):
        if chunk.content:
            yield chunk.content