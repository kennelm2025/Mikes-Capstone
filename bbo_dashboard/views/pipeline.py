import streamlit as st
import plotly.graph_objects as go
from data import PIPELINE_STEPS, FUNCTIONS, STRATEGY, CLASSIFIERS, WEEKLY, SCORES, CURRENT_WEEK, get_all_time_best, get_sigma_display

STEP_COLORS = {
    "⚙️":"#6366f1","📂":"#3b82f6","🔬":"#06b6d4","📊":"#10b981","🏷️":"#f59e0b",
    "🤖":"#8b5cf6","🔍":"#ec4899","🎨":"#14b8a6","📈":"#f97316","🎲":"#84cc16",
    "🧠":"#f97316","🌐":"#06b6d4","🎯":"#3b82f6","📉":"#8b5cf6","🗺️":"#10b981","🏆":"#f59e0b",
}

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if v != 0 and abs(v) < 0.001: return f"{v:.2e}"
    return f"{v:.4f}"

def render(fn=None, wk_idx=None):
    if fn is None: fn = "F7"
    if wk_idx is None: wk_idx = CURRENT_WEEK - 1

    info       = FUNCTIONS[fn]
    week_label = f"W{wk_idx + 1}"
    scores     = SCORES[fn]
    score_wk   = scores[wk_idx] if wk_idx < len(scores) else None
    atb        = get_all_time_best(fn)
    strat      = STRATEGY[fn]
    clf        = CLASSIFIERS[fn]
    wk_data    = WEEKLY[fn][wk_idx] if wk_idx < len(WEEKLY[fn]) else {}
    hp         = wk_data.get("hyperparams", {})
    sigma_raw  = hp.get("sigma", strat.get("sigma", "—"))
    sigma_disp = f"[{', '.join(str(v) for v in sigma_raw)}]" if isinstance(sigma_raw, list) else str(sigma_raw)
    submission = wk_data.get("submission", "—")
    learned    = wk_data.get("learned", "—")
    experiment = wk_data.get("experiment", "—")
    hp_rat     = wk_data.get("hp_rationale", "—")
    is_pending = score_wk is None

    # ── Page header ───────────────────────────────────────────────────────────
    st.markdown(f"""
    <div class='page-hero'>
      <div class='page-eyebrow'>{fn} · {week_label} · Pipeline Walkthrough</div>
      <div class='page-title'>{fn} — {info['dims']}D · {week_label} Pipeline</div>
      <div class='page-sub'>{info['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── KPI strip ─────────────────────────────────────────────────────────────
    st.markdown(f"""
    <div style='display:grid;grid-template-columns:repeat(5,1fr);gap:10px;margin-bottom:1.5rem'>
      <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;padding:14px 16px;border-top:2px solid #6366f1'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#5a6a8a;text-transform:uppercase;margin-bottom:4px'>{week_label} Score</div>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:1.2rem;font-weight:700;color:{"#f59e0b" if score_wk==atb else "#e8eeff"}'>{"⏳ pending" if is_pending else fmt(score_wk)}</div>
      </div>
      <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;padding:14px 16px;border-top:2px solid #f59e0b'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#5a6a8a;text-transform:uppercase;margin-bottom:4px'>All-Time Best</div>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:1.2rem;font-weight:700;color:#f59e0b'>★ {fmt(atb)}</div>
      </div>
      <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;padding:14px 16px;border-top:2px solid #3b82f6'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#5a6a8a;text-transform:uppercase;margin-bottom:4px'>Exploit Ratio</div>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:1.2rem;font-weight:700;color:#e8eeff'>{hp.get("exploit_ratio", "—")}</div>
      </div>
      <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;padding:14px 16px;border-top:2px solid #10b981'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#5a6a8a;text-transform:uppercase;margin-bottom:4px'>CV Winner</div>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:1.0rem;font-weight:700;color:#e8eeff'>{clf["name"]}</div>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.65rem;color:#5a6a8a'>{clf["cv"]*100:.1f}% CV acc</div>
      </div>
      <div style='background:#0a1020;border:1px solid #141e30;border-radius:10px;padding:14px 16px;border-top:2px solid #ec4899'>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.58rem;color:#5a6a8a;text-transform:uppercase;margin-bottom:4px'>Strategy</div>
        <div style='font-family:"IBM Plex Mono",monospace;font-size:0.72rem;font-weight:700;color:#ec4899'>{strat["action"].split()[0]}</div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Submission box ────────────────────────────────────────────────────────
    if submission and submission not in ("—", "[PENDING]"):
        st.markdown(f"""
        <div class='sub-box'>
          <div class='sub-label'>{week_label} · {fn} · Submission String</div>
          {submission}{"  ⏳ awaiting portal result" if is_pending else ""}
        </div>
        """, unsafe_allow_html=True)

    # ── Visual pipeline flow ──────────────────────────────────────────────────
    st.markdown('<div class="sec-head">Visual Pipeline Flow</div>', unsafe_allow_html=True)

    n = len(PIPELINE_STEPS)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=list(range(n)), y=[0]*n, mode="lines",
        line=dict(color="#141e30", width=4), showlegend=False, hoverinfo="skip",
    ))
    for i, step in enumerate(PIPELINE_STEPS):
        color = STEP_COLORS.get(step["icon"], "#2563eb")
        fig.add_trace(go.Scatter(
            x=[i], y=[0], mode="markers+text",
            marker=dict(size=42, color=color, line=dict(color="#060a10", width=3)),
            text=[step["step"].replace("Step ", "")],
            textfont=dict(size=8, color="white", family="IBM Plex Mono"),
            textposition="middle center",
            name=step["title"],
            hovertemplate=f"<b>{step['step']}: {step['title']}</b><br>{step['desc'][:100]}<extra></extra>",
        ))
        fig.add_annotation(
            x=i, y=-0.42,
            text=step["title"].replace(" ", "<br>"),
            showarrow=False,
            font=dict(size=7.5, color="#4a5a7a", family="IBM Plex Mono"),
            align="center",
        )
    fig.update_layout(
        height=220, paper_bgcolor="#060a10", plot_bgcolor="#060a10",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.5, n-0.5]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.85, 0.45]),
        showlegend=False, margin=dict(l=20, r=20, t=10, b=10),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Step-by-step detail with fn/week context ──────────────────────────────
    st.markdown(f'<div class="sec-head">Step-by-Step Detail — {fn} · {week_label}</div>', unsafe_allow_html=True)

    selected_step = st.selectbox(
        "Select Step",
        [f"{s['step']} — {s['icon']} {s['title']}" for s in PIPELINE_STEPS],
        index=0,
        key="pipeline_step_select",
    )
    step_key  = selected_step.split(" — ")[0]
    step_data = next(s for s in PIPELINE_STEPS if s["step"] == step_key)
    color     = STEP_COLORS.get(step_data["icon"], "#2563eb")

    # Build the fn/week-specific context for each step
    step_context = {
        "Step 0":  f"FUNCTION_ID = {fn} | WEEK = {wk_idx+1} | MAXIMIZE = True | exploit_ratio = {hp.get('exploit_ratio','—')} | sigma = {sigma_disp} | ucb_kappa = {hp.get('ucb_kappa','—')} | gp_restarts = {hp.get('gp_restarts','—')}",
        "Step 1":  f"Load f{fn[1]}_w{wk_idx+1}_inputs.npy and f{fn[1]}_w{wk_idx+1}_outputs.npy. n_samples = {wk_idx+1} points in {info['dims']}D space.",
        "Step 2":  f"Inspect {wk_idx+1} samples across {info['dims']} dimensions. Score range: {fmt(min(s for s in scores[:wk_idx+1] if s is not None))} to {fmt(max(s for s in scores[:wk_idx+1] if s is not None))}." if any(s is not None for s in scores[:wk_idx+1]) else "Data inspection.",
        "Step 3":  f"Plot W1–{week_label} trajectory. ATB so far = {fmt(atb)}. Trend: {'improving' if len([s for s in scores[:wk_idx+1] if s is not None]) > 1 else 'single point'}.",
        "Step 4":  f"Binary labels at 70th percentile. n_positives ≈ {max(1, int((wk_idx+1)*0.3))} of {wk_idx+1} samples labelled class=1.",
        "Step 5":  f"8-model CV competition. Winner: {clf['name']} at {clf['cv']*100:.1f}% CV accuracy (±{clf['std']*100:.1f}%).",
        "Step 5B": f"CNN-1D filter inspection for {fn}. Identifies which coordinate pairs are most structurally significant.",
        "Step 6":  f"Refit all 8 models on full {wk_idx+1}-sample dataset. Plot P(class=1) distributions.",
        "Step 7":  f"CV winner confirmed: {clf['name']}. Filters 10,000 candidates → top 50% by P(class=1).",
        "Step 7B": f"Why {clf['name']} won: {clf['family']} family. CV accuracy {clf['cv']*100:.1f}%. See notebook for boundary analysis.",
        "Step 8":  f"Generate 10,000 candidates. exploit_ratio={hp.get('exploit_ratio','—')}, sigma={sigma_disp}. Rationale: {hp_rat[:120]}",
        "Step 9":  f"GP fit (Matérn 5/2) on {wk_idx+1} points. Strategy: {strat['action']}.",
        "Step 10": f"EI + UCB acquisition. Selected submission: {submission[:60] if submission not in ('—','[PENDING]') else '—'}",
        "Step 11": f"Per-dimension acquisition curves for {fn} {week_label}. sigma per dim = {sigma_disp}.",
        "Step 11B":f"Ollama llama3.1 Step 11B: {experiment[:150]}",
        "Step 12": f"GP surfaces for top-2 sensitive dimensions of {fn}.",
        "Step 13": f"Final dashboard. {week_label} submission: {submission}. {'⏳ Awaiting portal result.' if is_pending else f'Portal returned: {fmt(score_wk)}'}",
        "Step 14": f"ATB override check. What we learned: {learned[:150]}",
        "Step 15": f"Save hyperparameters to f{fn[1]}_w{wk_idx+1}_hyperparameters.json.",
    }

    context_text = step_context.get(step_key, "")

    st.markdown(f"""
    <div style='background:#0a1020;border:1px solid #141e30;border-radius:12px;
                padding:22px 24px;border-left:4px solid {color};margin-top:0.5rem'>
      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.62rem;color:{color};
                  text-transform:uppercase;letter-spacing:0.2em;margin-bottom:8px'>
        {step_data["step"]} · {fn} · {week_label}
      </div>
      <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:700;
                  color:#e8eeff;margin-bottom:12px'>
        {step_data["icon"]} {step_data["title"]}
      </div>
      <div style='color:#8a9abf;font-size:0.92rem;line-height:1.8;max-width:800px;margin-bottom:12px'>
        {step_data["desc"]}
      </div>
      <div style='background:#050810;border:1px solid #1a2540;border-left:3px solid {color};
                  border-radius:0 8px 8px 0;padding:10px 16px;font-family:"IBM Plex Mono",monospace;
                  font-size:0.78rem;color:#60a5fa;line-height:1.6'>
        {fn} · {week_label} · {context_text}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── What we learned this week ─────────────────────────────────────────────
    st.markdown(f'<div class="sec-head">What We Learned — {fn} · {week_label}</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>Result & Learning</div>
          <div class='info-card-body' style='font-size:0.85rem'>{learned}</div>
        </div>
        <div class='info-card'>
          <div class='info-card-title'>Experiment / Observation</div>
          <div class='info-card-body' style='font-size:0.85rem'>{experiment}</div>
        </div>
        """, unsafe_allow_html=True)
    with c2:
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>Hyperparameter Rationale</div>
          <div class='info-card-body' style='font-size:0.85rem'>{hp_rat}</div>
        </div>
        <div class='info-card'>
          <div class='info-card-title'>Parameters Used</div>
          <div class='info-card-body' style='font-size:0.85rem'>
            exploit_ratio = {hp.get('exploit_ratio','—')}<br>
            sigma = {sigma_disp}<br>
            ucb_kappa = {hp.get('ucb_kappa','—')}<br>
            gp_restarts = {hp.get('gp_restarts','—')}
          </div>
        </div>
        """, unsafe_allow_html=True)

    # ── All steps summary grid ────────────────────────────────────────────────
    st.markdown(f'<div class="sec-head">All Steps — {fn} · {week_label}</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, step in enumerate(PIPELINE_STEPS):
        col = cols[i % 3]
        c   = STEP_COLORS.get(step["icon"], "#2563eb")
        is_sel = step["step"] == step_key
        ctx = step_context.get(step["step"], "")[:80]
        with col:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid {"#1e3a6e" if is_sel else "#141e30"};
                        border-radius:8px;padding:12px 14px;margin-bottom:8px;
                        border-left:3px solid {c}'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:{c};margin-bottom:2px'>
                {step["step"]}</div>
              <div style='font-size:0.82rem;font-weight:600;color:#e8eeff;margin-bottom:4px'>
                {step["icon"]} {step["title"]}</div>
              <div style='font-size:0.70rem;color:#4a5a7a;line-height:1.4;margin-bottom:4px'>
                {step["desc"][:70]}…</div>
              <div style='font-size:0.68rem;color:#2563eb;font-family:"IBM Plex Mono",monospace;line-height:1.4'>
                {ctx}{"…" if len(ctx)==80 else ""}</div>
            </div>
            """, unsafe_allow_html=True)
