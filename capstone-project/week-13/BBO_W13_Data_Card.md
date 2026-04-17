# Data Card — BBO Capstone Week 13
### Mike Kennelly | Imperial College | FINAL Query (Week 13 of 13)

---

## 1. Dataset Overview

| Property | Value |
|----------|-------|
| **Dataset name** | BBO Capstone Evaluation History — W1–W12 |
| **Version** | Week 13 (final, 16 npy files) |
| **Format** | NumPy `.npy` arrays (inputs + outputs per function) |
| **Total files** | 16 (f1–f8, inputs + outputs) |
| **Total evaluations** | 263 across all 8 functions (see per-function breakdown below) |
| **Collection method** | Sequential portal evaluation — one submission per function per week |
| **Collection period** | Weeks 1–12, Imperial College BBO Capstone portal |
| **Provenance** | Black-box oracle evaluations — function internals unknown |

---

## 2. Per-Function Dataset Summary

| Fn | Dims | n (W13) | n/p ratio | Y range | Y mean | Y std | ATB | ATB Week |
|----|------|---------|-----------|---------|--------|-------|-----|----------|
| F1 | 2D | 21 | 10.5 | −5.4e-07 to +8.97e-07 | ≈0.0 | ≈1.7e-07 | 8.968e-07 | W11 (= W12 exact match) |
| F2 | 2D | 22 | 11.0 | −0.030 to **+0.6880** | 0.385 | 0.190 | **0.6880** | **W12 ★ NEW ATB** |
| F3 | 3D | 26 | 8.7 | −0.399 to −0.000707 | −0.091 | 0.078 | −0.001285 | W11 |
| F4 | 4D | 41 | 10.3 | −32.6 to +0.23759 | −5.17 | 6.65 | 0.23759 | W2 (triple-confirmed) |
| F5 | 4D | **30*** | 7.5 | 24.5 to 8662.5 | 3,172 | 3,014 | 8662.48 | W9 (triple-confirmed) |
| F6 | 5D | 31 | 6.2 | −2.571 to +0.03602 | −0.785 | 0.587 | 0.03602 | W9 |
| F7 | 6D | 41 | 6.8 | 0.576 to **2.8939** | 2.014 | 0.667 | **2.8939** | **W12 ★ NEW ATB (7th consecutive)** |
| F8 | 8D | 51 | 6.4 | 5.500 to 9.83196 | 8.277 | 0.842 | 9.83196 | W2 (W12 exact match, 10-wk gap) |

**Total evaluations W13:** 21+22+26+41+30+31+41+51 = **263 evaluations**

**\*F5 W13 npy exception:** n stays at 30, not 31. W12 submission `[1,1,1,1]` → 8662.48 was an exact row-level duplicate of the W9 row already in the W12 npy. Per the W11→W12 precedent (skip-append rule), no row is appended when the submission exactly matches an existing row. F5 W13 npy retains the W12 shape.

---

## 3. File Reference

### W13 Input/Output Files

| File | Shape | Description |
|------|-------|-------------|
| `f1_w13_inputs.npy` | (21, 2) | F1 input coordinates, W1–W12 |
| `f1_w13_outputs.npy` | (21,) | F1 oracle evaluations, W1–W12 |
| `f2_w13_inputs.npy` | (22, 2) | F2 input coordinates, W1–W12 |
| `f2_w13_outputs.npy` | (22,) | F2 oracle evaluations, W1–W12 |
| `f3_w13_inputs.npy` | (26, 3) | F3 input coordinates, W1–W12 |
| `f3_w13_outputs.npy` | (26,) | F3 oracle evaluations, W1–W12 |
| `f4_w13_inputs.npy` | (41, 4) | F4 input coordinates, W1–W12 |
| `f4_w13_outputs.npy` | (41,) | F4 oracle evaluations, W1–W12 |
| `f5_w13_inputs.npy` | (30, 4) | F5 input coordinates — **unchanged from W12 (skip-append)** |
| `f5_w13_outputs.npy` | (30,) | F5 oracle evaluations — unchanged from W12 |
| `f6_w13_inputs.npy` | (31, 5) | F6 input coordinates, W1–W12 |
| `f6_w13_outputs.npy` | (31,) | F6 oracle evaluations, W1–W12 |
| `f7_w13_inputs.npy` | (41, 6) | F7 input coordinates, W1–W12 |
| `f7_w13_outputs.npy` | (41,) | F7 oracle evaluations, W1–W12 |
| `f8_w13_inputs.npy` | (51, 8) | F8 input coordinates, W1–W12 |
| `f8_w13_outputs.npy` | (51,) | F8 oracle evaluations, W1–W12 |

### How the W13 Files Were Built

Each W13 npy file = the corresponding W12 file with the W12 portal result appended as a new row:

```python
X_w13 = np.vstack([X_w12, w12_submission_coords])
Y_w13 = np.append(Y_w12, w12_portal_result)
```

**F5 exception:** the W12 submission `[1,1,1,1]` → 8662.48 was an exact duplicate of the W9 row already in the W12 npy (both at [1,1,1,1], both returning 8662.48). Per the skip-append rule established W11→W12, no row is appended in this case. F5 W13 npy shape is unchanged at (30, 4).

---

## 4. ★ Oracle Stochasticity — Quantified at W12

The W12 portal results produced the first unambiguous evidence of oracle stochasticity on 3 of 8 functions. Identical coordinate replays returned different scalar values; the other 5 functions remained deterministic across 2+ exact replays. **This is a key W13 data-level finding that shapes the submission strategy.**

| Fn | Empirical σ | Replay evidence | Status | W13 consequence |
|----|-------------|-----------------|--------|-----------------|
| F1 | — | W11 → W12: 8.968e-07 (1 exact replay) | Deterministic | ATB replay guarantees ATB |
| F2 | ~0.035 | W5: 0.6497 · W9: 0.6497 · W11: 0.6090 · W12: **0.6880** | Stochastic with upside | Replay captures expected value in best basin |
| F3 | ~0.003 | W11: −0.00128 · W12: −0.00713 | Stochastic | W11 ATB still best-known; noise within GP alpha tolerance |
| F4 | — | W2: 0.23759 · W11: 0.23759 · W12: 0.23759 (triple) | Deterministic | Safest override |
| F5 | — | W9: 8662.48 · W11: 8662.48 · W12: 8662.48 (triple) | Deterministic corner | Safest override |
| F6 | **~0.063** | W9: +0.0360 · W11: −0.0102 · W12: −0.0883 | **Stochastic (HIGHEST)** | Range 0.124 at identical coords; GP alpha raised to 1e-4 |
| F7 | — | No exact replays (trending cluster, coords shift each week) | Unknown | GP pipeline with fallback |
| F8 | — | W2: 9.8320 · W12: 9.83196 (exact match across 10-week gap) | Deterministic | Double-confirmed |

### Why this matters for W13 strategy

Noise is in the **oracle**, not the **input**. On stochastic oracles (F2, F3, F6), identical coordinates can return different scalar values each time. This has three consequences:

1. **Best-known input still dominates by expected value** — GP-predicted gains on noisy oracles are confounded with noise; replaying best-known is the risk-minimising choice.
2. **GP α must be raised on the noisiest function** — F6 W13 uses `alpha = 1e-4` (vs 1e-6 elsewhere) to model oracle noise properly within the GP fit.
3. **Deterministic confirmations gain evidential weight** — F1, F4, F5, F8 have each had at least one exact-coord replay return the exact same output. On these, override is not just the risk-minimising choice — it's the **guaranteed-result** choice.

---

## 5. Week-by-Week Submission History (W1–W12)

### F1 (2D) — Near-zero degenerate landscape

| Week | X1 | X2 | Output | vs ATB |
|------|----|----|--------|--------|
| W1 | 0.0825 | 1.5395 | 0.0 | — |
| W2 | 0.6842 | 0.7042 | 8.838e-07 | NEW ATB |
| W3–W10 | … | … | … | All below ATB |
| W11 | 0.6842 | 0.7042 | **8.968e-07** | **NEW ATB** |
| W12 | 0.6842 | 0.7042 | **8.968e-07** | **= ATB exact (deterministic)** |

**W13 submission:** `0.684200-0.704200` (replicate W11/W12 ATB)

---

### F2 (2D) — Two-zone landscape (Module 22 primary + Module 23 kernel-PCA case)

| Week | X1 | X2 | Output | Zone | vs ATB |
|------|----|----|--------|------|--------|
| W1–W4 | … | … | … | HIGH X2 | — |
| W5 | 0.7101 | **0.1616** | 0.6497 | LOW X2 | NEW ATB (at W5) |
| W6–W8 | … | … | … | LOW X2 | — |
| W9 | 0.6427 | 0.9384 | 0.3252 | HIGH X2 (drifted) | — |
| W10 | 0.6402 | 0.0402 | 0.1636 | LOW X2 (too low) | — |
| W11 | 0.7101 | **0.1616** | 0.6090 | LOW X2 | Regressed (noise) |
| W12 | 0.7101 | **0.1616** | **0.6880** | LOW X2 | **NEW ATB ★ (+0.038)** |

**Module 22 clustering (updated W13):**
- HIGH X2 zone (W1,W2,W3,W4,W9): centroid [0.733, 0.904], mean output = 0.225
- **LOW X2 zone (W5,W6,W7,W8,W10,W11,W12): centroid [0.704, 0.119], mean output = 0.534** (W12 raises mean)
- Inter-zone distance = 0.963 | Zone B intra-spread = 0.028 (slightly widened by W12 but still tight)

**Module 23 PCA lens:** Kernel-PCA case — linear PCA on the full 22 points is degenerate because PC1 runs through both basins. Kernel PCA (RBF, γ=5.0) recovers zone separation (KPC1 separation 0.58). Within the LOW-X2 basin, linear PCA shows 2D active structure.

**F2 stochasticity:** W5, W9, W11, W12 at identical coords returned 0.6497, 0.6497, 0.6090, **0.6880** respectively — σ~0.035, with visible upside in W12. Replay captures this upside in expected value.

**W13 submission:** `0.710068-0.161630` (replicate W12 NEW ATB)

---

### F3 (3D) — Closest-to-zero maximisation (Module 23 scree / 1 flat PC case)

| Week | X1 | X2 | X3 | Output | vs ATB |
|------|----|----|----|----|--------|
| W1–W5 | … | … | … | … | Below ATB |
| W6 | **0.9981** | 0.6212 | 0.4531 | −0.00707 | NEW ATB |
| W7 | 1.0000 | 0.5717 | 0.5040 | −0.00534 | NEW ATB |
| W8–W10 | … | … | … | … | Below ATB |
| W11 | **0.9981** | 0.6212 | 0.4531 | **−0.001285** | **NEW ATB** |
| W12 | **0.9981** | 0.6212 | 0.4531 | −0.00713 | Regressed (noise σ~0.003) |

**Module 23 PCA lens:** Scree / 1 flat PC case. X1 locked at 0.998 (near the 1.0 boundary) — variance in X1 is near zero in the top subset, yielding 1 flat PC. Effective dim = 2. X1 is the **removable PC** — a boundary anchor that the W12 regression did not perturb.

**W13 submission:** `0.998126-0.621218-0.453080` (replicate W11 ATB — W12 regression is oracle noise, not a coord problem)

---

### F4 (4D) — Single isolated positive basin (Module 23 isolated case)

| Week | Output | vs ATB | Note |
|------|--------|--------|------|
| W1 | −2.6271 | — | Baseline |
| W2 | **+0.23759** | **NEW ATB** | Only positive result |
| W3–W10 | … | — | All negative |
| W11 | **+0.23759** | Exact match | ATB replicated |
| W12 | **+0.23759** | Exact match | **Triple-confirmed deterministic** |

**Module 23 PCA lens:** Isolated basin, all 4 dims narrow-active. No flat PC. PC1 share ≈ 0.57 — moderate. The basin is a structural singleton in the landscape.

**W2/W11/W12 ATB coords:** [0.439249, 0.414994, 0.384687, 0.397917]

**W13 submission:** `0.439249-0.414994-0.384687-0.397917` (triple-confirmed deterministic basin)

---

### F5 (4D) — Corner maximisation (Module 23 flat-scree secondary showcase)

| Week | Output | vs ATB | X1 value |
|------|--------|--------|----------|
| W1 | 60.07 | — | 0.1199 |
| W2–W8 | … | NEW ATB (multiple) | Climbing |
| W9 | **8,662.48** | **NEW ATB** | **1.000 (first corner hit)** |
| W10 | 8,471.3 | — | 1.000 (X3=0.989 perturbation) |
| W11 | **8,662.48** | Exact match | 1.000 |
| W12 | **8,662.48** | Exact match | 1.000 (**triple-confirmed, skip-append**) |

**Module 23 PCA lens:** Flat-scree / corner case — the capstone's cleanest demonstration of "everything collapses to a point". In the confirmed-corner subset (all dims ≥ 0.95, n=3):
- Total variance = **0.000108**
- All 4 dims below lock threshold — all 4 PCs effectively flat
- Effective dimensionality in the good cluster ≈ 0

**W10 perturbation evidence:** X3=0.989 → 8471 (drop of 191), confirming [1,1,1,1] is the exact global maximum.

**W13 submission:** `1.000000-1.000000-1.000000-1.000000` (triple-confirmed corner; npy unchanged per skip-append)

---

### F6 (5D) — X5-threshold landscape (Module 23 threshold / dominant-PC case, HIGHEST noise)

| Week | Output | vs ATB | X5 value |
|------|--------|--------|----------|
| W1–W8 | All negative | — | Various |
| W9 | **+0.03602** | **NEW ATB** | **0.1153** |
| W10 | −0.1443 | — | 0.0787 (too low) |
| W11 | −0.01024 | — | 0.1153 (regressed at same coords) |
| W12 | **−0.08826** | — | 0.1153 (regressed again, deepest) |

**F6 oracle noise evidence (HIGHEST in capstone):** W9 +0.036, W11 −0.010, W12 −0.088 at **identical coordinates** — empirical σ = 0.0628, range = 0.124. Noise is in the oracle, not the input.

**Module 23 PCA lens:** Threshold / dominant-PC case. PC1 loadings on the top subset: X5 = +0.611 (largest magnitude), confirming the strategy-doc prediction that X5 is the dominant direction. But X5 is **not removable** (variance 0.0085 above lock threshold) — it is the dominant *active* PC. Contrasts cleanly with F3's X1 (removable boundary anchor) and F5's locked-everywhere corner.

**W9 ATB coords:** [0.406643, 0.339495, 0.634775, 0.769397, 0.115269]

**W13 submission:** `0.406643-0.339495-0.634775-0.769397-0.115269` (replicate W9 ATB — W11/W12 regressions are oracle noise)

---

### F7 (6D) — Trending cluster (Module 22 secondary + Module 23 1-dominant-PC)

| Week | Output | vs Prior ATB | Step Size (6D) |
|------|--------|-------------|----------------|
| W1–W5 | … | — | — |
| W6 | 2.1190 | NEW ATB (ridge entry) | — |
| W7 | 2.4134 | NEW ATB | 0.294 (y-delta) |
| W8 | 2.5982 | NEW ATB | 0.185 |
| W9 | 2.5968 | — (≈flat) | −0.001 |
| W10 | 2.7201 | NEW ATB | 0.123 |
| W11 | 2.8501 | NEW ATB | 0.130 |
| W12 | **2.8939** | **NEW ATB** | **0.044 (smallest positive step)** |

**7 consecutive improvements W6→W12.** Step sizes decelerating — **the W11→W12 step (0.044) is the smallest positive step in the streak, suggesting ridge saturation.**

**Module 23 PCA lens — TERTIARY showcase:** Ridge-only PCA on top-7 points (W6–W12) shows:
- PC1 share = **0.900** — single dominant direction
- |corr(PC1 projection, y)| = **0.976** — nearly monotonic 1D climb
- PC1 loadings: X1=+0.611, X3=+0.523, X2=−0.429, X5=−0.373, X4≈0, X6=+0.171 — X1 dominates, matching strategy-doc prediction

**W12 ATB coords:** [0.179941, 0.306897, 0.455194, 0.249116, 0.295985, 0.730083]

**W13 submission:** Run GP pipeline. Evaluate 3 trust conditions at Step 14. **Fallback:** `0.179941-0.306897-0.455194-0.249116-0.295985-0.730083` (W12 NEW ATB).

---

### F8 (8D) — Zero-boundary structure (Module 23 PRIMARY PCA showcase)

| Week | Output | vs ATB | X1 | X3 | X7 |
|------|--------|--------|----|----|-----|
| W1 | 9.0093 | — | 0.0091 | 0.5160 | 0.5792 |
| W2 | **9.8320** | **NEW ATB** | **0.000** | **0.000** | **0.000** |
| W3 | 9.8188 | −0.013 | 0.012 | 0.002 | 0.153 |
| W4–W10 | … | Below ATB | All drifting from zeros |
| W11 | 9.8269 | −0.005 | 0.031 | 0.010 | 0.162 |
| W12 | **9.83196** | **= ATB exact** | **0.000** | **0.000** | **0.000** |

**W2 + W12 double-confirmed across 10-week gap at identical coords with identical output (9.8320 vs 9.83196, match to 4 d.p.) — deterministic oracle on the zero-boundary.**

**Module 23 PCA lens — PRIMARY showcase:** Near-ATB subset (top-5 rows by output, all y > 9.81) shows:
- **X1 variance = 0.00033, mean = 0.025** → ZERO-LOCKED
- **X3 variance = 0.000018, mean = 0.003** → ZERO-LOCKED (tightest dim in capstone)
- **X7 variance = 0.0052, mean = 0.129** → ZERO-LOCKED
- Scree: `[0.928, 0.041, 0.029, 0.003, 0.000, 0.000, 0.000, 0.000]` — **PCs 6, 7, 8 are literally 0.000**

**Effective dimensionality reduction: 8 → 5.** Three flat PCs (X1, X3, X7) can be removed without information loss within the good cluster. The **F8 ANISO_SIGMA** operationalises this: X1, X3, X7 get σ=0.006; the 5 active dims get σ=0.015.

**W2/W12 ATB coords:** [0.000000, 0.179297, 0.000000, 0.071406, 0.929270, 0.459981, 0.000000, 0.541212]

**W13 submission:** `0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212` (**three exact zeros preserved** — do not round X1, X3, X7)

---

## 6. Module 22 + Module 23 — Combined Data Structure Analysis

### Module 22 Cluster Statistics (carried forward + W12 update)

| Fn | n | Top-3 Spread | ATB→Centroid | Cluster Type | W13 Decision |
|----|---|-------------|--------------|--------------|--------------|
| F1 | 21 | 0.014 | 0.007 | Tight static | Replicate W11/W12 ATB |
| F2 | 22 | 0.028 | 0.012 | **Two-zone** (LOW-X2 wider by W12) | Replicate W12 NEW ATB |
| F3 | 26 | 0.047 | 0.024 | Tight static | Replicate W11 ATB |
| F4 | 41 | 0.062 | 0.031 | Isolated | Replicate W2 ATB (triple-confirmed) |
| F5 | 30 | 0.007 | 0.003 | Corner (tightest) | Replicate [1,1,1,1] (triple-confirmed) |
| F6 | 31 | 0.030 | 0.015 | Tight static + X5 threshold | Replicate W9 ATB (noise-agnostic) |
| F7 | 41 | 0.066 | 0.051 | **Trending (7-point)** | GP pipeline + fallback |
| F8 | 51 | 0.455 | 0.422 | Loose zero-boundary | Replicate W2/W12 ATB (10-wk gap) |

### Module 23 PCA Classification (NEW at W13)

| Fn | PCA case | Flat PCs | Effective dim | PC1 share (top/ridge subset) | Notes |
|----|----------|----------|---------------|------------------------------|-------|
| F1 | Tight attractor | — | — | — | No PC reduction |
| F2 | Kernel-PCA (linear degenerate) | 0 linear, 1 kernel | 2 | — | KPC1 sep = 0.58 |
| F3 | Scree / 1 flat PC | 1 (X1 locked) | 2 | high | X1 boundary anchor |
| F4 | Isolated (all narrow-active) | 0 | 4 | 0.57 | No reduction |
| F5 | Flat-scree / corner | ≈4 (all flat in confirmed corner) | ≈0 | — | Total var ≈ 0.0001 |
| F6 | Threshold / dominant-PC | 0 | 5 | 0.46 top-subset | X5 PC1 loading +0.611 |
| F7 | Trending ridge / 1-dominant-PC | 0 | 1 | **0.900 (ridge)** | \|corr(PC1,y)\|=0.976 |
| **F8** | **Zero-boundary / 3 flat PCs** | **3 (X1, X3, X7)** | **5** | **0.928 (near-ATB)** | **PRIMARY showcase** |

### Interpreting Spread + PCA Together

**Tight + no PC reduction (F1, F4):** Point attractor, all dims carry signal. Override.

**Tight + 1 flat PC (F3):** Point attractor with one boundary anchor. Override; GP wouldn't exit the anchored dim anyway.

**Corner + all flat PCs (F5):** Point attractor where all dims are boundary-anchored simultaneously. Override; the entire coordinate system is redundant inside the good cluster.

**Threshold + dominant-PC (F6):** Point attractor with one direction (X5) carrying most sensitivity. Override; perturbation along X5 creates the noise regime we're already seeing.

**Zero-boundary + 3 flat PCs (F8):** Structural attractor where 3 dims must equal 0. Override; the PCA lens formalises why X1=X3=X7=0 is not an arbitrary coincidence.

**Trending + 1-dominant-PC (F7):** Dynamic cluster with 1 true degree of freedom. GP pipeline — this is the only geometry where surrogate extrapolation is theoretically justified.

---

## 7. Data Limitations

| Limitation | Detail |
|------------|--------|
| **Black-box oracle** | Function definitions are unknown. No gradient information. Repeated evaluations at the same point are limited: F4 W2/W11/W12 triple, F5 W9/W11/W12 triple, F6 W9/W11/W12 triple (with noise), F8 W2/W12 double across 10-week gap. |
| **Small n** | n ranges from 21 (F1) to 51 (F8). Classifier CV uses 2–5 folds. GP fits on 21–51 points in 2–8D. |
| **Single query per week** | No mid-week corrections. A bad submission cannot be recovered within the same week. |
| **Quantified oracle stochasticity** | F2 σ~0.035, F3 σ~0.003, F6 σ~0.063 (HIGHEST). **These are now measured from replay data, not assumed.** F1, F4, F5, F8 are deterministic across all replays performed. F7 has no exact replays (trending). |
| **No held-out test set** | All evaluations are training data for the surrogate. There is no independent validation split. |
| **Boundary evaluations** | Several functions have evaluations at or near coordinate boundaries (X=0 for F8; X=1 for F3, F5). GP uncertainty is elevated at boundaries — σ values less reliable there. |
| **F5 skip-append** | F5 W13 npy is 30 rows (unchanged from W12) because W12 submission was an exact row-level duplicate of the W9 entry. The triple-confirmation (W9+W11+W12) is preserved in submission history, not npy structure. |

---

## 8. What Changed from W12 to W13 (Data-Level)

| Change | Description |
|--------|-------------|
| New ATBs | F2: 0.6497 → **0.6880** (W12). F7: 2.8501 → **2.8939** (W12, 7th consecutive). |
| Deterministic confirmations | F1 (1 exact replay), F4 (triple), F5 (triple), F8 (10-wk gap double) all now confirmed noise-free. |
| Stochastic quantification | F2 σ~0.035, F3 σ~0.003, F6 σ~0.063 — first time these noise levels are **measured** from portal data rather than assumed. |
| F5 shape unchanged | W12 submission was exact duplicate of W9 row — skip-append rule applied. |
| All other npys +1 row | W12 portal result appended to W12 npy to create W13 npy. |

---

## 9. Intended Use

| Property | Value |
|----------|-------|
| **Primary use** | Training GP/classifier surrogates for BBO Capstone W13 FINAL submissions |
| **Secondary use** | Module 22 clustering + Module 23 PCA analysis to validate W13 submission strategy |
| **Tertiary use** | Characterising oracle stochasticity via replay data (F2/F3/F6/F8 all have 2+ coord replays documenting noise behaviour) |
| **Prohibited use** | Any real-world optimisation application without independent validation and noise characterisation |
| **Licence** | Academic use only — Imperial College BBO Capstone |

---

*BBO Capstone Data Card — Mike Kennelly — Imperial College — Week 13 FINAL Query*
