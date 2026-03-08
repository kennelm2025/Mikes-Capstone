import streamlit as st
import plotly.graph_objects as go
from data import FUNCTIONS, SCORES, STRATEGY, running_best, get_all_time_best

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if abs(v) < 0.0001 and v != 0: return f"{v:.2e}"
    return f"{v:.4f}"

ACTION_COLOR = {
    "EXPLORE": "#10b981", "EXPLOIT": "#4c9be8", "RECOVER": "#f59e0b",
}

def action_color(action):
    for k, v in ACTION_COLOR.items():
        if k in action: return v
    return "#888"

def render(fn):
    info     = FUNCTIONS[fn]
    maximize = info["objective"] == "MAXIMISE"
    strat    = STRATEGY[fn]
    scores   = SCORES[fn]
    atb      = get_all_time_best(fn)
    actuals  = [s for s in scores if s is not None]
    rb       = running_best(scores, maximize)

    st.markdown(f"## 🧠 Strategy & Rationale — {fn}")
    st.caption(f"{info['dims']}D · {info['objective']} · {info['desc']}")

    # ── Strategy header card ──────────────────────────────────────────────────
    action  = strat["action"]
    acolor  = action_color(action)
    st.markdown(f"""
    <div style="background:#1a1f2e;border-radius:10px;padding:20px 24px;border-left:5px solid {acolor};margin-bottom:1.2rem">
      <div style="font-size:0.72rem;color:#4a5570;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:6px">W7 Strategy</div>
      <div style="font-size:1.5rem;font-weight:700;color:{acolor};margin-bottom:10px">{action}</div>
      <div style="color:#9aa4c0;line-height:1.75;font-size:0.95rem">{strat['rationale']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Two column: hyper params + pattern ───────────────────────────────────
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("#### ⚙️ W7 Hyperparameters")
        params = [
            ("Exploit Ratio",  f"{strat['exploit_ratio']:.0%}",  "% of candidates from exploit distribution"),
            ("Sigma (σ)",       f"{strat['sigma']:.4f}",          "Gaussian spread around best point"),
            ("UCB κ",           f"{strat.get('ucb_kappa',2.0)}",  "Optimism parameter in UCB acquisition"),
            ("GP Restarts",     f"{strat.get('gp_restarts',5)}",  "GP hyperparameter optimisation restarts"),
        ]
        for label, val, tip in params:
            st.markdown(f"""
            <div style="display:flex;justify-content:space-between;align-items:center;
                        padding:8px 14px;background:#13182a;border-radius:6px;margin:4px 0">
              <div>
                <div style="color:#c5cae9;font-size:0.88rem;font-weight:600">{label}</div>
                <div style="color:#4a5570;font-size:0.7rem">{tip}</div>
              </div>
              <div style="color:{acolor};font-size:1.1rem;font-weight:700;font-family:monospace">{val}</div>
            </div>
            """, unsafe_allow_html=True)

    with col2:
        st.markdown("#### 🔍 Observed Pattern")
        st.markdown(f"""
        <div style="background:#13182a;border-radius:10px;padding:18px 20px">
          <div style="color:#4a5570;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px">Best Point Identified</div>
          <div style="color:#22c55e;font-size:1rem;font-weight:600;margin-bottom:10px">{strat['best_week']}</div>
          <div style="color:#4a5570;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em;margin-bottom:8px">Coordinate Pattern</div>
          <div style="color:#c5cae9;font-size:0.88rem;line-height:1.6">{strat['pattern']}</div>
          <div style="margin-top:14px;color:#4a5570;font-size:0.72rem;text-transform:uppercase;letter-spacing:0.1em">All-Time Best Score</div>
          <div style="color:#f59e0b;font-size:1.2rem;font-weight:700;font-family:monospace">{fmt(atb)}</div>
        </div>
        """, unsafe_allow_html=True)

    st.divider()

    # ── All-functions strategy comparison ─────────────────────────────────────
    st.markdown("### 📋 Strategy Comparison — All Functions")

    col_labels = ["Function", "Dims", "Objective", "W7 Action", "Exploit %", "σ", "UCB κ", "Best Week", "Pattern"]
    rows = []
    for fid, info2 in FUNCTIONS.items():
        s = STRATEGY[fid]
        rows.append([
            fid,
            f"{info2['dims']}D",
            "MAX ▲" if info2["objective"] == "MAXIMISE" else "MIN ▼",
            s["action"],
            f"{s['exploit_ratio']:.0%}",
            f"{s['sigma']:.4f}",
            f"{s.get('ucb_kappa',2.0)}",
            s["best_week"],
            s["pattern"],
        ])
    import pandas as pd
    df = pd.DataFrame(rows, columns=col_labels).set_index("Function")
    st.dataframe(df, use_container_width=True, height=330)

    st.divider()

    # ── Exploit ratio vs sigma scatter ────────────────────────────────────────
    st.markdown("### 📐 Exploit Ratio vs σ — Design Space")
    fns   = list(FUNCTIONS.keys())
    ratios = [STRATEGY[f]["exploit_ratio"] for f in fns]
    sigmas = [STRATEGY[f]["sigma"] for f in fns]
    actions_txt = [STRATEGY[f]["action"] for f in fns]
    colors_pts  = [action_color(a) for a in actions_txt]

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=ratios, y=sigmas,
        mode="markers+text",
        text=fns, textposition="top center",
        textfont=dict(size=12, color="white"),
        marker=dict(size=18, color=colors_pts, line=dict(color="white", width=1.5)),
        hovertemplate="<b>%{text}</b><br>Exploit: %{x:.0%}<br>σ: %{y:.4f}<extra></extra>",
    ))
    fig.update_layout(
        height=360, paper_bgcolor="#0f1117", plot_bgcolor="#161b27",
        font=dict(color="#c5cae9"),
        xaxis=dict(title="Exploit Ratio", tickformat=".0%", gridcolor="#1e2535", range=[0.3, 1.0]),
        yaxis=dict(title="Sigma (σ)", gridcolor="#1e2535"),
        margin=dict(l=40, r=20, t=20, b=60),
        annotations=[
            dict(x=0.35, y=0.21, text="← More EXPLORE", showarrow=False, font=dict(color="#10b981", size=11)),
            dict(x=0.93, y=0.01, text="More EXPLOIT →", showarrow=False, font=dict(color="#4c9be8", size=11)),
        ]
    )
    col1, col2 = st.columns([3,1])
    with col1:
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown("**Reading this chart:**")
        st.markdown("""
- **Top-left**: Wide explore, high σ → broad search
- **Bottom-right**: Tight exploit, low σ → local refinement
- **Circle colour**: green=EXPLORE, blue=EXPLOIT, amber=RECOVER
        """)
