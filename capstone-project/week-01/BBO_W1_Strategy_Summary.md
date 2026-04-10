# BBO Capstone — Week 1 Strategy Summary
**Mike Kennelly | All functions MAXIMISATION — higher is always better**

---

## Overview

Week 1 is pure exploration. Each function receives a small set of initial
samples from the platform (n=4–10 points depending on dimensionality).
With no prior submission history, the strategy is simple: fit a GP to the
initial data, compute EI and UCB across the search space, and submit the
point with the highest acquisition score.

Pipeline this week: **GP + EI/UCB only — no classifier, no candidate filter.**

Key reference: Jones et al. (1998) — EI as the principled acquisition function
for expensive black-box optimisation with a limited query budget.

---

## F1 — EXPLORE (2D)
**Initial samples only | GP + EI/UCB | Submitted: [0.083, 1.54] → W1 = 0.000**

All initial outputs effectively zero. No signal to exploit.
EI and UCB both flat across the space — submission driven by UCB exploration bonus.
W1 result: 0.000 (platform minimum).

---

## F2 — EXPLORE (2D)
**Initial samples only | GP + EI/UCB | Submitted: [0.706, 1.488] → W1 = 0.525**

Positive result from first submission — GP found a promising region in [0.7, 1.0]^2.
W1 = 0.525 is a strong opening result. EI peak in X1~0.7 region confirmed.

---

## F3 — EXPLORE (3D)
**Initial samples only | GP + EI/UCB | Submitted: [0.966, 0.518, 0.403] → W1 = -0.0136**

All initial outputs negative. Best of -0.0136 at [0.966, 0.518, 0.403] —
X1 near upper boundary is the key signal. This W1 result turns out to be
the all-time best for F3 across all 5 weeks.

---

## F4 — EXPLORE (4D)
**Initial samples only | GP + EI/UCB | Submitted: [0.414, 0.477, 0.466, 0.474] → W1 = -2.627**

All initial outputs deeply negative. GP has limited signal in 4D from initial samples.
Submission in the [0.4–0.5]^4 region based on EI. Result -2.627 is poor
but establishes a baseline for the search.

---

## F5 — EXPLORE (4D)
**Initial samples only | GP + EI/UCB | Submitted: [0.120, 0.499, 0.478, 0.495] → W1 = 60.07**

Positive result — W1 = 60.07 in the mid-range of the space.
The function has large output values (later confirmed in the thousands).
W1 result is low relative to what is achievable but confirms the function is active.

---

## F6 — EXPLORE (5D)
**Initial samples only | GP + EI/UCB | Submitted: [0.022, 0.563, 0.467, 0.534, 0.424] → W1 = -1.339**

All initial outputs negative. 5D space is hard to cover with initial samples.
GP uncertainty is high everywhere. Submission driven by UCB exploration bonus.
W1 = -1.339 — poor result, X1 near zero but other dims mid-range.

---

## F7 — EXPLORE (6D)
**Initial samples only | GP + EI/UCB | Submitted: [0.058, 0.396, 0.390, 0.513, 0.467, 0.485] → W1 = 0.809**

Positive result. X1=0.058 near zero boundary — strong structural signal
that will be confirmed by W2 and W3. W1 = 0.809 is a reasonable opening
score in 6D.

---

## F8 — EXPLORE (8D)
**Initial samples only | GP + EI/UCB | Submitted: [0.009, 0.472, 0.516, 0.430, 0.469, 0.460, 0.579, 0.507] → W1 = 9.009**

Strong opening result — W1 = 9.009 in a function with range ~5.5–9.8.
X1 near zero boundary is an early structural signal. GP has reasonable
coverage of 8D with initial samples.

---

## Summary Table

| Fn | Dims | Strategy | W1 Result | Key Signal |
|----|------|----------|-----------|------------|
| F1 | 2D   | EXPLORE  | ≈ 0.000   | No signal — flat landscape |
| F2 | 2D   | EXPLORE  | 0.525     | X1~0.7 promising region |
| F3 | 3D   | EXPLORE  | -0.0136   | X1~0.97 upper boundary (all-time best) |
| F4 | 4D   | EXPLORE  | -2.627    | [0.4–0.5]^4 region baseline |
| F5 | 4D   | EXPLORE  | 60.07     | Mid-range positive — large value function |
| F6 | 5D   | EXPLORE  | -1.339    | No clear signal yet |
| F7 | 6D   | EXPLORE  | 0.809     | X1≈0.06 boundary signal |
| F8 | 8D   | EXPLORE  | 9.009     | X1≈0.01 boundary — strong opening |

All functions: Pure GP + EI/UCB | No classifier | No candidate filter
| Jones et al. (1998) EI acquisition | Rasmussen & Williams (2006) GP surrogate

---

*Week 1 | BBO Capstone | Mike Kennelly*
