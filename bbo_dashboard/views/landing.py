import streamlit as st
import plotly.graph_objects as go
from data import FUNCTIONS, SCORES, STRATEGY, CURRENT_WEEK, get_all_time_best, running_best

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

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.0f}"
    if v != 0 and abs(v) < 0.001: return f"{v:.2e}"
    return f"{v:.4f}"

def render():
    # ── Full-width Hero ───────────────────────────────────────────────────────
    st.markdown("""
    <style>
    .hero-wrap {
        width: 100%;
        padding: 2.8rem 0 2rem;
        border-bottom: 1px solid #111827;
        margin-bottom: 2rem;
    }
    .hero-eyebrow {
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.68rem;
        color: #2563eb;
        text-transform: uppercase;
        letter-spacing: 0.35em;
        margin-bottom: 16px;
    }
    .hero-title {
        font-family: Syne, sans-serif;
        font-size: clamp(2.2rem, 4vw, 3.6rem);
        font-weight: 800;
        color: #e8eeff;
        line-height: 1.05;
        white-space: normal;
        margin-bottom: 20px;
        letter-spacing: -0.01em;
        max-width: 100%;
    }
    .hero-title span { color: #2563eb; }
    .hero-subtitle-row {
        display: flex;
        align-items: center;
        gap: 20px;
        flex-wrap: wrap;
        margin-bottom: 18px;
    }
    .hero-divider { width: 1px; height: 32px; background: #1a2540; }
    .hero-name {
        font-family: Syne, sans-serif;
        font-size: 1.05rem;
        font-weight: 700;
        color: #e8eeff;
    }
    .hero-name-sub {
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.65rem;
        color: #4a5a7a;
        margin-top: 2px;
    }
    .imperial-logo {
        display: flex;
        align-items: center;
        gap: 10px;
        background: rgba(255,255,255,0.03);
        border: 1px solid #1a2540;
        border-radius: 8px;
        padding: 8px 14px;
    }
    .imperial-crest {
        font-size: 1.6rem;
        line-height: 1;
    }
    .imperial-text-block { display: flex; flex-direction: column; }
    .imperial-name {
        font-family: Syne, sans-serif;
        font-size: 0.88rem;
        font-weight: 700;
        color: #e8eeff;
        line-height: 1.2;
    }
    .imperial-sub {
        font-family: "IBM Plex Mono", monospace;
        font-size: 0.60rem;
        color: #4a5a7a;
        margin-top: 1px;
    }
    .hero-desc {
        color: #8a9abf;
        font-size: 1.05rem;
        max-width: 100%;
        line-height: 1.8;
    }
    </style>

    <div class="hero-wrap">
        <div class="hero-eyebrow">Capstone Project · Imperial College London · Data Oct 2025 – May 2026 Cohort</div>
        <div class="hero-title">Black-Box Optimisation<br><span style='color:#2563eb'>Capstone</span></div>
        <div class="hero-subtitle-row">
            <div style="font-family:Syne,sans-serif;font-size:1.05rem;font-weight:700;color:#e8eeff">
                Presented by Mike Kennelly · Professional Certificate in ML & AI
            </div>
        </div>
        <div class="hero-desc">
            The Capstone is a 13-week Black-Box Optimisation challenge. Each week we receive
            an additional data point across 8 unknown functions — our goal is to predict the
            global maximum of each. Weekly learnings, strategies and notebooks are published
            to our GitHub repo, with predictions submitted to the Capstone console where
            results are scored and new data points unlocked for the following week.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Function graphs — 2 per row, enlarged ─────────────────────────────────
    st.markdown(f'<div class="sec-head">Function Overview — All 8 Functions · W1–W{CURRENT_WEEK} Trajectories</div>', unsafe_allow_html=True)

    fns = list(FUNCTIONS.keys())

    for row_start in range(0, 8, 2):
        pair = fns[row_start:row_start+2]
        cols = st.columns(2)

        for col_idx, fn in enumerate(pair):
            info     = FUNCTIONS[fn]
            maximize = info["objective"] == "MAXIMISE"
            scores   = SCORES[fn]
            actuals  = [s for s in scores if s is not None]
            atb      = get_all_time_best(fn)
            strat    = STRATEGY[fn]
            action   = strat["action"]

            if "EXPLORE" in action:   acolor, abg = "#34d399", "rgba(16,185,129,0.12)"
            elif "RECOVER" in action: acolor, abg = "#fbbf24", "rgba(245,158,11,0.12)"
            else:                     acolor, abg = "#60a5fa", "rgba(59,130,246,0.12)"

            rb = running_best(scores, maximize)
            rb_vals = [r for r in rb if r is not None][:len(actuals)]
            week_labels = [f"W{i+1}" for i in range(len(actuals))]

            bar_colors = ["#4a5a7a"]
            for i in range(1, len(actuals)):
                imp = (actuals[i] > actuals[i-1]) if maximize else (actuals[i] < actuals[i-1])
                bar_colors.append("#22c55e" if imp else "#ef4444")

            # Highlight best week
            best_val = max(actuals) if maximize else min(actuals)
            best_idx_local = actuals.index(best_val)
            bar_colors[best_idx_local] = "#f59e0b"

            w7_score = actuals[-1] if actuals else None
            is_best = (w7_score == atb) if w7_score is not None else False

            with cols[col_idx]:
                # Card header
                st.markdown(f"""
                <div style='background:linear-gradient(160deg,#0a1020,#0d1525);
                            border:1px solid #141e30;border-radius:14px;
                            padding:20px 22px 6px;margin-bottom:0;
                            border-top:3px solid {acolor};position:relative'>
                  <div style='display:flex;justify-content:space-between;align-items:flex-start;margin-bottom:4px'>
                    <div>
                      <span style='font-family:Syne,sans-serif;font-size:2rem;font-weight:800;color:#e8eeff'>{fn}</span>
                      <span style='font-family:"IBM Plex Mono",monospace;font-size:0.72rem;
                                  color:#2d3a52;margin-left:10px'>{info["dims"]}D · {info["objective"]}</span>
                    </div>
                    <div style='font-size:0.68rem;background:{abg};color:{acolor};
                                padding:4px 12px;border-radius:12px;font-weight:600;
                                font-family:"IBM Plex Mono",monospace;margin-top:4px'>
                      {action.split()[0]}
                    </div>
                  </div>
                  <div style='font-size:0.88rem;color:#4a5a7a;margin-bottom:10px;line-height:1.5'>{info["desc"]}</div>
                  <div style='display:flex;gap:24px;margin-bottom:12px'>
                    <div>
                      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;margin-bottom:2px'>ALL-TIME BEST</div>
                      <div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;font-weight:700;color:#f59e0b'>★ {fmt(atb)}</div>
                    </div>
                    <div>
                      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;margin-bottom:2px'>' + f'W{CURRENT_WEEK}' + ' SCORE</div>
                      <div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;font-weight:700;
                                  color:{"#34d399" if is_best else "#e8eeff"}'>{fmt(w7_score)}</div>
                    </div>
                    <div>
                      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#2d3a52;margin-bottom:2px'>DIMS</div>
                      <div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;font-weight:700;color:#e8eeff'>{info["dims"]}D</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

                # Trajectory chart — enlarged
                fig = go.Figure()
                fig.add_trace(go.Bar(
                    x=week_labels, y=actuals,
                    marker_color=bar_colors,
                    marker_line_width=0,
                    opacity=0.9,
                    name="Score",
                    text=[fmt(v) for v in actuals],
                    textposition="outside",
                    textfont=dict(size=11, color="white", family="IBM Plex Mono"),
                    hovertemplate="%{x}: <b>%{y:.4g}</b><extra></extra>",
                ))
                fig.add_trace(go.Scatter(
                    x=week_labels, y=rb_vals,
                    mode="lines+markers",
                    line=dict(color="#f59e0b", width=2.5, dash="dash"),
                    marker=dict(size=7, color="#f59e0b"),
                    name="Running best",
                ))
                fig.update_layout(
                    paper_bgcolor="#0a1020",
                    plot_bgcolor="#0a1020",
                    font=dict(color="#4a5a7a", family="IBM Plex Mono"),
                    height=320,
                    margin=dict(l=10, r=10, t=20, b=10),
                    showlegend=True,
                    legend=dict(
                        bgcolor="rgba(0,0,0,0)",
                        font=dict(size=10, color="#4a5a7a"),
                        orientation="h",
                        yanchor="bottom", y=1.01,
                        xanchor="right", x=1,
                    ),
                    xaxis=dict(gridcolor="#0d1320", showgrid=False,
                               tickfont=dict(size=11, color="#4a5a7a")),
                    yaxis=dict(gridcolor="#111827", showgrid=True,
                               gridwidth=0.5, tickfont=dict(size=10, color="#4a5a7a")),
                )
                st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

                # Sparkline + bottom strip
                st.markdown(f"""
                <div style='background:#060a10;border:1px solid #0d1320;border-radius:0 0 14px 14px;
                            padding:10px 22px 14px;margin-top:-8px;border-top:none'>
                  <div style='display:flex;gap:3px;margin-bottom:4px'>
                    {build_sparkline(scores, maximize)}
                  </div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.55rem;color:#2d3a52'>
                    W1 → ' + str(CURRENT_WEEK) + ' · green=improvement · gold=all-time best
                  </div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<div style='margin-bottom:12px'></div>", unsafe_allow_html=True)

    # ── How It Works ──────────────────────────────────────────────────────────
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
                        padding:20px;border-top:2px solid {color}'>
              <div style='font-family:Syne,sans-serif;font-size:1rem;font-weight:700;
                          color:{color};margin-bottom:10px'>{title}</div>
              <div style='color:#8a9abf;font-size:0.95rem;line-height:1.75'>{body}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Navigate ──────────────────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Navigate This Dashboard</div>', unsafe_allow_html=True)
    nav_items = [
        ("📊 All Functions", "#2563eb", "Side-by-side comparison. Filter by week. Compare strategies, scores, and submission strings."),
        ("🔬 Weekly Analysis", "#6366f1", "Drill into any function × week. Hyperparameters, rationale, CNN experiment notes."),
        ("📋 Source Code", "#10b981", "View the notebook source for any function. See the pipeline step-by-step."),
        ("🏗️ Pipeline", "#f59e0b", "Full 13-step pipeline walkthrough. Visual flow. Each step explained."),
    ]
    nav_cols = st.columns(4)
    for col, (title, color, desc) in zip(nav_cols, nav_items):
        with col:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;
                        padding:16px;border-left:3px solid {color}'>
              <div style='font-family:Syne,sans-serif;font-weight:700;color:{color};
                          margin-bottom:6px;font-size:0.95rem'>{title}</div>
              <div style='color:#8a9abf;font-size:0.88rem;line-height:1.6'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)
