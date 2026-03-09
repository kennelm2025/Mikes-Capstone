import streamlit as st
from data import FUNCTIONS, SCORES, STRATEGY, CLASSIFIERS, W7_PRED, TURBO_SUMMARY, running_best, get_all_time_best, get_sigma_display
import plotly.graph_objects as go

def render(fn):
    maximize = FUNCTIONS[fn]["objective"] == "MAXIMISE"
    scores   = SCORES[fn]
    actuals  = [s for s in scores[:6] if s is not None]
    rb       = running_best(scores[:6], maximize)
    atb      = get_all_time_best(fn)
    strat    = STRATEGY[fn]
    clf      = CLASSIFIERS[fn]
    pred     = W7_PRED[fn]
    turbo    = TURBO_SUMMARY[fn]

    st.markdown(f'<div class="page-header">BBO Capstone · Week 7 · {fn}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-title">{fn} — {FUNCTIONS[fn]["desc"]}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="page-subtitle">{FUNCTIONS[fn]["dims"]}D · {FUNCTIONS[fn]["objective"]} · Search space {FUNCTIONS[fn]["search"]}</div>', unsafe_allow_html=True)

    def card(label, value, sub=""):
        return f"""<div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-sub">{sub}</div>
        </div>"""

    def fmt(v):
        if v is None: return "—"
        if abs(v) >= 1000: return f"{v:,.0f}"
        if abs(v) < 0.001 and v != 0: return f"{v:.2e}"
        return f"{v:.4f}"

    sigma_disp = get_sigma_display(fn)
    sigma_type = strat.get("sigma_type", "isotropic")
    turbo_dir  = turbo["direction"]
    turbo_col  = "#4ade80" if turbo_dir == "EXPAND" else "#f87171"

    st.markdown(f"""
    <div class="metric-row">
        {card("All-Time Best", fmt(atb), strat["best_week"])}
        {card("W6 Score", fmt(actuals[-1]), "Last submitted")}
        {card("GP μ (W7)", fmt(pred["mu"]), "GP mean prediction")}
        {card("GP UCB (W7)", fmt(pred["ucb"]), f"μ + {strat.get('ucb_kappa',2.0)}σ")}
        {card("W7 Strategy", strat["action"].split()[0], strat["action"])}
        {card("Winning Model", clf["name"], f"CV {clf['cv']:.1%}")}
    </div>
    """, unsafe_allow_html=True)

    # ── Strategy badge + rationale ────────────────────────────────────────────
    action = strat["action"]
    if "EXPLORE" in action:   badge_cls = "badge-explore"
    elif "RECOVER" in action: badge_cls = "badge-recover"
    else:                     badge_cls = "badge-exploit"

    st.markdown('<div class="section-header">W7 Strategy</div>', unsafe_allow_html=True)
    st.markdown(f'<span class="strategy-badge {badge_cls}">{action}</span>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#9aa4c0;line-height:1.75;max-width:800px">{strat["rationale"]}</p>', unsafe_allow_html=True)

    # ── W7 Submission string ──────────────────────────────────────────────────
    sub_str = strat.get("w7_submission", "—")
    st.markdown(f"""
    <div style="background:#0d1018;border:1px solid #1e2538;border-radius:8px;
                padding:0.8rem 1.2rem;margin:0.5rem 0 1rem 0;font-family:'Space Mono',monospace">
      <span style="color:#4a5570;font-size:0.72rem">W7 SUBMISSION STRING</span><br>
      <span style="color:#4ade80;font-size:0.95rem;letter-spacing:0.03em">{sub_str}</span>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="section-header">Week-on-Week Trajectory</div>', unsafe_allow_html=True)
        weeks_labels = ["W1","W2","W3","W4","W5","W6"]
        colors = ["#95a5a6"]
        for i in range(1, len(actuals)):
            improved = actuals[i] > actuals[i-1] if maximize else actuals[i] < actuals[i-1]
            colors.append("#4ade80" if improved else "#f87171")

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=weeks_labels, y=actuals,
            marker_color=colors, marker_line_width=0,
            opacity=0.85, name="Score",
            hovertemplate="%{x}: <b>%{y:.4g}</b><extra></extra>",
        ))
        rb_vals = [r for r in rb if r is not None]
        fig.add_trace(go.Scatter(
            x=weeks_labels, y=rb_vals,
            mode="lines", line=dict(color="#f59e0b", width=2.5, dash="dash"),
            name="Running best",
            hovertemplate="%{x} best: <b>%{y:.4g}</b><extra></extra>",
        ))
        fig.add_trace(go.Bar(
            x=["W7 (pred)"], y=[pred["ucb"]],
            marker_color="rgba(129,140,248,0.45)",
            marker_line=dict(color="#818cf8", width=1.5),
            name=f"W7 UCB={pred['ucb']:.4g}",
            hovertemplate=f"W7 UCB: <b>{pred['ucb']:.4g}</b><extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=["W7 (pred)"], y=[pred["mu"]],
            mode="markers",
            marker=dict(symbol="diamond", size=12, color="#818cf8",
                        line=dict(color="white", width=2)),
            name=f"GP μ={pred['mu']:.4g}",
            error_y=dict(type="data", array=[2*pred["sigma"]], color="#818cf8",
                         thickness=2, width=8),
            hovertemplate=f"GP μ: <b>{pred['mu']:.4g}</b> ± 2σ={2*pred['sigma']:.4g}<extra></extra>",
        ))
        fig.add_hline(y=atb, line_dash="dot", line_color="#f87171",
                      line_width=1.5, annotation_text=f"Best={atb:.4g}",
                      annotation_font_color="#f87171", annotation_font_size=11)
        fig.update_layout(
            paper_bgcolor="#111520", plot_bgcolor="#111520",
            font=dict(color="#9aa4c0", family="DM Sans"),
            height=320, margin=dict(l=10, r=10, t=10, b=40),
            showlegend=True,
            legend=dict(bgcolor="rgba(0,0,0,0)", font_size=11,
                        orientation="h", yanchor="bottom", y=1.02),
            xaxis=dict(gridcolor="#1e2538", showgrid=False),
            yaxis=dict(gridcolor="#1e2538", showgrid=True),
            barmode="group",
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    with col2:
        st.markdown('<div class="section-header">W7 Hyperparameters</div>', unsafe_allow_html=True)
        params = {
            "Exploit ratio": f"{strat['exploit_ratio']:.0%}",
            "Sigma (σ)": f"{sigma_disp}" + (" ⟨anisotropic⟩" if sigma_type == "anisotropic" else ""),
            "TuRBO direction": turbo_dir,
            "UCB κ": f"{strat.get('ucb_kappa', 2.0)}",
            "GP restarts": f"{strat.get('gp_restarts', 5)}",
            "Best pattern": strat["pattern"],
        }
        rows = ""
        for k, v in params.items():
            if k == "TuRBO direction":
                v_html = f'<span style="color:{turbo_col};font-weight:600">{v}</span>'
            elif "anisotropic" in str(v):
                v_html = f'<span style="color:#eef2ff">{sigma_disp}</span> <span style="color:#f59e0b;font-size:0.75rem">anisotropic</span>'
            else:
                v_html = f'<span style="color:#eef2ff">{v}</span>'
            rows += (
                f"<tr><td style='color:#4a5570;font-family:Space Mono,monospace;"
                f"font-size:0.72rem;padding:0.45rem 0.8rem'>{k}</td>"
                f"<td style='padding:0.45rem 0.8rem;font-size:0.88rem'>{v_html}</td></tr>"
            )
        st.markdown(f"""
        <table style="width:100%;border-collapse:collapse;background:#0d1018;
                      border:1px solid #1e2538;border-radius:8px;overflow:hidden">
          <tbody>{rows}</tbody>
        </table>
        """, unsafe_allow_html=True)

        # TuRBO note
        st.markdown(f"""
        <div style="margin-top:0.8rem;background:#0d1018;border-left:3px solid {turbo_col};
                    padding:0.5rem 0.8rem;border-radius:0 6px 6px 0">
          <span style="color:#4a5570;font-size:0.70rem">TuRBO NOTE</span><br>
          <span style="color:#9aa4c0;font-size:0.80rem">{turbo["note"]}</span>
        </div>
        """, unsafe_allow_html=True)

        st.markdown('<div class="section-header">Winning Classifier</div>', unsafe_allow_html=True)
        family_map = {"SVM":"clf-svm","RF":"clf-rf","NN":"clf-nn","CNN":"clf-cnn","LogReg":"clf-lr","DT":"clf-svm"}
        clf_cls = family_map.get(clf["family"], "clf-svm")
        st.markdown(f"""
        <div style="display:flex;flex-direction:column;gap:0.6rem">
          <span class="clf-pill {clf_cls}">🏆 {clf["name"]}</span>
          <div style="color:#6b7a9a;font-size:0.83rem">
            CV Accuracy: <span style="color:#eef2ff;font-weight:600">{clf['cv']:.1%}</span>
            &nbsp;±&nbsp;<span style="color:#eef2ff">{clf['std']:.1%}</span>
          </div>
        </div>
        """, unsafe_allow_html=True)
