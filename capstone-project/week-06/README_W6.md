# BBO Capstone — Week 6
**Mike Kennelly | Black-Box Optimisation | Adaptive GP/EI Pipeline**

---

## What Is This?

Week 6 of an 8-week Black-Box Optimisation (BBO) capstone project.
Each week we submit one query point per function and receive a score back.
**The goal is always MAXIMISATION — higher values are always better.**

This week we run 8 function-specific notebooks built from a single generic
template (`Capstone_BBO_Generic_v3.ipynb`). Each notebook is pre-configured
with a function-specific strategy documented in the header cells.

---

## Repository Contents — Week 6

```
Notebooks
---------
Capstone_BBO_Generic_v3.ipynb   Generic template — adaptive model + GP/EI
Capstone_F1_W6.ipynb            F1  2D  EXPLORE
Capstone_F2_W6.ipynb            F2  2D  TIGHT EXPLOIT
Capstone_F3_W6.ipynb            F3  3D  EXPLOIT CAREFULLY
Capstone_F4_W6.ipynb            F4  4D  EXPLOIT AGGRESSIVELY
Capstone_F5_W6.ipynb            F5  4D  PRECISION EXPLOIT
Capstone_F6_W6.ipynb            F6  5D  EXPLOIT WITH MOMENTUM
Capstone_F7_W6.ipynb            F7  6D  STRUCTURED EXPLOIT
Capstone_F8_W6.ipynb            F8  8D  EXPLOIT + CNN EXPERIMENT

Data Files (input to each notebook)
------------------------------------
f1_w6_inputs.npy  /  f1_w6_outputs.npy     15 samples  2D
f2_w6_inputs.npy  /  f2_w6_outputs.npy     15 samples  2D
f3_w6_inputs.npy  /  f3_w6_outputs.npy     20 samples  3D
f4_w6_inputs.npy  /  f4_w6_outputs.npy     35 samples  4D
f5_w6_inputs.npy  /  f5_w6_outputs.npy     25 samples  4D
f6_w6_inputs.npy  /  f6_w6_outputs.npy     25 samples  5D
f7_w6_inputs.npy  /  f7_w6_outputs.npy     35 samples  6D
f8_w6_inputs.npy  /  f8_w6_outputs.npy     45 samples  8D

Strategy & Documentation
-------------------------
README_W6.md                    This file
BBO_W6_Strategy.md              Full function-by-function strategy rationale
Module17_CNN_BBO_Reflection.docx  Assignment reflection (CNNs + BBO)
```

---

## Pipeline (identical for all 8 functions)

```
STEP 0  Config & hyperparameter documentation (function-specific settings)
STEP 1  Imports  (all libraries documented with role + Module 17 connection)
STEP 2  Load W6 data  (.npy files — W5 history + W5 score appended)
STEP 3  Visualise historical performance
STEP 4  Binary labels  (top 30% = class 1 — HIGH values are the target)
STEP 5  Train 7 classifiers  (SVM, DTree, RF, LogReg, NN-Small/Med/Large)
        F8 only: +1D CNN classifier experiment (Module 17 connection)
STEP 6  Visualise all model predictions
STEP 7  CV model comparison — select winner + auto-document winner rationale
STEP 8  Generate 10,000 candidates (exploit/explore split)
STEP 9  Gaussian Process regression  (Matern 5/2 kernel — mu + sigma)
STEP 10 Acquisition functions  (EI and UCB — MAXIMISATION throughout)
STEP 11 Per-dimension acquisition curves  (EI + UCB per dim)
STEP 12 Acquisition surface visualisations
STEP 13 Top candidates + submission dashboard
STEP 14 Final formatted submission string
STEP 15 Save hyperparameter record  (JSON + text report)
```

---

## How to Run

1. Place the `.npy` data files in the same directory as the notebook
2. Open the function notebook (e.g. `Capstone_F3_W6.ipynb`)
3. Run all cells — config is pre-set, no changes needed
4. Read the submission string printed at the end of Step 14
5. Check the saved `F{x}_W6_hyperparameters.json` for the full run record

---

## W6 Snapshot — Strategy Per Function

| Fn | Dims | W6 Samples | All-Time Best | W5 Score   | W6 Strategy            |
|----|------|-----------|---------------|------------|------------------------|
| F1 | 2D   | 15        | ~0.000        | -0.0000005 | EXPLORE                |
| F2 | 2D   | 15        | 0.6497 (NEW)  | +0.6497    | TIGHT EXPLOIT          |
| F3 | 3D   | 20        | -0.0136       | -0.0590    | EXPLOIT CAREFULLY      |
| F4 | 4D   | 35        | -0.5268       | -2.4571    | EXPLOIT AGGRESSIVELY   |
| F5 | 4D   | 25        | 2912.99       | +24.48     | PRECISION EXPLOIT      |
| F6 | 5D   | 25        | -0.3630       | -1.7662    | EXPLOIT WITH MOMENTUM  |
| F7 | 6D   | 35        | 1.3650        | +0.5763    | STRUCTURED EXPLOIT     |
| F8 | 8D   | 45        | 9.8188        | +8.9560    | EXPLOIT + CNN EXPT     |

Full rationale for each function: see `BBO_W6_Strategy.md`

---

## Module 17 — CNNs & BBO

This week's academic module covered Convolutional Neural Networks.
Key parallels drawn between CNNs and our BBO approach:

- **Progressive feature extraction**: BBO weeks mirror CNN layers —
  early weeks map the landscape (edges), later weeks refine the peak (objects)
- **Pooling = candidate filtering**: two-stage reduction (classifier -> GP)
  retains only the strongest signal, discarding clearly bad regions
- **ReLU = EI non-negativity**: EI = max(0, improvement) — points that
  cannot beat the current best produce EI = 0, creating a sparse acquisition map
- **Loss function proxy gap**: EI optimises a surrogate objective, not the
  true function. GP R² is tracked in every Step 15 record as a reliability check
- **CNN experiment on F8**: only function with sufficient data (45 samples, 8D)
  to test a 1D convolutional classifier alongside the standard 7 models

See `Module17_CNN_BBO_Reflection.docx` for the full assignment response.

---

## Data Format

All `.npy` files are NumPy arrays:

- `f{x}_w6_inputs.npy`  — shape `(n, dims)` — input coordinates in [0, 1]^d
- `f{x}_w6_outputs.npy` — shape `(n,)`      — corresponding function values

W6 files = W5 files with the W5 submission point and W5 score appended
as the final row/value respectively.

---

*Week 6 | BBO Capstone | Mike Kennelly*
