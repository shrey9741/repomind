import streamlit as st
import sys
import os
import time

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RepoMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap');

:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #111118;
    --bg-card: #16161f;
    --bg-input: #1c1c28;
    --accent-green: #00ff88;
    --accent-blue: #4488ff;
    --accent-purple: #9966ff;
    --text-primary: #f0f0f8;
    --text-secondary: #8888aa;
    --text-muted: #555570;
    --border: #2a2a3a;
    --border-bright: #3a3a55;
}

html, body, [class*="css"] {
    font-family: 'Syne', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse at 20% 20%, rgba(0,255,136,0.03) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(68,136,255,0.03) 0%, transparent 50%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* ── Sidebar Toggle Fix ── */
[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 0 8px 8px 0 !important;
    color: var(--accent-green) !important;
    position: fixed !important;
    top: 1rem !important;
    left: 0 !important;
    z-index: 999999 !important;
    width: 2rem !important;
    height: 2rem !important;
    align-items: center !important;
    justify-content: center !important;
    cursor: pointer !important;
}

[data-testid="collapsedControl"]:hover {
    border-color: var(--accent-green) !important;
    background: rgba(0,255,136,0.1) !important;
}

[data-testid="collapsedControl"] svg {
    fill: var(--accent-green) !important;
    color: var(--accent-green) !important;
}

.repomind-logo {
    font-family: 'Syne', sans-serif;
    font-weight: 800;
    font-size: 1.8rem;
    letter-spacing: -0.02em;
    background: linear-gradient(135deg, var(--accent-green), var(--accent-blue));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}

.repomind-tagline {
    font-size: 0.75rem;
    color: var(--text-muted);
    letter-spacing: 0.1em;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 1.5rem;
}

.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.5rem;
    margin-top: 1.2rem;
}

.repo-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 0.5rem;
}

.repo-card-name {
    font-weight: 700;
    font-size: 0.9rem;
    color: var(--accent-green);
    font-family: 'JetBrains Mono', monospace;
}

.repo-card-stat {
    font-size: 0.72rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 4px;
}

.msg-user {
    background: linear-gradient(135deg, rgba(68,136,255,0.12), rgba(68,136,255,0.06));
    border: 1px solid rgba(68,136,255,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin: 8px 0;
    margin-left: 3rem;
    font-size: 0.92rem;
    line-height: 1.6;
}

.msg-user::before {
    content: "YOU";
    font-size: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-blue);
    letter-spacing: 0.15em;
    display: block;
    margin-bottom: 6px;
    font-weight: 700;
}

.msg-ai {
    background: linear-gradient(135deg, rgba(0,255,136,0.06), rgba(0,255,136,0.02));
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 16px 16px 16px 4px;
    padding: 14px 18px;
    margin: 8px 0;
    margin-right: 3rem;
    font-size: 0.92rem;
    line-height: 1.6;
    position: relative;
}

.msg-ai::before {
    content: "REPOMIND";
    font-size: 0.6rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-green);
    letter-spacing: 0.15em;
    display: block;
    margin-bottom: 6px;
    font-weight: 700;
}

/* ── Typing animation ── */
@keyframes blink {
    0%, 100% { opacity: 1; }
    50% { opacity: 0; }
}

@keyframes fadeIn {
    from { opacity: 0; transform: translateY(4px); }
    to { opacity: 1; transform: translateY(0); }
}

.msg-ai { animation: fadeIn 0.3s ease-out; }

.typing-indicator {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 14px 18px;
    background: linear-gradient(135deg, rgba(0,255,136,0.06), rgba(0,255,136,0.02));
    border: 1px solid rgba(0,255,136,0.15);
    border-radius: 16px 16px 16px 4px;
    margin: 8px 0;
    margin-right: 3rem;
}

.typing-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    background: var(--accent-green);
    animation: blink 1.2s infinite;
}

.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

.response-time {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.62rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    margin-top: 6px;
    padding: 2px 8px;
    background: rgba(0,0,0,0.2);
    border-radius: 20px;
    border: 1px solid var(--border);
}

.source-chip {
    display: inline-block;
    background: rgba(153,102,255,0.1);
    border: 1px solid rgba(153,102,255,0.25);
    border-radius: 6px;
    padding: 3px 10px;
    font-size: 0.68rem;
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-purple);
    margin: 2px 3px 2px 0;
}

.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 12px 16px;
    text-align: center;
}

.metric-value {
    font-size: 1.4rem;
    font-weight: 800;
    font-family: 'JetBrains Mono', monospace;
    color: var(--accent-green);
}

.metric-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.1em;
    margin-top: 2px;
}

.welcome-container {
    text-align: center;
    padding: 4rem 2rem;
}

.welcome-icon { font-size: 4rem; margin-bottom: 1rem; }

.welcome-title {
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -0.03em;
    margin-bottom: 0.5rem;
}

.welcome-subtitle {
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.85rem;
    margin-bottom: 2rem;
}

.suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 10px;
    max-width: 600px;
    margin: 0 auto;
}

.suggestion-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    text-align: left;
}

.suggestion-icon { font-size: 1.2rem; margin-bottom: 6px; }

.suggestion-text {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* ── Mobile responsiveness ── */
@media (max-width: 768px) {
    .msg-user { margin-left: 0.5rem !important; }
    .msg-ai { margin-right: 0.5rem !important; }
    .welcome-title { font-size: 1.4rem !important; }
    .suggestion-grid { grid-template-columns: 1fr !important; }
    .repomind-logo { font-size: 1.4rem !important; }
    .block-container { padding: 0.5rem !important; }
    .metric-card { padding: 8px 10px !important; }
    .metric-value { font-size: 1.1rem !important; }

    /* Mobile sidebar toggle always visible */
    [data-testid="collapsedControl"] {
        display: flex !important;
        position: fixed !important;
        top: 0.5rem !important;
        left: 0 !important;
        z-index: 999999 !important;
    }
}

.stTextInput input, .stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
}

.stTextInput input:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.1) !important;
}

/* ── All buttons default ── */
.stButton button {
    background: var(--bg-card) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.82rem !important;
    width: 100% !important;
    transition: all 0.2s !important;
    text-align: left !important;
}

.stButton button:hover {
    border-color: var(--accent-green) !important;
    color: var(--text-primary) !important;
    background: rgba(0,255,136,0.05) !important;
}

/* ── Sidebar buttons ── */
[data-testid="stSidebar"] .stButton button {
    background: var(--bg-card) !important;
    color: var(--accent-blue) !important;
    border: 1px solid rgba(68,136,255,0.3) !important;
    font-weight: 600 !important;
    text-align: center !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    background: rgba(68,136,255,0.1) !important;
    border-color: var(--accent-blue) !important;
    color: var(--text-primary) !important;
    transform: translateY(-1px) !important;
}

/* ── Send button ── */
div[data-testid="column"]:last-child .stButton button {
    background: linear-gradient(135deg, var(--accent-green), #00cc6a) !important;
    color: #0a0a0f !important;
    border: none !important;
    font-weight: 700 !important;
    text-align: center !important;
}

hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,255,136,0.1) !important;
    color: var(--accent-green) !important;
}

::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-bright); border-radius: 2px; }
</style>
""", unsafe_allow_html=True)


# ─── Core Functions ───────────────────────────────────────────────────────────
@st.cache_resource
def get_embedding_model():
    from sentence_transformers import SentenceTransformer
    return SentenceTransformer("all-MiniLM-L6-v2")


def ingest_repo_direct(github_url: str, force: bool = False):
    from app.ingestion.github_loader import clone_repo, get_repo_name
    from app.ingestion.file_extractor import extract_files
    from app.ingestion.code_chunker import chunk_files
    from app.vectorstore.vectordb import build_index
    from app.utils.file_utils import index_exists

    repo_name = get_repo_name(github_url)

    if index_exists(repo_name) and not force:
        yield {"status": "already_indexed", "repo_name": repo_name}
        return

    yield {"status": "cloning", "message": f"Cloning {repo_name}..."}
    repo_path = clone_repo(github_url, force_reclone=force)

    yield {"status": "extracting", "message": "Extracting files..."}
    files = extract_files(repo_path)

    yield {"status": "chunking", "message": f"Chunking {len(files)} files..."}
    chunks = chunk_files(files)

    yield {"status": "indexing", "message": f"Indexing {len(chunks)} chunks..."}
    build_index(chunks, repo_name)

    yield {
        "status": "complete",
        "repo_name": repo_name,
        "message": f"Done! {len(chunks)} chunks from {len(files)} files indexed.",
        "total_chunks": len(chunks),
        "total_files": len(files),
    }


def chat_direct(question: str, repo_name: str, use_agent: bool = True):
    try:
        if use_agent:
            try:
                from app.agents.agent_controller import run_agent
                answer = run_agent(question=question, repo_name=repo_name)
                return {"answer": answer, "sources": [], "mode": "agent"}
            except Exception as agent_error:
                print(f"⚠️ Agent failed: {agent_error}, falling back to RAG...")
                from app.llm.llm_engine import query_repo
                result = query_repo(question=question, repo_name=repo_name, k=5)
                return result
        else:
            from app.llm.llm_engine import query_repo
            result = query_repo(question=question, repo_name=repo_name, k=5)
            return result
    except Exception as e:
        return {
            "answer": f"⚠️ Something went wrong: {str(e)}\n\nPlease try rephrasing your question or try again.",
            "sources": [],
            "mode": "error",
        }


def get_indexed_repos_direct():
    from app.utils.file_utils import get_indexed_repos
    return get_indexed_repos()


def get_repo_stats_direct(repo_name: str):
    from app.utils.file_utils import get_repo_stats
    return get_repo_stats(repo_name)


def analyze_structure_direct(repo_name: str):
    from app.analysis.repo_structure import analyze_repo_structure, format_repo_summary
    analysis = analyze_repo_structure(repo_name)
    return {"analysis": analysis, "summary": format_repo_summary(analysis)}


def analyze_deps_direct(repo_name: str):
    from app.analysis.dependency_graph import build_dependency_graph, format_dependency_summary
    graph = build_dependency_graph(repo_name)
    return {"graph": graph, "summary": format_dependency_summary(graph)}


def analyze_bugs_direct(repo_name: str):
    from app.analysis.bug_detector import detect_bugs_in_chunks, format_bug_report
    report = detect_bugs_in_chunks(repo_name)
    return {"report": report, "formatted": format_bug_report(report)}


# ─── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_repo" not in st.session_state:
    st.session_state.selected_repo = None
if "use_agent" not in st.session_state:
    st.session_state.use_agent = True


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="repomind-logo">RepoMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="repomind-tagline">AI · Code Intelligence</div>', unsafe_allow_html=True)
    st.markdown("---")

    st.markdown('<div class="section-label">Add Repository</div>', unsafe_allow_html=True)
    github_url = st.text_input(
        "GitHub URL",
        placeholder="https://github.com/user/repo",
        label_visibility="collapsed",
    )

    col1, col2 = st.columns([3, 1])
    with col1:
        ingest_btn = st.button("⚡ Ingest Repo", use_container_width=True)
    with col2:
        force_reclone = st.checkbox("↺", help="Force re-clone")

    if ingest_btn and github_url:
        progress = st.progress(0)
        status_text = st.empty()
        stage_map = {
            "cloning": 20, "extracting": 40,
            "chunking": 60, "indexing": 80, "complete": 100
        }

        for update in ingest_repo_direct(github_url, force=force_reclone):
            status = update.get("status", "")
            msg = update.get("message", "")
            progress.progress(stage_map.get(status, 10))
            status_text.markdown(
                f'<div class="section-label">{msg}</div>',
                unsafe_allow_html=True
            )
            if status == "complete":
                st.success(f"✅ {msg}")
                st.rerun()
            elif status == "already_indexed":
                st.success("✅ Already indexed!")
                st.rerun()

    st.markdown("---")

    st.markdown('<div class="section-label">Indexed Repositories</div>', unsafe_allow_html=True)
    repos = get_indexed_repos_direct()

    if not repos:
        st.markdown(
            '<div style="color:#555570;font-size:0.8rem;font-family:JetBrains Mono,monospace;">No repos indexed yet</div>',
            unsafe_allow_html=True
        )
    else:
        for repo in repos:
            stats = get_repo_stats_direct(repo)
            chunks = stats.get("total_chunks", "?")
            is_selected = st.session_state.selected_repo == repo
            border_color = "#00ff88" if is_selected else "#2a2a3a"

            st.markdown(f"""
            <div class="repo-card" style="border-color:{border_color};">
                <div class="repo-card-name">📦 {repo}</div>
                <div class="repo-card-stat">{chunks} chunks indexed</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Select {repo}", key=f"sel_{repo}", use_container_width=True):
                st.session_state.selected_repo = repo
                st.session_state.messages = []
                st.rerun()

    st.markdown("---")

    st.markdown('<div class="section-label">Settings</div>', unsafe_allow_html=True)
    st.session_state.use_agent = st.toggle(
        "🤖 Agentic Mode",
        value=st.session_state.use_agent,
        help="Agent uses tools to reason. Disable for faster simple RAG."
    )


# ─── Main Content ─────────────────────────────────────────────────────────────
selected = st.session_state.selected_repo

if selected is None:
    st.markdown("""
    <div class="welcome-container">
        <div class="welcome-icon">🧠</div>
        <div class="welcome-title">Chat with any codebase</div>
        <div class="welcome-subtitle">← Select or ingest a repository to get started</div>
        <div class="suggestion-grid">
            <div class="suggestion-card">
                <div class="suggestion-icon">🏗️</div>
                <div class="suggestion-text">Understand project architecture and folder structure</div>
            </div>
            <div class="suggestion-card">
                <div class="suggestion-icon">🔍</div>
                <div class="suggestion-text">Find where specific functionality is implemented</div>
            </div>
            <div class="suggestion-card">
                <div class="suggestion-icon">🐛</div>
                <div class="suggestion-text">Detect potential bugs and security issues</div>
            </div>
            <div class="suggestion-card">
                <div class="suggestion-icon">📖</div>
                <div class="suggestion-text">Generate documentation for any module</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    stats = get_repo_stats_direct(selected)
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

    with col1:
        st.markdown(f"""
        <div style="border-bottom:1px solid var(--border);padding-bottom:1rem;margin-bottom:1.5rem;">
            <div style="font-size:1.5rem;font-weight:800;letter-spacing:-0.02em;">📦 {selected}</div>
            <div style="font-size:0.8rem;color:var(--text-muted);font-family:JetBrains Mono,monospace;">
                {'🤖 Agentic RAG' if st.session_state.use_agent else '⚡ Simple RAG'} · Ask anything about this repository
            </div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{stats.get("total_chunks","?")}</div><div class="metric-label">Chunks</div></div>', unsafe_allow_html=True)
    with col3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{"✅" if stats.get("indexed") else "❌"}</div><div class="metric-label">Indexed</div></div>', unsafe_allow_html=True)
    with col4:
        if st.button("🗑️ Clear"):
            st.session_state.messages = []
            st.rerun()

    tab1, tab2, tab3, tab4 = st.tabs(["💬 CHAT", "🏗️ STRUCTURE", "🔗 DEPENDENCIES", "🐛 BUG SCAN"])

    # ── Chat Tab ──
    with tab1:
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                response_time = msg.get("response_time", None)
                time_badge = f'<div class="response-time">⚡ {response_time:.1f}s</div>' if response_time else ""
                st.markdown(f'<div class="msg-ai">{msg["content"]}{time_badge}</div>', unsafe_allow_html=True)
                if msg.get("sources"):
                    chips = "".join([
                        f'<span class="source-chip">📄 {s["file"]}</span>'
                        for s in msg["sources"][:5]
                    ])
                    st.markdown(chips, unsafe_allow_html=True)

        if not st.session_state.messages:
            st.markdown('<div class="section-label" style="margin-top:1rem">Suggested Questions</div>', unsafe_allow_html=True)
            suggestions = [
                f"What is the overall architecture of {selected}?",
                f"How does {selected} handle error handling?",
                f"What are the main entry points of {selected}?",
                f"Explain the folder structure of {selected}",
            ]
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                        st.session_state.messages.append({"role": "user", "content": suggestion})

                        typing_placeholder = st.empty()
                        typing_placeholder.markdown("""
                        <div class="typing-indicator">
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                        </div>
                        """, unsafe_allow_html=True)

                        start_time = time.time()
                        result = chat_direct(suggestion, selected, st.session_state.use_agent)
                        elapsed = time.time() - start_time

                        typing_placeholder.empty()
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result.get("answer", "No answer"),
                            "sources": result.get("sources", []),
                            "response_time": elapsed,
                        })
                        st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)
        input_col, btn_col = st.columns([6, 1])
        with input_col:
            question = st.text_input(
                "Ask anything",
                placeholder=f"Ask anything about {selected}...",
                label_visibility="collapsed",
                key="chat_input",
            )
        with btn_col:
            send = st.button("Send →", use_container_width=True)

        if send and question:
            st.session_state.messages.append({"role": "user", "content": question})

            typing_placeholder = st.empty()
            typing_placeholder.markdown("""
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
            """, unsafe_allow_html=True)

            start_time = time.time()
            result = chat_direct(question, selected, st.session_state.use_agent)
            elapsed = time.time() - start_time

            typing_placeholder.empty()
            st.session_state.messages.append({
                "role": "assistant",
                "content": result.get("answer", "No answer"),
                "sources": result.get("sources", []),
                "response_time": elapsed,
            })
            st.rerun()

    # ── Structure Tab ──
    with tab2:
        if st.button("🔍 Analyze Structure", use_container_width=True):
            with st.spinner("Analyzing..."):
                result = analyze_structure_direct(selected)
            analysis = result.get("analysis", {})
            m1, m2, m3 = st.columns(3)
            with m1:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{analysis.get("total_files",0)}</div><div class="metric-label">Files</div></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{analysis.get("total_dirs",0)}</div><div class="metric-label">Dirs</div></div>', unsafe_allow_html=True)
            with m3:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{len(analysis.get("languages",{}))}</div><div class="metric-label">Languages</div></div>', unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)
            col_a, col_b = st.columns(2)
            with col_a:
                st.markdown('<div class="section-label">Languages</div>', unsafe_allow_html=True)
                for lang, count in analysis.get("languages", {}).items():
                    st.markdown(f'<span class="source-chip">🔤 {lang}: {count}</span>', unsafe_allow_html=True)
                if analysis.get("entry_points"):
                    st.markdown('<div class="section-label" style="margin-top:1rem">Entry Points</div>', unsafe_allow_html=True)
                    for ep in analysis["entry_points"]:
                        st.markdown(f'<span class="source-chip">🚀 {ep}</span>', unsafe_allow_html=True)
            with col_b:
                if analysis.get("large_files"):
                    st.markdown('<div class="section-label">Large Files</div>', unsafe_allow_html=True)
                    for lf in analysis["large_files"]:
                        st.markdown(f'<span class="source-chip">⚠️ {lf["file"]} ({lf["size_kb"]}KB)</span>', unsafe_allow_html=True)
            st.code(analysis.get("tree", ""), language=None)

    # ── Dependencies Tab ──
    with tab3:
        if st.button("🔗 Analyze Dependencies", use_container_width=True):
            with st.spinner("Building graph..."):
                result = analyze_deps_direct(selected)
            graph = result.get("graph", {})
            m1, m2 = st.columns(2)
            with m1:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{graph.get("total_files",0)}</div><div class="metric-label">Files</div></div>', unsafe_allow_html=True)
            with m2:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{graph.get("total_deps",0)}</div><div class="metric-label">Dependencies</div></div>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown('<div class="section-label">Most Imported Modules</div>', unsafe_allow_html=True)
            for module, count in graph.get("top_imports", []):
                bar_width = min(100, int(count * 3))
                st.markdown(f"""
                <div style="margin-bottom:8px;">
                    <div style="display:flex;justify-content:space-between;margin-bottom:3px;">
                        <span style="font-family:JetBrains Mono,monospace;font-size:0.8rem;color:#f0f0f8;">{module}</span>
                        <span style="font-family:JetBrains Mono,monospace;font-size:0.75rem;color:#555570;">{count}x</span>
                    </div>
                    <div style="background:#1c1c28;border-radius:4px;height:6px;overflow:hidden;">
                        <div style="background:linear-gradient(90deg,#00ff88,#4488ff);width:{bar_width}%;height:100%;border-radius:4px;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Bug Scan Tab ──
    with tab4:
        st.markdown(
            '<div style="color:#8888aa;font-size:0.82rem;font-family:JetBrains Mono,monospace;margin-bottom:1rem;">AI-powered static analysis using LLM reasoning</div>',
            unsafe_allow_html=True
        )
        if st.button("🐛 Run Bug Scan", use_container_width=True):
            with st.spinner("🔍 Scanning for bugs..."):
                result = analyze_bugs_direct(selected)
            report = result.get("report", {})
            st.markdown(
                f'<div class="metric-card" style="margin-bottom:1rem;"><div class="metric-value">{report.get("files_analyzed",0)}</div><div class="metric-label">Files Scanned</div></div>',
                unsafe_allow_html=True
            )
            st.markdown(
                f'<div class="msg-ai">{report.get("findings","No findings")}</div>',
                unsafe_allow_html=True
            )