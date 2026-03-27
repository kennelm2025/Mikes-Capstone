# BBO Capstone — Black-Box Optimisation
### Mike Kennelly · Professional Certificate in ML & AI · Imperial College London · DATA 2026 Cohort

[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen)](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)
[![Week](https://img.shields.io/badge/Week-10-blue)]()
[![Functions](https://img.shields.io/badge/Functions-8-orange)]()

---

## Project Overview

A 13-week Black-Box Optimisation challenge. Each week one new data point is revealed per function — the goal is to predict the global maximum of 8 unknown functions using Gaussian Processes, classifier-guided candidate filtering and adaptive hyperparameter strategies.

**Live dashboard:** [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

---

## Results (W1–W10)

| Fn | Dims | ATB | ATB Week | W9 Score | W10 Submitted | GP Prediction |
|----|------|-----|----------|----------|---------------|---------------|
| F1 | 2D | 8.84e-7 | W2 | -2.45e-183 | `0.911939-0.661887` | mu=-0.000084 |
| F2 | 2D | 0.6497 | W5 | 0.6497 (=ATB) | `0.640219-0.040241` | mu=0.461 |
| F3 | 3D | -0.000707 | W6 | -0.01348 | `0.929491-0.684416-0.621434` | mu=-0.040 |
| F4 | 4D | 0.2376 | W2 | -1.4047 | `0.476870-0.494027-0.420410-0.346682` | mu=-0.110 |
| F5 | 4D | **8662.48** | W9 ★ | 8662.48 | `1.000000-1.000000-0.989930-1.000000` | mu=8604 |
| F6 | 5D | **0.0360** | W9 ★ | 0.0360 | `0.389852-0.333817-0.652408-0.764251-0.078672` | **mu=0.141 (+0.105)** |
| F7 | 6D | **2.5982** | W8 | 2.5968 | `0.125051-0.359133-0.441354-0.282350-0.330896-0.702888` | **mu=2.690 (+0.091)** |
| F8 | 8D | 9.832 | W2 | 9.8115 | `0.043512-0.408722-0.007093-0.181174-0.420743-0.529348-0.164598-0.795731` | **mu=9.895 (+0.070)** |

**★** New all-time best in W9 — F5, F6  
**Bold GP prediction** = GP predicts new best (F6, F7, F8) — awaiting portal results

---

## W10 Strategy Summary

| Fn | Strategy | ANISO sigma | Ratio | κ | Module 20 Ollama |
|----|----------|-------------|-------|---|-----------------|
| F1 | EXPLORE — NEAR-UNIFORM RANDOM | 0.45 isotropic | 0.10 | 4.0 | 3-run plan: explore W10, return to [0.684,0.704] W11-W12 |
| F2 | RETURN TO ATB — ANISO X2 LOCK | [0.012, 0.007] | 0.95 | 2.0 | 4-run unanimous — X2=0.007 lock LOW X2 region |
| F3 | EXPLOIT W6 ATB — ANISO X1 | [0.010, 0.018, 0.018] | 0.92 | 2.0 | 4-run unanimous — X1=0.010 recover gradient |
| F4 | RETURN TO W2 ATB — ANISO | [0.060, 0.050, 0.100, 0.070] | 0.60 | 3.0 | 3-run — X1/X4 unanimous, X2/X3 non-stationary |
| F5 | EXPLOIT BOUNDARY — ANISO PROBE | [0.010, 0.015, 0.025, 0.010] | 0.92 | 2.0 | 4-run unanimous — X1/X4 tight, X3 free probe |
| F6 | EXPLOIT W9 ATB — ANISO LOCK | [0.015, 0.012, 0.010, 0.020, 0.013] | 0.92 | 2.0 | 6-run converged — X3 dominant (sens 3.11) |
| F7 | EXPLOIT W8 ATB — ANISO X3 | [0.010, 0.030, 0.018, 0.020, 0.020, 0.030] | 0.92 | 2.5 | 4-run unanimous — X3=0.018 strongest consensus |
| F8 | EXPLOIT ATB — ANISO ZERO-BOUNDARY | [0.006, 0.020, 0.006, 0.020, 0.025, 0.030, 0.006, 0.020] | 0.92 | 2.0 | 4-run iterative — X4/X5/X6 unanimous |

### Module 20 — Ollama llama3.1 Integration (W10)

W10 deploys Ollama llama3.1 as a parameter recommendation engine across all 8 functions (Step 11B). GP sensitivity scores and full submission history sent to LLM; per-dimension sigma values returned.

**Key findings:**
- **F2**: X2=0.007 unanimous 4/4 — most consistent result. Two-region context produced zero divergence.
- **F3**: X1=0.010 unanimous 4/4 — full history prompt identified W1-W6 gradient, flagged W9 drift as regression.
- **F7**: X3=0.018 unanimous 4/4 — strongest anisotropic consensus in the capstone.
- **F4**: X2/X3 flipped between runs — non-stationary landscapes produce unreliable LLM recommendations when GP sensitivity shifts.
- **Lesson**: Prompt context quality determines recommendation reliability.

---

## W10 GP Diagnostics

| Fn | CV Winner | CV Acc | GP mu | GP sigma | EI | delta vs ATB |
|----|-----------|--------|-------|----------|----|-------------|
| F1 | Random Forest | 77.8% | -0.000084 | 0.000686 | 0.000000 | -0.000084 |
| F2 | CNN-1D | 74.6% | 0.461 | 0.185 | 0.013 | -0.188 |
| F3 | Decision Tree | 82.1% | -0.040 | 0.065 | 0.008 | -0.040 |
| F4 | Random Forest | 86.8% | -0.110 | 3.129 | 1.073 | -0.347 |
| F5 | Linear SVM | 100.0% | 8604 | 39.6 | 1.232 | -58.4 |
| F6 | Random Forest | 82.1% | **0.141** | 0.038 | 0.095 | **+0.105** |
| F7 | Linear SVM | 73.9% | **2.690** | 0.050 | 0.082 | **+0.091** |
| F8 | CNN-1D | 89.3% | **9.895** | 0.161 | 0.099 | **+0.070** |

---

## Pipeline

Each week follows a 15-step notebook pipeline including Step 11B (Ollama llama3.1) added in W10:

| Step | Description |
|------|-------------|
| 0 | Config & Strategy |
| 1-3 | Imports, Load, History |
| 4 | Binary Labels |
| 5/5B | CV Model Comparison + CNN Inspection |
| 6-7B | Refit, CV Chart, Why-Winner |
| 8 | Candidate Generation (anisotropic sigma) |
| 9-10 | GP Fit + Acquisition Functions |
| 11 | Acquisition Curves |
| **11B** | **Ollama llama3.1 Sensitivity Interpretation (Module 20)** |
| 12A/12B | GP Surfaces + CNN Grid Scan |
| 13/13B | Dashboard + Week-on-Week Chart |
| 14 | Final Formatted Submission |
| 15 | Save Hyperparameter Record |

---

## Academic Basis

| Reference | Application |
|-----------|-------------|
| Jones et al. (1998) | Expected Improvement acquisition function |
| Rasmussen & Williams (2006) | Gaussian Process fundamentals |
| Srinivas et al. (2010) | GP-UCB acquisition |
| Eriksson et al. (2019) | TuRBO trust regions |
| Cybenko (1989) | Universal approximation — NN classifier |
| Goodfellow et al. (2016) | CNN-1D foundations |
| Vaswani et al. (2017) | Anisotropic sigma (F6/F7/F8) |
| Kaplan et al. (2020) | Low-temperature precision sampling (F2/F3/F5) |
| Shannon (1948) | Information theory — delimiting context |
| Wei et al. (2022) | High-temperature exploration (F1) |
| Hoffmann et al. (2022) | Chinchilla — compute-optimal scaling |
| Bender et al. (2021) | Stochastic parrots — Module 20 risks |
| Demirci et al. (2023) | LLM labour market — Module 20 |

---

*W1–W10 · BBO Optimisation · Imperial College London · DATA 2026 Cohort*
