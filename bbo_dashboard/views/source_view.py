import streamlit as st
import plotly.graph_objects as go
import numpy as np
from data import FUNCTIONS, SCORES, STRATEGY, WEEKLY, COORDS, CLASSIFIERS, CV_RESULTS, TURBO_SUMMARY, PIPELINE_STEPS, CURRENT_WEEK, running_best, get_all_time_best

# Representative source code excerpts for each pipeline step
STEP_CODE = {
    "Step 0": '''# ─── Step 0: Config & Strategy ────────────────────────────────────────────
FUNCTION_ID   = "F7"
WEEK          = 7
MAXIMIZE      = True

EXPLOIT_RATIO  = 0.90          # 90% candidates from exploit distribution
EXPLOIT_SIGMA  = [0.015, 0.035, 0.035, 0.035, 0.035, 0.035]  # Anisotropic!
UCB_KAPPA      = 2.5
GP_RESTARTS    = 8

# Strategy box printout
W = 90
print("╔" + "═"*W + "╗")
print(f"║  WEEK {WEEK} · {FUNCTION_ID} · EXPLOIT W6 NEW BEST".ljust(W) + " ║")
print(f"║  σ = {EXPLOIT_SIGMA}  κ={UCB_KAPPA}  restarts={GP_RESTARTS}".ljust(W) + " ║")
print("╚" + "═"*W + "╝")''',

    "Step 1": '''# ─── Step 1: Data Load ────────────────────────────────────────────────────
import numpy as np, json, os

DATA_DIR = f"data/f{FUNCTION_ID[1]}_week{WEEK-1}/"
X_train  = np.load(DATA_DIR + f"f{FUNCTION_ID[1]}_w{WEEK-1}_inputs.npy")
y_train  = np.load(DATA_DIR + f"f{FUNCTION_ID[1]}_w{WEEK-1}_outputs.npy")

# Week log override — inject confirmed best coords
LOG_FILE = f"week_log_F{FUNCTION_ID[1]}.json"
if os.path.exists(LOG_FILE):
    with open(LOG_FILE) as f:
        log = json.load(f)
    best_coords = np.array(log["all_time_best_coords"])
    best_score  = log["all_time_best_score"]
    # Inject into training data if not already present
    if best_score not in y_train:
        X_train = np.vstack([X_train, best_coords])
        y_train = np.append(y_train, best_score)

n_dims  = X_train.shape[1]
n_train = X_train.shape[0]
print(f"Loaded: n={n_train}, dims={n_dims}, y∈[{y_train.min():.4f}, {y_train.max():.4f}]")''',

    "Step 4": '''# ─── Step 4: Candidate Generation ──────────────────────────────────────────
from scipy.stats import qmc

N_CANDIDATES   = 10_000
best_idx       = np.argmax(y_train) if MAXIMIZE else np.argmin(y_train)
best_point     = X_train[best_idx]

n_exploit = int(N_CANDIDATES * EXPLOIT_RATIO)
n_explore = N_CANDIDATES - n_exploit

# EXPLOIT: Gaussian around best point
# numpy broadcasts array sigma → anisotropic per-dimension widths
X_exploit = np.random.normal(0, EXPLOIT_SIGMA, (n_exploit, n_dims)) + best_point
X_exploit  = np.clip(X_exploit, 0, 1)

# EXPLORE: Sobol quasi-random sequence
sampler   = qmc.Sobol(d=n_dims, scramble=True)
X_explore = sampler.random(n_explore)

X_candidates = np.vstack([X_exploit, X_explore])
print(f"Generated {n_exploit} exploit + {n_explore} explore = {N_CANDIDATES} candidates")''',

    "Step 5": '''# ─── Step 5: Classifier Training (8 Models) ────────────────────────────────
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import StratifiedKFold, cross_val_score
from sklearn.preprocessing import StandardScaler
import torch, torch.nn as nn

THRESHOLD = np.percentile(y_train, 70)
y_binary  = (y_train >= THRESHOLD).astype(int) if MAXIMIZE else (y_train <= THRESHOLD).astype(int)

scaler = StandardScaler()
X_sc   = scaler.fit_transform(X_train)

models = {
    "Linear SVM":         SVC(kernel="linear", probability=True, C=1.0),
    "RBF SVM":            SVC(kernel="rbf",    probability=True, C=1.0),
    "Logistic Regression":LogisticRegression(max_iter=500),
    "Decision Tree":      DecisionTreeClassifier(max_depth=4),
    "Random Forest":      RandomForestClassifier(n_estimators=100),
    "Extra Trees":        ExtraTreesClassifier(n_estimators=100),
    "NN-Large":           MLPClassifier(hidden_layer_sizes=(64,32,16), max_iter=500),
    "CNN-1D":             TinyCNN(n_dims),  # custom PyTorch model
}

cv = StratifiedKFold(n_splits=5, shuffle=True)
results = {}
for name, model in models.items():
    if name != "CNN-1D":
        scores = cross_val_score(model, X_sc, y_binary, cv=cv, scoring="accuracy")
        results[name] = (scores.mean(), scores.std())

winner = max(results, key=lambda k: results[k][0])
print(f"Winner: {winner}  CV={results[winner][0]:.3f} ± {results[winner][1]:.3f}")''',

    "Step 5B": '''# ─── Step 5B: CNN Inspection (Module 17 Learning Exercise) ────────────────
import matplotlib.pyplot as plt
import torch

model = TinyCNN(n_dims)
# ... (training omitted) ...

# 1. PARAMETER COUNT
def count_params(m): return sum(p.numel() for p in m.parameters() if p.requires_grad)
print(f"TinyCNN params:  {count_params(cnn_model):,}")
print(f"NN-Large params: {count_params(nn_model):,}")

# 2. FILTER WEIGHTS — Conv1d(1→8, kernel_size=2)
weights = cnn_model.conv.weight.detach().cpu().numpy()  # shape (8, 1, 2)
fig, axes = plt.subplots(2, 4, figsize=(12, 4))
for i, ax in enumerate(axes.flat):
    w = weights[i, 0, :]  # [w0, w1]
    colors = ["#ef4444" if w[j] < 0 else "#22c55e" for j in range(2)]
    ax.bar(["w[0]", "w[1]"], w, color=colors)
    ax.set_title(f"Filter {i}", fontsize=9)
    ax.axhline(0, color="white", linewidth=0.5)
plt.suptitle("Conv1d Filter Weights — Learned Coord Pair Detectors")

# 3. FEATURE MAPS — best point activation
best_t = torch.FloatTensor(best_point).unsqueeze(0).unsqueeze(0)
with torch.no_grad():
    feat_maps = cnn_model.conv(best_t).squeeze().numpy()  # (8,)

peak_filter = np.argmax(feat_maps)
print(f"Peak activation: Filter {peak_filter}, value={feat_maps[peak_filter]:.4f}")
print(f"→ Coord pair [{peak_filter}, {peak_filter+1}] = [{best_point[peak_filter]:.4f}, {best_point[peak_filter+1]:.4f}]")''',

    "Step 9": '''# ─── Step 9: Gaussian Process Fit ──────────────────────────────────────────
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel

kernel = (
    ConstantKernel(1.0, (1e-3, 1e3))
    * Matern(length_scale=np.ones(n_dims), length_scale_bounds=(1e-2, 10.0), nu=2.5)
    + WhiteKernel(noise_level=1e-4, noise_level_bounds=(1e-8, 1e-1))
)

gp = GaussianProcessRegressor(
    kernel=kernel,
    alpha=1e-6,
    n_restarts_optimizer=GP_RESTARTS,
    normalize_y=True,
)
gp.fit(X_sc_filtered, y_filtered)

mu, sigma = gp.predict(X_sc_candidates, return_std=True)
length_scales = gp.kernel_.k1.k2.length_scale
print(f"GP R² = {gp.score(X_sc_filtered, y_filtered):.4f}")
print(f"Length scales: {length_scales}")''',

    "Step 10": '''# ─── Step 10: Acquisition Functions ────────────────────────────────────────
from scipy.stats import norm

f_best = y_filtered.max() if MAXIMIZE else y_filtered.min()

# Expected Improvement
Z   = (mu - f_best) / (sigma + 1e-9) if MAXIMIZE else (f_best - mu) / (sigma + 1e-9)
EI  = (mu - f_best) * norm.cdf(Z) + sigma * norm.pdf(Z) if MAXIMIZE \
      else (f_best - mu) * norm.cdf(Z) + sigma * norm.pdf(Z)
EI  = np.maximum(EI, 0)

# UCB
UCB = mu + UCB_KAPPA * sigma if MAXIMIZE else -(mu - UCB_KAPPA * sigma)

# Combined acquisition
EI_norm  = (EI  - EI.min())  / (EI.max()  - EI.min()  + 1e-9)
UCB_norm = (UCB - UCB.min()) / (UCB.max() - UCB.min() + 1e-9)
acq_combined = EI_norm + UCB_norm

best_idx   = np.argmax(acq_combined)
submission = X_candidates[best_idx]
print(f"Submission: {submission}")
print(f"EI={EI[best_idx]:.4f}  UCB={UCB[best_idx]:.4f}  μ={mu[best_idx]:.4f}  σ={sigma[best_idx]:.4f}")''',
}


def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if v != 0 and abs(v) < 0.001: return f"{v:.2e}"
    return f"{v:.4f}"

def render_step_chart(step_key, fn, wk_idx):
    """Render a live Plotly chart for pipeline steps that have visualisable data."""
    maximize = FUNCTIONS[fn]["objective"] == "MAXIMISE"
    scores   = SCORES[fn]
    actuals  = [s for s in scores if s is not None]
    n        = min(wk_idx + 1, len(actuals))
    week_labels = [f"W{i+1}" for i in range(n)]

    DARK = "#060a10"
    PLOT = "#0a1020"

    # ── Step 3: History Plot ──────────────────────────────────────────────────
    if step_key == "Step 3":
        sc = actuals[:n]
        rb = running_best(scores, maximize)[:n]
        bar_colors = ["#4a5a7a"]
        for i in range(1, len(sc)):
            imp = (sc[i] > sc[i-1]) if maximize else (sc[i] < sc[i-1])
            bar_colors.append("#22c55e" if imp else "#ef4444")
        if sc: bar_colors[-1] = "#38bdf8"
        fig = go.Figure()
        fig.add_trace(go.Bar(x=week_labels, y=sc, marker_color=bar_colors,
                             marker_line_width=0, opacity=0.9, name="Score",
                             text=[fmt(v) for v in sc], textposition="outside",
                             textfont=dict(size=10, color="white", family="IBM Plex Mono")))
        fig.add_trace(go.Scatter(x=week_labels, y=[r for r in rb if r is not None],
                                 mode="lines+markers", line=dict(color="#f59e0b", width=2, dash="dash"),
                                 marker=dict(size=5), name="Running best"))
        fig.update_layout(height=300, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                          font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                          margin=dict(l=10,r=10,t=30,b=10),
                          title=dict(text=f"{fn} — Historical Performance (W1–W{n})",
                                     font=dict(size=12, color="#c8d4f0")),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font_size=10),
                          xaxis=dict(gridcolor="#0d1320", showgrid=False),
                          yaxis=dict(gridcolor="#111827", showgrid=True))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Step 4: Binary Labels distribution ───────────────────────────────────
    elif step_key == "Step 4":
        sc = actuals[:n]
        if sc:
            threshold = np.percentile(sc, 70)
            colors = ["#22c55e" if (s >= threshold if maximize else s <= threshold) else "#ef4444" for s in sorted(sc)]
            fig = go.Figure(go.Bar(
                x=list(range(len(sc))), y=sorted(sc), marker_color=colors,
                text=[fmt(v) for v in sorted(sc)], textposition="outside",
                textfont=dict(size=9, color="white", family="IBM Plex Mono")))
            fig.add_hline(y=threshold, line_dash="dot", line_color="#f59e0b",
                          annotation_text=f"Top 30% threshold: {fmt(threshold)}",
                          annotation_font=dict(color="#f59e0b", size=9))
            fig.update_layout(height=280, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                              font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                              margin=dict(l=10,r=10,t=30,b=10),
                              title=dict(text=f"{fn} — Binary Labels (green=class 1, red=class 0)",
                                         font=dict(size=12, color="#c8d4f0")),
                              xaxis=dict(title="Rank (sorted)", showgrid=False),
                              yaxis=dict(gridcolor="#111827"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Step 5 / Step 7: CV Model Comparison — full league table ─────────────
    elif step_key in ("Step 5", "Step 7"):
        clf      = CLASSIFIERS[fn]
        cv_rows  = CV_RESULTS.get(fn, [])
        # Sort by cv descending
        cv_rows  = sorted(cv_rows, key=lambda x: x["cv"], reverse=True)
        names    = [r["name"] for r in cv_rows]
        cvs      = [r["cv"] for r in cv_rows]
        stds     = [r["std"] for r in cv_rows]
        colors   = ["#22c55e" if r["winner"] else "#4a6a9a" for r in cv_rows]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=names, x=cvs,
            orientation="h",
            marker_color=colors,
            marker_line_width=0,
            error_x=dict(type="data", array=stds, color="#7a8fbb", thickness=1.5, width=4),
            # Score inside bar on left, ± std outside on right
            text=[f"  {v:.1%} ± {s:.1%}" for v, s in zip(cvs, stds)],
            textposition="inside",
            insidetextanchor="start",
            textfont=dict(size=10, color="white", family="IBM Plex Mono"),
            hovertemplate="%{y}: <b>%{x:.1%}</b> ± %{error_x.array:.1%}<extra></extra>",
        ))
        fig.update_layout(
            height=320,
            paper_bgcolor=DARK, plot_bgcolor=PLOT,
            font=dict(color="#7a8fbb", family="IBM Plex Mono"),
            margin=dict(l=10, r=20, t=40, b=10),
            title=dict(text=f"{fn} — CV Model Comparison (all 8 models) · green = winner",
                       font=dict(size=11, color="#c8d4f0")),
            xaxis=dict(tickformat=".0%", range=[0, 1.05], gridcolor="#111827",
                       title=dict(text="CV Accuracy", font=dict(size=10))),
            yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
            bargap=0.25,
            uniformtext=dict(minsize=9, mode="hide"),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        # Winner rationale — why this model type wins
        _rationale = {
            "RF":     "Random Forest wins because ensemble averaging reduces variance on small datasets. "
                      "With n<50 samples, single trees overfit — 100-tree averaging provides stable P(class=1) estimates.",
            "DT":     "Decision Tree wins by learning hard threshold rules on boundary dimensions. "
                      "At high n/p ratios, the tree finds clear separating cuts (e.g. X1<0.1 or X5>0.9).",
            "SVM":    "Linear SVM wins because the high-value region is linearly separable in this function's space. "
                      "The maximum-margin hyperplane cleanly separates class 1 from class 0.",
            "CNN":    "CNN-1D wins by scanning adjacent coordinate pairs for local structure. "
                      "Its 8 filters detect coordinate relationships (e.g. X1≈0 AND X6>0.6) that scalar models miss.",
            "LogReg": "Logistic Regression wins due to the smooth, probabilistic landscape — "
                      "a linear decision boundary in log-odds space separates high from low regions effectively.",
        }
        # Find winner FIRST, then derive family
        _winner_row = next((r for r in cv_rows if r["winner"]), cv_rows[0])
        # Derive family from winner name, not CLASSIFIERS dict (which may be stale)
        _wname = _winner_row["name"]
        if "CNN" in _wname:           _fam = "CNN"
        elif "Forest" in _wname:      _fam = "RF"
        elif "Tree" in _wname:        _fam = "DT"
        elif "SVM" in _wname:         _fam = "SVM"
        elif "Logistic" in _wname:    _fam = "LogReg"
        else:                         _fam = clf["family"]
        _why = _rationale.get(_fam, "Selected by highest stratified k-fold CV accuracy across all 8 classifiers.")
        # Find the actual winner from CV_RESULTS
        st.markdown(f"""
        <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;
                    padding:14px 18px;margin-top:0.5rem;border-left:3px solid #22c55e'>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                      text-transform:uppercase;letter-spacing:0.18em;margin-bottom:6px'>
            ★ Winner: {_winner_row["name"]} · CV={_winner_row["cv"]:.1%} ± {_winner_row["std"]:.1%}</div>
          <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.75'>
            {_why}</div>
        </div>""", unsafe_allow_html=True)

    # ── Step 8: Candidate generation split ───────────────────────────────────
    elif step_key == "Step 8":
        strat = STRATEGY[fn]
        ratio = strat["exploit_ratio"]
        n_exploit = int(10000 * ratio)
        n_explore = 10000 - n_exploit
        fig = go.Figure(go.Pie(
            labels=["Exploit (Gaussian around best)", "Explore (uniform random)"],
            values=[n_exploit, n_explore],
            marker_colors=["#3b82f6", "#22c55e"],
            hole=0.55,
            textinfo="label+percent",
            textfont=dict(size=10, color="white", family="IBM Plex Mono"),
            hovertemplate="%{label}: %{value:,} candidates<extra></extra>"))
        sigma = strat.get("sigma", "—")
        sigma_str = f"{sigma}" if not isinstance(sigma, list) else f"aniso {sigma}"
        fig.update_layout(height=280, paper_bgcolor=DARK,
                          font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                          margin=dict(l=10,r=10,t=40,b=10),
                          title=dict(text=f"{fn} W{wk_idx+1} — 10,000 Candidates · σ={sigma_str}",
                                     font=dict(size=11, color="#c8d4f0")),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font_size=9, x=0.5, xanchor="center", y=-0.05))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Step 13: Submission dashboard ────────────────────────────────────────
    elif step_key == "Step 13":
        sc = actuals[:n]
        rb = running_best(scores, maximize)[:n]
        # Trajectory
        bar_colors = ["#4a5a7a"]
        for i in range(1, len(sc)):
            imp = (sc[i] > sc[i-1]) if maximize else (sc[i] < sc[i-1])
            bar_colors.append("#22c55e" if imp else "#ef4444")
        if sc: bar_colors[-1] = "#38bdf8"
        fig = go.Figure()
        fig.add_trace(go.Bar(x=week_labels, y=sc, marker_color=bar_colors,
                             marker_line_width=0, opacity=0.9, name="Score",
                             text=[fmt(v) for v in sc], textposition="outside",
                             textfont=dict(size=9, color="white", family="IBM Plex Mono")))
        fig.add_trace(go.Scatter(x=week_labels, y=[r for r in rb if r is not None],
                                 mode="lines+markers", line=dict(color="#f59e0b", width=2, dash="dash"),
                                 marker=dict(size=5), name="Running best"))
        atb = get_all_time_best(fn)
        fig.add_hline(y=atb, line_dash="dot", line_color="#f59e0b",
                      annotation_text=f"ATB: {fmt(atb)}",
                      annotation_font=dict(color="#f59e0b", size=9))
        fig.update_layout(height=300, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                          font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                          margin=dict(l=10,r=10,t=30,b=10),
                          title=dict(text=f"{fn} — Submission Dashboard · W{n} · ATB={fmt(atb)}",
                                     font=dict(size=12, color="#c8d4f0")),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font_size=10),
                          xaxis=dict(gridcolor="#0d1320", showgrid=False),
                          yaxis=dict(gridcolor="#111827"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        # Submission coords bar chart
        coords_wk = COORDS[fn][wk_idx] if wk_idx < len(COORDS[fn]) else None
        if coords_wk:
            dims = [f"X{i+1}" for i in range(len(coords_wk))]
            fig2 = go.Figure(go.Bar(
                x=dims, y=coords_wk,
                marker_color=["#38bdf8" if abs(c)<0.1 or abs(c-1)<0.1 else "#4a6a9a" for c in coords_wk],
                text=[f"{c:.4f}" for c in coords_wk], textposition="outside",
                textfont=dict(size=10, color="white", family="IBM Plex Mono")))
            fig2.update_layout(height=220, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                               font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                               margin=dict(l=10,r=10,t=30,b=10),
                               title=dict(text=f"Submitted Coordinates — W{wk_idx+1}",
                                          font=dict(size=11, color="#c8d4f0")),
                               xaxis=dict(showgrid=False),
                               yaxis=dict(gridcolor="#111827", range=[-0.05, 1.15]))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})

def render(fn, wk_idx):
    info   = FUNCTIONS[fn]
    weekly = WEEKLY[fn][wk_idx]
    week_label = f"W{wk_idx+1}"

    st.markdown(f"""
    <div class='page-hero'>
      <div class='page-eyebrow'>{fn} · {week_label} · Source Code</div>
      <div class='page-title'>Pipeline Source — {fn}</div>
      <div class='page-sub'>13-step BBO notebook · {info['dims']}D · {info['objective']}</div>
    </div>
    """, unsafe_allow_html=True)

    # Week / submission reminder
    sub_str = weekly.get("submission", "—")
    st.markdown(f"""
    <div class='sub-box'>
      <div class='sub-label'>{fn} · {week_label} · Submission String</div>
      {sub_str}
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sec-head">Select Pipeline Step to View Code</div>', unsafe_allow_html=True)

    step_options = [f"{s['step']} — {s['icon']} {s['title']}" for s in PIPELINE_STEPS]
    selected = st.selectbox("Pipeline Step", step_options, index=0)
    step_key = selected.split(" — ")[0]

    # Step description
    step_data = next((s for s in PIPELINE_STEPS if s["step"] == step_key), None)
    if step_data:
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>{step_data["icon"]} {step_data["title"]}</div>
          <div class='info-card-body'>{step_data["desc"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Live chart for this step
    CHART_STEPS = {"Step 3", "Step 4", "Step 5", "Step 7", "Step 8", "Step 13"}
    if step_key in CHART_STEPS:
        st.markdown('<div class="sec-head">Live Chart — This Step</div>', unsafe_allow_html=True)
        render_step_chart(step_key, fn, wk_idx)

    # Code block
    code = STEP_CODE.get(step_key)
    if code:
        st.markdown('<div class="sec-head">Code Excerpt</div>', unsafe_allow_html=True)
        st.code(code, language="python")
    else:
        st.markdown(f"""
        <div class='info-card'>
          <div class='info-card-title'>Code structure for {step_key}</div>
          <div class='info-card-body'>
            This step follows the standard BBO pipeline pattern. The full notebook
            (<code>Capstone_{fn}_W{wk_idx+1}.ipynb</code>) contains the complete implementation.
            See the GitHub repo for the downloadable .ipynb files.
          </div>
        </div>
        """, unsafe_allow_html=True)

    # All steps quick reference
    st.markdown('<div class="sec-head">All Steps — Quick Reference</div>', unsafe_allow_html=True)
    cols = st.columns(3)
    for i, step in enumerate(PIPELINE_STEPS):
        with cols[i % 3]:
            is_selected = step["step"] == step_key
            border_col = "#2563eb" if is_selected else "#141e30"
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid {border_col};border-radius:8px;
                        padding:10px 12px;margin-bottom:8px'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.62rem;
                          color:#2563eb;margin-bottom:3px'>{step["step"]}</div>
              <div style='font-size:0.80rem;font-weight:600;color:#e8eeff;margin-bottom:3px'>
                {step["icon"]} {step["title"]}</div>
              <div style='font-size:0.72rem;color:#4a5a7a;line-height:1.4'>{step["desc"][:80]}…</div>
            </div>
            """, unsafe_allow_html=True)
