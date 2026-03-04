# BBO Capstone — Black-Box Optimisation Pipeline
**Mike Kennelly | MSc AI | Weeks 1–6**

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
- **CNN-1D as Model 8** — convolutional classifier added Week 6 to detect coordinate-pair patterns
- **Week log override** — true best points from submission emails injected into GP training where `.npy` files had missing history

---

## Repository Structure

```
Capstone_FX_W1.ipynb    # Week 1 notebooks — GP + EI/UCB baseline (F1–F8)
Capstone_FX_W2.ipynb    # Week 2 — local refinement added
Capstone_FX_W3.ipynb    # Week 3 — SVM classifier pre-filter introduced
Capstone_FX_W4.ipynb    # Week 4 — multi-model CV, 7 classifiers compared
Capstone_FX_W5.ipynb    # Week 5 — pipeline stabilised
Capstone_FX_W6.ipynb    # Week 6 — CNN-1D Model 8, week log overrides
week_log_FX.json        # True W1–W5 history per function (ground truth)
f{n}_w5_inputs.npy      # Input history from platform
f{n}_w5_outputs.npy     # Output history from platform
W6_Submissions.txt      # Week 6 copy-paste submission file
references.md           # Academic justifications for all design choices
BBO_W6_Strategy.docx    # Full strategy table — all 8 functions
BBO_W6_Reflection.docx  # Written reflection — CNN concepts and BBO
```

---

## W6 Strategy At a Glance

| Fn | Dims | n | Strategy | True Best | Key Insight |
|----|------|---|----------|-----------|-------------|
| F1 | 2D | 14 | EXPLORE | W2 ≈ 0 | All values near-zero — broad sampling |
| F2 | 2D | 14 | EXPLOIT W5 | W5 = 0.650 | Best at X2=0.16, not X2=0.93 as assumed |
| F3 | 3D | 19 | RECOVER W1 | W1 = -0.014 | Consistent decline since W1 |
| F4 | 4D | 34 | RECOVER W2 | W2 = +0.238 | Only positive value — missing from .npy |
| F5 | 4D | 24 | RECOVER W3 | W3 = 4,891 | X1=0.803 not 0.355 — critical correction |
| F6 | 5D | 24 | RECOVER W2 | W2 = -0.237 | X4 high + X5 low is the key pattern |
| F7 | 6D | 34 | RECOVER W2 | W2 = 1.739 | .npy showed idx6=0.808, true best 2× higher |
| F8 | 8D | 44 | EXPLOIT | W2 = 9.832 | Most consistent function |

**Critical discovery:** `.npy` files were missing W2, W3 and W5 submissions for most functions. Week logs built from submission emails were used as ground truth. F2, F4, F5 and F7 were all targeting the wrong coordinates before this correction.

---

## CNN-1D Results (Week 6)

CNN-1D was added as Model 8 and evaluated against 7 classical classifiers via 5-fold CV:

| Function | CNN Score | Winner | Gap | Why CNN performed well |
|----------|-----------|--------|-----|----------------------|
| F5 | 85.7% | RF (tied) | 0.0% | All dims high — clear boundary pattern |
| F4 | 83.3% | LR 83.9% | 0.6% | Tight coordinate cluster at optimum |
| F6 | ~75% | LR 75.0% | ~0% | X4/X5 pattern detectable by Conv1d |
| F1 | ~65% | SVM 66.7% | ~2% | Flat landscape — no pattern to learn |

CNN performs best where the optimum has a **local coordinate structure** — tight clusters or boundary patterns that Conv1d detects by scanning adjacent feature pairs.

---

## Running a Notebook

1. Place `week_log_FX.json` and `fX_w6_inputs/outputs.npy` in the same folder as the notebook
2. Run all cells top to bottom
3. Step 14 prints the formatted submission string

**Requirements:** `numpy`, `scikit-learn`, `matplotlib`, `scipy`, `torch`

---

## Academic Basis

All design choices are justified against peer-reviewed literature. See [`references.md`](references.md) for full citations and one-line explanations of what each paper justifies in the pipeline.

Key references:
- Jones et al. (1998) — Expected Improvement
- Rasmussen & Williams (2006) — Gaussian Processes
- Srinivas et al. (2010) — GP-UCB
- Eriksson et al. (2019) — TuRBO trust regions (planned Week 7)
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
| W7 | Adaptive TuRBO trust region (planned) |
