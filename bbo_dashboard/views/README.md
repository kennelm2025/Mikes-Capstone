# 🎯 BBO Capstone — Interactive Dashboard

**Mike Kennelly | Black-Box Optimisation | W1–W13 FINAL**

An interactive Streamlit dashboard presenting all 8 BBO functions across 13 weeks of optimisation — scores, strategies, winning classifiers, GP predictions, Module 22 clustering, Module 23 PCA, and full pipeline walkthrough.

W13 is the final portal submission (Module 24 is reflection-only). All W1–W13 data is baked into `data.py`.

## 🚀 Run on Streamlit Cloud (Examiner Instructions)

Click the badge below to open the live dashboard — no install required:

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

## 💻 Run Locally

```bash
git clone https://github.com/kennelm2025/Mikes-Capstone
cd Mikes-Capstone/bbo_dashboard
pip install -r requirements.txt
streamlit run app.py
```

## 📱 Dashboard Pages

| Page | Description |
|---|---|
| 🏠 **Home** | Project overview, all-functions trajectories W1–W13, summary cards |
| 📊 **All Functions** | Side-by-side trajectories (W1–W13), improvement heatmap, full submission table |
| 🔬 **Weekly Analysis** | Per-function drill-down: scores, coords, strategy, classifier, GP predictions for selected week |
| 📋 **Source Code** | Rendered Jupyter notebook source per function/week |
| 🏗️ **Pipeline** | 15-step pipeline visual flow with function/week context per step |

## 📊 Functions Covered — W13 Final State

| Fn | Dims | Objective | W13 Strategy | All-Time Best | ATB Week |
|---|---|---|---|---|---|
| F1 | 2D | MAXIMISE | ATB OVERRIDE (deterministic) | 8.968e-07 | W11 |
| F2 | 2D | MAXIMISE | ATB OVERRIDE (W12 NEW ATB) | 0.6880 | W12 ★ |
| F3 | 3D | MAXIMISE | ATB OVERRIDE (σ~0.003 noise) | -0.000707 | W11 |
| F4 | 4D | MAXIMISE | ATB OVERRIDE (triple-confirmed) | +0.23759 | W2 |
| F5 | 4D | MAXIMISE | ATB OVERRIDE [1,1,1,1] corner | 8662.48 | W9 |
| F6 | 5D | MAXIMISE | ATB OVERRIDE (σ~0.063 HIGHEST) | 0.03602 | W9 |
| F7 | 6D | MAXIMISE | GP PIPELINE + ATB FALLBACK | **2.8939** | **W12 ★** |
| F8 | 8D | MAXIMISE | ATB OVERRIDE (PRIMARY Module 23 PCA — 3 flat PCs) | 9.83196 | W2 |

**★ New ATBs at W12:** F2 (+0.038 over W5) · F7 (7th consecutive improvement)

## 🧩 Module 23 PCA Taxonomy (new at W13)

Each function is classified by its variance structure under Module 23 PCA analysis:

| Fn | PCA case | Flat PCs | Effective dim |
|---|---|---|---|
| F1 | Tight attractor | — | — |
| F2 | Kernel-PCA (two basins) | 0 linear | 2 (kernel) |
| F3 | Scree / 1 flat PC (X1 locked) | 1 | 2 |
| F4 | Isolated basin | 0 | 4 |
| F5 | **Flat-scree corner** | ~4 | ~0 (cleanest) |
| F6 | Threshold / dominant-PC | 0 | 5 |
| F7 | **Trending ridge** | 0 | 1 (PC1 share 0.900) |
| **F8** | **Zero-boundary / 3 flat PCs** | **3** | **5** (PRIMARY showcase) |

## 🏗️ Pipeline Architecture (W13)

Each week's notebook follows a 15-step pipeline (was 13 at W11, +2 new at W13):

```
Step 0:  Config & Strategy
Step 1:  Data Load (.npy files)
Step 2:  Data Inspection
Step 3:  History Plot + Module 22 Clustering
Step 4:  Binary Labels (top 30%)
Step 5:  CV Model Comparison (8 classifiers, 5-fold CV)
Step 5B: CNN-1D Inspection (Module 17)
Step 5C: ★ NEW W13 — Module 23 PCA Variance Analysis
Step 6:  Refit & Visualise
Step 7:  CV Chart & Winner
Step 7B: Why This Classifier Won
Step 8:  Candidate Generation (anisotropic TuRBO)
Step 9:  GP Fit (Matérn 5/2)
Step 10: Acquisition Functions (EI + UCB)
Step 11: Per-Dimension Acquisition Curves
Step 11B: Ollama LLM Advisor (Module 20)
Step 12: GP Surfaces
Step 13: Submission Dashboard
Step 14: ★ NEW W13 — Final Submission Decision
         ATB override for F1-F6, F8 (FINAL round risk-minimisation)
         F7 unique: 3 trust conditions (μ>ATB, R²<0.999999, gain>σ/2)
         If ALL pass → GP EI candidate. If ANY fails → W12 ATB fallback.
Step 15: ★ NEW W13 — Hyperparameter Record (JSON + TXT with PCA block)
```

## ⚡ F7 — The Only GP Pipeline Function

F7 is the only function where the notebook runs the full GP pipeline at W13. Why? Because F7 has:
- 7 consecutive ATB improvements (W6 → W12)
- 1-dominant-PC structure (ridge: PC1 share 0.900, |corr(PC1,y)|=0.976)
- Dynamic cluster (moving centroid — not static attractor)

All other functions have static attractors where GP extrapolation cannot beat confirmed ATBs. The F7 FINAL round uses 3 strict trust conditions before accepting the GP candidate; author execution saw all 3 FAIL → FALLBACK to W12 ATB coords.

## 🛠️ Deploy to Streamlit Cloud

1. Fork/push this repo to GitHub (the `bbo_dashboard/` folder is self-contained)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `bbo_dashboard/app.py`
5. Click **Deploy** — live in ~60 seconds

All data is baked into `data.py` — no external files, no API keys needed.

## 📂 File Layout

```
bbo_dashboard/
├── app.py              ← Main Streamlit entry point (sidebar + routing)
├── data.py             ← All baked data: SCORES, COORDS, STRATEGY, WEEKLY, CLASSIFIERS, etc.
├── requirements.txt    ← streamlit, plotly, pandas, numpy, scipy
├── README.md           ← This file
├── all_functions.py    ← 📊 All Functions view (2×4 trajectory grid + heatmap + submission table)
├── landing.py          ← 🏠 Home view (project overview + all-function cards)
├── weekly.py           ← 🔬 Weekly Analysis view (per-function drill-down)
├── pipeline.py         ← 🏗️ Pipeline view (15-step flow + step-by-step context)
└── source_view.py      ← 📋 Source Code view (rendered notebook per function/week)
```

## 📎 Related Capstone Deliverables

Outside `bbo_dashboard/`, the capstone repository root contains:

- `README.md` — capstone-level W1–W13 overview
- `BBO_W13_Model_Card.md` — model card (Mitchell et al. 2019 framework)
- `BBO_W13_Data_Card.md` — data card (Gebru et al. 2021 framework)
- `W13_Submissions.txt` — all 8 W13 submission strings in portal format
- `week-01/` through `week-13/` — historical notebooks + npy data

---

*W1–W13 FINAL · BBO Optimisation · Imperial College London · DATA 2026 Cohort · Mike Kennelly*
