import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from data import FUNCTIONS, SCORES, W7_PRED, STRATEGY, COORDS, running_best, get_all_time_best

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if abs(v) < 0.0001 and v != 0: return f"{v:.2e}"
    return f"{v:.4f}"

def render(fn):
    info     = FUNCTIONS[fn]
    maximize = info["objective"] == "MAXIMISE"
    scores   = SCORES[fn]
    pred     = W7_PRED[fn]
    strat    = STRATEGY[fn]
    atb      = get_all_time_best(fn)
    actuals  = [s for s in scores if s is not None]

    st.markdown(f"## 🔮 GP Predictions (W7) — {fn}")
    st.caption(f"Gaussian Process predicted outcome for Week 7 submission. "
               f"UCB = μ + {strat.get('ucb_kappa',2.0)}σ is the optimistic upper bound used as the W7 prediction bar.")

    # ── GP metrics ────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("GP μ",      fmt(pred["mu"]),    "Mean prediction")
    c2.metric("GP σ",      fmt(pred["sigma"]), "Uncertainty")
    c3.metric("GP UCB",    fmt(pred["ucb"]),   f"μ + {strat.get('ucb_kappa',2.0)}σ")
    delta_best = pred["mu"] - atb
    sign = "+" if delta_best >= 0 else ""
    c4.metric("Δ vs Best", f"{sign}{fmt(delta_best)}", "GP μ minus all-time best")
    c5.metric("All-time Best", fmt(atb), strat["best_week"])

    st.divider()

    # ── Main prediction chart with uncertainty ────────────────────────────────
    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown("### Week-on-Week + W7 GP Prediction")
        week_labels = [f"W{i+1}" for i in range(len(actuals))]
        bar_colors  = ["#6b7a9a"]
        for i in range(1, len(actuals)):
            improved = (actuals[i] > actuals[i-1]) if maximize else (actuals[i] < actuals[i-1])
            bar_colors.append("#22c55e" if improved else "#ef4444")

        rb      = running_best(scores, maximize)
        rb_vals = [r for r in rb if r is not None]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=week_labels, y=actuals,
            marker_color=bar_colors, marker_line_width=0,
            opacity=0.85, name="Actual Score",
            text=[fmt(v) for v in actuals],
            textposition="outside", textfont=dict(size=10, color="white"),
        ))
        fig.add_trace(go.Scatter(
            x=week_labels, y=rb_vals,
            mode="lines", line=dict(color="#f59e0b", width=2.5, dash="dash"),
            name="Running Best",
        ))
        # W7 UCB bar
        fig.add_trace(go.Bar(
            x=["W7 (pred)"], y=[pred["ucb"]],
            marker_color="rgba(129,140,248,0.4)",
            marker_line=dict(color="#818cf8", width=2),
            marker_pattern_shape="/",
            name=f"W7 UCB = {fmt(pred['ucb'])}",
            text=[f"UCB={fmt(pred['ucb'])}"],
            textposition="outside", textfont=dict(size=10, color="#a78bfa"),
        ))
        # GP μ with ±2σ error bar
        fig.add_trace(go.Scatter(
            x=["W7 (pred)"], y=[pred["mu"]],
            mode="markers",
            marker=dict(symbol="diamond", size=14, color="#818cf8",
                        line=dict(color="white", width=2)),
            error_y=dict(type="data", array=[2*pred["sigma"]],
                         color="#818cf8", thickness=2, width=12),
            name=f"GP μ±2σ",
            hovertemplate=f"GP μ: {fmt(pred['mu'])} ± 2σ = {fmt(2*pred['sigma'])}<extra></extra>",
        ))
        fig.add_hline(y=atb, line_dash="dot", line_color="#f87171", line_width=1.5,
                      annotation_text=f"All-time best: {fmt(atb)}",
                      annotation_font_color="#f87171", annotation_position="right")

        fig.update_layout(
            height=400, paper_bgcolor="#0f1117", plot_bgcolor="#161b27",
            font=dict(color="#c5cae9"), barmode="group",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(gridcolor="#1e2535"),
            yaxis=dict(gridcolor="#1e2535", title="Function Value"),
            margin=dict(l=10, r=20, t=60, b=40),
        )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.markdown("### EI Decomposition")
        st.markdown("""
**Why GP μ can be below the all-time best — and that's fine:**

EI (Expected Improvement) does **not** select the point with the highest GP mean.
It selects the point that maximises:

```
EI(x) = (μ - y_best) · Φ(Z)
       + σ · φ(Z)
```

Where `Z = (μ - y_best) / σ`.

The second term `σ · φ(Z)` is the **exploration bonus** — a point with high uncertainty 
can score high EI even if its mean is below the current best. This is the explore/exploit 
balance working as intended.

**UCB vs μ as prediction:**
- **GP μ** = what the GP expects at that point
- **UCB** = μ + κσ = optimistic upper bound (what the function *could* be)

The W7 bar shows **UCB** as the "prediction" because it captures the GP's belief 
about the potential upside, not just the mean.
        """)

        st.markdown("### GP Parameters")
        st.markdown(f"""
| Parameter | Value |
|---|---|
| Kernel | Matérn 5/2 + WhiteKernel |
| GP Restarts | {strat.get('gp_restarts', 5)} |
| UCB κ | {strat.get('ucb_kappa', 2.0)} |
| Exploit σ | {strat['sigma']} |
| EI ξ (jitter) | 0.01 |
        """)

    st.divider()

    # ── All-functions GP prediction overview ──────────────────────────────────
    st.markdown("### 🌐 All Functions — W7 GP Predictions vs All-Time Best")

    fns_list  = list(FUNCTIONS.keys())
    atbs      = [get_all_time_best(f) for f in fns_list]
    mus       = [W7_PRED[f]["mu"]  for f in fns_list]
    ucbs      = [W7_PRED[f]["ucb"] for f in fns_list]
    sigmas_2  = [2 * W7_PRED[f]["sigma"] for f in fns_list]

    fig2 = go.Figure()
    fig2.add_trace(go.Bar(
        name="All-Time Best", x=fns_list, y=atbs,
        marker_color="#f59e0b", marker_line_width=0, opacity=0.7,
        hovertemplate="<b>%{x}</b><br>All-time best: %{y:.4g}<extra></extra>",
    ))
    fig2.add_trace(go.Scatter(
        name="GP UCB (W7)", x=fns_list, y=ucbs,
        mode="markers+lines",
        marker=dict(symbol="diamond", size=12, color="#818cf8", line=dict(color="white", width=1.5)),
        line=dict(color="#818cf8", width=1.5, dash="dot"),
        error_y=dict(type="data", array=sigmas_2, color="#818cf8", thickness=1.5, width=6),
        hovertemplate="<b>%{x}</b><br>UCB: %{y:.4g}<extra></extra>",
    ))
    fig2.update_layout(
        height=350, paper_bgcolor="#0f1117", plot_bgcolor="#161b27",
        font=dict(color="#c5cae9"), barmode="overlay",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#1e2535"),
        yaxis=dict(gridcolor="#1e2535", title="Function Value"),
        margin=dict(l=10, r=10, t=60, b=40),
    )
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Bar = all-time best score. Diamond = W7 GP UCB (optimistic prediction). "
               "UCB above the bar suggests the GP sees potential for a new record.")
