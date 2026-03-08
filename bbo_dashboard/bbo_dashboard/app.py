"""
BBO Capstone — Interactive Dashboard
Mike Kennelly | Black-Box Optimisation Capstone
Run:  streamlit run app.py
"""
import streamlit as st

st.set_page_config(
    page_title="BBO Capstone Dashboard",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  [data-testid="stSidebar"] { background: #0d1117 !important; }
  [data-testid="stSidebar"] * { color: #c5cae9; }
  .stMetric label { color: #6b7a9a !important; font-size: 0.75rem !important; }
  .stMetric [data-testid="metric-container"] { background: #161b27; border-radius: 8px; padding: 10px 14px; }
  .metric-row { display: flex; gap: 12px; margin: 1rem 0; flex-wrap: wrap; }
  .metric-card { background: #1e2130; border-radius: 10px; padding: 14px 18px;
    border-left: 4px solid #4c9be8; flex: 1; min-width: 130px; }
  .metric-label { font-size: 0.68rem; color: #4a5570; text-transform: uppercase;
    letter-spacing: 0.1em; margin-bottom: 4px; }
  .metric-value { font-size: 1.35rem; font-weight: 700; color: #eef2ff; font-family: monospace; }
  .metric-sub   { font-size: 0.72rem; color: #4a5570; margin-top: 2px; }
  .section-header { font-size: 0.68rem; color: #3d9cf0; text-transform: uppercase;
    letter-spacing: 0.2em; margin: 1.2rem 0 0.5rem; }
  .page-header { font-size: 0.68rem; letter-spacing: 0.2em; color: #3d9cf0;
    text-transform: uppercase; margin-bottom: 1rem; }
  .page-title  { font-size: 2rem; font-weight: 700; color: #eef2ff; line-height: 1.2; margin-bottom: 0.5rem; }
  .page-subtitle { color: #6b7a9a; font-size: 0.9rem; margin-bottom: 1.5rem; }
  .strategy-badge { display: inline-block; padding: 4px 14px; border-radius: 14px;
    font-size: 0.8rem; font-weight: 600; margin-bottom: 0.8rem; }
  .badge-exploit { background: #1e3a5f; color: #60a5fa; }
  .badge-explore { background: #1a3d2b; color: #4ade80; }
  .badge-recover { background: #3d2a0a; color: #fbbf24; }
  .clf-pill { display: inline-block; padding: 5px 14px; border-radius: 14px;
    font-size: 0.85rem; font-weight: 600; margin-bottom: 0.5rem; }
  .clf-svm { background: #1e3a5f; color: #4c9be8; }
  .clf-rf  { background: #1a3d2b; color: #34d399; }
  .clf-nn  { background: #2d1b5e; color: #a78bfa; }
  .clf-cnn { background: #4a1942; color: #f472b6; }
  .clf-lr  { background: #3d2a0a; color: #f59e0b; }
  div[data-testid="stDataFrame"] { border-radius: 8px; }
  .stPlotlyChart { border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

from data import FUNCTIONS, SCORES, STRATEGY, CLASSIFIERS, W7_PRED, PIPELINE_STEPS, COORDS, WEEKS

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎯 BBO Capstone")
    st.markdown("<div style='color:#4a5570;font-size:0.78rem;margin-bottom:1.5rem'>"
                "Mike Kennelly &nbsp;·&nbsp; W1–W7</div>", unsafe_allow_html=True)

    page = st.radio(
        "NAVIGATE",
        ["🏠  Overview", "📊  Scores & Trajectory", "🧭  Strategy",
         "🤖  Classifiers", "⚙️  Pipeline", "📋  All Functions"],
        label_visibility="visible",
    )
    st.markdown("---")
    fn = st.selectbox("FUNCTION", list(FUNCTIONS.keys()), index=4)
    obj = FUNCTIONS[fn]["objective"]
    badge_color = "#22c55e" if obj == "MAXIMISE" else "#f472b6"
    st.markdown(
        f"<div style='font-size:0.78rem;color:#4a5570;margin-top:0.4rem'>"
        f"<b style='color:{badge_color}'>{obj}</b> &nbsp;·&nbsp; {FUNCTIONS[fn]['dims']}D</div>",
        unsafe_allow_html=True
    )
    st.markdown(f"<div style='font-size:0.75rem;color:#3d4a6a;margin-top:4px'>"
                f"{FUNCTIONS[fn]['desc']}</div>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("<div style='font-size:0.68rem;color:#3d4a6a'>W7 Notebooks on GitHub →<br>"
                "Streamlit Cloud auto-deploys on push</div>", unsafe_allow_html=True)

# ── Route ──────────────────────────────────────────────────────────────────────
if "Overview" in page:
    from pages.overview      import render; render(fn)
elif "Scores" in page:
    from pages.scores        import render; render(fn)
elif "Strategy" in page:
    from pages.strategy      import render; render(fn)
elif "Classifiers" in page:
    from pages.classifiers   import render; render(fn)
elif "Pipeline" in page:
    from pages.pipeline      import render; render(fn)
elif "All Functions" in page:
    from pages.all_functions import render; render()
