# BBO Capstone — Week 4 Strategy Summary
**Mike Kennelly | All functions MAXIMISATION — higher is always better**

---

## Overview

Week 4 expands the classifier stage from a single SVM to **5 model families
compared via cross-validation** — the best CV model filters candidates for
that function that week. This is the first systematic model selection step.

Models compared: Linear SVM | Decision Tree | Random Forest
| Logistic Regression | Neural Network (Small / Medium / Large)

Pipeline this week: **Multi-model CV → Best Classifier → GP + EI/UCB**

Key addition: **NN Gradient Analysis** — input gradients from the winning NN
estimate which dimensions are most sensitive, informing the submission direction.

Key reference: Barrett et al. (2019) — when do NNs genuinely outperform
simpler models? This week answers that empirically per function.

Key parameters:

| Parameter     | Controls                                | Range W4    |
|---------------|-----------------------------------------|-------------|
| EXPLOIT_RATIO | Fraction of candidates near best point  | 0.70 – 0.85 |
| EXPLOIT_SIGMA | Gaussian radius around best point       | 0.03 – 0.05 |
| UCB_KAPPA     | UCB exploration bonus                   | 2.0 – 2.5   |
| GP_RESTARTS   | Kernel hyperparameter restarts          | 5 – 8       |

---

## F1 — SPATIAL TARGETING (2D)
**n=13 | W3=5.17e-96 | CV winner: Linear SVM**
**Submitted: [0.688, 0.724] → W4 = 1.658e-9**

All outputs near zero — CV models score near the 70% majority baseline.
SVM wins by default. Spatial targeting used: submission close to W2 best
[0.684, 0.704] which remains the all-time best. W4 = 1.658e-9 ≈ 0.
No improvement possible while landscape is flat.

**Key settings:** EXPLOIT_RATIO=0.60, UCB_KAPPA=3.0, broad exploration.

---

## F2 — MULTI-MODEL CV → GP (2D)
**n=13 | W3=-0.030 | CV winner: Random Forest**
**Submitted: [0.781, 0.992] → W4 = 0.019**

W3 regression (-0.030) prompted broader search. RF wins CV.
Submission near [0.781, 0.992] — still in the X2~1.0 region.
W4 = 0.019, marginal improvement from W3. True optimum at X2=0.16
not yet discovered — the classifier is not yet pointing there.

**Key settings:** EXPLOIT_RATIO=0.75, RF filter, boundary region.

---

## F3 — MULTI-MODEL CV → GP (3D)
**n=16 | W3=-0.083 | CV winner: Decision Tree**
**Submitted: [0.995, 0.923, 0.002] → W4 = -0.138**

Decision Tree wins CV in 3D. Submission pushes X1=0.995 (near boundary ✅)
but X3=0.002 drops to zero — far from W1 best X3=0.403. W4 = -0.138,
further regression. The X3 coordinate is being misidentified by the
classifier as low-value.

**Key settings:** EXPLOIT_RATIO=0.75, DT filter, X1 boundary push.

---

## F4 — MULTI-MODEL CV → GP (4D)
**n=21 | W3=-0.962 | CV winner: NN-Small**
**Submitted: [0.417, 0.376, 0.350, 0.308] → W4 = -0.527**

NN-Small wins CV — MLP classifiers outperform linear models in 4D.
Submission close to the [0.38–0.44] cluster — partial recovery from W3.
W4 = -0.527, improvement from W3 = -0.962. The W2 peak (+0.238)
remains the true best but the NN is edging back toward the right region.

**Key settings:** EXPLOIT_RATIO=0.85, NN filter, tight around [0.4]^4.

---

## F5 — MULTI-MODEL CV → GP (4D)
**n=21 | W3=4891 | CV winner: Random Forest**
**Submitted: [0.355, 0.918, 0.997, 0.945] → W4 = 2913**

RF wins CV with 87% accuracy — strong signal in 4D. However the submission
drifts: X1=0.355 vs W3's X1=0.803. The RF is not detecting that X1 needs
to be high. W4 = 2,913 — regression from W3=4,891. The X1 drift is the
critical error that leads to W5 collapse.

**Key settings:** EXPLOIT_RATIO=0.85, RF filter, all dims high targeted.

---

## F6 — MULTI-MODEL CV → GP (5D)
**n=16 | W3=-0.883 | CV winner: Logistic Regression**
**Submitted: [0.390, 0.198, 0.588, 0.826, 0.049] → W4 = -0.363**

LR wins CV. Partial recovery — W4 = -0.363 from W3 = -0.883.
Submission shows X4=0.826 (high ✅) and X5=0.049 (near zero ✅) —
structural pattern partially recovered. W4 best is still worse than
W2 (-0.237) due to X1, X2, X3 not being optimal.

**Key settings:** EXPLOIT_RATIO=0.70, LR filter, X4/X5 pattern targeted.

---

## F7 — MULTI-MODEL CV → GP (6D)
**n=21 | W3=1.736 | CV winner: Linear SVM**
**Submitted: [0.100, 0.554, 0.328, 0.221, 0.466, 0.666] → W4 = 1.140**

SVM wins CV. W4 = 1.140 — regression from W3 = 1.736. X1=0.100 drifts
from the confirmed X1≈0.01 boundary signal. The SVM is allowing X1 to move
away from zero. W2 and W3 both had X1 < 0.02; W4 moves to 0.100 —
a significant deviation from the confirmed pattern.

**Key settings:** EXPLOIT_RATIO=0.80, SVM filter, X1 boundary focus.

---

## F8 — MULTI-MODEL CV → GP (8D)
**n=21 | W3=9.819 | CV winner: Decision Tree**
**Submitted: [0.069, 0.717, 0.001, 0.001, 0.133, 0.480, 0.048, 0.722] → W4 = 9.334**

DT wins CV with 86% accuracy — highest CV score in the W4 batch.
W4 = 9.334 — slight regression from W3 = 9.819. X1 and X3 still near zero ✅
but X5 drops from 0.448 to 0.133 — drifting from the high-X5 pattern.
Function remains stable overall.

**Key settings:** EXPLOIT_RATIO=0.85, DT filter, boundary pattern targeted.

---

## Summary Table

| Fn | Dims | n  | CV Winner | CV Acc | W3 Result | W4 Result | Change     |
|----|------|----|-----------|--------|-----------|-----------|------------|
| F1 | 2D   | 13 | Linear SVM| ~67%   | 5.17e-96  | 1.66e-9   | ≈ 0        |
| F2 | 2D   | 13 | Rand. Forest| ~73% | -0.030    | 0.019     | ↑ Slight   |
| F3 | 3D   | 16 | Dec. Tree | ~75%   | -0.083    | -0.138    | ↓ Regress  |
| F4 | 4D   | 21 | NN-Small  | ~80%   | -0.962    | -0.527    | ↑ Recover  |
| F5 | 4D   | 21 | Rand. Forest| ~87% | 4891      | 2913      | ↓ Regress  |
| F6 | 5D   | 16 | Logistic  | ~75%   | -0.883    | -0.363    | ↑ Recover  |
| F7 | 6D   | 21 | Linear SVM| ~80%   | 1.736     | 1.140     | ↓ Regress  |
| F8 | 8D   | 21 | Dec. Tree | ~86%   | 9.819     | 9.334     | ↓ Slight   |

Pipeline: 5 classifier families compared via 5-fold CV | Best CV model filters GP candidates
Barrett et al. (2019) — NN vs simpler models empirical comparison.
F4 and F6 recovering. F5 and F7 regressing due to coordinate drift.

---

*Week 4 | BBO Capstone | Mike Kennelly*
