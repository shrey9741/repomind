import os
from dotenv import load_dotenv

load_dotenv()

OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-coder")
OLLAMA_FALLBACK_MODEL = os.getenv("OLLAMA_FALLBACK_MODEL", "mistral")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")
VECTOR_DB = os.getenv("VECTOR_DB", "faiss")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REPOS_DIR = os.path.join(BASE_DIR, os.getenv("REPOS_DIR", "data/repos"))
VECTOR_DB_DIR = os.path.join(BASE_DIR, os.getenv("VECTOR_DB_DIR", "vector_db"))

os.makedirs(REPOS_DIR, exist_ok=True)
os.makedirs(VECTOR_DB_DIR, exist_ok=True)

AGENT_MODEL = os.getenv("AGENT_MODEL", "mistral")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")