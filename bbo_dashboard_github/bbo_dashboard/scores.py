import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import FUNCTIONS, SCORES, W7_PRED, COORDS, STRATEGY, W7_GLANCE, running_best, get_all_time_best, WEEKS, get_sigma_display

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if abs(v) < 0.0001 and v != 0: return f"{v:.2e}"
    return f"{v:.4f}"

def render(fn):
    info     = FUNCTIONS[fn]
    maximize = info["objective"] == "MAXIMISE"
    scores   = SCORES[fn]
    strat    = STRATEGY[fn]
    pred     = W7_PRED[fn]
    atb      = get_all_time_best(fn)
    actuals  = [s for s in scores if s is not None]
    rb       = running_best(scores, maximize)

    st.markdown(f"## 📊 Scores & Trajectory — {fn}")
    st.caption(f"{info['dims']}D · {info['objective']} · {info['desc']}")

    # ── KPI row ───────────────────────────────────────────────────────────────
    c1,c2,c3,c4,c5 = st.columns(5)
    c1.metric("All-Time Best",  fmt(atb),          strat["best_week"])
    c2.metric("W1 Score",       fmt(scores[0]),     "Starting point")
    c3.metric("W6 Score",       fmt(scores[5]),     "Last submitted")
    c4.metric("GP μ (W7)",      fmt(pred["mu"]),    "GP mean")
    c5.metric("GP UCB (W7)",    fmt(pred["ucb"]),   f"Optimistic bound")

    # W7 submission string
    sub_str = strat.get("w7_submission", "—")
    sigma_disp = get_sigma_display(fn)
    sigma_type = strat.get("sigma_type", "isotropic")
    sigma_label = f"{sigma_disp} ({'anisotropic' if sigma_type == 'anisotropic' else 'isotropic'})"
    st.markdown(f"""
    <div style="background:#0d1018;border:1px solid #1e2538;border-radius:8px;
                padding:0.7rem 1.1rem;margin:0.4rem 0;font-family:'Space Mono',monospace;display:inline-block">
      <span style="color:#4a5570;font-size:0.70rem">W7 SUBMISSION · σ={sigma_label}</span><br>
      <span style="color:#4ade80;font-size:0.92rem">{sub_str}</span>
    </div>
    """, unsafe_allow_html=True)

    st.divider()

    # ── Main trajectory chart ─────────────────────────────────────────────────
    st.markdown("### Week-on-Week Trajectory")
    week_labels = [f"W{i+1}" for i in range(len(actuals))]
    bar_colors  = ["#6b7a9a"]
    for i in range(1, len(actuals)):
        improved = (actuals[i] > actuals[i-1]) if maximize else (actuals[i] < actuals[i-1])
        bar_colors.append("#22c55e" if improved else "#ef4444")

    rb_vals = [r for r in rb if r is not None]

    fig = go.Figure()
    # Actual bars
    fig.add_trace(go.Bar(
        x=week_labels, y=actuals,
        marker_color=bar_colors, marker_line_width=0,
        opacity=0.85, name="Submitted score",
        text=[fmt(v) for v in actuals],
        textposition="outside", textfont=dict(size=11, color="white"),
        hovertemplate="%{x}: <b>%{y:.4g}</b><extra></extra>",
    ))
    # Running best
    fig.add_trace(go.Scatter(
        x=week_labels, y=rb_vals,
        mode="lines+markers", line=dict(color="#f59e0b", width=2.5, dash="dash"),
        marker=dict(size=6, color="#f59e0b"),
        name="Running best",
    ))
    # W7 UCB prediction bar
    fig.add_trace(go.Bar(
        x=["W7 (pred)"], y=[pred["ucb"]],
        marker_color="rgba(129,140,248,0.4)",
        marker_line=dict(color="#818cf8", width=2),
        marker_pattern_shape="/",
        name=f"W7 UCB={pred['ucb']:.4g}",
    ))
    # GP μ with error bar
    fig.add_trace(go.Scatter(
        x=["W7 (pred)"], y=[pred["mu"]],
        mode="markers", marker=dict(symbol="diamond", size=14, color="#818cf8",
                                     line=dict(color="white", width=2)),
        error_y=dict(type="data", array=[2*pred["sigma"]], color="#818cf8", thickness=2, width=10),
        name=f"GP μ±2σ = {pred['mu']:.4g}±{2*pred['sigma']:.4g}",
    ))
    # All-time best line
    fig.add_hline(y=atb, line_dash="dot", line_color="#f87171", line_width=1.5,
                  annotation_text=f"All-time best: {fmt(atb)}",
                  annotation_font_color="#f87171", annotation_font_size=11,
                  annotation_position="right")

    fig.update_layout(
        height=420, paper_bgcolor="#0f1117", plot_bgcolor="#161b27",
        font=dict(color="#c5cae9"), barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, bgcolor="rgba(0,0,0,0)"),
        xaxis=dict(gridcolor="#1e2535", title="Week"),
        yaxis=dict(gridcolor="#1e2535", title="Function Value"),
        margin=dict(l=10, r=20, t=60, b=40),
    )
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Score table + submitted coordinates ───────────────────────────────────
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("### Score History")
        rows = []
        rb2 = running_best(scores, maximize)
        for i, (s, r) in enumerate(zip(scores[:6], rb2[:6])):
            is_best = (s == atb) if s is not None else False
            rows.append({
                "Week": f"W{i+1}",
                "Score": fmt(s),
                "Running Best": fmt(r),
                "New Best?": "⭐" if is_best else "",
                "vs W1": fmt((s - actuals[0])) if s is not None and actuals else "—",
            })
        import pandas as pd
        df = pd.DataFrame(rows).set_index("Week")
        st.dataframe(df, use_container_width=True, height=280)

    with col2:
        st.markdown("### Submitted Coordinates")
        coords = COORDS[fn]
        n_dims = info["dims"]
        dim_labels = [f"X{j+1}" for j in range(n_dims)]

        fig2 = go.Figure()
        palette = ["#4c9be8","#22c55e","#f59e0b","#a78bfa","#f472b6","#34d399"]
        for i, (coord, score) in enumerate(zip(coords[:6], scores[:6])):
            if coord is None or score is None: continue
            fig2.add_trace(go.Scatter(
                x=dim_labels, y=coord,
                mode="lines+markers",
                name=f"W{i+1} ({fmt(score)})",
                line=dict(color=palette[i % len(palette)], width=2),
                marker=dict(size=8, color=palette[i % len(palette)]),
                hovertemplate="<b>%{x}</b>: %{y:.4f}<extra>W" + str(i+1) + "</extra>",
            ))
        fig2.update_layout(
            height=280, paper_bgcolor="#0f1117", plot_bgcolor="#161b27",
            font=dict(color="#c5cae9"), margin=dict(l=10, r=10, t=10, b=40),
            legend=dict(font_size=10, bgcolor="rgba(0,0,0,0)"),
            xaxis=dict(title="Dimension", gridcolor="#1e2535"),
            yaxis=dict(title="Coordinate Value", gridcolor="#1e2535", range=[-0.05, 1.1]),
        )
        fig2.add_hline(y=0, line_color="#3d4a6a", line_width=1)
        fig2.add_hline(y=1, line_color="#3d4a6a", line_width=1, line_dash="dot")
        st.plotly_chart(fig2, use_container_width=True)
        st.caption("Each line = one week's submitted coordinates across all dimensions. Dashed line = boundary at 1.0.")
