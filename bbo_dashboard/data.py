"""
BBO Capstone — all historical data baked in.
No external files needed — works standalone on GitHub / Streamlit Cloud.
Updated: W9 — W8 actuals filled in, W9 submissions pending.

HOW TO UPDATE EACH WEEK:
  1. Increment CURRENT_WEEK.
  2. Replace trailing None in each SCORES[fn] with the new actual score.
  3. Append new coords to COORDS[fn].
  4. Append new weekly dict to WEEKLY[fn].
  5. Update STRATEGY[fn] for the new week.
  Nothing else needs touching — all views derive from CURRENT_WEEK.
"""

# ── Single source-of-truth: update this every week ───────────────────────────
CURRENT_WEEK = 9   # ← increment after each portal result

# ── Function metadata ─────────────────────────────────────────────────────────
FUNCTIONS = {
    "F1": {"dims": 2, "objective": "MAXIMISE", "search": "[0,1]²",
           "desc": "2D maximisation — flat near-zero landscape, exploring for signal"},
    "F2": {"dims": 2, "objective": "MAXIMISE", "search": "[0,1]²",
           "desc": "2D maximisation — strong peak near X2≈0.16"},
    "F3": {"dims": 3, "objective": "MAXIMISE", "search": "[0,1]³",
           "desc": "3D — negative-valued; higher (closer to 0) is better; optimum near X1→1"},
    "F4": {"dims": 4, "objective": "MAXIMISE", "search": "[0,1]⁴",
           "desc": "4D maximisation — near-centre optimum ~[0.44,0.41,0.38,0.40]"},
    "F5": {"dims": 4, "objective": "MAXIMISE", "search": "[0,1]⁴",
           "desc": "4D maximisation — extreme range, X2–X4 saturated at 1.0"},
    "F6": {"dims": 5, "objective": "MAXIMISE", "search": "[0,1]⁵",
           "desc": "5D — negative-valued; higher (closer to 0) is better; X4 high / X5 low"},
    "F7": {"dims": 6, "objective": "MAXIMISE", "search": "[0,1]⁶",
           "desc": "6D maximisation — X1 near-zero / X6 elevated pattern"},
    "F8": {"dims": 8, "objective": "MAXIMISE", "search": "[0,1]⁸",
           "desc": "8D maximisation — X1≈0, X3≈0, X8≈0.75 boundary pattern"},
}

# ── Week-by-week scores (W1–W7 actuals) ──────────────────────────────────────
SCORES = {
    "F1": [0.0,        8.84e-7,    5.17e-96,   1.66e-9,    -5.44e-7,   1.67e-85,   -2.22e-17,  1.26e-49,   None],
    "F2": [0.5246,     0.2847,     -0.0298,    0.0188,     0.6497,     0.5844,     0.5338,     0.4926,     None],
    "F3": [-0.01358,   -0.03277,   -0.08337,   -0.13795,   -0.05900,   -0.000707,  -0.00534,   -0.1132,    None],
    "F4": [-2.6271,    0.2376,     -0.9620,    -0.5268,    -2.4571,    -0.1294,    -0.2651,    -0.5542,    None],
    "F5": [60.07,      4062.1,     4890.6,     2913.0,     24.48,      5875.1,     7596.79,    8382.47,    None],
    "F6": [-1.3389,    -0.2372,    -0.8835,    -0.3630,    -1.7662,    -0.1727,    -0.3422,    -0.4006,    None],
    "F7": [0.8085,     1.7392,     1.7358,     1.1399,     0.5763,     2.1190,     2.4134,     2.5982,     None],
    "F8": [9.0093,     9.8320,     9.8188,     9.3341,     8.9560,     9.7741,     9.8251,     9.8021,     None],
}
# W7 actuals will be filled in after Tudor portal results received
# Submission strings:
# F1: 0.582827-0.482269
# F2: 0.688952-0.168811
# F3: 1.000000-0.571651-0.503999
# F4: 0.451762-0.438642-0.400163-0.395091
# F5: 0.937682-1.000000-1.000000-1.000000
# F6: 0.497320-0.294798-0.563080-0.684981-0.129206
# F7: 0.078067-0.385415-0.381193-0.266170-0.353901-0.693102  (anisotropic σ)
# F8: 0.040422-0.331667-0.003668-0.158463-0.396893-0.509806-0.166490-0.780552

# ── GP W7 predictions (mu, sigma from EI winner) ─────────────────────────────
W7_PRED = {
    "F1": {"mu": 0.0,       "sigma": 0.0,      "ucb": 0.0},
    "F2": {"mu": 0.6412,    "sigma": 0.018,    "ucb": 0.677},
    "F3": {"mu": -0.00045,  "sigma": 0.0008,   "ucb": 0.00115},
    "F4": {"mu": 0.2201,    "sigma": 0.022,    "ucb": 0.264},
    "F5": {"mu": 5821.2,    "sigma": 145.5,    "ucb": 6112.2},
    "F6": {"mu": -0.1512,   "sigma": 0.028,    "ucb": -0.095},
    "F7": {"mu": 2.0920,    "sigma": 0.1448,   "ucb": 2.454},
    "F8": {"mu": 9.878,     "sigma": 0.019,    "ucb": 9.916},
}

# ── Submitted coordinates per week (W1–W7) ───────────────────────────────────
COORDS = {
    "F1": [
        [0.0825, 1.5395],
        [0.6842, 0.7042],
        [0.9010, 0.8770],
        [0.6884, 0.7241],
        [0.5323, 0.6306],
        [0.0739, 0.4071],
        [0.582827, 0.482269],
        [0.887104, 0.668800],
        None,  # W9 — pending
    ],
    "F2": [
        [0.5, 0.5],
        [0.65, 0.20],
        [0.62, 0.18],
        [0.68, 0.19],
        [0.710, 0.162],
        [0.703, 0.927],
        [0.688952, 0.168811],
        [0.712753, 0.042543],
        [0.710, 0.162],  # W9 — target coords
    ],
    "F3": [
        [0.40, 0.55, 0.50],
        [0.55, 0.58, 0.48],
        [0.70, 0.60, 0.45],
        [0.85, 0.63, 0.44],
        [0.92, 0.62, 0.46],
        [0.998, 0.621, 0.453],
        [1.000000, 0.571651, 0.503999],
        [0.981542, 0.540570, 0.192008],
        [1.000, 0.572, 0.504],  # W9 — target coords
    ],
    "F4": [
        [0.50, 0.50, 0.50, 0.50],
        [0.439, 0.415, 0.385, 0.398],
        [0.35, 0.42, 0.40, 0.36],
        [0.41, 0.43, 0.38, 0.40],
        [0.30, 0.38, 0.45, 0.30],
        [0.410, 0.438, 0.456, 0.350],
        [0.451762, 0.438642, 0.400163, 0.395091],
        [0.353438, 0.477554, 0.423301, 0.418067],
        None,  # W9 — pending
    ],
    "F5": [
        [0.1199, 0.4986, 0.4779, 0.4947],
        [0.2990, 0.9683, 1.0,    1.0   ],
        [0.8030, 0.9455, 0.9975, 0.9763],
        [0.3547, 0.9182, 0.9966, 0.9454],
        [0.4531, 0.6716, 0.3037, 0.7912],
        [0.7810, 1.0,    1.0,    1.0   ],
        [0.937682, 1.000000, 1.000000, 1.000000],
        [0.985104, 1.000000, 1.000000, 1.000000],
        [1.000, 1.000, 1.000, 1.000],  # W9 — target coords
    ],
    "F6": [
        [0.50, 0.50, 0.50, 0.50, 0.50],
        [0.38, 0.30, 0.55, 0.80, 0.12],
        [0.55, 0.45, 0.60, 0.70, 0.20],
        [0.42, 0.33, 0.58, 0.76, 0.15],
        [0.60, 0.50, 0.65, 0.65, 0.25],
        [0.427, 0.326, 0.598, 0.780, 0.144],
        [0.497320, 0.294798, 0.563080, 0.684981, 0.129206],
        [0.460210, 0.301460, 0.549552, 0.839145, 0.200664],
        [0.427, 0.326, 0.598, 0.780, 0.144],  # W9 — target coords
    ],
    "F7": [
        [0.50, 0.40, 0.35, 0.25, 0.38, 0.65],
        [0.08, 0.41, 0.34, 0.24, 0.38, 0.70],
        [0.06, 0.40, 0.33, 0.23, 0.37, 0.68],
        [0.12, 0.43, 0.36, 0.26, 0.40, 0.66],
        [0.18, 0.45, 0.40, 0.30, 0.42, 0.60],
        [0.055, 0.407, 0.341, 0.242, 0.375, 0.685],
        [0.078067, 0.385415, 0.381193, 0.266170, 0.353901, 0.693102],
        [0.096399, 0.368153, 0.413112, 0.285892, 0.336821, 0.699617],
        [0.096, 0.368, 0.413, 0.286, 0.337, 0.700],  # W9 — target coords
    ],
    "F8": [
        [0.009077, 0.47215,  0.51597,  0.430449, 0.468951, 0.460126, 0.579196, 0.50672 ],
        [0.0,      0.179297, 0.0,      0.071406, 0.92927,  0.459981, 0.0,      0.541212],
        [0.012005, 0.365808, 0.002051, 0.165458, 0.44785,  0.535087, 0.152929, 0.745216],
        [0.069272, 0.717004, 0.001256, 0.001021, 0.132919, 0.479931, 0.048004, 0.722152],
        [0.124245, 0.707381, 0.198569, 0.790421, 0.197258, 0.733195, 0.378511, 0.886089],
        [0.0,      0.387061, 0.068459, 0.146466, 0.368072, 0.66282,  0.291841, 0.727685],
        [0.040422, 0.331667, 0.003668, 0.158463, 0.396893, 0.509806, 0.16649,  0.780552],
        [0.008368, 0.331528, 0.000000, 0.160107, 0.374002, 0.541189, 0.166880, 0.765946],
        [0.000, 0.179, 0.000, 0.071, 0.929, 0.460, 0.000, 0.541],  # W9 — target coords (W2 ATB inject)
    ],
}

# ── W8 Strategy per function ──────────────────────────────────────────────────
STRATEGY = {
    "F1": {
        "action": "EXPLORE — EXTREME WIDENING",
        "exploit_ratio": 0.15,
        "sigma": 0.45,
        "sigma_type": "isotropic",
        "ucb_kappa": 4.0,
        "gp_restarts": 5,
        "turbo": "EXPAND",
        "rationale": (
            "W8 = 1.26e-49 — 8th near-zero. Maximum-entropy search: σ=0.45 (full-space), ratio=0.15. "
            "Wei et al. (2022) / Module 19: high-temperature sampling when landscape is flat."
        ),
        "best_week": "W2 (8.84e-7)",
        "pattern": "Flat — no dominant region found across 8 weeks",
        "w9_submission": "[PENDING]",
    },
    "F2": {
        "action": "RETURN TO W5 ATB — PRECISION LOCK",
        "exploit_ratio": 0.95,
        "sigma": 0.008,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 5,
        "turbo": "SHRINK",
        "rationale": (
            "W8 = 0.4926 — X2 drifted to 0.043. Return to W5 ATB [0.710, 0.162]: σ=0.008 (2σ=±0.016), ratio=0.95. "
            "Kaplan et al. (2020) / Module 19: low-temperature precision sampling."
        ),
        "best_week": "W5 (0.6497)",
        "pattern": "Strong peak at X2≈0.16, X1≈0.71",
        "w9_submission": "[PENDING]",
    },
    "F3": {
        "action": "RETURN TO W7 ATB — PRECISION LOCK",
        "exploit_ratio": 0.92,
        "sigma": 0.015,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 6,
        "turbo": "SHRINK",
        "rationale": (
            "W8 = -0.1132 — X3 drifted to 0.192. Return to W7 ATB region [1.000, 0.572, 0.504]: "
            "σ=0.015, ratio=0.92. Shannon (1948) / Module 19: delimiting context."
        ),
        "best_week": "W6 (-0.000707)",
        "pattern": "X1 → 1.0 boundary dominates; X2/X3 near [0.57, 0.50]",
        "w9_submission": "[PENDING]",
    },
    "F4": {
        "action": "EXPLORE — BOUNDARY CORNERS",
        "exploit_ratio": 0.25,
        "sigma": 0.18,
        "sigma_type": "isotropic",
        "ucb_kappa": 3.5,
        "gp_restarts": 8,
        "turbo": "EXPAND",
        "rationale": (
            "W8 = -0.5542 — exploring. Try boundary corners [0.1×4],[0.9×4]: ratio=0.25, σ=0.18, κ=3.5. "
            "Wei et al. (2022) / Module 19: high-temperature sampling when landscape unknown."
        ),
        "best_week": "W2 (+0.2376)",
        "pattern": "Landscape unknown post-inject — exploring boundary corners",
        "w9_submission": "[PENDING]",
    },
    "F5": {
        "action": "PUSH X1→1.0 — LOCKED AT BOUNDARY",
        "exploit_ratio": 0.92,
        "sigma": 0.025,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "turbo": "SHRINK",
        "rationale": (
            "W8 = 8382.47 NEW ATB. X1=0.985 — push to 1.0: σ=0.025, ratio=0.92. X2-X4 locked. "
            "Kaplan et al. (2020) / Module 19: gradient commit toward confirmed boundary."
        ),
        "best_week": "W8 (8382.47)",
        "pattern": "X2=X3=X4=1.0 boundary; X1 increasing (0.78→0.99)",
        "w9_submission": "[PENDING]",
    },
    "F6": {
        "action": "PRECISION LOCK W6 ATB",
        "exploit_ratio": 0.92,
        "sigma": 0.018,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "turbo": "SHRINK",
        "rationale": (
            "W8 = -0.4006 — drift continued. Pin to W6 ATB [0.427, 0.326, 0.598, 0.780, 0.144]: "
            "σ=0.018, ratio=0.92. Shannon (1948) / Module 19: delimiting context in 5D."
        ),
        "best_week": "W6 (-0.1727)",
        "pattern": "X4 high (~0.78), X5 low (~0.14)",
        "w9_submission": "[PENDING]",
    },
    "F7": {
        "action": "ANISOTROPIC σ TIGHTEN — W8 NEW ATB",
        "exploit_ratio": 0.92,
        "sigma": [0.010, 0.025, 0.025, 0.025, 0.025, 0.025],
        "sigma_type": "anisotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "turbo": "SHRINK",
        "rationale": (
            "W8 = 2.5982 NEW ATB. Tighten: X1 σ=0.010, X2-X6 σ=0.025, ratio=0.92. "
            "Vaswani et al. (2017) / Module 19: per-dimension σ mirrors per-head attention specialisation."
        ),
        "best_week": "W8 (2.5982)",
        "pattern": "X1 near-zero (~0.08-0.10), X6 elevated (~0.69-0.70)",
        "w9_submission": "[PENDING]",
    },
    "F8": {
        "action": "ANISOTROPIC σ — PER-DIM BOUNDARY LOCK",
        "exploit_ratio": 0.92,
        "sigma": [0.008, 0.015, 0.008, 0.030, 0.020, 0.015, 0.008, 0.030],
        "sigma_type": "anisotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 10,
        "turbo": "SHRINK",
        "rationale": (
            "W8 = 9.8021. First anisotropic F8: X1/X3/X7 σ=0.008 (zero-boundary), X5/X8 σ=0.030. "
            "Vaswani et al. (2017) / Module 19: per-dim structure = per-head specialisation."
        ),
        "best_week": "W2 (9.8320)",
        "pattern": "X1≈0, X3≈0, X7≈0 near-zero; X5≈0.93 elevated",
        "w9_submission": "[PENDING]",
    },
}
# ── W9 Summary at a glance ────────────────────────────────────────────────────
W7_GLANCE = {
    "F1": {"true_best": "8.84e-7",   "best_wk": "W2", "w7_score": "-2.22e-17", "strategy": "EXPLORE",                          "override": False},
    "F2": {"true_best": "0.6497",    "best_wk": "W5", "w7_score": "0.5338",    "strategy": "EXPLOIT W5 BEST — PRECISION TIGHTEN","override": False},
    "F3": {"true_best": "-0.00534",  "best_wk": "W7", "w7_score": "-0.00534",  "strategy": "EXPLOIT W7 NEW BEST — TIGHTEN",     "override": False},
    "F4": {"true_best": "+0.2376",   "best_wk": "W2", "w7_score": "-0.2651",   "strategy": "ABANDON INJECT — EXPLORE NEW REGIONS","override": False},
    "F5": {"true_best": "7,596",     "best_wk": "W7", "w7_score": "7,596",     "strategy": "EXPLOIT W7 NEW BEST — PUSH X1 HIGHER","override": False},
    "F6": {"true_best": "-0.1727",   "best_wk": "W6", "w7_score": "-0.3422",   "strategy": "EXPLOIT W6 BEST — RETURN AND TIGHTEN","override": False},
    "F7": {"true_best": "2.4134",    "best_wk": "W7", "w7_score": "2.4134",    "strategy": "EXPLOIT W7 NEW BEST — ANISOTROPIC σ", "override": False},
    "F8": {"true_best": "9.8320",    "best_wk": "W2", "w7_score": "9.8251",    "strategy": "EXPLOIT W2 BEST — PRECISION INJECT",  "override": True},
}

# ── TuRBO sigma adaptation summary (W7→W8) ───────────────────────────────────
TURBO_SUMMARY = {
    "F1": {"sigma_prev": 0.40,  "sigma_cur": 0.45,   "direction": "EXPAND",  "note": "8 weeks near-zero — extreme widen to σ=0.45, ratio=0.15 (Wei et al. 2022)"},
    "F2": {"sigma_prev": 0.010, "sigma_cur": 0.008,  "direction": "SHRINK",  "note": "X2 drift — tightest ever σ=0.008, ratio=0.95 (Kaplan et al. 2020)"},
    "F3": {"sigma_prev": 0.018, "sigma_cur": 0.015,  "direction": "SHRINK",  "note": "X3 drift — return to W7 ATB with σ=0.015 (Shannon 1948)"},
    "F4": {"sigma_prev": 0.12,  "sigma_cur": 0.18,   "direction": "EXPAND",  "note": "Boundary corners — σ=0.18, ratio=0.25 (Wei et al. 2022)"},
    "F5": {"sigma_prev": 0.035, "sigma_cur": 0.025,  "direction": "SHRINK",  "note": "W8 new ATB 8382 — push X1→1.0 with σ=0.025 (Kaplan et al. 2020)"},
    "F6": {"sigma_prev": 0.025, "sigma_cur": 0.018,  "direction": "SHRINK",  "note": "Precision lock W6 ATB with σ=0.018 (Shannon 1948)"},
    "F7": {"sigma_prev": "aniso [0.012,0.028×5]", "sigma_cur": "aniso [0.010,0.025×5]", "direction": "SHRINK",
           "note": "W8 new ATB 2.5982 — tighten both X1 and X2-X6 (Vaswani et al. 2017)"},
    "F8": {"sigma_prev": 0.012, "sigma_cur": "aniso [0.008,0.015,0.008,0.030,0.020,0.015,0.008,0.030]", "direction": "SHRINK",
           "note": "First anisotropic F8 — per-dim zero-boundary structure (Vaswani et al. 2017)"},
}
# ── Winning classifiers per function (W7) ────────────────────────────────────
CLASSIFIERS = {
    "F1": {"name": "Linear SVM",         "cv": 0.750, "std": 0.14, "family": "SVM"},
    "F2": {"name": "Logistic Regression", "cv": 0.833, "std": 0.10, "family": "LogReg"},
    "F3": {"name": "Random Forest",       "cv": 0.833, "std": 0.10, "family": "RF"},
    "F4": {"name": "Linear SVM",          "cv": 0.833, "std": 0.12, "family": "SVM"},
    "F5": {"name": "Random Forest",       "cv": 0.880, "std": 0.08, "family": "RF"},
    "F6": {"name": "Random Forest",       "cv": 0.833, "std": 0.10, "family": "RF"},
    "F7": {"name": "Linear SVM",          "cv": 0.771, "std": 0.19, "family": "SVM"},
    "F8": {"name": "Decision Tree",       "cv": 0.867, "std": 0.08, "family": "DT"},
}

# ── All 8 model CV results per function (W8 actuals for F1-F3, W7 for F4-F8) ─
CV_RESULTS = {
    "F1": [  # W8 actuals from hyperparameters.json
        {"name": "Random Forest",        "cv": 0.875, "std": 0.125, "winner": True},
        {"name": "Decision Tree",        "cv": 0.812, "std": 0.062, "winner": False},
        {"name": "CNN-1D",               "cv": 0.750, "std": 0.125, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.750, "std": 0.000, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.750, "std": 0.125, "winner": False},
        {"name": "Linear SVM",           "cv": 0.688, "std": 0.062, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.688, "std": 0.062, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.188, "std": 0.062, "winner": False},
    ],
    "F2": [  # W8 actuals from run_report.txt
        {"name": "CNN-1D",               "cv": 0.812, "std": 0.062, "winner": True},
        {"name": "Decision Tree",        "cv": 0.750, "std": 0.125, "winner": False},
        {"name": "Random Forest",        "cv": 0.750, "std": 0.000, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.750, "std": 0.125, "winner": False},
        {"name": "Linear SVM",           "cv": 0.688, "std": 0.062, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.688, "std": 0.062, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.500, "std": 0.125, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.500, "std": 0.000, "winner": False},
    ],
    "F3": [  # W8 actuals from run_report.txt
        {"name": "CNN-1D",               "cv": 0.714, "std": 0.202, "winner": True},
        {"name": "Random Forest",        "cv": 0.667, "std": 0.178, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.667, "std": 0.067, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.667, "std": 0.067, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.571, "std": 0.117, "winner": False},
        {"name": "Linear SVM",           "cv": 0.524, "std": 0.178, "winner": False},
        {"name": "Decision Tree",        "cv": 0.524, "std": 0.178, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.429, "std": 0.000, "winner": False},
    ],
    "F4": [  # W7 from model_card.md — Linear SVM winner
        {"name": "Linear SVM",           "cv": 0.833, "std": 0.120, "winner": True},
        {"name": "Random Forest",        "cv": 0.806, "std": 0.085, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.778, "std": 0.096, "winner": False},
        {"name": "CNN-1D",               "cv": 0.750, "std": 0.118, "winner": False},
        {"name": "Decision Tree",        "cv": 0.750, "std": 0.118, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.722, "std": 0.096, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.694, "std": 0.085, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.583, "std": 0.096, "winner": False},
    ],
    "F5": [  # W7 from model_card.md — Random Forest winner
        {"name": "Random Forest",        "cv": 0.880, "std": 0.080, "winner": True},
        {"name": "CNN-1D",               "cv": 0.857, "std": 0.090, "winner": False},
        {"name": "Decision Tree",        "cv": 0.833, "std": 0.100, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.786, "std": 0.085, "winner": False},
        {"name": "Linear SVM",           "cv": 0.762, "std": 0.095, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.738, "std": 0.110, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.714, "std": 0.090, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.667, "std": 0.110, "winner": False},
    ],
    "F6": [  # W7 from model_card.md — Random Forest winner
        {"name": "Random Forest",        "cv": 0.833, "std": 0.100, "winner": True},
        {"name": "CNN-1D",               "cv": 0.810, "std": 0.110, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.786, "std": 0.095, "winner": False},
        {"name": "Decision Tree",        "cv": 0.762, "std": 0.120, "winner": False},
        {"name": "Linear SVM",           "cv": 0.738, "std": 0.105, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.714, "std": 0.095, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.690, "std": 0.110, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.643, "std": 0.120, "winner": False},
    ],
    "F7": [  # W7 from model_card.md — Linear SVM winner
        {"name": "Linear SVM",           "cv": 0.771, "std": 0.190, "winner": True},
        {"name": "CNN-1D",               "cv": 0.743, "std": 0.180, "winner": False},
        {"name": "Random Forest",        "cv": 0.743, "std": 0.160, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.714, "std": 0.175, "winner": False},
        {"name": "Decision Tree",        "cv": 0.686, "std": 0.190, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.657, "std": 0.180, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.629, "std": 0.170, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.571, "std": 0.190, "winner": False},
    ],
    "F8": [  # W7 from model_card.md — Decision Tree winner
        {"name": "Decision Tree",        "cv": 0.867, "std": 0.080, "winner": True},
        {"name": "CNN-1D",               "cv": 0.844, "std": 0.090, "winner": False},
        {"name": "Random Forest",        "cv": 0.822, "std": 0.085, "winner": False},
        {"name": "Logistic Regression",  "cv": 0.800, "std": 0.095, "winner": False},
        {"name": "Linear SVM",           "cv": 0.778, "std": 0.090, "winner": False},
        {"name": "NN-Large (128,64,32)", "cv": 0.756, "std": 0.100, "winner": False},
        {"name": "NN-Medium (64,32)",    "cv": 0.711, "std": 0.095, "winner": False},
        {"name": "NN-Small (16,8)",      "cv": 0.667, "std": 0.110, "winner": False},
    ],
}

# ── Pipeline steps ────────────────────────────────────────────────────────────
PIPELINE_STEPS = [
    {"step": "Step 0",  "title": "Config & Strategy",      "icon": "⚙️",
     "desc": "Sets FUNCTION_ID, WEEK, MAXIMIZE flag, hyperparameters (EXPLOIT_RATIO, EXPLOIT_SIGMA, UCB_KAPPA, GP_RESTARTS). Prints a box summary of the week's plan."},
    {"step": "Step 1",  "title": "Data Load",               "icon": "📂",
     "desc": "Loads f{n}_w{k}_inputs.npy and f{n}_w{k}_outputs.npy. Validates shape and range. Week log overrides inject missing best points for F2, F4, F8."},
    {"step": "Step 2",  "title": "Data Inspection",         "icon": "🔬",
     "desc": "Prints data summary stats: n_samples, n_dims, y range, percentiles. Identifies boundary points (x_i < 0.1 or x_i > 0.9)."},
    {"step": "Step 3",  "title": "History Plot",             "icon": "📊",
     "desc": "Plots submitted y values W1–W6, colour-coded green/red by improvement. Running best line overlaid."},
    {"step": "Step 4",  "title": "Binary Labels",            "icon": "🏷️",
     "desc": "Labels y_train by 70th-percentile threshold. Prints class balance. Used by all 8 classifiers in Step 5."},
    {"step": "Step 5",  "title": "CV Model Comparison",     "icon": "🤖",
     "desc": "Trains 8 models: Linear SVM, Decision Tree, Random Forest, Logistic Regression, NN-Small/Medium/Large, CNN-1D. 5-fold StratifiedKFold CV."},
    {"step": "Step 5B", "title": "CNN Inspection",          "icon": "🔍",
     "desc": "Module 17 learning exercise. Extracts learned Conv1d filter weights (8×2), plots feature map activations for best training point. Identifies which coord pairs CNN found most structurally significant."},
    {"step": "Step 6",  "title": "Refit & Visualise",       "icon": "🎨",
     "desc": "Refits all 8 models on full dataset. Plots P(class=1) distributions for each model across training data."},
    {"step": "Step 7",  "title": "CV Chart & Winner",       "icon": "📈",
     "desc": "Bar chart comparing all 8 models by CV accuracy. Confirms CV winner used in Step 8 candidate filtering."},
    {"step": "Step 7B", "title": "Why This Classifier Won", "icon": "🧠",
     "desc": "Dynamic analysis box: winner family rationale, candidate filter quality stats, boundary dimension analysis, data geometry commentary."},
    {"step": "Step 8",  "title": "Candidate Generation",   "icon": "🎲",
     "desc": "Generates 10,000 candidates: EXPLOIT_RATIO% from Gaussian(best_point, EXPLOIT_SIGMA) — isotropic or anisotropic array. Remainder uniform random. Classifier filters to top 50%."},
    {"step": "Step 9",  "title": "GP Fit",                  "icon": "🌐",
     "desc": "Fits Gaussian Process (Matérn 5/2 kernel) on scaled X_train→y_train. Reports GP R², kernel parameters, fitted length scales per dimension."},
    {"step": "Step 10", "title": "Acquisition Functions",   "icon": "🎯",
     "desc": "Computes EI (Expected Improvement) and UCB (μ + κσ) over filtered candidates. Selects submission = argmax(norm(EI) + norm(UCB))."},
    {"step": "Step 11", "title": "Acquisition Curves",      "icon": "📉",
     "desc": "Per-dimension EI and UCB sweeps. Shows how each dimension contributes to acquisition signal."},
    {"step": "Step 12", "title": "GP Surfaces",             "icon": "🗺️",
     "desc": "2D contour plots of GP μ, σ, EI, UCB over top-2 sensitive dimensions. Best point (★) and submission (◆) overlaid."},
    {"step": "Step 13", "title": "Submission Dashboard",    "icon": "🏆",
     "desc": "Full dashboard: trajectory, submission coords, EI decomposition, dimension sensitivity. Prints final submission string."},
]

WEEKS = [f"W{i+1}" for i in range(CURRENT_WEEK)]

def running_best(scores, maximize):
    result, rb = [], None
    for s in scores:
        if s is None:
            result.append(None); continue
        if rb is None: rb = s
        rb = max(rb, s) if maximize else min(rb, s)
        result.append(rb)
    return result

def get_all_time_best(fn):
    scores = [s for s in SCORES[fn] if s is not None]
    maximize = FUNCTIONS[fn]["objective"] == "MAXIMISE"
    return max(scores) if maximize else min(scores)

def get_sigma_display(fn):
    """Return sigma as displayable string — handles anisotropic arrays."""
    s = STRATEGY[fn]["sigma"]
    if isinstance(s, list):
        return f"[{', '.join(str(v) for v in s)}]"
    return str(s)

# ── Per-week knowledge: what we learned, hyperparams used, experiments ────────
# Indexed as WEEKLY[fn][week_index]  (0=W1 … 6=W7)
WEEKLY = {
    "F1": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Initial week — balanced 50/50 split, moderate sigma, default UCB kappa.",
            "learned": "Score ≈ 0. No detectable structure in the 2D landscape. Function appears near-flat.",
            "experiment": "Baseline run — no special experiment. Established that F1 scores are essentially zero.",
            "submission": "0.0825-1.5395",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.60, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Slight exploit increase after tiny positive signal. Sigma held at 0.10.",
            "learned": "Score 8.84e-7 — infinitesimally above zero. GP length scales suggest no strong gradient direction.",
            "experiment": "Tested UCB vs EI — both agreed near-uniform acquisition. No dominant region.",
            "submission": "0.6842-0.7042",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.12, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Increased kappa to force exploration after two near-zero results.",
            "learned": "Score 5.17e-96 — effectively zero again. Wider kappa found nothing better.",
            "experiment": "High-kappa exploration run. Confirmed: no exploitable structure anywhere in [0,1]².",
            "submission": "0.9010-0.8770",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Reset to baseline after exploration found nothing. Holding pattern.",
            "learned": "Score 1.66e-9 — still effectively zero. Pattern: F1 is a genuinely flat function.",
            "experiment": "Boundary scan — submitted point at [0.69, 0.72] to test mid-range. No improvement.",
            "submission": "0.6884-0.7241",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "No signal to guide strategy. Kept defaults and widened Sobol fraction.",
            "learned": "Score -5.44e-7 — first negative result. GP confirms no positive gradient anywhere.",
            "experiment": "Sobol quasi-random sampling across full [0,1]². Confirmed flat landscape hypothesis.",
            "submission": "0.5323-0.6306",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.40, "sigma": 0.08, "ucb_kappa": 3.0, "gp_restarts": 5},
            "hp_rationale": "Deliberate explore week — low exploit ratio, reduced sigma, high kappa to map unvisited regions.",
            "learned": "Score 1.67e-85 — zero again. All 6 weeks ≈ 0. Function has no exploitable peak in [0,1]².",
            "experiment": "CNN-1D classification — poor signal (75% CV). Confirmed: no coordinate structure to learn.",
            "submission": "0.0739-0.4071",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.40, "sigma": 0.216, "ucb_kappa": 3.0, "gp_restarts": 5},
            "hp_rationale": "σ tripled to 0.216 — near-random width. With 6 zero-weeks, any precision is wasted. Massive explore to find any structure at all.",
            "learned": "Score -2.22e-17 — 7th consecutive near-zero. F1 confirmed as adversarial flat function. No structure detectable in [0,1]².",
            "experiment": "Step 5B CNN inspection: filters learned near-uniform weights — confirms absence of local coordinate structure.",
            "submission": "0.582827-0.482269",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.20, "sigma": 0.40, "ucb_kappa": 4.0, "gp_restarts": 5},
            "hp_rationale": "Extreme explore: ratio=0.20 (80% random), σ=0.40 (near-random width), κ=4.0. EI unreliable near zero — UCB dominates. Final attempt to find any signal before accepting F1 is fundamentally flat.",
            "learned": "Score 1.26e-49 — 8th consecutive near-zero. F1 confirmed adversarial-flat.",
            "experiment": "Maximum-entropy explore σ=0.40, ratio=0.20. Confirmed: F1 is adversarial-flat. All 8 weeks near-zero.",
            "submission": "0.887104-0.668800",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.15, "sigma": 0.45, "ucb_kappa": 4.0, "gp_restarts": 5},
            "hp_rationale": "Extreme explore: ratio=0.15 (85% random), σ=0.45 (effective full-space coverage), κ=4.0. High-temperature sampling — Wei et al. (2022): maximise entropy when landscape is flat. Module 19.",
            "learned": "Awaiting W9 result.",
            "experiment": "Maximum-entropy search. Nine consecutive near-zero weeks — either a spike will be found or F1 is confirmed globally flat.",
            "submission": "[PENDING]",
        },
    ],
    "F2": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline run. Submitted [0.5, 0.5] — centre of space.",
            "learned": "Score 0.5246. Strong first result — clear signal exists near centre-left of X2 axis.",
            "experiment": "Initial centre submission. Established F2 has a positive, well-defined peak.",
            "submission": "0.5000-0.5000",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Exploit W1 signal — moved toward lower X2 based on GP gradient.",
            "learned": "Score 0.2847 — regressed. GP moved too far from W1 region. X2≈0.20 better than X2≈0.50.",
            "experiment": "GP gradient follow. Lesson: gradient can mislead at small n — should stay closer to W1.",
            "submission": "0.6500-0.2000",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.70, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Tighten around X2≈0.18 based on W2 signal.",
            "learned": "Score -0.0298 — worst result yet. GP overfit — moved away from the peak entirely.",
            "experiment": "Tight exploit run. Showed that at n=10 the GP kernel is unreliable — need more exploration.",
            "submission": "0.6200-0.1800",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.60, "sigma": 0.10, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Recovery — widen sigma and increase kappa to escape the bad W3 region.",
            "learned": "Score 0.0188 — recovering but still below W1. X2≈0.19 region is promising.",
            "experiment": "UCB kappa increase to force exploration. Confirmed: peak is near X2=0.16-0.19.",
            "submission": "0.6800-0.1900",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.75, "sigma": 0.06, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Precision tighten around X2=0.162 — highest confidence in this region.",
            "learned": "Score 0.6497 — new all-time best! X2≈0.162, X1≈0.710. Peak clearly identified.",
            "experiment": "Tight σ=0.06 around W4's near-peak coords. Successful precision exploit.",
            "submission": "0.7100-0.1620",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.80, "sigma": 0.04, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Exploit W5 peak tightly — σ=0.04 is very narrow around [0.71, 0.162].",
            "learned": "Score 0.5844 — regression from W5. GP moved slightly off peak. W5 coords remain best.",
            "experiment": "CNN-1D tracking — logistic regression won. F2 boundary is smooth, not coordinate-structured.",
            "submission": "0.7030-0.9270",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.0175, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Inject W5 best [0.710, 0.162] directly into training data. Ultra-tight σ=0.0175 (2σ=±0.035 in [0,1]) to pin around the confirmed peak.",
            "learned": "Score 0.5338 — still below ATB 0.6497. GP didn't fully converge to W5 peak. W8 needs tighter precision.",
            "experiment": "Week log override: W5 coords injected to correct npy gap. Tests whether GP can improve on W5 with denser sampling around peak.",
            "submission": "0.688952-0.168811",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.90, "sigma": 0.010, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Tightest F2 sigma ever: σ=0.010 (2σ=±0.020). Ratio=0.90. W5 best [0.710, 0.162] in npy — no override needed. Target: exceed ATB 0.6497.",
            "learned": "Score 0.4926 — regression. X2 drifted to 0.043 vs ATB 0.162. GP exploration pulled X2 toward lower boundary.",
            "experiment": "Precision tighten σ=0.010. X2 drifted to 0.043 vs ATB 0.162. W9 tightens to σ=0.008, ratio=0.95.",
            "submission": "0.712753-0.042543",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.95, "sigma": 0.008, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Tightest F2 ever: σ=0.008 (2σ=±0.016), ratio=0.95. Low-temperature precision sampling — Kaplan et al. (2020): concentrate mass on confirmed best. Module 19. Pin X2 within [0.146, 0.178].",
            "learned": "Awaiting W9 result.",
            "experiment": "Return precisely to W5 ATB [0.710, 0.162]. Four consecutive regressions — σ=0.008 should prevent X2 drift.",
            "submission": "0.710000-0.162000",
        },
    ],
    "F3": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline. F3 is 3D negative-valued — maximising means approaching zero from below.",
            "learned": "Score -0.01358. Best first-week result across all functions. X1≈0.4 already positive signal.",
            "experiment": "Baseline 3D submit. F3 responds well even to random starting points — smooth landscape.",
            "submission": "0.4000-0.5500-0.5000",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.60, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Exploit W1 — push X1 higher toward boundary.",
            "learned": "Score -0.03277 — regression. Moving X1 further right without enough data was premature.",
            "experiment": "X1 boundary push. Showed X2/X3 also matter — can't optimise X1 in isolation.",
            "submission": "0.5500-0.5800-0.4800",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Continue X1 push with joint X2/X3 refinement.",
            "learned": "Score -0.08337 — worse. GP trajectory not converging. Need to push X1→1.0 more aggressively.",
            "experiment": "Joint 3D optimisation. Lesson: X1=1.0 is the dominant axis — should anchor it first.",
            "submission": "0.7000-0.6000-0.4500",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.70, "sigma": 0.07, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Push X1 harder — submit X1=0.85 to test boundary hypothesis.",
            "learned": "Score -0.13795 — worst yet. Suggests we overshot in X2/X3 direction.",
            "experiment": "X1=0.85 boundary test. Confirmed: X2/X3 near [0.63, 0.44] are the sweet spot.",
            "submission": "0.8500-0.6300-0.4400",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.70, "sigma": 0.07, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Recovery — back to W1-era X1 level with corrected X2/X3.",
            "learned": "Score -0.059 — recovering. GP length scale on X1 very short — confirms X1 is sensitive.",
            "experiment": "Recover strategy worked. X1≈0.92, X2≈0.62, X3≈0.46 is the right neighbourhood.",
            "submission": "0.9200-0.6200-0.4600",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.04, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Tight exploit with X1 pushed to 0.998 — testing the X1→1.0 boundary directly.",
            "learned": "Score -0.000707 — near-perfect! X1=0.998 essentially at the boundary. Monotonic improvement finally achieved.",
            "experiment": "CNN-1D random forest winner. Confirmed X1 boundary is the primary structural feature.",
            "submission": "0.9980-0.6210-0.4530",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.90, "sigma": 0.024, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "σ=0.024 (2σ=±0.048) — very tight. X1=1.0 hit exactly. X2/X3 allowed small refinement.",
            "learned": "Score -0.00534 — NEW ALL-TIME BEST! X1=1.000 exactly on boundary. X2/X3 shifted to [0.572, 0.504]. Monotonic improvement confirmed.",
            "experiment": "Step 5B: CNN filters showed moderate activation on X1 pair — consistent with boundary dominance hypothesis.",
            "submission": "1.000000-0.571651-0.503999",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.90, "sigma": 0.018, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Tighten further: σ=0.018 (vs W7's 0.024). X1 pinned at 1.0. Refine X2/X3 around [0.572, 0.504]. W7 new best in npy — no override needed.",
            "learned": "Score -0.1132 — severe regression. X3 drifted to 0.192 vs proven 0.504. GP exploration overwhelmed exploit cloud.",
            "experiment": "Post-new-best precision tighten σ=0.018. X3 drifted to 0.192 vs proven 0.504. W9 returns to W7 ATB with σ=0.015.",
            "submission": "0.981542-0.540570-0.192008",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.92, "sigma": 0.015, "ucb_kappa": 2.0, "gp_restarts": 6},
            "hp_rationale": "Tighten: σ=0.015 (2σ=±0.030), ratio=0.92. Delimiting context — Shannon (1948): narrow distribution = higher information per query. Module 19. Target: W7 ATB region [1.000, 0.572, 0.504].",
            "learned": "Awaiting W9 result.",
            "experiment": "Return to W7 ATB coords after W8 X3 drift. σ=0.015 confines X3 within ±0.030 of 0.504.",
            "submission": "1.000000-0.572000-0.504000",
        },
    ],
    "F4": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline 4D run. Submitted centre [0.5, 0.5, 0.5, 0.5].",
            "learned": "Score -2.6271 — very negative. Centre is not the optimum. 4D space needs careful navigation.",
            "experiment": "Centre baseline. F4 is harder than F3 — the optimum is not at the centre.",
            "submission": "0.5000-0.5000-0.5000-0.5000",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "GP gradient from W1 pointed toward slightly off-centre region near [0.44, 0.41, 0.38, 0.40].",
            "learned": "Score +0.2376 — massive jump to positive! Near-symmetric off-centre point works. This is the all-time best.",
            "experiment": "GP gradient follow in 4D. Found that a slight off-centre symmetric cluster is optimal.",
            "submission": "0.4390-0.4150-0.3850-0.3980",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Try to refine further around W2 best.",
            "learned": "Score -0.9620 — bad regression. Moved too far from the W2 sweet spot.",
            "experiment": "Refinement attempt. Showed the W2 optimum is a sharp narrow peak — very easy to overshoot.",
            "submission": "0.3500-0.4200-0.4000-0.3600",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Recovery toward W2 region with wider kappa to avoid getting stuck.",
            "learned": "Score -0.5268 — still negative but recovering. The W2 peak is narrow and precise.",
            "experiment": "Recovery run. Confirmed: F4 optimum is fragile — small deviations cause large penalties.",
            "submission": "0.4100-0.4300-0.3800-0.4000",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.60, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Widen search slightly — possible the true optimum is adjacent to W2 coords.",
            "learned": "Score -2.4571 — terrible. Wider search went the wrong direction entirely.",
            "experiment": "Wide search in 4D. Confirmed: W2 coords are unique — do not deviate from [0.439, 0.415, 0.385, 0.398].",
            "submission": "0.3000-0.3800-0.4500-0.3000",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.75, "sigma": 0.05, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Best precision exploit around W2 coords. Week log override injected W2 point.",
            "learned": "Score -0.1294 — improving but still below W2. The exact W2 coordinates remain uniquely best.",
            "experiment": "Week log inject + tight exploit. Showed GP still needs the exact W2 point in training data.",
            "submission": "0.4100-0.4380-0.4560-0.3500",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.0175, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Ultra-tight σ=0.0175 with W2 coords injected. Target: land within ±0.01 of [0.439, 0.415, 0.385, 0.398].",
            "learned": "Score -0.2651 — inject failed conclusively. Despite landing within ±0.015 of W2, score is deeply negative. W2 is not reproducible.",
            "experiment": "Step 5B: CNN detected tight cluster at W2 best coords. Linear SVM won — confirms linear separability of the near-centre peak.",
            "submission": "0.451762-0.438642-0.400163-0.395091",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.35, "sigma": 0.12, "ucb_kappa": 3.5, "gp_restarts": 8},
            "hp_rationale": "Inject ABANDONED. W2 coords confirmed not reproducible. W8 explores new regions: ratio=0.35 (65% random), σ=0.12, κ=3.5. Let GP find a fresh region.",
            "learned": "Score -0.5542 — exploring new regions after inject abandoned. No reproducible structure found yet.",
            "experiment": "Fresh GP-guided search ratio=0.35, σ=0.12. W9 continues boundary-corner exploration with σ=0.18, ratio=0.25.",
            "submission": "0.353438-0.477554-0.423301-0.418067",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.25, "sigma": 0.18, "ucb_kappa": 3.5, "gp_restarts": 8},
            "hp_rationale": "Continue wide explore: ratio=0.25 (75% random), σ=0.18, κ=3.5. High-temperature sampling — Wei et al. (2022): landscape unknown after inject failure. Module 19. Try boundary corners [0.1×4],[0.9×4].",
            "learned": "Awaiting W9 result.",
            "experiment": "Boundary-corner exploration after two wide-explore weeks. Testing whether F4 peak is near the corner of [0,1]⁴.",
            "submission": "[PENDING]",
        },
    ],
    "F5": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline 4D. F5 has extreme scale — scores in thousands.",
            "learned": "Score 60.07. Huge range — F5 is not near-zero like F1-F4. Boundary exploration critical.",
            "experiment": "Initial baseline. Established F5 has extreme positive values — likely exponential response surface.",
            "submission": "0.1199-0.4986-0.4779-0.4947",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "GP pointed toward X2/X3/X4 → 1.0 boundary after W1 signal.",
            "learned": "Score 4,062. Massive jump. X2=X3=X4→1.0 boundary confirmed. X1≈0.30.",
            "experiment": "Boundary push on X2-X4. Confirmed: F5 optimum is at the corner of [0,1]⁴.",
            "submission": "0.2990-0.9683-1.0000-1.0000",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.75, "sigma": 0.06, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Exploit W2 boundary — push X1 toward 0.8, keep X2-X4 at 1.0.",
            "learned": "Score 4,890 — new best. X1≈0.80 better than X1≈0.30. X1 monotonically positive.",
            "experiment": "X1 sweep while X2-X4 locked at 1.0. Confirmed: higher X1 = higher score.",
            "submission": "0.8030-0.9455-0.9975-0.9763",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.70, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Attempt to refine X1 further while keeping boundary pattern.",
            "learned": "Score 2,913 — regression. X1=0.35 is worse. Confirmed X1 should stay ≥ 0.8.",
            "experiment": "X1 lower bound test. Confirmed: X1 < 0.5 destroys performance even with X2-X4=1.0.",
            "submission": "0.3547-0.9182-0.9966-0.9454",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.60, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Wider search after W4 regression — explore X1 range [0.3-0.9].",
            "learned": "Score 24.48 — terrible. Exploration completely missed. W3 coords remain best.",
            "experiment": "Wide X1 explore. Failed. Lesson: stay locked on X1≥0.78, X2-X4=1.0.",
            "submission": "0.4531-0.6716-0.3037-0.7912",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.04, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Return to W3 pattern — tight exploit around [0.78, 1.0, 1.0, 1.0].",
            "learned": "Score 5,875 — new all-time best! X1=0.781 is better than W3's X1=0.803. GP UCB=6,472.",
            "experiment": "CNN-1D tied first at 85.7% — boundary pattern strongly detectable. X2-X4=1.0 is a hard constraint.",
            "submission": "0.7810-1.0000-1.0000-1.0000",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.048, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "σ=0.048 slightly wider than W6 — allows X1 to probe above 0.78 while X2-X4 stay near 1.0. Anisotropic considered but rejected — pulled X1 to 0.718 (below W6).",
            "learned": "Score 7596.79 — NEW ALL-TIME BEST! +1722 vs W6. X1=0.938 — highest ever. X2/X3/X4=1.0 locked. Confirms X1 → 1.0 is the target.",
            "experiment": "Step 5B: CNN feature maps confirmed X2-X4 boundary lock. Anisotropic sigma [0.090, 0.018×3] tested but reverted — wider X1 unexpectedly hurt.",
            "submission": "0.937682-1.000000-1.000000-1.000000",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.90, "sigma": 0.035, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Tighten to σ=0.035 around W7 best. Ratio=0.90. X2-X4 locked at 1.0. Probe X1 ∈ [0.93, 1.0] — can X1=1.0 give further gain?",
            "learned": "Score 8382.47 — NEW ALL-TIME BEST! +785.68 vs W7=7596.79. X1=0.985 approaching the 1.0 boundary.",
            "experiment": "X1 push σ=0.035. W8 hit X1=0.985 → 8382.47 (new ATB). W9 pushes X1 → 1.0 with σ=0.025.",
            "submission": "0.985104-1.000000-1.000000-1.000000",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.92, "sigma": 0.025, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Tighten: σ=0.025, ratio=0.92. Low-temperature gradient commit — Kaplan et al. (2020): scale precision toward confirmed boundary. Module 19. Target: X1 → 1.0, X2-X4 locked at 1.0.",
            "learned": "Awaiting W9 result.",
            "experiment": "Push X1 from 0.985 → 1.0 with tighter σ. W8 confirmed monotonic X1 → 1.0 trend.",
            "submission": "1.000000-1.000000-1.000000-1.000000",
        },
    ],
    "F6": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline 5D. F6 is negative-valued — closer to 0 is better.",
            "learned": "Score -1.3389. Moderate start. 5D space is harder to navigate than lower dims.",
            "experiment": "Baseline 5D submission. Established negative range and initial GP landscape.",
            "submission": "0.5000-0.5000-0.5000-0.5000-0.5000",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "GP gradient from W1 pointed toward X4 high, X5 low.",
            "learned": "Score -0.2372 — massive improvement. X4≈0.80, X5≈0.12 is the key pattern.",
            "experiment": "5D GP gradient follow. Discovered X4-high/X5-low is the dominant structural feature.",
            "submission": "0.3800-0.3000-0.5500-0.8000-0.1200",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.70, "sigma": 0.07, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Exploit W2 pattern with slight refinement of X1-X3.",
            "learned": "Score -0.8835 — bad regression. Moved too far in X1-X3 dimensions.",
            "experiment": "Joint 5D exploit. Showed X1≈0.38-0.43, X2≈0.30-0.33, X3≈0.55-0.60 are correct.",
            "submission": "0.5500-0.4500-0.6000-0.7000-0.2000",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Recovery toward W2 region with wider kappa.",
            "learned": "Score -0.3630 — recovering. W2 pattern confirmed: X4≈0.76, X5≈0.15.",
            "experiment": "Recovery run. F6 landscape confirmed: X4-high (≥0.75), X5-low (≤0.15) are hard constraints.",
            "submission": "0.4200-0.3300-0.5800-0.7600-0.1500",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.09, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Wider search in 5D to probe whether X1-X3 can be further improved.",
            "learned": "Score -1.7662 — catastrophic regression. Wide search in 5D is dangerous — too many wrong directions.",
            "experiment": "5D wide explore. Failed badly. Lesson: in 5D, stay tightly around confirmed best pattern.",
            "submission": "0.6000-0.5000-0.6500-0.6500-0.2500",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.04, "ucb_kappa": 2.5, "gp_restarts": 8},
            "hp_rationale": "Tight return to W2 pattern. Week log override injected W2 best coords.",
            "learned": "Score -0.1727 — new all-time best! X4=0.780, X5=0.144 perfectly locked.",
            "experiment": "CNN-1D random forest winner. X4/X5 boundary pattern cleanly classifiable.",
            "submission": "0.4270-0.3260-0.5980-0.7800-0.1440",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.042, "ucb_kappa": 2.5, "gp_restarts": 8},
            "hp_rationale": "σ=0.042 slight expand from W6's 0.04 — 5D space benefits from a little extra room. X4/X5 constraint maintained.",
            "learned": "Score -0.3422 — bad regression. Expand failed. W7 coords drifted: X4 dropped to 0.685 (vs W6's 0.780), X5 jumped to 0.129. Must return to W6 best.",
            "experiment": "Step 5B: CNN feature maps showed moderate X4/X5 activation. Random forest won again — consistent with W6.",
            "submission": "0.497320-0.294798-0.563080-0.684981-0.129206",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.025, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Return to W6 best [0.427, 0.326, 0.598, 0.780, 0.144]. Tighten: σ=0.025 (vs W7's 0.042). W6 best in npy. X4≈0.78, X5≈0.14 hard constraints.",
            "learned": "Score -0.4006 — regression despite return to W6 region. X4 near 0.839 (vs ATB 0.780), X5 near 0.201 (vs ATB 0.144).",
            "experiment": "Post-expand σ=0.025. W8 still saw X4/X5 drift. W9 precision-locks to ATB [0.427,0.326,0.598,0.780,0.144] with σ=0.018.",
            "submission": "0.460210-0.301460-0.549552-0.839145-0.200664",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.92, "sigma": 0.018, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Precision lock: σ=0.018, ratio=0.92. Delimiting context — Shannon (1948): constrain to known-good region. Module 19. Pin to W6 ATB [0.427, 0.326, 0.598, 0.780, 0.144].",
            "learned": "Awaiting W9 result.",
            "experiment": "Direct lock on W6 ATB coordinates. W8 σ=0.025 still saw X4/X5 drift — W9 tightens further.",
            "submission": "0.427000-0.326000-0.598000-0.780000-0.144000",
        },
    ],
    "F7": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline 6D. F7 is the most complex function in the batch.",
            "learned": "Score 0.8085. Reasonable start for 6D. GP found X1≈0.50, X6≈0.65 pattern.",
            "experiment": "Baseline 6D submission. F7 is positive and non-trivial — exploitable structure exists.",
            "submission": "0.5000-0.4000-0.3500-0.2500-0.3800-0.6500",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Exploit W1 — GP pointed toward X1→0, X6 elevated.",
            "learned": "Score 1.7392 — huge jump! X1≈0.08, X6≈0.70 is the key pattern. X1 near-zero critical.",
            "experiment": "6D GP follow. Discovered the X1→0 boundary is the primary driver of F7 performance.",
            "submission": "0.0800-0.4100-0.3400-0.2400-0.3800-0.7000",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.70, "sigma": 0.07, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Refine around W2 pattern — slightly tighter X1.",
            "learned": "Score 1.7358 — marginal regression. X1=0.06 slightly worse than X1=0.08. Non-monotonic near boundary.",
            "experiment": "X1 tightening test. Showed X1 is non-monotonic near zero — optimal is around X1≈0.05-0.08.",
            "submission": "0.0600-0.4000-0.3300-0.2300-0.3700-0.6800",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Widen slightly — X1 boundary is tricky, need more samples around it.",
            "learned": "Score 1.1399 — regression. X1=0.12 is clearly worse. X1 optimum is 0.05-0.08.",
            "experiment": "X1 boundary width test. Confirmed: X1 below 0.10 is critical — above 0.10 performance drops.",
            "submission": "0.1200-0.4300-0.3600-0.2600-0.4000-0.6600",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.60, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Wider explore — check if X6 can be further elevated.",
            "learned": "Score 0.5763 — worst since W1. Wide explore failed in 6D. X2-X5 mid-range hurts.",
            "experiment": "6D wide explore. Failed badly. Lesson: in 6D, tight X1 is non-negotiable — any deviation destroys score.",
            "submission": "0.1800-0.4500-0.4000-0.3000-0.4200-0.6000",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.04, "ucb_kappa": 2.5, "gp_restarts": 8},
            "hp_rationale": "Return to W2/W3 pattern — tight X1≈0.055, X6≈0.685.",
            "learned": "Score 2.119 — massive new best! +0.38 jump. X1=0.055 is the sweet spot.",
            "experiment": "CNN-1D: filters 3/4 peaked on coord pair [0,1] — confirmed X1 is dominant. Neural Network won CV.",
            "submission": "0.0550-0.4070-0.3410-0.2420-0.3750-0.6850",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.90, "sigma": [0.015, 0.035, 0.035, 0.035, 0.035, 0.035], "ucb_kappa": 2.5, "gp_restarts": 8},
            "hp_rationale": "ANISOTROPIC sigma: X1 tight (σ=0.015, 2σ=±0.030) — CNN filter maps confirmed X1 is dominant. X2-X6 slightly looser (σ=0.035). This is the first anisotropic submission in the capstone.",
            "learned": "Score 2.4134 — NEW ALL-TIME BEST! +0.294 vs W6. Anisotropic sigma confirmed working. X1=0.078 maintained near-zero. W8 tightens further.",
            "experiment": "Step 5B CNN inspection: filters 3 & 4 activated at 1.56 and 1.44 on coord pair [0,1]. First time CNN output directly changed hyperparameter choice.",
            "submission": "0.078067-0.385415-0.381193-0.266170-0.353901-0.693102",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.90, "sigma": [0.012, 0.028, 0.028, 0.028, 0.028, 0.028], "ucb_kappa": 2.5, "gp_restarts": 8},
            "hp_rationale": "Anisotropic tightened further: X1 σ 0.015→0.012, X2-X6 σ 0.035→0.028. W7 new best in npy. X1 near-zero anchor maintained.",
            "learned": "Score 2.5982 — NEW ALL-TIME BEST! +0.185 vs W7=2.4134. Anisotropic σ delivering consecutive new bests.",
            "experiment": "Second anisotropic σ=[0.012,0.028×5]. W8 yielded 2.5982 (new ATB). W9 tightens to σ=[0.010,0.025×5].",
            "submission": "0.096399-0.368153-0.413112-0.285892-0.336821-0.699617",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.92, "sigma": [0.010, 0.025, 0.025, 0.025, 0.025, 0.025], "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Anisotropic tightened: X1 σ=0.010, X2-X6 σ=0.025. Multi-head attention analogy — Vaswani et al. (2017): per-dimension σ mirrors per-head specialisation. Module 19.",
            "learned": "Awaiting W9 result.",
            "experiment": "Third consecutive anisotropic submission. W8 new best 2.5982 — W9 tightens further around X1 near-zero anchor.",
            "submission": "0.096000-0.368000-0.413000-0.286000-0.337000-0.700000",
        },
    ],
    "F8": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline 8D. Most complex function — 8 dimensions. Sobol sampling essential.",
            "learned": "Score 9.009. Strong start for 8D. X1≈0.10, X3≈0.10 boundary pattern emerging.",
            "experiment": "Baseline 8D submission. F8 has a well-defined positive landscape even at n=5.",
            "submission": "0.009077-0.472150-0.515970-0.430449-0.468951-0.460126-0.579196-0.506720",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.07, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "GP gradient from W1 pointed toward X1=0, X3=0, X7=0, X5≈0.93.",
            "learned": "Score 9.832 — all-time best! X1=0, X3=0, X7=0 (zero boundary), X8≈0.54. Near-zero dims + elevated X5.",
            "experiment": "8D boundary lock. Confirmed: the three-zeros pattern (X1=X3=X7=0) is the key structure.",
            "submission": "0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.75, "sigma": 0.06, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Exploit W2 pattern — try to push further in 8D.",
            "learned": "Score 9.818 — just below W2. Very close! The W2 point is a near-optimal precise configuration.",
            "experiment": "8D precision exploit. Showed that W2 coords are uniquely optimal — slight variations drop 0.01.",
            "submission": "0.012005-0.365808-0.002051-0.165458-0.447850-0.535087-0.152929-0.745216",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Wider search — 8D has many local optima, check neighbourhood.",
            "learned": "Score 9.334 — regression. W2 coords are uniquely best in 8D — high-dim landscape is unforgiving.",
            "experiment": "8D neighbourhood search. Failed. Lesson: in 8D, the zero-boundary coords are a global attractor.",
            "submission": "0.069272-0.717004-0.001256-0.001021-0.132919-0.479931-0.048004-0.722152",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Further from W2 — testing upper boundary region.",
            "learned": "Score 8.956 — worst since W1. Confirmed: any deviation from W2 boundary pattern is harmful.",
            "experiment": "Upper boundary test. Failed. The zero-boundary (X1=X3=X7≈0) is non-negotiable for F8.",
            "submission": "0.124245-0.707381-0.198569-0.790421-0.197258-0.733195-0.378511-0.886089",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.80, "sigma": 0.04, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Return to W2 coords exactly — week log override injected W2 best.",
            "learned": "Score 9.774 — close to W2 but not quite. W2 npy file had the exact coords missing — inject fixed this.",
            "experiment": "Week log override for 8D. CNN-1D won CV (91.7%) — 8D boundary pattern most CNN-detectable of all functions.",
            "submission": "0.000000-0.387061-0.068459-0.146466-0.368072-0.662820-0.291841-0.727685",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.0175, "ucb_kappa": 2.0, "gp_restarts": 10},
            "hp_rationale": "Ultra-tight σ=0.0175 in 8D — 2σ=±0.035. GP restarts increased to 10 for 8D landscape. Target: beat W2's 9.832.",
            "learned": "Score 9.8251 — only 0.007 from ATB! X1=0.040, X3=0.004 near-zero maintained. X8=0.781 elevated. So close — W8 goes even tighter.",
            "experiment": "Step 5B: Decision Tree won CV (86.7%) — 8D boundary best classified by hard threshold rules. TinyCNN has 137 params vs NN-Large's 2,049 — 15× efficiency.",
            "submission": "0.040422-0.331667-0.003668-0.158463-0.396893-0.509806-0.166490-0.780552",
        },
        {  # W8
            "hyperparams": {"exploit_ratio": 0.92, "sigma": 0.012, "ucb_kappa": 2.0, "gp_restarts": 10},
            "hp_rationale": "Tightest ever: ratio=0.92, σ=0.012 (2σ=±0.024). Inject override ACTIVE: W2 coords [0.0, 0.179, 0.0, 0.071, 0.929, 0.460, 0.0, 0.541]. Target: beat 9.832 by any margin.",
            "learned": "Score 9.8021 — slight regression from W7=9.8251. Still within 0.030 of W2 ATB=9.8320.",
            "experiment": "Maximum precision σ=0.012 in 8D. W8 got 9.8021 — slight regression. W9 tries anisotropic σ per zero-boundary dims.",
            "submission": "0.008368-0.331528-0.000000-0.160107-0.374002-0.541189-0.166880-0.765946",
        },
        {  # W9
            "hyperparams": {"exploit_ratio": 0.92, "sigma": [0.008, 0.015, 0.008, 0.030, 0.020, 0.015, 0.008, 0.030], "ucb_kappa": 2.0, "gp_restarts": 10},
            "hp_rationale": "Anisotropic: X1/X3/X7 σ=0.008 (zero-boundary dims tightest), X2/X6 σ=0.015, X5/X8 σ=0.030 (free dims). Multi-head attention — Vaswani et al. (2017): per-dimension structure. Module 19.",
            "learned": "Awaiting W9 result.",
            "experiment": "First anisotropic F8 submission. Per-dimension σ based on W2 ATB structure: X1=X3=X7≈0 → tight; X5≈0.93 → looser.",
            "submission": "0.000000-0.179297-0.000000-0.071406-0.929270-0.459981-0.000000-0.541212",
        },
    ],
}
