from typing import List, Dict, Optional
from app.vectorstore.vectordb import search_index


def retrieve(
    query: str,
    repo_name: str,
    k: int = 5,
    language_filter: Optional[str] = None,
    chunk_type_filter: Optional[str] = None,
) -> List[Dict]:
    """
    Retrieve the most relevant code chunks for a given query.

    Args:
        query         : Natural language question
        repo_name     : Name of the indexed repo (e.g. 'flask')
        k             : Number of chunks to retrieve
        language_filter   : Optional - only return chunks of this language (e.g. 'python')
        chunk_type_filter : Optional - only return 'function', 'class', 'module', 'block'

    Returns:
        List of relevant chunk dicts with content + metadata
    """
    # Fetch more than k so we have room to filter
    fetch_k = k * 3 if (language_filter or chunk_type_filter) else k
    results = search_index(query, repo_name, k=fetch_k)

    # Apply filters
    if language_filter:
        results = [r for r in results if r.get("language") == language_filter]

    if chunk_type_filter:
        results = [r for r in results if r.get("chunk_type") == chunk_type_filter]

    # Return top k after filtering
    return results[:k]


def format_context(chunks: List[Dict]) -> str:
    """
    Format retrieved chunks into a clean context string for the LLM.
    Each chunk is labeled with its file path and type.
    """
    if not chunks:
        return "No relevant code found."

    context_parts = []

    for i, chunk in enumerate(chunks, 1):
        header = f"[{i}] File: {chunk['relative_path']} | Type: {chunk['chunk_type']} | Language: {chunk['language']}"
        code_block = f"```{chunk['language']}\n{chunk['content']}\n```"
        context_parts.append(f"{header}\n{code_block}")

    return "\n\n---\n\n".join(context_parts)


def retrieve_and_format(
    query: str,
    repo_name: str,
    k: int = 5,
    language_filter: Optional[str] = None,
    chunk_type_filter: Optional[str] = None,
) -> tuple[List[Dict], str]:
    """
    Convenience function — retrieve chunks AND format them in one call.
    Returns (chunks, formatted_context_string)
    """
    chunks = retrieve(
        query=query,
        repo_name=repo_name,
        k=k,
        language_filter=language_filter,
        chunk_type_filter=chunk_type_filter,
    )
    context = format_context(chunks)
    return chunks, context