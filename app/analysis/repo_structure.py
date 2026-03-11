import os
from typing import Dict, List
from app.config import REPOS_DIR

SKIP_DIRS = {
    ".git", "__pycache__", "node_modules", ".venv",
    "venv", "env", "dist", "build", ".idea", ".vscode"
}

SUPPORTED_EXTENSIONS = {
    ".py": "python", ".js": "javascript", ".ts": "typescript",
    ".java": "java", ".cpp": "cpp", ".c": "c", ".cs": "csharp",
    ".go": "go", ".rb": "ruby", ".rs": "rust", ".md": "markdown",
    ".html": "html", ".css": "css", ".json": "json",
    ".yaml": "yaml", ".yml": "yaml", ".sh": "bash",
}


def analyze_repo_structure(repo_name: str) -> Dict:
    """
    Analyze the repository structure and return a detailed summary.
    """
    repo_path = os.path.join(REPOS_DIR, repo_name)

    if not os.path.exists(repo_path):
        return {"error": f"Repository '{repo_name}' not found."}

    total_files = 0
    total_dirs = 0
    languages = {}
    entry_points = []
    large_files = []
    tree_lines = []

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]

        depth = root.replace(repo_path, "").count(os.sep)
        if depth > 4:
            continue

        indent = "  " * depth
        folder_name = os.path.basename(root)
        tree_lines.append(f"{indent}📁 {folder_name}/")
        total_dirs += 1

        sub_indent = "  " * (depth + 1)
        for filename in files:
            ext = os.path.splitext(filename)[1].lower()
            filepath = os.path.join(root, filename)
            relative = os.path.relpath(filepath, repo_path)

            tree_lines.append(f"{sub_indent}📄 {filename}")
            total_files += 1

            # Track languages
            if ext in SUPPORTED_EXTENSIONS:
                lang = SUPPORTED_EXTENSIONS[ext]
                languages[lang] = languages.get(lang, 0) + 1

            # Detect entry points
            if filename in ["main.py", "app.py", "index.py", "run.py",
                           "server.py", "index.js", "main.js", "manage.py"]:
                entry_points.append(relative)

            # Detect large files
            try:
                size = os.path.getsize(filepath)
                if size > 50000:  # files larger than 50KB
                    large_files.append({
                        "file": relative,
                        "size_kb": round(size / 1024, 1)
                    })
            except Exception:
                pass

    # Sort languages by count
    languages = dict(sorted(languages.items(), key=lambda x: x[1], reverse=True))

    return {
        "repo_name":    repo_name,
        "total_files":  total_files,
        "total_dirs":   total_dirs,
        "languages":    languages,
        "entry_points": entry_points,
        "large_files":  large_files[:5],  # top 5 largest
        "tree":         "\n".join(tree_lines),
    }


def format_repo_summary(analysis: Dict) -> str:
    """Format the analysis result into a readable string."""
    if "error" in analysis:
        return f"❌ {analysis['error']}"

    lines = [
        f"📦 Repository: {analysis['repo_name']}",
        f"📁 Total Directories: {analysis['total_dirs']}",
        f"📄 Total Files: {analysis['total_files']}",
        "",
        "🔤 Languages detected:",
    ]

    for lang, count in analysis["languages"].items():
        lines.append(f"   {lang}: {count} files")

    if analysis["entry_points"]:
        lines.append("\n🚀 Entry Points:")
        for ep in analysis["entry_points"]:
            lines.append(f"   → {ep}")

    if analysis["large_files"]:
        lines.append("\n⚠️ Large Files:")
        for lf in analysis["large_files"]:
            lines.append(f"   → {lf['file']} ({lf['size_kb']} KB)")

    return "\n".join(lines)