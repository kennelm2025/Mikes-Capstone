# BBO Capstone — Black-Box Optimisation

### Mike Kennelly · Professional Certificate in ML & AI · Imperial College London · DATA 2026 Cohort

[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen)](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)
[![Week](https://img.shields.io/badge/Week-12-blue)]()
[![Functions](https://img.shields.io/badge/Functions-8-orange)]()
[![Final](https://img.shields.io/badge/Query-Final-gold)]()

---

## Project Overview

A 13-week Black-Box Optimisation challenge. Each week one new data point is revealed per function — the goal is to predict the global maximum of 8 unknown functions using Gaussian Processes, classifier-guided candidate filtering and adaptive hyperparameter strategies.

**Live dashboard:** [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

**GitHub repository:** [github.com/kennelm2025/Mikes-Capstone](https://github.com/kennelm2025/Mikes-Capstone)

---

## Module 22 Documentation

> **Examiners:** The model card and datasheet required for Module 22 Part 3 are linked directly below.

| Document | Link |
|----------|------|
| **Model Card** — BBO pipeline W12 (Mitchell et al. 2019) | [BBO_W12_Model_Card.md](BBO_W12_Model_Card.md) |
| **Datasheet** — BBO oracle dataset W12 (Gebru et al. 2021) | [BBO_W12_Data_Card.md](BBO_W12_Data_Card.md) |
| **Live Dashboard for BBO Capstone** | **mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app** |
---

## Module 21 Documentation

| Document | Link |
|----------|------|
| **Model Card** — BBO pipeline W12 (Mitchell et al. 2019) | [BBO_W12_Model_Card.md](BBO_W12_Model_Card.md) |
| **Datasheet** — BBO oracle dataset W12 (Gebru et al. 2021) | [BBO_W12_Data_Card.md](BBO_W12_Data_Card.md) |
---

## Final Results (W1–W12)

| Fn | Dims | ATB | ATB Week | W11 Score | W12 Submitted | Strategy |
|----|------|-----|----------|-----------|---------------|----------|
| F1 | 2D | **8.968e-07** | W11 ★ | 8.968e-07 | `0.684200-0.704200` | ATB override |
| F2 | 2D | 0.6497 | W5 | 0.6090 | `0.710068-0.161630` | ATB override |
| F3 | 3D | **-0.001285** | W11 ★ | -0.001285 | `0.998126-0.621218-0.453080` | ATB override |
| F4 | 4D | 0.2376 | W2 | 0.23759 | `0.439249-0.414994-0.384687-0.397917` | ATB override |
| F5 | 4D | **8662.48** | W9 ★ | 8662.48 | `1.000000-1.000000-1.000000-1.000000` | ATB override |
| F6 | 5D | **0.0360** | W9 ★ | -0.0102 | `0.406643-0.339495-0.634775-0.769397-0.115269` | ATB override |
| F7 | 6D | **2.8501** | W11 ★ | 2.8501 | `0.179941-0.306897-0.455194-0.249116-0.295985-0.730083` | **GP pipeline** |
| F8 | 8D | 9.8320 | W2 | 9.8269 | `0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212` | ATB override |

**★** New ATB set at W11 — F1, F3, F7  
**F7 bold** = GP pipeline trusted — 6-week consecutive improvement streak, GP mu=2.857 > ATB=2.850

---

## W12 Strategy Summary

### The Final Query Decision

W12 is the last query for every function. The governing rule applied across all 8 functions:

> **Rule:** If W11 did not beat the prior ATB → submit exact ATB coordinates unchanged.  
> **Exception:** F7 only — run GP pipeline. GP mu=2.857 > ATB=2.850 → submitted GP EI candidate.  
> **Module 22 applied:** Hierarchical clustering (centroid distance, top-cluster spread, zone separation) computed across all 11 rounds to validate every submission decision.

| Fn | Strategy | ANISO sigma | Cluster Type | Override reason |
|----|----------|-------------|--------------|-----------------|
| F1 | ATB OVERRIDE — W11 coords | [0.015, 0.015] | Tight Attractor | W11 = new ATB. GP EI~0. Flat near-zero landscape. |
| F2 | ATB OVERRIDE — W5 coords | [0.012, 0.008] | ★ Two-Zone Cluster | ATB = LOW-X2 zone centroid (dist=0.012). Zone separation=0.963. |
| F3 | ATB OVERRIDE — W11 coords | [0.005, 0.020, 0.025] | Tight Attractor | W11 = new ATB. X1=0.998 boundary anchor confirmed. |
| F4 | ATB OVERRIDE — W2 coords | [0.012×4] | Isolated Attractor | Only positive in 11 weeks. W11 exact match confirms coords. |
| F5 | ATB OVERRIDE — all-ones | [0.005×4] | Corner Attractor | Tightest cluster (spread=0.007). Corner structurally confirmed. |
| F6 | ATB OVERRIDE — W9 coords | [0.015×4, 0.008] | Tight Attractor | ATB IS cluster centroid (dist=0.013). X5=0.115 threshold. |
| F7 | GP PIPELINE — EI candidate | [0.015, 0.012×4, 0.015] | ★ Trending Cluster | 6-week streak. Dynamic cluster validates GP extrapolation. |
| F8 | ATB OVERRIDE — W2 coords | [0.006, 0.015, 0.006, 0.015×4, 0.006, 0.015] | Zero-Boundary | X1=X3=X7=0 confirmed. W11 9.827 still below W2 ATB. |

---

## W12 GP Diagnostics

| Fn | CV Winner | CV Acc | GP mu | GP sigma | EI | Decision |
|----|-----------|--------|-------|----------|----|----------|
| F1 | Random Forest | ~80% | ~-0.0002 | ~0.0008 | ~0.0 | ATB override — flat landscape |
| F2 | CNN-1D | ~77% | ~0.46 | ~0.19 | ~0.013 | ATB override — GP selects wrong X2 region |
| F3 | NN-Small (16,8) | ~71% | ~-0.073 | ~0.080 | ~0.006 | ATB override — GP pulls X1 from boundary |
| F4 | Random Forest | ~88% | ~0.234 | ~2.251 | ~0.891 | ATB override — sigma=2.25 unreliable |
| F5 | Linear SVM | ~97% | ~8596 | ~37.9 | ~0.606 | ATB override — corner confirmed maximum |
| F6 | Linear SVM | ~80% | ~0.074 | ~0.149 | ~0.075 | ATB override — X5 threshold fragile |
| F7 | Logistic Regression | ~82% | **2.857** | 0.088 | 0.057 | **GP pipeline — mu=2.857 > ATB=2.850** |
| F8 | Random Forest | ~87% | ~9.800 | ~0.205 | ~0.065 | ATB override — W11 9.827 below W2 ATB |

---

## Pipeline

Each week follows a 15-step notebook pipeline. W12 adds Module 22 clustering analysis at Step 3 and the final ATB override / GP decision at Step 14:

| Step | Description |
|------|-------------|
| 0 | Config & Strategy |
| 1–3 | Imports, Load, History + **Module 22 clustering analysis** |
| 4 | Binary Labels |
| 5 / 5B | CV Model Comparison + CNN Inspection (Module 17) |
| 6–7B | Refit, CV Chart, Why-Winner |
| 8 | Candidate Generation (anisotropic sigma) |
| 9–10 | GP Fit + Acquisition Functions |
| 11 | Acquisition Curves (Global + Per-Dimension) |
| **11B** | **Ollama llama3.1 Sensitivity Interpretation (Module 20)** |
| 12A / 12B | GP Surfaces + CNN Grid Scan (2D functions only) |
| 13 / 13B | Dashboard + Week-on-Week Chart |
| **14** | **Final Submission — ATB override (F1-F6, F8) or GP pipeline (F7)** |
| 15 | Save Hyperparameter Record |

---

## Module 22 Deliverables

| File | Description |
|------|-------------|
| [week-12/BBO_W12_Model_Card.md](capstone-project/week-12/BBO_W12_Model_Card.md) | Model card — Mitchell et al. 2019 framework, W12 final |
| [week-12/BBO_W12_Data_Card.md](capstone-project/week-12/BBO_W12_Data_Card.md) | Data card — Gebru et al. 2021 framework, W12 final |
| [week-12/BBO_W11_Model_Card.md](capstone-project/week-12/BBO_W11_Model_Card.md) | Model card — W11 |
| [week-12/BBO_W11_Data_Card.md](capstone-project/week-12/BBO_W11_Data_Card.md) | Data card — W11 |
| [week-12/Capstone_F2_W12.ipynb](capstone-project/week-12/Capstone_F2_W12.ipynb) | F2 W12 notebook — Two-Zone Cluster showcase |
| [week-12/Capstone_F7_W12.ipynb](capstone-project/week-12/Capstone_F7_W12.ipynb) | F7 W12 notebook — Trending Cluster showcase |
| [week-12/W12_Submissions.txt](capstone-project/week-12/W12_Submissions.txt) | All 8 W12 submission strings |
| [week-12/BBO_W12_Strategy_Summary.docx](capstone-project/week-12/BBO_W12_Strategy_Summary.docx) | Full W12 strategy document |

---

## Module 21 Deliverables

| File | Description |
|------|-------------|
| [week-11/model_card_bbo_w11.md](capstone-project/week-11/model_card_bbo_w11.md) | Model card — Mini-lesson 21.2 framework (Mitchell et al. 2019) |
| [week-11/datasheet_bbo_w11.md](capstone-project/week-11/datasheet_bbo_w11.md) | Dataset datasheet — Gebru et al. 2021 |
| [week-11/BBO_W11_Submissions.txt](capstone-project/week-11/BBO_W11_Submissions.txt) | All 8 W11 submission strings with rationale |

---

## Academic Basis

| Reference | Application |
|-----------|-------------|
| Jones et al. (1998) | Expected Improvement acquisition function |
| Rasmussen & Williams (2006) | Gaussian Process fundamentals |
| Srinivas et al. (2010) | GP-UCB acquisition |
| Eriksson et al. (2019) | TuRBO trust regions — exploit ratio strategy |
| Cybenko (1989) | Universal approximation — NN classifier |
| Goodfellow et al. (2016) | CNN-1D foundations (Module 17) |
| Kaplan et al. (2020) | Scaling laws — diminishing returns on F5/F7 |
| Wei et al. (2022) | Emergent capabilities — F5 boundary emergence |
| Hoffmann et al. (2022) | Compute-optimal scaling — query budget framing |
| Mitchell et al. (2019) | Model Cards for Model Reporting — Module 21/22 |
| Gebru et al. (2021) | Datasheets for Datasets — Module 21/22 |
| Shannon (1948) | Information theory — uncertainty framing |
| Bender et al. (2021) | Stochastic parrots — Module 20 LLM risks |
| Ward et al. (2023) | Hierarchical clustering in optimisation landscapes — Module 22 |

---

## Repository Structure

```
Mikes-Capstone/
├── README.md                               <- This file
└── capstone-project/
    ├── week-01/ ... week-10/               <- Historical weekly notebooks and data
    ├── week-11/
    │   ├── model_card_bbo_w11.md           <- Model card (Module 21)
    │   ├── datasheet_bbo_w11.md            <- Datasheet (Module 21)
    │   ├── BBO_W11_Strategy_Summary.docx
    │   ├── BBO_W11_Final_Submission.docx
    │   ├── BBO_W11_Submissions.txt
    │   ├── Capstone_F1_W11.ipynb / _run2.ipynb
    │   ├── Capstone_F2_W11.ipynb / _run2.ipynb
    │   ├── Capstone_F3_W11.ipynb
    │   ├── Capstone_F4_W11.ipynb / _run2.ipynb
    │   ├── Capstone_F5_W11.ipynb / _run2.ipynb
    │   ├── Capstone_F6_W11.ipynb / _run2.ipynb
    │   ├── Capstone_F7_W11.ipynb
    │   └── Capstone_F8_W11.ipynb
    └── week-12/
        ├── BBO_W12_Model_Card.md           <- Model card (Module 22)
        ├── BBO_W12_Data_Card.md            <- Data card (Module 22)
        ├── BBO_W12_Strategy_Summary.docx
        ├── W12_Submissions.txt
        ├── Capstone_F1_W12.ipynb ... Capstone_F8_W12.ipynb
        ├── f1_w12_inputs.npy ... f8_w12_outputs.npy
        └── README.md
```

---

*W1–W12 · BBO Optimisation · Imperial College London · DATA 2026 Cohort*
