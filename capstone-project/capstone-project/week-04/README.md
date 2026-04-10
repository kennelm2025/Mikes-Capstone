# Bayesian Optimisation Capstone — Week 4
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London


Week 4 expands from a single SVM to 5 classifier families compared via
cross-validation. The best CV model filters candidates for that function
that week. NN gradient analysis added to identify sensitive dimensions.

---

## Pipeline

```
Load data → Binary labels (top 30%) → Train 5 classifier families
→ 5-fold CV → Select winner → Generate 10,000 candidates
→ Filter by winner → Fit GP → EI + UCB → Submit
```

**5 models compared:**
Linear SVM | Decision Tree | Random Forest
| Logistic Regression | Neural Network (Small / Medium / Large)

---

## Key Results

| Fn | Dims | CV Winner     | CV Acc | W3 Result | W4 Result | Change    |
|----|------|---------------|--------|-----------|-----------|-----------|
| F1 | 2D   | Linear SVM    | ~67%   | 5.17e-96  | 1.66e-9   | ≈ 0       |
| F2 | 2D   | Rand. Forest  | ~73%   | -0.030    | 0.019     | ↑ Slight  |
| F3 | 3D   | Dec. Tree     | ~75%   | -0.083    | -0.138    | ↓ Regress |
| F4 | 4D   | NN-Small      | ~80%   | -0.962    | -0.527    | ↑ Recover |
| F5 | 4D   | Rand. Forest  | ~87%   | 4891      | 2913      | ↓ Regress |
| F6 | 5D   | Logistic Reg  | ~75%   | -0.883    | -0.363    | ↑ Recover |
| F7 | 6D   | Linear SVM    | ~80%   | 1.736     | 1.140     | ↓ Regress |
| F8 | 8D   | Dec. Tree     | ~86%   | 9.819     | 9.334     | ↓ Slight  |

F4 and F6 recovering. F5 and F7 regressing due to coordinate drift —
classifiers not enforcing the confirmed boundary patterns.

---

## Academic Basis
- Barrett et al. (2019) — when do NNs outperform simpler models?
- Cybenko (1989), Goodfellow et al. (2016) — classifier foundations
- Jones (1998), Rasmussen & Williams (2006) — GP + EI

## Requirements
`numpy` `scikit-learn` `matplotlib` `scipy`

---
*Week 4 | BBO Capstone | Mike Kennelly*
