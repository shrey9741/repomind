import os
import re
import json
from typing import Dict, List
from app.config import REPOS_DIR


def extract_python_imports(content: str) -> List[str]:
    """Extract all import statements from Python file."""
    imports = []

    # Match: import x, from x import y
    patterns = [
        r"^import\s+([\w.]+)",
        r"^from\s+([\w.]+)\s+import",
    ]

    for line in content.split("\n"):
        line = line.strip()
        for pattern in patterns:
            match = re.match(pattern, line)
            if match:
                imports.append(match.group(1))

    return imports


def extract_js_imports(content: str) -> List[str]:
    """Extract all import statements from JS/TS files."""
    imports = []

    patterns = [
        r'import\s+.*?\s+from\s+["\'](.+?)["\']',
        r'require\(["\'](.+?)["\']\)',
    ]

    for pattern in patterns:
        matches = re.findall(pattern, content)
        imports.extend(matches)

    return imports


def build_dependency_graph(repo_name: str) -> Dict:
    """
    Build a dependency graph showing which files import which.
    Returns a dict with nodes and edges.
    """
    repo_path = os.path.join(REPOS_DIR, repo_name)

    if not os.path.exists(repo_path):
        return {"error": f"Repository '{repo_name}' not found."}

    nodes = []
    edges = []
    skip_dirs = {".git", "__pycache__", "node_modules", "venv", ".venv"}

    for root, dirs, files in os.walk(repo_path):
        dirs[:] = [d for d in dirs if d not in skip_dirs]

        for filename in files:
            filepath = os.path.join(root, filename)
            relative = os.path.relpath(filepath, repo_path)
            ext = os.path.splitext(filename)[1].lower()

            if ext not in [".py", ".js", ".ts"]:
                continue

            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
            except Exception:
                continue

            # Add as node
            nodes.append(relative)

            # Extract imports
            if ext == ".py":
                imports = extract_python_imports(content)
            else:
                imports = extract_js_imports(content)

            # Add edges for local imports only
            for imp in imports:
                imp_clean = imp.replace(".", os.sep)
                edges.append({
                    "from": relative,
                    "imports": imp,
                })

    # Find most imported modules
    import_counts = {}
    for edge in edges:
        imp = edge["imports"]
        import_counts[imp] = import_counts.get(imp, 0) + 1

    top_imports = sorted(import_counts.items(), key=lambda x: x[1], reverse=True)[:10]

    return {
        "repo_name":   repo_name,
        "total_files": len(nodes),
        "total_deps":  len(edges),
        "top_imports": top_imports,
        "edges":       edges[:50],  # limit for readability
    }


def format_dependency_summary(graph: Dict) -> str:
    """Format dependency graph into readable summary."""
    if "error" in graph:
        return f"❌ {graph['error']}"

    lines = [
        f"🔗 Dependency Graph: {graph['repo_name']}",
        f"📄 Files analyzed: {graph['total_files']}",
        f"🔀 Total dependencies: {graph['total_deps']}",
        "",
        "📊 Most imported modules:",
    ]

    for module, count in graph["top_imports"]:
        lines.append(f"   {module}: imported {count} times")

    return "\n".join(lines)