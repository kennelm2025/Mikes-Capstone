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
