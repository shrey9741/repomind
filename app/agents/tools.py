import os
from typing import Optional
from langchain.tools import tool
from app.retrieval.retriever import retrieve, format_context
from app.config import REPOS_DIR


@tool
def search_codebase(query: str, repo_name: str, k: int = 5) -> str:
    """
    Search the codebase semantically for relevant code chunks.
    Use this when the user asks about how something works,
    where something is implemented, or wants to understand code.
    """
    chunks = retrieve(query=query, repo_name=repo_name, k=k)
    if not chunks:
        return "No relevant code found for this query."
    return format_context(chunks)


@tool
def read_file(relative_path: str, repo_name: str) -> str:
    """
    Read the full contents of a specific file in the repository.
    Use this when you need to see the complete file,
    not just a chunk of it.
    """
    file_path = os.path.join(REPOS_DIR, repo_name, relative_path)

    if not os.path.exists(file_path):
        return f"File not found: {relative_path}"

    try:
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        # Limit to 3000 chars to avoid overwhelming the LLM
        if len(content) > 3000:
            content = content[:3000] + "\n\n... [truncated for length]"

        return f"File: {relative_path}\n\n```\n{content}\n```"

    except Exception as e:
        return f"Error reading file: {e}"


@tool
def get_repo_structure(repo_name: str, max_depth: int = 3) -> str:
    """
    Get the folder and file structure of the repository.
    Use this when the user asks about project structure,
    organization, or wants to know what files exist.
    """
    repo_path = os.path.join(REPOS_DIR, repo_name)

    if not os.path.exists(repo_path):
        return f"Repository '{repo_name}' not found locally."

    lines = []
    skip_dirs = {".git", "__pycache__", "node_modules", ".venv", "venv"}

    for root, dirs, files in os.walk(repo_path):
        # Filter skip dirs
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        # Calculate depth
        depth = root.replace(repo_path, "").count(os.sep)
        if depth >= max_depth:
            dirs.clear()
            continue

        indent = "  " * depth
        folder_name = os.path.basename(root)
        lines.append(f"{indent}📁 {folder_name}/")

        sub_indent = "  " * (depth + 1)
        for file in files:
            lines.append(f"{sub_indent}📄 {file}")

    return "\n".join(lines)


@tool
def search_by_language(query: str, repo_name: str, language: str, k: int = 5) -> str:
    """
    Search codebase but only return results from a specific language.
    Use when user specifies they want Python, JavaScript, etc. results.
    Supported: python, javascript, typescript, java, cpp, go, rust
    """
    chunks = retrieve(
        query=query,
        repo_name=repo_name,
        k=k,
        language_filter=language,
    )
    if not chunks:
        return f"No {language} code found for this query."
    return format_context(chunks)


@tool
def search_functions_only(query: str, repo_name: str, k: int = 5) -> str:
    """
    Search codebase and return only function definitions.
    Use when user asks 'what functions handle X' or
    'find the function that does Y'.
    """
    chunks = retrieve(
        query=query,
        repo_name=repo_name,
        k=k,
        chunk_type_filter="function",
    )
    if not chunks:
        return "No matching functions found."
    return format_context(chunks)