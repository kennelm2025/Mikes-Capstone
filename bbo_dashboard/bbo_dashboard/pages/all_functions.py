import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data import FUNCTIONS, SCORES, W7_PRED, STRATEGY, CLASSIFIERS, running_best, get_all_time_best

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if abs(v) < 0.0001 and v != 0: return f"{v:.2e}"
    return f"{v:.4f}"

def render():
    st.markdown("## 📋 All Functions — Side by Side")
    st.caption("Compare performance, strategy, and predictions across all 8 BBO functions simultaneously.")

    # ── 2×4 trajectory grid ───────────────────────────────────────────────────
    st.markdown("### Week-on-Week Trajectories (W1–W6 + W7 Prediction)")
    fig = make_subplots(
        rows=2, cols=4,
        subplot_titles=[f"{fid} — {FUNCTIONS[fid]['dims']}D {FUNCTIONS[fid]['objective'][:3]}"
                        for fid in FUNCTIONS],
        vertical_spacing=0.20, horizontal_spacing=0.07,
    )
    for idx, (fid, info) in enumerate(FUNCTIONS.items()):
        row, col = divmod(idx, 4); row+=1; col+=1
        maximize = info["objective"] == "MAXIMISE"
        scores   = SCORES[fid]
        actuals  = [s for s in scores if s is not None]
        pred     = W7_PRED[fid]
        rb       = running_best(scores, maximize)
        rb_vals  = [r for r in rb if r is not None]
        week_labels = [f"W{i+1}" for i in range(len(actuals))]
        bar_colors  = ["#6b7a9a"]
        for i in range(1, len(actuals)):
            imp = (actuals[i] > actuals[i-1]) if maximize else (actuals[i] < actuals[i-1])
            bar_colors.append("#22c55e" if imp else "#ef4444")

        fig.add_trace(go.Bar(x=week_labels, y=actuals, marker_color=bar_colors,
                             marker_line_width=0, opacity=0.85, showlegend=False,
                             hovertemplate="%{x}: <b>%{y:.4g}</b><extra>" + fid + "</extra>"),
                      row=row, col=col)
        fig.add_trace(go.Scatter(x=week_labels, y=rb_vals, mode="lines",
                                 line=dict(color="#f59e0b", width=1.8, dash="dash"),
                                 showlegend=False),
                      row=row, col=col)
        if pred.get("ucb"):
            fig.add_trace(go.Scatter(x=["W7"], y=[pred["ucb"]], mode="markers",
                                     marker=dict(symbol="diamond", size=10, color="#818cf8",
                                                 line=dict(color="white", width=1)),
                                     showlegend=False,
                                     hovertemplate=f"W7 UCB: {pred['ucb']:.4g}<extra></extra>"),
                          row=row, col=col)

    fig.update_layout(height=500, paper_bgcolor="#0f1117", plot_bgcolor="#161b27",
                      font=dict(color="#c5cae9", size=9),
                      margin=dict(l=10, r=10, t=60, b=10))
    fig.update_xaxes(gridcolor="#1e2535", tickfont=dict(size=7))
    fig.update_yaxes(gridcolor="#1e2535", tickfont=dict(size=7))
    st.plotly_chart(fig, use_container_width=True)

    st.divider()

    # ── Heatmap: improvement week-over-week ────────────────────────────────────
    st.markdown("### 🌡️ Improvement Heatmap (Week-on-Week Delta)")
    st.caption("Green = improved on prior week, Red = regressed. Intensity = magnitude of change.")

    import numpy as np
    fns_list = list(FUNCTIONS.keys())
    weeks    = ["W1→W2", "W2→W3", "W3→W4", "W4→W5", "W5→W6"]
    z_matrix = []
    for fid in fns_list:
        maximize = FUNCTIONS[fid]["objective"] == "MAXIMISE"
        scores   = [s for s in SCORES[fid] if s is not None]
        row_vals = []
        for i in range(min(5, len(scores)-1)):
            delta = scores[i+1] - scores[i]
            if not maximize: delta = -delta  # flip so green = good
            row_vals.append(delta)
        while len(row_vals) < 5: row_vals.append(0)
        z_matrix.append(row_vals)

    z_arr    = np.array(z_matrix, dtype=float)
    # Normalise per-row to handle different scales
    z_norm   = np.zeros_like(z_arr)
    for i, row in enumerate(z_arr):
        rng = max(abs(row.max()), abs(row.min()), 1e-12)
        z_norm[i] = row / rng

    text_vals = [[fmt(z_arr[i][j]) for j in range(5)] for i in range(len(fns_list))]

    fig2 = go.Figure(go.Heatmap(
        z=z_norm, x=weeks, y=fns_list,
        text=text_vals, texttemplate="%{text}",
        textfont=dict(size=10, color="white"),
        colorscale=[[0,"#ef4444"],[0.5,"#1e2538"],[1,"#22c55e"]],
        zmid=0, showscale=True,
        hovertemplate="<b>%{y} %{x}</b><br>Delta: %{text}<extra></extra>",
        colorbar=dict(title="Relative<br>Improvement", tickfont=dict(size=9)),
    ))
    fig2.update_layout(height=300, paper_bgcolor="#0f1117",
                       font=dict(color="#c5cae9", size=11),
                       margin=dict(l=10, r=10, t=20, b=40))
    st.plotly_chart(fig2, use_container_width=True)

    st.divider()

    # ── Leaderboard ────────────────────────────────────────────────────────────
    st.markdown("### 🏆 All Functions — Combined Leaderboard")
    import pandas as pd

    lb_rows = []
    for fid, info in FUNCTIONS.items():
        maximize = info["objective"] == "MAXIMISE"
        scores   = [s for s in SCORES[fid] if s is not None]
        atb      = get_all_time_best(fid)
        w6       = scores[5] if len(scores) >= 6 else None
        strat    = STRATEGY[fid]
        clf      = CLASSIFIERS[fid]
        pred     = W7_PRED[fid]

        # Trend: is W6 the all-time best?
        is_best_now = (w6 == atb) if w6 is not None else False
        trend = "⭐ At Best" if is_best_now else ("📈 Improving" if (
            w6 is not None and len(scores) >= 2 and
            ((maximize and w6 > scores[4]) or (not maximize and w6 < scores[4]))
        ) else "📉 Regressed")

        lb_rows.append({
            "Fn": fid,
            "Dims": f"{info['dims']}D",
            "Objective": "MAX ▲" if maximize else "MIN ▼",
            "All-Time Best": fmt(atb),
            "Best Week": strat["best_week"],
            "W6 Score": fmt(w6),
            "Trend": trend,
            "W7 Strategy": strat["action"],
            "W7 UCB": fmt(pred["ucb"]),
            "W7 Classifier": clf["name"],
            "CV Acc": f"{clf['cv']:.0%}",
        })

    df = pd.DataFrame(lb_rows).set_index("Fn")
    st.dataframe(df, use_container_width=True, height=330)
