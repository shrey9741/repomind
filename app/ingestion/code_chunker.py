from typing import List, Dict


# Chunk size settings
MAX_CHUNK_SIZE = 1500   # max characters per chunk
CHUNK_OVERLAP = 100     # overlap between chunks


def chunk_by_functions(content: str, language: str, relative_path: str) -> List[Dict]:
    """
    Split code into chunks. For Python files, split by functions/classes.
    For other files, use character-level splitting.
    """
    if language == "python":
        return _chunk_python(content, relative_path)
    else:
        return _chunk_by_characters(content, relative_path, language)


def _chunk_python(content: str, relative_path: str) -> List[Dict]:
    """Split Python files by function and class definitions."""
    chunks = []
    lines = content.split("\n")
    current_chunk_lines = []
    current_chunk_start = 0
    chunk_type = "module"

    for i, line in enumerate(lines):
        stripped = line.strip()

        # Detect function or class definition
        is_def = stripped.startswith("def ") or stripped.startswith("async def ")
        is_class = stripped.startswith("class ")

        if (is_def or is_class) and current_chunk_lines:
            # Save current chunk before starting new one
            chunk_content = "\n".join(current_chunk_lines).strip()
            if chunk_content:
                chunks.append(_make_chunk(
                    content=chunk_content,
                    relative_path=relative_path,
                    language="python",
                    chunk_type=chunk_type,
                    start_line=current_chunk_start,
                    end_line=i - 1,
                ))
            current_chunk_lines = [line]
            current_chunk_start = i
            chunk_type = "class" if is_class else "function"
        else:
            current_chunk_lines.append(line)

        # If chunk is getting too large, force split
        if len("\n".join(current_chunk_lines)) > MAX_CHUNK_SIZE:
            chunk_content = "\n".join(current_chunk_lines).strip()
            if chunk_content:
                chunks.append(_make_chunk(
                    content=chunk_content,
                    relative_path=relative_path,
                    language="python",
                    chunk_type=chunk_type,
                    start_line=current_chunk_start,
                    end_line=i,
                ))
            current_chunk_lines = []
            current_chunk_start = i + 1
            chunk_type = "module"

    # Don't forget the last chunk
    if current_chunk_lines:
        chunk_content = "\n".join(current_chunk_lines).strip()
        if chunk_content:
            chunks.append(_make_chunk(
                content=chunk_content,
                relative_path=relative_path,
                language="python",
                chunk_type=chunk_type,
                start_line=current_chunk_start,
                end_line=len(lines) - 1,
            ))

    return chunks


def _chunk_by_characters(content: str, relative_path: str, language: str) -> List[Dict]:
    """Generic character-level chunking for non-Python files."""
    chunks = []
    start = 0

    while start < len(content):
        end = start + MAX_CHUNK_SIZE
        chunk_content = content[start:end].strip()

        if chunk_content:
            chunks.append(_make_chunk(
                content=chunk_content,
                relative_path=relative_path,
                language=language,
                chunk_type="block",
                start_line=content[:start].count("\n"),
                end_line=content[:end].count("\n"),
            ))

        start = end - CHUNK_OVERLAP  # overlap for context continuity

    return chunks


def _make_chunk(content, relative_path, language, chunk_type, start_line, end_line) -> Dict:
    """Helper to create a chunk dict."""
    return {
        "content": content,
        "relative_path": relative_path,
        "language": language,
        "chunk_type": chunk_type,
        "start_line": start_line,
        "end_line": end_line,
    }


def chunk_files(files: List[Dict]) -> List[Dict]:
    """
    Process all extracted files and return all chunks.
    """
    all_chunks = []

    for file in files:
        chunks = chunk_by_functions(
            content=file["content"],
            language=file["language"],
            relative_path=file["relative_path"],
        )
        all_chunks.extend(chunks)

    print(f"✅ Created {len(all_chunks)} chunks from {len(files)} files")
    return all_chunks