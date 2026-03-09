# Bayesian Optimisation Capstone — Week 7
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London

Adaptive Bayesian Optimisation pipeline for maximising 8 unknown black-box functions simultaneously. One submission per function per week. No access to gradients, source code, or function form.

---

## How It Works

Each week's notebook runs the same pipeline:

```
Load data → Binary labels (top 30%) → Train 8 classifiers (incl. CNN-1D)
→ CV select winner → Generate 10,000 candidates → Filter by classifier
→ Fit GP → Compute EI + UCB → Submit top candidate
```

**Key design decisions:**
- **GP + EI** — Gaussian Process surrogate with Expected Improvement acquisition (Jones et al., 1998)
- **Dual acquisition** — EI and UCB combined; scores normalised and summed (Srinivas et al., 2010)
- **Classifier pre-filter** — top 30% labelled as class 1; best CV model from 8 classifiers filters 10,000 candidates before GP runs
- **CNN-1D as Model 8** — convolutional classifier tracking performance week on week as sample size grows
- **Week log override** — true best points from submission emails injected into GP training where `.npy` files have missing history
- **TuRBO sigma adaptation** — exploit sigma adjusted per-function based on W6 trajectory outcome

---

## Repository Structure

```
Capstone_FX_W1.ipynb    # Week 1 notebooks — GP + EI/UCB baseline (F1–F8)
Capstone_FX_W2.ipynb    # Week 2 — local refinement added
Capstone_FX_W3.ipynb    # Week 3 — SVM classifier pre-filter introduced
Capstone_FX_W4.ipynb    # Week 4 — multi-model CV, 7 classifiers compared
Capstone_FX_W5.ipynb    # Week 5 — pipeline stabilised
Capstone_FX_W6.ipynb    # Week 6 — CNN-1D Model 8, week log overrides
Capstone_FX_W7.ipynb    # Week 7 — TuRBO sigma adaptation, per-function strategies from W6 outcomes
week_log_FX.json        # True W1–W6 history per function (ground truth)
f{n}_w7_inputs.npy      # Input history from platform (W7)
f{n}_w7_outputs.npy     # Output history from platform (W7)
W7_Submissions.txt      # Week 7 copy-paste submission file
references.md           # Academic justifications for all design choices
BBO_W7_Strategy.docx    # Full strategy table — all 8 functions
BBO_W7_Reflection.docx  # Written reflection
```

---

## W7 Strategy At a Glance

| Fn | Dims | n  | Strategy | True Best | W6 Score | σ W7 | TuRBO | W7 Submission |
|----|------|----|----------|-----------|----------|------|-------|---------------|
| F1 | 2D   | 15 | EXPLORE | W2 ≈ 0 | ≈ 0 | 0.216 | EXPAND | `0.582827-0.482269` |
| F2 | 2D   | 15 | EXPLOIT W5 BEST | W5 = 0.6497 | 0.584 | 0.0175 | SHRINK | `0.688952-0.168811` |
| F3 | 3D   | 20 | EXPLOIT W6 NEW BEST | W6 = -0.000707 | -0.000707 | 0.024 | SHRINK | `1.000000-0.571651-0.503999` |
| F4 | 4D   | 35 | RECOVER W2 BEST ⚠️ | W2 = +0.2376 | -0.129 | 0.0175 | SHRINK | `0.451762-0.438642-0.400163-0.395091` |
| F5 | 4D   | 25 | EXPLOIT W6 NEW BEST | W6 = 5,875 | 5,875 | 0.048 | EXPAND | `0.937682-1.000000-1.000000-1.000000` |
| F6 | 5D   | 25 | EXPLOIT W6 NEW BEST | W6 = -0.1727 | -0.1727 | 0.042 | EXPAND | `0.497320-0.294798-0.563080-0.684981-0.129206` |
| F7 | 6D   | 35 | EXPLOIT W6 NEW BEST | W6 = 2.119 | 2.119 | [0.015,0.035×5] ★ | SHRINK | `0.078067-0.385415-0.381193-0.266170-0.353901-0.693102` |
| F8 | 8D   | 45 | EXPLOIT W2 BEST ⚠️ | W2 = 9.832 | 9.774 | 0.0175 | SHRINK | `0.040422-0.331667-0.003668-0.158463-0.396893-0.509806-0.166490-0.780552` |

**Key W7 decisions:**
- F3, F5, F6, F7 all set new all-time bests in W6 — exploit these discoveries
- F2 W6 regressed slightly from W5 best — hold tight on W5 region, tighten sigma
- F4 and F8 use week log overrides ⚠️ — best points missing from npy files, injected from email confirmations
- F7 ★ uses **anisotropic sigma** `[0.015, 0.035, 0.035, 0.035, 0.035, 0.035]` — motivated by CNN filter map analysis (Step 5B) which showed filters 3 & 4 peaking on coord pair [0,1], confirming X1 is the dominant structural dimension

---

## TuRBO Sigma Adaptation (Week 7)

Exploit sigma adjusted per function based on W6 trajectory. EXPAND = sigma increased (wider search); SHRINK = sigma decreased (precision around confirmed best).

| Fn | sigma W6 | sigma W7 | Direction | Rationale |
|----|----------|----------|-----------|-----------|
| F1 | 0.08 | 0.216 | EXPAND | No improvement in 6 weeks — cast dramatically wider net |
| F2 | 0.04 | 0.0175 | SHRINK | W5 region confirmed — precision around [0.710, 0.162] |
| F3 | 0.04 | 0.024 | SHRINK | New best W6 confirmed — tighten precision around W6 coords |
| F4 | 0.04 | 0.0175 | SHRINK | W2 tight cluster [0.38-0.44] confirmed — precision inject |
| F5 | 0.04 | 0.048 | EXPAND | Boundary pattern X2-X4=1.0 — slightly wider cloud to find better X1 |
| F6 | 0.04 | 0.042 | EXPAND | New best W6 in 5D — marginal expand, n/p=5.0 still sparse |
| F7 | 0.04 | 0.030 | SHRINK | New best W6=2.119 confirmed — tighten precision around X1=0.055 region |
| F8 | 0.03 | 0.0175 | SHRINK | W2 boundary pattern (X1,X3,X7~0) confirmed — precision inject |

---

## CNN-1D Status (Week 7)

CNN-1D runs as Model 8 in Step 5 CV comparison across all functions. Results below are W6 actuals where available; marked as tracking where CV outcome was not definitive.

| Function | n (W7) | Dims | CNN W6 Status | Notes |
|----------|--------|------|---------------|-------|
| F1 | 15 | 2D | Tracking | Near-zero landscape — almost no classification signal |
| F2 | 15 | 2D | Tracking | Small n, 2D — CNN vs MLP gap expected to narrow with more data |
| F3 | 20 | 3D | Tracking | Competitive at n=20 — more signal than F1/F2 |
| F4 | 35 | 4D | Strong (83.3%) | Tight coordinate cluster at W2 best — local pattern detectable |
| F5 | 25 | 4D | Strong (85.7%) | All-dims-high boundary pattern — clearest structure in batch |
| F6 | 25 | 5D | Competitive | X4 high + X5 low pattern — Conv1d detects adjacent feature pairs |
| F7 | 35 | 6D | Competitive | X1 boundary pattern at 0.055 — more data than F1/F2 |
| F8 | 45 | 8D | Tracking | Best conditions (n=45, 8D) — most statistically meaningful result |

CNN performs best where the optimum has **local coordinate structure** — tight clusters or boundary patterns that Conv1d detects by scanning adjacent feature pairs.

---

## Running a Notebook

1. Place `week_log_FX.json` and `fX_w7_inputs/outputs.npy` in the same folder as the notebook
2. Run all cells top to bottom (Kernel → Restart & Run All)
3. Step 14 prints the formatted submission string

**Requirements:** `numpy`, `scikit-learn`, `matplotlib`, `scipy`, `torch`

---

## Academic Basis

All design choices are justified against peer-reviewed literature. See [`references.md`](references.md) for full citations.

Key references:
- Jones et al. (1998) — Expected Improvement
- Rasmussen & Williams (2006) — Gaussian Processes
- Srinivas et al. (2010) — GP-UCB
- Eriksson et al. (2019) — TuRBO trust regions (sigma adaptation applied W7)
- Cybenko (1989) & Goodfellow et al. (2016) — classifier foundations

---

## Pipeline Evolution

| Week | Key Addition |
|------|-------------|
| W1 | GP + EI/UCB baseline |
| W2 | Local refinement around best point |
| W3 | SVM classifier pre-filter |
| W4 | Multi-model CV — 7 classifiers |
| W5 | Pipeline stabilised, week log system built |
| W6 | CNN-1D Model 8, week log overrides, true best corrections |
| W7 | TuRBO sigma adaptation per function based on W6 outcomes |

---

## W7 Actual Submissions

All 8 functions submitted. Strings confirmed from Step 14 notebook output.

| Fn | Dims | Strategy | W7 Submission String |
|----|------|----------|----------------------|
| F1 | 2D | EXPLORE | `0.582827-0.482269` |
| F2 | 2D | EXPLOIT W5 BEST | `0.688952-0.168811` |
| F3 | 3D | EXPLOIT W6 NEW BEST | `1.000000-0.571651-0.503999` |
| F4 | 4D | RECOVER W2 BEST | `0.451762-0.438642-0.400163-0.395091` |
| F5 | 4D | EXPLOIT W6 NEW BEST | `0.937682-1.000000-1.000000-1.000000` |
| F6 | 5D | EXPLOIT W6 NEW BEST | `0.497320-0.294798-0.563080-0.684981-0.129206` |
| F7 | 6D | EXPLOIT W6 NEW BEST | `0.078067-0.385415-0.381193-0.266170-0.353901-0.693102` |
| F8 | 8D | EXPLOIT W2 BEST | `0.040422-0.331667-0.003668-0.158463-0.396893-0.509806-0.166490-0.780552` |

**Notable submission observations:**
- F3: X1=1.000000 — GP pushed to exact boundary, consistent with W6 best at X1=0.998
- F5: X1 moved from 0.781 → 0.938 — GP searching for better X1 near boundary with X2–X4 locked at 1.0
- F7: X1=0.081 — holding near zero boundary (W6 was X1=0.055), tight exploitation confirmed
- F4: All coords in [0.395–0.452] — tight cluster around W2 inject point as intended
- F2: X2=0.169 — close to inject point [0.710, 0.162], exploitation working correctly
