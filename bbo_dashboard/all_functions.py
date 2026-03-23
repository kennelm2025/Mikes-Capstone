import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
import pandas as pd
from data import FUNCTIONS, SCORES, W7_PRED, STRATEGY, CLASSIFIERS, W7_GLANCE, TURBO_SUMMARY, COORDS, WEEKLY, CURRENT_WEEK, running_best, get_all_time_best, get_sigma_display

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if abs(v) < 0.0001 and v != 0: return f"{v:.2e}"
    return f"{v:.4f}"

def render(wk_idx=None):
    if wk_idx is None:
        wk_idx = CURRENT_WEEK - 1
    week_label = f"W{wk_idx+1}"
    st.markdown(f"""
    <div class='page-hero'>
      <div class='page-eyebrow'>All Functions · All Weeks · {week_label} Selected</div>
      <div class='page-title'>All 8 Functions</div>
      <div class='page-sub'>Side-by-side comparison · Use sidebar Week selector to change view · All data W1–W' + str(CURRENT_WEEK) + '</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Summary cards for selected week ──────────────────────────────────────
    st.markdown(f'<div class="sec-head">All Functions · {week_label} At a Glance</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, (fn, info) in enumerate(FUNCTIONS.items()):
        maximize = info["objective"] == "MAXIMISE"
        scores   = SCORES[fn]
        score_wk = scores[wk_idx] if wk_idx < len(scores) else None
        atb      = get_all_time_best(fn)
        strat    = STRATEGY[fn]
        action   = strat["action"]
        sub_str  = WEEKLY[fn][wk_idx].get("submission", "—") if wk_idx < len(WEEKLY[fn]) else "—"

        is_best = (score_wk == atb) if score_wk is not None else False
        if "EXPLORE" in action:   acolor = "#34d399"
        elif "RECOVER" in action: acolor = "#fbbf24"
        else:                     acolor = "#60a5fa"

        with cols[i % 4]:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;
                        padding:14px 16px;margin-bottom:10px;border-top:2px solid {acolor}'>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:8px'>
                <span style='font-family:Syne,sans-serif;font-size:1.3rem;font-weight:800;color:#e8eeff'>{fn}</span>
                <span style='font-family:"IBM Plex Mono",monospace;font-size:0.62rem;color:#2d3a52'>{info["dims"]}D</span>
              </div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#2d3a52;margin-bottom:3px'>
                {week_label} SCORE</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:1.1rem;font-weight:600;
                          color:{"#f59e0b" if is_best else "#e8eeff"};margin-bottom:6px'>
                {"★ " if is_best else ""}{fmt(score_wk)}
              </div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.62rem;
                          color:{acolor};margin-bottom:6px'>{action.split()[0]}</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#1a2a1a;
                          word-break:break-all;line-height:1.4'>{sub_str[:35]}…</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Score Trajectories — All Functions</div>', unsafe_allow_html=True)

    # ── 2×4 trajectory grid ───────────────────────────────────────────────────
    fig = make_subplots(
        rows=2, cols=4,
        subplot_titles=[f"{fid} — {FUNCTIONS[fid]['dims']}D" for fid in FUNCTIONS],
        vertical_spacing=0.22, horizontal_spacing=0.07,
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

        bar_colors = ["#3d4f70"]
        for i in range(1, len(actuals)):
            imp = (actuals[i] > actuals[i-1]) if maximize else (actuals[i] < actuals[i-1])
            bar_colors.append("#22c55e" if imp else "#ef4444")
        # Highlight selected week
        if wk_idx < len(bar_colors): bar_colors[wk_idx] = "#2563eb"

        fig.add_trace(go.Bar(x=week_labels, y=actuals, marker_color=bar_colors,
                             marker_line_width=0, opacity=0.85, showlegend=False,
                             hovertemplate="%{x}: <b>%{y:.4g}</b><extra>" + fid + "</extra>"),
                      row=row, col=col)
        fig.add_trace(go.Scatter(x=week_labels, y=rb_vals, mode="lines",
                                 line=dict(color="#f59e0b", width=1.5, dash="dash"), showlegend=False),
                      row=row, col=col)

    fig.update_layout(
        height=480, paper_bgcolor="#060a10", plot_bgcolor="#0a1020",
        font=dict(color="#4a5a7a", size=9, family="IBM Plex Mono"),
        margin=dict(l=10, r=10, t=50, b=10),
    )
    fig.update_xaxes(gridcolor="#0d1320", tickfont=dict(size=7))
    fig.update_yaxes(gridcolor="#0d1320", tickfont=dict(size=7))
    st.plotly_chart(fig, use_container_width=True)

    st.markdown('<div class="sec-head">Improvement Heatmap — Week-on-Week</div>', unsafe_allow_html=True)
    fns_list = list(FUNCTIONS.keys())
    n_transitions = CURRENT_WEEK - 1
    weeks    = [f"W{i+1}\u2192W{i+2}" for i in range(n_transitions)]
    z_matrix, text_matrix = [], []
    for fid in fns_list:
        maximize = FUNCTIONS[fid]["objective"] == "MAXIMISE"
        sc = [s for s in SCORES[fid] if s is not None]
        row_vals, text_vals = [], []
        for i in range(min(n_transitions, len(sc)-1)):
            delta = sc[i+1] - sc[i]
            if not maximize: delta = -delta
            row_vals.append(delta)
            text_vals.append(fmt(sc[i+1] - sc[i]))
        while len(row_vals) < n_transitions: row_vals.append(0); text_vals.append("—")
        z_matrix.append(row_vals); text_matrix.append(text_vals)

    z_arr = np.array(z_matrix, dtype=float)
    z_norm = np.zeros_like(z_arr)
    for i, row in enumerate(z_arr):
        rng = max(abs(row.max()), abs(row.min()), 1e-12)
        z_norm[i] = row / rng

    fig2 = go.Figure(go.Heatmap(
        z=z_norm, x=weeks, y=fns_list,
        text=text_matrix, texttemplate="%{text}",
        textfont=dict(size=9, color="white", family="IBM Plex Mono"),
        colorscale=[[0,"#7f1d1d"],[0.35,"#1a2540"],[0.65,"#1a2540"],[1,"#14532d"]],
        zmid=0, showscale=False,
        hovertemplate="<b>%{y} %{x}</b><br>Δ = %{text}<extra></extra>",
    ))
    fig2.update_layout(height=260, paper_bgcolor="#060a10",
                       font=dict(color="#4a5a7a", size=10, family="IBM Plex Mono"),
                       margin=dict(l=10, r=10, t=10, b=40))
    st.plotly_chart(fig2, use_container_width=True)
    st.caption("Green = improved vs prior week · Red = regressed · Intensity = relative magnitude")

    # ── W7 submission strings table ───────────────────────────────────────────
    st.markdown('<div class="sec-head">Submission Strings — All Functions · All Weeks Available</div>', unsafe_allow_html=True)

    rows_html = ""
    for fn in FUNCTIONS:
        maximize = FUNCTIONS[fn]["objective"] == "MAXIMISE"
        for wi in range(CURRENT_WEEK):
            score = SCORES[fn][wi] if wi < len(SCORES[fn]) else None
            sub   = WEEKLY[fn][wi].get("submission","—") if wi < len(WEEKLY[fn]) else "—"
            wl    = f"W{wi+1}"
            is_selected = wi == wk_idx
            sc_color = "#f59e0b" if (score is not None and score == get_all_time_best(fn)) else "#8a9abf"
            if score is None: sc_color = "#2d3a52"
            highlight = "background:#0d1a30;" if is_selected else ""
            rows_html += f"""<tr style='{highlight}'>
              <td style='padding:5px 10px;font-family:"IBM Plex Mono",monospace;font-size:0.75rem;color:#e8eeff'>{fn}</td>
              <td style='padding:5px 10px;font-family:"IBM Plex Mono",monospace;font-size:0.75rem;color:{"#2563eb" if is_selected else "#2d3a52"}'>{wl}</td>
              <td style='padding:5px 10px;font-family:"IBM Plex Mono",monospace;font-size:0.75rem;color:{sc_color}'>{fmt(score)}</td>
              <td style='padding:5px 10px;font-family:"IBM Plex Mono",monospace;font-size:0.68rem;color:#22c55e;word-break:break-all'>{sub}</td>
            </tr>"""

    st.markdown(f"""
    <div style='max-height:400px;overflow-y:auto;border:1px solid #141e30;border-radius:10px'>
    <table style='width:100%;border-collapse:collapse;background:#080e1a'>
      <thead style='position:sticky;top:0;background:#0a1020'>
        <tr>
          <th style='padding:7px 10px;text-align:left;font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#2d3a52;text-transform:uppercase'>Fn</th>
          <th style='padding:7px 10px;text-align:left;font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#2d3a52;text-transform:uppercase'>Wk</th>
          <th style='padding:7px 10px;text-align:left;font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#2d3a52;text-transform:uppercase'>Score</th>
          <th style='padding:7px 10px;text-align:left;font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#2d3a52;text-transform:uppercase'>Submission String</th>
        </tr>
      </thead>
      <tbody>{rows_html}</tbody>
    </table>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Blue row = currently selected {week_label} · ★ gold = all-time best score for that function")
