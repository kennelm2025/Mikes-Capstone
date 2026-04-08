# BBO Capstone — Black-Box Optimisation
### Mike Kennelly · Professional Certificate in ML & AI · Imperial College London · DATA 2026 Cohort

[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen)](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)
[![Week](https://img.shields.io/badge/Week-11-blue)]()
[![Functions](https://img.shields.io/badge/Functions-8-orange)]()

---

## Project Overview

A 13-week Black-Box Optimisation challenge. Each week one new data point is revealed per function — the goal is to predict the global maximum of 8 unknown functions using Gaussian Processes, classifier-guided candidate filtering and adaptive hyperparameter strategies.

**Live dashboard:** [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

**GitHub repository:** [github.com/kennelm2025/Mikes-Capstone](https://github.com/kennelm2025/Mikes-Capstone)

---

## Module 21 Documentation

| Document | Link |
|----------|------|
| **Model Card** — BBO pipeline (Mitchell et al. 2019 framework) | [capstone-project/week-11/model_card_bbo_w11.md](capstone-project/week-11/model_card_bbo_w11.md) |
| **Datasheet** — BBO oracle dataset (Gebru et al. 2021 framework) | [capstone-project/week-11/datasheet_bbo_w11.md](capstone-project/week-11/datasheet_bbo_w11.md) |

---

## Results (W1–W11)

| Fn | Dims | ATB | ATB Week | W10 Score | W11 Submitted | Strategy |
|----|------|-----|----------|-----------|---------------|----------|
| F1 | 2D | 8.84e-7 | W2 | 4.11e-58 | `0.684200-0.704200` | ATB override |
| F2 | 2D | 0.6497 | W9 | 0.1636 | `0.710068-0.161630` | ATB override |
| F3 | 3D | -0.000707 | W6 | -0.090154 | `0.998126-0.621218-0.453080` | ATB override |
| F4 | 4D | 0.2376 | W2 | -1.8014 | `0.439249-0.414994-0.384687-0.397917` | ATB override |
| F5 | 4D | **8662.48** | W9 ★ | 8471.33 | `1.000000-1.000000-1.000000-1.000000` | ATB override |
| F6 | 5D | **0.0360** | W9 ★ | -0.1443 | `0.406643-0.339495-0.634775-0.769397-0.115269` | ATB override |
| F7 | 6D | **2.7201** | W10 ★ | 2.7201 | `0.165978-0.338682-0.444076-0.255770-0.300940-0.704355` | **GP pipeline** |
| F8 | 8D | 9.8320 | W2 | 9.8013 | `0.031481-0.311811-0.010280-0.180196-0.397721-0.420494-0.162029-0.787262` | GP Run 1 (submitted) |

**★** All-time best still standing — F5 (W9), F6 (W9), F7 (W10)
**F7 bold** = GP pipeline trusted — 5-week consecutive improvement streak, GP mu exceeds ATB

---

## W11 Strategy Summary

### The ATB Override Decision

W11 introduces a formal override rule: when GP training R²=1.0 AND fewer than 5 positive class labels exist in the binary classifier, the GP surrogate is memorising rather than generalising and cannot be trusted. All eight functions returned R²=1.0 in the W11 fit. Seven functions triggered the override; F7 passed (5-week improvement streak, GP mu=2.767 > ATB=2.720).

| Fn | Strategy | ANISO sigma | Ratio | κ | Override reason |
|----|----------|-------------|-------|---|----------------|
| F1 | ATB OVERRIDE — W2 coords | N/A | N/A | N/A | 10 consecutive near-zero; GP mu far below ATB |
| F2 | ATB OVERRIDE — W9 coords | N/A | N/A | N/A | GP R²=1.0; only 3 positives |
| F3 | ATB OVERRIDE — W6 coords | [0.005, 0.020, 0.025] | 0.92 | 2.0 | GP output X1=0.266 — wrong direction |
| F4 | ATB OVERRIDE — W2 coords | N/A | N/A | N/A | GP within 0.003 of ATB; known coords safer |
| F5 | ATB OVERRIDE — all-ones | N/A | N/A | N/A | Structurally maximised at corner [1,1,1,1] |
| F6 | ATB OVERRIDE — W9 coords | N/A | N/A | N/A | GP R²=1.0; only 3 positives |
| F7 | GP PIPELINE — EI candidate | [0.010, 0.030, 0.018, 0.020, 0.020, 0.030] | 0.92 | 2.0 | 5-week streak; GP mu=2.767 > ATB=2.720 |
| F8 | SUBMITTED — GP Run 1 | [0.006, 0.020, 0.006, 0.020, 0.025, 0.030, 0.006, 0.020] | 0.92 | 2.0 | Highest mu across 3 GP runs |

---

## W11 GP Diagnostics

| Fn | CV Winner | CV Acc | GP mu | GP sigma | EI | Decision |
|----|-----------|--------|-------|----------|----|----------|
| F1 | Random Forest | 79.4% | -0.000187 | 0.000819 | 0.000000 | ATB override — mu far below ATB |
| F2 | Random Forest | 84.9% | 0.661 | 0.070 | 0.029 | ATB override — R²=1.0, 3 positives |
| F3 | NN-Small (16,8) | 70.8% | -0.073 | 0.080 | 0.006 | ATB override — X1=0.266 wrong direction |
| F4 | Random Forest | 87.5% | 0.234 | 2.251 | 0.891 | ATB override — sigma=2.25 unreliable |
| F5 | Linear SVM | 96.9% | 8595.95 | 37.92 | 0.606 | ATB override — all-ones confirmed maximum |
| F6 | Linear SVM | 79.5% | **0.074** | 0.149 | 0.075 | ATB override — R²=1.0 despite positive delta |
| F7 | Logistic Regression | 82.1% | **2.767** | 0.088 | 0.057 | **GP pipeline — mu=2.767 > ATB=2.720** |
| F8 | Random Forest | 87.3% | 9.800 | 0.205 | 0.065 | Submitted — GP Run 1 highest mu |

---

## W12 Plan (Final Query)

**General rule:** If W11 portal result improves on ATB → exploit around new best with tight ANISO_SIGMA. If W11 does not improve → submit exact ATB coordinates. F7: run GP pipeline on W11 result before deciding. F5: always all-ones.

| Fn | Default W12 String | Decision Rule |
|----|-------------------|---------------|
| F1 | `0.684200-0.704200` | If W11 > 8.84e-07 → exploit. Else → exact ATB. |
| F2 | `0.710068-0.161630` | If W11 > 0.6497 → exploit. Else → exact ATB. |
| F3 | `0.998126-0.621218-0.453080` | If W11 > -0.000707 → exploit. Else → exact ATB. |
| F4 | `0.439249-0.414994-0.384687-0.397917` | If W11 > 0.2376 → exploit. Else → exact ATB. |
| F5 | `1.000000-1.000000-1.000000-1.000000` | Always all-ones — no decision needed. |
| F6 | `0.406643-0.339495-0.634775-0.769397-0.115269` | If W11 > 0.0360 → exploit. Else → exact ATB. |
| F7 | Run GP on W11 result | W11 result → retrain GP → generate W12 EI candidate. |
| F8 | `0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212` | If W11 > 9.8320 → exploit. Else → exact W2 ATB. |

---

## Pipeline

Each week follows a 15-step notebook pipeline. W11 adds the ATB override check at Step 14:

| Step | Description |
|------|-------------|
| 0 | Config & Strategy |
| 1–3 | Imports, Load, History |
| 4 | Binary Labels |
| 5/5B | CV Model Comparison + CNN Inspection |
| 6–7B | Refit, CV Chart, Why-Winner |
| 8 | Candidate Generation (anisotropic sigma) |
| 9–10 | GP Fit + Acquisition Functions |
| 11 | Acquisition Curves (Global + Per-Dimension) |
| **11B** | **Ollama llama3.1 Sensitivity Interpretation (Module 20)** |
| 12A/12B | GP Surfaces + CNN Grid Scan (N/A for 3D+) |
| 13/13B | Dashboard + Week-on-Week Chart |
| **14** | **Final Submission + ATB Override Decision** |
| 15 | Save Hyperparameter Record |

---

## Module 21 Deliverables

| File | Description | Location |
|------|-------------|----------|
| [`model_card_bbo_w11.md`](capstone-project/week-11/model_card_bbo_w11.md) | Model card — Mini-lesson 21.2 framework | `/week-11/` |
| [`datasheet_bbo_w11.md`](capstone-project/week-11/datasheet_bbo_w11.md) | Dataset datasheet — Gebru et al. 2021 | `/week-11/` |
| [`capstone_21_1_reflection.md`](capstone-project/week-11/capstone_21_1_reflection.md) | W11 strategy reflection (700 words) | `/week-11/` |
| [`capstone_21_2_datasheet_modelcard.md`](capstone-project/week-11/capstone_21_2_datasheet_modelcard.md) | Combined capstone datasheet + model card | `/week-11/` |
| [`discussion_21_1_datasheet_pima.md`](capstone-project/week-11/discussion_21_1_datasheet_pima.md) | Discussion board — Pima datasheet | `/week-11/` |
| [`discussion_21_2_model_card.md`](capstone-project/week-11/discussion_21_2_model_card.md) | Discussion board — model card analysis | `/week-11/` |
| [`discussion_21_3_tradeoffs.md`](capstone-project/week-11/discussion_21_3_tradeoffs.md) | Discussion board — explainability trade-offs | `/week-11/` |
| [`BBO_W11_Submissions.txt`](capstone-project/week-11/BBO_W11_Submissions.txt) | All 8 W11 submission strings with rationale | `/week-11/` |

---

## Academic Basis

| Reference | Application |
|-----------|-------------|
| Jones et al. (1998) | Expected Improvement acquisition function |
| Rasmussen & Williams (2006) | Gaussian Process fundamentals |
| Srinivas et al. (2010) | GP-UCB acquisition |
| Eriksson et al. (2019) | TuRBO trust regions — exploit ratio strategy |
| Cybenko (1989) | Universal approximation — NN classifier |
| Goodfellow et al. (2016) | CNN-1D foundations |
| Kaplan et al. (2020) | Scaling laws — diminishing returns on F5/F7 |
| Wei et al. (2022) | Emergent capabilities — F5 boundary emergence |
| Hoffmann et al. (2022) | Compute-optimal scaling — query budget framing |
| Mitchell et al. (2019) | Model Cards for Model Reporting — Module 21 |
| Gebru et al. (2021) | Datasheets for Datasets — Module 21 |
| Shannon (1948) | Information theory — uncertainty framing |
| Bender et al. (2021) | Stochastic parrots — Module 20 LLM risks |

---

## Repository Structure

```
capstone-project/
├── README.md                               ← This file
├── week-01/ … week-10/                     ← Historical weekly notebooks and data
└── week-11/
    ├── model_card_bbo_w11.md               ← Model card (Module 21)
    ├── datasheet_bbo_w11.md                ← Datasheet (Module 21)
    ├── capstone_21_1_reflection.md
    ├── capstone_21_2_datasheet_modelcard.md
    ├── discussion_21_1_datasheet_pima.md
    ├── discussion_21_2_model_card.md
    ├── discussion_21_3_tradeoffs.md
    ├── BBO_W11_Submissions.txt
    ├── Capstone_F1_W11_run2.ipynb
    ├── Capstone_F2_W11_run2.ipynb
    ├── Capstone_F3_W11.ipynb
    ├── Capstone_F4_W11_run2.ipynb
    ├── Capstone_F5_W11_run2.ipynb
    ├── Capstone_F6_W11_run2.ipynb
    ├── Capstone_F7_W11.ipynb
    ├── Capstone_F8_W11.ipynb
    ├── f1_w11_inputs.npy … f8_w11_inputs.npy
    └── f1_w11_outputs.npy … f8_w11_outputs.npy
```

---

*W1–W11 · BBO Optimisation · Imperial College London · DATA 2026 Cohort*
