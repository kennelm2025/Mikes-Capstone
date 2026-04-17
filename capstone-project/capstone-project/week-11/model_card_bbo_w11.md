# Model Card: Adaptive GP/EI Black-Box Optimisation Pipeline

**Mike Kennelly | Imperial College London | PCMLAI Capstone | April 2026**

*Built following the model card framework from Mini-lesson 21.2 and Mitchell et al. (2019) "Model Cards for Model Reporting" (FAccT '19). Structure mirrors the Datatonic Loan Default XGBoost example from Mini-lesson 21.2.*

---

## Model overview

| Property | Value |
|----------|-------|
| **Model name** | Adaptive GP/EI Black-Box Optimisation Pipeline |
| **Type** | Bayesian optimisation surrogate — Gaussian Process with Expected Improvement acquisition |
| **Task** | Sequential maximisation of unknown black-box functions over [0,1]ⁿ |
| **Version** | v11 — Week 11 of 13, penultimate iteration |
| **Developer** | Mike Kennelly, Imperial College London PCMLAI Capstone |
| **Deployment** | Weekly oracle query submission — one coordinate per function per week |
| **Frameworks** | scikit-learn (GP, classifiers), PyTorch (CNN-1D), NumPy, SciPy |
| **Repository** | [github.com/kennelm2025/Mikes-Capstone](https://github.com/kennelm2025/Mikes-Capstone) |

The pipeline addresses a sequential optimisation problem under a strict evaluation budget. At each weekly iteration it fits a Gaussian Process surrogate on all accumulated oracle evaluations, computes Expected Improvement (EI) and Upper Confidence Bound (UCB) acquisition functions across 10,000 candidates pre-filtered by a trained binary classifier, and submits the highest-EI candidate to the oracle. Eight unknown functions are optimised in parallel, each with its own data file, trained classifier and fitted GP.

---

## Intended use

**Primary tasks:**
- Sequential black-box maximisation of continuous functions over bounded domains [0,1]ⁿ where n ≤ 10 and each evaluation is expensive (one oracle query per iteration)
- Small-budget optimisation settings where the total evaluation count per function is 10–50 — the regime where GP surrogates outperform model-free approaches
- Pedagogical demonstration of the full GP surrogate + EI acquisition loop with all pipeline steps documented and inspectable

**Target users:**
- Students and researchers studying Bayesian optimisation methods
- ML practitioners evaluating surrogate-based optimisation for expensive function settings
- Reviewers and examiners assessing the capstone pipeline design

**Limitations — use cases to avoid:**
- **High-dimensional spaces (n > 15):** GP fitting complexity is O(n³) in sample count — computationally prohibitive without sparse approximations at large n
- **Multi-modal or discontinuous functions:** A single Matérn kernel cannot adequately model landscapes with many local optima — evolutionary or multi-start approaches would be more appropriate
- **Sole automated decision-making:** As the W11 ATB override events demonstrate, GP suggestions must be validated against domain knowledge before acting on them. This pipeline should be used as a decision aid, not a sole determinant — directly mirroring the Datatonic card's guidance on credit risk
- **Safety-critical real-time applications:** GP fitting with multiple random restarts takes several seconds per function — not suitable for millisecond-level decisions

---

## Training data

| Property | Value |
|----------|-------|
| **Size** | 19–49 rows per function (varies by dimensionality); 8 separate datasets |
| **Source** | Imperial College BBO Capstone oracle portal — one evaluation per function per week |
| **Collection** | Each row is a student-submitted coordinate x ∈ [0,1]ⁿ paired with oracle output y = f(x) |
| **Features** | n-dimensional coordinates in the normalised unit hypercube [0,1]ⁿ |
| **Outputs** | Scalar oracle value (unbounded; varies by function — F5 in thousands, F3 near zero) |
| **Data integrity** | Output files contain ONLY portal-returned values — no imputation or estimation |
| **Storage** | `.npy` format in `/capstone-project/week-{n}/` folders in the public GitHub repository |

The datasets are small by ML standards — F1 has 19 rows, F8 has 49 — but this is structurally correct for the BBO setting: if large datasets were available, the black-box problem would already be solved. The GP's utility is precisely that it extracts maximum information from a minimal number of evaluations.

The binary classifier is retrained each week on the accumulated data with fresh labels (top 30% = class 1, bottom 70% = class 0). These labels are derived at runtime — not stored — ensuring the classification boundary always reflects the current best-known landscape.

---

## Inputs and outputs

**Input:** An n-dimensional coordinate vector x = (x₁, x₂, ..., xₙ) where each xᵢ ∈ [0,1]. Submitted to the portal as a dash-separated string: `x1-x2-...-xn` to 6 decimal places.

**Output:** A scalar value y = f(x) returned by the oracle — the true function evaluation at the submitted coordinate. This is the ground truth signal; no proxy metric is used.

**Pipeline intermediate outputs (for inspection, not submission):**
- GP posterior mean μ(x) and standard deviation σ(x) across the candidate pool
- EI(x) and UCB(x) acquisition values at each candidate
- Binary classifier P(class=1) probability for each of 10,000 generated candidates
- Per-dimension EI and UCB curves (Step 11 diagnostic)
- GP acquisition surface plots for the two most sensitive dimensions (Step 12A)

---

## Strategy details: eleven rounds

The pipeline's core structure was fixed from Week 1. What evolved was the strategy — how candidates are generated, which model is trusted, and when to override the surrogate.

### Technique evolution across eleven rounds

| Phase | Weeks | Key technique | Impact |
|-------|-------|---------------|--------|
| Baseline | W1–W3 | Isotropic Gaussian exploration, equal sigma all dimensions | Landscape discovery |
| Function profiling | W4–W6 | Per-function exploit ratio; boundary patterns identified (F5, F8) | F5 new ATB W6 |
| Anisotropic sigma | W7–W8 | Per-dimension σ from GP sensitivity; Ollama llama3.1 consensus | F7 two new ATBs W7–W8 |
| GP reliability rule | W8–W10 | R²=1.0 + n_positives < 5 → ATB override | Prevented 6 bad submissions |
| Final strategy | W11 | 7/8 functions ATB override; F7 continues GP gradient | W12 plan locked |

**Anisotropic sigma** (introduced W7) was the most impactful improvement. Rather than sampling all dimensions with equal uncertainty, each dimension received its own sigma value based on GP sensitivity scores: `ANISO_SIGMA = [σ₁, σ₂, ..., σd]`. For F3, X1 received σ=0.005 (near-boundary lock) while X2/X3 received σ=0.020–0.025. This was guided by Ollama llama3.1 via a structured prompt containing the full 10-week submission history alongside GP sensitivity scores — a Module 20 learning exercise applied directly to strategy improvement.

**The ATB override rule** emerged as the single most important reliability decision. When the GP returns R²=1.0 on training data with fewer than 5 positive class labels, the surrogate is memorising rather than generalising — it cannot be trusted to suggest new candidates. In W11, this condition applied to 7 of 8 functions.

### Eight classifiers evaluated each week

Following the principle from Mini-lesson 21.2 that model cards should document the evaluation approach, the pipeline tests 8 classifier types and selects the CV winner:

| Model | Role |
|-------|------|
| Linear SVM | Linear decision boundary |
| Decision Tree (depth 4) | Sharp threshold rules |
| Random Forest (100 trees) | Robust ensemble |
| Logistic Regression | Probabilistic boundary |
| NN-Small (16,8) | Simple non-linear |
| NN-Medium (64,32) | Moderate complexity |
| NN-Large (128,64,32) | High complexity |
| CNN-1D (Conv1d→8→Linear) | Adjacent-pair pattern detection |

The CNN-1D was added in Week 7 as a Module 17 learning exercise — tracking whether convolutional pattern detection on adjacent coordinate pairs outperforms MLP classifiers as sample size grows.

---

## Performance

### All-time best oracle scores (primary metric)

| Function | Dims | ATB Score | ATB Week | n at W11 | n/p ratio |
|----------|------|-----------|----------|----------|-----------|
| F1 | 2 | 8.838e-07 | W2 | 19 | 9.5 |
| F2 | 2 | 0.6497 | W9 | 19 | 9.5 |
| F3 | 3 | -0.000707 | W6 | 24 | 8.0 |
| F4 | 4 | 0.2376 | W2 | 29 | 7.3 |
| F5 | 4 | 8662.48 | W9 | 29 | 7.3 |
| F6 | 5 | 0.0360 | W9 | 34 | 6.8 |
| F7 | 6 | 2.7201 | W10 | 39 | 6.5 |
| F8 | 8 | 9.8320 | W2 | 49 | 6.1 |

### Metrics used and why

**Primary metric — oracle return value:** The scalar y = f(x) returned by the portal for each submitted coordinate. This is the only ground truth available; all pipeline metrics are diagnostic.

**GP training R²:** Measures surrogate fit quality on training data. R²=1.0 at small n is a warning sign — the GP is interpolating, not generalising. This is the primary trigger for the ATB override rule.

**Binary classifier CV accuracy (stratified k-fold):** Measures how reliably the classifier identifies high-value regions. Below 60% = classifier provides no useful signal above random. Reported in every notebook's Step 7 output.

**EI and UCB at selected point:** Reported in each submission box. EI > 0 indicates the GP believes improvement is possible; UCB provides the optimistic upper bound (μ + 2σ).

**n/p ratio (samples ÷ dimensions):** Below 5 = data-sparse; GP and classifier reliability are both degraded. All 8 functions maintained n/p > 6 by W11.

### Performance trajectory highlights

**F5** demonstrates the clearest diminishing-returns scaling pattern: five consecutive new ATBs from W6–W9 (scores: 5875 → 7597 → 8382 → 8662) as X coordinates converged to [1.0, 1.0, 1.0, 1.0]. Each gain was smaller than the last — consistent with Kaplan et al.'s (2020) power-law scaling of returns.

**F7** shows a 5-week consecutive improvement streak (W6–W10: 2.119 → 2.413 → 2.598 → 2.597 → 2.720). This is the function where the GP pipeline remained trusted into W11 because the gradient signal was consistent and the improvement increments were stable.

**F1** is the documented failure case: the optimum appears to be a near-zero spike (8.838e-07) found only at W2. Ten subsequent queries returned values between 10⁻⁹ and 10⁻⁵⁸ — many orders of magnitude below the ATB. The function landscape is structurally hostile to GP-based search: nearly flat everywhere except an extremely sharp, difficult-to-relocate spike.

---

## Assumptions and limitations

### Assumptions underlying the strategy

**Smoothness (Matérn ν=5/2):** The GP kernel assumes the function is twice differentiable everywhere. This holds for F5 and F7 but is violated by F1's spike landscape and F3's sharp X1 boundary effect.

**Stationarity:** The GP kernel assumes equal correlation length scales across the domain. This is violated by F3 (X1 far more sensitive than X2/X3) and F8 (X1, X3, X7 should remain near zero). Anisotropic sigma in candidate generation partially compensates, but the GP kernel itself remains isotropic.

**Classifier signal:** With fewer than 5 positive examples from a 15-sample training set, no classifier reliably learns the high/low boundary. The pipeline detects this via CV accuracy below 60% and treats it as a failure condition.

**Surrogate generalisability:** The pipeline's core assumption is that the GP generalises beyond training data. When R²=1.0 at small n, this assumption is provably violated. The ATB override rule is the explicit response.

### Constraints and failure modes

**GP overfitting (R²=1.0):** The most frequent failure mode in this project. Occurs in 6 of 8 functions by W10. A GP with R²=1.0 produces EI values that point to candidates near observed good points but without genuine predictive validity. Mitigation: ATB override rule.

**Boundary drift:** For F3 and F8, the GP repeatedly pulled candidates away from confirmed boundary structure despite anisotropic sigma constraints. F3's X1 drifted from 0.998 (W6 ATB) to 0.750 (W9) and 0.929 (W10). The GP's learned gradient, when distorted by regression weeks, can overpower the candidate generation constraints.

**Classifier collapse with imbalanced positives:** TOP_PERCENTILE=30 on n=15 yields 4–5 positive labels. Decision Tree and Random Forest can overfit perfectly to these few examples; SVM and Logistic Regression can underfit entirely. Both failure modes pass through silently unless CV accuracy is checked.

**Single-point budget constraint:** One query per function per week means a single poor submission can set a function back by 2–3 recovery weeks. F3 W8 (score: -0.113) and F4 W5 (score: -2.457) are examples where a single GP-suggested coordinate caused significant regression.

**Dimensionality scaling:** GP complexity is O(n³) in training sample count. At n=49 samples (F8) the pipeline remains fast. At n=200+ and d=20+, sparse GP approximations (e.g. inducing point methods from Titsias 2009) would be required.

---

## Ethical considerations

### Bias risks

The pipeline has no demographic bias in the conventional sense — it optimises mathematical functions, not decisions about people. However, it has an analogous form of structural bias: **surrogate bias**. The GP's prior (zero mean, Matérn kernel) encodes assumptions about function smoothness and stationarity. For functions that violate these assumptions (F1, F3, F8), the surrogate systematically misrepresents the landscape, directing queries toward regions that look promising to the GP but are empirically poor. This is equivalent to a credit scoring model that systematically underestimates risk for a specific demographic because its training data was unrepresentative.

### Transparency

Following the Datatonic model card example from Mini-lesson 21.2, transparency is implemented at three levels:

**Code transparency:** Every pipeline step is numbered, documented, and produces printed output. Steps 5 (classifier CV), 9 (GP fit), 10 (acquisition), and 14 (submission) all print diagnostic information that allows a reader to verify the decision chain without running the notebook.

**Data transparency:** Output `.npy` files contain only portal-returned values — no imputed or estimated scores. The data integrity note appears at the top of every notebook. The `week_log_FX.json` files used for visualisation are explicitly separated from the GP training data.

**Decision transparency:** The ATB override decision is documented in the submission text file (`BBO_W11_Submissions.txt`) alongside the GP output it replaced, the R² value that triggered the override, and the rationale for each function. This creates an auditable record of every human intervention in the pipeline.

### Recommendations for responsible use

Following the Datatonic card's recommendation for "regular retraining and fairness audits":

- **Regular GP diagnostics:** R² should be checked at every iteration. R²=1.0 should trigger the override evaluation, not be treated as a positive signal.
- **Surrogate validation:** Before acting on any GP-suggested candidate, compare its coordinates against the full submission history. A candidate in a region never previously explored with high GP confidence is likely an artefact of overfitting, not a genuine discovery.
- **Document all overrides:** Every instance where the human operator chose not to follow the GP should be recorded with the specific signal that triggered the decision. This log would allow a future practitioner to tune the override threshold empirically.
- **Use as decision aid, not sole determinant:** Consistent with the Datatonic card's limitation statement, this pipeline should inform but not automate submission decisions — particularly in W12 where the final query budget is exhausted with one submission.

### Reproducibility and real-world adaptation

The full pipeline is public at [github.com/kennelm2025/Mikes-Capstone](https://github.com/kennelm2025/Mikes-Capstone). Every input coordinate submitted and every output received is recorded. A researcher with access to the Imperial College portal could reproduce every weekly decision from the stored `.npy` files and notebook configurations alone.

For real-world adaptation — materials discovery, drug dosing optimisation, engineering parameter tuning — the pipeline's structure transfers directly. The domain-specific changes required are: (1) replace the Imperial College oracle with the real evaluation function, (2) adjust `TOP_PERCENTILE` to reflect the expected fraction of good regions, (3) recalibrate `ANISO_SIGMA` based on domain knowledge about which parameters are most sensitive. The ethical requirement that each override decision is documented becomes more significant in proportion to the stakes of the application.

---

## Distribution

| Property | Value |
|----------|-------|
| **Availability** | Public GitHub repository — model card, notebooks, data files, and submission records all open |
| **Oracle functions** | Proprietary to Imperial College BBO Capstone system — function definitions not available |
| **Data licence** | Student-generated inputs freely shareable; oracle outputs provided under Imperial College course terms |
| **Version history** | W7 model card (initial), W8 update, W11 final — all committed to `/capstone-project/week-{n}/` |

---

## References

- Mitchell, M., Wu, S., Zaldivar, A., Barnes, P., Vasserman, L., Hutchinson, B., Spitzer, E., Raji, I.D. and Gebru, T. (2019). Model Cards for Model Reporting. *Proceedings of the Conference on Fairness, Accountability, and Transparency (FAccT '19)*. ACM.
- Rasmussen, C.E. and Williams, C.K.I. (2006). *Gaussian Processes for Machine Learning*. MIT Press.
- Snoek, J., Larochelle, H. and Adams, R.P. (2012). Practical Bayesian Optimisation of Machine Learning Algorithms. *NeurIPS 2012*.
- Eriksson, D., Pearce, M., Gardner, J., Turner, R.D. and Poloczek, M. (2019). Scalable Global Optimisation via Local Bayesian Optimisation (TuRBO). *NeurIPS 2019*.
- Kaplan, J., McCandlish, S., Henighan, T., Brown, T.B., Chess, B., Child, R., Gray, S., Radford, A., Wu, J. and Amodei, D. (2020). Scaling Laws for Neural Language Models. *arXiv:2001.08361*.
- Gebru, T., Morgenstern, J., Vecchione, B., Vaughan, J.W., Daumé III, H., Iii, H.D. and Crawford, K. (2021). Datasheets for Datasets. *Communications of the ACM*, 64(12), 86–92.
- Egan, C. and Latifi, M. (2021). Improving credit default prediction using explainable AI. *(Mini-lesson 21.2 reference)*
- Titsias, M.K. (2009). Variational learning of inducing variables in sparse Gaussian processes. *AISTATS 2009*.

---

*Last updated: April 8, 2026 | Week 11 of 13 | Mike Kennelly | Imperial College London*
*Paired with: `datasheet_bbo_w11.md` | Linked from: `capstone-project/README.md`*
