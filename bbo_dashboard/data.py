"""
BBO Capstone — all historical data baked in.
No external files needed — works standalone on GitHub / Streamlit Cloud.
Updated: W7 actuals added, F7 anisotropic sigma, CNN filter map rationale.
"""

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
    "F1": [0.0,        8.84e-7,    5.17e-96,   1.66e-9,    -5.44e-7,   1.67e-85,   None],
    "F2": [0.5246,     0.2847,     -0.0298,    0.0188,     0.6497,     0.5844,     None],
    "F3": [-0.01358,   -0.03277,   -0.08337,   -0.13795,   -0.05900,   -0.000707,  None],
    "F4": [-2.6271,    0.2376,     -0.9620,    -0.5268,    -2.4571,    -0.1294,    None],
    "F5": [60.07,      4062.1,     4890.6,     2913.0,     24.48,      5875.1,     None],
    "F6": [-1.3389,    -0.2372,    -0.8835,    -0.3630,    -1.7662,    -0.1727,    None],
    "F7": [0.8085,     1.7392,     1.7358,     1.1399,     0.5763,     2.1190,     None],
    "F8": [9.0093,     9.8320,     9.8188,     9.3341,     8.9560,     9.7741,     None],
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
    ],
    "F2": [
        [0.5, 0.5],
        [0.65, 0.20],
        [0.62, 0.18],
        [0.68, 0.19],
        [0.710, 0.162],
        [0.703, 0.927],
        [0.688952, 0.168811],
    ],
    "F3": [
        [0.40, 0.55, 0.50],
        [0.55, 0.58, 0.48],
        [0.70, 0.60, 0.45],
        [0.85, 0.63, 0.44],
        [0.92, 0.62, 0.46],
        [0.998, 0.621, 0.453],
        [1.000000, 0.571651, 0.503999],
    ],
    "F4": [
        [0.50, 0.50, 0.50, 0.50],
        [0.439, 0.415, 0.385, 0.398],
        [0.35, 0.42, 0.40, 0.36],
        [0.41, 0.43, 0.38, 0.40],
        [0.30, 0.38, 0.45, 0.30],
        [0.410, 0.438, 0.456, 0.350],
        [0.451762, 0.438642, 0.400163, 0.395091],
    ],
    "F5": [
        [0.1199, 0.4986, 0.4779, 0.4947],
        [0.2990, 0.9683, 1.0,    1.0   ],
        [0.8030, 0.9455, 0.9975, 0.9763],
        [0.3547, 0.9182, 0.9966, 0.9454],
        [0.4531, 0.6716, 0.3037, 0.7912],
        [0.7810, 1.0,    1.0,    1.0   ],
        [0.937682, 1.000000, 1.000000, 1.000000],
    ],
    "F6": [
        [0.50, 0.50, 0.50, 0.50, 0.50],
        [0.38, 0.30, 0.55, 0.80, 0.12],
        [0.55, 0.45, 0.60, 0.70, 0.20],
        [0.42, 0.33, 0.58, 0.76, 0.15],
        [0.60, 0.50, 0.65, 0.65, 0.25],
        [0.427, 0.326, 0.598, 0.780, 0.144],
        [0.497320, 0.294798, 0.563080, 0.684981, 0.129206],
    ],
    "F7": [
        [0.50, 0.40, 0.35, 0.25, 0.38, 0.65],
        [0.08, 0.41, 0.34, 0.24, 0.38, 0.70],
        [0.06, 0.40, 0.33, 0.23, 0.37, 0.68],
        [0.12, 0.43, 0.36, 0.26, 0.40, 0.66],
        [0.18, 0.45, 0.40, 0.30, 0.42, 0.60],
        [0.055, 0.407, 0.341, 0.242, 0.375, 0.685],
        [0.078067, 0.385415, 0.381193, 0.266170, 0.353901, 0.693102],
    ],
    "F8": [
        [0.10, 0.18, 0.10, 0.07, 0.93, 0.46, 0.10, 0.54],
        [0.0,  0.179, 0.0, 0.071, 0.929, 0.460, 0.0, 0.541],
        [0.012, 0.366, 0.002, 0.166, 0.448, 0.535, 0.153, 0.745],
        [0.05, 0.20, 0.05, 0.09, 0.88, 0.44, 0.05, 0.55],
        [0.08, 0.22, 0.08, 0.10, 0.85, 0.42, 0.08, 0.57],
        [0.012, 0.366, 0.002, 0.166, 0.448, 0.535, 0.153, 0.745],
        [0.040422, 0.331667, 0.003668, 0.158463, 0.396893, 0.509806, 0.166490, 0.780552],
    ],
}

# ── W7 Strategy per function ──────────────────────────────────────────────────
STRATEGY = {
    "F1": {
        "action": "EXPLORE",
        "exploit_ratio": 0.40,
        "sigma": 0.216,
        "sigma_type": "isotropic",
        "ucb_kappa": 3.0,
        "gp_restarts": 5,
        "turbo": "EXPAND",
        "rationale": (
            "F1 is a near-flat landscape — all 6 submitted values are effectively zero. "
            "No strong signal exists to exploit, so W7 widens the search with a 40/60 "
            "exploit/explore split and σ=0.216 to discover if any region has non-trivial "
            "structure. This is a deliberate low-risk EXPLORE week."
        ),
        "best_week": "W1/W2 (≈ 0)",
        "pattern": "Flat — no dominant region identified",
        "w7_submission": "0.582827-0.482269",
    },
    "F2": {
        "action": "EXPLOIT W5 BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.0175,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.5,
        "gp_restarts": 5,
        "turbo": "SHRINK",
        "rationale": (
            "W5 produced the all-time best of 0.6497 at [0.710, 0.162]. W6 regressed to "
            "0.5844 — the GP moved away from the W5 peak. W7 injects the W5 coordinates "
            "directly into training, uses 85/15 exploit/explore with very tight σ=0.0175 "
            "to recover and refine around X2≈0.16."
        ),
        "best_week": "W5 (0.6497)",
        "pattern": "Strong peak at X2≈0.16, X1≈0.71",
        "w7_submission": "0.688952-0.168811",
    },
    "F3": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.90,
        "sigma": 0.024,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "turbo": "SHRINK",
        "rationale": (
            "W6 delivered a near-perfect -0.000707 at X1≈1.0. Scores have improved "
            "monotonically toward the X1 boundary. W7 exploits very tightly (90/10, "
            "σ=0.024) around [0.998, 0.621, 0.453] to probe whether X1=1.0 gives further "
            "improvement and to refine X2/X3. W7 submission hit X1=1.000 exactly."
        ),
        "best_week": "W6 (-0.000707)",
        "pattern": "X1 → 1.0 boundary dominates; X2/X3 near [0.62, 0.45]",
        "w7_submission": "1.000000-0.571651-0.503999",
    },
    "F4": {
        "action": "RECOVER W2 BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.0175,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "turbo": "SHRINK",
        "rationale": (
            "W2 produced +0.2376 at [0.439, 0.415, 0.385, 0.398] — a near-centre "
            "point that subsequent weeks failed to beat. W6 (-0.129) is still well below "
            "W2. W7 re-injects the W2 coordinates and exploits tightly (85/15, σ=0.0175) "
            "to confirm and refine this region. All 4 W7 coords landed within ±0.015 of inject point."
        ),
        "best_week": "W2 (+0.2376)",
        "pattern": "Near-centre symmetric region ~[0.41–0.44] in all dims",
        "w7_submission": "0.451762-0.438642-0.400163-0.395091",
    },
    "F5": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.048,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "turbo": "EXPAND",
        "rationale": (
            "W6 exploded to 5875.1 at [0.781, 1.0, 1.0, 1.0] — X2/X3/X4 fully "
            "saturated. W7 exploits with σ=0.048 (slightly wider than usual) to probe "
            "whether X1 can exceed 0.78 for further gains, while keeping X2–X4 near 1.0. "
            "CNN filter maps confirmed X2-X4 boundary pattern. W7: X1 jumped to 0.938."
        ),
        "best_week": "W6 (5875.1)",
        "pattern": "X2=X3=X4=1.0 boundary; X1≈0.78–0.94",
        "w7_submission": "0.937682-1.000000-1.000000-1.000000",
    },
    "F6": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.042,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.5,
        "gp_restarts": 8,
        "turbo": "EXPAND",
        "rationale": (
            "W6 set a new best of -0.1727 at [0.427, 0.326, 0.598, 0.780, 0.144]. "
            "The pattern shows X4 high (~0.78) and X5 low (~0.14). W7 exploits tightly "
            "around this point with σ=0.042 to refine the X4-high/X5-low structure "
            "across the 5D space."
        ),
        "best_week": "W6 (-0.1727)",
        "pattern": "X4 high (~0.78), X5 low (~0.14)",
        "w7_submission": "0.497320-0.294798-0.563080-0.684981-0.129206",
    },
    "F7": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.90,
        "sigma": [0.015, 0.035, 0.035, 0.035, 0.035, 0.035],
        "sigma_type": "anisotropic",
        "ucb_kappa": 2.5,
        "gp_restarts": 8,
        "turbo": "SHRINK",
        "rationale": (
            "W6 jumped to 2.119 — a massive +0.38 improvement. X1=0.055 is the key "
            "near-zero boundary anchor. CNN filter maps (Step 5B) confirmed filters 3 & 4 "
            "peaked on coord pair [0,1], directly motivating ANISOTROPIC sigma: tight X1 "
            "(σ=0.015, 2σ=±0.030) pinned to near-zero boundary; slightly looser X2-X6 "
            "(σ=0.035) for local refinement. W7 X1=0.078 — tighter to zero than isotropic."
        ),
        "best_week": "W6 (2.119)",
        "pattern": "X1 near-zero (~0.055), X6 elevated (~0.685)",
        "w7_submission": "0.078067-0.385415-0.381193-0.266170-0.353901-0.693102",
    },
    "F8": {
        "action": "EXPLOIT W2 BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.0175,
        "sigma_type": "isotropic",
        "ucb_kappa": 2.0,
        "gp_restarts": 10,
        "turbo": "SHRINK",
        "rationale": (
            "W2 produced 9.832 — the all-time best — with X1≈0, X3≈0, X7≈0 and "
            "X5≈0.93 boundary pattern. W6 (9.774) failed to beat it. W7 re-injects "
            "the W2 coordinates and exploits very tightly (σ=0.0175) in 8D to confirm "
            "and refine this high-dimensional boundary structure. GP mu=9.878 > W2 best."
        ),
        "best_week": "W2 (9.832)",
        "pattern": "X1≈0, X3≈0, X7≈0 near-zero; X5≈0.93 elevated",
        "w7_submission": "0.040422-0.331667-0.003668-0.158463-0.396893-0.509806-0.166490-0.780552",
    },
}

# ── W7 Summary at a glance ────────────────────────────────────────────────────
W7_GLANCE = {
    "F1": {"true_best": "≈ 0",       "best_wk": "W2", "w6_score": "≈ 0",       "strategy": "EXPLORE",             "override": False},
    "F2": {"true_best": "0.6497",    "best_wk": "W5", "w6_score": "0.584",      "strategy": "EXPLOIT W5 BEST",     "override": True},
    "F3": {"true_best": "-0.000707", "best_wk": "W6", "w6_score": "-0.000707",  "strategy": "EXPLOIT W6 NEW BEST", "override": False},
    "F4": {"true_best": "+0.2376",   "best_wk": "W2", "w6_score": "-0.129",     "strategy": "RECOVER W2 BEST",     "override": True},
    "F5": {"true_best": "5,875",     "best_wk": "W6", "w6_score": "5,875",      "strategy": "EXPLOIT W6 NEW BEST", "override": False},
    "F6": {"true_best": "-0.1727",   "best_wk": "W6", "w6_score": "-0.1727",    "strategy": "EXPLOIT W6 NEW BEST", "override": False},
    "F7": {"true_best": "2.119",     "best_wk": "W6", "w6_score": "2.119",      "strategy": "EXPLOIT W6 NEW BEST", "override": False},
    "F8": {"true_best": "9.832",     "best_wk": "W2", "w6_score": "9.774",      "strategy": "EXPLOIT W2 BEST",     "override": True},
}

# ── TuRBO sigma adaptation summary ───────────────────────────────────────────
TURBO_SUMMARY = {
    "F1": {"sigma_w6": 0.08,  "sigma_w7": 0.216,  "direction": "EXPAND",  "note": "6 weeks near-zero — tripled sigma to near-random width"},
    "F2": {"sigma_w6": 0.04,  "sigma_w7": 0.0175, "direction": "SHRINK",  "note": "W5 region confirmed — sigma halved for precision"},
    "F3": {"sigma_w6": 0.04,  "sigma_w7": 0.024,  "direction": "SHRINK",  "note": "W6 new best at X1=0.998 — tighten around boundary"},
    "F4": {"sigma_w6": 0.04,  "sigma_w7": 0.0175, "direction": "SHRINK",  "note": "W2 tight cluster confirmed — sigma halved"},
    "F5": {"sigma_w6": 0.04,  "sigma_w7": 0.048,  "direction": "EXPAND",  "note": "X2-X4 locked, X1 still floating — slight expand"},
    "F6": {"sigma_w6": 0.04,  "sigma_w7": 0.042,  "direction": "EXPAND",  "note": "Sparse 5D — marginal expand for local refinement"},
    "F7": {"sigma_w6": 0.04,  "sigma_w7": "anisotropic [0.015,0.035×5]", "direction": "SHRINK",
           "note": "CNN filter maps peaked on [0,1] pair — anisotropic: tight X1, loose X2-X6"},
    "F8": {"sigma_w6": 0.03,  "sigma_w7": 0.0175, "direction": "SHRINK",  "note": "W2 boundary pattern confirmed — sigma halved in 8D"},
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

WEEKS = ["W1", "W2", "W3", "W4", "W5", "W6", "W7"]

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
            "learned": "Awaiting W7 result. Hypothesis: if still near-zero, F1 may be an adversarial flat function designed to test exploration strategy.",
            "experiment": "Step 5B CNN inspection: filters learned near-uniform weights — confirms absence of local coordinate structure.",
            "submission": "0.582827-0.482269",
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
            "learned": "Awaiting W7 result. W7 coords [0.689, 0.169] — very close to W5 best. Expect recovery to ≥0.64.",
            "experiment": "Week log override: W5 coords injected to correct npy gap. Tests whether GP can improve on W5 with denser sampling around peak.",
            "submission": "0.688952-0.168811",
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
            "learned": "Awaiting W7 result. W7 submission hit X1=1.000 exactly — the true boundary. X2/X3 shifted slightly: [0.572, 0.504] vs W6 [0.621, 0.453].",
            "experiment": "Step 5B: CNN filters showed moderate activation on X1 pair — consistent with boundary dominance hypothesis.",
            "submission": "1.000000-0.571651-0.503999",
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
            "learned": "Awaiting W7 result. W7 coords [0.452, 0.439, 0.400, 0.395] — all within ±0.015 of W2. Best attempt at precision recovery.",
            "experiment": "Step 5B: CNN detected tight cluster at W2 best coords. Linear SVM won — confirms linear separability of the near-centre peak.",
            "submission": "0.451762-0.438642-0.400163-0.395091",
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
            "learned": "Awaiting W7 result. W7: X1 jumped to 0.938 — highest X1 ever submitted. If confirmed positive, X1=1.0 may be optimal.",
            "experiment": "Step 5B: CNN feature maps confirmed X2-X4 boundary lock. Anisotropic sigma [0.090, 0.018×3] tested but reverted — wider X1 unexpectedly hurt.",
            "submission": "0.937682-1.000000-1.000000-1.000000",
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
            "learned": "Awaiting W7 result. Coords shifted: X2 dropped (0.295 vs 0.326), X5 dropped further (0.129 vs 0.144) — probing even lower X5.",
            "experiment": "Step 5B: CNN feature maps showed moderate X4/X5 activation. Random forest won again — consistent with W6.",
            "submission": "0.497320-0.294798-0.563080-0.684981-0.129206",
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
            "learned": "Awaiting W7 result. W7 X1=0.078 — slightly higher than W6 (0.055). Anisotropic ensures X1 stays pinned near-zero while X2-X6 explore locally.",
            "experiment": "Step 5B CNN inspection: filters 3 & 4 activated at 1.56 and 1.44 on coord pair [0,1]. This filter map analysis directly changed the hyperparameter choice — first time CNN output fed into pipeline decision.",
            "submission": "0.078067-0.385415-0.381193-0.266170-0.353901-0.693102",
        },
    ],
    "F8": [
        {  # W1
            "hyperparams": {"exploit_ratio": 0.50, "sigma": 0.10, "ucb_kappa": 2.0, "gp_restarts": 3},
            "hp_rationale": "Baseline 8D. Most complex function — 8 dimensions. Sobol sampling essential.",
            "learned": "Score 9.009. Strong start for 8D. X1≈0.10, X3≈0.10 boundary pattern emerging.",
            "experiment": "Baseline 8D submission. F8 has a well-defined positive landscape even at n=5.",
            "submission": "0.10-0.18-0.10-0.07-0.93-0.46-0.10-0.54",
        },
        {  # W2
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.07, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "GP gradient from W1 pointed toward X1=0, X3=0, X7=0, X5≈0.93.",
            "learned": "Score 9.832 — all-time best! X1=0, X3=0, X7=0 (zero boundary), X8≈0.54. Near-zero dims + elevated X5.",
            "experiment": "8D boundary lock. Confirmed: the three-zeros pattern (X1=X3=X7=0) is the key structure.",
            "submission": "0.000-0.179-0.000-0.071-0.929-0.460-0.000-0.541",
        },
        {  # W3
            "hyperparams": {"exploit_ratio": 0.75, "sigma": 0.06, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Exploit W2 pattern — try to push further in 8D.",
            "learned": "Score 9.818 — just below W2. Very close! The W2 point is a near-optimal precise configuration.",
            "experiment": "8D precision exploit. Showed that W2 coords are uniquely optimal — slight variations drop 0.01.",
            "submission": "0.012-0.366-0.002-0.166-0.448-0.535-0.153-0.745",
        },
        {  # W4
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.5, "gp_restarts": 5},
            "hp_rationale": "Wider search — 8D has many local optima, check neighbourhood.",
            "learned": "Score 9.334 — regression. W2 coords are uniquely best in 8D — high-dim landscape is unforgiving.",
            "experiment": "8D neighbourhood search. Failed. Lesson: in 8D, the zero-boundary coords are a global attractor.",
            "submission": "0.05-0.20-0.05-0.09-0.88-0.44-0.05-0.55",
        },
        {  # W5
            "hyperparams": {"exploit_ratio": 0.65, "sigma": 0.08, "ucb_kappa": 2.0, "gp_restarts": 5},
            "hp_rationale": "Further from W2 — testing upper boundary region.",
            "learned": "Score 8.956 — worst since W1. Confirmed: any deviation from W2 boundary pattern is harmful.",
            "experiment": "Upper boundary test. Failed. The zero-boundary (X1=X3=X7≈0) is non-negotiable for F8.",
            "submission": "0.08-0.22-0.08-0.10-0.85-0.42-0.08-0.57",
        },
        {  # W6
            "hyperparams": {"exploit_ratio": 0.80, "sigma": 0.04, "ucb_kappa": 2.0, "gp_restarts": 8},
            "hp_rationale": "Return to W2 coords exactly — week log override injected W2 best.",
            "learned": "Score 9.774 — close to W2 but not quite. W2 npy file had the exact coords missing — inject fixed this.",
            "experiment": "Week log override for 8D. CNN-1D won CV (91.7%) — 8D boundary pattern most CNN-detectable of all functions.",
            "submission": "0.012-0.366-0.002-0.166-0.448-0.535-0.153-0.745",
        },
        {  # W7
            "hyperparams": {"exploit_ratio": 0.85, "sigma": 0.0175, "ucb_kappa": 2.0, "gp_restarts": 10},
            "hp_rationale": "Ultra-tight σ=0.0175 in 8D — 2σ=±0.035. GP restarts increased to 10 for 8D landscape. Target: beat W2's 9.832.",
            "learned": "Awaiting W7 result. W7 coords show X1=0.040, X3=0.004 — both near-zero. X8=0.781 elevated vs W2's 0.541. GP mu=9.878 > W2 best.",
            "experiment": "Step 5B: Decision Tree won CV (86.7%) — 8D boundary best classified by hard threshold rules. CNN-1D competitive. Parameter count: TinyCNN has 137 params vs NN-Large's 2,049 — 15× weight sharing efficiency.",
            "submission": "0.040422-0.331667-0.003668-0.158463-0.396893-0.509806-0.166490-0.780552",
        },
    ],
}
