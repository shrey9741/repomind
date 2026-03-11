import os
from typing import List, Dict

# File extensions we want to process
SUPPORTED_EXTENSIONS = {
    ".py": "python",
    ".js": "javascript",
    ".ts": "typescript",
    ".java": "java",
    ".cpp": "cpp",
    ".c": "c",
    ".cs": "csharp",
    ".go": "go",
    ".rb": "ruby",
    ".rs": "rust",
    ".md": "markdown",
    ".txt": "text",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".yaml": "yaml",
    ".yml": "yaml",
    ".sh": "bash",
}

# Folders to skip
SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv", "venv",
    "env", ".env", "dist", "build", ".idea", ".vscode",
    "*.egg-info", ".mypy_cache", ".pytest_cache"
}


def extract_files(repo_path: str) -> List[Dict]:
    """
    Walk through the repo and extract all supported code files.
    Returns a list of dicts with file info and content.
    """
    extracted = []

    for root, dirs, files in os.walk(repo_path):
        # Remove skip dirs in-place so os.walk doesn't go into them
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        for filename in files:
            ext = os.path.splitext(filename)[1].lower()

            if ext not in SUPPORTED_EXTENSIONS:
                continue

            filepath = os.path.join(root, filename)
            relative_path = os.path.relpath(filepath, repo_path)

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()

                # Skip empty files
                if not content.strip():
                    continue

                extracted.append({
                    "filepath": filepath,
                    "relative_path": relative_path,
                    "filename": filename,
                    "language": SUPPORTED_EXTENSIONS[ext],
                    "content": content,
                    "size": len(content),
                })

            except Exception as e:
                print(f"⚠️ Could not read {filepath}: {e}")
                continue

    print(f"✅ Extracted {len(extracted)} files from {repo_path}")
    return extracted


def get_repo_summary(files: List[Dict]) -> Dict:
    """Generate a quick summary of extracted files."""
    languages = {}
    for f in files:
        lang = f["language"]
        languages[lang] = languages.get(lang, 0) + 1

    return {
        "total_files": len(files),
        "languages": languages,
        "total_size_chars": sum(f["size"] for f in files),
    }