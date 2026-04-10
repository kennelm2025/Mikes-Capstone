# Bayesian Optimisation Capstone
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London

> Adaptive Bayesian Optimisation pipeline for maximising 8 unknown black-box
> functions simultaneously. One submission per function per week. No gradient
> access, no source code, no function form.

---

## The Problem

Eight black-box functions. One query per function per week. The only feedback
is a scalar score returned after each submission. The goal is to find the
maximum of each function in as few evaluations as possible — using everything
seen so far to make the next query count.

Functions range from 2D to 8D with wildly different landscapes: F1 is
effectively flat (all outputs near zero), F5 peaks at 4,891 with a sharp
spike, F8 is consistent and broad across 8 dimensions.

---

## How the Pipeline Works

```
Load data → Binary labels (top 30% = good)
→ Train 8 classifiers → 5-fold CV → Select winner
→ Generate 10,000 candidates → Filter by classifier
→ Fit GP (Matérn kernel) → Compute EI + UCB
→ Combine scores → Submit top candidate
```

The pipeline evolved across 6 weeks — from a bare GP baseline to a full
multi-model classifier → GP system with CNN-1D augmentation:

| Week | Key Development |
|------|----------------|
| W1 | GP + EI/UCB baseline — pure exploration |
| W2 | Local refinement around best point |
| W3 | SVM classifier pre-filter introduced |
| W4 | Multi-model CV — 5 classifier families compared |
| W5 | Pipeline stabilised — week log audit reveals missing npy data |
| W6 | CNN-1D as Model 8 — week log overrides for 5 functions |
| W7+ | Adaptive TuRBO trust region planned |

---

## Repository Structure

```
capstone-project/
├── README.md               ← This file
├── references.md           ← Academic justifications for all design choices
├── week-01/                ← GP + EI/UCB baseline
│   ├── README_W1.md
│   ├── BBO_W1_Strategy_Summary.md
│   ├── W1_Submissions.txt
│   └── Capstone_F[1-8]_W1.ipynb
├── week-02/                ← Local refinement added
│   └── ...same structure...
├── week-03/                ← SVM classifier pre-filter
│   └── ...same structure...
├── week-04/                ← Multi-model CV (5 families)
│   └── ...same structure...
├── week-05/                ← Pipeline stabilised + week log discovery
│   └── ...same structure...
├── week-06/                ← CNN-1D Model 8 + true best corrections
│   ├── README.md
│   ├── BBO_W6_Strategy_Summary.md
│   ├── W6_Submissions.txt
│   ├── week_log_F[1-8].json
│   ├── BBO_W6_Strategy.docx
│   ├── BBO_W6_Reflection.docx
│   └── Capstone_F[1-8]_W6.ipynb
└── week-07 to week-12/     ← Upcoming weeks
```

---

## W6 Results at a Glance

| Fn | Dims | True Best | Best Wk | W5 Score | W6 Strategy |
|----|------|-----------|---------|----------|-------------|
| F1 | 2D   | ≈ 0       | W2      | ≈ 0      | EXPLORE |
| F2 | 2D   | 0.6497    | W5      | 0.6497   | EXPLOIT W5 |
| F3 | 3D   | -0.0136   | W1      | -0.059   | RECOVER W1 |
| F4 | 4D   | +0.238 ⚠️ | W2      | -2.457   | RECOVER W2 |
| F5 | 4D   | 4,891 ⚠️  | W3      | 24.48    | RECOVER W3 |
| F6 | 5D   | -0.237 ⚠️ | W2      | -1.766   | RECOVER W2 |
| F7 | 6D   | 1.739 ⚠️  | W2      | 0.576    | RECOVER W2 |
| F8 | 8D   | 9.832     | W2      | 8.956    | EXPLOIT |

⚠️ = true best was missing from `.npy` files — recovered via week log audit.

---

## Critical Discovery — Missing npy Data

Cross-referencing submission emails against platform `.npy` files revealed
that 4 functions had incomplete histories. True bests for F4, F5, F6 and F7
were all missing — causing the GP to target wrong coordinates for weeks.

The fix: `week_log_FX.json` files built from submission emails are injected
into GP training at runtime, overriding the incomplete npy history.

---

## CNN-1D Experiment (Week 6)

CNN-1D added as Model 8, compared against 7 classical classifiers via 5-fold CV:

- **F5** — CNN tied first at 85.7% (matched Random Forest, tighter variance)
- **F4** — CNN scored 83.3%, just 0.6% behind winner, P(best point)=1.000

CNN works best where the optimum has local coordinate structure — tight
clusters or boundary patterns that Conv1d detects by scanning adjacent
feature pairs.

---

## Running a Notebook

```bash
pip install numpy scikit-learn matplotlib scipy torch

# For W6: place in same folder as notebook:
#   week_log_FX.json + fX_w6_inputs.npy + fX_w6_outputs.npy

# Run all cells top to bottom
# Final cell prints the formatted submission string
```

---

## Academic Basis

| Paper | Role in Pipeline |
|-------|-----------------|
| Jones et al. (1998) | Expected Improvement acquisition |
| Rasmussen & Williams (2006) | GP surrogate + Matérn kernel |
| Srinivas et al. (2010) | GP-UCB dual acquisition |
| Eriksson et al. (2019) — TuRBO | Trust-region candidate generation |
| Cybenko (1989) | Universal approximation — classifier basis |
| Goodfellow et al. (2016) | Neural network architecture choices |
| Barrett et al. (2019) | When do NNs outperform simpler models? |
| Calandra et al. (2016) | Real-world BO with expensive evaluations |
| Chennu et al. | Bayesian interpretation of weekly score signals |

Full citations → [`references.md`](references.md)

---

## Contributors
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London
---

*BBO Capstone | Active through Week 12*
