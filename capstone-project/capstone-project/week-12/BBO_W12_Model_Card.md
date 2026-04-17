# Model Card — BBO Capstone Week 12
### Mike Kennelly | Imperial College | Final Query

---

## 1. Model Overview

| Property | Value |
|----------|-------|
| **Model name** | Adaptive Multi-Classifier + GP/EI Pipeline |
| **Version** | Week 12 — Final iteration |
| **Framework** | scikit-learn 1.x · PyTorch (CNN-1D) · scipy |
| **Task** | Black-Box Optimisation — MAXIMISE f(x), x ∈ [0,1]^d |
| **Functions** | F1 (2D) · F2 (2D) · F3 (3D) · F4 (4D) · F5 (4D) · F6 (5D) · F7 (6D) · F8 (8D) |
| **Total queries** | 12 per function (one submission per week) |
| **Author** | Mike Kennelly — Imperial College BBO Capstone |
| **Date** | Week 12, April 2026 |

---

## 2. Model Architecture

The pipeline runs four sequential stages each week per function.

### Stage 1 — Binary Classification (8-model CV ensemble)

Historical evaluations are labelled: top-30% outputs = class 1 (HIGH), remainder = class 0 (LOW). Eight classifier families are trained and ranked by stratified k-fold cross-validation. The winner filters the candidate pool passed to the GP.

| # | Model | Key Parameters | Role |
|---|-------|----------------|------|
| 1 | Linear SVM | C=1.0, probability=True | Regularised linear boundary — robust at low n/p ratios |
| 2 | Decision Tree | max_depth=4 | Axis-aligned splits for per-dimension threshold effects |
| 3 | Random Forest | n_estimators=100 | Ensemble — won F6 W9 precision lock at CV=91.7% |
| 4 | Logistic Regression | max_iter=1000, L2 | Calibrated probabilities — won F7 W11 |
| 5 | NN-Small | (16,8), early_stopping | Small-data MLP |
| 6 | NN-Medium | (64,32), early_stopping | General-purpose MLP |
| 7 | NN-Large | (128,64,32), early_stopping | High-capacity MLP |
| 8 | CNN-1D (Module 17) | Conv1d(1→8, k=2) + ReLU + Dropout(0.3) + Linear | Scans adjacent coordinate pairs — learning exercise |

### Stage 2 — Candidate Generation (Anisotropic TuRBO)

10,000 candidates are generated per function each week. Exploitation candidates are drawn from an anisotropic Gaussian N(best_point, Σ) where Σ = diag(ANISO_SIGMA²) — per-dimension standard deviations set by Ollama (llama3.1) sensitivity analysis. Exploration candidates are uniform random draws across [0,1]^d. The CV winner then filters the pool to the top 50% by P(class=1).

### Stage 3 — Gaussian Process Regression

A Gaussian Process with Matérn ν=5/2 kernel (+ ConstantKernel amplitude, normalize_y=True, n_restarts_optimizer=10) is fitted on the full labelled history. Outputs:

- **μ(x)** — predicted function mean at candidate point x
- **σ(x)** — epistemic uncertainty

### Stage 4 — Acquisition Functions (EI + UCB)

Expected Improvement is the primary acquisition function. UCB is computed in parallel as a reference.

```
EI(x) = (μ(x) − y_best − ξ)·Φ(Z) + σ(x)·φ(Z)    Z = (μ(x) − y_best − ξ)/σ(x)    ξ = 0.01
UCB(x) = μ(x) + κ·σ(x)    κ = 2.0
```

For functions under **ATB override**, the GP runs for documentation but the submission uses confirmed ATB coordinates. For **F7 only**, the GP EI candidate is submitted if μ > ATB and trust conditions are met.

---

## 3. Week 12 Decision Framework

> **Rule:** If W11 did not beat the prior ATB → submit exact ATB coordinates unchanged.
>
> **Exception:** F7 only — run GP pipeline. If GP μ > 2.8501 and R² is not degenerate → submit GP EI candidate. Otherwise submit W11 ATB fallback.
>
> **Rationale:** GP surrogates with R²=1.0 (memorising) provide no trustworthy gradient signal for improvement. Exact ATB replication dominates GP exploration for all non-trending functions at week 12.

### Per-Function W12 Settings

| Fn | Dims | ATB | ATB Wk | W11 Status | W12 Method | Cluster Type | ANISO_SIGMA |
|----|------|-----|--------|------------|------------|--------------|-------------|
| F1 | 2D | 8.968e-07 | W11 | NEW ATB ✓ | ATB OVERRIDE | Tight Attractor | [0.015, 0.015] |
| F2 | 2D | 0.6497 | W5 | Regressed | ATB OVERRIDE | ★ Two-Zone Cluster | [0.012, 0.008] |
| F3 | 3D | −0.001285 | W11 | NEW ATB ✓ | ATB OVERRIDE | Tight Attractor | [0.005, 0.020, 0.025] |
| F4 | 4D | 0.23759 | W2 | Exact match | ATB OVERRIDE | Isolated Attractor | [0.012×4] |
| F5 | 4D | 8662.48 | W9 | Exact match | ATB OVERRIDE | Corner Attractor | [0.005×4] |
| F6 | 5D | 0.03602 | W9 | Regressed | ATB OVERRIDE | Tight Attractor | [0.015×4, 0.008] |
| F7 | 6D | 2.8501 | W11 | NEW ATB ✓ | GP PIPELINE | ★ Trending Cluster | [0.015, 0.012×4, 0.015] |
| F8 | 8D | 9.8320 | W2 | Regressed | ATB OVERRIDE | Zero-Boundary | [0.006, 0.015, 0.006, 0.015×4, 0.006, 0.015] |

### Portal Submission Strings

```
F1: 0.684200-0.704200
F2: 0.710068-0.161630
F3: 0.998126-0.621218-0.453080
F4: 0.439249-0.414994-0.384687-0.397917
F5: 1.000000-1.000000-1.000000-1.000000
F6: 0.406643-0.339495-0.634775-0.769397-0.115269
F7: 0.165978-0.338682-0.444076-0.255770-0.300940-0.704355  ← RUN GP FIRST
F8: 0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212
```

---

## 4. Module 22 Clustering Integration

Module 22 unsupervised learning — hierarchical clustering, centroid distance, linkage analysis — was applied to the 11-round submission history for all 8 functions to validate and justify the W12 strategy. Two functions are featured as primary showcases.

### F2 — Two-Zone Hierarchical Clustering (Primary Showcase)

Complete linkage clustering on Euclidean distance in [0,1]² across 11 rounds cleanly separates two basins of attraction:

| Zone | Weeks | X2 Region | Centroid | Mean Output |
|------|-------|-----------|----------|-------------|
| Zone A — HIGH X2 | W1, W2, W3, W4, W9 | X2 > 0.50 | [0.733, 0.904] | 0.225 |
| Zone B — LOW X2 | W5, W6, W7, W8, W10, W11 | X2 ≤ 0.50 | [0.702, 0.118] | 0.506 |

**Key findings:**

- Inter-zone distance = **0.963** — clean dendrogram separation under complete linkage
- Zone B intra-cluster spread = **0.025** — confirms a genuine point attractor, not noise
- ATB (W5, 0.6497) sits at distance **0.012** from Zone B centroid — the ATB IS the cluster centroid
- Zone A mean output (0.225) << Zone B mean output (0.506) — Zone B is the high-value basin

**W12 implication:** Submitting the ATB coordinates is equivalent to submitting the Zone B centroid. The clustering analysis provides formal justification for the override strategy — no GP exploration can improve on a confirmed point attractor without a new evaluation in that zone.

**Module 22 concept applied:** Point attractor (tight spread < 0.05) vs multi-modal landscape (spread > 0.40). Zone B qualifies as a confirmed single-centroid attractor.

---

### F7 — Trending / Dynamic Cluster (Secondary Showcase)

W6–W11 form a directional cluster rather than a static attractor. This is the distinguishing feature that justifies running the GP pipeline for F7 when all other functions use ATB override.

| Week | Output | Step Size (6D) | Direction |
|------|--------|----------------|-----------|
| W6 | 2.119 | — | Baseline |
| W7 | 2.413 | 0.061 | X1↑ X6↑ |
| W8 | 2.598 | 0.049 | X1↑ X6↑ |
| W9 | 2.597 | 0.001 | Near-stationary |
| W10 | 2.720 | 0.042 | X1↑ X6↑ |
| W11 | 2.850 | 0.061 | X1↑ X6↑ |

**Key findings:**

- Intra-cluster spread = **0.066** — tight enough to confirm genuine gradient, not scatter
- Consistent direction: X1 rising (+0.041 W10→W11), X6 rising, X2–X5 declining each week
- Each weekly step ≈ 0.04–0.06 units in 6D space — small, consistent, improving

**W12 implication:** A dynamic (moving centroid) cluster indicates the GP is tracking a real landscape ridge. GP extrapolation is justified. In contrast, static attractors (F2, F4, F6) have no directional signal — ATB override is correct there.

**Module 22 concept applied:** Dynamic cluster (centroid shifting over time) vs static point attractor. The cluster type directly drives the pipeline decision — the only function where GP is trusted over override.

---

### Cluster Summary — All 8 Functions

| Fn | Top-3 Spread | ATB→Centroid | Cluster Type | W12 Decision |
|----|-------------|--------------|--------------|--------------|
| F1 | 0.014 | 0.007 | Tight static | Replicate W11 ATB |
| F2 | 0.025 | 0.012 | **Two-zone** (LOW-X2 confirmed) | ATB = Zone B centroid → override |
| F3 | 0.047 | 0.024 | Tight static (X1=1.0 anchor) | Replicate W11 ATB |
| F4 | 0.062 | 0.031 | Isolated positive basin | Replicate W2 ATB |
| F5 | 0.007 | 0.003 | Tightest — corner | All-ones corner → override |
| F6 | 0.030 | 0.015 | Tight static (X5 threshold) | Replicate W9 ATB |
| F7 | 0.066 | 0.051 | **Trending / dynamic** | GP pipeline — extrapolate direction |
| F8 | 0.455 | 0.422 | Loose (zero-boundary pattern) | Replicate W2 ATB exactly |

---

## 5. Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| TOP_PERCENTILE | 30% | Top 30% of outputs = class 1 — sufficient positive examples at n=20–50 |
| N_CANDIDATES | 10,000 | Dense coverage for all dimensionalities (2D–8D) |
| EI_XI | 0.01 | Small exploration jitter — encourages exploitation near known best |
| UCB_KAPPA | 2.0 | Moderate ~2σ exploration bonus |
| GP_RESTARTS | 10 | Kernel hyperparameter optimisation restarts |
| FILTER_PERCENTILE | 50 | Discard bottom 50% of candidates by P(class=1) |
| CV_FOLDS | 2–5 (adaptive) | max(2, min(5, min(n_pos, n_neg) / 2)) |
| RANDOM_SEED | 42 | Reproducibility |
| GP kernel | Matérn ν=5/2 + ConstantKernel | normalize_y=True, alpha=1e-6 |

---

## 6. Limitations and Risks

| Limitation | Description | Mitigation |
|------------|-------------|------------|
| Stochastic functions | F2 returned 0.6090 (not 0.6497) when W11 replicated exact W5 ATB coords — identical input, different output | Accept stochasticity; ATB replication is still the best available strategy |
| GP over-fitting | R²=1.0 from W6 onward for most functions. Surrogate memorises rather than generalises. EI values unreliable for extrapolation | ATB override for 7/8 functions. GP used for documentation only |
| Dimensionality curse | F8 (8D, n=50) = 0.000050% space coverage. Global optimum cannot be verified | Structural zero-boundary pattern (X1=X3=X7=0) constrains effective search |
| Non-stationarity | F4 landscape is non-stationary — 9 explorations near ATB all returned negative | Exact ATB replication; avoid GP exploration in non-stationary regime |
| Cluster myopia | Hierarchical clustering greedy — merges cannot be undone. Two-zone F2 result depends on distance metric | Cross-validated: Euclidean and cosine agree on F2 two-zone structure |
| Single final query | Week 12 = last evaluation. No recovery from a bad submission | ATB override is the risk-minimising strategy — no new information can be incorporated |

---

## 7. Intended Use

| Property | Value |
|----------|-------|
| **Primary use** | Imperial College BBO Capstone Project — academic optimisation competition |
| **Secondary use** | Demonstrating Bayesian optimisation pipeline design for assessment |
| **Module coverage** | Mod 17 (CNN-1D) · Mod 19 (TuRBO/delimiting context) · Mod 20 (Ollama LLM) · Mod 22 (clustering) |
| **Out-of-scope** | Production deployment, safety-critical systems, any real-world application without full re-validation |

---

*BBO Capstone Model Card — Mike Kennelly — Imperial College — Week 12 Final Query*
