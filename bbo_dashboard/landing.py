import streamlit as st
import plotly.graph_objects as go
from data import FUNCTIONS, SCORES, STRATEGY, get_all_time_best, running_best

def build_sparkline(scores, maximize):
    bars = []
    for j, s in enumerate(scores):
        if s is None:
            color = "#1a2540"
        elif j == 0:
            color = "#4a5a7a"
        elif scores[j-1] is not None:
            color = "#22c55e" if ((maximize and s > scores[j-1]) or (not maximize and s < scores[j-1])) else "#ef4444"
        else:
            color = "#4a5a7a"
        bars.append(f"<div style='flex:1;height:4px;border-radius:2px;background:{color}'></div>")
    return "".join(bars)

def render():
    # ── Hero ──────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style='padding: 2rem 0 1rem'>
      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.68rem;color:#2563eb;
                  text-transform:uppercase;letter-spacing:0.3em;margin-bottom:12px'>
        Imperial College London · DATA 2026 Cohort
      </div>
      <div style='font-family:Syne,sans-serif;font-size:3.2rem;font-weight:800;
                  color:#e8eeff;line-height:1.1;margin-bottom:14px'>
        Black-Box<br>Optimisation<br><span style='color:#2563eb'>Capstone</span>
      </div>
      <div style='color:#4a5a7a;font-size:1rem;max-width:640px;line-height:1.7;margin-bottom:2rem'>
        A 7-week machine learning experiment in which an unknown black-box function
        must be maximised using only a small number of costly evaluations per week.
        No gradient information. No closed-form expression. Only the score returned
        after each submission.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Presented by ─────────────────────────────────────────────────────────
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#0d1320,#111827);border:1px solid #1a2540;
                    border-radius:12px;padding:20px 22px;border-top:2px solid #2563eb'>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;
                      text-transform:uppercase;letter-spacing:0.2em;margin-bottom:8px'>Presented by</div>
          <div style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:700;color:#e8eeff'>Mike Kennelly</div>
          <div style='font-size:0.78rem;color:#4a5a7a;margin-top:4px'>MSc Data Science</div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#0d1320,#111827);border:1px solid #1a2540;
                    border-radius:12px;padding:20px 22px;border-top:2px solid #6366f1'>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;
                      text-transform:uppercase;letter-spacing:0.2em;margin-bottom:8px'>Facilitated by</div>
          <div style='font-family:Syne,sans-serif;font-size:1.1rem;font-weight:700;color:#e8eeff'>Imperial College<br>London</div>
          <div style='font-size:0.78rem;color:#4a5a7a;margin-top:4px'>DATA 2026 · Module 17</div>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div style='background:linear-gradient(135deg,#0d1320,#111827);border:1px solid #1a2540;
                    border-radius:12px;padding:20px 22px;border-top:2px solid #10b981'>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;
                      text-transform:uppercase;letter-spacing:0.2em;margin-bottom:8px'>The Challenge</div>
          <div style='color:#8a9abf;font-size:0.88rem;line-height:1.7'>
            8 unknown functions · 2D to 8D search spaces · Up to 5 evaluations per week ·
            Gaussian Process surrogate model · Bayesian acquisition (EI + UCB) ·
            Adaptive classifier pipeline · CNN-1D filter inspection
          </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Function Overview — All 8 Functions · W1–W7</div>', unsafe_allow_html=True)

    # ── Function summary grid ─────────────────────────────────────────────────
    fns = list(FUNCTIONS.keys())
    cols = st.columns(4)
    for i, fn in enumerate(fns):
        info     = FUNCTIONS[fn]
        maximize = info["objective"] == "MAXIMISE"
        scores   = SCORES[fn]
        actuals  = [s for s in scores if s is not None]
        atb      = get_all_time_best(fn)
        strat    = STRATEGY[fn]

        def fmt(v):
            if v is None: return "—"
            if abs(v) >= 1000: return f"{v:,.0f}"
            if v != 0 and abs(v) < 0.001: return f"{v:.2e}"
            return f"{v:.4f}"

        action = strat["action"]
        if "EXPLORE" in action:   acolor, abg = "#34d399", "rgba(16,185,129,0.12)"
        elif "RECOVER" in action: acolor, abg = "#fbbf24", "rgba(245,158,11,0.12)"
        else:                     acolor, abg = "#60a5fa", "rgba(59,130,246,0.12)"

        w6_score = actuals[-1] if actuals else None
        improved = (w6_score == atb) if w6_score is not None else False

        with cols[i % 4]:
            st.markdown(f"""
            <div style='background:linear-gradient(160deg,#0a1020,#0d1525);
                        border:1px solid #141e30;border-radius:12px;padding:16px 18px;
                        margin-bottom:10px;position:relative;overflow:hidden'>
              <div style='position:absolute;top:0;left:0;right:0;height:2px;background:{acolor}'></div>
              <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:8px'>
                <div style='font-family:Syne,sans-serif;font-size:1.5rem;font-weight:800;color:#e8eeff'>{fn}</div>
                <div style='font-family:"IBM Plex Mono",monospace;font-size:0.65rem;
                            color:#2d3a52;background:#060a10;padding:3px 8px;border-radius:4px'>
                  {info["dims"]}D
                </div>
              </div>
              <div style='font-size:0.78rem;color:#4a5a7a;margin-bottom:10px;line-height:1.4'>{info["desc"][:60]}…</div>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
                <div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;margin-bottom:2px'>BEST SCORE</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:1rem;
                              font-weight:600;color:{"#34d399" if improved else "#e8eeff"}'>{fmt(atb)}</div>
                </div>
                <div style='text-align:right'>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;margin-bottom:2px'>W7 STRATEGY</div>
                  <div style='font-size:0.68rem;background:{abg};color:{acolor};
                              padding:2px 8px;border-radius:10px;font-weight:600'>{action.split()[0]}</div>
                </div>
              </div>
              <div style='display:flex;gap:3px;margin-top:8px'>
                {build_sparkline(scores, maximize)}
              </div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.55rem;color:#2d3a52;margin-top:3px'>
                W1 → W7 · green=improvement
              </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">How It Works</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    steps_text = [
        ("01 / Submit Coordinates", "#2563eb",
         "Each week, submit a point in [0,1]ⁿ to the black-box oracle. The oracle returns a scalar score — no gradient, no formula, no explanation."),
        ("02 / Build Surrogate", "#6366f1",
         "A Gaussian Process (Matérn 5/2) is fitted to all previous evaluations. It provides a probabilistic mean μ and uncertainty σ over the search space."),
        ("03 / Acquire & Decide", "#10b981",
         "Expected Improvement (EI) and UCB acquisition functions select the next point. An adaptive classifier pipeline (8 models) filters 10,000 candidates before GP."),
    ]
    for col, (title, color, body) in zip([c1, c2, c3], steps_text):
        with col:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #141e30;border-radius:12px;
                        padding:20px;border-top:2px solid {color};height:100%'>
              <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
                          color:{color};margin-bottom:10px'>{title}</div>
              <div style='color:#4a5a7a;font-size:0.86rem;line-height:1.7'>{body}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Navigate This Dashboard</div>', unsafe_allow_html=True)
    nav_items = [
        ("📊 All Functions", "#2563eb", "See all 8 functions side by side. Filter by week. Compare strategies, scores, and submission strings."),
        ("🔬 Weekly Analysis", "#6366f1", "Drill into any function × week. Hyperparameters, rationale, what was learned, CNN experiment notes."),
        ("📋 Source Code", "#10b981", "View the notebook source code structure for any function. See the pipeline step-by-step."),
        ("🏗️ Pipeline", "#f59e0b", "Full 13-step pipeline walkthrough. Visual flow diagram. Each step explained with purpose and method."),
    ]
    nav_cols = st.columns(4)
    for col, (title, color, desc) in zip(nav_cols, nav_items):
        with col:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;
                        padding:16px;border-left:3px solid {color}'>
              <div style='font-family:Syne,sans-serif;font-weight:700;color:{color};
                          margin-bottom:6px;font-size:0.95rem'>{title}</div>
              <div style='color:#4a5a7a;font-size:0.80rem;line-height:1.6'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
