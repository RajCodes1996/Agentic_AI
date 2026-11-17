from urllib.parse import urlparse
import streamlit as st
from agent import run_research

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------
st.set_page_config(
    page_title="NEXUS — Research Engine",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --------------------------------------------------
# HIGH-CONTRAST SLATE THEME CSS
# --------------------------------------------------
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500;600&display=swap');

:root {
    --bg-main: #0F172A;         /* Deep Slate Navy — easy on eyes, never pitch black */
    --bg-sidebar: #131C31;      /* Slightly lighter slate for clear separation */
    --bg-card: #1E293B;         /* Distinct card surface */
    --bg-input: #0B1120;        /* Recessed input field */
    --border-color: #334155;    /* Clearly visible slate borders */
    --border-hover: #64748B;
    --text-main: #F8FAFC;       /* Crisp white-slate text */
    --text-sub: #CBD5E1;        /* Bright secondary text */
    --text-muted: #94A3B8;      /* Clearly legible muted labels */
    --accent-blue: #38BDF8;     /* Sky cyan accent */
    --accent-green: #34D399;    /* Emerald status */
}

/* Main App Canvas */
.stApp {
    background-color: var(--bg-main) !important;
    color: var(--text-main) !important;
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Hide Streamlit top toolbar clutter cleanly */
header[data-testid="stHeader"] {
    background-color: var(--bg-main) !important;
}
#MainMenu, footer, [data-testid="stToolbar"] {
    visibility: hidden !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1180px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: var(--bg-sidebar) !important;
    border-right: 1px solid var(--border-color) !important;
}
section[data-testid="stSidebar"] * {
    color: var(--text-main);
}

/* Typography */
h1, h2, h3, h4, p, li, label {
    font-family: 'Inter', sans-serif !important;
    color: var(--text-main) !important;
}
.mono {
    font-family: 'JetBrains Mono', monospace !important;
}

/* Brand Header */
.brand-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding-bottom: 1.25rem;
    margin-bottom: 1.5rem;
    border-bottom: 1px solid var(--border-color);
}
.brand-title {
    font-size: 1.45rem;
    font-weight: 700;
    letter-spacing: -0.02em;
    color: #FFFFFF;
}
.status-badge {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--accent-green);
    background: rgba(52, 211, 153, 0.14);
    border: 1px solid rgba(52, 211, 153, 0.4);
    padding: 5px 12px;
    border-radius: 999px;
    display: inline-flex;
    align-items: center;
    gap: 8px;
}
.status-dot {
    width: 7px;
    height: 7px;
    background-color: var(--accent-green);
    border-radius: 50%;
    box-shadow: 0 0 8px var(--accent-green);
}

/* Search Form Container */
div[data-testid="stForm"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 12px !important;
    padding: 1.15rem 1.35rem !important;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}

/* Text Input & Placeholder Visibility */
.stTextInput input {
    background-color: var(--bg-input) !important;
    color: #FFFFFF !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    padding: 0.7rem 1rem !important;
    font-size: 0.95rem !important;
}
.stTextInput input::placeholder {
    color: #94A3B8 !important;
    opacity: 1 !important;
}
.stTextInput input:focus {
    border-color: var(--accent-blue) !important;
    box-shadow: 0 0 0 1px var(--accent-blue) !important;
}

/* Primary Submit Button (Sky Blue) */
div[data-testid="stFormSubmitButton"] > button {
    background: linear-gradient(135deg, #0284C7, #2563EB) !important;
    color: #FFFFFF !important;
    border: 1px solid #38BDF8 !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    height: 44px !important;
    transition: all 0.15s ease !important;
}
div[data-testid="stFormSubmitButton"] > button:hover {
    filter: brightness(1.12);
    transform: translateY(-1px);
}

/* Secondary / Sample Buttons (Dark Slate) */
.stButton > button {
    background-color: var(--bg-card) !important;
    color: var(--text-sub) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
    font-size: 0.82rem !important;
    min-height: 40px !important;
    text-align: left !important;
    transition: all 0.15s ease !important;
}
.stButton > button:hover {
    background-color: #27354F !important;
    color: #FFFFFF !important;
    border-color: var(--accent-blue) !important;
}

/* Bulletproof Selectbox & Floating Dropdown Portal Fix */
div[data-testid="stSelectbox"] div[data-baseweb="select"],
div[data-testid="stSelectbox"] div[data-baseweb="select"] > div,
div[data-testid="stSelectbox"] div[data-baseweb="select"] div,
div[data-testid="stSelectbox"] input {
    background-color: #1E293B !important;
    border-color: #334155 !important;
    border-radius: 8px !important;
    color: #F8FAFC !important;
    -webkit-text-fill-color: #F8FAFC !important;
}

div[data-testid="stSelectbox"] svg {
    fill: #F8FAFC !important;
    color: #F8FAFC !important;
}

/* Floating dropdown menu (rendered in root portal) */
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
ul[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
}

ul[data-baseweb="menu"] li,
ul[role="listbox"] li,
li[role="option"] {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
}

ul[data-baseweb="menu"] li:hover,
ul[role="listbox"] li:hover,
li[role="option"]:hover,
li[aria-selected="true"] {
    background-color: #334155 !important;
    color: #38BDF8 !important;
}

/* Section Labels */
.section-tag {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #94A3B8;
    margin-bottom: 8px;
}

/* KPI Metric Cards */
.kpi-card {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 10px;
    padding: 1.1rem 1.25rem;
}
.kpi-label {
    font-size: 0.74rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: var(--text-muted);
    margin-bottom: 6px;
}
.kpi-val {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.55rem;
    font-weight: 700;
    color: #FFFFFF;
}
.kpi-sub {
    font-size: 0.78rem;
    color: var(--text-sub);
    margin-top: 4px;
}

/* Research Step Rows */
.step-row {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin-bottom: 0.7rem;
    display: flex;
    align-items: flex-start;
    gap: 14px;
}
.step-num {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--accent-blue);
    background: rgba(56, 189, 248, 0.12);
    border: 1px solid rgba(56, 189, 248, 0.35);
    padding: 2px 9px;
    border-radius: 5px;
}
.step-text {
    font-size: 0.94rem;
    color: var(--text-main);
    line-height: 1.55;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 24px;
    border-bottom: 1px solid var(--border-color);
}
.stTabs [data-baseweb="tab"] {
    color: var(--text-muted) !important;
    font-size: 0.9rem;
    font-weight: 600;
    padding-bottom: 10px;
}
.stTabs [aria-selected="true"] {
    color: var(--accent-blue) !important;
    border-bottom-color: var(--accent-blue) !important;
}

/* Expanders (Evidence Cards) */
div[data-testid="stExpander"] {
    background-color: var(--bg-card) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 8px !important;
    margin-bottom: 0.6rem;
}
div[data-testid="stExpander"] summary p {
    color: #F8FAFC !important;
    font-weight: 500 !important;
}

/* Report Box */
.report-box {
    background-color: var(--bg-card);
    border: 1px solid var(--border-color);
    border-radius: 12px;
    padding: 1.85rem 2.1rem;
    line-height: 1.75;
    font-size: 0.96rem;
    color: var(--text-main);
}

/* Download Button */
div[data-testid="stDownloadButton"] > button {
    background-color: #1E293B !important;
    color: #38BDF8 !important;
    border: 1px solid #38BDF8 !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background-color: #0284C7 !important;
    color: #FFFFFF !important;
}

hr {
    border-color: var(--border-color) !important;
}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# HELPERS
# --------------------------------------------------
def extract_domain(url: str) -> str:
    try:
        netloc = urlparse(url).netloc
        return netloc.replace("www.", "") if netloc else "web"
    except Exception:
        return "web"

# --------------------------------------------------
# SESSION STATE
# --------------------------------------------------
if "research_result" not in st.session_state:
    st.session_state.research_result = None
if "research_topic" not in st.session_state:
    st.session_state.research_topic = ""
if "draft_topic" not in st.session_state:
    st.session_state.draft_topic = ""

# --------------------------------------------------
# SIDEBAR — SYSTEM TELEMETRY & CONFIG
# --------------------------------------------------
with st.sidebar:
    st.markdown("""
    <div style="display:flex; align-items:center; justify-content:space-between; margin-bottom:4px;">
        <span style="font-weight:700; font-size:1.15rem; color:#FFFFFF;">⚡ NEXUS</span>
        <span class="mono" style="font-size:0.72rem; color:#38BDF8; background:rgba(56,189,248,0.12); border:1px solid rgba(56,189,248,0.3); padding:2px 7px; border-radius:4px;">v1.0</span>
    </div>
    <div style="font-size:0.82rem; color:#94A3B8; margin-bottom:1rem;">Autonomous Research Runtime</div>
    """, unsafe_allow_html=True)

    st.divider()

    st.markdown('<div class="section-tag">Model Routing</div>', unsafe_allow_html=True)
    provider = st.selectbox(
        "Inference Backend",
        ["ollama", "gemini"],
        label_visibility="collapsed",
        format_func=lambda x: (
            "Ollama · Local Inference" if x == "ollama"
            else "Gemini · Cloud Inference"
        )
    )

    st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
    st.markdown('<div class="section-tag">Runtime Stack</div>', unsafe_allow_html=True)
    st.markdown("""
    <div style="background:#1E293B; border:1px solid #334155; border-radius:8px; padding:12px 14px; font-size:0.82rem;">
        <div style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #334155;">
            <span style="color:#94A3B8;">Search</span>
            <span class="mono" style="color:#F8FAFC;">Tavily API</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:5px 0; border-bottom:1px solid #334155;">
            <span style="color:#94A3B8;">Pipeline</span>
            <span class="mono" style="color:#F8FAFC;">Plan → Search → Synth</span>
        </div>
        <div style="display:flex; justify-content:space-between; padding:5px 0;">
            <span style="color:#94A3B8;">Verification</span>
            <span class="mono" style="color:#34D399;">Citation Guard</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    if st.session_state.research_result:
        if st.button("Reset Workspace", use_container_width=True):
            st.session_state.research_result = None
            st.session_state.research_topic = ""
            st.session_state.draft_topic = ""
            st.rerun()

    st.markdown(
        '<div class="mono" style="font-size:0.72rem; color:#94A3B8; margin-top:1rem;">AGENT 01 / 15 · LOCAL HOST</div>',
        unsafe_allow_html=True
    )

# --------------------------------------------------
# TOP BAR
# --------------------------------------------------
st.markdown(f"""
<div class="brand-header">
    <div class="brand-title">NEXUS Research Intelligence</div>
    <div class="status-badge">
        <span class="status-dot"></span>
        <span>ENGINE READY · {provider.upper()}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# --------------------------------------------------
# COMMAND INPUT & QUICK PROMPTS
# --------------------------------------------------
with st.form("research_form", border=False):
    col_in, col_btn = st.columns([5, 1.2])
    with col_in:
        topic = st.text_input(
            "Research Query",
            value=st.session_state.draft_topic,
            label_visibility="collapsed",
            placeholder="Ask a complex research question (e.g., Compare LoRA vs QLoRA memory tradeoffs)..."
        )
    with col_btn:
        submitted = st.form_submit_button("Run Agent →", use_container_width=True)

# Sample Prompts when idle
if not st.session_state.research_result:
    st.markdown('<div class="section-tag" style="margin-top:18px;">Suggested Investigations</div>', unsafe_allow_html=True)
    samples = [
        "State of small language models (SLMs) on edge hardware",
        "Retrieval-Augmented Generation vs Long-Context LLMs",
        "Multi-agent orchestration frameworks comparison"
    ]
    p_cols = st.columns(len(samples))
    for idx, sample in enumerate(samples):
        with p_cols[idx]:
            if st.button(sample, key=f"sample_{idx}", use_container_width=True):
                st.session_state.draft_topic = sample
                st.rerun()

# --------------------------------------------------
# EXECUTION FLOW
# --------------------------------------------------
if submitted:
    if not topic.strip():
        st.warning("Enter a research topic to initialize the agent.")
    else:
        try:
            with st.status(f"Executing research pipeline via {provider.upper()}...", expanded=True) as status:
                st.write("`[01/03]` Decomposing query into sub-questions...")
                result = run_research(
                    topic=topic.strip(),
                    provider=provider
                )
                st.write(f"`[02/03]` Retrieved and ranked {len(result.get('evidence', []))} web sources...")
                st.write("`[03/03]` Synthesizing report and validating inline citations...")
                status.update(label="Research mission complete", state="complete", expanded=False)

            st.session_state.research_result = result
            st.session_state.research_topic = topic.strip()
            st.session_state.draft_topic = topic.strip()
            st.rerun()

        except Exception as error:
            st.error(f"Pipeline execution error: {error}")

# --------------------------------------------------
# RESULTS WORKSPACE
# --------------------------------------------------
result = st.session_state.research_result

if result:
    timings = result.get("timings", {})
    total_time = sum(timings.values())
    evidence_list = result.get("evidence", [])
    questions_list = result["plan"].research_questions

    st.markdown("<div style='height:14px'></div>", unsafe_allow_html=True)

    # KPI Telemetry Strip
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Sources Indexed</div>
            <div class="kpi-val">{len(evidence_list)}</div>
            <div class="kpi-sub">Tavily web chunks</div>
        </div>
        """, unsafe_allow_html=True)
    with k2:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Sub-Queries</div>
            <div class="kpi-val">{len(questions_list)}</div>
            <div class="kpi-sub">Planned search vectors</div>
        </div>
        """, unsafe_allow_html=True)
    with k3:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Inference Node</div>
            <div class="kpi-val">{provider.upper()}</div>
            <div class="kpi-sub">{'Local runtime' if provider == 'ollama' else 'Cloud API'}</div>
        </div>
        """, unsafe_allow_html=True)
    with k4:
        st.markdown(f"""
        <div class="kpi-card">
            <div class="kpi-label">Total Latency</div>
            <div class="kpi-val">{total_time:.2f}s</div>
            <div class="kpi-sub">End-to-end wall time</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<div style='height:22px'></div>", unsafe_allow_html=True)

    # Navigation Tabs
    tab_report, tab_sources, tab_plan, tab_perf = st.tabs([
        "Synthesis Report",
        f"Evidence ({len(evidence_list)})",
        f"Query Plan ({len(questions_list)})",
        "Telemetry"
    ])

    with tab_report:
        if result.get("invalid_citations"):
            st.warning(
                f"Citation Guard flagged unverified references: {result['invalid_citations']}"
            )

        r_col1, r_col2 = st.columns([4, 1.3])
        with r_col1:
            st.markdown(f"### {st.session_state.research_topic}")
        with r_col2:
            st.download_button(
                label="Export Markdown",
                data=result["markdown_report"],
                file_name="nexus_research_report.md",
                mime="text/markdown",
                use_container_width=True
            )

        st.markdown('<div class="report-box">', unsafe_allow_html=True)
        st.markdown(result["analysis"])
        st.markdown('</div>', unsafe_allow_html=True)

        if result.get("saved_path"):
            st.markdown(
                f'<div class="mono" style="font-size:0.78rem; color:#94A3B8; margin-top:10px;">Saved artifact → {result["saved_path"]}</div>',
                unsafe_allow_html=True
            )

    with tab_sources:
        if not evidence_list:
            st.info("No external evidence was retrieved for this query.")
        else:
            for idx, source in enumerate(evidence_list, start=1):
                title = source.get("title") or f"Untitled Source {idx}"
                url = source.get("url", "#")
                domain = extract_domain(url)
                score = source.get("score")
                score_str = f"{score:.2f}" if isinstance(score, (int, float)) else str(score or "N/A")

                with st.expander(f"[{idx:02d}]  {title}  —  {domain} (score: {score_str})"):
                    st.markdown(
                        f'<div class="mono" style="font-size:0.78rem; color:#38BDF8; margin-bottom:8px;">'
                        f'SUB-QUERY: {source.get("research_question", "N/A")}</div>',
                        unsafe_allow_html=True
                    )
                    st.write(source.get("content", "No excerpt available."))
                    if url != "#":
                        st.markdown(f"[Open source ({domain}) ↗]({url})")

    with tab_plan:
        st.caption("Decomposed search queries generated by the planner node prior to retrieval.")
        for idx, question in enumerate(questions_list, start=1):
            st.markdown(f"""
            <div class="step-row">
                <span class="step-num">Q{idx:02d}</span>
                <div class="step-text">{question}</div>
            </div>
            """, unsafe_allow_html=True)

    with tab_perf:
        st.caption("Stage-by-stage execution latency breakdown.")
        for stage, duration in timings.items():
            pct = (duration / total_time * 100) if total_time > 0 else 0
            c_label, c_bar, c_val = st.columns([2, 5, 1.2])
            with c_label:
                st.markdown(f"**{stage.replace('_', ' ').title()}**")
            with c_bar:
                st.progress(min(duration / total_time, 1.0) if total_time > 0 else 0.0)
            with c_val:
                st.markdown(
                    f'<div class="mono" style="text-align:right; font-size:0.85rem;">{duration:.2f}s ({pct:.0f}%)</div>',
                    unsafe_allow_html=True
                )