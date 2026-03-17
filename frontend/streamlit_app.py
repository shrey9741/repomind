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
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Fira+Code:wght@300;400;500;600&display=swap');

:root {
    --bg-primary: #080810;
    --bg-secondary: #0d0d18;
    --bg-card: #12121e;
    --bg-card-hover: #171726;
    --bg-input: #0f0f1c;
    --accent-green: #0dffb0;
    --accent-blue: #3d7fff;
    --accent-purple: #8b5cf6;
    --accent-pink: #f472b6;
    --accent-cyan: #22d3ee;
    --text-primary: #eeeef8;
    --text-secondary: #9898b8;
    --text-muted: #4a4a6a;
    --border: #1e1e30;
    --border-bright: #2e2e48;
    --glow-green: rgba(13,255,176,0.15);
    --glow-blue: rgba(61,127,255,0.15);
    --shadow: 0 8px 32px rgba(0,0,0,0.4);
}

* { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Space Grotesk', sans-serif;
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
}

.stApp {
    background: var(--bg-primary) !important;
    background-image:
        radial-gradient(ellipse 80% 50% at 10% 0%, rgba(13,255,176,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 60% 40% at 90% 100%, rgba(61,127,255,0.04) 0%, transparent 60%),
        radial-gradient(ellipse 40% 60% at 50% 50%, rgba(139,92,246,0.02) 0%, transparent 70%);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container { padding-top: 1.5rem !important; max-width: 100% !important; }

/* ═══════════════════════════════════════════════
   SIDEBAR — PERMANENT FIX
═══════════════════════════════════════════════ */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-bright) !important;
    box-shadow: 4px 0 24px rgba(0,0,0,0.3) !important;
}

[data-testid="stSidebar"] * { color: var(--text-primary) !important; }

/* Force sidebar toggle ALWAYS visible */
[data-testid="collapsedControl"],
button[data-testid="collapsedControl"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    position: fixed !important;
    top: 1.2rem !important;
    left: 0 !important;
    z-index: 9999999 !important;
    width: 2.2rem !important;
    height: 2.2rem !important;
    min-width: 2.2rem !important;
    min-height: 2.2rem !important;
    background: var(--bg-card) !important;
    border: 1px solid var(--accent-green) !important;
    border-left: none !important;
    border-radius: 0 10px 10px 0 !important;
    cursor: pointer !important;
    align-items: center !important;
    justify-content: center !important;
    transition: all 0.2s ease !important;
    box-shadow: 3px 0 12px rgba(13,255,176,0.2) !important;
}

[data-testid="collapsedControl"]:hover {
    background: rgba(13,255,176,0.12) !important;
    box-shadow: 3px 0 18px rgba(13,255,176,0.35) !important;
    width: 2.6rem !important;
}

[data-testid="collapsedControl"] svg,
[data-testid="collapsedControl"] * {
    fill: var(--accent-green) !important;
    color: var(--accent-green) !important;
    stroke: var(--accent-green) !important;
}

/* ═══════════════════════════════════════════════
   LOGO & BRANDING
═══════════════════════════════════════════════ */
.repomind-logo {
    font-family: 'Space Grotesk', sans-serif;
    font-weight: 700;
    font-size: 1.75rem;
    letter-spacing: -0.04em;
    line-height: 1;
    margin-bottom: 0.2rem;
    position: relative;
    display: inline-block;
}

.repomind-logo .logo-repo {
    color: var(--text-primary);
}

.repomind-logo .logo-mind {
    background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.repomind-tagline {
    font-size: 0.68rem;
    color: var(--text-muted);
    letter-spacing: 0.18em;
    text-transform: uppercase;
    font-family: 'Fira Code', monospace;
    margin-bottom: 1.5rem;
}

/* ═══════════════════════════════════════════════
   SECTION LABELS
═══════════════════════════════════════════════ */
.section-label {
    font-size: 0.62rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: var(--text-muted);
    font-family: 'Fira Code', monospace;
    margin-bottom: 0.6rem;
    margin-top: 1.2rem;
    display: flex;
    align-items: center;
    gap: 6px;
}

.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ═══════════════════════════════════════════════
   REPO CARDS
═══════════════════════════════════════════════ */
.repo-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 12px 14px;
    margin-bottom: 0.4rem;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.repo-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, var(--accent-green), transparent);
    opacity: 0;
    transition: opacity 0.3s;
}

.repo-card:hover::before { opacity: 1; }

.repo-card-name {
    font-weight: 600;
    font-size: 0.88rem;
    color: var(--accent-green);
    font-family: 'Fira Code', monospace;
    display: flex;
    align-items: center;
    gap: 6px;
}

.repo-card-stat {
    font-size: 0.7rem;
    color: var(--text-muted);
    font-family: 'Fira Code', monospace;
    margin-top: 4px;
}

/* ═══════════════════════════════════════════════
   CHAT MESSAGES
═══════════════════════════════════════════════ */
.msg-user {
    background: linear-gradient(135deg, rgba(61,127,255,0.1), rgba(61,127,255,0.05));
    border: 1px solid rgba(61,127,255,0.18);
    border-radius: 18px 18px 5px 18px;
    padding: 14px 18px;
    margin: 10px 0;
    margin-left: 4rem;
    font-size: 0.9rem;
    line-height: 1.65;
    animation: slideInRight 0.25s ease-out;
    box-shadow: 0 4px 16px rgba(61,127,255,0.08);
}

.msg-user-label {
    font-size: 0.58rem;
    font-family: 'Fira Code', monospace;
    color: var(--accent-blue);
    letter-spacing: 0.18em;
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
}

.msg-ai {
    background: linear-gradient(135deg, rgba(13,255,176,0.07), rgba(13,255,176,0.02));
    border: 1px solid rgba(13,255,176,0.12);
    border-radius: 18px 18px 18px 5px;
    padding: 14px 18px;
    margin: 10px 0;
    margin-right: 4rem;
    font-size: 0.9rem;
    line-height: 1.65;
    animation: slideInLeft 0.25s ease-out;
    box-shadow: 0 4px 16px rgba(13,255,176,0.06);
    position: relative;
}

.msg-ai-label {
    font-size: 0.58rem;
    font-family: 'Fira Code', monospace;
    color: var(--accent-green);
    letter-spacing: 0.18em;
    display: block;
    margin-bottom: 6px;
    font-weight: 600;
}

@keyframes slideInRight {
    from { opacity: 0; transform: translateX(12px); }
    to   { opacity: 1; transform: translateX(0); }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-12px); }
    to   { opacity: 1; transform: translateX(0); }
}

/* ═══════════════════════════════════════════════
   TYPING INDICATOR
═══════════════════════════════════════════════ */
.typing-indicator {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 12px 18px;
    background: linear-gradient(135deg, rgba(13,255,176,0.07), rgba(13,255,176,0.02));
    border: 1px solid rgba(13,255,176,0.12);
    border-radius: 18px 18px 18px 5px;
    margin: 10px 0;
    margin-right: 4rem;
}

.typing-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent-green);
    animation: pulse 1.4s infinite ease-in-out;
}
.typing-dot:nth-child(2) { animation-delay: 0.2s; }
.typing-dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes pulse {
    0%, 60%, 100% { transform: scale(0.8); opacity: 0.4; }
    30% { transform: scale(1.2); opacity: 1; }
}

/* ═══════════════════════════════════════════════
   RESPONSE TIME BADGE
═══════════════════════════════════════════════ */
.response-time {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    font-size: 0.6rem;
    font-family: 'Fira Code', monospace;
    color: var(--text-muted);
    margin-top: 8px;
    padding: 3px 8px;
    background: rgba(0,0,0,0.3);
    border-radius: 20px;
    border: 1px solid var(--border);
}

/* ═══════════════════════════════════════════════
   SOURCE CHIPS
═══════════════════════════════════════════════ */
.source-chip {
    display: inline-block;
    background: rgba(139,92,246,0.1);
    border: 1px solid rgba(139,92,246,0.22);
    border-radius: 7px;
    padding: 3px 10px;
    font-size: 0.67rem;
    font-family: 'Fira Code', monospace;
    color: #a78bfa;
    margin: 2px 3px 2px 0;
    transition: all 0.15s;
}

.source-chip:hover {
    background: rgba(139,92,246,0.18);
    border-color: rgba(139,92,246,0.4);
}

/* ═══════════════════════════════════════════════
   METRIC CARDS
═══════════════════════════════════════════════ */
.metric-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 14px 16px;
    text-align: center;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}

.metric-card::after {
    content: '';
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-green), var(--accent-blue));
    opacity: 0.4;
}

.metric-value {
    font-size: 1.5rem;
    font-weight: 700;
    font-family: 'Fira Code', monospace;
    background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.metric-label {
    font-size: 0.62rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.12em;
    margin-top: 3px;
    font-family: 'Fira Code', monospace;
}

/* ═══════════════════════════════════════════════
   WELCOME SCREEN
═══════════════════════════════════════════════ */
.welcome-container {
    text-align: center;
    padding: 5rem 2rem 3rem;
}

.welcome-brain {
    font-size: 4.5rem;
    margin-bottom: 1.2rem;
    display: block;
    animation: float 4s ease-in-out infinite;
    filter: drop-shadow(0 0 24px rgba(13,255,176,0.3));
}

@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}

.welcome-title {
    font-size: 2.4rem;
    font-weight: 700;
    letter-spacing: -0.04em;
    margin-bottom: 0.5rem;
    background: linear-gradient(135deg, var(--text-primary) 30%, var(--accent-green));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.welcome-subtitle {
    color: var(--text-muted);
    font-family: 'Fira Code', monospace;
    font-size: 0.82rem;
    margin-bottom: 2.5rem;
    letter-spacing: 0.05em;
}

.suggestion-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 12px;
    max-width: 640px;
    margin: 0 auto;
}

.suggestion-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 18px;
    text-align: left;
    transition: all 0.2s ease;
    cursor: pointer;
}

.suggestion-card:hover {
    border-color: var(--border-bright);
    background: var(--bg-card-hover);
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(13,255,176,0.08);
}

.suggestion-icon { font-size: 1.4rem; margin-bottom: 8px; display: block; }

.suggestion-text {
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.45;
}

/* ═══════════════════════════════════════════════
   REPO HEADER
═══════════════════════════════════════════════ */
.repo-header {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 1.2rem;
    display: flex;
    align-items: center;
    gap: 12px;
}

.repo-header-name {
    font-size: 1.25rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    font-family: 'Fira Code', monospace;
    color: var(--accent-green);
}

.repo-header-mode {
    font-size: 0.72rem;
    color: var(--text-muted);
    font-family: 'Fira Code', monospace;
    margin-top: 2px;
}

.mode-badge {
    display: inline-flex;
    align-items: center;
    gap: 5px;
    padding: 3px 10px;
    border-radius: 20px;
    font-size: 0.65rem;
    font-family: 'Fira Code', monospace;
    font-weight: 500;
    letter-spacing: 0.05em;
}

.mode-badge-agent {
    background: rgba(13,255,176,0.1);
    border: 1px solid rgba(13,255,176,0.25);
    color: var(--accent-green);
}

.mode-badge-rag {
    background: rgba(61,127,255,0.1);
    border: 1px solid rgba(61,127,255,0.25);
    color: var(--accent-blue);
}

/* ═══════════════════════════════════════════════
   INPUTS
═══════════════════════════════════════════════ */
.stTextInput input, .stTextArea textarea {
    background: var(--bg-input) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 12px !important;
    color: var(--text-primary) !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.86rem !important;
    transition: all 0.2s !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--accent-green) !important;
    box-shadow: 0 0 0 3px rgba(13,255,176,0.08) !important;
    background: var(--bg-card) !important;
}

.stTextInput input::placeholder {
    color: var(--text-muted) !important;
}

/* ═══════════════════════════════════════════════
   BUTTONS
═══════════════════════════════════════════════ */
.stButton button {
    background: var(--bg-card) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-bright) !important;
    border-radius: 12px !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.83rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    letter-spacing: 0.01em !important;
}

.stButton button:hover {
    border-color: var(--accent-green) !important;
    color: var(--accent-green) !important;
    background: rgba(13,255,176,0.05) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 16px rgba(13,255,176,0.1) !important;
}

/* Sidebar buttons */
[data-testid="stSidebar"] .stButton button {
    background: var(--bg-card) !important;
    color: var(--text-secondary) !important;
    border: 1px solid var(--border-bright) !important;
    text-align: left !important;
    padding-left: 12px !important;
}

[data-testid="stSidebar"] .stButton button:hover {
    border-color: var(--accent-green) !important;
    color: var(--accent-green) !important;
}

/* Primary / Send button — last column */
div[data-testid="column"]:last-child .stButton button {
    background: linear-gradient(135deg, var(--accent-green), #00c886) !important;
    color: #080810 !important;
    border: none !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    box-shadow: 0 4px 16px rgba(13,255,176,0.25) !important;
}

div[data-testid="column"]:last-child .stButton button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 24px rgba(13,255,176,0.4) !important;
    color: #080810 !important;
}

/* Ingest button */
[data-testid="stSidebar"] div[data-testid="column"]:first-child .stButton button {
    background: linear-gradient(135deg, rgba(13,255,176,0.12), rgba(13,255,176,0.06)) !important;
    border: 1px solid rgba(13,255,176,0.3) !important;
    color: var(--accent-green) !important;
    font-weight: 700 !important;
    text-align: center !important;
}

[data-testid="stSidebar"] div[data-testid="column"]:first-child .stButton button:hover {
    background: rgba(13,255,176,0.18) !important;
    box-shadow: 0 4px 16px rgba(13,255,176,0.15) !important;
}

/* ═══════════════════════════════════════════════
   TABS
═══════════════════════════════════════════════ */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card) !important;
    border-radius: 14px !important;
    padding: 5px !important;
    border: 1px solid var(--border) !important;
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    border-radius: 10px !important;
    font-family: 'Fira Code', monospace !important;
    font-size: 0.73rem !important;
    letter-spacing: 0.05em !important;
    padding: 6px 14px !important;
    transition: all 0.2s !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-secondary) !important;
    background: rgba(255,255,255,0.04) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, rgba(13,255,176,0.12), rgba(13,255,176,0.06)) !important;
    color: var(--accent-green) !important;
    border: 1px solid rgba(13,255,176,0.2) !important;
}

/* ═══════════════════════════════════════════════
   PROGRESS & SPINNER
═══════════════════════════════════════════════ */
.stProgress > div > div {
    background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan)) !important;
    border-radius: 4px !important;
}

.stProgress > div {
    background: var(--bg-card) !important;
    border-radius: 4px !important;
    height: 6px !important;
}

/* ═══════════════════════════════════════════════
   TOGGLE
═══════════════════════════════════════════════ */
.stToggle label { color: var(--text-secondary) !important; font-size: 0.85rem !important; }

/* ═══════════════════════════════════════════════
   DIVIDER
═══════════════════════════════════════════════ */
hr { border-color: var(--border) !important; margin: 1rem 0 !important; }

/* ═══════════════════════════════════════════════
   SCROLLBAR
═══════════════════════════════════════════════ */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb {
    background: var(--border-bright);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover { background: var(--text-muted); }

/* ═══════════════════════════════════════════════
   ANALYSIS CONTENT
═══════════════════════════════════════════════ */
.analysis-box {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 18px;
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    color: var(--text-secondary);
    line-height: 1.7;
    white-space: pre-wrap;
    margin-top: 1rem;
}

.bar-row {
    margin-bottom: 10px;
}

.bar-label {
    display: flex;
    justify-content: space-between;
    margin-bottom: 4px;
}

.bar-name {
    font-family: 'Fira Code', monospace;
    font-size: 0.8rem;
    color: var(--text-primary);
}

.bar-count {
    font-family: 'Fira Code', monospace;
    font-size: 0.75rem;
    color: var(--text-muted);
}

.bar-track {
    background: var(--bg-input);
    border-radius: 4px;
    height: 6px;
    overflow: hidden;
}

.bar-fill {
    height: 100%;
    border-radius: 4px;
    background: linear-gradient(90deg, var(--accent-green), var(--accent-cyan));
    transition: width 0.6s ease;
}

/* ═══════════════════════════════════════════════
   MOBILE
═══════════════════════════════════════════════ */
@media (max-width: 768px) {
    .msg-user { margin-left: 0.5rem !important; }
    .msg-ai { margin-right: 0.5rem !important; }
    .welcome-title { font-size: 1.6rem !important; }
    .suggestion-grid { grid-template-columns: 1fr !important; }
    .block-container { padding: 0.5rem !important; }
    .metric-value { font-size: 1.1rem !important; }
    [data-testid="collapsedControl"] {
        display: flex !important;
        position: fixed !important;
        top: 0.5rem !important;
        left: 0 !important;
        z-index: 9999999 !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }
}
</style>

<script>
// Ensure sidebar toggle is always accessible
(function keepToggleVisible() {
    function fixToggle() {
        const btns = document.querySelectorAll('[data-testid="collapsedControl"]');
        btns.forEach(btn => {
            btn.style.cssText += ';display:flex!important;visibility:visible!important;opacity:1!important;pointer-events:auto!important;z-index:9999999!important;';
        });
    }
    fixToggle();
    const obs = new MutationObserver(fixToggle);
    obs.observe(document.body, { childList: true, subtree: true, attributes: true });
    setInterval(fixToggle, 800);
})();
</script>
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
    st.markdown("""
    <div style="padding: 0.5rem 0 0.2rem;">
        <div class="repomind-logo">
            <span class="logo-repo">Repo</span><span class="logo-mind">Mind</span>
        </div>
        <div class="repomind-tagline">AI · Code Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

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
            '<div style="color:var(--text-muted);font-size:0.78rem;font-family:Fira Code,monospace;padding:8px 0;">No repos indexed yet</div>',
            unsafe_allow_html=True
        )
    else:
        for repo in repos:
            stats = get_repo_stats_direct(repo)
            chunks = stats.get("total_chunks", "?")
            is_selected = st.session_state.selected_repo == repo
            border_color = "var(--accent-green)" if is_selected else "var(--border)"
            bg_color = "rgba(13,255,176,0.05)" if is_selected else "var(--bg-card)"

            st.markdown(f"""
            <div class="repo-card" style="border-color:{border_color};background:{bg_color};">
                <div class="repo-card-name">📦 {repo}</div>
                <div class="repo-card-stat">{chunks} chunks · indexed</div>
            </div>
            """, unsafe_allow_html=True)

            if st.button(f"{'✓ Selected' if is_selected else 'Select'} {repo}", key=f"sel_{repo}", use_container_width=True):
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

    st.markdown("""
    <div style="margin-top:auto;padding-top:1.5rem;">
        <div style="font-size:0.62rem;color:var(--text-muted);font-family:Fira Code,monospace;text-align:center;letter-spacing:0.1em;">
            REPOMIND · AI CODE INTELLIGENCE
        </div>
    </div>
    """, unsafe_allow_html=True)


# ─── Main Content ─────────────────────────────────────────────────────────────
selected = st.session_state.selected_repo

if selected is None:
    st.markdown("""
    <div class="welcome-container">
        <span class="welcome-brain">🧠</span>
        <div class="welcome-title">Chat with any codebase</div>
        <div class="welcome-subtitle">← Select or ingest a repository to get started</div>
        <div class="suggestion-grid">
            <div class="suggestion-card">
                <span class="suggestion-icon">🏗️</span>
                <div class="suggestion-text">Understand project architecture and folder structure</div>
            </div>
            <div class="suggestion-card">
                <span class="suggestion-icon">🔍</span>
                <div class="suggestion-text">Find where specific functionality is implemented</div>
            </div>
            <div class="suggestion-card">
                <span class="suggestion-icon">🐛</span>
                <div class="suggestion-text">Detect potential bugs and security issues</div>
            </div>
            <div class="suggestion-card">
                <span class="suggestion-icon">📖</span>
                <div class="suggestion-text">Generate documentation for any module</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

else:
    stats = get_repo_stats_direct(selected)

    # ── Repo Header ──
    mode_badge = (
        '<span class="mode-badge mode-badge-agent">🤖 Agentic RAG</span>'
        if st.session_state.use_agent
        else '<span class="mode-badge mode-badge-rag">⚡ Simple RAG</span>'
    )

    col_header, col_clear = st.columns([5, 1])
    with col_header:
        st.markdown(f"""
        <div class="repo-header">
            <div>
                <div class="repo-header-name">📦 {selected}</div>
                <div class="repo-header-mode">{mode_badge} · Ask anything about this repository</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    with col_clear:
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # ── Metric Row ──
    m1, m2, m3 = st.columns(3)
    with m1:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{stats.get("total_chunks","?")}</div><div class="metric-label">Chunks</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{"✅" if stats.get("indexed") else "❌"}</div><div class="metric-label">Indexed</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown(f'<div class="metric-card"><div class="metric-value">{len(st.session_state.messages) // 2}</div><div class="metric-label">Exchanges</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs(["💬  CHAT", "🏗️  STRUCTURE", "🔗  DEPENDENCIES", "🐛  BUG SCAN"])

    # ══ Chat Tab ══
    with tab1:
        # Message history
        for msg in st.session_state.messages:
            if msg["role"] == "user":
                st.markdown(f"""
                <div class="msg-user">
                    <span class="msg-user-label">YOU</span>
                    {msg["content"]}
                </div>
                """, unsafe_allow_html=True)
            else:
                response_time = msg.get("response_time", None)
                time_badge = f'<div class="response-time">⚡ {response_time:.1f}s</div>' if response_time else ""
                st.markdown(f"""
                <div class="msg-ai">
                    <span class="msg-ai-label">REPOMIND</span>
                    {msg["content"]}
                    {time_badge}
                </div>
                """, unsafe_allow_html=True)
                if msg.get("sources"):
                    chips = "".join([
                        f'<span class="source-chip">📄 {s["file"]}</span>'
                        for s in msg["sources"][:5]
                    ])
                    st.markdown(f'<div style="margin-top:4px;margin-left:2px;">{chips}</div>', unsafe_allow_html=True)

        # Suggestions if no messages
        if not st.session_state.messages:
            st.markdown('<div class="section-label" style="margin-top:1.5rem;">Suggested Questions</div>', unsafe_allow_html=True)
            suggestions = [
                f"What is the overall architecture of {selected}?",
                f"How does {selected} handle errors?",
                f"What are the main entry points of {selected}?",
                f"Explain the folder structure of {selected}",
            ]
            cols = st.columns(2)
            for i, suggestion in enumerate(suggestions):
                with cols[i % 2]:
                    if st.button(suggestion, key=f"sug_{i}", use_container_width=True):
                        st.session_state.messages.append({"role": "user", "content": suggestion})
                        typing_ph = st.empty()
                        typing_ph.markdown("""
                        <div class="typing-indicator">
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                            <span class="typing-dot"></span>
                        </div>
                        """, unsafe_allow_html=True)
                        start = time.time()
                        result = chat_direct(suggestion, selected, st.session_state.use_agent)
                        elapsed = time.time() - start
                        typing_ph.empty()
                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": result.get("answer", "No answer"),
                            "sources": result.get("sources", []),
                            "response_time": elapsed,
                        })
                        st.rerun()

        # Input bar
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
            typing_ph = st.empty()
            typing_ph.markdown("""
            <div class="typing-indicator">
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
                <span class="typing-dot"></span>
            </div>
            """, unsafe_allow_html=True)
            start = time.time()
            result = chat_direct(question, selected, st.session_state.use_agent)
            elapsed = time.time() - start
            typing_ph.empty()
            st.session_state.messages.append({
                "role": "assistant",
                "content": result.get("answer", "No answer"),
                "sources": result.get("sources", []),
                "response_time": elapsed,
            })
            st.rerun()

    # ══ Structure Tab ══
    with tab2:
        if st.button("🔍 Analyze Structure", use_container_width=True):
            with st.spinner("Analyzing repository structure..."):
                result = analyze_structure_direct(selected)
            analysis = result.get("analysis", {})

            s1, s2, s3 = st.columns(3)
            with s1:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{analysis.get("total_files",0)}</div><div class="metric-label">Files</div></div>', unsafe_allow_html=True)
            with s2:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{analysis.get("total_dirs",0)}</div><div class="metric-label">Directories</div></div>', unsafe_allow_html=True)
            with s3:
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

            st.markdown('<div class="section-label" style="margin-top:1rem">Directory Tree</div>', unsafe_allow_html=True)
            st.code(analysis.get("tree", ""), language=None)

    # ══ Dependencies Tab ══
    with tab3:
        if st.button("🔗 Analyze Dependencies", use_container_width=True):
            with st.spinner("Building dependency graph..."):
                result = analyze_deps_direct(selected)
            graph = result.get("graph", {})

            d1, d2 = st.columns(2)
            with d1:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{graph.get("total_files",0)}</div><div class="metric-label">Files</div></div>', unsafe_allow_html=True)
            with d2:
                st.markdown(f'<div class="metric-card"><div class="metric-value">{graph.get("total_deps",0)}</div><div class="metric-label">Dependencies</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="section-label" style="margin-top:1.5rem">Most Imported Modules</div>', unsafe_allow_html=True)

            top_imports = graph.get("top_imports", [])
            max_count = max((c for _, c in top_imports), default=1)

            for module, count in top_imports:
                bar_pct = int((count / max_count) * 100)
                st.markdown(f"""
                <div class="bar-row">
                    <div class="bar-label">
                        <span class="bar-name">{module}</span>
                        <span class="bar-count">{count}×</span>
                    </div>
                    <div class="bar-track">
                        <div class="bar-fill" style="width:{bar_pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ══ Bug Scan Tab ══
    with tab4:
        st.markdown(
            '<div style="color:var(--text-muted);font-size:0.8rem;font-family:Fira Code,monospace;margin-bottom:1rem;padding:10px 14px;background:var(--bg-card);border:1px solid var(--border);border-radius:10px;">🔬 AI-powered static analysis using LLM reasoning — scans for bugs, security issues, and code smells.</div>',
            unsafe_allow_html=True
        )
        if st.button("🐛 Run Bug Scan", use_container_width=True):
            with st.spinner("🔍 Scanning for bugs and vulnerabilities..."):
                result = analyze_bugs_direct(selected)
            report = result.get("report", {})

            st.markdown(f"""
            <div class="metric-card" style="margin-bottom:1.2rem;text-align:left;display:flex;align-items:center;gap:16px;">
                <div>
                    <div class="metric-value">{report.get("files_analyzed",0)}</div>
                    <div class="metric-label">Files Scanned</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="section-label">Findings</div>', unsafe_allow_html=True)
            st.markdown(f"""
            <div class="msg-ai">
                <span class="msg-ai-label">BUG SCAN RESULTS</span>
                {report.get("findings","No findings")}
            </div>
            """, unsafe_allow_html=True)