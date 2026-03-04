# Bayesian Optimisation Capstone
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London

> Maximising eight unknown black-box functions simultaneously.
> One query per function per week. No gradients, no source code, no function form.

---

## The Challenge

Eight synthetic black-box functions that accept inputs and return a single scalar output.
The goal is to find the inputs that produce the highest possible output for each function —
with only one submission per function per week and no visibility of the function internals.

**Key characteristics:**
- **Black box** — no access to the function's internal workings
- **Maximisation** — every function is a maximisation task
- **Sparse data** — each function starts with only 10 known data points
- **One query per week** — every submission must count
- **Increasing complexity** — functions range from 2D (F1, F2) to 8D (F8)

**Submission format:** `x1-x2-x3-...-xn` where each xᵢ ∈ [0, 1] to six decimal places.
Example (4D): `0.803046-0.945451-0.997548-0.976270`

---

## Why Bayesian Optimisation?

With only one evaluation per week, standard approaches fail:

| Approach | Why it fails |
|----------|-------------|
| Grid search | 10^6 points needed in 6D — would take centuries |
| Random search | No learning between queries |
| Gradient descent | No gradient available |
| Neural network | Needs thousands of examples to train |

**Bayesian Optimisation** is specifically designed for expensive black-box functions.
It builds a probabilistic surrogate (Gaussian Process) of the unknown function and uses
an acquisition function to decide where to query next — balancing exploitation of known
good regions against exploration of uncertain ones.

For F8 (8D, ~44 samples): coverage is approximately 0.00004% of the search space.
BO is literally the only viable approach.

---

## Technical Approach

### Gaussian Process Surrogate

```python
kernel = ConstantKernel(1.0, (1e-10, 1e10)) * \
         Matern(length_scale=0.3, length_scale_bounds=(0.01, 10.0), nu=2.5) + \
         WhiteKernel(noise_level=1e-10, noise_level_bounds=(1e-12, 1e-2))
```

- **Matérn ν=2.5** — balances smoothness and flexibility across all 8 functions
- **ConstantKernel** — scales output variance
- **normalize_y=True** — numerical stability across functions with very different scales
- **n_restarts_optimizer** — avoids poor local optima in hyperparameter fitting

### Acquisition Functions

Two acquisition strategies computed and combined each week:

**Expected Improvement (EI)** — Jones et al. (1998). Integrates GP uncertainty to give
a principled explore/exploit balance. EI = max(0, μ − best) weighted by GP confidence.

**Upper Confidence Bound (UCB)** — Srinivas et al. (2010). Uses μ + κσ to directly
trade off predicted value against uncertainty. κ tuned per function dimensionality.

### Classifier Pre-Filter (from Week 3)

Historical outputs converted to binary labels (top 30% = class 1). A classifier
is trained and used to screen 10,000 random candidates before the GP ranks them —
concentrating the GP's attention on structurally promising regions.

From Week 4, five classifier families compared via 5-fold CV each week:
Linear SVM | Decision Tree | Random Forest | Logistic Regression | Neural Network

From Week 6, CNN-1D added as Model 8 — detects local coordinate-pair patterns
via Conv1d that standard classifiers miss.

### Explore / Exploit Parameters

| Dimension | EXPLOIT_RATIO | EXPLOIT_SIGMA | UCB κ |
|-----------|--------------|---------------|-------|
| 2D (F1, F2) | 0.60–0.85 | 0.06–0.08 | 2.0–3.0 |
| 3D–4D (F3–F5) | 0.80–0.85 | 0.04–0.05 | 2.0–2.5 |
| 5D–8D (F6–F8) | 0.80–0.85 | 0.04–0.05 | 2.0–2.5 |

---

## Pipeline Evolution

| Week | Key Development | Academic Basis |
|------|----------------|----------------|
| W1 | GP + EI/UCB baseline | Jones (1998), Rasmussen & Williams (2006) |
| W2 | Local refinement around best point | Jones (1998) — exploitation |
| W3 | SVM classifier pre-filter | Cybenko (1989), Goodfellow et al. (2016) |
| W4 | Multi-model CV — 5 classifier families | Barrett et al. (2019) |
| W5 | Pipeline stabilised — week log audit | Chennu et al. — noisy signal interpretation |
| W6 | CNN-1D Model 8, true best corrections | Eriksson et al. (2019), Barrett et al. |
| W7+ | Adaptive TuRBO trust region (planned) | Eriksson et al. (2019) |

---

## Repository Structure

Each week folder is self-contained with its own README, strategy document,
submission record, and notebooks. See each week's README for detail.

```
capstone-project/
├── README.md               ← This file
├── references.md           ← Academic justifications
├── week-01/                ← GP + EI/UCB baseline
├── week-02/                ← Local refinement added
├── week-03/                ← SVM classifier pre-filter
├── week-04/                ← Multi-model CV (5 families)
├── week-05/                ← Week log audit + pipeline stabilised
├── week-06/                ← CNN-1D + true best corrections
└── week-07 to week-12/     ← Upcoming
```

Each week folder contains:
```
week-XX/
├── README_WX.md                  ← Week summary and results
├── BBO_WX_Strategy_Summary.md    ← Per-function strategy rationale
├── WX_Submissions.txt            ← Exact coordinates submitted + results
└── Capstone_F[1-8]_WX.ipynb     ← One notebook per function
```

---

## Academic Foundations

| Paper | Justifies |
|-------|-----------|
| Jones et al. (1998) | Expected Improvement acquisition |
| Rasmussen & Williams (2006) | GP surrogate, Matérn kernel |
| Srinivas et al. (2010) | GP-UCB dual acquisition strategy |
| Eriksson et al. (2019) — TuRBO | Trust-region candidate generation |
| Cybenko (1989) | Universal approximation — classifier basis |
| Goodfellow et al. (2016) | Neural network architecture |
| Barrett et al. (2019) | When do NNs outperform simpler models? |
| Calandra et al. (2016) | Real-world BO with expensive evaluations |
| Chennu et al. | Bayesian interpretation of weekly score signals |
| Kelta | Explore/exploit ratio formalisation |

Full citations and per-paper pipeline justifications: [`references.md`](references.md)

---

## Running Any Notebook

```bash
pip install numpy scikit-learn matplotlib scipy torch

# Place in same folder as the notebook:
#   fX_wY_inputs.npy  +  fX_wY_outputs.npy
# W6 notebooks also require:
#   week_log_FX.json

# Run all cells top to bottom
# Final cell prints the formatted submission string
```

---

## Contributors
Mike Kennelly — ML & AI Professional Certificate | Imperial College London

---

*BBO Capstone | Active through Week 12*
