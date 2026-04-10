# Model Card — BBO Capstone Week 11
### Mike Kennelly | Imperial College | Penultimate Query

---

## 1. Model Overview

| Property | Value |
|----------|-------|
| **Model name** | Adaptive Multi-Classifier + GP/EI Pipeline |
| **Version** | Week 11 — Penultimate iteration |
| **Framework** | scikit-learn 1.x · PyTorch (CNN-1D) · scipy · Ollama llama3.1 |
| **Task** | Black-Box Optimisation — MAXIMISE f(x), x in [0,1]^d |
| **Functions** | F1 (2D) · F2 (2D) · F3 (3D) · F4 (4D) · F5 (4D) · F6 (5D) · F7 (6D) · F8 (8D) |
| **Total queries** | 11 per function (one submission per week) |
| **Author** | Mike Kennelly — Imperial College BBO Capstone |
| **Date** | Week 11, April 2026 |

---

## 2. Model Architecture

The pipeline runs four sequential stages each week per function.

### Stage 1 — Binary Classification (8-model CV ensemble)

Historical evaluations labelled: top-30% outputs = class 1 (HIGH), remainder = class 0 (LOW).
Eight classifier families trained and ranked by stratified k-fold cross-validation. The winner
filters the candidate pool passed to the GP.

| # | Model | Key Parameters | Role / W11 Notes |
|---|-------|----------------|-----------------|
| 1 | Linear SVM | C=1.0, probability=True | Won F6 W11 (aniso sigma run) |
| 2 | Decision Tree | max_depth=4 | Axis-aligned splits |
| 3 | Random Forest | n_estimators=100 | Won F4 W11, F8 W11 (CV~90%) |
| 4 | Logistic Regression | max_iter=1000, L2 | Won F7 W11 |
| 5 | NN-Small | (16,8), early_stopping | Won F3 W11 |
| 6 | NN-Medium | (64,32), early_stopping | General-purpose |
| 7 | NN-Large | (128,64,32), early_stopping | Won F2 W11 (CNN-1D run) |
| 8 | CNN-1D (Module 17) | Conv1d(1->8, k=2) + ReLU + Dropout(0.3) + Linear | Learning exercise — won F2 W11 run2 |

### Stage 2 — Candidate Generation (Anisotropic TuRBO)

10,000 candidates generated per function. Exploitation candidates drawn from
anisotropic Gaussian N(best_point, diag(ANISO_SIGMA^2)) — per-dimension sigma set by
Ollama llama3.1 sensitivity analysis (Module 20 learning exercise). Exploration candidates
are uniform random draws across [0,1]^d. CV winner filters pool to top 50% by P(class=1).

### Stage 3 — Gaussian Process Regression

Matern v=5/2 kernel + ConstantKernel, normalize_y=True, n_restarts_optimizer=10.
Fitted on full labelled history. R2=1.0 for most functions (memorising) from W6 onward.

### Stage 4 — Acquisition Functions (EI + UCB)

```
EI(x) = (mu(x) - y_best - xi)*Phi(Z) + sigma(x)*phi(Z)    Z = (mu(x) - y_best - xi)/sigma(x)    xi = 0.01
UCB(x) = mu(x) + kappa*sigma(x)    kappa = 2.0
```

For functions under **ATB override** (run2 notebooks): GP runs for documentation but
the submission uses confirmed ATB coordinates directly.
For **F7**: GP pipeline trusted — genuine gradient signal from 5 consecutive improvements.

---

## 3. Week 11 Strategy Per Function

### Overview

W11 introduced a dual-notebook approach for most functions:
- **run1 notebook** — full GP pipeline with Ollama-guided ANISO_SIGMA
- **run2 notebook** — ATB OVERRIDE, submitting confirmed best coordinates directly

The run2 (override) string was submitted in all cases except F7.

| Fn | Dims | W10 ATB | W10 Score | W11 Strategy | W11 Override String | W11 Result |
|----|------|---------|-----------|--------------|---------------------|------------|
| F1 | 2D | 8.838e-07 (W2) | 4.109e-58 | ATB OVERRIDE — replicate W2 best [0.684, 0.704] | 0.684200-0.704200 | **8.968e-07 NEW ATB** |
| F2 | 2D | 0.6497 (W9) | 0.163649 | ATB OVERRIDE — replicate W9/W5 best | 0.710068-0.161630 | 0.6090 (regressed) |
| F3 | 3D | -0.000707 (W6) | -0.090154 | ATB OVERRIDE — replicate W6 best [0.998, 0.621, 0.453] | 0.998126-0.621218-0.453080 | **-0.001285 NEW ATB** |
| F4 | 4D | 0.23759 (W2) | -1.801384 | ATB OVERRIDE — replicate W2 best | 0.439249-0.414994-0.384687-0.397917 | 0.23759 (exact match) |
| F5 | 4D | 8662.48 (W9) | 8471.330 | ATB OVERRIDE — corner [1,1,1,1] | 1.000000-1.000000-1.000000-1.000000 | 8662.48 (exact match) |
| F6 | 5D | 0.03602 (W9) | -0.144285 | ATB OVERRIDE — replicate W9 best | 0.406643-0.339495-0.634775-0.769397-0.115269 | -0.01024 (regressed) |
| F7 | 6D | 2.7201 (W10) | 2.7201 | GP PIPELINE — gradient continue, 5th consecutive | GP EI output | **2.8501 NEW ATB** |
| F8 | 8D | 9.8251 (W7) | 9.8013 | SPARSITY HYPOTHESIS — zero X1/X3/X7 | GP EI output | 9.8269 (below ATB) |

### W11 Hyperparameters Per Function

| Fn | EXPLOIT_RATIO | ANISO_SIGMA | EI_XI | UCB_KAPPA | GP_RESTARTS | CV Winner (run1) |
|----|--------------|-------------|-------|-----------|-------------|-----------------|
| F1 | 0.85 | [0.015, 0.015] | 0.01 | 2.0 | 10 | Random Forest |
| F2 | 0.92 | [0.012, 0.008] | 0.01 | 2.0 | 10 | CNN-1D (run2) / RF (run1) |
| F3 | 0.92 | [0.005, 0.020, 0.025] | 0.01 | 2.0 | 10 | NN-Small |
| F4 | 0.92 | [0.012, 0.012, 0.012, 0.012] | 0.01 | 2.0 | 10 | Random Forest |
| F5 | 0.95 | [0.005, 0.005, 0.005, 0.005] | 0.01 | 2.0 | 10 | Linear SVM |
| F6 | 0.92 | [0.015, 0.015, 0.015, 0.015, 0.008] | 0.01 | 2.0 | 10 | Linear SVM |
| F7 | 0.92 | [0.015, 0.012, 0.012, 0.012, 0.012, 0.015] | 0.01 | 2.0 | 10 | Logistic Regression |
| F8 | 0.95 | [0.006, 0.015, 0.006, 0.015, 0.015, 0.015, 0.006, 0.015] | 0.01 | 2.0 | 10 | Random Forest |

---

## 4. W11 Results Analysis

### What Changed from W10 to W11

| Fn | W10 | W11 | Delta | Outcome |
|----|-----|-----|-------|---------|
| F1 | 4.109e-58 | **8.968e-07** | +8.97e-07 | NEW ATB — spatial targeting to [0.684, 0.704] worked |
| F2 | 0.163649 | 0.6090 | +0.445 | Recovery but below W5 ATB (0.6497) |
| F3 | -0.090154 | **-0.001285** | +0.089 | NEW ATB — X1=0.998 anchor confirmed |
| F4 | -1.801384 | 0.23759 | +2.039 | Matched W2 ATB exactly — coords confirmed |
| F5 | 8471.330 | 8662.48 | +191.2 | Matched W9 ATB exactly — corner confirmed |
| F6 | -0.144285 | -0.01024 | +0.134 | Recovery but below W9 ATB (0.03602) |
| F7 | 2.7201 | **2.8501** | +0.130 | NEW ATB — 6th consecutive improvement |
| F8 | 9.8013 | 9.8269 | +0.026 | Recovery but below W2 ATB (9.8320) |

**W11 summary:** 3 new ATBs (F1, F3, F7). 2 exact ATB matches (F4, F5). 3 regressions that still recovered vs W10 (F2, F6, F8).

---

## 5. Module Integration

### Module 17 — CNN-1D (Learning Exercise)

A tiny 1D CNN (Conv1d(1->8, k=2) + ReLU + Dropout(0.3) + Linear(8->1)) is included as
Model 8 in the CV comparison across all functions. Tracks CNN performance week-on-week as
n grows toward 40+. At W11:

| Fn | n | n/dims | CNN CV | vs Best Classifier | CNN Status |
|----|---|--------|--------|-------------------|------------|
| F1 | 19 | 9.5 | 71.7% | ~= SVM (71.7%) | Floor case — 2D, 3 positives |
| F2 | 20 | 10.0 | 77.4% | Won (run2) | Competitive at n=20 |
| F3 | 24 | 8.0 | Low | Lost to NN-Small | 3D, small n |
| F4 | 39 | 9.75 | Moderate | Lost to RF | 4D, non-stationary |
| F5 | 30 | 7.5 | Low | Lost to Linear SVM | Corner landscape |
| F6 | 29 | 5.8 | 77.4% | 4th of 8 | 5D — moderate |
| F7 | 39 | 6.5 | Good | Competitive | 6D — best CNN data budget |
| F8 | 49 | 6.1 | Moderate | Lost to RF | 8D, 7 adjacent pairs |

### Module 19 — TuRBO / Delimiting Context

Anisotropic sigma values are set using the TuRBO framework principle: tight sigma on
high-sensitivity or structurally-anchored dimensions, relaxed sigma on low-sensitivity
dimensions. Applied explicitly in F3 (X1 sigma=0.005 to lock boundary), F6 (X5 sigma=0.008
to lock threshold dimension), F8 (X1/X3/X7 sigma=0.006 for zero-boundary anchors).

### Module 20 — Ollama llama3.1

Ollama (localhost:11434) called via Step 11B in each notebook with structured prompts
following 5 principles: role anchor, context before data, structured data format,
one-shot example, chain-of-thought reasoning. Outputs per-dimension sigma recommendations
(ANISO_SIGMA) for the candidate generation step. Three iterative runs per function with
settings updated between each.

### Module 22 — Clustering (Applied retrospectively to W11 strategy)

Module 22 hierarchical clustering applied to W1-W10 history to justify W11 ATB override
decisions. See Data Card for full cluster analysis.

---

## 6. Limitations

| Limitation | Description | W11 Impact |
|------------|-------------|------------|
| GP memorisation | R2=1.0 for F1, F2, F3, F4, F6, F8 — surrogate memorises data | ATB override used for 7/8 functions |
| Stochastic oracle | F2 W11 exact W5 coords returned 0.609 not 0.6497 | Accepted — best known coords still submitted |
| n/p at floor | F6: n/p=5.8, F8: n/p=6.1 — borderline for reliable GP | Mitigated by classifier pre-filtering |
| Non-stationarity | F4: 9 explorations near ATB all negative in W3-W10 | W11 override matched ATB exactly, confirming coords |
| Single query | One portal submission per week — no correction possible | ATB override is the risk-minimising strategy |

---

## 7. Intended Use

| Property | Value |
|----------|-------|
| **Primary use** | Imperial College BBO Capstone — academic optimisation competition |
| **Secondary use** | Assessment demonstration of Bayesian optimisation pipeline design |
| **Module coverage** | Mod 17 (CNN-1D) · Mod 19 (TuRBO) · Mod 20 (Ollama) · Mod 22 (clustering) |
| **Out-of-scope** | Production deployment or any real-world application |

---

*BBO Capstone Model Card — Mike Kennelly — Imperial College — Week 11*
