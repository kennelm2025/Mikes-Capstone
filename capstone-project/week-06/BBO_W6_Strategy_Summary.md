# BBO Capstone — Week 6 Strategy Summary
**Mike Kennelly | All functions MAXIMISATION — higher is always better**

---

## Overview

After 5 weeks of evaluations, each function now has between 15 and 45
historical data points. The strategy for each function this week is driven
by three things:

1. **Trajectory** — is the function improving, stuck, or regressing?
2. **Data density** — n/p ratio (samples / dimensions) determines how
   much we trust the Gaussian Process surrogate
3. **Module 17 signal** — CNN concepts (progressive feature extraction,
   overfitting balance, loss function proxy gap) directly shaped each decision

Key parameters that differ across functions:

| Parameter       | Controls                                 | Range used W6  |
|-----------------|------------------------------------------|----------------|
| EXPLOIT_RATIO   | Fraction of candidates near best point   | 0.60 -- 0.90   |
| EXPLOIT_SIGMA   | Gaussian radius around best point        | 0.02 -- 0.08   |
| UCB_KAPPA       | Exploration bonus in UCB = mu + kappa*sigma | 2.0 -- 3.0  |
| GP_RESTARTS     | Kernel hyperparameter search restarts    | 5 -- 10        |

---

## F1 — EXPLORE
**2D | 15 samples | n/p = 7.5 | Best = ~0.000 | W5 = -0.0000005**

### What the data says
Five weeks of evaluations and the best score is essentially zero. The
function is either bounded near zero by design, or — more likely — every
submission so far has missed the true high-value region entirely. Continuing
to exploit around a near-zero point will not produce improvement.

### Strategy
Raise EXPLOIT_RATIO to 0.60 (from default 0.80) so 40% of candidates are
drawn uniformly at random across [0,1]^2. Widen EXPLOIT_SIGMA to 0.08 to
cast a broader net around the current best. Raise UCB_KAPPA to 3.0 to add
a stronger exploration bonus in the acquisition function.

The per-dimension EI curves (Step 11) are the key diagnostic this week.
If EI peaks at the boundary of [0,1] for either dimension, the true optimum
may be in a region we have not yet sampled.

### Module 17 connection
Module 17 asks how progressive feature extraction influenced BBO strategy.
F1 is the clearest answer: we are still in the edge-detection phase. CNNs
do not skip from raw pixels to object classification — they build up a
hierarchy of features layer by layer. We cannot exploit a peak we have not
yet located. The weak EI signal (best ~0) means the proxy objective is
unreliable, so UCB with kappa=3 (which relies less on the EI proxy) is
the more honest acquisition function this week.

### Key settings
    EXPLOIT_RATIO = 0.60    # 40% uniform exploration
    EXPLOIT_SIGMA = 0.08    # Wider search radius
    UCB_KAPPA     = 3.0     # Elevated — EI proxy is weak near zero

---

## F2 — TIGHT EXPLOIT
**2D | 15 samples | n/p = 7.5 | Best = 0.6497 (W5 NEW BEST) | W5 = +0.6497**

### What the data says
Week 5 delivered the highest score ever on F2 — 0.6497 — a qualitative
jump from the previous best of 0.611. The W5 submission point [0.710, 0.162]
is confirmed as a high-value region. The function is all-positive and the
mean is 0.259, so the best of 0.6497 is well above average. The EI signal
is strong.

### Strategy
Press the advantage. Raise EXPLOIT_RATIO to 0.85 and tighten EXPLOIT_SIGMA
to 0.03. The search concentrates 85% of candidates in a tight Gaussian
(radius ±0.06) around [0.710, 0.162]. GP_RESTARTS raised to 8 for extra
precision on the peak shape. UCB_KAPPA kept at standard 2.0 — the EI
proxy is reliable when the best is well above the dataset mean.

### Module 17 connection
Module 17 Q2 asks about LeNet-style breakthroughs and incremental BBO
improvement. F2's W5 result IS that breakthrough moment. The function
returned modest scores for weeks (0.2--0.5 range) then W5 delivered a
qualitative jump. Just as LeNet proved the paradigm and AlexNet scaled it
up, W6 for F2 is the scale-up step: same region, tighter focus, more GP
restarts. Module 17 Q4 (activations / EI non-negativity) is also relevant:
with best=0.6497 well above the mean, the EI landscape will be sharply
peaked — most candidates produce EI=0 except in the W5 neighbourhood.
This is the BBO equivalent of a sparse ReLU activation map.

### Key settings
    EXPLOIT_RATIO = 0.85    # W5 new best -- press hard
    EXPLOIT_SIGMA = 0.03    # Tight search around [0.710, 0.162]
    GP_RESTARTS   = 8       # Extra precision on peak shape

---

## F3 — EXPLOIT CAREFULLY
**3D | 20 samples | n/p = 6.7 | Best = -0.0136 @ idx17 | W5 = -0.0590**

### What the data says
All 20 output values are negative. The function maximum is somewhere near
zero and we are hunting it. The best point [0.966, 0.518, 0.403] has X1
very close to the upper boundary (0.966), suggesting the function climbs
steeply near X1=1. W5 regressed to -0.059, moving away from the best.
Recovery is needed in W6.

### Strategy
Return to the best-known region with moderate exploitation (EXPLOIT_RATIO
0.75) and modest tightening of sigma to 0.04. Keep 25% exploration as
insurance against GP overfitting on 20 samples in 3D. Raise GP_RESTARTS
to 8 — a 3D Matern kernel has three independent length scales and benefits
from thorough search.

The per-dimension EI curves are the key diagnostic: does EI for X1 peak
near 0.97--0.99, suggesting X1 wants to push further toward the boundary?
If yes, that guides the W7 submission direction.

### Module 17 connection
Module 17 Q3 (depth vs overfitting) maps directly. With 20 samples in 3D
(n/p=6.7), the GP is fitting a 3D surface with limited data. The 25%
exploration retained in EXPLOIT_RATIO=0.75 is the BBO equivalent of
dropout — regularising the exploitation to prevent the model over-committing
to a surrogate that may have poor coverage. Module 17 Q4 (loss function
proxy gap) is also flagged: if GP R^2 < 0.5 after Step 9, the EI proxy
is unreliable and UCB should be trusted more than EI for the final
candidate selection.

### Key settings
    EXPLOIT_RATIO = 0.75    # 25% exploration -- GP overfitting insurance
    EXPLOIT_SIGMA = 0.04    # Modest tighten around [0.966, 0.518, 0.403]
    GP_RESTARTS   = 8       # 3D kernel -- thorough length scale search

---

## F4 — EXPLOIT AGGRESSIVELY
**4D | 35 samples | n/p = 8.75 | Best = -0.5268 @ idx33 | W5 = -2.4571**

### What the data says
F4 has the most compelling exploitation case of all 8 functions. The last
several evaluations show a dramatic convergence trajectory: from values
in the -20 to -30 range down to -0.527 in just a few steps. The best
point [0.417, 0.376, 0.350, 0.308] was the second-to-last historical
evaluation, meaning we had been converging rapidly. All four coordinates
cluster tightly in the [0.3--0.42] range — a clear structural signal.
W5 submitted a point that scored -2.457, a regression, but still in the
top 15% of all 35 evaluations.

### Strategy
Aggressive exploitation: EXPLOIT_RATIO=0.85, EXPLOIT_SIGMA=0.03. The
search concentrates tightly around [0.417, 0.376, 0.350, 0.308]. With 35
samples and only 4 dimensions (n/p=8.75) the GP is reliable enough to
trust the EI acquisition fully. GP_RESTARTS raised to 8 to capture the
tight peak structure around the [0.3--0.42]^4 region precisely.

### Module 17 connection
F4 is the textbook answer to Module 17 Q1 (progressive feature extraction).
The evaluation history IS a three-layer CNN: early evaluations (idx 0--20)
found rough boundaries at -10 to -30, like raw pixel noise. Middle evals
(idx 20--30) found moderate improvement at -3 to -7, like texture detection.
The final evaluations found the peak region: -0.527. W6 is the final
classification step. Module 17 Q3 (overfitting balance) is also answered:
with n/p=8.75, the GP is well-conditioned enough to support EXPLOIT_RATIO
0.85 without over-committing — the equivalent of having enough training data
that you can train a deeper network without dropout.

### Key settings
    EXPLOIT_RATIO = 0.85    # Rapid convergence trajectory -- exploit hard
    EXPLOIT_SIGMA = 0.03    # All 4 coords in [0.3-0.42] -- tight target
    GP_RESTARTS   = 8       # 4D kernel -- ensure peak structure captured

---

## F5 — PRECISION EXPLOIT
**4D | 25 samples | n/p = 6.25 | Best = 2912.987 @ idx23 | W5 = +24.48**

### What the data says
F5 has the most dramatic landscape of all 8 functions. The best score of
2912.987 is nearly 3x the second-best value (1088.86). This is a sharp
spike in 4D space at [0.354, 0.918, 0.997, 0.945], with X3 and X4 pushed
firmly toward the upper boundary. W5 drifted far from the spike, returning
only 24.478. The GP must be re-anchored to the spike location in W6.

### Strategy
Maximum exploitation: EXPLOIT_RATIO=0.90, EXPLOIT_SIGMA=0.02 — the
tightest settings of any function. 90% of 10,000 candidates are drawn
from a very tight Gaussian (radius ±0.04) around the spike. GP_RESTARTS
set to 10 (maximum) because the outlier spike is the hardest GP fitting
challenge in the batch — the GP may smooth over it, producing a poor
surrogate. GP R^2 must be checked carefully in Step 9.

### Module 17 connection
F5 answers Module 17 Q1 (progressive extraction) most literally. The
evaluation history is a perfect three-stage CNN hierarchy: edges (weeks
1--3, values 4--108), textures (weeks 3--5, values 355--1089), semantic
object (week 5 endpoint, value 2912). W6 is precision inference.

Module 17 Q4 (activations) is sharply relevant. EI = max(0, mu - 2912.987).
With the dataset mean at 293, almost every candidate produces EI=0 except
in the spike neighbourhood. This is the most extreme sparse activation map
in the batch — the BBO equivalent of a ReLU layer that passes only one
or two neurons per input. The per-dimension EI curves for X3 and X4 should
both peak near 1.0 (upper boundary effect).

### Key settings
    EXPLOIT_RATIO = 0.90    # Maximum -- spike is confirmed
    EXPLOIT_SIGMA = 0.02    # Tightest -- spike is sharp not a ridge
    GP_RESTARTS   = 10      # Maximum -- outlier spike stresses the GP

---

## F6 — EXPLOIT WITH MOMENTUM
**5D | 25 samples | n/p = 5.0 | Best = -0.3630 @ idx23 | W5 = -1.7662**

### What the data says
All 25 output values are negative. The best point [0.390, 0.198, 0.588,
0.826, 0.049] has an interesting structure: X4=0.826 is high and X5=0.049
is very close to the zero boundary. The last 6 evaluations showed a strong
improving trend culminating in the best ever score at idx 23. W5 then
regressed to -1.766. Recovery mode for W6.

### Strategy
Return to the best-known region but with elevated caution. EXPLOIT_RATIO
reduced to 0.70 (30% exploration) because n/p=5.0 is the sparsest GP
problem in the W6 batch — 25 samples across 5 dimensions. UCB_KAPPA
raised to 2.5 because sparse GP uncertainty means the sigma estimates are
less reliable; a higher exploration bonus compensates. GP_RESTARTS=8 for
the 5 independent length scales in the 5D Matern kernel.

The per-dimension EI curves are the most valuable diagnostic for F6: does
X5 EI peak at or near 0.0 (confirming a boundary effect)? Does X4 EI peak
above 0.826 (suggesting we should push X4 toward 1.0 in W7)?

### Module 17 connection
F6 is the clearest overfitting warning of the W6 batch. Module 17 Q3
(depth vs overfitting) asked whether we faced the same trade-offs as CNN
training. F6's answer: 25 samples in 5D is like training a CNN on 25
images. The 30% exploration in EXPLOIT_RATIO=0.70 and elevated kappa=2.5
are the direct equivalents of L2 regularisation and dropout.

Module 17 Q4 (convolutions as per-dimension filters) is also relevant:
the GP Matern kernel learns 5 independent length scales, one per dimension.
A short length scale for X5 (where the best point has X5=0.049) would
confirm X5 is a high-frequency dimension -- the function is sensitive to
small changes there, like a high-frequency convolutional filter detecting
fine edges near the zero boundary.

Module 17 Q5 (Dunbar edge AI deployment) resonates most here. A CNN
deployed with only 25 training images would not be trusted without careful
uncertainty quantification. The GP R^2 saved in Step 15 is our deployment
confidence score: if R^2 < 0.4, the model should not be relied upon for
aggressive exploitation decisions.

### Key settings
    EXPLOIT_RATIO = 0.70    # n/p=5.0 is sparse -- 30% exploration = regularisation
    UCB_KAPPA     = 2.5     # Sparse GP -- elevated exploration bonus
    GP_RESTARTS   = 8       # 5 length scale params in 5D kernel

---

## F7 — STRUCTURED EXPLOIT
**6D | 35 samples | n/p = 5.83 | Best = 1.3650 @ idx6 | W5 = +0.5763**

### What the data says
F7 found its best value at idx 6 -- the seventh evaluation ever -- and has
been circling the 1.2--1.3 range recently without beating it. The last
four evaluations returned 1.228, 0.809, 1.140, then W5 dropped to 0.576.
The best point [0.058, 0.492, 0.247, 0.218, 0.420, 0.731] has a distinctive
profile: X1=0.058 is near the zero boundary and X6=0.731 is high. This
suggests the function has strong directional structure in at least X1 and X6.

### Strategy
Standard exploitation settings (EXPLOIT_RATIO=0.80) with a modest tightening
of sigma to 0.04. The region around the best point is known -- 20% exploration
is appropriate insurance in 6D. GP_RESTARTS raised to 8 for the 6 independent
length scales in the 6D Matern kernel.

The per-dimension EI curves (Step 11) are the key diagnostic: does X1 EI
peak near 0.0--0.05 (confirming the boundary effect)? Does X6 EI peak above
0.731 (suggesting X6 should be pushed toward 1.0 in W7)? Reading the 6 GP
fitted length scales after Step 9 reveals which dimensions are the
high-frequency "edge-detection" channels -- short length scale = sensitive,
needs precise targeting.

### Module 17 connection
F7 is the perfect answer to Module 17 Q2 (LeNet breakthroughs and incremental
improvement). The best value was found at idx 6 -- equivalent to LeNet proving
the paradigm in 1998. Every evaluation since has been the incremental refinement
phase: AlexNet (2012), VGG (2014), ResNet (2016) -- getting closer to the peak
without fundamentally changing the approach. W6 is the ResNet step: we introduce
skip connections in the form of per-dimension acquisition curves that let
information flow directly from idx 6 to the W6 submission.

Module 17 Q4 (convolutions) is also relevant: the 6 GP length scales are the
6 learned convolutional filters over the input dimensions. Short length scale
for X1 (near boundary) would confirm a high-frequency, edge-detection response
in that dimension -- the most actionable output of the Step 9 GP fit.

### Key settings
    EXPLOIT_RATIO = 0.80    # Standard -- region known, 20% exploration in 6D
    EXPLOIT_SIGMA = 0.04    # Modest tighten -- best point well-identified
    GP_RESTARTS   = 8       # 6 length scales in 6D kernel

---

## F8 — EXPLOIT + CNN EXPERIMENT
**8D | 45 samples | n/p = 5.63 | Best = 9.8188 @ idx42 | W5 = +8.9560**

### What the data says
F8 is the most mature and data-rich function in the batch. The best score
of 9.8188 was achieved at idx 42 -- the second-to-last historical evaluation
-- and W5 returned 9.334, confirming the GP has stayed in the high-value
region. The top 5 scores (9.183, 9.334, 9.344, 9.598, 9.819) are tightly
clustered, giving the GP excellent signal. All 45 outputs are positive
(range 5.5--9.82, std=1.04) -- the most well-conditioned GP fitting problem
in the batch. The best point [0.012, 0.366, 0.002, 0.165, 0.448, 0.535,
0.153, 0.745] has X1=0.012 and X3=0.002 both near the zero boundary -- a
strong structural signature.

### Strategy
EXPLOIT_RATIO=0.85, EXPLOIT_SIGMA=0.03 -- the tightest Gaussian around the
8D best point. GP_RESTARTS=10 (maximum) to fit the 8 independent length
scales of the 8D Matern kernel. F8 also runs a 1D CNN classifier as an 8th
competitor in the Step 5 model comparison. The CNN is the only Module 17
experiment in the entire W6 batch.

### CNN experiment rationale
Three conditions must be met to justify testing a CNN over standard MLP:

    1. Sufficient samples:    F8 has 45 -- only function above 40
    2. Sufficient dimensions: 8D gives conv filter meaningful local structure
    3. Sufficient signal:     tight range (5.5-9.82) = clear positive class

A 1D CNN treats the 8 input coordinates as an 8-channel sequence and applies
a sliding convolutional filter (kernel size 3) to detect local co-occurrence
patterns -- e.g. low X1 AND low X3 together predict high output. This is
exactly the interaction structure the best point's X1=0.012, X3=0.002
signature suggests.

Decision rule: if CNN CV accuracy > all 7 standard models, CNN filters the
10,000 candidates. Otherwise fall back to the standard CV winner. The GP
surrogate is used in all cases regardless.

### Module 17 connection — all five questions answered by F8

Q1 (Progressive extraction):
    45 evaluations = textbook three-stage hierarchy.
    Evals 1-20:  broad exploration, values 5.5-9.0  (edges)
    Evals 21-38: finding high-value clusters, 8.0-9.6 (textures)
    Evals 39-43: converging on peak, 9.18-9.82 (object recognition)
    W6 is inference: features extracted, object identified, classify precisely.

Q2 (LeNet breakthroughs):
    F8's improvement curve from mean 7.85 early to 9.82 recent mirrors
    the accuracy curves of successive CNN generations on ImageNet. More data
    + better surrogate = incrementally higher peak, just like AlexNet -> VGG.

Q3 (Depth / overfitting balance):
    The CNN experiment IS the direct answer. Which architecture's capacity
    best matches 45 samples in 8D? Small, Medium, Large MLP, or 1D CNN?
    The CV comparison in Step 7 resolves this empirically.

Q4 (Convolutions / pooling / activations / loss):
    Convolutions: 1D CNN detects co-occurrence in 8-coord input.
                  GP Matern kernel detects same via short X1, X3 length scales.
    Pooling:      85% of candidates Gaussian-pooled near best point.
                  5,000 of 10,000 survive the classifier filter (2nd pool).
    Activations:  EI = max(0, mu - 9.819 - 0.01) -- sparse but meaningful.
    Loss proxy:   EI optimises a surrogate objective, not the true function.
                  GP R^2 and sigma calibration tracked in Step 15 JSON.

Q5 (Dunbar edge AI / benchmarking):
    F8's Step 15 JSON records the CNN experiment outcome, 8 GP length scales,
    CV winner rationale, and submission coordinates. This is the deployment
    documentation Dunbar described as essential for responsible deployment.
    Success is not just 'did we beat 9.819' but: is the result reproducible,
    is the GP calibrated, did the CNN add value?

### Key settings
    EXPLOIT_RATIO  = 0.85    # Strong recent trajectory -- press on
    EXPLOIT_SIGMA  = 0.03    # X1=0.012, X3=0.002 near zero -- precision needed
    GP_RESTARTS    = 10      # Maximum -- 8 length scales in 8D kernel
    CNN_EXPERIMENT = True    # Module 17 experiment -- 1D conv classifier

---

## Summary Table

| Fn | Dims | n/p  | Strategy               | exploit | sigma | kappa | gp_r |
|----|------|------|------------------------|---------|-------|-------|------|
| F1 | 2D   | 7.50 | EXPLORE                | 0.60    | 0.08  | 3.0   | 5    |
| F2 | 2D   | 7.50 | TIGHT EXPLOIT          | 0.85    | 0.03  | 2.0   | 8    |
| F3 | 3D   | 6.67 | EXPLOIT CAREFULLY      | 0.75    | 0.04  | 2.0   | 8    |
| F4 | 4D   | 8.75 | EXPLOIT AGGRESSIVELY   | 0.85    | 0.03  | 2.0   | 8    |
| F5 | 4D   | 6.25 | PRECISION EXPLOIT      | 0.90    | 0.02  | 2.0   | 10   |
| F6 | 5D   | 5.00 | EXPLOIT WITH MOMENTUM  | 0.70    | 0.05  | 2.5   | 8    |
| F7 | 6D   | 5.83 | STRUCTURED EXPLOIT     | 0.80    | 0.04  | 2.0   | 8    |
| F8 | 8D   | 5.63 | EXPLOIT + CNN EXPT     | 0.85    | 0.03  | 2.0   | 10   |

Note: gp_r = GP_RESTARTS. All functions use N_CANDIDATES=10000,
TOP_PERCENTILE=30, FILTER_PERCENTILE=50, RANDOM_SEED=42, MAXIMIZE=True.

---

*Week 6 | BBO Capstone | Mike Kennelly*
