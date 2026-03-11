import streamlit as st
import requests
import time

# ─── Page Config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="RepoMind",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = "http://localhost:8000"

# ─── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;600;700&family=Syne:wght@400;600;700;800&display=swap');

/* ── Root Variables ── */
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

/* ── Global ── */
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

/* ── Hide Streamlit Branding ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1rem !important; }

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border) !important;
}

[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Logo ── */
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

/* ── Section Headers ── */
.section-label {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-bottom: 0.5rem;
    margin-top: 1.2rem;
}

/* ── Status Badge ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 0.72rem;
    font-family: 'JetBrains Mono', monospace;
    font-weight: 600;
    letter-spacing: 0.05em;
}

.status-online {
    background: rgba(0,255,136,0.1);
    border: 1px solid rgba(0,255,136,0.3);
    color: var(--accent-green);
}

.status-offline {
    background: rgba(255,80,80,0.1);
    border: 1px solid rgba(255,80,80,0.3);
    color: #ff5050;
}

.status-dot {
    width: 6px;
    height: 6px;
    border-radius: 50%;
    display: inline-block;
}

.dot-online { background: var(--accent-green); }
.dot-offline { background: #ff5050; }

/* ── Repo Card ── */
.repo-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 14px 16px;
    margin-bottom: 0.5rem;
    transition: border-color 0.2s;
}

.repo-card:hover {
    border-color: var(--border-bright);
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

/* ── Chat Area ── */
.chat-header {
    border-bottom: 1px solid var(--border);
    padding-bottom: 1rem;
    margin-bottom: 1.5rem;
}

.chat-title {
    font-size: 1.5rem;
    font-weight: 800;
    letter-spacing: -0.02em;
    color: var(--text-primary);
}

.chat-subtitle {
    font-size: 0.8rem;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 2px;
}

/* ── Messages ── */
.msg-user {
    background: linear-gradient(135deg, rgba(68,136,255,0.12), rgba(68,136,255,0.06));
    border: 1px solid rgba(68,136,255,0.2);
    border-radius: 16px 16px 4px 16px;
    padding: 14px 18px;
    margin: 8px 0;
    margin-left: 3rem;
    font-size: 0.92rem;
    line-height: 1.6;
    position: relative;
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

/* ── Sources ── */
.sources-header {
    font-size: 0.65rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    margin-top: 12px;
    margin-bottom: 6px;
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

/* ── Input Area ── */
.stTextInput input, .stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.88rem !important;
    transition: border-color 0.2s !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 2px rgba(0,255,136,0.1) !important;
}

/* ── Buttons ── */
.stButton button {
    background: linear-gradient(135deg, var(--accent-green), #00cc6a) !important;
    color: #0a0a0f !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.02em !important;
    padding: 0.5rem 1.5rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}

.stButton button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0,255,136,0.25) !important;
}

/* ── Select box ── */
.stSelectbox select, [data-baseweb="select"] {
    background: var(--bg-input) !important;
    border-color: var(--border) !important;
    color: var(--text-primary) !important;
    border-radius: 10px !important;
}

/* ── Metrics ── */
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

/* ── Welcome Screen ── */
.welcome-container {
    text-align: center;
    padding: 4rem 2rem;
}

.welcome-icon {
    font-size: 4rem;
    margin-bottom: 1rem;
}

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
    cursor: pointer;
    transition: all 0.2s;
}

.suggestion-card:hover {
    border-color: var(--accent-green);
    background: rgba(0,255,136,0.03);
}

.suggestion-icon { font-size: 1.2rem; margin-bottom: 6px; }
.suggestion-text {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

/* ── Progress ── */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent-green), var(--accent-blue)) !important;
    border-radius: 10px !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent-green) !important;
}

/* ── Divider ── */
hr {
    border-color: var(--border) !important;
    margin: 1rem 0 !important;
}

/* ── Analysis Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 10px !important;
    padding: 4px !important;
    gap: 4px !important;
    border: 1px solid var(--border) !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 8px !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 0.75rem !important;
    letter-spacing: 0.05em !important;
}

.stTabs [aria-selected="true"] {
    background: rgba(0,255,136,0.1) !important;
    color: var(--accent-green) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--border-bright);
    border-radius: 2px;
}
</style>
""", unsafe_allow_html=True)


# ─── Helper Functions ─────────────────────────────────────────────────────────
def check_api():
    try:
        r = requests.get(f"{API_URL}/health", timeout=3)
        return r.status_code == 200
    except:
        return False


def get_repos():
    try:
        r = requests.get(f"{API_URL}/repos", timeout=5)
        return r.json().get("repos", [])
    except:
        return []


def get_repo_stats(repo_name):
    try:
        r = requests.get(f"{API_URL}/repos/{repo_name}", timeout=5)
        return r.json()
    except:
        return {}


def ingest_repo(github_url, force=False):
    try:
        r = requests.post(f"{API_URL}/ingest", json={
            "github_url": github_url,
            "force_reclone": force
        }, timeout=10)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def get_status(repo_name):
    try:
        r = requests.get(f"{API_URL}/status/{repo_name}", timeout=5)
        return r.json()
    except:
        return {"status": "error"}


def chat_with_repo(question, repo_name, use_agent=True):
    try:
        r = requests.post(f"{API_URL}/chat", json={
            "question": question,
            "repo_name": repo_name,
            "use_agent": use_agent,
            "k": 5,
        }, timeout=120)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def analyze_structure(repo_name):
    try:
        r = requests.post(f"{API_URL}/analyze/structure",
                         json={"repo_name": repo_name}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def analyze_dependencies(repo_name):
    try:
        r = requests.post(f"{API_URL}/analyze/dependencies",
                         json={"repo_name": repo_name}, timeout=30)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


def analyze_bugs(repo_name):
    try:
        r = requests.post(f"{API_URL}/analyze/bugs",
                         json={"repo_name": repo_name}, timeout=60)
        return r.json()
    except Exception as e:
        return {"error": str(e)}


# ─── Session State ────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "selected_repo" not in st.session_state:
    st.session_state.selected_repo = None
if "use_agent" not in st.session_state:
    st.session_state.use_agent = True


# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    # Logo
    st.markdown('<div class="repomind-logo">RepoMind</div>', unsafe_allow_html=True)
    st.markdown('<div class="repomind-tagline">AI · Code Intelligence</div>', unsafe_allow_html=True)

    # API Status
    api_ok = check_api()
    if api_ok:
        st.markdown('<span class="status-badge status-online"><span class="status-dot dot-online"></span>API Online</span>', unsafe_allow_html=True)
    else:
        st.markdown('<span class="status-badge status-offline"><span class="status-dot dot-offline"></span>API Offline</span>', unsafe_allow_html=True)
        st.error("Start the API: `uvicorn app.main:app --reload --port 8000`")

    st.markdown("---")

    # ── Ingest New Repo ──
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
        with st.spinner("Starting ingestion..."):
            result = ingest_repo(github_url, force=force_reclone)

        if "error" in result:
            st.error(result["error"])
        elif result.get("status") == "already_indexed":
            st.success(f"✅ Already indexed!")
        else:
            repo_name = result.get("repo_name", "")
            st.info(f"⏳ Indexing **{repo_name}**...")

            # Poll status
            progress = st.progress(0)
            status_text = st.empty()
            stage_map = {
                "cloning": 20, "extracting": 40,
                "chunking": 60, "indexing": 80, "complete": 100
            }

            for _ in range(120):
                status = get_status(repo_name)
                stage = status.get("status", "")
                msg = status.get("message", "")
                progress.progress(stage_map.get(stage, 10))
                status_text.markdown(f'<div class="section-label">{msg}</div>', unsafe_allow_html=True)

                if stage == "complete":
                    st.success(f"✅ {msg}")
                    st.rerun()
                    break
                elif stage == "error":
                    st.error(f"❌ {msg}")
                    break
                time.sleep(2)

    st.markdown("---")

    # ── Indexed Repos ──
    st.markdown('<div class="section-label">Indexed Repositories</div>', unsafe_allow_html=True)
    repos = get_repos()

    if not repos:
        st.markdown('<div style="color: #555570; font-size: 0.8rem; font-family: JetBrains Mono, monospace;">No repos indexed yet</div>', unsafe_allow_html=True)
    else:
        for repo in repos:
            stats = get_repo_stats(repo)
            chunks = stats.get("total_chunks", "?")
            is_selected = st.session_state.selected_repo == repo

            border_color = "#00ff88" if is_selected else "#2a2a3a"
            st.markdown(f"""
            <div class="repo-card" style="border-color: {border_color}; cursor: pointer;">
                <div class="repo-card-name">📦 {repo}</div>
                <div class="repo-card-stat">{chunks} chunks indexed</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"Select {repo}", key=f"sel_{repo}", use_container_width=True):
                st.session_state.selected_repo = repo
                st.session_state.messages = []
                st.rerun()

    st.markdown("---")

    # ── Settings ──
    st.markdown('<div class="section-label">Settings</div>', unsafe_allow_html=True)
    st.session_state.use_agent = st.toggle(
        "🤖 Agentic Mode",
        value=st.session_state.use_agent,
        help="Agent uses tools to reason. Disable for faster simple RAG."
    )


# ─── Main Content ─────────────────────────────────────────────────────────────
selected = st.session_state.selected_repo

if selected is None:
    # ── Welcome Screen ──
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
    # ── Repo Header ──
    stats = get_repo_stats(selected)
    col1, col2, col3, col4 = st.columns([4, 1, 1, 1])

    with col1:
        st.markdown(f"""
        <div class="chat-header">
            <div class="chat-title">📦 {selected}</div>
            <div class="chat-subtitle">{'🤖 Agentic RAG' if st.session_state.use_agent else '⚡ Simple RAG'} · Ask anything about this repository</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{stats.get('total_chunks', '?')}</div>
            <div class="metric-label">Chunks</div>
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-value">{'✅' if stats.get('indexed') else '❌'}</div>
            <div class="metric-label">Indexed</div>
        </div>
        """, unsafe_allow_html=True)

    with col4:
        if st.button("🗑️ Clear", help="Clear chat history"):
            st.session_state.messages = []
            st.rerun()

    # ── Tabs ──
    tab1, tab2, tab3, tab4 = st.tabs(["💬 CHAT", "🏗️ STRUCTURE", "🔗 DEPENDENCIES", "🐛 BUG SCAN"])

    # ── Chat Tab ──
    with tab1:
        # Display messages
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f'<div class="msg-user">{msg["content"]}</div>', unsafe_allow_html=True)
            else:
                st.markdown(f'<div class="msg-ai">{msg["content"]}</div>', unsafe_allow_html=True)
                if msg.get("sources"):
                    st.markdown('<div class="sources-header">Sources</div>', unsafe_allow_html=True)
                    chips = "".join([
                        f'<span class="source-chip">📄 {s["file"]}</span>'
                        for s in msg["sources"][:5]
                    ])
                    st.markdown(chips, unsafe_allow_html=True)

        # Suggested questions
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
                        with st.spinner("🧠 Thinking..."):
                            result = chat_with_repo(suggestion, selected, st.session_state.use_agent)
                        if "error" in result:
                            answer = f"❌ Error: {result['error']}"
                            st.session_state.messages.append({"role": "assistant", "content": answer})
                        else:
                            st.session_state.messages.append({
                                "role": "assistant",
                                "content": result.get("answer", "No answer"),
                                "sources": result.get("sources", []),
                            })
                        st.rerun()

        # Input
        st.markdown("<br>", unsafe_allow_html=True)
        with st.container():
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

            with st.spinner("🧠 RepoMind is thinking..."):
                result = chat_with_repo(question, selected, st.session_state.use_agent)

            if "error" in result:
                answer = f"❌ Error: {result['error']}"
                st.session_state.messages.append({"role": "assistant", "content": answer})
            else:
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result.get("answer", "No answer"),
                    "sources": result.get("sources", []),
                })
            st.rerun()

    # ── Structure Tab ──
    with tab2:
        if st.button("🔍 Analyze Structure", use_container_width=True):
            with st.spinner("Analyzing repository structure..."):
                result = analyze_structure(selected)

            if "error" in result:
                st.error(result["error"])
            else:
                analysis = result.get("analysis", {})
                summary = result.get("summary", "")

                # Metrics row
                m1, m2, m3 = st.columns(3)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{analysis.get("total_files", 0)}</div><div class="metric-label">Total Files</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{analysis.get("total_dirs", 0)}</div><div class="metric-label">Directories</div></div>', unsafe_allow_html=True)
                with m3:
                    langs = analysis.get("languages", {})
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{len(langs)}</div><div class="metric-label">Languages</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)

                col_a, col_b = st.columns(2)
                with col_a:
                    st.markdown('<div class="section-label">Languages</div>', unsafe_allow_html=True)
                    for lang, count in langs.items():
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

                st.markdown('<div class="section-label" style="margin-top:1rem">File Tree</div>', unsafe_allow_html=True)
                st.code(analysis.get("tree", ""), language=None)

    # ── Dependencies Tab ──
    with tab3:
        if st.button("🔗 Analyze Dependencies", use_container_width=True):
            with st.spinner("Building dependency graph..."):
                result = analyze_dependencies(selected)

            if "error" in result:
                st.error(result["error"])
            else:
                graph = result.get("graph", {})
                summary = result.get("summary", "")

                m1, m2 = st.columns(2)
                with m1:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{graph.get("total_files", 0)}</div><div class="metric-label">Files Analyzed</div></div>', unsafe_allow_html=True)
                with m2:
                    st.markdown(f'<div class="metric-card"><div class="metric-value">{graph.get("total_deps", 0)}</div><div class="metric-label">Dependencies</div></div>', unsafe_allow_html=True)

                st.markdown("<br>", unsafe_allow_html=True)
                st.markdown('<div class="section-label">Most Imported Modules</div>', unsafe_allow_html=True)

                for module, count in graph.get("top_imports", []):
                    bar_width = min(100, int(count * 3))
                    st.markdown(f"""
                    <div style="margin-bottom: 8px;">
                        <div style="display:flex; justify-content:space-between; margin-bottom:3px;">
                            <span style="font-family: JetBrains Mono, monospace; font-size:0.8rem; color:#f0f0f8;">{module}</span>
                            <span style="font-family: JetBrains Mono, monospace; font-size:0.75rem; color:#555570;">{count}x</span>
                        </div>
                        <div style="background:#1c1c28; border-radius:4px; height:6px; overflow:hidden;">
                            <div style="background: linear-gradient(90deg, #00ff88, #4488ff); width:{bar_width}%; height:100%; border-radius:4px;"></div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

    # ── Bug Scan Tab ──
    with tab4:
        st.markdown('<div style="color: #8888aa; font-size: 0.82rem; font-family: JetBrains Mono, monospace; margin-bottom: 1rem;">AI-powered static analysis using LLM reasoning</div>', unsafe_allow_html=True)

        if st.button("🐛 Run Bug Scan", use_container_width=True):
            with st.spinner("🔍 Scanning for bugs and security issues..."):
                result = analyze_bugs(selected)

            if "error" in result:
                st.error(result["error"])
            else:
                report = result.get("report", {})
                st.markdown(f'<div class="metric-card" style="margin-bottom:1rem;"><div class="metric-value">{report.get("files_analyzed", 0)}</div><div class="metric-label">Files Scanned</div></div>', unsafe_allow_html=True)
                st.markdown('<div class="section-label">Findings</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="msg-ai">{report.get("findings", "No findings")}</div>', unsafe_allow_html=True)