# BBO Capstone — Week 3 Strategy Summary
**Mike Kennelly | All functions MAXIMISATION — higher is always better**

---

## Overview

Week 3 introduces the **SVM classifier pre-filter** — the most significant
pipeline change of the capstone. Rather than letting the GP search the
entire [0,1]^n space, a classifier is trained on binary labels (top 30% =
class 1) and used to screen 10,000 random candidates before the GP ranks them.

Pipeline this week: **SVM → GP + EI/UCB**

The SVM pre-filter concentrates the GP's attention on structurally promising
regions — reducing wasted evaluations in clearly bad areas of the search space.
Not all functions use the SVM this week: F7 uses pure GP (SVM CV too low),
and F6 uses a conditional strategy (SVM only if CV > threshold).

Key reference: Cybenko (1989), Goodfellow et al. (2016) — classifier theory.

---

## F1 — EXPLORE (2D)
**n=12 | W2=8.84e-7 | Strategy: EXPLORE + Model Testing**
**Submitted: [0.901, 0.877] → W3 = 5.17e-96**

All values near zero — SVM has no signal to learn. Model testing introduced
but CV scores are near the 70% majority baseline. W3 submission moves to
[0.901, 0.877] — new region not previously sampled. Result essentially zero.

**Key settings:** EXPLOIT_RATIO=0.60, broad UCB exploration.

---

## F2 — SVM → GP (2D)
**n=12 | W2=0.285 | Strategy: EXPLOIT with SVM filter**
**Submitted: [1.0, 1.0] → W3 = -0.030**

W2 regression (0.285 from W1=0.525) prompted a broader search. SVM trained
on 12 points. W3 submission pushed to [1.0, 1.0] — boundary region.
W3 = -0.030, a further regression. The X2=0.93 region turns out to be
misleading — true optimum at X2=0.16 not found until W5.

**Key settings:** SVM filter active, boundary push on both dims.

---

## F3 — SVM → GP, RECOVER W1 (3D)
**n=15 | W2=-0.033 | Strategy: RECOVER W1 best**
**Submitted: [0.446, 0.068, 0.479] → W3 = -0.083**

W1 best (-0.0136) not replicated in W2. Strategy: return to W1 coordinates
[0.966, 0.518, 0.403]. However W3 submission drifted significantly —
[0.446, 0.068, 0.479] is far from the W1 best. Further regression.
SVM with only 15 points in 3D has limited reliability.

**Key settings:** SVM filter, EXPLOIT_RATIO=0.75, focus on X1 boundary.

---

## F4 — SVM → GP (4D)
**n=20 | W2=+0.238 | Strategy: RECOVER W2 peak**
**Submitted: [0.434, 0.401, 0.305, 0.393] → W3 = -0.962**

W2 peak (+0.238) not replicated. Coordinates [0.439, 0.415, 0.385, 0.398]
were the W2 target but W3 drifts slightly — [0.434, 0.401, 0.305, 0.393].
X3=0.305 drops below the tight [0.38–0.44] cluster. Result -0.962.
The W2 best was missing from npy — GP had incomplete information.

**Key settings:** SVM filter, EXPLOIT_RATIO=0.85, tight around [0.4]^4.

---

## F5 — SVM → GP, BOUNDARY PUSH (4D)
**n=20 | W2=4062 | Strategy: EXPLOIT boundary — all dims high**
**Submitted: [0.803, 0.945, 0.998, 0.976] → W3 = 4890.6**

New all-time best — W3 = 4,891. GP correctly pushed all four dimensions
toward the upper boundary. X1=0.803 is higher than W2's X1=0.299,
showing the function wants X1 high as well as X2–X4. This is the
true all-time best for F5 — missing from npy file.

**Key settings:** SVM filter, EXPLOIT_RATIO=0.85, all dims → upper boundary.

---

## F6 — CONDITIONAL SVM → GP (5D)
**n=15 | W2=-0.237 | Strategy: RECOVER W2 best**
**Submitted: [0.211, 0.061, 0.455, 0.906, 0.004] → W3 = -0.883**

W2 best (-0.237) not replicated. SVM used conditionally — only if CV > threshold.
W3 submission drifts from W2 coordinates: X4=0.906 (high ✅) but X5=0.004
(near zero ✅) — structural pattern partially preserved. However X1, X2, X3
are far off. Result -0.883, significant regression.

**Key settings:** Conditional SVM, X4 high + X5 low pattern targeted.

---

## F7 — PURE GP, LOCAL FOCUS (6D)
**n=20 | W2=1.739 | Strategy: RECOVER W2/W3 peak region**
**Submitted: [0.0, 0.426, 0.306, 0.172, 0.358, 0.637] → W3 = 1.736**

Excellent result — W3 = 1.736 nearly matches W2 = 1.739. Pure GP used
(no SVM — CV too low in 6D with 20 points). X1=0.0 pushed to boundary,
X2–X6 all close to W2 coordinates. W2 and W3 together confirm this
region is the true peak for F7.

**Key settings:** Pure GP only, X1=0 boundary, local focus around W2.

---

## F8 — SVM → GP (8D)
**n=20 | W2=9.832 | Strategy: EXPLOIT W2 peak**
**Submitted: [0.012, 0.366, 0.002, 0.165, 0.448, 0.535, 0.153, 0.745] → W3 = 9.819**

Strong result — W3 = 9.819, just below W2 = 9.832. The X1≈0, X3≈0 boundary
pattern holds. X5 drops from 0.929 to 0.448 — slight drift from peak but
result remains very strong. SVM filter operational with 20 points in 8D.

**Key settings:** SVM filter, EXPLOIT_RATIO=0.85, boundary pattern maintained.

---

## Summary Table

| Fn | Dims | n  | W2 Result | W3 Result | Change     | Pipeline      | Key Development |
|----|------|----|-----------|-----------|------------|---------------|-----------------|
| F1 | 2D   | 12 | 8.84e-7   | 5.17e-96  | ≈ 0        | Model test    | Still flat |
| F2 | 2D   | 12 | 0.285     | -0.030    | ↓ Regress  | SVM → GP      | Boundary push backfires |
| F3 | 3D   | 15 | -0.033    | -0.083    | ↓ Regress  | SVM → GP      | Drifted from W1 best |
| F4 | 4D   | 20 | +0.238    | -0.962    | ↓ Regress  | SVM → GP      | W2 peak not replicated |
| F5 | 4D   | 20 | 4062      | 4891 ✅   | ↑ NEW BEST | SVM → GP      | All dims high confirmed |
| F6 | 5D   | 15 | -0.237    | -0.883    | ↓ Regress  | Cond. SVM     | X4/X5 pattern lost |
| F7 | 6D   | 20 | 1.739     | 1.736 ✅  | ≈ HOLD     | Pure GP       | W2/W3 peak confirmed |
| F8 | 8D   | 20 | 9.832     | 9.819     | ≈ HOLD     | SVM → GP      | Boundary pattern holds |

Pipeline: SVM classifier pre-filter introduced | Cybenko (1989), Goodfellow et al. (2016)
F5 and F7 strong — F3, F4, F6 regressing.

---

*Week 3 | BBO Capstone | Mike Kennelly*
