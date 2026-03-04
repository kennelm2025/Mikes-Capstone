# BBO Capstone — Week 2
**Mike Kennelly | MSc AI | Black-Box Optimisation**

Week 2 incorporates the first submission result. GP refitted on expanded
history. Local refinement added — neighbourhood search around the current
best point tests whether small coordinate moves improve acquisition score.

---

## Pipeline

```
Load data (initial + W1 result) → Refit GP → Compute EI + UCB
→ Local refinement around best point → Submit
```

Still no classifier — GP + acquisition drives candidate selection.

---

## Key Results

| Fn | Dims | W1 Result | W2 Result  | Change    | Note |
|----|------|-----------|------------|-----------|------|
| F1 | 2D   | ≈ 0       | 8.84e-7 ✅ | ≈ 0       | All-time best (still near zero) |
| F2 | 2D   | 0.525     | 0.285      | ↓ Regress | GP exploring around W1 |
| F3 | 3D   | -0.0136   | -0.033     | ↓ Regress | W1 best not replicated |
| F4 | 4D   | -2.627    | +0.238 ✅  | ↑ PEAK    | Only positive value — missing from npy |
| F5 | 4D   | 60.07     | 4062 ✅    | ↑ LEAP    | Boundary push — missing from npy |
| F6 | 5D   | -1.339    | -0.237 ✅  | ↑ PEAK    | X4↑ X5↓ pattern — missing from npy |
| F7 | 6D   | 0.809     | 1.739 ✅   | ↑ PEAK    | X1≈0 confirmed — missing from npy |
| F8 | 8D   | 9.009     | 9.832 ✅   | ↑ PEAK    | All-time best — boundary pattern |

✅ = all-time best | 4 functions peaked at W2, all missing from npy files

---

## Critical Note
W2 bests for F4, F5, F6 and F7 were **missing from npy files** — discovered
via the week log system in W5. Without this correction, W6 would have targeted
wrong coordinates for these 4 functions.

---

## Academic Basis
- Jones et al. (1998) — EI acquisition
- Rasmussen & Williams (2006) — GP surrogate + local refinement

## Requirements
`numpy` `scikit-learn` `matplotlib` `scipy`

---
*Week 2 | BBO Capstone | Mike Kennelly*
