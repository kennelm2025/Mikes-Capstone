# BBO Capstone — Week 5 Strategy Summary
**Mike Kennelly | All functions MAXIMISATION — higher is always better**

---

## Overview

Week 5 uses the same 5-model CV pipeline as Week 4 — the pipeline is now
stabilised. The key development this week is the **week log system**: submission
emails were cross-referenced against npy files to identify missing data points.
This revealed that several functions had incomplete histories in their npy files,
with W2, W3 and W5 submissions absent for F4, F5, F6 and F7.

Pipeline this week: **Multi-model CV → Best Classifier → GP + EI/UCB**
(same as W4 — pipeline stabilised)

Key development: Week log ground truth system identifies missing npy data.
This shapes the entire W6 strategy — without it, 4 functions would have
targeted the wrong coordinates in W6.

Key parameters:

| Parameter     | Controls                                | Range W5    |
|---------------|-----------------------------------------|-------------|
| EXPLOIT_RATIO | Fraction of candidates near best point  | 0.70 – 0.90 |
| EXPLOIT_SIGMA | Gaussian radius around best point       | 0.02 – 0.05 |
| UCB_KAPPA     | UCB exploration bonus                   | 2.0 – 3.0   |
| GP_RESTARTS   | Kernel hyperparameter restarts          | 5 – 10      |

---

## F1 — SPATIAL TARGETING (2D)
**n=14 | W4=1.658e-9 | CV winner: Linear SVM**
**Submitted: [0.532, 0.631] → W5 = -5.44e-7**

Still flat. SVM wins but CV near majority baseline — no useful signal.
W5 = -5.44e-7 ≈ 0. The function continues to return near-zero values
regardless of where submissions land. W6 strategy: broad EXPLORE.

**Key settings:** EXPLOIT_RATIO=0.60, UCB_KAPPA=3.0, broad exploration.

---

## F2 — MULTI-MODEL CV → GP (2D)
**n=14 | W4=0.019 | CV winner: Random Forest**
**Submitted: [0.710, 0.162] → W5 = 0.6497 ✅ NEW ALL-TIME BEST**

Breakthrough — W5 = 0.6497, the all-time best for F2. The submission moved
to a completely new region: X2=0.162 vs the previously assumed X2~0.93.
RF classifier correctly identified this new region as high-value.
This W5 result is the foundation for W6 strategy — EXPLOIT W5.

**Key settings:** EXPLOIT_RATIO=0.75, RF filter, new region discovered.

---

## F3 — MULTI-MODEL CV → GP (3D)
**n=17 | W4=-0.138 | CV winner: Decision Tree**
**Submitted: [0.150, 0.442, 0.335] → W5 = -0.059**

Partial recovery — W5 = -0.059 from W4 = -0.138. But far from W1 best
(-0.0136). X1=0.150 is distant from the confirmed W1 X1=0.966 boundary.
DT is not reliably pointing at the high-value region. W6 strategy:
forcibly return to W1 coordinates with best_point override.

**Key settings:** EXPLOIT_RATIO=0.75, DT filter, partial X1 recovery.

---

## F4 — MULTI-MODEL CV → GP (4D)
**n=22 | W4=-0.527 | CV winner: NN-Small**
**Submitted: [0.366, 0.526, 0.395, 0.305] → W5 = -2.457**

Sharp regression — W5 = -2.457 from W4 = -0.527. The NN-Small filters
candidates but the submission drifts significantly: X2=0.526 is much higher
than the W2 peak X2=0.415. Week log confirms W2 = +0.238 is missing from npy —
GP has never seen the true best. W6 strategy: override best_point to W2 coords.

**Key settings:** EXPLOIT_RATIO=0.85, NN filter, [0.4]^4 targeted.

---

## F5 — MULTI-MODEL CV → GP (4D)
**n=22 | W4=2913 | CV winner: Random Forest**
**Submitted: [0.453, 0.672, 0.304, 0.791] → W5 = 24.48**

Catastrophic regression — W5 = 24 from W4 = 2,913. The RF classifier failed
to keep X1 near 0.803. W5 coordinates are completely wrong: X1=0.453,
X2=0.672, X3=0.304, X4=0.791 — none of the four dimensions are in the
confirmed peak region. Week log confirms W3 = 4,891 at X1=0.803 is missing
from npy. W6 strategy: override to W3 coords with X1=0.803 explicit.

**Key settings:** EXPLOIT_RATIO=0.90, RF filter, all dims high targeted.

---

## F6 — MULTI-MODEL CV → GP (5D)
**n=22 | W4=-0.363 | CV winner: Logistic Regression**
**Submitted: [0.017, 0.022, 0.044, 0.800, 0.457] → W5 = -1.766**

Sharp regression — W5 = -1.766 from W4 = -0.363. X4=0.800 is high ✅
but X5=0.457 has moved away from the confirmed X5≈0.07 pattern.
X1, X2, X3 are all near zero — completely wrong. The LR classifier lost
the X5 signal entirely. Week log confirms W2 = -0.237 is missing from npy.
W6 strategy: override to W2 coords.

**Key settings:** EXPLOIT_RATIO=0.70, LR filter, X4/X5 pattern targeted.

---

## F7 — MULTI-MODEL CV → GP (6D)
**n=22 | W4=1.140 | CV winner: Linear SVM**
**Submitted: [0.273, 0.675, 0.454, 0.546, 0.235, 0.550] → W5 = 0.576**

Further regression — W5 = 0.576 from W4 = 1.140. X1=0.273 — far from
the confirmed X1≈0.016 boundary. The SVM is consistently allowing X1 to
drift upward away from the zero boundary. Week log confirms W2 = 1.739
is missing from npy. W6 strategy: override to W2 coords with X1=0.016.

**Key settings:** EXPLOIT_RATIO=0.80, SVM filter, X1 boundary targeted.

---

## F8 — MULTI-MODEL CV → GP (8D)
**n=22 | W4=9.334 | CV winner: Decision Tree**
**Submitted: [0.124, 0.707, 0.199, 0.790, 0.197, 0.733, 0.379, 0.886] → W5 = 8.956**

Slight regression — W5 = 8.956 from W4 = 9.334. Coordinates have drifted
significantly from W2/W3 peak pattern (X1≈0, X3≈0, X5≈0.93). The DT
classifier is not enforcing the boundary pattern strongly. W6 strategy:
return to W2 coords, tighter exploitation.

**Key settings:** EXPLOIT_RATIO=0.85, DT filter, boundary pattern targeted.

---

## Summary Table

| Fn | Dims | n  | CV Winner  | W4 Result | W5 Result  | Change      | W6 Action        |
|----|------|----|------------|-----------|------------|-------------|------------------|
| F1 | 2D   | 14 | Linear SVM | 1.66e-9   | -5.44e-7   | ≈ 0         | EXPLORE          |
| F2 | 2D   | 14 | Rand. Forest| 0.019    | 0.6497 ✅  | ↑ NEW BEST  | EXPLOIT W5       |
| F3 | 3D   | 17 | Dec. Tree  | -0.138    | -0.059     | ↑ Partial   | RECOVER W1       |
| F4 | 4D   | 22 | NN-Small   | -0.527    | -2.457     | ↓ CRASH     | RECOVER W2 ⚠️   |
| F5 | 4D   | 22 | Rand. Forest| 2913     | 24.48      | ↓ CRASH     | RECOVER W3 ⚠️   |
| F6 | 5D   | 22 | Logistic   | -0.363    | -1.766     | ↓ CRASH     | RECOVER W2 ⚠️   |
| F7 | 6D   | 22 | Linear SVM | 1.140     | 0.576      | ↓ Decline   | RECOVER W2 ⚠️   |
| F8 | 8D   | 22 | Dec. Tree  | 9.334     | 8.956      | ↓ Slight    | EXPLOIT tighter  |

⚠️ = best_point override required in W6 — true best missing from npy file.

**Critical W5 finding:** Week log cross-reference revealed that F4, F5, F6
and F7 all had their true best submissions missing from npy files. Without
this correction, W6 would have targeted the wrong coordinates for 4 functions.

Pipeline: 5 classifier families | 5-fold CV | GP + EI + UCB
Srinivas et al. (2010) GP-UCB | Jones (1998) EI | Rasmussen & Williams (2006) GP

---

*Week 5 | BBO Capstone | Mike Kennelly*
