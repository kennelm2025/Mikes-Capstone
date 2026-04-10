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
- **Anisotropic sigma (W7)** — per-dimension exploitation widths for F7, motivated by CNN filter map analysis showing X1 dominance

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
├── week-07/    Capstone_F1–F8_W7.ipynb   TuRBO sigma + anisotropic F7 (current)
├── week-08 to week-13/                   Upcoming submissions
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
- `BBO_WY_Strategy_Summary.docx` — strategy table for all 8 functions

---

## W7 Strategy At a Glance (Week 7 of 13)

| Fn | Dims | n  | Strategy | All-time Best | σ W7 | Direction | W7 Submission |
|----|------|----|----------|--------------|------|-----------|---------------|
| F1 | 2D | 15 | EXPLORE — escape flat region | ≈ 0 | 0.216 | EXPAND | `0.582827-0.482269` |
| F2 | 2D | 15 | EXPLOIT W5 best | 0.6497 | 0.0175 | SHRINK | `0.688952-0.168811` |
| F3 | 3D | 20 | EXPLOIT W6 new best | −0.000707 | 0.024 | SHRINK | `1.000000-0.571651-0.503999` |
| F4 | 4D | 35 | RECOVER W2 best ⚠️ | +0.2376 | 0.0175 | SHRINK | `0.451762-0.438642-0.400163-0.395091` |
| F5 | 4D | 25 | EXPLOIT W6 new best | 5,875 | 0.048 | EXPAND | `0.937682-1.000000-1.000000-1.000000` |
| F6 | 5D | 25 | EXPLOIT W6 new best | −0.1727 | 0.042 | EXPAND | `0.497320-0.294798-0.563080-0.684981-0.129206` |
| F7 | 6D | 35 | EXPLOIT W6 new best ★ | 2.119 | [0.015, 0.035×5] | SHRINK | `0.078067-0.385415-0.381193-0.266170-0.353901-0.693102` |
| F8 | 8D | 45 | RECOVER W2 best ⚠️ | 9.832 | 0.0175 | SHRINK | `0.040422-0.331667-0.003668-0.158463-0.396893-0.509806-0.166490-0.780552` |

**⚠️** Week log override applied — best point injected from email confirmation (not in .npy file)  
**★** First anisotropic sigma submission: CNN filter map analysis confirmed X1 is dominant structural dimension

---

## Hyperparameter Optimisation

All hyperparameters are documented in `FX_WY_hyperparameters.json` for every function-week combination. Key parameters:

| Parameter | Purpose | Typical range | W7 rationale |
|-----------|---------|---------------|-------------|
| `EXPLOIT_RATIO` | Fraction of 10k candidates near best point | 0.4–0.9 | High (0.85) for strong best points; 0.4 for F1 exploration |
| `EXPLOIT_SIGMA` | Gaussian σ around best point | 0.015–0.216 | Tightened (SHRINK) after new best; widened (EXPAND) after stagnation |
| `UCB_KAPPA` | Exploration weight in UCB = μ + κσ | 2.0–3.0 | 3.0 = ~99.7% CI; 2.5 when exploiting known region |
| `EI_XI` | Exploration jitter in EI | 0.01 | Fixed; prevents over-committing to tiny improvements |
| `GP_RESTARTS` | Random restarts for kernel optimisation | 5–10 | 5 restarts balances fit quality vs runtime |
| `FILTER_PERCENTILE` | Classifier filter threshold | 50% | Keeps top 5,000 of 10,000 candidates for GP |

**Sigma adaptation rule (TuRBO-inspired):** if W(n) > W(n-1), SHRINK sigma (precision around new best); if W(n) ≤ W(n-1), EXPAND sigma (wider search). F7 uses anisotropic sigma based on CNN inspection.

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
| W8–W13 | Upcoming |

---

## Results (W1–W7)

Full interactive results on the [live dashboard](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app).

W7 actual scores pending portal processing. W1–W6 highlights:
- **F5** — strongest signal; X2–X4 saturated at 1.0, GP searching for optimal X1 near boundary
- **F7** — first anisotropic submission; CNN confirmed X1≈0 structural boundary
- **F4, F8** — week log overrides recovering best points missing from .npy files

---

## Running a Notebook

1. Place `week_log_FX.json` and `fX_wY_inputs/outputs.npy` in the same folder as the notebook
2. Run all cells top to bottom (Kernel → Restart & Run All)
3. Step 14 prints the formatted submission string ready to paste into the portal

**Requirements:** `numpy`, `scikit-learn`, `matplotlib`, `scipy`, `torch`

---

## Academic Basis

All design choices are justified against peer-reviewed literature. See [`references.md`](references.md) for full citations.

| Reference | Application |
|-----------|-------------|
| Jones et al. (1998) | Expected Improvement acquisition function |
| Rasmussen & Williams (2006) | Gaussian Process fundamentals |
| Srinivas et al. (2010) | GP-UCB acquisition, exploration-exploitation balance |
| Eriksson et al. (2019) | TuRBO trust regions — sigma adaptation strategy |
| Cybenko (1989) | Universal approximation — NN classifier justification |
| Goodfellow et al. (2016) | Deep learning — CNN-1D classifier foundations |
