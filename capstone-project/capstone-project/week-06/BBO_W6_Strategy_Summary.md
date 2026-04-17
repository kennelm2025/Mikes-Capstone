# BBO Capstone — Week 6 Strategy Summary
**Mike Kennelly | All functions MAXIMISATION — higher is always better**

---

## Overview

After 5 weeks of evaluations, each function has between 14 and 44 historical
data points. Week 6 strategy is driven by three things:

1. **Week log ground truth** — submission emails used to reconstruct true
   W1–W5 history. Several `.npy` files were missing W2, W3 and W5 data.
   True best points differ from npy bests for F2, F4, F5, F6 and F7.
2. **Trajectory** — is the function improving, stuck, or regressing?
3. **Data density** — n/p ratio (samples / dimensions) determines how
   much we trust the Gaussian Process surrogate.

Key parameters that differ across functions:

| Parameter     | Controls                                      | Range used W6 |
|---------------|-----------------------------------------------|---------------|
| EXPLOIT_RATIO | Fraction of candidates near best point        | 0.70 – 0.85   |
| EXPLOIT_SIGMA | Gaussian radius around best point             | 0.04 – 0.08   |
| UCB_KAPPA     | Exploration bonus in UCB = mu + kappa*sigma   | 2.0 – 3.0     |
| GP_RESTARTS   | Kernel hyperparameter search restarts         | 5 – 8         |

**New in Week 6:** CNN-1D added as Model 8 across all functions. True best
points from week logs override npy defaults in the data load cell.

---

## F1 — EXPLORE
**2D | n=14 | n/p=7.0 | True best = 8.84e-7 (W2) | W5 = -5.4e-7**

### What the data says
Five weeks of evaluations and all scores are effectively zero — the range
across all submissions is smaller than 1e-6. The function is either bounded
near zero by design or every submission has missed the true high-value region.
Exploiting around a near-zero best will not produce improvement.

### Strategy
Broad exploration — EXPLOIT_RATIO=0.70, EXPLOIT_SIGMA=0.08, UCB_KAPPA=3.0.
30% of candidates drawn uniformly at random. The per-dimension EI curves
are the key diagnostic: if EI peaks at a boundary, the optimum may be in
a region not yet sampled.

### Key settings
```
EXPLOIT_RATIO = 0.70    # 30% uniform exploration
EXPLOIT_SIGMA = 0.08    # Wide search radius
UCB_KAPPA     = 3.0     # Elevated — EI proxy is unreliable near zero
GP_RESTARTS   = 5
```

---

## F2 — EXPLOIT W5 BEST — NEW REGION
**2D | n=14 | n/p=7.0 | True best = 0.6497 (W5) | W5 = 0.6497**

### What the data says
W5 delivered the all-time best of 0.6497 at coordinates [0.710, 0.162].
This is a completely different region from the previously assumed best near
X2=0.93. The week log reveals the full history: W1=0.525, W2=0.285,
W3=-0.030, W4=0.019, W5=0.650. The function found a new high-value region
near X2=0.16 in W5.

### Strategy
Exploit the W5 discovery. EXPLOIT_RATIO=0.85, candidates concentrated around
[0.710, 0.162]. Best point override applied in code — npy file shows a
different (lower) best due to missing history.

### Key settings
```
EXPLOIT_RATIO = 0.85    # W5 new best — exploit the new region
EXPLOIT_SIGMA = 0.04    # Tight around [0.710, 0.162]
UCB_KAPPA     = 2.0
GP_RESTARTS   = 5
# best_point override: [0.7101, 0.1616], best_val=0.6497
```

---

## F3 — RECOVER W1
**3D | n=19 | n/p=6.3 | True best = -0.0136 (W1) | W5 = -0.0590**

### What the data says
W1 produced the best score ever at -0.0136 from [0.966, 0.518, 0.403].
Every subsequent week has been worse — W2=-0.033, W3=-0.083, W4=-0.138,
W5=-0.059 (partial recovery). The npy best matches the week log — no
missing data issue here. X1 near the upper boundary (0.966) is a strong
structural signal.

### Strategy
Recover to the W1 region. EXPLOIT_RATIO=0.80, centred on [0.966, 0.518, 0.403].
Per-dimension EI curves are the key diagnostic: does X1 EI peak near 0.97–1.0?

### Key settings
```
EXPLOIT_RATIO = 0.80    # 20% exploration — GP overfitting insurance in 3D
EXPLOIT_SIGMA = 0.05    # Around [0.966, 0.518, 0.403]
UCB_KAPPA     = 2.5
GP_RESTARTS   = 5
```

---

## F4 — RECOVER W2
**4D | n=34 | n/p=8.5 | True best = +0.2376 (W2) | W5 = -2.4571**

### What the data says
The week log reveals the true history: W1=-2.627, W2=+0.238, W3=-0.962,
W4=-0.527, W5=-2.457. W2 produced the only positive value in 5 weeks —
+0.238 at [0.439, 0.415, 0.385, 0.398]. This point is **missing from the
npy file**. The npy showed -0.527 as the best, which led to wrong target
coordinates in earlier weeks. W5 regressed badly.

### Strategy
Recover to the W2 region. Best point override is critical — without it the
GP targets -0.527 at the wrong coordinates. All four W2 coords cluster
tightly in [0.38–0.44] — a clear structural pattern.

### Key settings
```
EXPLOIT_RATIO = 0.85    # Recover to W2 region
EXPLOIT_SIGMA = 0.04    # Around [0.439, 0.415, 0.385, 0.398]
UCB_KAPPA     = 2.0
GP_RESTARTS   = 5
# best_point override: [0.4392, 0.415, 0.3847, 0.3979], best_val=+0.2376
```

---

## F5 — RECOVER W3
**4D | n=24 | n/p=6.0 | True best = 4890.58 (W3) | W5 = 24.48**

### What the data says
The week log reveals: W1=60, W2=4062, W3=4891 (peak), W4=2913, W5=24.
The true best of 4890.58 at [0.803, 0.945, 0.998, 0.976] is **missing from
the npy file** — the npy showed W4=2912 as best, with X1=0.355. This was a
critical error: X1 should be ~0.80 not ~0.35. ALL four dimensions are near
the upper boundary in the W3 best, not just X2–X4. W5 collapsed to 24 after
targeting the wrong X1 coordinate.

### Strategy
Recover to the W3 region with X1=0.803 explicitly targeted. Best point
override essential. All four dims high is the confirmed pattern.

### Key settings
```
EXPLOIT_RATIO = 0.85    # Recover to W3 — all dims high
EXPLOIT_SIGMA = 0.04    # Around [0.803, 0.945, 0.998, 0.976]
UCB_KAPPA     = 2.0
GP_RESTARTS   = 5
# best_point override: [0.803, 0.9455, 0.9975, 0.9763], best_val=4890.58
# CRITICAL: X1=0.803 not 0.355
```

---

## F6 — RECOVER W2
**5D | n=24 | n/p=4.8 | True best = -0.2372 (W2) | W5 = -1.7662**

### What the data says
Week log: W1=-1.339, W2=-0.237 (best), W3=-0.883, W4=-0.363, W5=-1.767.
True best -0.237 at [0.410, 0.299, 0.510, 0.814, 0.072] is missing from npy
— npy showed -0.363 (W4) as best. Key structural pattern: X4=0.814 (high)
and X5=0.072 (near zero lower boundary). n/p=4.8 is the lowest in the batch —
the most data-sparse function.

### Strategy
Recover to W2 coords with elevated UCB_KAPPA to account for GP uncertainty
at low n/p. Best point override applied. X4 high + X5 low is the confirmed
pattern to target.

### Key settings
```
EXPLOIT_RATIO = 0.85    # Recover to W2 region
EXPLOIT_SIGMA = 0.04    # Around [0.410, 0.299, 0.510, 0.814, 0.072]
UCB_KAPPA     = 2.5     # Elevated — n/p=4.8 is sparse
GP_RESTARTS   = 5
# best_point override: [0.4096, 0.2992, 0.5097, 0.8141, 0.0721], best_val=-0.2372
```

---

## F7 — RECOVER W2
**6D | n=34 | n/p=5.7 | True best = 1.7392 (W2) | W5 = 0.5763**

### What the data says
Week log: W1=0.809, W2=1.739 (best), W3=1.736, W4=1.140, W5=0.576.
True best 1.739 at [0.016, 0.438, 0.301, 0.218, 0.388, 0.698] is **missing
from the npy file** — the npy showed idx6=0.808 (W1) as best, which is less
than half the true best. W2 and W3 both near 1.74 confirm the region is
real. W4 and W5 declined as submissions moved away. X1≈0.016 (near zero
boundary) is a strong structural signal.

### Strategy
Recover to W2/W3 confirmed peak region. Best point override essential.
EXPLOIT_RATIO raised to 0.85 given the W4/W5 regression.

### Key settings
```
EXPLOIT_RATIO = 0.85    # Recover to W2/W3 peak — W5 regressed badly
EXPLOIT_SIGMA = 0.04    # Around [0.016, 0.438, 0.301, 0.218, 0.388, 0.698]
UCB_KAPPA     = 2.5     # Elevated — 6D with missing history
GP_RESTARTS   = 8       # 6 length scales — thorough search
# best_point override: [0.0162, 0.4377, 0.3014, 0.2179, 0.3884, 0.6978], best_val=1.7392
```

---

## F8 — EXPLOIT
**8D | n=44 | n/p=5.5 | True best = 9.832 (W2) | W5 = 8.956**

### What the data says
Week log: W1=9.009, W2=9.832 (best), W3=9.819, W4=9.334, W5=8.956.
The most consistent function in the batch — tight range, no catastrophic
regression. Gap between true best (9.832) and npy best (9.819) is only
0.013 — effectively the same. Structural pattern: X1, X3, X7 near zero,
X5=0.929 (high).

### Strategy
Standard exploitation — the landscape is broad and stable. No override
needed as npy best closely matches true best. CNN-1D as Model 8 is most
viable here given the largest n in the batch (n=44).

### Key settings
```
EXPLOIT_RATIO = 0.80    # Standard — broad landscape, stable trajectory
EXPLOIT_SIGMA = 0.05    # Around [0.0, 0.179, 0.0, 0.071, 0.929, 0.460, 0.0, 0.541]
UCB_KAPPA     = 2.0
GP_RESTARTS   = 5
```

---

## Summary Table

| Fn | Dims | n  | n/p | True Best   | Wk | W5 Score | Strategy       | Ratio | Sigma | κ   | Override |
|----|------|----|-----|-------------|-----|----------|----------------|-------|-------|-----|----------|
| F1 | 2D   | 14 | 7.0 | ≈ 0         | W2  | ≈ 0      | EXPLORE        | 0.70  | 0.08  | 3.0 | —        |
| F2 | 2D   | 14 | 7.0 | 0.6497      | W5  | 0.6497   | EXPLOIT W5     | 0.85  | 0.04  | 2.0 | ✅       |
| F3 | 3D   | 19 | 6.3 | -0.0136     | W1  | -0.059   | RECOVER W1     | 0.80  | 0.05  | 2.5 | —        |
| F4 | 4D   | 34 | 8.5 | +0.2376     | W2  | -2.457   | RECOVER W2     | 0.85  | 0.04  | 2.0 | ✅       |
| F5 | 4D   | 24 | 6.0 | 4890.58     | W3  | 24.48    | RECOVER W3     | 0.85  | 0.04  | 2.0 | ✅       |
| F6 | 5D   | 24 | 4.8 | -0.2372     | W2  | -1.766   | RECOVER W2     | 0.85  | 0.04  | 2.5 | ✅       |
| F7 | 6D   | 34 | 5.7 | 1.7392      | W2  | 0.576    | RECOVER W2     | 0.85  | 0.04  | 2.5 | ✅       |
| F8 | 8D   | 44 | 5.5 | 9.832       | W2  | 8.956    | EXPLOIT        | 0.80  | 0.05  | 2.0 | —        |

✅ = best_point override applied — true best missing from `.npy` file.

All functions: N_CANDIDATES=10,000 | TOP_PERCENTILE=30 | FILTER_PERCENTILE=50
| RANDOM_SEED=42 | MAXIMIZE=True | CNN-1D as Model 8

---

*Week 6 | BBO Capstone | Mike Kennelly*
