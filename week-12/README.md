# BBO Capstone — Week 12 Submission

### Mike Kennelly · Professional Certificate in ML & AI · Imperial College London · DATA 2026 Cohort

[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen)](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)
[![Week](https://img.shields.io/badge/Week-12-blue)]()
[![Functions](https://img.shields.io/badge/Functions-8-orange)]()
[![Final](https://img.shields.io/badge/Query-Final-gold)]()

---

## What's in this folder

This is the **Week 12** submission folder.

**Parent repository:** [github.com/kennelm2025/Mikes-Capstone](https://github.com/kennelm2025/Mikes-Capstone)  
**Live dashboard:** [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

---

## Project Overview

A 13-week Black-Box Optimisation challenge. Each week one new data point is revealed per function — the goal is to predict the global maximum of 8 unknown functions using Gaussian Processes, classifier-guided candidate filtering and adaptive hyperparameter strategies.

---

## Module 22 Documentation

> **Examiners:** The model card and datasheet required for Module 22 are linked directly below.

| Document | Link |
|----------|------|
| **Model Card** — BBO pipeline W12 (Mitchell et al. 2019) | [BBO_W12_Model_Card.md](BBO_W12_Model_Card.md) |
| **Datasheet** — BBO oracle dataset W12 (Gebru et al. 2021) | [BBO_W12_Data_Card.md](BBO_W12_Data_Card.md) |
| **Live Dashboard for BBO Capstone** | [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app) |

---

## Results (W1–W12)

| Fn | Dims | ATB | ATB Week | W11 Score | W11 Status | W12 Submitted | Strategy |
|----|------|-----|----------|-----------|------------|---------------|----------|
| F1 | 2D | **8.968e-07** | W11 ★ | 8.968e-07 | NEW ATB | `0.684200-0.704200` | ATB override |
| F2 | 2D | 0.6497 | W5 | 0.6090 | Regressed | `0.710068-0.161630` | ATB override |
| F3 | 3D | **-0.001285** | W11 ★ | -0.001285 | NEW ATB | `0.998126-0.621218-0.453080` | ATB override |
| F4 | 4D | 0.23759 | W2 | 0.23759 | Exact match | `0.439249-0.414994-0.384687-0.397917` | ATB override |
| F5 | 4D | **8662.48** | W9 | 8662.48 | Exact match | `1.000000-1.000000-1.000000-1.000000` | ATB override |
| F6 | 5D | 0.03602 | W9 | -0.01024 | Regressed | `0.406643-0.339495-0.634775-0.769397-0.115269` | ATB override |
| F7 | 6D | **2.8501** | W11 ★ | 2.8501 | NEW ATB | `0.165978-0.338682-0.444076-0.255770-0.300940-0.704355` | **GP pipeline** |
| F8 | 8D | 9.8320 | W2 | 9.8269 | Regressed | `0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212` | ATB override |

**★** New ATB set at W11 — F1, F3, F7  
**F7 bold** = GP pipeline trusted — 6-week consecutive improvement streak W6–W11, dynamic cluster confirmed by Module 22 analysis

---

## W11 Results Summary

| Fn | W10 Score | W11 Submitted | W11 Result | Delta | Outcome |
|----|-----------|---------------|------------|-------|---------|
| F1 | 4.109e-58 | `0.684200-0.704200` | **8.968e-07** | +8.97e-07 | NEW ATB ✓ |
| F2 | 0.163649 | `0.710068-0.161630` | 0.6090 | +0.445 | Regressed vs W5 ATB |
| F3 | -0.090154 | `0.998126-0.621218-0.453080` | **-0.001285** | +0.089 | NEW ATB ✓ |
| F4 | -1.801384 | `0.439249-0.414994-0.384687-0.397917` | 0.23759 | +2.039 | Exact ATB match ✓ |
| F5 | 8471.330 | `1.000000-1.000000-1.000000-1.000000` | 8662.48 | +191.2 | Exact ATB match ✓ |
| F6 | -0.144285 | `0.406643-0.339495-0.634775-0.769397-0.115269` | -0.01024 | +0.134 | Regressed vs W9 ATB |
| F7 | 2.7201 | `0.165978-0.338682-0.444076-0.255770-0.300940-0.704355` | **2.8501** | +0.130 | NEW ATB ✓ (6th consec.) |
| F8 | 9.8013 | `0.031481-0.311811-0.010280-0.180196-0.397721-0.420494-0.162029-0.787262` | 9.8269 | +0.026 | Regressed vs W2 ATB |

---

## W12 Strategy Summary

### The Final Query Decision Rule

W12 is the last query for every function. The governing rule applied across all 8 functions:

> **Rule:** If W11 did not beat the prior ATB → submit exact ATB coordinates unchanged.  
> **Exception:** F7 only — run GP pipeline on W12 npy. If GP mu > 2.8501 → submit GP EI candidate. If not → submit W11 ATB fallback.  
> **Rationale:** GP surrogates with R²=1.0 (memorising) provide no trustworthy gradient signal. Exact ATB replication dominates GP exploration at the final query for all non-trending functions.

### Module 22 Clustering — Validation of W12 Decisions

Module 22 hierarchical clustering was applied to the full 11-round submission history to formally validate the W12 strategy. Two functions are featured as primary showcases:

**F2 — Two-Zone Hierarchical Clustering (primary showcase)**

Complete linkage clustering on Euclidean distance in [0,1]² cleanly separates two basins:

| Zone | Weeks | X2 Region | Centroid | Mean Output |
|------|-------|-----------|----------|-------------|
| Zone A — HIGH X2 | W1, W2, W3, W4, W9 | X2 > 0.50 | [0.733, 0.904] | 0.225 |
| Zone B — LOW X2 | W5, W6, W7, W8, W10, W11 | X2 ≤ 0.50 | [0.702, 0.118] | 0.506 |

Inter-zone distance = 0.963. Zone B spread = 0.025 (tight attractor). ATB (W5) sits at distance 0.012 from Zone B centroid — the ATB IS the cluster centroid. Submitting the ATB coordinates is equivalent to submitting the cluster centroid.

**F7 — Trending / Dynamic Cluster (secondary showcase)**

W6–W11 form a directional cluster (intra-spread = 0.066, consistent step direction) rather than a static attractor. This is the formal justification for trusting the GP for F7 when all others are overridden.

| Week | Output | Step (6D) |
|------|--------|-----------|
| W6 | 2.119 | — |
| W7 | 2.413 | 0.061 |
| W8 | 2.598 | 0.049 |
| W9 | 2.597 | 0.001 |
| W10 | 2.720 | 0.042 |
| W11 | 2.850 | 0.061 |

### W12 Per-Function Settings

| Fn | Strategy | ANISO sigma | EXPLOIT_RATIO | Cluster Type | Override rationale |
|----|----------|-------------|---------------|--------------|--------------------|
| F1 | ATB OVERRIDE — W11 coords | [0.015, 0.015] | 0.85 | Tight Attractor | W11 = new ATB. GP EI~0. Flat near-zero landscape. |
| F2 | ATB OVERRIDE — W5 coords | [0.012, 0.008] | 0.92 | ★ Two-Zone Cluster | ATB = LOW-X2 centroid (dist=0.012). Zone separation confirmed. |
| F3 | ATB OVERRIDE — W11 coords | [0.005, 0.020, 0.025] | 0.92 | Tight Attractor | W11 = new ATB. X1=0.998 boundary anchor confirmed. |
| F4 | ATB OVERRIDE — W2 coords | [0.012×4] | 0.92 | Isolated Attractor | Only positive in 11 weeks. W11 exact match confirms coords. |
| F5 | ATB OVERRIDE — corner | [0.005×4] | 0.95 | Corner Attractor | [1,1,1,1] structural maximum — tightest cluster (spread=0.007). |
| F6 | ATB OVERRIDE — W9 coords | [0.015×4, 0.008] | 0.92 | Tight Attractor | Only positive in 11 weeks. X5=0.115 threshold confirmed. |
| F7 | GP PIPELINE | [0.015, 0.012×4, 0.015] | 0.92 | ★ Trending Cluster | 6 consecutive ATBs. Dynamic cluster validates GP extrapolation. |
| F8 | ATB OVERRIDE — W2 coords | [0.006, 0.015, 0.006, 0.015×4, 0.006, 0.015] | 0.95 | Zero-Boundary | X1=X3=X7=0 structure confirmed. W11 9.827 still below W2 ATB. |

---

## W12 GP Diagnostics

| Fn | CV Winner | CV Acc | GP mu | GP sigma | EI | Decision |
|----|-----------|--------|-------|----------|----|----------|
| F1 | Random Forest | ~80% | ~-0.0002 | ~0.0008 | ~0.0 | ATB override — flat landscape, EI~0 |
| F2 | CNN-1D | ~77% | ~0.46 | ~0.19 | ~0.013 | ATB override — GP selects wrong X2 region |
| F3 | NN-Small | ~71% | ~-0.073 | ~0.080 | ~0.006 | ATB override — GP pulls X1 from boundary |
| F4 | Random Forest | ~88% | ~0.234 | ~2.251 | ~0.891 | ATB override — sigma=2.25 unreliable |
| F5 | Linear SVM | ~97% | ~8596 | ~37.9 | ~0.606 | ATB override — corner confirmed maximum |
| F6 | Linear SVM | ~80% | ~0.074 | ~0.149 | ~0.075 | ATB override — R²=1.0, X5 threshold fragile |
| F7 | Logistic Reg. | ~82% | Run GP on W12 npy | — | — | **GP pipeline — check mu > 2.8501** |
| F8 | Random Forest | ~87% | ~9.800 | ~0.205 | ~0.065 | ATB override — W11 9.827 below W2 ATB |

*F7 W12 GP values depend on W12 npy run — check notebook Step 14 output before submitting.*

---

## Pipeline

Each week follows a 15-step notebook pipeline. W12 adds the Module 22 clustering markdown at Step 3 and the final ATB override / GP decision at Step 14:

| Step | Description |
|------|-------------|
| 0 | Config & Strategy — W12 ATB coords, ANISO_SIGMA, cluster type documented |
| 1–3 | Imports, Load, History + **Module 22 clustering analysis in Step 3 markdown** |
| 4 | Binary Labels (top 30%) |
| 5 / 5B | CV Model Comparison (8 classifiers) + CNN-1D Inspection (Module 17) |
| 6–7B | Refit, CV Chart, Why-Winner |
| 8 | Candidate Generation (anisotropic sigma, exploit/explore split) |
| 9–10 | GP Fit (Matern v=5/2) + Acquisition Functions (EI + UCB) |
| 11 | Acquisition Curves — Global + Per-Dimension sensitivity |
| 11B | Ollama llama3.1 Sensitivity Interpretation (Module 20) |
| 12A / 12B | GP Surfaces + CNN Grid Scan (2D functions only) |
| 13 / 13B | Dashboard + Week-on-Week Chart |
| **14** | **Final Submission — ATB override (F1-F6, F8) or GP pipeline (F7)** |
| 15 | Save Hyperparameter Record (JSON + TXT, encoding='utf-8') |

---

## Module 22 Deliverables (this folder)

| File | Description |
|------|-------------|
| [BBO_W12_Model_Card.md](BBO_W12_Model_Card.md) | Model card — Mitchell et al. 2019 framework, W12 final |
| [BBO_W12_Data_Card.md](BBO_W12_Data_Card.md) | Data card — Gebru et al. 2021 framework, W12 final |
| [Capstone_F1_W12.ipynb](Capstone_F1_W12.ipynb) | F1 W12 notebook — Tight Attractor, ATB override |
| [Capstone_F2_W12.ipynb](Capstone_F2_W12.ipynb) | F2 W12 notebook — **Two-Zone Cluster**, ATB override |
| [Capstone_F3_W12.ipynb](Capstone_F3_W12.ipynb) | F3 W12 notebook — Tight Attractor, ATB override |
| [Capstone_F4_W12.ipynb](Capstone_F4_W12.ipynb) | F4 W12 notebook — Isolated Attractor, ATB override |
| [Capstone_F5_W12.ipynb](Capstone_F5_W12.ipynb) | F5 W12 notebook — Corner Attractor, ATB override |
| [Capstone_F6_W12.ipynb](Capstone_F6_W12.ipynb) | F6 W12 notebook — Tight Attractor, ATB override |
| [Capstone_F7_W12.ipynb](Capstone_F7_W12.ipynb) | F7 W12 notebook — **Trending Cluster**, GP pipeline |
| [Capstone_F8_W12.ipynb](Capstone_F8_W12.ipynb) | F8 W12 notebook — Zero-Boundary, ATB override |

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
| Kaplan et al. (2020) | Scaling laws — diminishing returns framing |
| Wei et al. (2022) | Emergent capabilities — F5 corner emergence |
| Hoffmann et al. (2022) | Compute-optimal scaling — query budget framing |
| Mitchell et al. (2019) | Model Cards for Model Reporting — Module 21/22 |
| Gebru et al. (2021) | Datasheets for Datasets — Module 21/22 |
| Shannon (1948) | Information theory — uncertainty framing |
| Bender et al. (2021) | Stochastic parrots — Module 20 LLM risks |
| Ward et al. (2023) | Hierarchical clustering in optimisation landscapes — Module 22 |

---

## Files in this folder

```
week-12/
├── README.md                                   <- This file
├── BBO_W12_Model_Card.md                       <- Model card (Module 22)
├── BBO_W12_Data_Card.md                        <- Data card (Module 22)
├── Capstone_F1_W12.ipynb                       <- Tight Attractor — ATB override
├── Capstone_F2_W12.ipynb                       <- Two-Zone Cluster — ATB override
├── Capstone_F3_W12.ipynb                       <- Tight Attractor — ATB override
├── Capstone_F4_W12.ipynb                       <- Isolated Attractor — ATB override
├── Capstone_F5_W12.ipynb                       <- Corner Attractor — ATB override
├── Capstone_F6_W12.ipynb                       <- Tight Attractor — ATB override
├── Capstone_F7_W12.ipynb                       <- Trending Cluster — GP pipeline
├── Capstone_F8_W12.ipynb                       <- Zero-Boundary — ATB override
├── f1_w12_inputs.npy / f1_w12_outputs.npy
├── f2_w12_inputs.npy / f2_w12_outputs.npy
├── f3_w12_inputs.npy / f3_w12_outputs.npy
├── f4_w12_inputs.npy / f4_w12_outputs.npy
├── f5_w12_inputs.npy / f5_w12_outputs.npy
├── f6_w12_inputs.npy / f6_w12_outputs.npy
├── f7_w12_inputs.npy / f7_w12_outputs.npy
└── f8_w12_inputs.npy / f8_w12_outputs.npy
```

---

*W1–W12 · BBO Optimisation · Imperial College London · DATA 2026 Cohort*
