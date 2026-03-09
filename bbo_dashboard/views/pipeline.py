import streamlit as st
import plotly.graph_objects as go
from data import PIPELINE_STEPS, FUNCTIONS, STRATEGY, CLASSIFIERS

STEP_COLORS = {
    "⚙️":"#6366f1","📂":"#3b82f6","🔬":"#06b6d4","📊":"#10b981","🏷️":"#f59e0b",
    "🤖":"#8b5cf6","🔍":"#ec4899","🎨":"#14b8a6","📈":"#f97316","🎲":"#84cc16",
    "🧠":"#f97316","🌐":"#06b6d4","🎯":"#3b82f6","📉":"#8b5cf6","🗺️":"#10b981","🏆":"#f59e0b",
}

def render(fn=None):
    st.markdown("""
    <div class='page-hero'>
      <div class='page-eyebrow'>BBO Pipeline · All Functions</div>
      <div class='page-title'>13-Step Pipeline</div>
      <div class='page-sub'>Fixed notebook structure used each week for all 8 functions</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Visual Pipeline Flow</div>', unsafe_allow_html=True)

    n = len(PIPELINE_STEPS)
    xs = list(range(n))
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=xs, y=[0]*n, mode="lines",
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

    st.markdown('<div class="sec-head">Step-by-Step Detail</div>', unsafe_allow_html=True)

    selected_step = st.selectbox(
        "Select Step",
        [f"{s['step']} — {s['icon']} {s['title']}" for s in PIPELINE_STEPS],
        index=0,
    )
    step_key = selected_step.split(" — ")[0]
    step_data = next(s for s in PIPELINE_STEPS if s["step"] == step_key)
    color = STEP_COLORS.get(step_data["icon"], "#2563eb")

    st.markdown(f"""
    <div style='background:#0a1020;border:1px solid #141e30;border-radius:12px;
                padding:22px 24px;border-left:4px solid {color};margin-top:0.5rem'>
      <div style='font-family:"IBM Plex Mono",monospace;font-size:0.62rem;color:{color};
                  text-transform:uppercase;letter-spacing:0.2em;margin-bottom:8px'>
        {step_data["step"]}
      </div>
      <div style='font-family:Syne,sans-serif;font-size:1.4rem;font-weight:700;
                  color:#e8eeff;margin-bottom:12px'>
        {step_data["icon"]} {step_data["title"]}
      </div>
      <div style='color:#8a9abf;font-size:0.92rem;line-height:1.8;max-width:800px'>
        {step_data["desc"]}
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">All Steps Summary</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, step in enumerate(PIPELINE_STEPS):
        col = cols[i % 3]
        c = STEP_COLORS.get(step["icon"], "#2563eb")
        is_sel = step["step"] == step_key
        with col:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid {"#1e3a6e" if is_sel else "#141e30"};
                        border-radius:8px;padding:12px 14px;margin-bottom:8px;
                        border-left:3px solid {c}'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:{c};margin-bottom:2px'>
                {step["step"]}</div>
              <div style='font-size:0.82rem;font-weight:600;color:#e8eeff;margin-bottom:4px'>
                {step["icon"]} {step["title"]}</div>
              <div style='font-size:0.72rem;color:#4a5a7a;line-height:1.4'>
                {step["desc"][:90]}…</div>
            </div>
            """, unsafe_allow_html=True)
