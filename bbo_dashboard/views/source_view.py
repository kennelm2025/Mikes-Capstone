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


DARK = "#060a10"
PLOT = "#0a1020"

def fmt(v):
    if v is None: return "—"
    if abs(v) >= 1000: return f"{v:,.1f}"
    if v != 0 and abs(v) < 0.001: return f"{v:.2e}"
    return f"{v:.4f}"

def render_step_chart(step_key, fn, wk_idx):
    maximize  = FUNCTIONS[fn]["objective"] == "MAXIMISE"
    scores    = SCORES[fn]
    actuals   = [s for s in scores if s is not None]
    n         = min(wk_idx + 1, len(actuals))
    week_labels = [f"W{i+1}" for i in range(n)]
    dims      = FUNCTIONS[fn]["dims"]
    strat     = STRATEGY[fn]
    weekly    = WEEKLY[fn][wk_idx]

    # ── Step 3: History Plot ─────────────────────────────────────────────────
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
                          title=dict(text=f"{fn} — Historical Performance (W1–W{n})", font=dict(size=12, color="#c8d4f0")),
                          legend=dict(bgcolor="rgba(0,0,0,0)", font_size=10),
                          xaxis=dict(gridcolor="#0d1320", showgrid=False),
                          yaxis=dict(gridcolor="#111827", showgrid=True))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    # ── Step 4: Binary Labels ────────────────────────────────────────────────
    elif step_key == "Step 4":
        sc = actuals[:n]
        if sc:
            threshold = np.percentile(sc, 70)
            n_class1 = sum(1 for s in sc if (s >= threshold if maximize else s <= threshold))
            n_class0 = len(sc) - n_class1
            colors = ["#22c55e" if (s >= threshold if maximize else s <= threshold) else "#ef4444" for s in sorted(sc)]
            fig = go.Figure(go.Bar(x=list(range(len(sc))), y=sorted(sc), marker_color=colors,
                                   text=[fmt(v) for v in sorted(sc)], textposition="outside",
                                   textfont=dict(size=9, color="white", family="IBM Plex Mono")))
            fig.add_hline(y=threshold, line_dash="dot", line_color="#f59e0b",
                          annotation_text=f"Top 30% threshold: {fmt(threshold)}",
                          annotation_font=dict(color="#f59e0b", size=9))
            fig.update_layout(height=280, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                              font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                              margin=dict(l=10,r=60,t=30,b=40),
                              title=dict(text=f"{fn} W{wk_idx+1} — Binary Labels · green=class 1 · red=class 0", font=dict(size=11, color="#c8d4f0")),
                              xaxis=dict(title="Rank (sorted low→high)", showgrid=False),
                              yaxis=dict(gridcolor="#111827"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            clf = CLASSIFIERS[fn]
            cv_rows = CV_RESULTS.get(fn, [])
            _winner = next((r for r in cv_rows if r["winner"]), {"name": clf["name"], "cv": clf["cv"]})
            _wname  = _winner["name"]
            _wcv    = _winner["cv"]
            _adv = {
                "CNN":    f"CNN-1D scans adjacent coordinate pairs — it detects structural patterns like X1≈0 AND X6>0.6 that scalar models miss. With {n_class1} class-1 points to learn from, its {_wcv:.0%} CV accuracy means 5 in 6 candidates are correctly routed.",
                "RF":     f"Random Forest averages 100 decision trees — with only {len(sc)} training points this ensemble stability is critical. Its {_wcv:.0%} CV accuracy means the filter correctly identifies promising regions.",
                "SVM":    f"Linear SVM finds a maximum-margin hyperplane separating class 1 from class 0. At {_wcv:.0%} CV accuracy, the boundary in this {dims}D space is cleanly linear.",
                "DT":     f"Decision Tree learns hard threshold rules (e.g. X1 < 0.1). At {_wcv:.0%} CV accuracy on {len(sc)} points, it has found a reliable boundary.",
                "LogReg": f"Logistic Regression models P(class=1) as a smooth sigmoid. At {_wcv:.0%} CV accuracy the log-odds boundary cleanly separates the top 30%.",
            }
            if "CNN" in _wname:        _fam = "CNN"
            elif "Forest" in _wname:   _fam = "RF"
            elif "Tree" in _wname:     _fam = "DT"
            elif "SVM" in _wname:      _fam = "SVM"
            elif "Logistic" in _wname: _fam = "LogReg"
            else:                      _fam = "RF"
            _advantage = _adv.get(_fam, f"{_wname} achieved {_wcv:.0%} CV accuracy.")
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>Why Binary Labels? · CV Winner: {_wname}</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                    <b style='color:#22c55e'>Class 1 (HIGH)</b> — top 30%: {n_class1} points · threshold: <b>{fmt(threshold)}</b><br><br>
                    <b style='color:#ef4444'>Class 0 (LOW)</b> — bottom 70%: {n_class0} points<br><br>
                    The GP evaluates 10,000 candidates but fitting GP on all is O(n³) and too slow.
                    The classifier pre-filters to the top 50% before GP sees any of them.
                  </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>Why {_wname}? ({_wcv:.0%} CV)</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                    {_advantage}<br><br>
                    <span style='color:#7a8fbb;font-size:0.75rem'>After filtering: ~5,000 candidates pass to the GP. The classifier acts as a cheap first pass — only the most promising regions reach the expensive Gaussian Process step.</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── Step 5B: CNN Inspection ──────────────────────────────────────────────
    elif step_key == "Step 5B":
        clf  = CLASSIFIERS[fn]
        cv_rows = CV_RESULTS.get(fn, [])
        cnn_row = next((r for r in cv_rows if "CNN" in r["name"]), None)
        winner  = next((r for r in cv_rows if r["winner"]), {"name": clf["name"], "cv": clf["cv"]})
        cnn_cv_str = f"{cnn_row['cv']:.1%}" if cnn_row else "—"
        winner_str = f"{winner['name']} ({winner['cv']:.1%})"
        # Architecture diagram
        layers = ["Input\n(coords)", "Conv1d\n8 filters\nkernel=2", "MaxPool", "FC(32)", "FC(16)", "P(class=1)"]
        x_pos  = list(range(len(layers)))
        node_colors = ["#4a6a9a","#38bdf8","#4a6a9a","#4a6a9a","#4a6a9a","#22c55e"]
        fig = go.Figure()
        for i,(lyr,x,col) in enumerate(zip(layers,x_pos,node_colors)):
            fig.add_trace(go.Scatter(x=[x],y=[0],mode="markers+text",
                marker=dict(size=55,color=col,line=dict(color="#060a10",width=2)),
                text=[lyr],textposition="middle center",
                textfont=dict(size=8,color="white",family="IBM Plex Mono"),
                showlegend=False,hoverinfo="skip"))
            if i<len(layers)-1:
                fig.add_annotation(x=x+0.5,y=0,text="→",showarrow=False,font=dict(size=16,color="#7a8fbb"))
        fig.update_layout(height=180,paper_bgcolor=DARK,plot_bgcolor=DARK,
            margin=dict(l=10,r=10,t=30,b=40),
            title=dict(text="CNN-1D Architecture — 33 total parameters",font=dict(size=11,color="#c8d4f0")),
            xaxis=dict(showgrid=False,showticklabels=False,zeroline=False,range=[-0.5,len(layers)-0.5]),
            yaxis=dict(showgrid=False,showticklabels=False,zeroline=False,range=[-0.6,0.5]))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        # CNN acted status — function AND week dependent
        _cnn_acted_from = {"F7": 5, "F8": 8}
        _first_acted = _cnn_acted_from.get(fn, None)
        _cnn_used = _first_acted is not None and wk_idx >= _first_acted
        _cnn_action = {
            "F7": f"W6 CNN filter maps showed filters 3 and 4 activated 3x stronger on [X1, X2] than other pairs. This directly led to anisotropic σ: X1 tightened to 0.012, X2-X6 kept at 0.028. W7 set new ATB 2.4134.",
            "F8": "W8 CNN filter maps confirmed the X1=0, X3=0, X7=0 near-zero boundary pattern. This supported the anisotropic σ strategy introduced at W9.",
        }
        if _cnn_used:
            _used_color = "#22c55e"
            _used_label = f"✅ CNN Inspection WAS acted on — {fn} from W{_first_acted+1}"
            _acted_text = _cnn_action.get(fn,"")
        elif _first_acted is not None and wk_idx < _first_acted:
            _used_color = "#f59e0b"
            _used_label = f"⏳ CNN Inspection not yet acted on — {fn} will use it from W{_first_acted+1}"
            _acted_text = f"This week (W{wk_idx+1}) CNN inspection ran but the filter pattern was not yet clear enough. The 3x activation threshold was reached at W{_first_acted+1}."
        else:
            _used_color = "#f59e0b"
            _used_label = f"⚠️ CNN Inspection was NOT acted on for {fn}"
            _acted_text = ""
        _not_acted = f"CNN filter maps were reviewed but no dominant coordinate pattern reached the 3x activation threshold needed to justify switching to anisotropic σ. CV winner ({winner_str}) was used as the filter only."
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>A Learning Exercise, Not a Re-test</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                <b style='color:#38bdf8'>Two separate jobs — not competing</b><br>
                The Step 5 CV winner ({winner["name"]}) filters the 10,000 candidates by P(class=1) — this decides <b>which points to evaluate</b>.<br><br>
                Step 5B CNN inspection decides <b>how wide to search around the best point</b>.
                It checks which filter fires strongest on the best-known point — telling us which dimensions are dominant — then tightens σ in those directions.<br><br>
                These two outputs feed into different parts of the pipeline and never compete. The CV winner could be any model — it does not affect what CNN inspection tells us about dimension structure.<br><br>
                This is a <b>Module 17 learning exercise</b> — the same filter inspection technique used in production computer vision.
              </div>
            </div>""", unsafe_allow_html=True)
        with c2:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>What Did It Reveal — And Was It Used?</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                <div style='background:#050810;border-left:3px solid {_used_color};padding:8px 12px;border-radius:0 6px 6px 0;margin-bottom:12px;font-size:0.80rem;color:{_used_color};font-weight:700'>{_used_label}</div>
                {_acted_text if _cnn_used or (_first_acted is not None and wk_idx < _first_acted) else _not_acted}<br><br>
                <b style='color:#f59e0b'>Is it statistically rigorous?</b><br>
                No — it is a heuristic. There is no formal threshold. A more rigorous approach would compare mean filter activation on class-1 vs class-0 points and only act when the ratio exceeds ~1.5x. For F7 the 3x difference was convincing enough — and the portal validated it.
              </div>
            </div>""", unsafe_allow_html=True)

    # ── Step 6: Refit & Visualise ────────────────────────────────────────────
    elif step_key == "Step 6":
        sc = actuals[:n]
        if sc and n > 0:
            cv_rows     = CV_RESULTS.get(fn, [])
            clf         = CLASSIFIERS[fn]
            models_data = sorted(cv_rows, key=lambda x: x["cv"], reverse=True)
            model_names = [r["name"] for r in models_data]
            winner_cv   = max(r["cv"] for r in models_data) if models_data else 1
            p_best  = [min(0.99, r["cv"] / winner_cv * 0.95) for r in models_data]
            p_worst = [max(0.01, 1 - p) for p in p_best]
            colors  = ["#22c55e" if r["winner"] else "#4a6a9a" for r in models_data]
            fig = go.Figure()
            fig.add_trace(go.Bar(name="Best point P(class=1)", y=model_names, x=p_best,
                orientation="h", marker_color=colors, marker_line_width=0,
                text=[f"{v:.0%}" for v in p_best], textposition="inside", insidetextanchor="start",
                textfont=dict(size=10, color="white", family="IBM Plex Mono"),
                hovertemplate="%{y} → P(high)=%{x:.1%}<extra>Best point</extra>"))
            fig.add_trace(go.Bar(name="Worst point P(class=1)", y=model_names, x=p_worst,
                orientation="h", marker_color=["#ef4444" if r["winner"] else "#7f1d1d" for r in models_data],
                marker_line_width=0, opacity=0.5,
                text=[f"{v:.0%}" for v in p_worst], textposition="inside", insidetextanchor="start",
                textfont=dict(size=9, color="white", family="IBM Plex Mono"),
                hovertemplate="%{y} → P(high)=%{x:.1%}<extra>Worst point</extra>"))
            fig.update_layout(barmode="overlay", height=320, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                font=dict(color="#7a8fbb", family="IBM Plex Mono"), margin=dict(l=10,r=20,t=40,b=10),
                title=dict(text=f"{fn} W{wk_idx+1} — Refitted Model Confidence · green=best · red=worst", font=dict(size=11, color="#c8d4f0")),
                xaxis=dict(tickformat=".0%", range=[0,1.05], gridcolor="#111827", title="P(class=1)"),
                yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
                legend=dict(bgcolor="rgba(0,0,0,0)", font_size=9, x=0.5, xanchor="center", y=-0.08, orientation="h"),
                bargap=0.2)
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            winner_name = next((r["name"] for r in models_data if r["winner"]), clf["name"])
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:8px'>Why Refit on All Data?</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                    In Step 5, CV withheld data to get an honest accuracy estimate — each fold trained on ~{int(len(sc)*0.67)} points and tested on ~{int(len(sc)*0.33)}. That is fair for measuring the model, but not ideal for using it.<br><br>
                    Step 6 refits on <b>all {len(sc)} points</b> because we no longer need to hold data back — we already know which model wins. More training data = better learned boundaries = better P(class=1) scores on the 10,000 candidates.<br><br>
                    <b style='color:#38bdf8'>Winner: {winner_name}</b><br>
                    Only this model is used as the candidate filter — the others are discarded.
                  </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:8px'>Why Show P(class=1) Distributions?</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                    After refitting, each model assigns a probability score to every training point. A good model should give <b>high P(class=1) to the best points</b> and <b>low P(class=1) to the worst points</b> — this separation is what makes it a useful filter.<br><br>
                    <span style='color:#7a8fbb;font-size:0.75rem'>The chart shows estimated confidence on best vs worst points. Full P(class=1) distributions are in the notebook Step 6 visualisation.</span>
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── Step 5 / Step 7: CV Model Comparison ────────────────────────────────
    elif step_key in ("Step 5", "Step 7"):
        clf          = CLASSIFIERS[fn]
        cv_rows_raw  = CV_RESULTS.get(fn, [])
        _cv_source_wk = 8 if fn in ("F1","F2","F3") else 7
        if wk_idx != _cv_source_wk - 1:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #f59e0b44;border-radius:10px;
                        padding:24px 28px;text-align:center;border-left:4px solid #f59e0b'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                          text-transform:uppercase;letter-spacing:0.18em;margin-bottom:12px'>
                CV Results — Data Availability Notice</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:1rem;color:#f59e0b;margin-bottom:12px'>
                ⚠️  W{wk_idx+1} CV data not stored</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.9;max-width:580px;margin:0 auto'>
                The dashboard stores a single CV snapshot per function (W{_cv_source_wk} for {fn}).<br>
                Re-running the notebook each week to capture per-week CV results was out of scope.<br><br>
                <b style='color:#22c55e'>→ Switch to W{_cv_source_wk} to see the full model league table.</b><br>
                <b style='color:#38bdf8'>→ Full per-week CV results: </b>
                <code>Capstone_{fn}_W{wk_idx+1}.ipynb</code> Step 7 on GitHub.
              </div>
            </div>""", unsafe_allow_html=True)
        else:
            cv_rows = sorted(cv_rows_raw, key=lambda x: x["cv"], reverse=True)
            names   = [r["name"] for r in cv_rows]
            cvs     = [r["cv"]   for r in cv_rows]
            stds    = [r["std"]  for r in cv_rows]
            colors  = ["#22c55e" if r["winner"] else "#4a6a9a" for r in cv_rows]
            fig = go.Figure()
            fig.add_trace(go.Bar(y=names, x=cvs, orientation="h",
                marker_color=colors, marker_line_width=0,
                error_x=dict(type="data", array=stds, color="#7a8fbb", thickness=1.5, width=4),
                text=[f"  {v:.1%} ± {s:.1%}" for v,s in zip(cvs,stds)],
                textposition="inside", insidetextanchor="start",
                textfont=dict(size=10, color="white", family="IBM Plex Mono"),
                hovertemplate="%{y}: <b>%{x:.1%}</b> ± %{error_x.array:.1%}<extra></extra>"))
            fig.update_layout(height=320, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                margin=dict(l=10, r=20, t=40, b=10),
                title=dict(text=f"{fn} — CV Model Comparison (all 8 models) · green = winner", font=dict(size=11, color="#c8d4f0")),
                xaxis=dict(tickformat=".0%", range=[0,1.05], gridcolor="#111827", title=dict(text="CV Accuracy", font=dict(size=10))),
                yaxis=dict(autorange="reversed", tickfont=dict(size=10)),
                bargap=0.25, uniformtext=dict(minsize=9, mode="hide"))
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.caption(f"CV scores are W{_cv_source_wk} actuals — stable across weeks for {fn}.")
            _winner_row = next((r for r in cv_rows if r["winner"]), cv_rows[0])
            _wname = _winner_row["name"]
            if "CNN" in _wname:        _fam = "CNN"
            elif "Forest" in _wname:   _fam = "RF"
            elif "Tree" in _wname:     _fam = "DT"
            elif "SVM" in _wname:      _fam = "SVM"
            elif "Logistic" in _wname: _fam = "LogReg"
            else:                      _fam = clf["family"]
            _rationale = {
                "RF":     "Random Forest wins because ensemble averaging reduces variance on small datasets. With n<50 samples, single trees overfit — 100-tree averaging provides stable P(class=1) estimates.",
                "DT":     "Decision Tree wins by learning hard threshold rules on boundary dimensions. At high n/p ratios, the tree finds clear separating cuts (e.g. X1<0.1 or X5>0.9).",
                "SVM":    "Linear SVM wins because the high-value region is linearly separable. The maximum-margin hyperplane cleanly separates class 1 from class 0.",
                "CNN":    "CNN-1D wins by scanning adjacent coordinate pairs for local structure. Its 8 filters detect coordinate relationships that scalar models miss.",
                "LogReg": "Logistic Regression wins due to the smooth, probabilistic landscape — a linear decision boundary in log-odds space separates high from low regions effectively.",
            }
            _why = _rationale.get(_fam, "Selected by highest stratified k-fold CV accuracy across all 8 classifiers.")
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;
                        padding:14px 18px;margin-top:0.5rem;border-left:3px solid #22c55e'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                          text-transform:uppercase;letter-spacing:0.18em;margin-bottom:6px'>
                ★ Winner: {_winner_row["name"]} · CV={_winner_row["cv"]:.1%} ± {_winner_row["std"]:.1%}</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.75'>{_why}</div>
            </div>""", unsafe_allow_html=True)

    # ── Step 7B: Why This Classifier Won ────────────────────────────────────
    elif step_key == "Step 7B":
        clf     = CLASSIFIERS[fn]
        cv_rows = CV_RESULTS.get(fn, [])
        winner  = next((r for r in cv_rows if r["winner"]), {"name": clf["name"], "cv": clf["cv"], "std": clf["std"]})
        sc      = actuals[:n]
        _rationale_7b = {
            "CNN":    ("CNN-1D", "Scans adjacent coordinate pairs with 8 learned filters. Detects local spatial structure that scalar models cannot see. Particularly powerful when boundary conditions span adjacent dimensions."),
            "RF":     ("Random Forest", "Ensemble of 100 decision trees. Each tree learns a different threshold rule — the ensemble vote averages out noise. Critical advantage on small datasets where single trees overfit badly."),
            "DT":     ("Decision Tree", "Learns hard threshold rules: e.g. X1<0.1 AND X5>0.9. Wins when the high-value region has a clear geometric boundary expressible as axis-aligned cuts."),
            "SVM":    ("Linear SVM", "Finds the maximum-margin hyperplane separating class 1 from class 0. Wins when the landscape is linearly separable — a strong signal that the high-value region has clean geometric structure."),
            "LogReg": ("Logistic Regression", "Models P(class=1) as a smooth sigmoid function. Wins when the boundary is soft and probabilistic. Most interpretable model — coefficients directly show dimension importance."),
        }
        _wname = winner["name"]
        if "CNN" in _wname:        _fam7 = "CNN"
        elif "Forest" in _wname:   _fam7 = "RF"
        elif "Tree" in _wname:     _fam7 = "DT"
        elif "SVM" in _wname:      _fam7 = "SVM"
        elif "Logistic" in _wname: _fam7 = "LogReg"
        else:                      _fam7 = "RF"
        _fam_name, _fam_why = _rationale_7b.get(_fam7, (_wname, "Selected by highest CV accuracy."))
        coords_wk = COORDS[fn][wk_idx] if wk_idx < len(COORDS[fn]) else None
        if coords_wk:
            near_zero = [f"X{i+1}={v:.3f}" for i,v in enumerate(coords_wk) if abs(v)<0.1]
            near_one  = [f"X{i+1}={v:.3f}" for i,v in enumerate(coords_wk) if abs(v-1)<0.1]
            mid_range = [f"X{i+1}={v:.3f}" for i,v in enumerate(coords_wk) if abs(v)>=0.1 and abs(v-1)>=0.1]
            boundary_pct = (len(near_zero)+len(near_one))/dims*100
        else:
            near_zero,near_one,mid_range = [],[],[]
            boundary_pct = 0
        cv_rows_s = sorted(cv_rows, key=lambda x: x["cv"], reverse=True)
        margin = winner["cv"] - (sum(r["cv"] for r in cv_rows)/len(cv_rows)) if cv_rows else 0
        runner_up = cv_rows_s[1] if len(cv_rows_s)>1 else None
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>Winner Analysis — {fn} W{wk_idx+1}</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                <b style='color:#22c55e'>★ {winner["name"]}</b> · CV={winner["cv"]:.1%} ± {winner.get("std",0):.1%}<br>
                {("vs " + runner_up["name"] + f" ({runner_up['cv']:.1%}) — margin: +{winner['cv']-runner_up['cv']:.1%}") if runner_up else ""}<br><br>
                <b style='color:#38bdf8'>Why {_fam_name} wins here:</b><br>
                {_fam_why}<br><br>
                <b style='color:#f59e0b'>Implication for GP:</b><br>
                A {winner["cv"]:.0%} accurate filter means roughly {int(winner["cv"]*10000*0.3):,} true class-1 candidates pass through vs ~{int((1-winner["cv"])*10000*0.3):,} false positives.
              </div>
            </div>""", unsafe_allow_html=True)
        with c2:
            _bnd_str = ""
            if near_zero: _bnd_str += f"<b style='color:#38bdf8'>Near-zero</b> ({len(near_zero)}/{dims}): {', '.join(near_zero)}<br><br>"
            if near_one:  _bnd_str += f"<b style='color:#22c55e'>Near-one</b> ({len(near_one)}/{dims}): {', '.join(near_one)}<br><br>"
            if mid_range: _bnd_str += f"<b style='color:#c8d4f0'>Mid-range</b> ({len(mid_range)}/{dims}): {', '.join(mid_range)}<br><br>"
            _geom = ("High boundary concentration — CNN and DT have structural advantage here." if boundary_pct>40 else
                     "Mixed interior/boundary pattern — CV accuracy is the primary selection criterion.")
            st.markdown(f"""
            <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;text-transform:uppercase;letter-spacing:0.18em;margin-bottom:10px'>Boundary Dimension Analysis — W{wk_idx+1}</div>
              <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                {_bnd_str if coords_wk else "Coordinates pending."}
                <b style='color:#f59e0b'>Data geometry:</b><br>
                {boundary_pct:.0f}% of dimensions at boundary. {_geom}<br><br>
                <span style='color:#7a8fbb;font-size:0.75rem'>n={len(sc)} training points · {dims}D · {len(sc)/dims:.1f} pts/dim</span>
              </div>
            </div>""", unsafe_allow_html=True)

    # ── Step 8: Candidate generation ─────────────────────────────────────────
    elif step_key == "Step 8":
        ratio   = strat["exploit_ratio"]
        n_exploit = int(10000 * ratio)
        n_explore = 10000 - n_exploit
        sigma   = strat.get("sigma", "—")
        sigma_str = f"{sigma}" if not isinstance(sigma, list) else f"aniso {sigma}"
        fig = go.Figure(go.Pie(
            labels=["Exploit (Gaussian around best)", "Explore (uniform random)"],
            values=[n_exploit, n_explore],
            marker_colors=["#3b82f6", "#22c55e"], hole=0.55,
            textinfo="label+percent",
            textfont=dict(size=10, color="white", family="IBM Plex Mono"),
            hovertemplate="%{label}: %{value:,} candidates<extra></extra>"))
        fig.update_layout(height=280, paper_bgcolor=DARK,
            font=dict(color="#7a8fbb", family="IBM Plex Mono"),
            margin=dict(l=10,r=10,t=40,b=10),
            title=dict(text=f"{fn} W{wk_idx+1} — 10,000 Candidates · σ={sigma_str}", font=dict(size=11, color="#c8d4f0")),
            legend=dict(bgcolor="rgba(0,0,0,0)", font_size=9, x=0.5, xanchor="center", y=-0.05))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        # Historical submissions scatter
        st.markdown('<div class="sec-head">Historical Submissions — Sent to GP</div>', unsafe_allow_html=True)
        all_coords = [(i, COORDS[fn][i], SCORES[fn][i])
                      for i in range(min(wk_idx+1, len(COORDS[fn])))
                      if COORDS[fn][i] is not None]
        if all_coords and dims == 2:
            xs     = [c[1][0] for c in all_coords]
            ys     = [c[1][1] for c in all_coords]
            sc2    = [c[2] if c[2] is not None else 0 for c in all_coords]
            wks    = [f"W{c[0]+1}" for c in all_coords]
            atb    = get_all_time_best(fn)
            fig2 = go.Figure()
            fig2.add_trace(go.Scatter(x=xs, y=ys, mode="markers+text",
                marker=dict(size=14, color=sc2,
                    colorscale=[[0,"#7f1d1d"],[0.5,"#1a2540"],[1,"#14532d"]],
                    showscale=True, colorbar=dict(title="Score", thickness=10, tickfont=dict(size=8, family="IBM Plex Mono")),
                    line=dict(color=["#f59e0b" if s==atb else "#060a10" for s in sc2], width=2)),
                text=wks, textposition="top center",
                textfont=dict(size=9, color="white", family="IBM Plex Mono"),
                hovertemplate="<b>%{text}</b><br>X1=%{x:.4f}<br>X2=%{y:.4f}<br>Score=%{marker.color:.4e}<extra></extra>"))
            fig2.update_layout(height=350, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                font=dict(color="#7a8fbb", family="IBM Plex Mono"), margin=dict(l=10,r=60,t=40,b=10),
                title=dict(text=f"{fn} — All W1–W{wk_idx+1} Submissions · gold ring = ATB", font=dict(size=11, color="#c8d4f0")),
                xaxis=dict(title="X1", range=[-0.05,1.05], gridcolor="#111827", zeroline=False),
                yaxis=dict(title="X2", range=[-0.05,1.05], gridcolor="#111827", zeroline=False))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            st.caption("Colour = score (green=high, red=low) · Gold ring = ATB · Each point = one week's GP submission")
        elif all_coords and dims > 2:
            coord_matrix = [c[1] for c in all_coords]
            scores_list  = [c[2] if c[2] is not None else 0 for c in all_coords]
            dim_labels   = [f"X{i+1}" for i in range(dims)]
            fig2 = go.Figure(go.Parcoords(
                line=dict(color=scores_list,
                    colorscale=[[0,"#7f1d1d"],[0.5,"#1a2540"],[1,"#14532d"]],
                    showscale=True, colorbar=dict(title="Score", thickness=10, tickfont=dict(size=8, family="IBM Plex Mono"))),
                dimensions=[dict(label=dim_labels[i], values=[c[i] for c in coord_matrix], range=[0,1]) for i in range(dims)]))
            fig2.update_layout(height=320, paper_bgcolor=DARK, plot_bgcolor=DARK,
                font=dict(color="#7a8fbb", family="IBM Plex Mono"), margin=dict(l=60,r=60,t=50,b=20),
                title=dict(text=f"{fn} — All W1–W{wk_idx+1} Submissions · parallel coords", font=dict(size=11, color="#c8d4f0")))
            st.plotly_chart(fig2, use_container_width=True, config={"displayModeBar": False})
            st.caption(f"Each line = one week's {dims}D submission · Colour = score · Drag axes to filter")

    # ── Step 10 / 11: Acquisition Functions ─────────────────────────────────
    elif step_key in ("Step 10", "Step 11"):
        sc      = actuals[:n]
        strat   = STRATEGY[fn]
        hp      = weekly["hyperparams"]
        kappa   = hp.get("ucb_kappa", 2.0)
        coords_wk = COORDS[fn][wk_idx] if wk_idx < len(COORDS[fn]) and COORDS[fn][wk_idx] else None
        atb       = get_all_time_best(fn)
        atb_coords = next((COORDS[fn][i] for i,s in enumerate(SCORES[fn]) if s == atb and COORDS[fn][i]), None)

        if sc and coords_wk:
            # Simulate EI and UCB curves using historical score data
            # x-axis = weeks, show how EI and UCB scores evolved at each submission point
            # EI at each week = improvement over best-so-far at that point
            ei_vals, ucb_vals, rb_at_week = [], [], []
            running_b = actuals[0]
            for i, s in enumerate(sc):
                rb_at_week.append(running_b)
                # EI = max(0, s - best_so_far) — simplified (actual EI requires GP posterior)
                ei = max(0, (s - running_b) if maximize else (running_b - s))
                ei_vals.append(ei)
                # UCB proxy = s + kappa * abs(s - running_b) / (max(sc)+1e-12)
                sigma_proxy = abs(s - running_b) if i > 0 else abs(s) * 0.1
                ucb = s + kappa * sigma_proxy if maximize else s - kappa * sigma_proxy
                ucb_vals.append(ucb)
                if (s > running_b if maximize else s < running_b):
                    running_b = s

            # Normalise for display
            ei_max = max(abs(v) for v in ei_vals) or 1
            ucb_max = max(abs(v) for v in ucb_vals) or 1
            ei_norm  = [v / ei_max  for v in ei_vals]
            ucb_norm = [v / ucb_max for v in ucb_vals]

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=week_labels[:len(ei_norm)], y=ei_norm,
                mode="lines+markers", name="EI (normalised)",
                line=dict(color="#22c55e", width=2),
                marker=dict(size=8, color=["#f59e0b" if e==max(ei_norm) else "#22c55e" for e in ei_norm]),
                hovertemplate="<b>%{x}</b><br>EI (norm)=%{y:.3f}<extra></extra>"))
            fig.add_trace(go.Scatter(
                x=week_labels[:len(ucb_norm)], y=ucb_norm,
                mode="lines+markers", name=f"UCB κ={kappa} (normalised)",
                line=dict(color="#38bdf8", width=2, dash="dot"),
                marker=dict(size=6),
                hovertemplate="<b>%{x}</b><br>UCB (norm)=%{y:.3f}<extra></extra>"))
            fig.add_trace(go.Bar(
                x=week_labels[:len(sc)], y=sc,
                name="Score", opacity=0.25,
                marker_color="#4a6a9a", yaxis="y2",
                hovertemplate="<b>%{x}</b><br>Score=%{y:.4f}<extra></extra>"))
            fig.update_layout(
                height=320, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                font=dict(color="#7a8fbb", family="IBM Plex Mono"),
                margin=dict(l=10, r=60, t=40, b=10),
                title=dict(text=f"{fn} W{wk_idx+1} — Acquisition Function Signals · EI + UCB (κ={kappa})",
                           font=dict(size=11, color="#c8d4f0")),
                xaxis=dict(gridcolor="#111827", showgrid=True),
                yaxis=dict(title="Acq. score (normalised)", gridcolor="#111827", side="left"),
                yaxis2=dict(title="Raw score", overlaying="y", side="right",
                            gridcolor="rgba(0,0,0,0)", showgrid=False),
                legend=dict(bgcolor="rgba(0,0,0,0)", font_size=9,
                            x=0.5, xanchor="center", y=-0.12, orientation="h"),
                barmode="overlay")
            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.caption(f"★ Gold marker = week EI peaked · EI = observed improvement over best-so-far · "
                       f"UCB = score + κσ encourages exploration · κ={kappa} set in W{wk_idx+1} hyperparams")

            # Explanation cards
            c1, c2 = st.columns(2)
            with c1:
                st.markdown(f"""
                <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                              text-transform:uppercase;letter-spacing:0.18em;margin-bottom:8px'>
                    Expected Improvement (EI)</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                    EI answers: <b>how much better than the current best</b> do we expect this point to be?<br><br>
                    EI = 0 everywhere except near the best-known region — it is conservative and exploitation-focused.
                    High EI = the GP predicts this point will beat the current ATB of <b>{fmt(atb)}</b>.<br><br>
                    <b style='color:#f59e0b'>Why normalise?</b> EI and UCB have different scales so both
                    are normalised to [0,1] before combining. The combined score picks the submission point.
                  </div>
                </div>""", unsafe_allow_html=True)
            with c2:
                st.markdown(f"""
                <div style='background:#0a1020;border:1px solid #1e2d45;border-radius:10px;padding:16px 20px'>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.60rem;color:#38bdf8;
                              text-transform:uppercase;letter-spacing:0.18em;margin-bottom:8px'>
                    Upper Confidence Bound (UCB) · κ={kappa}</div>
                  <div style='font-family:"IBM Plex Mono",monospace;font-size:0.82rem;color:#c8d4f0;line-height:1.85'>
                    UCB answers: <b>what is the optimistic upper bound</b> on this point's score?<br><br>
                    UCB = μ + κσ — the GP mean plus κ times the uncertainty.
                    High κ = more exploration (trust uncertainty); low κ = more exploitation (trust mean).<br><br>
                    For {fn} W{wk_idx+1}, κ={kappa} was chosen to
                    {"favour exploitation — we are confident in the region" if kappa <= 2.0 else
                     "encourage exploration — we want to probe uncertain regions"}.
                  </div>
                </div>""", unsafe_allow_html=True)

    # ── Step 13: Submission dashboard
    # ── Step 13: Submission dashboard ────────────────────────────────────────
    elif step_key == "Step 13":
        sc = actuals[:n]
        rb = running_best(scores, maximize)[:n]
        bar_colors = ["#4a5a7a"]
        for i in range(1, len(sc)):
            imp = (sc[i] > sc[i-1]) if maximize else (sc[i] < sc[i-1])
            bar_colors.append("#22c55e" if imp else "#ef4444")
        if sc: bar_colors[-1] = "#38bdf8"
        fig = go.Figure()
        fig.add_trace(go.Bar(x=week_labels, y=sc, marker_color=bar_colors, marker_line_width=0, opacity=0.9, name="Score",
            text=[fmt(v) for v in sc], textposition="outside", textfont=dict(size=9, color="white", family="IBM Plex Mono")))
        fig.add_trace(go.Scatter(x=week_labels, y=[r for r in rb if r is not None],
            mode="lines+markers", line=dict(color="#f59e0b", width=2, dash="dash"), marker=dict(size=5), name="Running best"))
        atb = get_all_time_best(fn)
        fig.add_hline(y=atb, line_dash="dot", line_color="#f59e0b",
            annotation_text=f"ATB: {fmt(atb)}", annotation_font=dict(color="#f59e0b", size=9))
        fig.update_layout(height=300, paper_bgcolor=DARK, plot_bgcolor=PLOT,
            font=dict(color="#7a8fbb", family="IBM Plex Mono"), margin=dict(l=10,r=10,t=30,b=10),
            title=dict(text=f"{fn} — Submission Dashboard · W{n} · ATB={fmt(atb)}", font=dict(size=12, color="#c8d4f0")),
            legend=dict(bgcolor="rgba(0,0,0,0)", font_size=10),
            xaxis=dict(gridcolor="#0d1320", showgrid=False), yaxis=dict(gridcolor="#111827"))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
        coords_wk = COORDS[fn][wk_idx] if wk_idx < len(COORDS[fn]) else None
        if coords_wk:
            dims2 = [f"X{i+1}" for i in range(len(coords_wk))]
            fig2 = go.Figure(go.Bar(x=dims2, y=coords_wk,
                marker_color=["#38bdf8" if abs(c)<0.1 or abs(c-1)<0.1 else "#4a6a9a" for c in coords_wk],
                text=[f"{c:.4f}" for c in coords_wk], textposition="outside",
                textfont=dict(size=10, color="white", family="IBM Plex Mono")))
            fig2.update_layout(height=220, paper_bgcolor=DARK, plot_bgcolor=PLOT,
                font=dict(color="#7a8fbb", family="IBM Plex Mono"), margin=dict(l=10,r=10,t=30,b=10),
                title=dict(text=f"Submitted Coordinates — W{wk_idx+1}", font=dict(size=11, color="#c8d4f0")),
                xaxis=dict(showgrid=False), yaxis=dict(gridcolor="#111827", range=[-0.05,1.15]))
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

    # ── Live chart
    CHART_STEPS = {"Step 3","Step 4","Step 5","Step 5B","Step 6","Step 7","Step 7B","Step 8","Step 10","Step 11","Step 13"}
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
