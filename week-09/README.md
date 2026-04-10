# BBO Capstone — Black-Box Optimisation
### Mike Kennelly · Professional Certificate in ML & AI · Imperial College London · DATA 2026 Cohort

[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen)](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)
[![Week](https://img.shields.io/badge/Week-9-blue)]()
[![Functions](https://img.shields.io/badge/Functions-8-orange)]()

---

## Project Overview

A 13-week Black-Box Optimisation challenge. Each week one new data point is revealed per function — the goal is to predict the global maximum of 8 unknown functions using Gaussian Processes, classifier-guided candidate filtering and adaptive hyperparameter strategies.

**Live dashboard:** [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

---

## Results (W1–W9)

| Fn | Dims | Objective | All-Time Best | Week | W9 Score | W9 Strategy |
|----|------|-----------|--------------|------|----------|-------------|
| F1 | 2D | MAXIMISE | 8.84e-7 | W2 | TBD | Extreme explore σ=0.45 |
| F2 | 2D | MAXIMISE | 0.6497 | W5 | TBD | Return to W5 ATB — precision lock |
| F3 | 3D | MAXIMISE | -0.000707 | W7 | TBD | Return to W7 ATB — precision lock |
| F4 | 4D | MAXIMISE | 0.2376 | W2 | TBD | Shannon entropy — hypercube sweep |
| F5 | 4D | MAXIMISE | **8382.47** | W8 | TBD | Push X1→1.0 boundary lock |
| F6 | 5D | MAXIMISE | -0.1727 | W6 | TBD | Precision lock W6 ATB |
| F7 | 6D | MAXIMISE | **2.5982** | W8 | TBD | Anisotropic σ tighten |
| F8 | 8D | MAXIMISE | 9.832 | W2 | TBD | Anisotropic σ per-dim boundary lock |

*W9 scores pending portal return*

---

## W9 Strategy Summary

| Fn | Action | σ | Ratio | κ | Module 19 Basis |
|----|--------|---|-------|---|-----------------|
| F1 | EXPLORE — EXTREME WIDENING | 0.45 | 0.15 | 4.0 | Wei et al. (2022) high-temperature |
| F2 | RETURN TO W5 ATB — PRECISION LOCK | 0.008 | 0.95 | 2.0 | Kaplan et al. (2020) low-temperature |
| F3 | RETURN TO W7 ATB — PRECISION LOCK | 0.015 | 0.92 | 2.0 | Shannon (1948) delimiting context |
| F4 | SHANNON MAXIMUM ENTROPY | structured grid | 0.0 | 4.0 | Shannon (1948) H = -Σp·log p |
| F5 | PUSH X1→1.0 — BOUNDARY LOCK | 0.025 | 0.92 | 2.0 | Kaplan et al. (2020) gradient commit |
| F6 | PRECISION LOCK W6 ATB | 0.018 | 0.92 | 2.0 | Shannon (1948) delimiting context |
| F7 | ANISOTROPIC σ TIGHTEN | [0.010, 0.025×5] | 0.92 | 2.0 | Vaswani et al. (2017) per-head attention |
| F8 | ANISOTROPIC σ PER-DIM | [0.008–0.030] | 0.92 | 2.0 | Vaswani et al. (2017) anisotropic |

### F4 Module 19 Experiment — Shannon Maximum Entropy

F4 has clustered near [0.4, 0.4, 0.4, 0.4] for 8 consecutive weeks. Shannon (1948) defines information entropy H = −Σ p(x) log p(x). A search distribution concentrated at one region has low H — each new sample adds little information. W9 replaces stochastic Gaussian exploration with a structured deterministic grid of 24 candidates: 16 corners of [0.1, 0.9]⁴ + 8 face centres. This maximises H by sampling maximally different regions.

**Prompt engineering parallel:** Just as few-shot prompts with diverse exemplars span the distribution, BBO exploration requires candidates that span the search space.

---

## Pipeline

Each week follows a 13-step notebook pipeline:

| Step | Description |
|------|-------------|
| 0 | Config & Strategy |
| 1 | Data Load |
| 2 | Data Inspection |
| 3 | History Plot |
| 4 | Binary Labels (70th percentile threshold) |
| 5 | CV Model Comparison (8 classifiers, StratifiedKFold) |
| 5B | CNN-1D Inspection (Module 17 learning exercise) |
| 6 | Refit & Visualise |
| 7 | CV Chart & Winner |
| 7B | Why This Classifier Won |
| 8 | Candidate Generation (10,000 candidates) |
| 9 | GP Fit (Matern 5/2 kernel) |
| 10 | Acquisition Functions (EI + UCB) |
| 11 | Acquisition Curves |
| 12 | GP Surfaces |
| 13 | Submission Dashboard |

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

---

## Repository Structure

```
capstone-project/
├── bbo_dashboard/          # Streamlit dashboard
│   ├── app.py
│   ├── data.py
│   └── views/
│       ├── landing.py
│       ├── all_functions.py
│       ├── weekly.py
│       ├── source_view.py
│       └── pipeline.py
├── notebooks/              # Weekly Jupyter notebooks (F1-F8, W1-W9)
├── data/                   # .npy input/output files per function per week
└── week_logs/              # JSON week logs per function
```

---

*W1–W9 · BBO Optimisation · Imperial College London · DATA 2026 Cohort*
