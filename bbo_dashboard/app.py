"""
BBO Capstone — Interactive Dashboard
Mike Kennelly | Black-Box Optimisation Capstone | Imperial College London / DATA 2026
"""
import sys, os
_here = os.path.dirname(os.path.abspath(__file__))
if _here not in sys.path:
    sys.path.insert(0, _here)

import streamlit as st

st.set_page_config(
    page_title="BBO Capstone · Mike Kennelly",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("""
<style>
  @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@300;400;500&display=swap');

  html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
  h1,h2,h3,h4 { font-family: 'Syne', sans-serif !important; }

  /* Sidebar */
  [data-testid="stSidebar"] {
    background: #080c14 !important;
    border-right: 1px solid #111827;
  }
  [data-testid="stSidebar"] * { color: #c8d4f0 !important; }
  [data-testid="stSidebar"] .stSelectbox label,
  [data-testid="stSidebar"] .stRadio label { color: #7a8fbb !important; font-size: 0.65rem !important;
    text-transform: uppercase; letter-spacing: 0.15em; }

  /* Main bg */
  .stApp { background: #060a10; }
  .main .block-container { padding: 1.5rem 2rem 3rem; max-width: 1400px; }

  /* Metric cards */
  .kpi-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(160px, 1fr)); gap: 12px; margin: 1rem 0 1.5rem; }
  .kpi-card {
    background: linear-gradient(135deg, #0d1320 0%, #111827 100%);
    border: 1px solid #1a2540;
    border-radius: 12px;
    padding: 16px 20px;
    position: relative;
    overflow: hidden;
  }
  .kpi-card::before {
    content: ''; position: absolute; top: 0; left: 0; right: 0; height: 2px;
    background: var(--accent, #3b82f6);
  }
  .kpi-label { font-size: 0.62rem; color: #6070a0; text-transform: uppercase; letter-spacing: 0.18em; margin-bottom: 6px; font-family: 'IBM Plex Mono', monospace; }
  .kpi-value { font-size: 1.4rem; font-weight: 700; color: #e8eeff; font-family: 'IBM Plex Mono', monospace; line-height: 1.1; }
  .kpi-sub   { font-size: 0.7rem; color: #6070a0; margin-top: 4px; }

  /* Section headers */
  .sec-head {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.62rem; color: #38bdf8; text-transform: uppercase;
    letter-spacing: 0.25em; margin: 1.8rem 0 0.6rem;
    display: flex; align-items: center; gap: 8px;
  }
  .sec-head::after { content: ''; flex: 1; height: 1px; background: #1e2d45; }

  /* Strategy badge */
  .badge {
    display: inline-block; padding: 5px 16px; border-radius: 20px;
    font-family: 'IBM Plex Mono', monospace; font-size: 0.78rem; font-weight: 500;
    letter-spacing: 0.05em; margin-bottom: 1rem;
  }
  .badge-exploit { background: rgba(59,130,246,0.15); color: #60a5fa; border: 1px solid rgba(59,130,246,0.3); }
  .badge-explore { background: rgba(16,185,129,0.15); color: #34d399; border: 1px solid rgba(16,185,129,0.3); }
  .badge-recover { background: rgba(245,158,11,0.15); color: #fbbf24; border: 1px solid rgba(245,158,11,0.3); }

  /* Week selector tabs */
  .week-tabs { display: flex; gap: 6px; margin: 0.8rem 0 1.2rem; flex-wrap: wrap; }
  .wtab {
    padding: 5px 14px; border-radius: 8px; font-family: 'IBM Plex Mono', monospace;
    font-size: 0.75rem; cursor: pointer; border: 1px solid #1a2540;
    background: #0d1320; color: #7a8fbb; text-decoration: none;
  }
  .wtab-active { background: #1e3a6e; color: #93c5fd; border-color: #2563eb; }

  /* Submission string */
  .sub-box {
    background: #050810; border: 1px solid #1a2540; border-left: 3px solid #22c55e;
    border-radius: 0 8px 8px 0; padding: 10px 16px; font-family: 'IBM Plex Mono', monospace;
    font-size: 0.88rem; color: #4ade80; margin: 0.8rem 0; word-break: break-all;
  }
  .sub-label { font-size: 0.60rem; color: #2d4a2d; text-transform: uppercase; letter-spacing: 0.15em; margin-bottom: 4px; }

  /* Info cards */
  .info-card {
    background: #0a1020; border: 1px solid #141e30; border-radius: 10px;
    padding: 18px 20px; margin: 8px 0; line-height: 1.75;
  }
  .info-card-title { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem;
    color: #38bdf8; text-transform: uppercase; letter-spacing: 0.18em; margin-bottom: 8px; }
  .info-card-body { color: #c8d4f0; font-size: 0.88rem; }

  /* Param row */
  .param-row { display: flex; justify-content: space-between; align-items: center;
    padding: 9px 14px; background: #080e1a; border-radius: 6px; margin: 4px 0; }
  .param-name { color: #7a8fbb; font-family: 'IBM Plex Mono', monospace; font-size: 0.72rem; }
  .param-val  { color: #e8eeff; font-family: 'IBM Plex Mono', monospace; font-size: 0.88rem; font-weight: 500; }

  /* Page hero */
  .page-hero { margin-bottom: 1.5rem; }
  .page-eyebrow { font-family: 'IBM Plex Mono', monospace; font-size: 0.62rem;
    color: #38bdf8; text-transform: uppercase; letter-spacing: 0.25em; margin-bottom: 6px; }
  .page-title { font-family: 'Syne', sans-serif; font-size: 2.2rem; font-weight: 800;
    color: #e8eeff; line-height: 1.15; margin-bottom: 6px; }
  .page-sub { color: #7a8fbb; font-size: 0.88rem; }

  /* Sidebar nav labels */
  .nav-section { font-family: 'IBM Plex Mono', monospace; font-size: 0.58rem;
    color: #5a6a8a !important; text-transform: uppercase; letter-spacing: 0.2em;
    margin: 1.2rem 0 0.4rem; padding-bottom: 4px; border-bottom: 1px solid #111827; }

  /* Source code viewer */
  .source-block { background: #050810; border: 1px solid #141e30; border-radius: 8px;
    padding: 16px; font-family: 'IBM Plex Mono', monospace; font-size: 0.75rem;
    color: #c8d4f0; overflow-x: auto; white-space: pre; line-height: 1.6; }

  div[data-testid="stDataFrame"] { border-radius: 8px; }
  .stPlotlyChart { border-radius: 10px; overflow: hidden; }
  [data-testid="stExpander"] { background: #0a1020 !important; border: 1px solid #141e30 !important; border-radius: 10px !important; }
</style>
""", unsafe_allow_html=True)

from data import FUNCTIONS, SCORES, STRATEGY, CLASSIFIERS, W7_PRED, PIPELINE_STEPS, COORDS, WEEKS, WEEKLY, W7_GLANCE, TURBO_SUMMARY, CURRENT_WEEK, running_best, get_all_time_best, get_sigma_display

# ── Import all views at module level (avoids Streamlit import-cache routing bug)
import views.landing      as _v_landing
import views.all_functions as _v_all
import views.weekly        as _v_weekly
import views.source_view   as _v_source
import views.pipeline      as _v_pipeline

# ── Session state defaults ──────────────────────────────────────────────────────
if "page" not in st.session_state:
    st.session_state["page"] = "🏠  Home"
if "fn" not in st.session_state:
    st.session_state["fn"] = list(FUNCTIONS.keys())[4]
if "wk_idx" not in st.session_state:
    st.session_state["wk_idx"] = CURRENT_WEEK - 1

# ── Sidebar ─────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='padding: 0.5rem 0 1rem'>
      <div style='font-family:Syne,sans-serif;font-size:1.2rem;font-weight:800;color:#e8eeff'>🎯 BBO Capstone</div>
      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.65rem;color:#5a6a8a;margin-top:2px'>MIKE KENNELLY · DATA 2026</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="nav-section">Navigate</div>', unsafe_allow_html=True)

    PAGE_OPTIONS = ["🏠  Home", "📊  All Functions", "🔬  Weekly Analysis", "📋  Source Code", "🏗️  Pipeline"]
    page = st.radio(
        "page",
        PAGE_OPTIONS,
        index=PAGE_OPTIONS.index(st.session_state["page"]),
        label_visibility="collapsed",
        key="page_radio",
    )
    st.session_state["page"] = page

    # Only show data selectors when not on Home page
    if "Home" not in page:
        st.markdown('<div class="nav-section">Select Data</div>', unsafe_allow_html=True)

    if "All Functions" in page:
        fn = "ALL"
        wk_idx = st.selectbox(
            "Week",
            list(range(CURRENT_WEEK)),
            index=CURRENT_WEEK - 1,
            format_func=lambda i: f"W{i+1} — Week {i+1}",
            key="wk_all",
        )
        st.session_state["wk_idx"] = wk_idx
        st.markdown(f"""
        <div style='background:#0a1020;border-radius:8px;padding:10px 12px;margin-top:8px;
                    font-family:"IBM Plex Mono",monospace;font-size:0.70rem;color:#38bdf8'>
          All 8 functions · All weeks available
        </div>""", unsafe_allow_html=True)
    elif "Home" not in page:
        fn_list = list(FUNCTIONS.keys())
        fn = st.selectbox(
            "Function",
            fn_list,
            index=fn_list.index(st.session_state["fn"]) if st.session_state["fn"] in fn_list else 4,
            format_func=lambda f: f"{f} — {FUNCTIONS[f]['dims']}D",
            key="fn_select",
        )
        st.session_state["fn"] = fn

        wk_idx = st.selectbox(
            "Week",
            list(range(CURRENT_WEEK)),
            index=min(st.session_state["wk_idx"], CURRENT_WEEK - 1),
            format_func=lambda i: f"W{i+1}",
            key="wk_select",
        )

        maximize = FUNCTIONS[fn]["objective"] == "MAXIMISE"
        scores   = SCORES[fn]
        actuals  = [s for s in scores if s is not None]
        n_actual = len(actuals)
        # Allow selecting up to CURRENT_WEEK-1 (latest week, even if pending)
        # Don't cap to n_actual-1 — that silently shows W8 when W9 is selected
        wk_idx   = min(wk_idx, CURRENT_WEEK - 1)
        st.session_state["wk_idx"] = wk_idx

        score_this_wk = scores[wk_idx] if wk_idx < len(scores) else None
        def fmt_s(v):
            if v is None: return "—"
            if abs(v) >= 1000: return f"{v:,.0f}"
            if v != 0 and abs(v) < 0.001: return f"{v:.2e}"
            return f"{v:.4f}"

        obj_col = "#34d399" if maximize else "#f472b6"
        st.markdown(f"""
        <div style='background:#0a1020;border:1px solid #141e30;border-radius:8px;
                    padding:12px 14px;margin-top:8px'>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;
                      color:#5a6a8a;text-transform:uppercase;letter-spacing:0.15em'>
            {fn} · W{wk_idx+1} Score
          </div>
          <div style='font-size:1.3rem;font-weight:700;color:#e8eeff;
                      font-family:"IBM Plex Mono",monospace;margin:4px 0'>
            {fmt_s(score_this_wk)}
          </div>
          <div style='font-size:0.68rem;color:{obj_col}'>{FUNCTIONS[fn]["objective"]} · {FUNCTIONS[fn]["dims"]}D</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown(f"<div style='font-size:0.63rem;color:#5a6a8a;font-family:IBM Plex Mono,monospace'>Imperial College London<br>DATA 2026 Cohort<br>W1–W{CURRENT_WEEK} · BBO Optimisation</div>", unsafe_allow_html=True)

# ── Route ────────────────────────────────────────────────────────────────────────
page = st.session_state["page"]
fn     = st.session_state["fn"]
wk_idx = st.session_state["wk_idx"]

if "Home" in page:
    _v_landing.render()
elif "All Functions" in page:
    _v_all.render(wk_idx)
elif "Weekly Analysis" in page:
    _v_weekly.render(fn, wk_idx)
elif "Source Code" in page:
    _v_source.render(fn, wk_idx)
elif "Pipeline" in page:
    _v_pipeline.render(fn)
