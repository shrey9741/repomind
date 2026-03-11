import os
from fastapi import FastAPI, BackgroundTasks, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio

from app.utils.file_utils import (
    get_indexed_repos,
    get_repo_stats,
    extract_repo_name,
    repo_exists_locally,
    index_exists,
)

# ─── App Setup ────────────────────────────────────────────────────────────────
app = FastAPI(
    title="RepoMind API",
    description="Chat with any GitHub repository using AI",
    version="1.0.0",
)

# Allow Streamlit frontend to talk to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Track ingestion status
ingestion_status = {}


# ─── Request Models ───────────────────────────────────────────────────────────
class IngestRequest(BaseModel):
    github_url: str
    force_reclone: bool = False


class ChatRequest(BaseModel):
    question: str
    repo_name: str
    k: int = 5
    language_filter: Optional[str] = None
    use_agent: bool = True


class AnalyzeRequest(BaseModel):
    repo_name: str


# ─── Background Ingestion ─────────────────────────────────────────────────────
def run_ingestion(github_url: str, repo_name: str, force_reclone: bool):
    """Full ingestion pipeline — runs in background."""
    try:
        ingestion_status[repo_name] = {
            "status": "cloning",
            "message": "Cloning repository..."
        }

        from app.ingestion.github_loader import clone_repo
        repo_path = clone_repo(github_url, force_reclone=force_reclone)

        ingestion_status[repo_name] = {
            "status": "extracting",
            "message": "Extracting files..."
        }

        from app.ingestion.file_extractor import extract_files
        files = extract_files(repo_path)

        ingestion_status[repo_name] = {
            "status": "chunking",
            "message": f"Chunking {len(files)} files..."
        }

        from app.ingestion.code_chunker import chunk_files
        chunks = chunk_files(files)

        ingestion_status[repo_name] = {
            "status": "indexing",
            "message": f"Embedding and indexing {len(chunks)} chunks..."
        }

        from app.vectorstore.vectordb import build_index
        build_index(chunks, repo_name)

        ingestion_status[repo_name] = {
            "status": "complete",
            "message": f"Successfully indexed {len(chunks)} chunks from {len(files)} files.",
            "total_files": len(files),
            "total_chunks": len(chunks),
        }

    except Exception as e:
        ingestion_status[repo_name] = {
            "status": "error",
            "message": str(e),
        }


# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/")
def root():
    return {
        "name": "RepoMind API",
        "version": "1.0.0",
        "status": "running",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.post("/ingest")
def ingest_repo(request: IngestRequest, background_tasks: BackgroundTasks):
    """
    Clone and index a GitHub repository.
    Runs in background — use /status/{repo_name} to track progress.
    """
    repo_name = extract_repo_name(request.github_url)

    # If already indexed and not forcing reclone
    if index_exists(repo_name) and not request.force_reclone:
        return {
            "message": f"Repository '{repo_name}' is already indexed.",
            "repo_name": repo_name,
            "status": "already_indexed",
        }

    # Start background ingestion
    ingestion_status[repo_name] = {
        "status": "starting",
        "message": "Starting ingestion pipeline..."
    }

    background_tasks.add_task(
        run_ingestion,
        request.github_url,
        repo_name,
        request.force_reclone,
    )

    return {
        "message": f"Ingestion started for '{repo_name}'",
        "repo_name": repo_name,
        "status": "started",
    }


@app.get("/status/{repo_name}")
def get_ingestion_status(repo_name: str):
    """Check the ingestion status of a repository."""
    if repo_name not in ingestion_status:
        # Check if already indexed
        if index_exists(repo_name):
            return {"status": "complete", "message": "Already indexed."}
        return {"status": "not_started", "message": "Ingestion not started."}

    return ingestion_status[repo_name]


@app.post("/chat")
def chat(request: ChatRequest):
    """
    Chat with an indexed repository.
    Uses agent if use_agent=True, otherwise uses simple RAG.
    """
    if not index_exists(request.repo_name):
        raise HTTPException(
            status_code=404,
            detail=f"Repository '{request.repo_name}' is not indexed. Please ingest it first."
        )

    if request.use_agent:
        from app.agents.agent_controller import run_agent
        answer = run_agent(
            question=request.question,
            repo_name=request.repo_name,
        )
        return {
            "answer": answer,
            "mode": "agent",
            "repo_name": request.repo_name,
        }
    else:
        from app.llm.llm_engine import query_repo
        result = query_repo(
            question=request.question,
            repo_name=request.repo_name,
            k=request.k,
            language_filter=request.language_filter,
        )
        return {
            "answer": result["answer"],
            "sources": result["sources"],
            "mode": "rag",
            "repo_name": request.repo_name,
        }


@app.get("/repos")
def list_repos():
    """List all indexed repositories."""
    repos = get_indexed_repos()
    return {
        "repos": repos,
        "total": len(repos),
    }


@app.get("/repos/{repo_name}")
def get_repo_info(repo_name: str):
    """Get info and stats about a specific repo."""
    if not index_exists(repo_name):
        raise HTTPException(
            status_code=404,
            detail=f"Repository '{repo_name}' not found."
        )
    return get_repo_stats(repo_name)


@app.post("/analyze/structure")
def analyze_structure(request: AnalyzeRequest):
    """Analyze repository folder structure."""
    from app.analysis.repo_structure import analyze_repo_structure, format_repo_summary
    analysis = analyze_repo_structure(request.repo_name)
    return {
        "analysis": analysis,
        "summary": format_repo_summary(analysis),
    }


@app.post("/analyze/dependencies")
def analyze_dependencies(request: AnalyzeRequest):
    """Analyze repository dependency graph."""
    from app.analysis.dependency_graph import build_dependency_graph, format_dependency_summary
    graph = build_dependency_graph(request.repo_name)
    return {
        "graph": graph,
        "summary": format_dependency_summary(graph),
    }


@app.post("/analyze/bugs")
def analyze_bugs(request: AnalyzeRequest):
    """Run AI-powered bug detection on repository."""
    from app.analysis.bug_detector import detect_bugs_in_chunks, format_bug_report
    report = detect_bugs_in_chunks(request.repo_name)
    return {
        "report": report,
        "formatted": format_bug_report(report),
    }