# References & Academic Justifications

# Bayesian Optimisation Capstone
### Mike Kennelly — ML & AI Professional Certificate | Imperial College London

This file documents the academic papers and frameworks that informed the design of the BBO pipeline. Each entry notes what it justifies in the codebase.

---

## Core Bayesian Optimisation

**Jones, D.R., Schonlau, M., & Welch, W.J. (1998)**
*Efficient Global Optimization of Expensive Black-Box Functions.*
Journal of Global Optimization, 13(4), 455–492.

> Justifies **Expected Improvement (EI)** as the acquisition function across all 8 notebooks (Step 10). EI is the principled solution to balancing exploitation of known good regions against exploration of uncertain ones under a limited query budget.

---

**Rasmussen, C.E. & Williams, C.K.I. (2006)**
*Gaussian Processes for Machine Learning.*
MIT Press.

> Justifies the **GP surrogate model** (Step 9) — specifically the Matérn kernel choice, output normalisation (`normalize_y=True`), and the `n_restarts_optimizer` setting for stable kernel hyperparameter fitting. The GP posterior provides both predicted mean and uncertainty at unsampled points.

---

**Srinivas, N., Krause, A., Kakade, S., & Seeger, M. (2010)**
*Gaussian Process Optimization in the Bandit Setting: No Regret and Experimental Design.*
ICML 2010.

> Justifies the **GP-UCB acquisition function** (Step 10) and the dual EI+UCB strategy. Running both in parallel and combining scores proved critical for volatile functions (F4, F7) where neither acquisition function alone was reliable across consecutive weeks.

---

**Eriksson, D., Pearce, M., Gardner, J., Turner, R.D., & Poloczek, M. (2019)**
*Scalable Global Optimization via Local Bayesian Optimization (TuRBO).*
NeurIPS 2019.

> Informs the **trust-region heuristic** in the candidate generation step (Step 8). Exploit candidates are Gaussian samples centred on the best point (σ=0.04), approximating a local trust region. A full adaptive TuRBO implementation (expand on improvement, shrink on stagnation) is planned for Week 7, particularly for F5, F7, and F8.

---

## Neural Networks & Classifiers

**Cybenko, G. (1989)**
*Approximation by Superpositions of a Sigmoidal Function.*
Mathematics of Control, Signals, and Systems, 2(4), 303–314.

> Provides theoretical grounding for the **MLP classifiers** (NN-Small, NN-Medium, NN-Large) in Step 5. The universal approximation theorem guarantees that a sufficiently wide single hidden layer can approximate any continuous function — justifying MLP use as a black-box classifier on the binary labels derived from BBO history.

---

**Goodfellow, I., Bengio, Y., & Courville, A. (2016)**
*Deep Feedforward Networks. In: Deep Learning.*
MIT Press, Chapter 6.

> Supports the **multi-layer neural network architecture** choices in Step 5, including activation functions, dropout regularisation, and the trade-off between depth and overfitting risk on small datasets (n=14–44).

---

**Barrett, D.G.T., et al. (2019)**
*Analyzing Biological and Artificial Neural Networks: Challenges with Opportunities for Synergy?*
Current Opinion in Neurobiology.

> Informed the decision of **when to trust neural network classifiers** over simpler models. Barrett et al. raise the practical question of when NNs genuinely outperform alternatives. The W6 CNN-1D results answered this directly — CNN placed first or second on F4 (83.3%) and F5 (85.7%) where coordinate structure was learnable, but added little on F1 where the landscape was flat.

---

## Applied Bayesian Methods

**Calandra, R., et al. (2016)**
*Bayesian Gait Optimization for Bipedal Locomotion.*
LION 2016.

> Provides a **real-world parallel** to the BBO challenge — expensive evaluations in a continuous parameter space with no gradient access, which is structurally identical to the capstone setup. Confirms that GP+EI pipelines are viable in practical sequential optimisation tasks beyond academic benchmarks.

---

**Chennu, S., et al. (2021)**
*Rapid and Scalable Bayesian AB Testing.*

> Relevant to **interpreting weekly submission results**. Each week's score is a noisy signal about the true optimum, not ground truth. The Bayesian belief-updating framework described by Chennu et al. maps directly onto how week-on-week results should update the GP prior rather than be treated as definitive measurements.

---

**Kelta, Z.**
*Mastering Bayesian Optimisation in Data Science.*

> Practical reference for **formalising explore/exploit ratio choices**. The EXPLOIT_RATIO and EXPLOIT_SIGMA hyperparameters in the Week 6 config cells are currently set by intuition and cross-validated against week log history — Kelta's framework provides a more rigorous basis for these decisions.

---

## Libraries & Frameworks

| Library | Version | Role in Pipeline |
|---------|---------|-----------------|
| `scikit-learn` | ≥1.3 | GaussianProcessRegressor, all classifiers, StandardScaler, StratifiedKFold CV |
| `PyTorch` | ≥2.0 | CNN-1D classifier (Model 8, added Week 6) |
| `NumPy` | ≥1.24 | Candidate generation, array operations throughout |
| `SciPy` | ≥1.10 | Normal distribution functions in EI calculation |
| `Matplotlib` | ≥3.7 | All visualisations (Steps 3, 6, 7, 11, 12) |

**Why scikit-learn over BoTorch/GPyTorch?**
Sample sizes (n=14–44) are too small to benefit from GPU-accelerated GP inference. Scikit-learn's validated API and transparent internals reduce implementation risk and make the pipeline auditable — important for a learning context.

---

## Week-by-Week Pipeline Evolution

| Week | Key Addition | Academic Basis |
|------|-------------|----------------|
| W1 | GP + EI/UCB baseline | Jones (1998), Rasmussen & Williams (2006) |
| W2 | Local refinement around best point | Jones (1998) — exploitation |
| W3 | SVM classifier pre-filter introduced | Cybenko (1989), Goodfellow et al. (2016) |
| W4 | Multi-model CV — 7 classifiers compared | Barrett et al. (2019) |
| W5 | Week log system — true best tracking | Chennu et al. — noisy signal interpretation |
| W6 | CNN-1D as Model 8, TuRBO-style trust region | Eriksson et al. (2019), Barrett et al. (2019) |
| W7 | Adaptive trust region (planned) | Eriksson et al. (2019) — full TuRBO |
