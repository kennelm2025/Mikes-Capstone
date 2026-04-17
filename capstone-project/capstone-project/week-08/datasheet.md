# Datasheet — BBO Capstone Dataset

**Project:** Black-Box Optimisation Capstone  
**Author:** Mike Kennelly — Imperial College London, ML & AI Professional Certificate  
**Week:** 8 of 13 | Data period: October 2025 – May 2026

---

## Motivation

**For what purpose was the dataset created?**  
The dataset was created to support a structured 13-week Bayesian Optimisation challenge. Each week, participants submit a coordinate guess for each of 8 unknown objective functions and receive back the corresponding output value. The dataset grows by one observation per function per week, simulating real-world sequential black-box optimisation — where each experiment is costly and the function form is unknown.

**Who created the dataset and on behalf of which entity?**  
The dataset is generated and maintained by the course team at Imperial College Business School's Executive Education programme (IMP-PCMLAI — Professional Certificate in Machine Learning & AI). The oracle functions are server-side black-box computations; participants never see the function definitions. The dataset was created as a pedagogical tool to teach Bayesian Optimisation under realistic experimental constraints.

**Who funded the creation of the dataset?**  
Imperial College London, as part of the fee-funded Professional Certificate in ML & AI programme.

---

## Composition

**What do the instances represent?**  
Each instance is a single query-response pair: an n-dimensional input coordinate (sampled from [0,1]ⁿ) and the corresponding scalar output value returned by the server-side oracle. There is one instance per function per week.

**How many instances are there?**

| Function | Dimensions | Samples at W8 | W7 Score | ATB | Notes |
|----------|-----------|--------------|---------|-----|-------|
| F1 | 2D | 16 | ≈0 | 8.84e-7 (W2) | Flat landscape — 7 consecutive near-zero weeks |
| F2 | 2D | 16 | 0.5338 | 0.6497 (W5) | Clear peak structure around [0.71, 0.16] |
| F3 | 3D | 21 | −0.00534 ★ | −0.00534 (W7) | X1=1.0 boundary confirmed; new best W7 |
| F4 | 4D | 36 | −0.2651 | 0.2376 (W2) | W2 inject failed; switching to exploration |
| F5 | 4D | 26 | 7596.79 ★ | 7596.79 (W7) | Massive new best; X2–X4 saturated at 1.0 |
| F6 | 5D | 26 | −0.3422 | −0.1727 (W6) | W7 expand failed; returning to W6 region |
| F7 | 6D | 36 | 2.4134 ★ | 2.4134 (W7) | Anisotropic σ confirmed; X1 dominant |
| F8 | 8D | 46 | 9.8251 | 9.8320 (W2) | 0.007 from ATB; boundary pattern held |

Total observations at W8: **223 query-response pairs** across 8 functions (215 at W7 + 8 W7 submissions).

**★** = new all-time best set in W7

**Is there any missing data?**  
For F8, the best-ever observed point (W2=9.832) is not correctly represented in the `.npy` files stored by the platform; it has been recovered from submission confirmation emails and injected via the `week_log_F8.json` override mechanism. F4's W2 best (0.2376) was also subject to an inject override, but this strategy was abandoned in W8 after W7 confirmed the coordinates are not reproducible.

**Does the dataset contain confidential data?**  
No personally identifiable information is present. The function definitions remain confidential to Imperial College — participants have no access to the underlying mathematical form of any function.

---

## Collection Process

**How was the data acquired?**  
Data is collected through the IMP-PCMLAI Capstone Project Portal. Each week, participants submit n-dimensional coordinates (one per function) through the portal web interface. The portal evaluates the coordinates against the server-side oracle and returns output values by email, typically within 24–48 hours. Processed results are also visible on the portal Dashboard.

**Sampling strategy?**  
The pipeline generates 10,000 candidate points per function per week using a hybrid strategy:
- **Exploitation candidates** — Gaussian samples centred on the current best-known point (sigma adapted weekly using TuRBO-inspired rules; anisotropic per-dimension for F7)
- **Exploration candidates** — Sobol quasi-random sequences for space-filling coverage

The GP + EI acquisition function then selects the single best candidate to submit.

**Over what time frame was the data collected?**  
Week 1 data collected approximately October 2025; collection continues through approximately May 2026 (Week 13). At W8, eight weeks of data have been collected (W1–W8, pending portal return).

---

## Preprocessing / Cleaning / Labelling

**Was any preprocessing done?**  
Yes. The following transformations are applied within each weekly notebook:

1. **Binary labelling** — outputs are labelled class 1 (HIGH) or class 0 (LOW) by thresholding at the 70th percentile. This converts the regression problem into a classification problem for the ensemble filter stage.
2. **Normalisation** — GP training uses `normalize_y=True` to standardise the output scale, stabilising kernel hyperparameter optimisation when the output range is large (e.g., F5 values in the thousands).
3. **Week log injection** — for F8 (and previously F4), missing best-ever points are prepended from the verified `week_log_FX.json` record before GP fitting.
4. **Candidate clipping** — all generated candidates are clipped to [0,1]ⁿ to respect the domain bounds.

**Notable W8 change:** F4 inject override removed. W7 confirmed the W2 coordinates at [0.439,0.415,0.385,0.398] do not reproduce the +0.2376 score. No override is applied to F4 from W8 onward.

**Was raw data saved in addition to preprocessed data?**  
Yes. Raw `.npy` files (`fX_wY_inputs.npy`, `fX_wY_outputs.npy`) from the platform are stored unmodified. The `week_log_FX.json` override records are stored separately. Both are committed to the GitHub repository.

---

## Uses

**What other tasks could this dataset be used for?**  
- Benchmarking Bayesian Optimisation algorithms on real (non-synthetic) black-box functions with known query budgets
- Studying the effect of sample size growth on surrogate model quality week-on-week
- Evaluating classifier pre-filtering as a scalability technique for high-dimensional GP
- Analysing anisotropic acquisition strategies in structured landscapes (F7 case study)
- Analysing the empirical performance of EI vs UCB acquisition functions under small-n conditions

**What might impact future uses?**  
- The functions are purpose-built for the course — they may not reflect industrial or scientific black-box functions
- Sample sizes are extremely small (n=16 to n=46 at W8) relative to dimensionality (2D–8D). Models trained on this data overfit easily, and classification CV accuracy should be interpreted cautiously
- The domain [0,1]ⁿ is normalised — absolute coordinate values have no physical meaning

**Are there tasks for which the dataset should not be used?**  
This dataset should not be used for any claims about real-world physical or engineering systems. The oracle functions are pedagogical constructs, not real-world measurements. It should not be used to train production models for safety-critical applications.

---

## Distribution

**How has the dataset been distributed?**  
The input/output `.npy` files and `week_log_FX.json` records are published on GitHub at [github.com/kennelm2025/Mikes-Capstone](https://github.com/kennelm2025/Mikes-Capstone) under the `capstone-project/week-XX/` folder structure.

**Is it subject to any copyright or IP licence?**  
The oracle function definitions and portal infrastructure are proprietary to Imperial College London. The collected query-response pairs and all analysis code are the work of Mike Kennelly and are published openly for educational and portfolio purposes. No commercial use is intended.

---

## Maintenance

**Who maintains the dataset?**  
Mike Kennelly maintains the GitHub repository. New weekly data is added after each portal processing cycle (approximately weekly, October 2025 – May 2026). Imperial College maintains the server-side oracle and portal infrastructure.
