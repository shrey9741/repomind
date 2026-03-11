import os
import shutil
from git import Repo
from app.config import REPOS_DIR


def get_repo_name(github_url: str) -> str:
    """Extract repo name from GitHub URL."""
    # handles both https://github.com/user/repo and https://github.com/user/repo.git
    name = github_url.rstrip("/").split("/")[-1]
    if name.endswith(".git"):
        name = name[:-4]
    return name


def clone_repo(github_url: str, force_reclone: bool = False) -> str:
    """
    Clone a GitHub repository into data/repos/<repo_name>/
    Returns the local path to the cloned repo.
    """
    repo_name = get_repo_name(github_url)
    repo_path = os.path.join(REPOS_DIR, repo_name)

    # If already cloned
    if os.path.exists(repo_path):
        if force_reclone:
            print(f"🔄 Re-cloning {repo_name}...")
            shutil.rmtree(repo_path)
        else:
            print(f"✅ Repo already exists at {repo_path}, skipping clone.")
            return repo_path

    print(f"📥 Cloning {github_url} into {repo_path}...")
    Repo.clone_from(github_url, repo_path)
    print(f"✅ Successfully cloned {repo_name}")

    return repo_path


def delete_repo(github_url: str):
    """Delete a cloned repository."""
    repo_name = get_repo_name(github_url)
    repo_path = os.path.join(REPOS_DIR, repo_name)

    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
        print(f"🗑️ Deleted {repo_name}")
    else:
        print(f"⚠️ Repo {repo_name} not found locally.")