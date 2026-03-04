# Bayesian Optimisation Capstone — Week 3
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London

Week 3 introduces the SVM classifier pre-filter — the most significant
pipeline change of the capstone. A classifier trained on binary labels
(top 30% = class 1) screens 10,000 random candidates before the GP ranks them.

---

## Pipeline

```
Load data → Binary labels (top 30%) → Train SVM classifier
→ Generate 10,000 candidates → Filter by SVM → Fit GP
→ Compute EI + UCB → Submit
```

**Why SVM first?** Concentrates GP attention on structurally promising
regions — reducing wasted evaluations in clearly bad areas.
Not all functions use SVM: F7 uses pure GP (CV too low in 6D),
F6 uses conditional SVM (only if CV > threshold).

---

## Key Results

| Fn | Dims | Pipeline      | W2 Result | W3 Result | Change    |
|----|------|---------------|-----------|-----------|-----------|
| F1 | 2D   | Model test    | 8.84e-7   | 5.17e-96  | ≈ 0       |
| F2 | 2D   | SVM → GP      | 0.285     | -0.030    | ↓ Regress |
| F3 | 3D   | SVM → GP      | -0.033    | -0.083    | ↓ Regress |
| F4 | 4D   | SVM → GP      | +0.238    | -0.962    | ↓ Regress |
| F5 | 4D   | SVM → GP      | 4062      | 4891 ✅   | ↑ NEW BEST|
| F6 | 5D   | Cond. SVM     | -0.237    | -0.883    | ↓ Regress |
| F7 | 6D   | Pure GP       | 1.739     | 1.736     | ≈ HOLD    |
| F8 | 8D   | SVM → GP      | 9.832     | 9.819     | ≈ HOLD    |

✅ = new all-time best

F5 and F7/F8 performing well. F3, F4, F6 regressing —
classifier has limited data to work with at n=15–20.

---

## Academic Basis
- Cybenko (1989) — theoretical grounding for classifier approach
- Goodfellow et al. (2016) — neural network classifiers
- Jones (1998), Rasmussen & Williams (2006) — GP + EI

## Requirements
`numpy` `scikit-learn` `matplotlib` `scipy`

---
*Week 3 | BBO Capstone | Mike Kennelly*
