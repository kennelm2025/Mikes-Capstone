import streamlit as st
from data import FUNCTIONS, SCORES, STRATEGY, WEEKLY, PIPELINE_STEPS, get_all_time_best

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
