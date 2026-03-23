# Black-Box Optimisation Capstone
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London

Adaptive Bayesian Optimisation pipeline for maximising 8 unknown black-box functions simultaneously over a 13-week challenge. One submission per function per week. No access to gradients, source code, or function form.

> **Live Dashboard:** [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

---

## Non-Technical Summary

This project tackles a classic problem in engineering and science: how do you find the best settings for a system when you can't see inside it? Each week, we submit a coordinate guess for 8 mystery functions and receive back a single score — no gradients, no formula, no explanation. The pipeline uses Gaussian Processes (a probabilistic model that builds a "belief map" of the landscape) combined with a classifier ensemble to intelligently decide where to probe next. Over 13 weeks, the system learns from every result and progressively narrows in on the global maximum of each function. Think of it as a smart, self-updating treasure map that gets more accurate with every clue.

---

## The Challenge

- **Duration:** 13 weeks (Module 12 → Module 24), October 2025 – May 2026
- **Functions:** 8 unknown black-box functions (F1–F8), dimensionality 2D to 8D
- **Budget:** 1 query per function per week — every submission counts
- **Objective:** Maximise each function's output; final score based on best-found value across all 13 weeks
- **Scoring:** Submitted via Imperial College's IMP-PCMLAI Capstone Portal; results returned by email

---

## Pipeline Architecture

Each weekly notebook runs the same core pipeline:

```
Load data → Binary labels (top 30%) → Train 8 classifiers (incl. CNN-1D)
→ CV select winner → Generate 10,000 candidates → Filter by classifier
→ Fit GP (Matérn 5/2) → Compute EI + UCB → Submit top candidate
```

**Key design decisions:**
- **GP + EI** — Gaussian Process surrogate with Expected Improvement acquisition (Jones et al., 1998)
- **Dual acquisition** — EI and UCB combined; EI is primary submission driver (Srinivas et al., 2010)
- **Classifier pre-filter** — top 30% labelled class 1; best CV model from 8 classifiers filters 10,000 candidates before GP evaluation
- **CNN-1D as Model 8** — convolutional classifier added Week 6, tracking performance as sample size grows week-on-week
- **Week log override** — true best points from submission emails injected into GP training where `.npy` files have missing history
- **TuRBO sigma adaptation** — exploit sigma adjusted per-function based on weekly trajectory outcome (Eriksson et al., 2019)
- **Anisotropic sigma (F7, W7+)** — per-dimension exploitation widths validated by W7 result (+0.294 improvement); X1 dominance confirmed

---

## Repository Structure

```
capstone-project/
├── week-01/    Capstone_F1–F8_W1.ipynb   GP + EI/UCB baseline
├── week-02/    Capstone_F1–F8_W2.ipynb   Local refinement around best point
├── week-03/    Capstone_F1–F8_W3.ipynb   SVM classifier pre-filter introduced
├── week-04/    Capstone_F1–F8_W4.ipynb   Multi-model CV — 7 classifiers
├── week-05/    Capstone_F1–F8_W5.ipynb   Pipeline stabilised, week log system built
├── week-06/    Capstone_F1–F8_W6.ipynb   CNN-1D Model 8, week log overrides
├── week-07/    Capstone_F1–F8_W7.ipynb   TuRBO sigma + anisotropic F7 (confirmed W7)
├── week-08/    Capstone_F1–F8_W8.ipynb   Act on W7 results; F4 inject abandoned
├── week-09/    Capstone_F1–F8_W9.ipynb   F5/F7 new bests; F2/F3 precision recovery (current)
├── week-09 to week-13/                   Upcoming submissions
│
├── bbo_dashboard/                        Streamlit dashboard (live)
│
├── README.md                             This file
├── datasheet.md                          Dataset documentation
└── model_card.md                         Model documentation
```

Each weekly folder contains:
- `Capstone_FX_WY.ipynb` — notebook for function X, week Y
- `FX_WY_hyperparameters.json` — full hyperparameter record
- `FX_WY_run_report.txt` — submission log with GP diagnostics
- `FX_WY_*.png` — visualisations (history, classifier CV, acquisition surfaces, dashboard)
- `week_log_FX.json` — W1–WY submission history with coordinates and scores
- `BBO_WY_Strategy_Summary.docx` — strategy table for all 8 functions

---

## W9 Strategy At a Glance (Week 9 of 13)

### W8 Actual Results

| Fn | W8 Score | ATB | New Best? |
|----|----------|-----|-----------|
| F1 | 1.26e-49 | 8.84e-7 (W2) | ❌ |
| F2 | 0.4926 | 0.6497 (W5) | ❌ |
| F3 | −0.1132 | −0.000707 (W6) | ❌ |
| F4 | −0.5542 | 0.2376 (W2) | ❌ |
| **F5** | **8382.47** | **8382.47 (W8)** | ★ NEW |
| F6 | −0.4006 | −0.1727 (W6) | ❌ |
| **F7** | **2.5982** | **2.5982 (W8)** | ★ NEW |
| F8 | 9.8021 | 9.8320 (W2) | ❌ |

### W9 Strategy

| Fn | Dims | n  | W8 Result | W9 Strategy | σ W9 | TuRBO | Module | Academic Basis |
|----|------|----|-----------|-------------|------|-------|--------|----------------|
| F1 | 2D | 17 | 1.26e-49 (8th near-zero) | EXPLORE — EXTREME WIDENING | 0.45 | EXPAND | Mod 19 | Wei et al. (2022) — high-temperature sampling; maximise entropy when landscape is flat |
| F2 | 2D | 17 | 0.4926 (X2 drift) | RETURN TO W5 ATB — PRECISION LOCK | 0.008 | SHRINK | Mod 19 | Kaplan et al. (2020) — low-temperature precision; concentrate mass on confirmed best |
| F3 | 3D | 22 | −0.1132 (X3 drift) | RETURN TO W7 ATB — PRECISION LOCK | 0.015 | SHRINK | Mod 19 | Shannon (1948) — delimiting context; narrow distribution = higher information per query |
| F4 | 4D | 37 | −0.5542 (exploring) | EXPLORE — BOUNDARY CORNERS | 0.18 | EXPAND | Mod 19 | Wei et al. (2022) — high-temperature sampling; landscape unknown after inject failure |
| F5 | 4D | 27 | 8382.47 ★ NEW | PUSH X1→1.0 — LOCKED AT BOUNDARY | 0.025 | SHRINK | Mod 19 | Kaplan et al. (2020) — gradient commit; scale exploitation toward confirmed boundary |
| F6 | 5D | 27 | −0.4006 (regression) | PRECISION LOCK W6 ATB | 0.018 | SHRINK | Mod 19 | Shannon (1948) — delimiting context; pin to [0.427, 0.326, 0.598, 0.780, 0.144] |
| F7 | 6D | 37 | 2.5982 ★ NEW | ANISOTROPIC σ TIGHTEN | [0.010, 0.025×5] | SHRINK | Mod 19 | Vaswani et al. (2017) — multi-head attention; per-dimension σ mirrors per-head specialisation |
| F8 | 8D | 47 | 9.8021 (0.030 from ATB) | ANISOTROPIC σ TIGHTEN | [0.008–0.030] | SHRINK | Mod 19 | Vaswani et al. (2017) — per-dimension structure; X3/X7 near-zero dims get tightest σ |

**★** New all-time best in W8 — tighten and exploit  
**F2/F3** GP drift regressions — W9 precision lock on confirmed ATB coords  
**F7/F8** anisotropic σ: different σ per dimension mirrors multi-head attention's per-head specialisation (Vaswani et al., 2017)  
**F1/F4** high-temperature explore: maximise entropy when no exploitable signal found (Wei et al., 2022)  
**F2/F3/F5/F6** low-temperature exploit: commit compute to confirmed best region (Kaplan et al., 2020; Shannon, 1948)

---

## Hyperparameter Optimisation

All hyperparameters are documented in `FX_WY_hyperparameters.json` for every function-week combination. Key parameters:

| Parameter | Purpose | Typical range | W8 rationale |
|-----------|---------|---------------|-------------|
| `EXPLOIT_RATIO` | Fraction of 10k candidates near best point | 0.15–0.95 | 0.95 for F2 (precision lock); 0.15 for F1 (max entropy explore) |
| `EXPLOIT_SIGMA` | Gaussian σ around best point | 0.008–0.45 | F2: 0.008 (tightest); F1: 0.45 (widest); F7/F8 anisotropic |
| `UCB_KAPPA` | Exploration weight in UCB = μ + κσ | 2.0–4.0 | 4.0 for F1/F4 (EI unreliable); 2.0 for exploit functions |
| `EI_XI` | Exploration jitter in EI | 0.01–0.05 | 0.05 for F1 (flat landscape); 0.01 standard elsewhere |
| `GP_RESTARTS` | Random restarts for kernel optimisation | 5–10 | 5 standard; higher for high-dim (F7/F8) |
| `FILTER_PERCENTILE` | Classifier filter threshold | 50% | Keeps top 5,000 of 10,000 candidates for GP |

**Sigma adaptation rule (TuRBO-inspired):** if W(n) > W(n-1), SHRINK sigma; if W(n) ≤ W(n-1), EXPAND sigma. F7 uses anisotropic sigma [σ_X1, σ_X2–X6] validated by W7 result.

---

## Pipeline Evolution

| Week | Key Addition |
|------|-------------|
| W1 | GP + EI/UCB baseline |
| W2 | Local refinement around best point |
| W3 | SVM classifier pre-filter |
| W4 | Multi-model CV — 7 classifiers |
| W5 | Pipeline stabilised, week log system |
| W6 | CNN-1D Model 8, week log overrides, true best corrections |
| W7 | TuRBO sigma adaptation per-function; anisotropic sigma for F7 from CNN filter map analysis |
| W8 | Act on W7 results; F4 inject abandoned; F1 extreme explore escalation; F7 anisotropic σ confirmed and tightened |
| W9 | F5+F7 new bests confirmed; F2/F3 precision recovery; F1/F4 continued explore; F6/F8 tighten toward ATB |
| W9–W13 | Upcoming |

---

## Results (W1–W8)

Full interactive results on the [live dashboard](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app).

**W8 highlights:**
- **F5** — new best 8382.47 (+785.68 vs W7=7596.79); X1 climbing toward 1.0 boundary
- **F7** — new best 2.5982 (+0.185 vs W7=2.4134); anisotropic σ continues to deliver
- **F2/F3** — GP drift caused regressions; both returning to confirmed ATB regions in W9
- **F8** — 9.8021, still pursuing W2 ATB of 9.8320

**W7 highlights:**
- **F5** — new best 7596.79 (+1722 vs W6); X2–X4 locked at 1.0, X1 climbing toward boundary
- **F7** — new best 2.4134; anisotropic σ methodology confirmed by result
- **F3** — new best −0.00534; X1=1.0 boundary confirmed
- **F4** — W2 inject conclusively failed; strategy pivots to wide exploration
- **F8** — 9.8251, only 0.007 from all-time best (W2=9.832)

---

## Running a Notebook

1. Place `week_log_FX.json` and `fX_wY_inputs/outputs.npy` in the same folder as the notebook
2. Run all cells top to bottom (Kernel → Restart & Run All)
3. Step 14 prints the formatted submission string ready to paste into the portal

**Requirements:** `numpy`, `scikit-learn`, `matplotlib`, `scipy`, `torch`

---

## Academic Basis

| Reference | Application |
|-----------|-------------|
| Jones et al. (1998) | Expected Improvement acquisition function |
| Rasmussen & Williams (2006) | Gaussian Process fundamentals |
| Srinivas et al. (2010) | GP-UCB acquisition, exploration-exploitation balance |
| Eriksson et al. (2019) | TuRBO trust regions — sigma adaptation strategy |
| Cybenko (1989) | Universal approximation — NN classifier justification |
| Goodfellow et al. (2016) | Deep learning — CNN-1D classifier foundations |
| Vaswani et al. (2017) | Attention is all you need — anisotropic σ (F7/F8) |
| Kaplan et al. (2020) | Scaling laws — low-temperature precision sampling (F2/F3/F5/F6) |
| Shannon (1948) | Information theory — delimiting context, entropy of search distributions |
| Wei et al. (2022) | Emergent abilities — high-temperature exploration rationale (F1/F4) |
| Prompt Engineering Guide | Few-shot prompting — structured acquisition decisions |
