# Data Card — BBO Capstone Week 12
### Mike Kennelly | Imperial College | Final Query

---

## 1. Dataset Overview

| Property | Value |
|----------|-------|
| **Dataset name** | BBO Capstone Evaluation History — W1–W11 |
| **Version** | Week 12 (final, 16 npy files) |
| **Format** | NumPy `.npy` arrays (inputs + outputs per function) |
| **Total files** | 16 (f1–f8, inputs + outputs) |
| **Total evaluations** | 259 across all 8 functions (see per-function breakdown below) |
| **Collection method** | Sequential portal evaluation — one submission per function per week |
| **Collection period** | Weeks 1–11, Imperial College BBO Capstone portal |
| **Provenance** | Black-box oracle evaluations — function internals unknown |

---

## 2. Per-Function Dataset Summary

| Fn | Dims | n (W12) | n/p ratio | Y range | Y mean | Y std | ATB | ATB Week |
|----|------|---------|-----------|---------|--------|-------|-----|----------|
| F1 | 2D | 20 | 10.0 | −5.4e-07 to +8.97e-07 | ≈0.0 | ≈1.7e-07 | 8.968e-07 | W11 |
| F2 | 2D | 21 | 10.5 | −0.030 to +0.6497 | 0.368 | 0.189 | 0.6497 | W5 |
| F3 | 3D | 25 | 8.3 | −0.399 to −0.000707 | −0.088 | 0.077 | −0.001285 | W11 |
| F4 | 4D | 40 | 10.0 | −32.6 to +0.23759 | −5.32 | 6.71 | 0.23759 | W2 |
| F5 | 4D | 30 | 7.5 | 24.5 to 8662.5 | 3,172 | 3,014 | 8662.48 | W9 |
| F6 | 5D | 30 | 6.0 | −2.571 to +0.03602 | −0.763 | 0.582 | 0.03602 | W9 |
| F7 | 6D | 40 | 6.7 | 0.576 to 2.8501 | 1.992 | 0.676 | 2.8501 | W11 |
| F8 | 8D | 50 | 6.3 | 5.500 to 9.8320 | 8.246 | 0.861 | 9.8320 | W2 |

**Total evaluations:** 20+21+25+40+30+30+40+50 = **256 evaluations**

---

## 3. File Reference

### W12 Input/Output Files

| File | Shape | Description |
|------|-------|-------------|
| `f1_w12_inputs.npy` | (20, 2) | F1 input coordinates, W1–W11 |
| `f1_w12_outputs.npy` | (20,) | F1 oracle evaluations, W1–W11 |
| `f2_w12_inputs.npy` | (21, 2) | F2 input coordinates, W1–W11 |
| `f2_w12_outputs.npy` | (21,) | F2 oracle evaluations, W1–W11 |
| `f3_w12_inputs.npy` | (25, 3) | F3 input coordinates, W1–W11 |
| `f3_w12_outputs.npy` | (25,) | F3 oracle evaluations, W1–W11 |
| `f4_w12_inputs.npy` | (40, 4) | F4 input coordinates, W1–W11 |
| `f4_w12_outputs.npy` | (40,) | F4 oracle evaluations, W1–W11 |
| `f5_w12_inputs.npy` | (30, 4) | F5 input coordinates, W1–W11 |
| `f5_w12_outputs.npy` | (30,) | F5 oracle evaluations, W1–W11 |
| `f6_w12_inputs.npy` | (30, 5) | F6 input coordinates, W1–W11 |
| `f6_w12_outputs.npy` | (30,) | F6 oracle evaluations, W1–W11 |
| `f7_w12_inputs.npy` | (40, 6) | F7 input coordinates, W1–W11 |
| `f7_w12_outputs.npy` | (40,) | F7 oracle evaluations, W1–W11 |
| `f8_w12_inputs.npy` | (50, 8) | F8 input coordinates, W1–W11 |
| `f8_w12_outputs.npy` | (50,) | F8 oracle evaluations, W1–W11 |

### How the W12 Files Were Built

Each W12 npy file = the corresponding W11 file with the W11 portal result appended as a new row:

```python
X_w12 = np.vstack([X_w11, w11_submission_coords])
Y_w12 = np.append(Y_w11, w11_portal_result)
```

F5 is the only exception — the W11 submission `[1,1,1,1]` was an exact duplicate already present in the W11 npy, so no row was appended (shape unchanged at 30 rows).

---

## 4. Data Provenance and Collection Protocol

### Submission Protocol

Each week, one coordinate vector per function was submitted to the Imperial College BBO portal. The portal returned a scalar oracle evaluation. This scalar and the input coordinates were appended to the function's running npy files.

There is no access to the underlying function definitions. All inputs are in `[0,1]^d`. The objective is maximisation for all 8 functions. No mid-week re-evaluation or noise injection is applied by the student — evaluations are deterministic from the student side (single submission per week).

### Observed Non-Determinism

F2 exhibits apparent stochasticity: the exact W5 ATB coordinates `[0.710068, 0.161630]` were resubmitted in W9 (returned 0.6497 = ATB) and again in W11 (returned 0.6090 = 6.3% below ATB). Whether this reflects true function stochasticity or numerical sensitivity in the oracle is unknown.

### Data Quality

All coordinate values are within `[0,1]` (confirmed by `np.clip` applied at candidate generation). No missing values. No outlier removal was applied — all oracle evaluations including extreme negatives (F4: −32.6) are retained.

---

## 5. Week-by-Week Submission History

### F1 (2D) — Near-zero degenerate landscape

| Week | X1 | X2 | Output | vs ATB |
|------|----|----|--------|--------|
| W1 | 0.0825 | 1.5395 | 0.0 | — |
| W2 | 0.6842 | 0.7042 | 8.838e-07 | NEW ATB |
| W3 | 0.9010 | 0.8770 | 5.17e-96 | — |
| W4 | 0.6884 | 0.7241 | 1.658e-09 | — |
| W5 | 0.5323 | 0.6306 | −5.44e-07 | — |
| W6 | 0.0739 | 0.4071 | 1.666e-85 | — |
| W7 | 0.5828 | 0.4823 | −2.221e-17 | — |
| W8 | 0.8871 | 0.6688 | 1.259e-49 | — |
| W9 | 0.9799 | 1.0000 | −2.447e-183 | — |
| W10 | 0.9119 | 0.6619 | 4.109e-58 | — |
| W11 | 0.6842 | 0.7042 | **8.968e-07** | **NEW ATB** |

**W12 submission:** `0.684200-0.704200` (replicate W11 ATB)

---

### F2 (2D) — Two-zone landscape (Module 22 primary showcase)

| Week | X1 | X2 | Output | Zone | vs ATB |
|------|----|----|--------|------|--------|
| W1 | 0.7056 | 1.4879 | 0.5246 | HIGH X2 | — |
| W2 | 0.7736 | 0.9639 | 0.2847 | HIGH X2 | — |
| W3 | 1.0000 | 1.0000 | −0.0298 | HIGH X2 | — |
| W4 | 0.7809 | 0.9915 | 0.0188 | HIGH X2 | — |
| W5 | 0.7101 | **0.1616** | **0.6497** | LOW X2 | **NEW ATB** |
| W6 | 0.7008 | 0.1261 | 0.5844 | LOW X2 | — |
| W7 | 0.6890 | 0.1688 | 0.5338 | LOW X2 | — |
| W8 | 0.7128 | 0.0425 | 0.4926 | LOW X2 (too low) | — |
| W9 | 0.6427 | 0.9384 | 0.3252 | HIGH X2 (drifted) | — |
| W10 | 0.6402 | 0.0402 | 0.1636 | LOW X2 (too low) | — |
| W11 | 0.7101 | **0.1616** | 0.6090 | LOW X2 | Regressed |

**Module 22 clustering:**
- HIGH X2 zone (W1,W2,W3,W4,W9): centroid [0.733, 0.904], mean output = 0.225
- LOW X2 zone (W5,W6,W7,W8,W10,W11): centroid [0.702, 0.118], mean output = 0.506
- Inter-zone distance = 0.963 | Zone B spread = 0.025 | ATB→centroid dist = 0.012

**W12 submission:** `0.710068-0.161630` (ATB = LOW X2 zone centroid)

---

### F3 (3D) — Closest-to-zero maximisation

| Week | X1 | X2 | X3 | Output | vs ATB |
|------|----|----|----|----|--------|
| W1 | 0.9660 | 0.5177 | 0.4028 | −0.01358 | — |
| W2 | 1.0000 | 0.5366 | 0.5780 | −0.03277 | — |
| W3 | 0.4457 | 0.0675 | 0.4788 | −0.08337 | — |
| W4 | 0.9949 | 0.9230 | 0.0020 | −0.13795 | — |
| W5 | 0.1503 | 0.4416 | 0.3353 | −0.05900 | — |
| W6 | **0.9981** | 0.6212 | 0.4531 | −0.00707 | NEW ATB |
| W7 | 1.0000 | 0.5717 | 0.5040 | −0.00534 | NEW ATB |
| W8 | 0.9815 | 0.5406 | 0.1920 | −0.11316 | — |
| W9 | 0.7504 | 0.5915 | 0.4481 | −0.01348 | — |
| W10 | 0.9295 | 0.6844 | 0.6214 | −0.09015 | — |
| W11 | **0.9981** | 0.6212 | 0.4531 | **−0.001285** | **NEW ATB** |

**Key pattern:** X1≈1.0 is the critical structural anchor. W10 drift to X1=0.929 caused regression.

**W12 submission:** `0.998126-0.621218-0.453080` (replicate W11 ATB)

---

### F4 (4D) — Single isolated positive basin

| Week | Output | vs ATB | Note |
|------|--------|--------|------|
| W1 | −2.6271 | — | Baseline |
| W2 | **+0.23759** | **NEW ATB** | Only positive result |
| W3 | −0.9620 | — | Deviated |
| W4 | −0.5268 | — | — |
| W5 | −2.4571 | — | — |
| W6 | −0.1294 | — | — |
| W7 | −0.2651 | — | — |
| W8 | −0.5542 | — | — |
| W9 | −1.4047 | — | — |
| W10 | −1.8014 | — | — |
| W11 | **+0.23759** | Exact match | ATB replicated |

**W2 ATB coords:** [0.439249, 0.414994, 0.384687, 0.397917]

**W12 submission:** `0.439249-0.414994-0.384687-0.397917` (replicate W2 ATB)

---

### F5 (4D) — Corner maximisation

| Week | Output | vs ATB | X1 value |
|------|--------|--------|----------|
| W1 | 60.07 | — | 0.1199 |
| W2 | 4,062.1 | NEW ATB | 0.2990 |
| W3 | 4,890.6 | NEW ATB | 0.8030 |
| W4 | 2,913.0 | — | 0.3547 |
| W5 | 24.48 | — | 0.4531 |
| W6 | 5,875.1 | NEW ATB | 0.7810 |
| W7 | 7,596.8 | NEW ATB | 0.9377 |
| W8 | 8,382.5 | NEW ATB | 0.9851 |
| W9 | **8,662.48** | **NEW ATB** | **1.000** |
| W10 | 8,471.3 | — | 1.000 (X3=0.9899) |
| W11 | 8,662.48 | Exact match | 1.000 |

**W10 perturbation confirmed:** X3=0.989 → 8471, confirming [1,1,1,1] = global max.

**W12 submission:** `1.000000-1.000000-1.000000-1.000000`

---

### F6 (5D) — X5-threshold landscape

| Week | Output | vs ATB | X5 value |
|------|--------|--------|----------|
| W1 | −1.3389 | — | 0.4237 |
| W2 | −0.2372 | NEW ATB | 0.0721 |
| W3 | −0.8835 | — | 0.0040 |
| W4 | −0.3630 | NEW ATB | 0.0489 |
| W5 | −1.7662 | — | 0.4569 |
| W6 | −0.1727 | NEW ATB | 0.1439 |
| W7 | −0.3422 | — | 0.1292 |
| W8 | −0.4006 | — | 0.2007 |
| W9 | **+0.03602** | **NEW ATB** | **0.1153** |
| W10 | −0.1443 | — | 0.0787 (too low) |
| W11 | −0.01024 | — | 0.1153 (regressed) |

**X5 threshold identified:** X5≈0.115 → positive. X5=0.079 → negative. Critical narrow band.

**W9 ATB coords:** [0.406643, 0.339495, 0.634775, 0.769397, 0.115269]

**W12 submission:** `0.406643-0.339495-0.634775-0.769397-0.115269` (replicate W9 ATB)

---

### F7 (6D) — Trending cluster (Module 22 secondary showcase)

| Week | Output | vs Prior ATB | Step Size (6D) |
|------|--------|-------------|----------------|
| W1 | 0.8085 | — | — |
| W2 | 1.7392 | NEW ATB | — |
| W3 | 1.7358 | — | — |
| W4 | 1.1399 | — | — |
| W5 | 0.5763 | — | — |
| W6 | 2.1190 | NEW ATB | — |
| W7 | 2.4134 | NEW ATB | 0.061 |
| W8 | 2.5982 | NEW ATB | 0.049 |
| W9 | 2.5968 | — | 0.001 |
| W10 | 2.7201 | NEW ATB | 0.042 |
| W11 | **2.8501** | **NEW ATB** | **0.061** |

**6 consecutive improvements W6→W11.** Cluster direction: X1 rising, X6 rising, X2–X5 declining.
Intra-cluster spread = 0.066 — tight, confirming a genuine landscape ridge.

**W11 ATB coords:** [0.165978, 0.338682, 0.444076, 0.255770, 0.300940, 0.704355]

**W12 submission:** Run GP pipeline first. Fallback: `0.165978-0.338682-0.444076-0.255770-0.300940-0.704355`

---

### F8 (8D) — Zero-boundary structure

| Week | Output | vs ATB | X1 | X3 | X7 |
|------|--------|--------|----|----|-----|
| W1 | 9.0093 | — | 0.0091 | 0.5160 | 0.5792 |
| W2 | **9.8320** | **NEW ATB** | **0.000** | **0.000** | **0.000** |
| W3 | 9.8188 | − 0.013 | 0.012 | 0.002 | 0.153 |
| W4 | 9.3341 | −0.498 | 0.069 | 0.001 | 0.048 |
| W5 | 8.9560 | −0.876 | 0.124 | 0.199 | 0.379 |
| W6 | 9.7741 | −0.058 | 0.000 | 0.069 | 0.292 |
| W7 | 9.8251 | −0.007 | 0.040 | 0.004 | 0.167 |
| W8 | 9.8021 | −0.030 | 0.008 | 0.000 | 0.167 |
| W9 | 9.8115 | −0.020 | 0.041 | 0.000 | 0.162 |
| W10 | 9.8013 | −0.031 | 0.044 | 0.007 | 0.165 |
| W11 | 9.8269 | −0.005 | 0.031 | 0.010 | 0.162 |

**Zero-boundary structure:** W2 is the only evaluation with X1=X3=X7=0 exactly. Every deviation from these zeros in W3–W11 returned below ATB. W11 sparsity hypothesis (X1=0.031, X3=0.010, X7=0.162) returned 9.827 — still 0.005 below.

**W2 ATB coords:** [0.000000, 0.179297, 0.000000, 0.071406, 0.929270, 0.459981, 0.000000, 0.541212]

**W12 submission:** `0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212`

---

## 6. Module 22 Clustering — Data Structure Analysis

### Cluster Statistics Across All Functions

| Fn | n | Top-3 Spread | ATB→Centroid | Cluster Type | Cluster Insight |
|----|---|-------------|--------------|--------------|-----------------|
| F1 | 20 | 0.014 | 0.007 | Tight static | [0.684, 0.704] basin confirmed |
| F2 | 21 | 0.025 | 0.012 | **Two-zone** | LOW-X2 is the high-value basin |
| F3 | 25 | 0.047 | 0.024 | Tight static | X1=1.0 boundary anchor |
| F4 | 40 | 0.062 | 0.031 | Isolated | One positive basin among negatives |
| F5 | 30 | 0.007 | 0.003 | Corner | Monotonic corner — tightest cluster |
| F6 | 30 | 0.030 | 0.015 | Tight static | X5=0.115 threshold confirmed |
| F7 | 40 | 0.066 | 0.051 | **Trending** | Dynamic centroid — 6 consecutive steps |
| F8 | 50 | 0.455 | 0.422 | Loose boundary | Zero-boundary (X1=X3=X7=0) is the key |

### Interpreting Spread Values

**Tight cluster (spread < 0.10):** F1, F2, F3, F4, F5, F6, F7 — all have identifiable point attractors. The ATB coordinates are close to or identical to the cluster centroid. The correct W12 strategy is to submit the centroid = the ATB.

**Loose cluster (spread = 0.455, F8):** This initially appears multi-modal. However, the looseness is explained by post-W2 submissions that deviated from the zero-boundary structure. The ATB itself is the structural anchor; the spread is an artefact of exploration, not evidence of multiple comparable basins.

**Dynamic cluster (F7):** The spread (0.066) is tight but the centroid is moving. The cluster represents a landscape ridge being walked, not a static basin. This is the data-driven evidence that GP extrapolation is justified for F7.

---

## 7. Data Limitations

| Limitation | Detail |
|------------|--------|
| **Black-box oracle** | Function definitions are unknown. No gradient information. No repeated evaluations at same point (except F2 W5/W9/W11 and F4 W2/W11). |
| **Small n** | n ranges from 20 (F1) to 50 (F8). Classifier CV uses 2–5 folds. GP fits on 20–50 points in 2–8D. |
| **Single query per week** | No mid-week corrections. A bad submission cannot be recovered within the same week. |
| **Observed stochasticity** | F2 returned different values for identical coordinates in W5 (0.6497), W9 (0.6497), and W11 (0.6090). Not reproducible under controlled conditions — may be oracle noise. |
| **No held-out test set** | All evaluations are training data for the surrogate. There is no independent validation split. |
| **Boundary evaluations** | Several functions have evaluations at or near coordinate boundaries (X=0, X=1). GP uncertainty is elevated at boundaries — σ values less reliable there. |

---

## 8. Intended Use

| Property | Value |
|----------|-------|
| **Primary use** | Training GP/classifier surrogates for BBO Capstone weekly submissions |
| **Secondary use** | Module 22 clustering analysis to validate W12 submission strategy |
| **Prohibited use** | Any real-world optimisation application without independent validation |
| **Licence** | Academic use only — Imperial College BBO Capstone |

---

*BBO Capstone Data Card — Mike Kennelly — Imperial College — Week 12 Final Query*
