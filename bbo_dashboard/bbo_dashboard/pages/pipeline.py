import streamlit as st
import plotly.graph_objects as go
from data import PIPELINE_STEPS, FUNCTIONS, STRATEGY, CLASSIFIERS

STEP_COLORS = {
    "⚙️":"#6366f1","📂":"#3b82f6","🔬":"#06b6d4","📊":"#10b981","🎲":"#f59e0b",
    "🤖":"#8b5cf6","📈":"#ec4899","🔽":"#14b8a6","🧠":"#f97316","📝":"#84cc16",
    "🌐":"#06b6d4","🎯":"#3b82f6","📉":"#8b5cf6","🗺️":"#10b981","🏆":"#f59e0b",
}

def render(fn=None):
    st.markdown("## 🏗️ Pipeline Code Structure")
    st.caption("The BBO notebook follows a fixed 13-step pipeline. Each step is described below. "
               "Select any step to see a deeper explanation and example code.")

    st.divider()

    # ── Pipeline flow diagram ─────────────────────────────────────────────────
    st.markdown("### Visual Pipeline Flow")

    step_names = [f"{s['icon']} {s['title']}" for s in PIPELINE_STEPS]
    step_nums  = [s["step"] for s in PIPELINE_STEPS]
    n = len(PIPELINE_STEPS)
    xs = list(range(n))
    ys = [0] * n

    fig = go.Figure()
    # Connector line
    fig.add_trace(go.Scatter(
        x=xs, y=ys, mode="lines",
        line=dict(color="#1e2538", width=3), showlegend=False, hoverinfo="skip",
    ))
    # Step circles
    for i, step in enumerate(PIPELINE_STEPS):
        color = STEP_COLORS.get(step["icon"], "#4c9be8")
        fig.add_trace(go.Scatter(
            x=[i], y=[0],
            mode="markers+text",
            marker=dict(size=38, color=color, line=dict(color="white", width=2)),
            text=[step["step"].replace("Step ", "")],
            textfont=dict(size=9, color="white", family="monospace"),
            textposition="middle center",
            name=step["title"],
            hovertemplate=f"<b>{step['step']}: {step['title']}</b><br>{step['desc'][:80]}...<extra></extra>",
        ))
        # Label below
        fig.add_annotation(
            x=i, y=-0.35,
            text=step["title"].replace(" ", "<br>"),
            showarrow=False,
            font=dict(size=8, color="#6b7a9a"),
            align="center",
        )

    fig.update_layout(
        height=200, paper_bgcolor="#0f1117", plot_bgcolor="#0f1117",
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.5, n-0.5]),
        yaxis=dict(showgrid=False, showticklabels=False, zeroline=False, range=[-0.7, 0.5]),
        showlegend=False,
        margin=dict(l=20, r=20, t=10, b=20),
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    st.caption("Hover over each step for a quick description. Click a step card below for full detail.")

    st.divider()

    # ── Step selector ─────────────────────────────────────────────────────────
    selected_step = st.selectbox(
        "Select a step for detailed breakdown",
        [f"{s['step']}: {s['title']}" for s in PIPELINE_STEPS],
        index=5,
    )
    step_idx = next(i for i, s in enumerate(PIPELINE_STEPS) if f"{s['step']}: {s['title']}" == selected_step)
    step = PIPELINE_STEPS[step_idx]
    color = STEP_COLORS.get(step["icon"], "#4c9be8")

    st.markdown(f"""
    <div style="background:#1a1f2e;border-radius:10px;padding:20px 24px;
                border-left:5px solid {color};margin-bottom:1.2rem">
      <div style="font-size:0.7rem;color:#4a5570;letter-spacing:0.15em;text-transform:uppercase">{step['step']}</div>
      <div style="font-size:1.4rem;font-weight:700;color:white;margin:6px 0">{step['icon']} {step['title']}</div>
      <div style="color:#9aa4c0;line-height:1.75">{step['desc']}</div>
    </div>
    """, unsafe_allow_html=True)

    # ── Code snippets for each step ───────────────────────────────────────────
    CODE_SNIPPETS = {
        "Step 0": '''# ── Config ──────────────────────────────────────────────
FUNCTION_ID   = "F5"
WEEK          = 7
MAXIMIZE      = True
EXPLOIT_RATIO = 0.85       # 85% candidates from exploit distribution
EXPLOIT_SIGMA = 0.048      # Gaussian σ around best_point
UCB_KAPPA     = 2.0        # UCB = μ + κσ
GP_RESTARTS   = 8          # GP hyperparameter optimisation restarts
FILTER_PERCENTILE = 50     # Keep top 50% by P(high)

# Strategy: EXPLOIT W6 NEW BEST — σ=0.048 around [0.781, 1.0, 1.0, 1.0]''',

        "Step 1": '''# ── Load Data ───────────────────────────────────────────
X_train = np.load(f"f{fn}_w{wk}_inputs.npy")    # shape: (n_samples, n_dims)
y_train = np.load(f"f{fn}_w{wk}_outputs.npy")   # shape: (n_samples,)

best_idx   = np.argmax(y_train) if MAXIMIZE else np.argmin(y_train)
best_value = y_train[best_idx]
best_point = X_train[best_idx]
print(f"n={len(y_train)}, dims={X_train.shape[1]}, best={best_value:.4f}")''',

        "Step 4": '''# ── Candidate Generation ────────────────────────────────
n_candidates = 10_000
n_exploit    = int(n_candidates * EXPLOIT_RATIO)
n_explore    = n_candidates - n_exploit

# Exploit: Gaussian around best point, clipped to [0,1]
X_exploit = np.clip(
    best_point + np.random.randn(n_exploit, n_dims) * EXPLOIT_SIGMA, 0, 1
)
# Explore: Sobol quasi-random sequence
from scipy.stats.qmc import Sobol
sobol = Sobol(n_dims, scramble=True)
X_explore = sobol.random(n_explore)

X_candidates = np.vstack([X_exploit, X_explore])
src_labels   = ["exploit"]*n_exploit + ["explore"]*n_explore''',

        "Step 5": '''# ── Train 8 Classifiers ─────────────────────────────────
# Binary label: top 30% of y_train = class 1
threshold = np.percentile(y_train, 70)
y_labels  = (y_train >= threshold).astype(int)

from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neural_network import MLPClassifier
# + custom CNN-1D via PyTorch

models = {
    "Linear SVM":         LinearSVC(C=1.0, max_iter=2000),
    "RBF SVM":            SVC(kernel="rbf", probability=True, C=1.0),
    "Logistic Regression":LogisticRegression(max_iter=500),
    "Decision Tree":      DecisionTreeClassifier(max_depth=4),
    "Random Forest":      RandomForestClassifier(n_estimators=100, class_weight="balanced"),
    "Extra Trees":        ExtraTreesClassifier(n_estimators=100),
    "Neural Network":     MLPClassifier(hidden_layer_sizes=(64,32), max_iter=500),
    "CNN-1D":             train_cnn1d(X_train, y_labels),   # custom function
}
# 5-fold CV for each, select winner by mean accuracy''',

        "Step 9": '''# ── Gaussian Process Fit ────────────────────────────────
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern, WhiteKernel, ConstantKernel

kernel = ConstantKernel(1.0) * Matern(length_scale=1.0, nu=2.5) + WhiteKernel(0.01)
gp = GaussianProcessRegressor(
    kernel=kernel,
    n_restarts_optimizer=GP_RESTARTS,
    normalize_y=True,
    alpha=1e-6,
)
scaler = StandardScaler()
X_sc   = scaler.fit_transform(X_train)
gp.fit(X_sc, y_train)

mu, sigma = gp.predict(scaler.transform(X_filt), return_std=True)
print(f"GP R²: {gp.score(X_sc, y_train):.4f}")
print(f"Kernel: {gp.kernel_}")''',

        "Step 10": '''# ── EI & UCB Acquisition ────────────────────────────────
from scipy.stats import norm

EI_XI = 0.01   # exploration bonus (jitter)

# Expected Improvement (maximisation)
imp    = mu - best_value - EI_XI
Z      = imp / (sigma + 1e-9)
EI_acq = np.maximum(imp * norm.cdf(Z) + sigma * norm.pdf(Z), 0)

# Upper Confidence Bound
UCB_acq = mu + UCB_KAPPA * sigma

# Select submission
best_ei_idx = np.argmax(EI_acq)
submission  = X_filt[best_ei_idx]
sub_mu      = mu[best_ei_idx]
sub_sigma   = sigma[best_ei_idx]
sub_ucb     = UCB_acq[best_ei_idx]

print(f"Submission: {submission}")
print(f"GP μ={sub_mu:.4f}  σ={sub_sigma:.4f}  UCB={sub_ucb:.4f}")
print(f"EI={EI_acq[best_ei_idx]:.4f}")''',
    }

    snippet = CODE_SNIPPETS.get(step["step"])
    if snippet:
        st.markdown("#### 📟 Code Snippet")
        st.code(snippet, language="python")

    # ── All steps grid ────────────────────────────────────────────────────────
    st.divider()
    st.markdown("### All Steps At a Glance")
    cols = st.columns(3)
    for i, s in enumerate(PIPELINE_STEPS):
        col = cols[i % 3]
        c   = STEP_COLORS.get(s["icon"], "#4c9be8")
        with col:
            st.markdown(f"""
            <div style="background:#13182a;border-radius:8px;padding:12px 14px;
                        border-left:3px solid {c};margin:5px 0;min-height:90px">
              <div style="font-size:0.7rem;color:#4a5570;font-family:monospace">{s['step']}</div>
              <div style="color:white;font-size:0.88rem;font-weight:600;margin:3px 0">{s['icon']} {s['title']}</div>
              <div style="color:#6b7a9a;font-size:0.75rem;line-height:1.45">{s['desc'][:90]}...</div>
            </div>
            """, unsafe_allow_html=True)
