"""
BBO Capstone — all historical data baked in.
No external files needed — works standalone on GitHub / Streamlit Cloud.
"""

# ── Function metadata ─────────────────────────────────────────────────────────
FUNCTIONS = {
    "F1": {"dims": 2, "objective": "MINIMISE", "search": "[0,1]²",
           "desc": "2D minimisation — flat near-zero landscape throughout"},
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

# ── Week-by-week scores (W1–W6 actuals, W7 = GP prediction placeholder) ──────
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

# ── GP W7 predictions (mu, sigma from EI winner) ─────────────────────────────
W7_PRED = {
    "F1": {"mu": 0.0,       "sigma": 0.0,      "ucb": 0.0},
    "F2": {"mu": 0.6412,    "sigma": 0.018,    "ucb": 0.677},
    "F3": {"mu": -0.00045,  "sigma": 0.0008,   "ucb": 0.00115},
    "F4": {"mu": 0.2201,    "sigma": 0.022,    "ucb": 0.264},
    "F5": {"mu": 5571.5,    "sigma": 450.2,    "ucb": 6472.0},
    "F6": {"mu": -0.1512,   "sigma": 0.028,    "ucb": -0.095},
    "F7": {"mu": 2.089,     "sigma": 0.041,    "ucb": 2.171},
    "F8": {"mu": 9.801,     "sigma": 0.019,    "ucb": 9.839},
}

# ── Submitted coordinates per week ───────────────────────────────────────────
COORDS = {
    "F1": [
        [0.0825, 1.5395],
        [0.6842, 0.7042],
        [0.9010, 0.8770],
        [0.6884, 0.7241],
        [0.5323, 0.6306],
        [0.0739, 0.4071],
        None,
    ],
    "F2": [
        [0.5, 0.5],
        [0.65, 0.20],
        [0.62, 0.18],
        [0.68, 0.19],
        [0.710, 0.162],
        [0.703, 0.927],
        None,
    ],
    "F3": [
        [0.40, 0.55, 0.50],
        [0.55, 0.58, 0.48],
        [0.70, 0.60, 0.45],
        [0.85, 0.63, 0.44],
        [0.92, 0.62, 0.46],
        [0.998, 0.621, 0.453],
        None,
    ],
    "F4": [
        [0.50, 0.50, 0.50, 0.50],
        [0.439, 0.415, 0.385, 0.398],
        [0.35, 0.42, 0.40, 0.36],
        [0.41, 0.43, 0.38, 0.40],
        [0.30, 0.38, 0.45, 0.30],
        [0.410, 0.438, 0.456, 0.350],
        None,
    ],
    "F5": [
        [0.1199, 0.4986, 0.4779, 0.4947],
        [0.2990, 0.9683, 1.0,    1.0   ],
        [0.8030, 0.9455, 0.9975, 0.9763],
        [0.3547, 0.9182, 0.9966, 0.9454],
        [0.4531, 0.6716, 0.3037, 0.7912],
        [0.7810, 1.0,    1.0,    1.0   ],
        None,
    ],
    "F6": [
        [0.50, 0.50, 0.50, 0.50, 0.50],
        [0.38, 0.30, 0.55, 0.80, 0.12],
        [0.55, 0.45, 0.60, 0.70, 0.20],
        [0.42, 0.33, 0.58, 0.76, 0.15],
        [0.60, 0.50, 0.65, 0.65, 0.25],
        [0.427, 0.326, 0.598, 0.780, 0.144],
        None,
    ],
    "F7": [
        [0.50, 0.40, 0.35, 0.25, 0.38, 0.65],
        [0.08, 0.41, 0.34, 0.24, 0.38, 0.70],
        [0.06, 0.40, 0.33, 0.23, 0.37, 0.68],
        [0.12, 0.43, 0.36, 0.26, 0.40, 0.66],
        [0.18, 0.45, 0.40, 0.30, 0.42, 0.60],
        [0.055, 0.407, 0.341, 0.242, 0.375, 0.685],
        None,
    ],
    "F8": [
        [0.10, 0.18, 0.10, 0.07, 0.93, 0.46, 0.10, 0.54],
        [0.0,  0.179, 0.0, 0.071, 0.929, 0.460, 0.0, 0.541],
        [0.012, 0.366, 0.002, 0.166, 0.448, 0.535, 0.153, 0.745],
        [0.05, 0.20, 0.05, 0.09, 0.88, 0.44, 0.05, 0.55],
        [0.08, 0.22, 0.08, 0.10, 0.85, 0.42, 0.08, 0.57],
        [0.012, 0.366, 0.002, 0.166, 0.448, 0.535, 0.153, 0.745],
        None,
    ],
}

# ── W7 Strategy per function ──────────────────────────────────────────────────
STRATEGY = {
    "F1": {
        "action": "EXPLORE",
        "exploit_ratio": 0.40,
        "sigma": 0.216,
        "ucb_kappa": 3.0,
        "gp_restarts": 5,
        "rationale": (
            "F1 is a near-flat landscape — all 6 submitted values are effectively zero. "
            "No strong signal exists to exploit, so W7 widens the search with a 40/60 "
            "exploit/explore split and σ=0.216 to discover if any region has non-trivial "
            "structure. This is a deliberate low-risk EXPLORE week."
        ),
        "best_week": "W1/W2 (≈ 0)",
        "pattern": "Flat — no dominant region identified",
    },
    "F2": {
        "action": "EXPLOIT W5 BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.0175,
        "ucb_kappa": 2.5,
        "gp_restarts": 5,
        "rationale": (
            "W5 produced the all-time best of 0.6497 at [0.710, 0.162]. W6 regressed to "
            "0.5844 — the GP moved away from the W5 peak. W7 injects the W5 coordinates "
            "directly into training, uses 85/15 exploit/explore with very tight σ=0.0175 "
            "to recover and refine around X2≈0.16."
        ),
        "best_week": "W5 (0.6497)",
        "pattern": "Strong peak at X2≈0.16, X1≈0.71",
    },
    "F3": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.90,
        "sigma": 0.024,
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "rationale": (
            "W6 delivered a near-perfect -0.000707 at X1≈1.0. Scores have improved "
            "monotonically toward the X1 boundary. W7 exploits very tightly (90/10, "
            "σ=0.024) around [0.998, 0.621, 0.453] to probe whether X1=1.0 gives further "
            "improvement and to refine X2/X3."
        ),
        "best_week": "W6 (-0.000707)",
        "pattern": "X1 → 1.0 boundary dominates; X2/X3 near [0.62, 0.45]",
    },
    "F4": {
        "action": "EXPLOIT W2 BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.0175,
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "rationale": (
            "W2 produced +0.2376 at [0.439, 0.415, 0.385, 0.398] — a near-centre "
            "point that subsequent weeks failed to beat. W6 (-0.129) is still well below "
            "W2. W7 re-injects the W2 coordinates and exploits tightly (85/15, σ=0.0175) "
            "to confirm and refine this region."
        ),
        "best_week": "W2 (+0.2376)",
        "pattern": "Near-centre symmetric region ~[0.41–0.44] in all dims",
    },
    "F5": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.048,
        "ucb_kappa": 2.0,
        "gp_restarts": 8,
        "rationale": (
            "W6 exploded to 5875.1 at [0.781, 1.0, 1.0, 1.0] — X2/X3/X4 fully "
            "saturated. W7 exploits with σ=0.048 (slightly wider than usual) to probe "
            "whether X1 can exceed 0.78 for further gains, while keeping X2–X4 near 1.0. "
            "The GP's UCB of 6472 suggests genuine upside potential."
        ),
        "best_week": "W6 (5875.1)",
        "pattern": "X2=X3=X4=1.0 boundary; X1≈0.78–0.94",
    },
    "F6": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.042,
        "ucb_kappa": 2.5,
        "gp_restarts": 8,
        "rationale": (
            "W6 set a new best of -0.1727 at [0.427, 0.326, 0.598, 0.780, 0.144]. "
            "The pattern shows X4 high (~0.78) and X5 low (~0.14). W7 exploits tightly "
            "around this point with σ=0.042 to refine the X4-high/X5-low structure "
            "across the 5D space."
        ),
        "best_week": "W6 (-0.1727)",
        "pattern": "X4 high (~0.78), X5 low (~0.14)",
    },
    "F7": {
        "action": "EXPLOIT W6 NEW BEST",
        "exploit_ratio": 0.90,
        "sigma": 0.030,
        "ucb_kappa": 2.5,
        "gp_restarts": 8,
        "rationale": (
            "W6 jumped to 2.119 — a massive improvement over W2's 1.739. The pattern "
            "is X1 near-zero (~0.055) with X6 elevated (~0.685). W7 exploits very tightly "
            "(90/10, σ=0.030) around this 6D point to consolidate the W6 breakthrough."
        ),
        "best_week": "W6 (2.119)",
        "pattern": "X1 near-zero (~0.055), X6 elevated (~0.685)",
    },
    "F8": {
        "action": "EXPLOIT W2 BEST",
        "exploit_ratio": 0.85,
        "sigma": 0.0175,
        "ucb_kappa": 2.0,
        "gp_restarts": 10,
        "rationale": (
            "W2 produced 9.832 — the all-time best — with X1≈0, X3≈0, X7≈0 and "
            "X5≈0.93 boundary pattern. W6 (9.774) failed to beat it. W7 re-injects "
            "the W2 coordinates and exploits very tightly (σ=0.0175) in 8D to confirm "
            "and refine this high-dimensional boundary structure."
        ),
        "best_week": "W2 (9.832)",
        "pattern": "X1≈0, X3≈0, X7≈0 near-zero; X5≈0.93 elevated",
    },
}

# ── Winning classifiers per function (W7 GP best model) ──────────────────────
CLASSIFIERS = {
    "F1": {"name": "Linear SVM",        "cv": 0.750, "std": 0.14, "family": "SVM"},
    "F2": {"name": "Logistic Regression","cv": 0.833, "std": 0.10, "family": "LogReg"},
    "F3": {"name": "Random Forest",      "cv": 0.833, "std": 0.10, "family": "RF"},
    "F4": {"name": "Linear SVM",         "cv": 0.833, "std": 0.12, "family": "SVM"},
    "F5": {"name": "Linear SVM",         "cv": 0.833, "std": 0.12, "family": "SVM"},
    "F6": {"name": "Random Forest",      "cv": 0.833, "std": 0.10, "family": "RF"},
    "F7": {"name": "Neural Network",     "cv": 0.833, "std": 0.08, "family": "NN"},
    "F8": {"name": "CNN-1D",             "cv": 0.917, "std": 0.08, "family": "CNN"},
}

# ── Pipeline code structure (13 steps) ───────────────────────────────────────
PIPELINE_STEPS = [
    {"step": "Step 0",  "title": "Config & Strategy",
     "icon": "⚙️",
     "desc": "Sets FUNCTION_ID, WEEK, MAXIMIZE flag, hyperparameters (EXPLOIT_RATIO, EXPLOIT_SIGMA, UCB_KAPPA, GP_RESTARTS). Prints a box summary of the week's plan."},
    {"step": "Step 1",  "title": "Data Load",
     "icon": "📂",
     "desc": "Loads f{n}_w{k}_inputs.npy and f{n}_w{k}_outputs.npy. Validates shape and range. Confirms all-time best score and coordinates from npy."},
    {"step": "Step 2",  "title": "Data Inspection",
     "icon": "🔬",
     "desc": "Prints data summary stats: n_samples, n_dims, y range, percentiles. Identifies boundary points (x_i < 0.1 or x_i > 0.9)."},
    {"step": "Step 3",  "title": "History Plot",
     "icon": "📊",
     "desc": "Plots submitted y values W1–W(k-1), colour-coded green/red by improvement. Running best line overlaid. Saved as PNG."},
    {"step": "Step 4",  "title": "Candidate Generation",
     "icon": "🎲",
     "desc": "Generates 10,000 candidates: EXPLOIT_RATIO% drawn from Gaussian around best_point (σ=EXPLOIT_SIGMA), remainder from Sobol quasi-random sequence."},
    {"step": "Step 5",  "title": "Classifier Training",
     "icon": "🤖",
     "desc": "Labels y_train by 70th-percentile threshold. Trains 8 model types: Linear SVM, RBF SVM, Logistic Regression, Decision Tree, Random Forest, Extra Trees, MLP, CNN-1D. 5-fold CV."},
    {"step": "Step 6",  "title": "Model Comparison",
     "icon": "📈",
     "desc": "Bar chart of all 8 models' CV accuracy with error bars. Selects winner by highest mean CV. Saved as PNG."},
    {"step": "Step 7",  "title": "Filter Candidates",
     "icon": "🔽",
     "desc": "Uses winning classifier P(class=1) to filter 10,000 → those above FILTER_PERCENTILE. Typically keeps 3,000–7,000 high-quality candidates."},
    {"step": "Step 7B", "title": "Why This Classifier Won",
     "icon": "🧠",
     "desc": "Prints a bordered analysis box: winner family rationale, candidate filter quality stats, boundary dimension analysis, WHY section with data-driven bullets."},
    {"step": "Step 8",  "title": "Week Commentary",
     "icon": "📝",
     "desc": "Markdown cell explaining the week's strategy: what happened last week, what pattern was identified, why this week's hyperparameters were chosen."},
    {"step": "Step 9",  "title": "GP Fit",
     "icon": "🌐",
     "desc": "Fits Gaussian Process (Matérn 5/2 kernel + WhiteKernel) on scaled X_train→y_train. Reports GP R², kernel parameters, fitted length scales."},
    {"step": "Step 10", "title": "Acquisition Functions",
     "icon": "🎯",
     "desc": "Computes EI (Expected Improvement) and UCB (μ + κσ) over filtered candidates. Selects submission = argmax EI. Prints Z-score, exploit/explore decomposition."},
    {"step": "Step 11", "title": "Acquisition Curves",
     "icon": "📉",
     "desc": "Per-dimension EI and UCB sweeps (fixing all other dims at best_point). Shows how each dimension contributes to acquisition signal."},
    {"step": "Step 12", "title": "GP Surfaces",
     "icon": "🗺️",
     "desc": "2D contour plots of GP μ, GP σ, EI, and UCB over the top-2 most sensitive dimensions. Best point (★) and submission point (◆) overlaid."},
    {"step": "Step 13", "title": "Dashboard & Submission",
     "icon": "🏆",
     "desc": "Full submission dashboard: week-on-week trajectory, submission coordinates, EI decomposition pie, dimension sensitivity, summary table. Prints final submission string."},
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
