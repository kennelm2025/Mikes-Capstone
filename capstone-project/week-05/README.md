# BBO Capstone — Week 5
**Mike Kennelly | MSc AI | Black-Box Optimisation**

Week 5 uses the same 5-model CV pipeline as W4 — now stabilised. The critical
development is the **week log system**: submission emails cross-referenced
against npy files revealed missing data for F4, F5, F6 and F7. This discovery
reshapes the entire W6 strategy.

---

## Pipeline

```
Load data → Binary labels (top 30%) → Train 5 classifier families
→ 5-fold CV → Select winner → Generate 10,000 candidates
→ Filter by winner → Fit GP → EI + UCB → Submit
```

Same as W4 — pipeline stabilised. Key work this week is the week log audit.

---

## Key Results

| Fn | Dims | CV Winner    | W4 Result | W5 Result  | Change     | W6 Action       |
|----|------|--------------|-----------|------------|------------|-----------------|
| F1 | 2D   | Linear SVM   | 1.66e-9   | -5.44e-7   | ≈ 0        | EXPLORE         |
| F2 | 2D   | Rand. Forest | 0.019     | 0.6497 ✅  | ↑ NEW BEST | EXPLOIT W5      |
| F3 | 3D   | Dec. Tree    | -0.138    | -0.059     | ↑ Partial  | RECOVER W1      |
| F4 | 4D   | NN-Small     | -0.527    | -2.457     | ↓ CRASH    | RECOVER W2 ⚠️  |
| F5 | 4D   | Rand. Forest | 2913      | 24.48      | ↓ CRASH    | RECOVER W3 ⚠️  |
| F6 | 5D   | Logistic Reg | -0.363    | -1.766     | ↓ CRASH    | RECOVER W2 ⚠️  |
| F7 | 6D   | Linear SVM   | 1.140     | 0.576      | ↓ Decline  | RECOVER W2 ⚠️  |
| F8 | 8D   | Dec. Tree    | 9.334     | 8.956      | ↓ Slight   | EXPLOIT tighter |

✅ = new all-time best | ⚠️ = best_point override required in W6

---

## Critical Discovery — Week Log System

Cross-referencing submission emails against npy files revealed:

| Function | Missing from npy | True best | Impact |
|----------|-----------------|-----------|--------|
| F4 | W2 submission | +0.238 at [0.439, 0.415, 0.385, 0.398] | GP never saw only positive value |
| F5 | W3 submission | 4891 at [0.803, 0.945, 0.998, 0.976] | X1=0.803 vs npy X1=0.355 |
| F6 | W2 submission | -0.237 at [0.410, 0.299, 0.510, 0.814, 0.072] | True best 35% better than npy best |
| F7 | W2 submission | 1.739 at [0.016, 0.438, 0.301, 0.218, 0.388, 0.698] | True best 2× npy best |

Without this correction all four functions would target wrong coordinates in W6.

---

## Academic Basis
- Chennu et al. — each week's score is a noisy signal, not ground truth
- Srinivas et al. (2010) — GP-UCB dual acquisition
- Jones (1998), Rasmussen & Williams (2006) — GP + EI

## Requirements
`numpy` `scikit-learn` `matplotlib` `scipy`

---
*Week 5 | BBO Capstone | Mike Kennelly*
