from typing import Dict, List
from app.retrieval.retriever import retrieve
from app.config import GROQ_API_KEY
from langchain_groq import ChatGroq


# Common bug patterns to check
BUG_PATTERNS = [
    "bare except clauses that catch all exceptions",
    "hardcoded passwords or API keys or secrets",
    "missing null or None checks before accessing attributes",
    "unused imports or variables",
    "infinite loops or missing loop termination conditions",
    "SQL queries built with string concatenation",
    "missing error handling in file operations",
    "deprecated function usage",
]


def detect_bugs_in_chunks(repo_name: str, k: int = 8) -> Dict:
    """
    Use AI to detect potential bugs in the most relevant code chunks.
    """
    llm = ChatGroq(
        model="llama-3.1-8b-instant",
        api_key=GROQ_API_KEY,
        temperature=0.1,
    )

    # Search for potentially problematic code patterns
    all_chunks = []
    search_queries = [
        "exception handling try except",
        "database query sql",
        "file open read write",
        "password secret key token",
        "loop iteration",
    ]

    for query in search_queries:
        chunks = retrieve(query=query, repo_name=repo_name, k=2)
        all_chunks.extend(chunks)

    if not all_chunks:
        return {"error": "No code chunks found to analyze."}

    # Deduplicate chunks
    seen = set()
    unique_chunks = []
    for chunk in all_chunks:
        key = chunk["relative_path"] + str(chunk.get("start_line", 0))
        if key not in seen:
            seen.add(key)
            unique_chunks.append(chunk)

    # Build context for LLM
    code_context = "\n\n---\n\n".join([
        f"File: {c['relative_path']}\n```{c['language']}\n{c['content'][:500]}\n```"
        for c in unique_chunks[:8]
    ])

    prompt = f"""You are a code review expert. Analyze the following code snippets from the '{repo_name}' repository and identify potential bugs, security issues, or code quality problems.

Look specifically for:
{chr(10).join(f"- {p}" for p in BUG_PATTERNS)}

Code to analyze:
{code_context}

For each issue found, provide:
1. File name and location
2. Type of issue
3. Why it's a problem
4. Suggested fix

If the code looks clean, say so. Be specific and concise."""

    response = llm.invoke(prompt)

    return {
        "repo_name":      repo_name,
        "files_analyzed": len(unique_chunks),
        "findings":       response.content,
    }


def format_bug_report(report: Dict) -> str:
    """Format bug detection results."""
    if "error" in report:
        return f"❌ {report['error']}"

    return f"""🐛 Bug Detection Report: {report['repo_name']}
📄 Files analyzed: {report['files_analyzed']}

{report['findings']}"""