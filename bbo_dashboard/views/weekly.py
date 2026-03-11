import streamlit as st
import plotly.graph_objects as go
from data import FUNCTIONS, SCORES, STRATEGY, CLASSIFIERS, W7_PRED, COORDS, WEEKLY, TURBO_SUMMARY, CURRENT_WEEK, running_best, get_all_time_best, get_sigma_display

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if v != 0 and abs(v) < 0.001: return f"{v:.2e}"
    return f"{v:.4f}"

def render(fn, wk_idx):
    info     = FUNCTIONS[fn]
    maximize = info["objective"] == "MAXIMISE"
    scores   = SCORES[fn]
    actuals  = [s for s in scores if s is not None]
    atb      = get_all_time_best(fn)
    strat    = STRATEGY[fn]       # W7 strategy
    clf      = CLASSIFIERS[fn]
    weekly   = WEEKLY[fn][wk_idx]
    week_label = f"W{wk_idx+1}"
    score_this_wk = scores[wk_idx] if wk_idx < len(scores) else None
    coords_this_wk = COORDS[fn][wk_idx] if wk_idx < len(COORDS[fn]) else None

    # ── Page header ───────────────────────────────────────────────────────────
    action = strat["action"]
    if "EXPLORE" in action:   badge_cls, acolor = "badge-explore", "#34d399"
    elif "RECOVER" in action: badge_cls, acolor = "badge-recover", "#fbbf24"
    else:                     badge_cls, acolor = "badge-exploit", "#60a5fa"

    st.markdown(f"""
    <div class='page-hero'>
      <div class='page-eyebrow'>{fn} · {week_label} · Weekly Analysis</div>
      <div class='page-title'>{fn} — {info['dims']}D Function</div>
      <div class='page-sub'>{info['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Week selector pills ───────────────────────────────────────────────────
    n_actual = len(actuals)
    tabs_html = '<div class="week-tabs">'
    for i in range(CURRENT_WEEK):
        available = i < n_actual or i == CURRENT_WEEK - 1
        label = f"W{i+1}"
        active = "wtab-active" if i == wk_idx else ""
        dim = "" if available else " style='opacity:0.35'"
        tabs_html += f'<span class="wtab {active}"{dim}>{label}</span>'
    tabs_html += "</div>"
    st.markdown(tabs_html + "<div style='font-size:0.65rem;color:#2d3a52;font-family:IBM Plex Mono,monospace;margin-bottom:1rem'>← Use sidebar Week selector to navigate</div>", unsafe_allow_html=True)

    # ── KPI row ───────────────────────────────────────────────────────────────
    is_best = (score_this_wk == atb) if score_this_wk is not None else False
    prev_score = scores[wk_idx-1] if wk_idx > 0 and scores[wk_idx-1] is not None else None
    if prev_score is not None and score_this_wk is not None:
        delta = score_this_wk - prev_score
        delta_str = f"{'▲' if delta > 0 else '▼'} {fmt(abs(delta))}"
        delta_col = "#34d399" if delta > 0 else "#ef4444"
        if not maximize: delta_col = "#ef4444" if delta > 0 else "#34d399"
    else:
        delta_str, delta_col = "—", "#4a5a7a"

    rb = running_best(scores, maximize)
    rb_this = rb[wk_idx] if wk_idx < len(rb) and rb[wk_idx] is not None else None

    st.markdown(f"""
    <div class='kpi-grid'>
      <div class='kpi-card' style='--accent:#2563eb'>
        <div class='kpi-label'>{week_label} Score</div>
        <div class='kpi-value'>{"★ " if is_best else ""}{fmt(score_this_wk)}</div>
        <div class='kpi-sub'>{"All-time best!" if is_best else "Submitted result"}</div>
      </div>
      <div class='kpi-card' style='--accent:{delta_col}'>
        <div class='kpi-label'>vs Prior Week</div>
        <div class='kpi-value' style='color:{delta_col}'>{delta_str}</div>
        <div class='kpi-sub'>{f"vs W{wk_idx} = {fmt(prev_score)}" if prev_score is not None else "No prior week"}</div>
      </div>
      <div class='kpi-card' style='--accent:#f59e0b'>
        <div class='kpi-label'>Running Best</div>
        <div class='kpi-value'>{fmt(rb_this)}</div>
        <div class='kpi-sub'>Best so far through {week_label}</div>
      </div>
      <div class='kpi-card' style='--accent:#10b981'>
        <div class='kpi-label'>All-Time Best</div>
        <div class='kpi-value'>{fmt(atb)}</div>
        <div class='kpi-sub'>{strat["best_week"]}</div>
      </div>
      <div class='kpi-card' style='--accent:{acolor}'>
        <div class='kpi-label'>W{CURRENT_WEEK} Strategy</div>
        <div class='kpi-value' style='font-size:0.85rem;color:{acolor}'>{action.split()[0]}</div>
        <div class='kpi-sub'>{action}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Submitted coordinates ─────────────────────────────────────────────────
    if coords_this_wk:
        sub_str = weekly.get("submission", "-".join(str(round(c,6)) for c in coords_this_wk))
        st.markdown(f"""
        <div class='sub-box'>
          <div class='sub-label'>{week_label} · {fn} · Submitted Coordinates</div>
          {sub_str}
        </div>
        """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        # ── Trajectory chart ──────────────────────────────────────────────────
        st.markdown('<div class="sec-head">Week-on-Week Trajectory</div>', unsafe_allow_html=True)
        week_labels = [f"W{i+1}" for i in range(len(actuals))]
        bar_colors = ["#4a5a7a"]
        for i in range(1, len(actuals)):
            imp = (actuals[i] > actuals[i-1]) if maximize else (actuals[i] < actuals[i-1])
            bar_colors.append("#22c55e" if imp else "#ef4444")
        # Highlight selected week
        if wk_idx < len(bar_colors):
            bar_colors[wk_idx] = "#2563eb"

        rb_vals = [r for r in rb if r is not None][:len(actuals)]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=week_labels, y=actuals, marker_color=bar_colors,
            marker_line_width=0, opacity=0.9, name="Score",
            text=[fmt(v) for v in actuals], textposition="outside",
            textfont=dict(size=10, color="white"),
            hovertemplate="%{x}: <b>%{y:.4g}</b><extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=week_labels, y=rb_vals, mode="lines+markers",
            line=dict(color="#f59e0b", width=2, dash="dash"),
            marker=dict(size=5, color="#f59e0b"),
            name="Running best",
        ))
        if wk_idx < len(actuals):
            fig.add_vline(x=wk_idx, line_dash="dot", line_color="#2563eb",
                          line_width=1.5, annotation_text=f"← {week_label}",
                          annotation_font_color="#2563eb", annotation_font_size=10)
        fig.update_layout(
            paper_bgcolor="#080e1a", plot_bgcolor="#080e1a",
            font=dict(color="#4a5a7a", family="IBM Plex Mono"),
            height=280, margin=dict(l=10, r=10, t=20, b=40),
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)", font_size=10,
                        orientation="h", yanchor="bottom", y=1.02),
            xaxis=dict(gridcolor="#0d1320", showgrid=False),
            yaxis=dict(gridcolor="#0d1320", showgrid=True, gridwidth=0.5),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        # ── Coordinate plot ───────────────────────────────────────────────────
        if coords_this_wk and len(coords_this_wk) > 0:
            st.markdown('<div class="sec-head">Submitted Coordinates</div>', unsafe_allow_html=True)
            dims = [f"X{i+1}" for i in range(len(coords_this_wk))]
            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=dims, y=coords_this_wk,
                marker_color=["#2563eb" if abs(c) < 0.1 or abs(c-1) < 0.1 else "#3d4f70" for c in coords_this_wk],
                marker_line_width=0, opacity=0.9,
                text=[f"{c:.4f}" for c in coords_this_wk],
                textposition="outside", textfont=dict(size=10, color="white"),
                hovertemplate="%{x}: <b>%{y:.4f}</b><extra></extra>",
            ))
            fig2.add_hline(y=0.5, line_dash="dot", line_color="#1a2540", line_width=1)
            fig2.update_layout(
                paper_bgcolor="#080e1a", plot_bgcolor="#080e1a",
                font=dict(color="#4a5a7a", family="IBM Plex Mono"),
                height=220, margin=dict(l=10, r=10, t=10, b=40),
                showlegend=False,
                xaxis=dict(gridcolor="#0d1320", showgrid=False),
                yaxis=dict(gridcolor="#0d1320", showgrid=True, gridwidth=0.5, range=[-0.05, 1.15]),
            )
            st.caption("Blue = near-boundary (< 0.1 or > 0.9)")
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

    with col2:
        # ── Hyperparameters ───────────────────────────────────────────────────
        st.markdown('<div class="sec-head">Hyperparameters Used</div>', unsafe_allow_html=True)
        hp = weekly["hyperparams"]
        sigma_val = hp.get("sigma", "—")
        if isinstance(sigma_val, list):
            sigma_disp = f"[{', '.join(str(v) for v in sigma_val)}] ★"
        else:
            sigma_disp = str(sigma_val)

        params = [
            ("Exploit Ratio", f"{hp.get('exploit_ratio', '—'):.0%}" if isinstance(hp.get('exploit_ratio'), float) else "—"),
            ("Sigma (σ)", sigma_disp),
            ("UCB κ", str(hp.get("ucb_kappa", "—"))),
            ("GP Restarts", str(hp.get("gp_restarts", "—"))),
        ]
        if wk_idx == CURRENT_WEEK - 1:  # latest week — show TuRBO
            turbo = TURBO_SUMMARY[fn]
            params.append(("TuRBO", turbo["direction"]))

        for pname, pval in params:
            color = "#fbbf24" if "★" in pval else ("#34d399" if pval == "EXPAND" else ("#ef4444" if pval == "SHRINK" else "#e8eeff"))
            st.markdown(f"""
            <div class='param-row'>
              <span class='param-name'>{pname}</span>
              <span class='param-val' style='color:{color}'>{pval}</span>
            </div>
            """, unsafe_allow_html=True)

        st.markdown(f"""
        <div class='info-card' style='margin-top:10px'>
          <div class='info-card-title'>Why These Parameters?</div>
          <div class='info-card-body'>{weekly["hp_rationale"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── What We Know / Learned ────────────────────────────────────────────────
    st.markdown('<div class="sec-head">What We Know · What We Learned</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>🔎 Observations This Week</div>
          <div class='info-card-body'>{weekly["learned"]}</div>
        </div>
        """, unsafe_allow_html=True)
        # Pattern from strategy
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>📐 Known Pattern (Cumulative)</div>
          <div class='info-card-body'>{strat["pattern"]}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>🧪 Learning / Experiment</div>
          <div class='info-card-body'>{weekly["experiment"]}</div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>🧭 W{CURRENT_WEEK} Strategy Rationale</div>
          <div class='info-card-body'>{strat["rationale"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # ── Score history table ───────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Full Score History — {fn}</div>'.format(fn=fn), unsafe_allow_html=True)
    rows = ""
    for i, (wl, sc) in enumerate(zip([f"W{j+1}" for j in range(CURRENT_WEEK)], scores)):
        if sc is None:
            sc_str, row_col = "Pending", "#2d3a52"
        else:
            sc_str = fmt(sc)
            rb_i = rb[i] if i < len(rb) and rb[i] is not None else None
            is_rb = (sc == rb_i) and sc is not None
            row_col = "#f59e0b" if is_rb else ("#34d399" if (i > 0 and scores[i-1] is not None and ((maximize and sc > scores[i-1]) or (not maximize and sc < scores[i-1]))) else "#4a5a7a")

        highlight = "background:#0d1a30;" if i == wk_idx else ""
        coords_i = COORDS[fn][i] if i < len(COORDS[fn]) and COORDS[fn][i] else []
        coord_str = " · ".join(f"{c:.4f}" for c in coords_i) if coords_i else "—"
        weekly_sub = WEEKLY[fn][i].get("submission", "—") if i < len(WEEKLY[fn]) else "—"
        rows += f"""
        <tr style='{highlight}'>
          <td style='padding:8px 12px;font-family:"IBM Plex Mono",monospace;font-size:0.78rem;color:#e8eeff;font-weight:{"700" if i==wk_idx else "400"}'>{wl}</td>
          <td style='padding:8px 12px;font-family:"IBM Plex Mono",monospace;font-size:0.85rem;color:{row_col}'>{sc_str}</td>
          <td style='padding:8px 12px;font-family:"IBM Plex Mono",monospace;font-size:0.70rem;color:#2d3a52'>{coord_str[:60]}</td>
        </tr>"""

    st.markdown(f"""
    <table style='width:100%;border-collapse:collapse;background:#080e1a;
                  border:1px solid #141e30;border-radius:10px;overflow:hidden'>
      <thead>
        <tr style='background:#0a1020'>
          <th style='padding:8px 12px;text-align:left;font-family:"IBM Plex Mono",monospace;
                     font-size:0.62rem;color:#2d3a52;text-transform:uppercase;letter-spacing:0.15em'>Week</th>
          <th style='padding:8px 12px;text-align:left;font-family:"IBM Plex Mono",monospace;
                     font-size:0.62rem;color:#2d3a52;text-transform:uppercase;letter-spacing:0.15em'>Score</th>
          <th style='padding:8px 12px;text-align:left;font-family:"IBM Plex Mono",monospace;
                     font-size:0.62rem;color:#2d3a52;text-transform:uppercase;letter-spacing:0.15em'>Coordinates</th>
        </tr>
      </thead>
      <tbody>{rows}</tbody>
    </table>
    """, unsafe_allow_html=True)
