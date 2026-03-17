# 🧠 RepoMind — Chat with Any GitHub Repository

[Live Demo](https://repomind-clbdwmy4qxnmlj2emlqs3d.streamlit.app/)

<div align="center">

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![LangChain](https://img.shields.io/badge/LangChain-0.2-green?style=for-the-badge)
![LangGraph](https://img.shields.io/badge/LangGraph-0.1-orange?style=for-the-badge)
![Streamlit](https://img.shields.io/badge/Streamlit-1.36-red?style=for-the-badge&logo=streamlit)
![FAISS](https://img.shields.io/badge/FAISS-Vector_DB-purple?style=for-the-badge)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.1_8B-yellow?style=for-the-badge)

**An AI-powered Agentic RAG system that lets you chat with any GitHub repository in natural language.**

· [Report Bug](https://github.com/shrey9741/repomind/issues) · [Request Feature](https://github.com/shrey9741/repomind/issues)

</div>

---

## 📌 What is RepoMind?

RepoMind solves a real developer problem: **large codebases are hard to navigate**. Instead of spending hours reading through hundreds of files, you can simply ask:

- *"How does this project handle authentication?"*
- *"Where is the routing logic implemented?"*
- *"What are the main entry points of this application?"*
- *"Are there any potential security vulnerabilities?"*

RepoMind clones any public GitHub repository, indexes it using vector embeddings, and uses an AI agent with multiple tools to answer your questions with source references.

---

## ✨ Key Features

| Feature | Description |
|---------|-------------|
| 💬 **Natural Language Chat** | Ask questions about any codebase in plain English |
| 🤖 **Agentic RAG** | LangGraph agent reasons over multiple tools to answer questions |
| ⚡ **Simple RAG Mode** | Fast vector search + direct LLM answer for quick queries |
| 🔍 **Semantic Code Search** | Finds relevant code by meaning, not just keywords |
| 🏗️ **Repo Structure Analysis** | Visualize folder structure, languages, and entry points |
| 🔗 **Dependency Graph** | Map import relationships between files |
| 🐛 **AI Bug Detection** | LLM-powered static analysis for common issues |
| 🎨 **Custom Dark UI** | Space Grotesk + Fira Code fonts, animated chat bubbles |

---

## 🏗️ Architecture

```
GitHub URL
    ↓
┌─────────────────────────────────────────┐
│           INGESTION PIPELINE            │
│  Clone → Extract → Chunk → Embed → Index│
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│           FAISS VECTOR STORE            │
│     1877+ code chunks as 384-dim vectors│
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│           LANGGRAPH AGENT               │
│  search_codebase → read_file →          │
│  get_repo_structure → search_by_language│
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│     GROQ LLM (LLaMA 3.1 8B Instant)    │
│     Generates answer with sources       │
└─────────────────────────────────────────┘
    ↓
┌─────────────────────────────────────────┐
│         STREAMLIT FRONTEND              │
│    Chat UI with tabs for analysis       │
└─────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

### Backend
- **LangChain** — RAG pipeline and prompt management
- **LangGraph** — Agentic reasoning with tool-calling state machine
- **GitPython** — Repository cloning and management

### AI & ML
- **Groq API** — Fast LLM inference using **LLaMA 3.1 8B Instant**
- **Sentence Transformers** — `all-MiniLM-L6-v2` for code embeddings
- **FAISS** — High-performance vector similarity search

### Frontend
- **Streamlit** — Interactive chat interface with custom dark theme
- **Custom CSS** — Space Grotesk + Fira Code fonts, slide-in animations, animated typing indicator

---

## 📁 Project Structure

```
repomind/
├── app/
│   ├── agents/
│   │   ├── agent_controller.py   # LangGraph agent with tool-calling (Groq)
│   │   └── tools.py              # search_codebase, read_file, get_structure
│   ├── ingestion/
│   │   ├── github_loader.py      # Clone GitHub repositories
│   │   ├── file_extractor.py     # Extract code files by language
│   │   └── code_chunker.py       # Function/class level chunking
│   ├── embeddings/
│   │   └── embedding_model.py    # Sentence Transformer wrapper
│   ├── vectorstore/
│   │   └── vectordb.py           # FAISS operations
│   ├── retrieval/
│   │   └── retriever.py          # Semantic search with filters
│   ├── llm/
│   │   └── llm_engine.py         # Groq LLM + RAG pipeline
│   ├── analysis/
│   │   ├── repo_structure.py     # Folder/language analysis
│   │   ├── dependency_graph.py   # Import relationship mapping
│   │   └── bug_detector.py       # AI-powered code review (Groq)
│   └── config.py                 # API keys and config
├── frontend/
│   └── streamlit_app.py          # Chat UI
├── requirements.txt
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- Git
- [Groq API Key](https://console.groq.com) (free)

### Installation

**1. Clone the repository:**
```bash
git clone https://github.com/shrey9741/repomind.git
cd repomind
```

**2. Create virtual environment:**
```bash
python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # macOS/Linux
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Set up environment variables:**

Create a `.env` file in the root directory:
```env
GROQ_API_KEY=your_groq_api_key_here
EMBEDDING_MODEL=all-MiniLM-L6-v2
VECTOR_DB=faiss
REPOS_DIR=data/repos
VECTOR_DB_DIR=vector_db
```

**5. Set PYTHONPATH (Windows):**
```bash
$env:PYTHONPATH = "D:\repomind"
```

### Running Locally

**Start the Streamlit frontend:**
```bash
streamlit run frontend/streamlit_app.py
```

Visit `http://localhost:8501` to use the app.

---

## 🤖 Agent Tools

The LangGraph agent has access to 5 tools it can call autonomously:

| Tool | Description |
|------|-------------|
| `search_codebase` | Semantic search across all indexed chunks |
| `read_file` | Read complete file contents |
| `get_repo_structure` | Get folder/file tree |
| `search_by_language` | Filter search by programming language |
| `search_functions_only` | Find specific function definitions |

---

## ☁️ Deployment

The app is deployed on **Streamlit Cloud** with **Groq API** for LLM inference.

To deploy your own instance:

1. Fork this repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file path: `frontend/streamlit_app.py`
5. Add secrets in Streamlit Cloud dashboard:
```toml
GROQ_API_KEY = "your_key_here"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
VECTOR_DB = "faiss"
REPOS_DIR = "data/repos"
VECTOR_DB_DIR = "vector_db"
```

---

## 🔮 Future Improvements

- [ ] Support for private repositories via GitHub token
- [ ] Multi-repo comparison and cross-repository search
- [ ] Code generation based on existing codebase patterns
- [ ] PR review automation using repository context
- [ ] ChromaDB persistent storage for cross-session memory
- [ ] Support for more LLM providers (OpenAI, Anthropic)

---

## 🧑‍💻 Author

**Shrey** — 3rd Year BTech IT Student

[![GitHub](https://img.shields.io/badge/GitHub-shrey9741-black?style=flat&logo=github)](https://github.com/shrey9741)

---

## 📄 License

This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.

---

<div align="center">
  <p>If you found this project helpful, please ⭐ star the repository!</p>
</div>
