# #Model Card — BBO Capstone Pipeline

**Project:** Black-Box Optimisation Capstone  
**Author:** Mike Kennelly — Imperial College London, ML & AI Professional Certificate  
**Version:** Week 7 pipeline | Last updated: March 2026

---

## Model Description

### Inputs

An n-dimensional coordinate vector **x** ∈ [0,1]ⁿ, where n ∈ {2, 3, 4, 5, 6, 8} depending on the function. At inference time, the pipeline evaluates 10,000 candidate points and selects one to submit.

### Outputs

A single n-dimensional coordinate string (e.g. `0.688952-0.168811`) representing the point most likely to be the global maximum of the target function, as estimated by the GP surrogate.

### Model Architecture

The pipeline is a **two-stage sequential system** combining a classifier ensemble with a Gaussian Process surrogate:

**Stage 1 — Classifier Ensemble (candidate filtering)**

Eight classifiers are trained on binary-labelled historical observations (top 30% = class 1). All eight are evaluated with 2-fold cross-validation, and the winner filters 10,000 generated candidates to the top 50% by P(class=1):

| Model | Architecture | Notes |
|-------|-------------|-------|
| Linear SVM | Linear kernel, C=1 | Fast; good on small n with linear boundaries |
| Decision Tree | Max depth 5 | Captures non-linear splits; prone to overfit at small n |
| Random Forest | 100 estimators | Ensemble stability; strong on structured patterns |
| Logistic Regression | L2, C=1 | Probabilistic; reliable baseline |
| NN-Small | [16, 8] | Simple landscapes; minimal parameters |
| NN-Medium | [64, 32] | General purpose; W7 winner for F1 |
| NN-Large | [128, 64, 32] | High-complexity landscapes; more data needed |
| CNN-1D | Conv1d(8 filters, kernel=2) → Pool → FC(32,16,1) | 33 params; scans adjacent coordinate pairs; added W6 as learning exercise |

**Stage 2 — Gaussian Process Surrogate**

A GP with Matérn ν=5/2 kernel (+ ConstantKernel amplitude) is fitted to all historical observations and used to compute acquisition functions over the filtered candidate set:

- **Kernel:** `ConstantKernel(1.0) × Matérn(length_scale=1.0, ν=2.5)`
- **Fitting:** `normalize_y=True`, `alpha=1e-6` (numerical stability nugget), `n_restarts=5`
- **Acquisition functions:**
  - **EI (primary):** `EI(x) = (μ - y_best - ξ)·Φ(Z) + σ·φ(Z)`, ξ=0.01
  - **UCB (reference):** `UCB(x) = μ + κ·σ`, κ=2.5–3.0
- **Submission:** argmax EI over the classifier-filtered candidate set

**Candidate generation:**

10,000 points generated per function using a hybrid scheme:
- Exploitation: Gaussian samples centred on best-known point (σ adapted per-function per-week)
- Exploration: Sobol quasi-random sequences for uniform space coverage

---

## Performance

### Classification CV Accuracy (W7, all 8 functions)

| Fn | CV Winner | CV Accuracy | Notes |
|----|-----------|------------|-------|
| F1 | NN-Medium (64,32) | 79.5% ± 8.0% | Flat landscape — limited signal |
| F2 | Random Forest | 93.8% ± 6.3% | Clear peak structure; strong classification signal |
| F3 | Random Forest | — | X1 boundary pattern detectable |
| F4 | Linear SVM | 83.3% | Tight cluster [0.38–0.44] — local structure strong |
| F5 | Random Forest | 88.0% | X2–X4=1.0 boundary — clearest structure in batch |
| F6 | Random Forest | — | X4 high / X5 low pattern |
| F7 | Linear SVM | 77.1% | X1≈0 boundary; CNN filter maps confirm |
| F8 | Decision Tree | 86.7% | Best n/dims ratio; most statistically meaningful |

*Note: CV uses 2 folds at n=15–45 — accuracy estimates have high variance. Treat directionally, not as precise metrics.*

### GP Fit Quality (W7)

| Fn | GP R² | Fitted length-scale | Interpretation |
|----|-------|-------------------|----------------|
| F1 | 1.000 | 0.107 | Interpolates perfectly; short length-scale signals sharp local structure |
| F2 | 1.000 | 0.229 | Smooth landscape; longer correlations |

GP achieves R²=1.0 on training data across all functions (interpolating regime — not generalisation). This is expected and correct for GP surrogates: the GP memorises all observations and uses uncertainty (σ) between points to guide search.

### Week-on-Week Trajectory (F1, illustrative)

F1 best values have remained near zero since W2 — the landscape is extremely flat. The GP correctly reports high uncertainty (wide UCB band) and the pipeline correctly escalates to EXPLORE mode (σ=0.216, expand strategy).

F2 shows a clear peak structure with best value 0.6497 at [0.71, 0.16] established in W5. W7 exploitation submission at [0.689, 0.169] confirms the GP has converged on the correct region.

---

## Limitations

**Small sample sizes:** At n=15 (F1, F2), 2-fold CV leaves only ~7 samples per fold. Cross-validation accuracy is noisy and should be treated as a directional signal, not a precise performance estimate.

**No access to true function:** The model cannot be evaluated against a ground truth landscape — performance is measured only by the score returned by the portal oracle. The GP's uncertainty estimate is the only internal quality signal.

**GP interpolation vs generalisation:** GP achieves R²=1.0 on training data by construction (it interpolates). The meaningful diagnostic is the fitted kernel length-scale (short = sharp local structure; long = smooth landscape).

**CV fold count:** 2-fold CV was chosen to maximise training data at small n, but this gives high-variance accuracy estimates. For n>50, increasing to 5-fold is recommended.

**CNN-1D overfitting:** With n=15–35 and 33 parameters, the CNN-1D overfits the training data. It is included as a learning exercise (Module 17 CNN inspection) and its filter maps provide qualitative structural insight; its CV accuracy should not be over-interpreted.

**Anisotropic sigma (F7):** The anisotropic sigma decision (`σ=[0.015, 0.035×5]`) is motivated by CNN filter map analysis which showed X1 dominance. This is a novel heuristic not yet validated against a ground-truth landscape — the W7 result will confirm or refute this choice.

---

## Trade-offs

**Exploitation vs Exploration:**  
Higher `EXPLOIT_RATIO` (0.85–0.9) concentrates the candidate pool near the current best, giving the GP high-quality local candidates but risking missing undiscovered global peaks. F1 demonstrates this failure mode: 6 weeks of exploitation near a flat peak returned near-zero scores. The W7 EXPAND strategy corrects this.

**Classifier filtering removes valid candidates:**  
Filtering by P(class=1) > 50th percentile removes half the candidate pool before GP evaluation. If the true global maximum happens to be in a region the classifier mislabels as class 0 (particularly at small n), the GP will never evaluate it. This is a known trade-off: filtering improves GP efficiency but introduces classifier-induced blind spots.

**GP computational cost vs quality:**  
GP inference scales as O(n³) with the number of training points. At n=45 (F8), this is manageable. As weeks progress to W13 (n≈100+), GP fitting will become slower and may require sparse GP approximations.

**Two-stage pipeline introduces compounding error:**  
A classification error in Stage 1 propagates to Stage 2 — the GP never sees the misclassified region. The CV winner selection mitigates this (choosing the most reliable classifier each week), but cannot eliminate it.

---

## Intended Use

This pipeline is designed for **sequential black-box optimisation under extreme query budgets** (1 query per week). It is suited for:
- Educational demonstration of Bayesian Optimisation principles
- Portfolio demonstration of multi-model CV, GP surrogates, and acquisition function design
- Research into hybrid classifier + GP pipelines for small-n high-dimensional settings

It is **not** suited for:
- Production systems requiring guaranteed convergence bounds
- Safety-critical applications where model errors have real-world consequences
- Settings where n > 200 without switching to sparse GP approximations
