# BBO Capstone — Week 1
**Mike Kennelly | MSc AI | Black-Box Optimisation**

Week 1 baseline. Each function receives initial platform samples and a first
GP surrogate is fitted. No submission history exists yet — pure exploration.

---

## Pipeline

```
Load initial samples → Fit GP (RBF kernel) → Compute EI + UCB
→ Submit highest acquisition score point
```

No classifier. No candidate filter. Acquisition function drives everything.

---

## Functions

| Fn | Dims | n (initial) | W1 Result | Key Signal |
|----|------|-------------|-----------|------------|
| F1 | 2D   | 10          | ≈ 0.000   | Flat landscape — no signal |
| F2 | 2D   | 10          | 0.525     | X1~0.7 promising region |
| F3 | 3D   | 13          | -0.0136   | X1~0.97 upper boundary ← all-time best |
| F4 | 4D   | 13          | -2.627    | [0.4–0.5]^4 baseline |
| F5 | 4D   | 13          | 60.07     | Mid-range positive — large value function |
| F6 | 5D   | 13          | -1.339    | No clear signal yet |
| F7 | 6D   | 13          | 0.809     | X1≈0.06 boundary signal |
| F8 | 8D   | 13          | 9.009     | X1≈0.01 boundary — strong opening |

---

## Academic Basis
- Jones et al. (1998) — Expected Improvement acquisition
- Rasmussen & Williams (2006) — Gaussian Process surrogate

## Requirements
`numpy` `scikit-learn` `matplotlib` `scipy`

---
*Week 1 | BBO Capstone | Mike Kennelly*
