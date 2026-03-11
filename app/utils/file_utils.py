import os
import json
from typing import Dict, List
from app.config import REPOS_DIR, VECTOR_DB_DIR


def repo_exists_locally(repo_name: str) -> bool:
    """Check if a repo has been cloned locally."""
    return os.path.exists(os.path.join(REPOS_DIR, repo_name))


def index_exists(repo_name: str) -> bool:
    """Check if a FAISS index exists for a repo."""
    index_path = os.path.join(VECTOR_DB_DIR, repo_name, "index.faiss")
    return os.path.exists(index_path)


def get_indexed_repos() -> List[str]:
    """Return list of all repos that have been indexed."""
    if not os.path.exists(VECTOR_DB_DIR):
        return []
    return [
        d for d in os.listdir(VECTOR_DB_DIR)
        if os.path.isdir(os.path.join(VECTOR_DB_DIR, d))
    ]


def extract_repo_name(github_url: str) -> str:
    """Extract repo name from GitHub URL."""
    name = github_url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return name


def get_repo_stats(repo_name: str) -> Dict:
    """Get basic stats about an indexed repo."""
    stats = {
        "repo_name": repo_name,
        "cloned": repo_exists_locally(repo_name),
        "indexed": index_exists(repo_name),
    }

    # Get chunk count from metadata file
    metadata_path = os.path.join(VECTOR_DB_DIR, repo_name, "metadata.json")
    if os.path.exists(metadata_path):
        with open(metadata_path, "r") as f:
            metadata = json.load(f)
        stats["total_chunks"] = len(metadata)

    return stats