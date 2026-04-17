# Model Card — BBO Capstone Week 13
### Mike Kennelly | Imperial College | FINAL Query (Week 13 of 13)

---

## 1. Model Overview

| Property | Value |
|----------|-------|
| **Model name** | Adaptive Multi-Classifier + GP/EI Pipeline — W13 Final |
| **Version** | Week 13 — FINAL iteration (no further submissions after W13) |
| **Framework** | scikit-learn 1.x · PyTorch (CNN-1D) · scipy |
| **Task** | Black-Box Optimisation — MAXIMISE f(x), x ∈ [0,1]^d |
| **Functions** | F1 (2D) · F2 (2D) · F3 (3D) · F4 (4D) · F5 (4D) · F6 (5D) · F7 (6D) · F8 (8D) |
| **Total queries** | 13 per function (one submission per week) |
| **Author** | Mike Kennelly — Imperial College BBO Capstone |
| **Date** | Week 13, April 2026 |
| **Module coverage** | Mod 17 (CNN-1D) · Mod 19 (TuRBO) · Mod 20 (Ollama) · Mod 22 (Clustering) · **Mod 23 (PCA)** |

---

## 2. Model Architecture

The pipeline runs five sequential stages each week per function. **Week 13 adds Stage 2b — Module 23 PCA variance analysis — between classification and candidate generation.**

### Stage 1 — Binary Classification (8-model CV ensemble)

Historical evaluations are labelled: top-30% outputs = class 1 (HIGH), remainder = class 0 (LOW). Eight classifier families are trained and ranked by stratified k-fold cross-validation. The winner filters the candidate pool passed to the GP.

| # | Model | Key Parameters | Role |
|---|-------|----------------|------|
| 1 | Linear SVM | C=1.0, probability=True | Regularised linear boundary — robust at low n/p ratios |
| 2 | Decision Tree | max_depth=4 | Axis-aligned splits for per-dimension threshold effects |
| 3 | Random Forest | n_estimators=100 | Ensemble — won F4/F6/F8 at W13 |
| 4 | Logistic Regression | max_iter=1000, L2 | Calibrated probabilities |
| 5 | NN-Small | (16,8), early_stopping | Small-data MLP |
| 6 | NN-Medium | (64,32), early_stopping | General-purpose MLP |
| 7 | NN-Large | (128,64,32), early_stopping | High-capacity MLP |
| 8 | CNN-1D (Module 17) | Conv1d(1→8, k=2) + ReLU + Dropout(0.3) + Linear | Scans adjacent coordinate pairs |

### Stage 2a — Candidate Generation (Anisotropic TuRBO)

10,000 candidates are generated per function each week. Exploitation candidates are drawn from an anisotropic Gaussian N(best_point, Σ) where Σ = diag(ANISO_SIGMA²) — per-dimension standard deviations set by Module 20 Ollama (llama3.1) sensitivity analysis and, from W13, **refined using Module 23 PCA findings** (locked dims get near-zero sigmas; active dims get normal sigmas). Exploration candidates are uniform random draws across [0,1]^d.

### Stage 2b — Module 23 PCA Variance Analysis (NEW at W13)

For each function, PCA is computed on:
- **(a)** the full W1–W12 dataset (for context)
- **(b)** a function-specific "confirmed good" subset (top-output or near-ATB)

The scree plots, explained-variance ratios and per-dimension variance produce a **Module 23 case classification** for each function. This classification informs (i) the narrative in the notebook markdown, (ii) the `pca_analysis` block in the hyperparameters JSON, and (iii) the final submission-TXT comment header.

**Two-subset approach for F5, F8:** When top-30% is too permissive (includes non-ATB rows that drift from the structural attractor), a tighter "confirmed good" subset is used. For F5 this is "all dims ≥ 0.95" (near-corner); for F8 it is "top-5 rows by output" (near-ATB, all y > 9.81). This gives the cleanest demonstration of the flat-PC structure.

### Stage 3 — Gaussian Process Regression

A Gaussian Process with Matérn ν=5/2 kernel (+ ConstantKernel amplitude, normalize_y=True, n_restarts_optimizer=10) is fitted on the full labelled history. Outputs:

- **μ(x)** — predicted function mean at candidate point x
- **σ(x)** — epistemic uncertainty

**F6 W13 change:** GP alpha raised from 1e-6 to **1e-4** to absorb the visible oracle noise (σ_empirical ≈ 0.063 across 3 ATB-coord replays).

### Stage 4 — Acquisition Functions (EI + UCB)

Expected Improvement is the primary acquisition function. UCB is computed in parallel as a reference.

```
EI(x) = (μ(x) − y_best − ξ)·Φ(Z) + σ(x)·φ(Z)    Z = (μ(x) − y_best − ξ)/σ(x)    ξ = 0.01
UCB(x) = μ(x) + κ·σ(x)    κ = 2.0
```

For functions under **ATB override**, the GP runs for documentation but the submission uses confirmed ATB coordinates. For **F7 only**, the GP EI candidate is submitted **only if ALL 3 W13 trust conditions pass** (see §4 below).

---

## 3. Week 13 Decision Framework

> **Rule:** If prior week did not beat ATB → submit exact ATB coordinates unchanged.
>
> **Exception:** F7 only — run GP pipeline. Submit GP EI candidate **only if ALL 3 trust conditions pass**. Otherwise fall back to W12 ATB coords.
>
> **Rationale:** W13 is the FINAL query. No recovery possible. Risk-minimisation dominates — on oracles now shown to be stochastic (F2, F3, F6), identical input coords can return different scalar values, so "best-known input" still dominates "best-GP-predicted input" by expected value. On oracles shown to be deterministic (F1, F4, F5, F8), exact replication is the guaranteed safe outcome.

### Per-Function W13 Settings

| Fn | Dims | ATB | ATB Wk | W12 Status | W13 Method | Module 22 Cluster | Module 23 PCA | ANISO_SIGMA |
|----|------|-----|--------|------------|------------|--------------------|----------------|-------------|
| F1 | 2D | 8.968e-07 | W11 | = ATB (deterministic) | ATB OVERRIDE | Tight Attractor | — | [0.015, 0.015] |
| F2 | 2D | **0.6880** | **W12 ★** | **NEW ATB +0.038** | ATB OVERRIDE | ★ Two-Zone | Kernel-PCA | [0.012, 0.008] |
| F3 | 3D | −0.001285 | W11 | Regressed σ~0.003 | ATB OVERRIDE | Tight + boundary anchor | Scree / 1 flat PC | [0.005, 0.020, 0.025] |
| F4 | 4D | 0.23759 | W2 | = ATB (triple) | ATB OVERRIDE | Isolated Basin | Isolated (no flat PC) | [0.012×4] |
| F5 | 4D | 8662.48 | W9 | = ATB (triple) | ATB OVERRIDE | Corner | ★ Flat-scree | [0.005×4] |
| F6 | 5D | 0.03602 | W9 | Regressed σ~0.063 | ATB OVERRIDE | Tight + X5 threshold | Threshold / dominant-PC | [0.015×4, 0.008] |
| F7 | 6D | **2.8939** | **W12 ★** | **NEW ATB 7th consec** | **GP PIPELINE + fallback** | ★ Trending Ridge | ★ 1-dominant-PC | [0.015, 0.012×4, 0.015] |
| F8 | 8D | 9.83196 | W2 | = ATB (10-wk gap) | ATB OVERRIDE | Zero-boundary | ★ 3 flat PCs (PRIMARY) | [0.006, 0.015, 0.006, 0.015×4, 0.006, 0.015] |

### Portal Submission Strings (W13)

```
F1: 0.684200-0.704200
F2: 0.710068-0.161630
F3: 0.998126-0.621218-0.453080
F4: 0.439249-0.414994-0.384687-0.397917
F5: 1.000000-1.000000-1.000000-1.000000
F6: 0.406643-0.339495-0.634775-0.769397-0.115269
F7: 0.179941-0.306897-0.455194-0.249116-0.295985-0.730083   ← GP decision logic at Step 14
F8: 0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212
```

---

## 4. F7 — GP Pipeline Decision Logic (Unique to F7, Strengthened for W13)

F7 is the only notebook where the submission depends on GP output. The W13 logic adds a **third trust condition** to the W12 decision framework — risk-minimisation is tightened for the final round.

### W13 Trust Conditions (ALL must pass)

| # | Condition | Rationale |
|---|-----------|-----------|
| 1 | `GP μ > 2.8939` | Must predict genuine improvement over new W12 ATB |
| 2 | `R² < 0.999999` | Not pure memorisation — some generalisation signal expected |
| 3 | `GP μ − ATB > σ / 2` | **NEW at W13** — predicted gain exceeds half the GP's own uncertainty |

**If ALL pass:** submit GP EI candidate.  
**If ANY fails:** fall back to W12 ATB coords `0.179941-0.306897-0.455194-0.249116-0.295985-0.730083`.

### Why the new "gain > σ/2" condition

On F7's trending ridge the GP can predict μ values slightly above ATB, but with σ comparable to or larger than the predicted gain. In that case the GP is saying "I think there's a bit more up there, but I'm quite uncertain." On a final round with no recovery, this level of confidence is not enough to override a confirmed 2.8939. The Netflix/Tagliabue lesson (Module 23 V8) applies: the best offline model is not always the best production choice — robust replay beats speculative new coords when offline confidence is low.

### Author-Execution Result

On my execution of the F7 W13 notebook against the real W13 npy:
- GP μ_max = 2.856 (**FAIL** cond 1: not > 2.8939)
- R² = 1.000000 (**FAIL** cond 2: pure memorisation)
- μ − ATB = −0.038, σ = 0.091 → gain < σ/2 = 0.046 (**FAIL** cond 3)
- **Decision: FALLBACK** — submit `0.179941-0.306897-0.455194-0.249116-0.295985-0.730083`

The F7 ridge appears to be saturating (W11→W12 step was 0.044 — the smallest positive step in the 7-consecutive streak). Users should check their local Step 14 output before submitting, as random-seed interactions may produce slightly different GP μ/σ values.

---

## 5. Module 22 Clustering — Carried Forward from W12

Module 22 clustering remains the **cluster-typology** layer of the analysis. It classifies each function's high-output region by shape (tight vs loose, static vs dynamic, single vs multi-basin). W13 retains the W12 clustering analysis verbatim for F2 (two-zone) and F7 (trending), and uses the `top-3 spread` and `ATB→centroid distance` metrics across all 8 functions.

### F2 — Two-Zone Hierarchical Clustering (Primary Module 22 showcase)

Complete linkage clustering on Euclidean distance in [0,1]² across 12 rounds cleanly separates two basins:

| Zone | Weeks | X2 Region | Centroid | Mean Output |
|------|-------|-----------|----------|-------------|
| Zone A — HIGH X2 | W1, W2, W3, W4, W9 | X2 > 0.50 | [0.733, 0.904] | 0.225 |
| Zone B — LOW X2 | W5, W6, W7, W8, W10, W11, W12 | X2 ≤ 0.50 | [0.704, 0.119] | 0.534 |

Inter-zone distance = 0.963. Zone B spread (now inclusive of W12 0.6880) slightly loosens to 0.028. **W12 added a new high point to Zone B without widening inter-zone separation — confirms Zone B as the high-value basin and establishes stochastic upside within it.**

### F7 — Trending / Dynamic Cluster (Secondary Module 22 showcase)

W6–W12 now form a **7-point** directional cluster. Step sizes: 0.294, 0.185, −0.001, 0.123, 0.130, 0.044. **The W11→W12 step (0.044) is the smallest positive step in the streak — suggests ridge saturation, informs the stricter W13 GP trust conditions.**

---

## 6. Module 23 PCA Integration — New at W13

PCA-style variance analysis applied to each function's W1–W12 history layers **variance-direction vocabulary** on top of Module 22's cluster typology. Module 22 tells us *what shape* each high-output region has; Module 23 tells us *which directions* carry the signal and *which are removable*.

### Module 23 Case Classification

| Function | Module 23 case | Effective dim | Flat PCs | Primary Module 23 lens |
|---|---|---|---|---|
| F1 | Tight attractor (no PC structure reduction) | — | — | — |
| F2 | Kernel-PCA (linear PCA degenerate; two basins) | 2 (kernel) | 0 | Video 1 (kernel PCA) |
| F3 | Scree / 1 flat PC (X1 locked at 1.0 boundary) | 2 | 1 | Video 3 (scree) |
| F4 | Isolated basin (all dims narrow-active, PC1≈0.57) | 4 | 0 | Video 5 (centring) |
| F5 | **Flat-scree / corner** (all dims locked in corner) | **≈0** | **≈4** | **Video 3 (secondary showcase)** |
| F6 | Threshold / dominant-PC (X5 PC1 loading +0.611) | 5 | 0 | Video 2 (max-variance direction) |
| F7 | **Trending ridge** (PC1 share 0.900, \|corr(PC1,y)\|=0.976) | **1** | 0 | **Video 2 + Video 7** |
| **F8** | **Zero-boundary** (X1=X3=X7=0 locked) | **5** | **3** | **Video 3 (PRIMARY showcase)** |

### PRIMARY Module 23 Showcase — F8 (Zero-Boundary, 3 Flat PCs)

F8 is the capstone's most explicit dimensionality-reduction case. In the near-ATB subset (top-5 rows by output, all y > 9.81):

- **X1 variance = 0.00033, mean = 0.025** → ZERO-LOCKED
- **X3 variance = 0.000018, mean = 0.003** → ZERO-LOCKED (tightest dim in capstone)
- **X7 variance = 0.0052, mean = 0.129** → ZERO-LOCKED (looser but confirmed)
- **Scree: [0.928, 0.041, 0.029, 0.003, 0.000, 0.000, 0.000, 0.000]** — PC1 captures 93%; PCs 6, 7, 8 are literally 0.000

**Effective dimensionality reduction: 8 → 5.** Three flat PCs can be removed without information loss within the good cluster.

**Operationalised in code:** `ANISO_SIGMA = [0.006, 0.015, 0.006, 0.015, 0.015, 0.015, 0.006, 0.015]` — X1, X3, X7 (the 3 flat PCs) get σ=0.006 near-zero exploration; the 5 active dims get σ=0.015 normal exploration. The Module 23 insight is not just analysed but **embedded in the candidate generator**.

### SECONDARY Module 23 Showcase — F5 (Flat-Scree, Corner)

F5 required a two-level subset analysis (Top-30% is permissive for F5 because W6–W8 climbing rows pollute the top quantile). The **confirmed-corner subset** (all dims ≥ 0.95, n=3) gives:

- Total variance in subset = **0.000108**
- Per-dim variance: X1=7.4e-5, X2≈0, X3=3.4e-5, X4≈0 — **all 4 dims below lock threshold**
- All 4 PCs effectively flat — the cluster collapses to a single point

### TERTIARY Module 23 Showcase — F7 (Trending Ridge, 1 Dominant PC)

Ridge-only PCA (top-7 W6–W12 points) shows:
- **PC1 share = 0.900** — single dominant direction
- **|corr(PC1 projection, y)| = 0.976** — the 7 points trace a nearly monotonic 1D climb
- PC1 loadings: X1=+0.611 (largest), X3=+0.523, X2=−0.429, X5=−0.373 — X1 dominates, matching the strategy-doc prediction
- y-values along PC1: 2.119 → 2.413 → 2.597 → 2.598 → 2.720 → 2.850 → 2.894 (strict climb)

This is the **PCA-based justification** for F7's GP-pipeline treatment. A 1-dominant-PC structure is exactly where surrogate models extrapolate well — the GP is effectively learning a 1D function. No other function has this geometry, which is why no other function earns GP trust.

---

## 7. Hyperparameters (W13)

| Parameter | Value | Change vs W12 |
|-----------|-------|---------------|
| TOP_PERCENTILE | 30% | unchanged |
| N_CANDIDATES | 10,000 | unchanged |
| EI_XI | 0.01 | unchanged |
| UCB_KAPPA | 2.0 | unchanged |
| GP_RESTARTS | 10 | unchanged |
| FILTER_PERCENTILE | 50 | unchanged |
| CV_FOLDS | 2–5 (adaptive) | unchanged |
| RANDOM_SEED | 42 | unchanged |
| GP kernel | Matérn ν=5/2 + ConstantKernel | unchanged |
| GP alpha (F1-F5, F7, F8) | 1e-6 | unchanged |
| **GP alpha (F6)** | **1e-4** | **RAISED to absorb oracle noise σ~0.063** |
| F7 trust conditions | (1) μ > ATB, (2) R² < 0.999999, (3) gain > σ/2 | **+ condition 3 NEW at W13** |

---

## 8. Limitations and Risks

| Limitation | Description | W13 Mitigation |
|------------|-------------|----------------|
| **Oracle stochasticity** | F2, F3, F6 confirmed stochastic at W12 (σ 0.003–0.063). Identical input, different output. | Replay best-known input. F6 GP alpha raised to 1e-4 to model the noise. |
| **GP over-fitting** | R² = 1.0 on all functions from W6 onward. Surrogate memorises rather than generalises. | ATB override for 7/8 functions. F7 gets GP only because ridge geometry has 1-dominant-PC structure where extrapolation is theoretically justified. |
| **Dimensionality curse** | F8 8D with n=51 = 0.000051% space coverage. | **Module 23 PCA reduces effective dim to 5** — 3-PC flattening turns hopeless 8D search into tractable 5D one. |
| **Non-stationarity** | F4 landscape: 40 non-ATB evaluations all negative; ATB is a single isolated positive basin. | Exact ATB replication; no GP exploration in non-stationary regime. Triple-confirmed deterministic. |
| **Single final query** | W13 = last evaluation. No recovery from a bad submission. | Strict trust conditions on F7; ATB override everywhere else. |
| **F5 npy skip-append** | W12 submission was exact duplicate of W9 row → no row appended, F5 npy stays at n=30. | Documented in README + Data Card; F5 PCA analysis uses widened confirmed-corner criterion to accommodate. |
| **F6 highest noise** | W9 +0.036, W11 −0.010, W12 −0.088 at identical coords = σ 0.063 (range 0.124). | GP cannot beat this without impossibly large predicted gain. ATB override is the only defensible strategy. |
| **F7 ridge saturation** | Step sizes 0.294→0.185→0.123→0.130→**0.044** (decelerating). | W13 trust conditions tightened; author execution produced FALLBACK. |
| **F8 three-zero preservation** | Submission string must contain exact `0.000000` three times. Rounding to 0.001 would violate zero-boundary. | Assertion in Step 14 code verifies exact zeros. |

---

## 9. Intended Use

| Property | Value |
|----------|-------|
| **Primary use** | Imperial College BBO Capstone Project — academic optimisation competition, FINAL query |
| **Secondary use** | Demonstrating Bayesian optimisation pipeline design with Module 22 cluster typology and Module 23 PCA variance analysis |
| **Module coverage** | Mod 17 (CNN-1D) · Mod 19 (TuRBO) · Mod 20 (Ollama) · Mod 22 (Clustering) · **Mod 23 (PCA + dimensionality reduction)** |
| **Out-of-scope** | Production deployment, safety-critical systems, any real-world application without full re-validation and noise characterisation |

---

## 10. What Changed from W12 to W13

| Change | Description |
|--------|-------------|
| New Step 5C (PCA) | Every notebook gains Module 23 variance analysis (scree plots, flat-PC detection, effective dim classification). Notebook grew 29 → 31 cells. |
| F7 3rd trust condition | `gain > σ/2` added on top of W12's `μ > ATB` and `R² < 0.999999`. Final-round risk-minimisation. |
| F6 GP alpha | Raised from 1e-6 to 1e-4 to absorb empirically-measured oracle noise (σ ≈ 0.063). |
| F5 npy | Unchanged from W12 (skip-append: W12 submission = exact W9 row duplicate). |
| ATB updates | F2: 0.6497 → 0.6880 (W12 NEW ATB). F7: 2.8501 → 2.8939 (W12 NEW ATB, 7th consecutive). |
| Oracle noise quantification | F2 σ~0.035, F3 σ~0.003, F6 σ~0.063 — quantified from W12 replay data. New sub-block in hyperparameters JSON per function. |
| `pca_analysis` JSON block | New in every W13 hyperparameters file — stores scree ratios, locked dims, effective dim, Module 23 case classification. |
| Submission TXT comment headers | Extended to 4 lines: metadata, ATB history, noise/PCA lens, raw coords. |

---

*BBO Capstone Model Card — Mike Kennelly — Imperial College — Week 13 FINAL Query*
