# 🎯 BBO Capstone — Interactive Dashboard

**Mike Kennelly | Black-Box Optimisation | W1–W7**

An interactive Streamlit dashboard presenting all 8 BBO functions across 7 weeks of optimisation — scores, strategies, winning classifiers, GP predictions, and full pipeline walkthrough.

## 🚀 Run on Streamlit Cloud (Examiner Instructions)

Click the badge below to open the live dashboard — no install required:

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://your-app-name.streamlit.app)

## 💻 Run Locally

```bash
git clone https://github.com/yourusername/bbo-capstone-dashboard
cd bbo-capstone-dashboard
pip install -r requirements.txt
streamlit run app.py
```

## 📱 Dashboard Pages

| Page | Description |
|---|---|
| 🏠 **Overview** | KPIs, trajectory chart, strategy badge, hyperparameters, winning classifier for selected function |
| 📊 **Scores & Trajectory** | Full week-on-week bar chart, score history table, submitted coordinates per dimension |
| 🧭 **Strategy** | W7 strategy rationale, hyperparameter design, all-functions strategy comparison, exploit vs explore scatter |
| 🤖 **Classifiers** | Winning model detail, all 8 model explanations, CV accuracy chart, pipeline flow |
| ⚙️ **Pipeline** | 13-step pipeline visual flow, step selector with code snippets |
| 📋 **All Functions** | Side-by-side trajectories, improvement heatmap, combined leaderboard |

## 📊 Functions Covered

| Fn | Dims | Objective | W7 Strategy | All-Time Best |
|---|---|---|---|---|
| F1 | 2D | MINIMISE | EXPLORE | ~0.0 |
| F2 | 2D | MAXIMISE | EXPLOIT W5 BEST | 0.6497 |
| F3 | 3D | MINIMISE | EXPLOIT W6 NEW BEST | -0.000707 |
| F4 | 4D | MAXIMISE | EXPLOIT W2 BEST | +0.2376 |
| F5 | 4D | MAXIMISE | EXPLOIT W6 NEW BEST | 5875.1 |
| F6 | 5D | MINIMISE | EXPLOIT W6 NEW BEST | -0.1727 |
| F7 | 6D | MAXIMISE | EXPLOIT W6 NEW BEST | 2.119 |
| F8 | 8D | MAXIMISE | EXPLOIT W2 BEST | 9.832 |

## 🏗️ Pipeline Architecture

Each week's notebook follows a fixed 13-step pipeline:

```
Step 0:  Config & Strategy
Step 1:  Data Load (.npy files)
Step 2:  Data Inspection
Step 3:  History Plot
Step 4:  Candidate Generation (10,000 — exploit + Sobol explore)
Step 5:  Train 8 Classifiers (SVM, RF, NN, CNN-1D, etc.) with 5-fold CV
Step 6:  Model Comparison chart
Step 7:  Filter Candidates by P(class=1)
Step 7B: WHY This Classifier Won (analysis box)
Step 8:  Week Commentary (strategy markdown)
Step 9:  Gaussian Process Fit (Matérn 5/2 + WhiteKernel)
Step 10: Acquisition Functions (EI + UCB → submission = argmax EI)
Step 11: Per-Dimension Acquisition Curves
Step 12: GP Acquisition Surfaces (2D contours)
Step 13: Submission Dashboard + Final Output String
```

## 🛠️ Deploy to Streamlit Cloud

1. Fork/push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Set main file: `app.py`
5. Click **Deploy** — live in ~60 seconds

All data is baked into `data.py` — no external files or API keys needed.
