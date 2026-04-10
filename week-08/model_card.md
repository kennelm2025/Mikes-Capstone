# Model Card — BBO Capstone Pipeline

**Project:** Black-Box Optimisation Capstone  
**Author:** Mike Kennelly — Imperial College London, ML & AI Professional Certificate  
**Version:** Week 8 pipeline | Last updated: March 2026

---

## Model Description

### Inputs

An n-dimensional coordinate vector **x** ∈ [0,1]ⁿ, where n ∈ {2, 3, 4, 5, 6, 8} depending on the function. At inference time, the pipeline evaluates 10,000 candidate points and selects one to submit.

### Outputs

A single n-dimensional coordinate string (e.g. `0.413304-0.095516-0.381193-0.266170-0.353901-0.693102`) representing the point most likely to be the global maximum of the target function, as estimated by the GP surrogate.

### Model Architecture

The pipeline is a **two-stage sequential system** combining a classifier ensemble with a Gaussian Process surrogate:

**Stage 1 — Classifier Ensemble (candidate filtering)**

Eight classifiers are trained on binary-labelled historical observations (top 30% = class 1). All eight are evaluated with stratified k-fold cross-validation (2–5 folds depending on sample size), and the winner filters 10,000 generated candidates to the top 50% by P(class=1):

| Model | Architecture | Notes |
|-------|-------------|-------|
| Linear SVM | Linear kernel, C=1 | Fast; good on small n with linear boundaries |
| Decision Tree | Max depth 5 | Captures non-linear splits; prone to overfit at small n |
| Random Forest | 100 estimators | Ensemble stability; strong on structured patterns |
| Logistic Regression | L2, C=1 | Probabilistic; reliable baseline |
| NN-Small | [16, 8] | Simple landscapes; minimal parameters |
| NN-Medium | [64, 32] | General purpose |
| NN-Large | [128, 64, 32] | High-complexity landscapes; more data needed |
| CNN-1D | Conv1d(8 filters, kernel=2) → Pool → FC(32,16,1) | 33 params; scans adjacent coordinate pairs; added W6 as learning exercise |

**Stage 2 — Gaussian Process Surrogate**

A GP with Matérn ν=5/2 kernel (+ ConstantKernel amplitude) is fitted to all historical observations and used to compute acquisition functions over the filtered candidate set:

- **Kernel:** `ConstantKernel(1.0) × Matérn(length_scale=1.0, ν=2.5)`
- **Fitting:** `normalize_y=True`, `alpha=1e-6` (numerical stability nugget), `n_restarts=5–10`
- **Acquisition functions:**
  - **EI (primary):** `EI(x) = (μ - y_best - ξ)·Φ(Z) + σ·φ(Z)`, ξ=0.01
  - **UCB (reference):** `UCB(x) = μ + κ·σ`, κ=2.0–4.0
- **Submission:** argmax EI over the classifier-filtered candidate set

**Candidate generation — W8:**

10,000 points generated per function using a hybrid scheme:

| Function | Exploit ratio | Exploit σ | Explore ratio | Notes |
|----------|-------------|---------|-------------|-------|
| F1 | 0.20 | 0.40 | 0.80 | Extreme explore — 7 near-zero weeks |
| F2 | 0.90 | 0.010 | 0.10 | Precision around W5 best [0.710,0.162] |
| F3 | 0.90 | 0.018 | 0.10 | Tighten around W7 best [1.0,0.572,0.504] |
| F4 | 0.35 | 0.12 | 0.65 | Wide explore — inject abandoned |
| F5 | 0.90 | 0.035 | 0.10 | Push X1 toward 1.0; X2-X4 locked |
| F6 | 0.85 | 0.025 | 0.15 | Return to W6 region; tighten |
| F7 | 0.90 | [0.012, 0.028×5] | 0.10 | Anisotropic — X1 confirmed dominant |
| F8 | 0.92 | 0.012 | 0.08 | Tightest settings — 0.007 from ATB |

---

## Performance

### W7 Actual Results

| Fn | W7 Score | ATB | New Best? | Δ vs ATB | Key Observation |
|----|---------|-----|-----------|---------|----------------|
| F1 | ≈0 | 8.84e-7 (W2) | ✗ | −8.84e-7 | 7th consecutive near-zero |
| F2 | 0.5338 | 0.6497 (W5) | ✗ | −0.116 | Drift continues from W5 peak |
| F3 | −0.00534 | −0.00534 (W7) | ★ | — | New best; X1=1.0 confirmed |
| F4 | −0.2651 | 0.2376 (W2) | ✗ | −0.503 | Inject failed conclusively |
| F5 | 7596.79 | 7596.79 (W7) | ★ | — | +1722 vs W6; X1 climbing |
| F6 | −0.3422 | −0.1727 (W6) | ✗ | −0.170 | W7 expand failed |
| F7 | 2.4134 | 2.4134 (W7) | ★ | — | Anisotropic σ confirmed |
| F8 | 9.8251 | 9.8320 (W2) | ✗ | −0.007 | 0.007 from ATB |

### Classification CV Accuracy (W7/W8)

| Fn | CV Winner | CV Accuracy | Notes |
|----|-----------|------------|-------|
| F1 | NN-Medium (64,32) | ~79% | Flat landscape — limited signal |
| F2 | Random Forest | ~94% | Clear peak structure |
| F3 | Random Forest | — | X1=1.0 boundary detectable |
| F4 | Linear SVM | ~83% | Cluster signal weakened after inject failure |
| F5 | Random Forest | ~88% | X2–X4=1.0 boundary — clearest in batch |
| F6 | Random Forest | — | X4 high / X5 low pattern |
| F7 | Linear SVM | ~77% | X1≈0 boundary; anisotropic structure confirmed |
| F8 | Decision Tree | ~87% | Best n/dims ratio; most statistically meaningful |

*Note: CV uses 2–5 folds at n=16–46 — accuracy estimates have high variance. Treat directionally, not as precise metrics.*

### GP Fit Quality

GP achieves R²≈1.0 on training data across all functions (interpolating regime — not generalisation). This is expected and correct for GP surrogates: the GP memorises all observations and uses uncertainty (σ) between points to guide search. The meaningful diagnostic is the fitted kernel length-scale: short = sharp local structure; long = smooth landscape.

### Week-on-Week Trajectory (W7 highlights)

F5 set a new all-time best of 7596.79 — a +1722 jump from W6=5875. X2–X4 are saturated at 1.0; the GP is now focused on driving X1 toward the 1.0 boundary. F7 confirmed the anisotropic σ hypothesis with a new best of 2.4134 (+0.294 vs W6). F4 inject strategy failed conclusively — W2 coordinates are not reproducible; W8 pivots to wide exploration.

### GP Fit Quality

GP achieves R²≈1.0 on training data across all functions (interpolating regime — not generalisation). This is expected and correct for GP surrogates: the GP memorises all observations and uses uncertainty (σ) between points to guide search. The meaningful diagnostic is the fitted kernel length-scale: short = sharp local structure; long = smooth landscape.

---

## Validated Methodologies (W7 Confirmation)

**Anisotropic sigma (F7):** The hypothesis that X1 is the dominant structural dimension in F7, motivated by CNN-1D filter map analysis in W6, was confirmed by the W7 result. The anisotropic submission `σ=[0.015, 0.035×5]` yielded a new all-time best of 2.4134 (+0.294 vs W6). This is the first pipeline methodology validated by a portal score result. W8 tightens further to `σ=[0.012, 0.028×5]`.

---

## Limitations

**Small sample sizes:** At n=16 (F1, F2), 2-fold CV leaves only ~8 samples per fold. Cross-validation accuracy should be treated as a directional signal, not a precise performance estimate.

**No access to true function:** The model cannot be evaluated against a ground truth landscape. The GP's uncertainty estimate is the only internal quality signal.

**GP interpolation vs generalisation:** GP achieves R²≈1.0 on training data by construction. Meaningful diagnostics are the fitted kernel length-scale and GP sigma at candidate points.

**CNN-1D overfitting:** With n=16–36 and 33 parameters, the CNN-1D overfits training data. It is included as a learning exercise and its filter maps provide qualitative structural insight for anisotropic sigma decisions.

**F4 landscape uncertainty:** After W7 confirmed the W2 inject failed, the landscape structure of F4 is unclear. With 36 training points at n/p=9.0, the GP has sufficient data to guide exploration but the true peak location is unknown.

**F1 structural ambiguity:** Seven consecutive near-zero weeks raise the possibility that F1 may be a near-zero function everywhere, not just in the regions explored so far. W8 extreme explore (σ=0.40, ratio=0.20) is the final test before reassessing.

---

## Trade-offs

**Exploitation vs Exploration:**  
Higher `EXPLOIT_RATIO` concentrates the candidate pool near the current best, giving the GP high-quality local candidates but risking missing undiscovered global peaks. F1 (7 near-zero weeks) and F4 (failed inject) both demonstrate this failure mode. W8 corrects both with aggressive exploration.

**Anisotropic vs isotropic sigma:**  
Anisotropic sigma gives the GP finer-grained control over the exploit region shape, but requires structural knowledge of which dimensions are dominant. For F7, CNN filter map analysis provided this signal. For other functions without confirmed structural patterns, isotropic sigma remains appropriate.

**Classifier filtering blind spots:**  
Filtering by P(class=1) > 50th percentile removes half the candidate pool before GP evaluation. If the true global maximum is in a region the classifier mislabels as class 0, the GP will never evaluate it. This risk is highest for F1 (flat landscape, low classification signal) and F4 (landscape structure unclear after inject failure).

**GP computational cost:**  
GP inference scales as O(n³). At n=46 (F8), this is manageable. As weeks progress toward W13 (n≈100+), GP fitting will become slower and may require sparse GP approximations.

---

## Intended Use

This pipeline is designed for **sequential black-box optimisation under extreme query budgets** (1 query per week). It is suited for:
- Educational demonstration of Bayesian Optimisation principles
- Portfolio demonstration of multi-model CV, GP surrogates, acquisition function design, and anisotropic exploitation
- Research into hybrid classifier + GP pipelines for small-n high-dimensional settings

It is **not** suited for:
- Production systems requiring guaranteed convergence bounds
- Safety-critical applications where model errors have real-world consequences
- Settings where n > 200 without switching to sparse GP approximations
