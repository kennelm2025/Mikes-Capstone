<!--
  ═══════════════════════════════════════════════════════════════════════════
  TRACER TAG: BBO-W13-README-v2-CLAUDE-2026-04-17
  If you can read this line in the GitHub rendered README (View Source), this
  is the correct v2 file. If you don't see this line anywhere, the upload
  did not overwrite. TRACER ID: 0x0417-W13-FIX-LINKS-V2
  ═══════════════════════════════════════════════════════════════════════════
-->

# BBO Capstone — Week 13 FINAL Submission  `[v2 · links fixed]`

### Mike Kennelly · Professional Certificate in ML & AI · Imperial College London · DATA 2026 Cohort

> 🔵 **TRACER NOTICE:** If you can see this blue blockquote at the top, this is the v2 README with all links fixed to use bare filenames (no `week-13/` prefix). The old version did not have this notice. If you don't see this notice, your file is still the old version.

[![Dashboard](https://img.shields.io/badge/Dashboard-Live-brightgreen)](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)
[![Week](https://img.shields.io/badge/Week-13-blue)]()
[![Functions](https://img.shields.io/badge/Functions-8-orange)]()
[![Final](https://img.shields.io/badge/Query-Final-gold)]()
[![Module](https://img.shields.io/badge/Module-23-purple)]()
[![Version](https://img.shields.io/badge/README-v2-brightgreen)]()

---

## What's in this folder

This is the **Week 13 FINAL** submission folder. W13 is the last portal query (Module 24 is reflection-only).

**Parent repository:** [github.com/kennelm2025/Mikes-Capstone](https://github.com/kennelm2025/Mikes-Capstone)  
**Live dashboard:** [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app)

---

## Module 22 + Module 23 Documentation

> **Examiners:** The model card and datasheet required for Module 22, updated for W13 with Module 23 PCA integration.

| Document | Link |
|----------|------|
| **Model Card** — BBO pipeline W13 (Mitchell et al. 2019) | [BBO_W13_Model_Card.md](BBO_W13_Model_Card.md) |
| **Datasheet** — BBO oracle dataset W13 (Gebru et al. 2021) | [BBO_W13_Data_Card.md](BBO_W13_Data_Card.md) |
| **W13 Submissions** — all 8 strings in portal format | [W13_Submissions.txt](W13_Submissions.txt) |
| **Live Dashboard for BBO Capstone** | [mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app](https://mikes-capstone-drgbnucptufy7tjbdrnvta.streamlit.app) |

> 🔵 **TRACER CHECK:** The links in the table above should show as `BBO_W13_Model_Card.md` (no `week-13/` prefix). If GitHub shows them as `week-13/BBO_W13_Model_Card.md`, the file was not overwritten.

---

## W12 Portal Results (returned by portal at start of W13)

| Fn | W12 Result | Prior ATB | ATB Wk | Outcome | W13 Implication |
|----|-----------|-----------|--------|---------|-----------------|
| F1 | 8.968e-07 | 8.968e-07 | W11 | **= ATB exact (deterministic)** | Replicate W11/W12 coords |
| F2 | **0.688004** | 0.6497 | W5 | **NEW ATB ★ (+0.038)** | Replicate W12 coords |
| F3 | −0.00713 | −0.000707 | W11 | Regressed (oracle noise σ~0.003) | Replicate W11 ATB |
| F4 | 0.237590 | 0.237591 | W2 | **= ATB exact (triple-confirmed)** | Replicate W2 ATB |
| F5 | 8662.4825 | 8662.4825 | W9 | **= ATB exact (triple-confirmed corner)** | Replicate corner |
| F6 | −0.088265 | 0.036017 | W9 | Regressed (oracle noise σ~0.063 — HIGHEST) | Replicate W9 ATB |
| F7 | **2.893857** | 2.8501 | W11 | **NEW ATB ★ (7th consecutive)** | GP pipeline with W12 ATB fallback |
| F8 | 9.831962 | 9.8320 | W2 | **= ATB exact (W2+W12, 10-week gap)** | Replicate W2/W12 ATB |

**★ New ATBs set at W12:** F2 (two-basin upside captured) · F7 (7th consecutive improvement)  
**Deterministic confirmations:** F1 (exact), F4 (triple), F5 (triple), F8 (10-week gap) — these four oracles are now confirmed noise-free.  
**Stochastic regressions:** F3 (σ~0.003) · F6 (σ~0.063) — noise is in the oracle, not the input.

---

## W13 Results — W1–W13 Full History

| Fn | Dims | ATB | ATB Wk | W12 Score | W12 Status | W13 Submitted | Strategy |
|----|------|-----|--------|-----------|------------|---------------|----------|
| F1 | 2D | **8.968e-07** | W11 ★ | 8.968e-07 | = ATB | `0.684200-0.704200` | ATB override |
| F2 | 2D | **0.688004** | W12 ★ | 0.688004 | NEW ATB | `0.710068-0.161630` | ATB override |
| F3 | 3D | **−0.000707** | W11 ★ | −0.00713 | Regressed | `0.998126-0.621218-0.453080` | ATB override |
| F4 | 4D | 0.237591 | W2 | 0.237590 | = ATB | `0.439249-0.414994-0.384687-0.397917` | ATB override |
| F5 | 4D | **8662.4825** | W9 | 8662.4825 | = ATB | `1.000000-1.000000-1.000000-1.000000` | ATB override |
| F6 | 5D | 0.036017 | W9 | −0.088265 | Regressed | `0.406643-0.339495-0.634775-0.769397-0.115269` | ATB override |
| F7 | 6D | **2.893857** | W12 ★ | 2.893857 | NEW ATB | `0.179941-0.306897-0.455194-0.249116-0.295985-0.730083` | **GP pipeline + ATB fallback** |
| F8 | 8D | 9.831962 | W2 | 9.831962 | = ATB | `0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212` | ATB override |

**F7 bold** = the only GP-pipeline function. Step 14 applies 3 trust conditions on the final round; fallback to W12 ATB if any condition fails.

---

## W13 Strategy Summary

### The Final-Round Decision Rule

W13 is the last query. The governing rule applied across all 8 functions:

> **Rule:** If prior week did not beat ATB → submit exact ATB coordinates unchanged.  
> **Exception:** F7 only — run GP pipeline on W13 npy. Submit GP EI candidate **only if ALL 3 trust conditions pass**: μ > ATB (2.893857), R² < 0.999999 (not pure memorisation), AND μ − ATB > σ/2 (predicted gain exceeds half GP uncertainty). Otherwise fall back to W12 ATB coords.  
> **Rationale:** On the final round with no recovery, a GP predicting a modest improvement with comparable uncertainty is not sufficient evidence to override a confirmed best. Risk-minimisation governs.

### Module 22 Clustering — Carried forward from W12

Module 22 hierarchical clustering on the 12-round history is retained as the **cluster-typology** layer of the analysis. It tells us *what kind* of high-output region each function has (tight static attractor, two-zone basin, trending ridge, zero-boundary, corner). Module 23 PCA (below) layers variance-direction vocabulary on top of this.

### Module 23 PCA — New at W13

Module 23 introduces **PCA-style variance analysis** as a second validation layer for W13 decisions. For each function, PCA is computed on (a) the full 12-round dataset and (b) a function-specific "confirmed good" subset (top-output or near-ATB). The resulting scree plots, explained-variance ratios and per-dimension variance classify each function into a **Module 23 case type**:

| Function | Module 23 case | Effective dim | Flat PCs | Primary lens |
|---|---|---|---|---|
| F1 | Tight attractor | — | — | — |
| F2 | Kernel-PCA (non-linear two-basin) | 2 (kernel) | 0 | Video 1 (kernel) |
| F3 | Scree / 1 flat PC (X1 locked at 1.0) | 2 | 1 | Video 3 (scree) |
| F4 | Isolated basin (all dims narrow-active) | 4 | 0 | Video 5 (centring) |
| F5 | **Flat-scree / corner** (all dims locked) | ≈0 | ≈4 | **Video 3 (secondary)** |
| F6 | Threshold / dominant-PC (X5) | 5 | 0 | Video 2 (max variance) |
| F7 | Trending ridge (1-dominant-PC) | 1 | 0 | Video 2 + Video 7 |
| **F8** | **Zero-boundary / 3 flat PCs** | **5** | **3** | **Video 3 (PRIMARY)** |

**Primary Module 23 showcase: F8** — X1=X3=X7=0 in the near-ATB subset yield 3 flat PCs, reducing the nominal 8D problem to an effective 5D one. The scree plot on F8's near-ATB subset captures 93% of variance in PC1 with PCs 6–8 literally flat.

**Secondary Module 23 showcase: F5** — the confirmed-corner subset has **total variance ≈ 0.0001**; all 4 PCs essentially flat. The cleanest "everything collapses to a point" scree in the capstone.

**Tertiary showcase: F7** — ridge-only PCA (top-7 W6–W12 points) shows PC1 share of **0.900** and |corr(PC1, y)| = **0.976**, confirming the 6D ridge has only 1 meaningful degree of freedom. This is the PCA-based justification for trusting GP extrapolation on F7 while overriding on all others.

### W13 Per-Function Settings

| Fn | Strategy | ANISO sigma | EXPLOIT_RATIO | Cluster + PCA lens | Rationale |
|----|----------|-------------|---------------|--------------------|-----------|
| F1 | ATB OVERRIDE | [0.015, 0.015] | 0.85 | Tight Attractor | W11/W12 exact match. Flat near-zero landscape. |
| F2 | ATB OVERRIDE | [0.012, 0.008] | 0.92 | ★ Two-Zone (kernel-PCA) | W12 NEW ATB in LOW-X2 basin; replay W12 coords. |
| F3 | ATB OVERRIDE | [0.005, 0.020, 0.025] | 0.92 | Tight + 1 flat PC | W12 regression = noise σ~0.003; W11 ATB still best. |
| F4 | ATB OVERRIDE | [0.012×4] | 0.92 | Isolated basin | Triple-confirmed deterministic basin. |
| F5 | ATB OVERRIDE | [0.005×4] | 0.95 | Corner + flat-scree | Triple-confirmed [1,1,1,1]. Cleanest PCA. |
| F6 | ATB OVERRIDE | [0.015×4, 0.008] | 0.92 | Threshold / dominant-PC | Highest noise σ~0.063 is oracle-side. |
| F7 | **GP PIPELINE + fallback** | [0.015, 0.012×4, 0.015] | 0.92 | ★ Trending Ridge | 7 consecutive improvements; step size decelerating. |
| F8 | ATB OVERRIDE | [0.006, 0.015, 0.006, 0.015×4, 0.006, 0.015] | 0.95 | ★ Zero-Boundary (3 flat PCs) | W2+W12 = 10-week-gap exact match. PRIMARY PCA case. |

The F8 `ANISO_SIGMA` **IS the Module 23 insight operationalised**: X1, X3, X7 (the 3 flat PCs) get σ=0.006 near-zero exploration; the 5 active dims get σ=0.015 normal exploration. Locked dims get small sigmas, active dims get normal ones.

---

## Oracle Stochasticity — Quantified at W12

W12 produced the first unambiguous evidence of oracle stochasticity on 3 of the 8 functions. Identical coordinate replays returned different scalar values, while the other 5 functions remained deterministic across 2+ exact replays.

| Fn | Empirical σ | Evidence | Status |
|----|-------------|----------|--------|
| F1 | — | 1 replay (W11 → W12 exact match) | Deterministic |
| F2 | ~0.035 | W5: 0.6497 · W9: 0.6497 · W11: 0.6090 · W12: 0.688004 | Stochastic (upside captured) |
| F3 | ~0.003 | W11: −0.000707 · W12: −0.00713 | Stochastic |
| F4 | — | W2 + W11 + W12 all = 0.237591 exact | Deterministic (triple) |
| F5 | — | W9 + W11 + W12 all = 8662.4825 exact | Deterministic (triple) |
| F6 | **~0.063** | W9: +0.036 · W11: −0.010 · W12: −0.088 | Stochastic (HIGHEST) |
| F7 | — | No exact replays (trending) | Unknown |
| F8 | — | W2 + W12 exact match across 10-week gap | Deterministic (10-wk gap) |

**Consequence for W13:** Noise is in the oracle, not the input. Best-known input still dominates all alternatives by expected value. This is a stronger argument for ATB override than "no better point found" — it says: *even if a new point had higher GP μ, the realised output would be drawn from the same noise distribution*. Exact replication is the risk-minimising strategy.

---

## W13 GP Diagnostics (run against W13 npy)

| Fn | CV Winner | GP R² | GP μ max | GP σ at max | Decision |
|----|-----------|-------|----------|-------------|----------|
| F1 | Random Forest | ~1.0 | ≈0 | small | ATB override (EI~0) |
| F2 | Random Forest | ~1.0 | 0.6439 | 0.1158 | ATB override (replay W12 NEW ATB) |
| F3 | NN-Small | ~1.0 | 0.0013 | 0.0166 | ATB override (noise σ~0.003) |
| F4 | Random Forest | ~1.0 | 0.234 | 2.25 | ATB override (triple-confirmed) |
| F5 | Linear SVM | ~1.0 | 8595.95 | 37.92 | ATB override (corner structural) |
| F6 | Random Forest | ~1.0 | 0.048 | 0.161 | ATB override (noise σ>gain) |
| F7 | Random Forest | ~1.0 | 2.856 | 0.091 | **Evaluate 3 trust conditions** |
| F8 | Decision Tree | ~1.0 | 10.14 | 0.18 | ATB override (10-wk gap match) |

**GP pipeline for F7 — W13 trust conditions:**

1. `GP μ > 2.893857` (beat new ATB)
2. `R² < 0.999999` (not pure memorisation)
3. `μ − ATB > σ/2` (gain exceeds half uncertainty — stricter final-round condition)

**If ALL pass:** submit GP EI candidate. **If ANY fails:** fall back to W12 ATB coords `0.179941-0.306897-0.455194-0.249116-0.295985-0.730083`.

In author-execution, **all 3 conditions failed** (μ = 2.856 < ATB; R² = 1.000000 pure memorisation; gain = −0.038 < σ/2 = 0.046) → FALLBACK fired. The F7 ridge appears to be saturating (W11→W12 step = 0.044, smallest positive step).

---

## Pipeline

W13 notebooks add **Step 5C — Module 23 PCA variance analysis** between Step 5B (CNN inspection) and Step 6 (Refit & Visualise), taking the notebook from 29 cells (W12) to 31 cells (W13). Step 14 (Final Submission Decision) and Step 15 (Hyperparameter Record) are also new at W13.

| Step | Description |
|------|-------------|
| 0 | Config & Strategy — W13 ATB coords, ANISO_SIGMA, cluster + PCA lens documented |
| 1–3 | Imports, Load, History (W1–W12) + **Module 22 clustering analysis retained** |
| 4 | Binary Labels (top 30%) |
| 5 / 5B | CV Model Comparison (8 classifiers) + CNN-1D Inspection (Module 17) |
| **5C** | **★ NEW W13: Module 23 PCA variance analysis — scree plots, flat-PC detection, effective dim** |
| 6–7B | Refit, CV Chart, Why-Winner |
| 8 | Candidate Generation (anisotropic sigma, exploit/explore split) |
| 9–10 | GP Fit (Matérn ν=5/2) + Acquisition Functions (EI + UCB) |
| 11 | Per-Dimension sensitivity curves |
| 12 | GP acquisition surfaces |
| 13 | Submission dashboard |
| **14** | **★ NEW W13: Final Submission Decision — ATB override OR GP decision logic (F7)** |
| **15** | **★ NEW W13: Hyperparameter Record (JSON + TXT with PCA block)** |

**F7 Step 14 difference:** unique to F7, Step 14 contains conditional logic evaluating the 3 trust conditions and selecting GP EI coords OR W12 ATB fallback. All other notebooks have a deterministic ATB-override Step 14.

---

## W13 Deliverables (this folder)

| File | Description |
|------|-------------|
| [BBO_W13_Model_Card.md](BBO_W13_Model_Card.md) | Model card — Mitchell et al. 2019 framework, W13 final + Module 23 |
| [BBO_W13_Data_Card.md](BBO_W13_Data_Card.md) | Data card — Gebru et al. 2021 framework, W13 final + oracle noise |
| [W13_Submissions.txt](W13_Submissions.txt) | All 8 W13 submission strings in portal format |
| [Capstone_F1_W13.ipynb](Capstone_F1_W13.ipynb) | F1 W13 — Tight Attractor, ATB override |
| [Capstone_F2_W13.ipynb](Capstone_F2_W13.ipynb) | F2 W13 — **Two-Zone + Kernel PCA**, ATB override |
| [Capstone_F3_W13.ipynb](Capstone_F3_W13.ipynb) | F3 W13 — 1 flat PC, ATB override |
| [Capstone_F4_W13.ipynb](Capstone_F4_W13.ipynb) | F4 W13 — Isolated Basin, ATB override |
| [Capstone_F5_W13.ipynb](Capstone_F5_W13.ipynb) | F5 W13 — **Flat-scree / Corner**, ATB override |
| [Capstone_F6_W13.ipynb](Capstone_F6_W13.ipynb) | F6 W13 — Threshold / Dominant-PC, ATB override |
| [Capstone_F7_W13.ipynb](Capstone_F7_W13.ipynb) | F7 W13 — **Trending Ridge**, GP pipeline + fallback |
| [Capstone_F8_W13.ipynb](Capstone_F8_W13.ipynb) | F8 W13 — **Zero-Boundary / 3 flat PCs (PRIMARY Module 23)** |

Each notebook run also produces, in this folder:
- `fN_w13_inputs.npy` / `fN_w13_outputs.npy` — W13 npy data (appended from W12)
- `FN_W13_hyperparameters.json` — captured config + PCA analysis block
- `FN_W13_run_report.txt` — notebook run report
- `FN_W13_submission.txt` / `FN_W13_submission.npy` — final submission string + vector
- `FN_W13_Step3_History.*` — history plot
- `FN_W13_Step5C_PCA.*` — PCA variance analysis plot
- `FN_W13_Step12_GPSurfaces.*` — GP acquisition surfaces

---

## Academic Basis

| Reference | Application |
|-----------|-------------|
| Jones et al. (1998) | Expected Improvement acquisition function |
| Rasmussen & Williams (2006) | Gaussian Process fundamentals |
| Srinivas et al. (2010) | GP-UCB acquisition |
| Eriksson et al. (2019) | TuRBO trust regions — exploit ratio strategy |
| Cybenko (1989) | Universal approximation — NN classifier |
| Goodfellow et al. (2016) | CNN-1D foundations (Module 17) |
| Kaplan et al. (2020) | Scaling laws — diminishing returns framing |
| Wei et al. (2022) | Emergent capabilities — F5 corner emergence |
| Hoffmann et al. (2022) | Compute-optimal scaling — query budget framing |
| Mitchell et al. (2019) | Model Cards for Model Reporting — Module 21/22 |
| Gebru et al. (2021) | Datasheets for Datasets — Module 21/22 |
| Shannon (1948) | Information theory — uncertainty framing |
| Bender et al. (2021) | Stochastic parrots — Module 20 LLM risks |
| Ward et al. (2023) | Hierarchical clustering in optimisation landscapes — Module 22 |
| **Jolliffe (2002) / Pearson (1901)** | **PCA foundations — Module 23** |
| **Tagliabue / "Netflix Prize" lesson** | **Production-robust model selection vs offline winner — Module 23 V8** |

---

*W1–W13 FINAL · BBO Optimisation · Imperial College London · DATA 2026 Cohort · Mike Kennelly*

<!--
  ═══════════════════════════════════════════════════════════════════════════
  TRACER FOOTER: BBO-W13-README-v2-CLAUDE-2026-04-17-END
  TRACER ID: 0x0417-W13-FIX-LINKS-V2
  ═══════════════════════════════════════════════════════════════════════════
-->
