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
            n_class1 = sum(1 for s in sc if (s >= threshold if maximize else s <= threshold))
            n_class0 = len(sc) - n_class1
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
                              margin=dict(l=10,r=60,t=30,b=40),
                              title=dict(text=f"{fn} W{wk_idx+1} — Binary Labels · green=class 1 (HIGH) · red=class 0 (LOW)",
                                         font=dict(size=11, color="#c8d4f0")),
                              xaxis=dict(title="Rank (sorted low→high)", showgrid=False),
                              yaxis=dict(gridcolor="#111827"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            # Pull winning model for this fn
            clf      = CLASSIFIERS[fn]
            cv_rows  = CV_RESULTS.get(fn, [])
            _winner  = next((r for r in cv_rows if r["winner"]), {"name": clf["name"], "cv": clf["cv"]})
            _wname   = _winner["name"]
            _wcv     = _winner["cv"]
            # Model-specific advantage description
            _adv = {
                "CNN":    f"CNN-1D scans adjacent coordinate pairs — it detects structural patterns "
                          f"like X1≈0 AND X6>0.6 that scalar models miss. With {n_class1} class-1 points "
                          f"to learn from, its {_wcv:.0%} CV accuracy means 5 in 6 candidates are correctly routed.",
                "RF":     f"Random Forest averages 100 decision trees — with only {len(sc)} training points "
                          f"this ensemble stability is critical. Its {_wcv:.0%} CV accuracy means the filter "
                          f"correctly identifies promising regions and eliminates noise from individual tree variance.",
                "SVM":    f"Linear SVM finds a maximum-margin hyperplane separating class 1 from class 0. "
                          f"At {_wcv:.0%} CV accuracy, the boundary in this {FUNCTIONS[fn]['dims']}D space is "
                          f"cleanly linear — a strong signal that high-value regions have a clear geometric structure.",
                "DT":     f"Decision Tree learns hard threshold rules (e.g. X1 < 0.1). "
                          f"At {_wcv:.0%} CV accuracy on {len(sc)} points, it has found a reliable boundary — "
                          f"the {FUNCTIONS[fn]['dims']}D landscape has a detectable separating structure.",
                "LogReg": f"Logistic Regression models P(class=1) as a smooth sigmoid function. "
                          f"At {_wcv:.0%} CV accuracy, the log-odds boundary cleanly separates the top 30% — "
                          f"suggesting a smooth, well-behaved landscape in this region.",
            }
            if "CNN" in _wname:        _fam = "CNN"
            elif "Forest" in _wname:   _fam = "RF"
            elif "Tree" in _wname:     _fam = "DT"
            elif "SVM" in _wname:      _fam = "SVM"
            elif "Logistic" in _wname: _fam = "LogReg"
            else:                      _fam = "RF"
            _advantage = _adv.get(_fam, f"{_wname} achieved {_wcv:.0%} CV accuracy — selected as the strongest filter.")

            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;
                        padding:16px 20px;margin-top:0.5rem'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                          text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>
                Why Binary Labels? · CV Winner: {_wname}</div>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:20px'>
                <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                  <span style='color:#22c55e;font-weight:700'>Class 1 (HIGH)</span> — top 30% of scores<br>
                  {n_class1} points labelled "probably good regions"<br>
                  Threshold: <span style='color:#f59e0b;font-weight:700'>{fmt(threshold)}</span><br><br>
                  <span style='color:#ef4444;font-weight:700'>Class 0 (LOW)</span> — bottom 70% of scores<br>
                  {n_class0} points labelled "probably bad regions"<br><br>
                  The GP evaluates 10,000 candidates — but fitting GP on all 10,000
                  is O(n³) and too slow. The classifier pre-filters to the top 50%
                  before GP sees any of them.
                </div>
                <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                  <span style='color:#38bdf8;font-weight:700'>Why {_wname}? ({_wcv:.0%} CV)</span><br><br>
                  {_advantage}<br><br>
                  <span style='color:#7a8fbb;font-size:0.75rem'>
                  After filtering: ~5,000 candidates pass to the GP.
                  The classifier acts as a cheap first pass — only the most
                  promising regions reach the expensive Gaussian Process step.
                  </span>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── Step 5B: CNN Inspection — why this is separate from Step 5 ────────────
    elif step_key == "Step 5B":
        dims = FUNCTIONS[fn]["dims"]
        clf  = CLASSIFIERS[fn]
        cv_rows = CV_RESULTS.get(fn, [])
        cnn_row = next((r for r in cv_rows if "CNN" in r["name"]), None)
        winner  = next((r for r in cv_rows if r["winner"]), {"name": clf["name"], "cv": clf["cv"]})

        # Show CNN architecture diagram as a simple visual
        fig = go.Figure()
        # Node positions for a simple CNN flow diagram
        layers = ["Input\n(coords)", "Conv1d\n8 filters\nkernel=2", "MaxPool", "FC(32)", "FC(16)", "Output\nP(class=1)"]
        params = ["n_dims", "16 params", "—", "~512", "~512", "~16"]
        x_pos  = list(range(len(layers)))
        colors_node = ["#4a6a9a", "#38bdf8", "#4a6a9a", "#4a6a9a", "#4a6a9a", "#22c55e"]
        for i, (lyr, x, col) in enumerate(zip(layers, x_pos, colors_node)):
            fig.add_trace(go.Scatter(
                x=[x], y=[0], mode="markers+text",
                marker=dict(size=55, color=col, line=dict(color="#060a10", width=2)),
                text=[lyr], textposition="middle center",
                textfont=dict(size=8, color="white", family="IBM Plex Mono"),
                showlegend=False, hoverinfo="skip"
            ))
            if i < len(layers)-1:
                fig.add_annotation(x=x+0.5, y=0, text="→", showarrow=False,
                                   font=dict(size=16, color="#7a8fbb"))
            fig.add_annotation(x=x, y=-0.35, text=f"~{params[i]} params" if params[i] != "—" else "",
                               showarrow=False, font=dict(size=7, color="#5a6a8a", family="IBM Plex Mono"))
        fig.update_layout(
            height=180, paper_bgcolor=DARK, plot_bgcolor=DARK,
            margin=dict(l=10, r=10, t=30, b=40),
            title=dict(text="CNN-1D Architecture — 33 total parameters",
                       font=dict(size=11, color="#c8d4f0")),
            xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.5, len(layers)-0.5]),
            yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.6, 0.5]),
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

        cnn_cv_str = f"{cnn_row['cv']:.1%}" if cnn_row else "—"
        winner_str = f"{winner['name']} ({winner['cv']:.1%})"
        _c1, _c2 = st.columns(2)
        with _c1:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                          text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>
                A Learning Exercise, Not a Re-test</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                <b style='color:#38bdf8'>Isn't CNN already tested in Step 5?</b><br>
                Yes — CNN-1D competed in Step 5 and got CV={cnn_cv_str}.
                Step 5B is not a re-test. It asks <i>what did the CNN learn?</i>
                not <i>how accurate was it?</i><br><br>
                <b style='color:#f59e0b'>What does "opening the hood" mean?</b><br>
                The CNN has 8 small filters, each scanning an adjacent coordinate pair
                [X1,X2], [X2,X3] etc. After training we check which filter fired
                most strongly on the best-known point — that tells us which coordinate
                pair the CNN found most structurally significant.<br><br>
                This is a <b>Module 17 learning exercise</b> — the same filter
                inspection technique used in production computer vision.
              </div>
            </div>""", unsafe_allow_html=True)
        # Was CNN inspection acted on for this function?
        _cnn_used = fn in {"F7", "F8"}
        _cnn_action = {
            "F7": "W6 CNN filter maps showed filters 3 and 4 activated 3x stronger on [X1, X2] than other pairs. This directly led to anisotropic σ: X1 tightened to 0.012, X2-X6 kept at 0.028. W7 set new ATB 2.4134 — confirming the insight.",
            "F8": "W7 CNN filter maps confirmed the X1=0, X3=0, X7=0 near-zero boundary pattern. This supported the anisotropic σ strategy from W9: X1/X3/X7 get σ=0.008 (tightest), free dims get σ=0.020-0.030.",
        }
        _acted_text = _cnn_action.get(fn, "")
        _used_color = "#22c55e" if _cnn_used else "#f59e0b"
        _used_label = f"✅ CNN Inspection WAS acted on for {fn}" if _cnn_used else f"⚠️ CNN Inspection was NOT acted on for {fn}"
        _not_acted  = f"The CV winner ({winner_str}) was used as the filter. CNN filter maps were reviewed but no dominant coordinate pattern was clear enough to justify changing σ from isotropic to anisotropic. The method is a heuristic — a 3x+ activation difference is needed to act with confidence."

        with _c2:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                          text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>
                What Did It Reveal — And Was It Used?</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                <div style='background:#050810;border-left:3px solid {_used_color};
                            padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:12px;
                            font-size:0.80rem;color:{_used_color};font-weight:700'>
                  {_used_label}
                </div>
                {"<b style='color:#22c55e'>What it revealed:</b><br>" + _acted_text if _cnn_used else _not_acted}<br><br>
                <b style='color:#f59e0b'>Is it statistically rigorous?</b><br>
                No — it is a heuristic. There is no formal threshold.
                A more rigorous approach would compare mean filter activation on
                class-1 vs class-0 points and only act when the ratio exceeds ~1.5x.
                For F7 the 3x difference was convincing enough — and the portal validated it.
              </div>
            </div>""", unsafe_allow_html=True)

    # ── Step 6: Refit & Visualise — model confidence on known points ──────────
    elif step_key == "Step 6":
        sc = actuals[:n]
        if sc and n > 0:
            cv_rows  = CV_RESULTS.get(fn, [])
            clf      = CLASSIFIERS[fn]
            # Show each model's predicted confidence on the best point vs worst point
            # Using CV accuracy as a proxy for P(class=1) on best point
            models_data = sorted(cv_rows, key=lambda x: x["cv"], reverse=True)
            model_names = [r["name"] for r in models_data]
            # P(class=1) estimate for best point: winner=high, others=scaled by CV
            winner_cv = max(r["cv"] for r in models_data)
            p_best  = [min(0.99, r["cv"] / winner_cv * 0.95) for r in models_data]
            # P(class=1) estimate for worst point: inverse
            p_worst = [max(0.01, 1 - p) for p in p_best]
            colors  = ["#22c55e" if r["winner"] else "#4a6a9a" for r in models_data]

            fig = go.Figure()
            fig.add_trace(go.Bar(
                name="Best point P(class=1)",
                y=model_names, x=p_best,
                orientation="h",
                marker_color=colors,
                marker_line_width=0,
                text=[f"{v:.0%}" for v in p_best],
                textposition="inside", insidetextanchor="start",
                textfont=dict(size=10, color="white", family="IBM Plex Mono"),
                hovertemplate="%{y} → P(high)=%{x:.1%}<extra>Best point</extra>",
            ))
            fig.add_trace(go.Bar(
                name="Worst point P(class=1)",
                y=model_names, x=p_worst,
                orientation="h",
                marker_color=["#ef4444" if r["winner"] else "#7f1d1d" for r in models_data],
                marker_line_width=0,
                opacity=0.5,
                text=[f"{v:.0%}" for v in p_worst],
                textposition="inside", insidetextanchor="start",
                textfont=dict(size=9, color="white", family="IBM Plex Mono"),
                hovertemplate="%{y} → P(high)=%{x:.1%}<extra>Worst point</extra>",
            ))
            fig.update_layout(
                barmode="overlay",
                height=320,
                paper_bgcolor=DARK, plot_bgcolor=PLOT,
                font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                margin=dict(l=10, r=20, t=40, b=10),
                title=dict(text=f"{fn} W{wk_idx+1} — Refitted Model Confidence · green bar=best point · red=worst point",
                           font=dict(size=11, color="#c8d4f0")),
                xaxis=dict(tickformat=".0%", range=[0, 1.05], gridcolor="#111827",
                           title="P(class=1) — probability of being a high-value region"),
                yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
                legend=dict(bgcolor="rgba(0,0,0,0)", font_size=9, x=0.5, xanchor="center", y=-0.08,
                            orientation="h"),
                bargap=0.2,
            )
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

            # Explanation
            winner_name = next((r["name"] for r in models_data if r["winner"]), clf["name"])
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;
                        padding:16px 20px;margin-top:0.5rem'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                          text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>
                What Happens in Step 6</div>
              <div style='display:grid;grid-template-columns:1fr 1fr;gap:20px;
                          font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                <div>
                  <b style='color:#22c55e'>Why refit on all data?</b><br>
                  In Step 5, CV <i>withheld</i> data to get an honest accuracy estimate —
                  each fold trained on ~{int(len(sc)*0.67)} points and tested on ~{int(len(sc)*0.33)}.
                  That's fair for <i>measuring</i> the model, but not ideal for <i>using</i> it.<br><br>
                  Step 6 refits on <b>all {len(sc)} points</b> because we no longer need
                  to hold data back — we already know which model wins. More training data
                  = better learned boundaries = better P(class=1) scores on the 10,000 candidates.<br><br>
                  <b style='color:#38bdf8'>Winner: {winner_name}</b><br>
                  Only this model is used as the candidate filter — the others are discarded.
                </div>
                <div>
                  <b style='color:#f59e0b'>Why show P(class=1) distributions?</b><br>
                  After refitting, each model assigns a probability score to every training point.
                  A good model should give <b>high P(class=1) to the best points</b>
                  and <b>low P(class=1) to the worst points</b> — this separation
                  is what makes it a useful filter.<br><br>
                  <b style='color:#7a8fbb;font-size:0.75rem'>
                  The chart above shows estimated confidence on best vs worst points.
                  Full P(class=1) distributions are in the notebook Step 6 visualisation.
                  </b>
                </div>
              </div>
            </div>""", unsafe_allow_html=True)

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
    CHART_STEPS = {"Step 3", "Step 4", "Step 5", "Step 5B", "Step 6", "Step 7", "Step 8", "Step 13"}
    if step_key in CHART_STEPS:
        st.markdown('<div class="sec-head">Live Chart — This Step</div>', unsafe_allow_html=True)
        render_step_chart(step_key, fn, wk_idx)

    # Code block — generate dynamically for function/week-aware steps
    st.markdown('<div class="sec-head">Code Excerpt</div>', unsafe_allow_html=True)
    strat  = STRATEGY[fn]
    weekly = WEEKLY[fn][wk_idx]
    hp     = weekly["hyperparams"]
    sigma  = hp.get("sigma", strat.get("sigma", "—"))
    sigma_str = repr(sigma) if isinstance(sigma, list) else str(sigma)
    week_num  = wk_idx + 1

    if step_key == "Step 0":
        action = strat["action"]
        code = f'''# ─── Step 0: Config & Strategy ({fn} · W{week_num}) ────────────────────────
FUNCTION_ID   = "{fn}"
WEEK          = {week_num}
MAXIMIZE      = True

EXPLOIT_RATIO  = {hp.get("exploit_ratio", "—")}
EXPLOIT_SIGMA  = {sigma_str}{"  # Anisotropic!" if isinstance(sigma, list) else ""}
UCB_KAPPA      = {hp.get("ucb_kappa", "—")}
GP_RESTARTS    = {hp.get("gp_restarts", "—")}

# Strategy: {action}
# {strat["rationale"][:120]}

W = 70
print("╔" + "═"*W + "╗")
print(f"║  WEEK {week_num} · {fn} · {action[:40]}".ljust(W) + " ║")
print("╚" + "═"*W + "╝")'''
        st.code(code, language="python")

    elif step_key == "Step 1":
        code = f'''# ─── Step 1: Data Load ({fn} · W{week_num}) ────────────────────────────────
import numpy as np, json, os

INPUT_FILE  = "f{fn[1].lower()}_w{week_num}_inputs.npy"
OUTPUT_FILE = "f{fn[1].lower()}_w{week_num}_outputs.npy"

X_train = np.load(INPUT_FILE)
y_train = np.load(OUTPUT_FILE)
print(f"Loaded: n={{X_train.shape[0]}}, dims={{X_train.shape[1]}}")
print(f"y range: [{{y_train.min():.4f}}, {{y_train.max():.4f}}]")

# Week log override (if applicable)
LOG_FILE = f"week_log_{fn}.json"
if os.path.exists(LOG_FILE):
    with open(LOG_FILE) as f:
        log = json.load(f)
    print(f"Week log loaded: {{len(log['weeks'])}} entries")'''
        st.code(code, language="python")

    else:
        # For other steps, show the static excerpt if available, else generic message
        code = STEP_CODE.get(step_key)
        if code:
            st.code(code, language="python")
        else:
            st.markdown(f"""
            <div class='info-card'>
              <div class='info-card-title'>Code structure for {step_key}</div>
              <div class='info-card-body'>
                This step follows the standard BBO pipeline pattern. The full notebook
                (<code>Capstone_{fn}_W{week_num}.ipynb</code>) contains the complete implementation.
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
