# BBO Capstone — Week 2 Strategy Summary
**Mike Kennelly | All functions MAXIMISATION — higher is always better**

---

## Overview

Week 2 incorporates the first submission result into the GP. Each function
now has n+1 data points (initial samples + W1 result). The GP is refitted
on the expanded history and EI/UCB recomputed. A local refinement step
is added — neighbourhood search around the current best point tests
whether small moves improve the acquisition score.

Pipeline this week: **GP + EI/UCB + Local Refinement — still no classifier.**

Key insight: with only one additional point, the GP posterior shifts
meaningfully in low dimensions (F1, F2) but changes little in higher
dimensions (F7, F8) where the initial sample set was already sparse.

---

## F1 — EXPLORE (2D)
**n=11 | W1=0.000 | Submitted: [0.684, 0.704] → W2 = 8.84e-7**

W1 returned zero — EI is flat. UCB exploration drives the submission
to a new region [0.684, 0.704]. W2 result of 8.84e-7 is the all-time
best for F1 — still effectively zero but confirmed as the peak found
across all 5 weeks.

**Strategy:** EXPLORE — raise UCB_KAPPA, broad sampling.

---

## F2 — EXPLOIT W1 (2D)
**n=11 | W1=0.525 | Submitted: [0.774, 0.964] → W2 = 0.285**

W1 = 0.525 was a strong opening. GP refitted around the [0.7, 1.0] region.
EI peaks nearby — W2 submission moves to [0.774, 0.964].
W2 = 0.285 — regression from W1. The function is not smooth in this region.

**Strategy:** EXPLOIT W1 region with local refinement.

---

## F3 — EXPLOIT W1 (3D)
**n=14 | W1=-0.0136 | Submitted: [1.0, 0.537, 0.578] → W2 = -0.0328**

W1 best at [0.966, 0.518, 0.403] — X1 near upper boundary is confirmed.
GP pushes X1 to 1.0. W2 = -0.033 — slight regression. X1=1.0 is not better
than X1=0.966. Local refinement needed around the W1 coordinates.

**Strategy:** EXPLOIT W1 with X1 boundary focus.

---

## F4 — EXPLOIT W1 (4D)
**n=14 | W1=-2.627 | Submitted: [0.439, 0.415, 0.385, 0.398] → W2 = +0.238**

Major breakthrough — W2 = +0.238 is the only positive value F4 ever achieves
across all 5 weeks. All four coordinates cluster tightly in [0.38–0.44].
This point is **missing from the npy file** — a critical gap discovered
via the week log system. GP in W2 identified the [0.4]^4 cluster correctly.

**Strategy:** EXPLOIT W1 region — GP found the peak in W2.

---

## F5 — EXPLOIT W1 (4D)
**n=14 | W1=60.07 | Submitted: [0.299, 0.968, 1.0, 1.0] → W2 = 4062.1**

Massive leap — W2 = 4,062 from W1 = 60. The GP correctly identified
that X2–X4 near the upper boundary predict very high outputs. X1=0.299
is lower than optimal (W3 will show X1=0.803 is better) but the
boundary push on X2–X4 is the key discovery. This point is also
**missing from the npy file**.

**Strategy:** EXPLOIT upper boundary region — remarkable W2 result.

---

## F6 — EXPLORE (5D)
**n=14 | W1=-1.339 | Submitted: [0.410, 0.299, 0.510, 0.814, 0.072] → W2 = -0.237**

Dramatic improvement — W2 = -0.237 from W1 = -1.339. The GP identified
the key pattern: X4=0.814 (high) and X5=0.072 (near zero). This W2 result
is the all-time best for F6 across all 5 weeks. Point is **missing from npy**.

**Strategy:** EXPLOIT — GP nailed the X4 high + X5 low pattern in W2.

---

## F7 — EXPLOIT W1 (6D)
**n=14 | W1=0.809 | Submitted: [0.016, 0.438, 0.301, 0.218, 0.388, 0.698] → W2 = 1.739**

Strong improvement — W2 = 1.739 from W1 = 0.809. X1=0.016 (near zero
boundary) confirmed as the key signal. This is the all-time best for F7
across all 5 weeks. Point is **missing from npy** — critical discovery
from the week log system.

**Strategy:** EXPLOIT W1 boundary signal — GP found the peak in W2.

---

## F8 — EXPLOIT W1 (8D)
**n=14 | W1=9.009 | Submitted: [0.0, 0.179, 0.0, 0.071, 0.929, 0.460, 0.0, 0.541] → W2 = 9.832**

Best result yet — W2 = 9.832 is the all-time best for F8. X1=0, X3=0, X7=0
near zero boundary and X5=0.929 high are the confirmed structural signals.
The GP correctly pushed the low dims to zero and the high dims upward.

**Strategy:** EXPLOIT W1 — strong structural signal, GP performed well.

---

## Summary Table

| Fn | Dims | n  | W1 Result | W2 Result  | Change     | Strategy         |
|----|------|----|-----------|------------|------------|------------------|
| F1 | 2D   | 11 | ≈ 0       | 8.84e-7 ✅ | ≈ 0        | EXPLORE          |
| F2 | 2D   | 11 | 0.525     | 0.285      | ↓ Regress  | EXPLOIT W1       |
| F3 | 3D   | 14 | -0.0136   | -0.033     | ↓ Regress  | EXPLOIT boundary |
| F4 | 4D   | 14 | -2.627    | +0.238 ✅  | ↑ PEAK     | EXPLOIT [0.4]^4  |
| F5 | 4D   | 14 | 60.07     | 4062 ✅    | ↑ LEAP     | EXPLOIT boundary |
| F6 | 5D   | 14 | -1.339    | -0.237 ✅  | ↑ PEAK     | EXPLOIT X4↑ X5↓  |
| F7 | 6D   | 14 | 0.809     | 1.739 ✅   | ↑ PEAK     | EXPLOIT X1≈0     |
| F8 | 8D   | 14 | 9.009     | 9.832 ✅   | ↑ PEAK     | EXPLOIT boundary |

✅ = all-time best achieved this week (4 functions peaked at W2)

Note: W2 bests for F4, F5, F6, F7 are **missing from npy files** —
recovered via week log system built from submission emails.

All functions: GP + EI/UCB + Local Refinement | No classifier yet
| Jones (1998), Rasmussen & Williams (2006)

---

*Week 2 | BBO Capstone | Mike Kennelly*
