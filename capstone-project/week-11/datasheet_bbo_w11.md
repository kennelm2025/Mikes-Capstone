# Data Card — BBO Capstone Week 11

### Mike Kennelly | Imperial College | Penultimate Query

\---

## 1\. Dataset Overview

|Property|Value|
|-|-|
|**Dataset name**|BBO Capstone Evaluation History — W1-W10|
|**Version**|Week 11 (penultimate, 16 npy files)|
|**Format**|NumPy .npy arrays (inputs + outputs per function)|
|**Total files**|16 (f1-f8, inputs + outputs)|
|**Total evaluations**|247 across all 8 functions . Lot 1|
|**Collection method**|Sequential portal evaluation — one submission per function per week|
|**Collection period**|Weeks 1-10, Imperial College BBO Capstone portal|
|**Provenance**|Black-box oracle — function internals unknown|

\---

## 2\. Per-Function Dataset Summary (W11 npy files — W1-W10 history)

|Fn|Dims|n (W11)|n/p ratio|Y min|Y max|Y mean|Y std|ATB entering W11|ATB Week|
|-|-|-|-|-|-|-|-|-|-|
|F1|2D|19|9.5|-3.61e-03|1.658e-09|-1.90e-04|8.3e-04|8.838e-07|W2|
|F2|2D|20|10.0|-0.066|0.6497|0.319|0.189|0.6497|W9|
|F3|3D|24|8.0|-0.399|-0.000707|-0.088|0.077|-0.000707|W6|
|F4|4D|39|9.75|-32.63|-0.129|-13.95|6.71|-0.129 (negative only)|W6|
|F5|4D|30|7.5|0.113|8662.48|1,799|2,886|8662.48|W9|
|F6|5D|29|5.8|-2.571|0.03602|-1.197|0.582|0.03602|W9|
|F7|6D|39|6.5|0.003|2.7201|0.572|0.676|2.7201|W10|
|F8|8D|49|6.1|5.500|9.8251|8.051|0.861|9.8251|W7|

**Note on F4:** The true ATB entering W11 is the W2 result of +0.23759 — however this sits in the W1-W10 npy file. The npy-reported best of -0.129 reflects that the W4 submission idx=34 is the argmax of the W11 npy slice (W1-W10 only). The +0.23759 ATB at idx=1 (W2) is correctly identified by np.argmax(Y) on the full array.

**Correction:** F4 W11 npy best is 0.23759 at idx=1 (W2 portal result correctly present in file).

\---

## 3\. File Reference

### W11 Input/Output Files

|File|Shape|Description|
|-|-|-|
|f1\_w11\_inputs.npy|(19, 2)|F1 coordinates W1-W10|
|f1\_w11\_outputs.npy|(19,)|F1 oracle values W1-W10|
|f2\_w11\_inputs.npy|(20, 2)|F2 coordinates W1-W10|
|f2\_w11\_outputs.npy|(20,)|F2 oracle values W1-W10|
|f3\_w11\_inputs.npy|(24, 3)|F3 coordinates W1-W10|
|f3\_w11\_outputs.npy|(24,)|F3 oracle values W1-W10|
|f4\_w11\_inputs.npy|(39, 4)|F4 coordinates W1-W10|
|f4\_w11\_outputs.npy|(39,)|F4 oracle values W1-W10|
|f5\_w11\_inputs.npy|(30, 4)|F5 coordinates W1-W10|
|f5\_w11\_outputs.npy|(30,)|F5 oracle values W1-W10|
|f6\_w11\_inputs.npy|(29, 5)|F6 coordinates W1-W10|
|f6\_w11\_outputs.npy|(29,)|F6 oracle values W1-W10|
|f7\_w11\_inputs.npy|(39, 6)|F7 coordinates W1-W10|
|f7\_w11\_outputs.npy|(39,)|F7 oracle values W1-W10|
|f8\_w11\_inputs.npy|(49, 8)|F8 coordinates W1-W10|
|f8\_w11\_outputs.npy|(49,)|F8 oracle values W1-W10|

**Total evaluations entering W11:** 19+20+24+39+30+29+39+49 = **249 evaluations**

### How W11 Files Were Built

Each W11 npy = W10 npy with the W10 portal result appended:

```python
X\_w11 = np.vstack(\[X\_w10, w10\_submission\_coords])
Y\_w11 = np.append(Y\_w10, w10\_portal\_result)
```

F5 shares rows with W9/W10 because \[1,1,1,1] was submitted multiple times — exact
duplicate rows retained in file (no deduplication applied).

\---

## 4\. Complete W1-W10 Submission History

### F1 (2D) — Near-zero degenerate landscape

|Week|X1|X2|Output|Note|
|-|-|-|-|-|
|W1|0.0825|1.5395|0.0|Baseline|
|W2|0.6842|0.7042|8.838e-07|ATB W2-W10|
|W3|0.9010|0.8770|5.17e-96|—|
|W4|0.6884|0.7241|1.658e-09|—|
|W5|0.5323|0.6306|-5.44e-07|—|
|W6|0.0739|0.4071|1.666e-85|—|
|W7|0.5828|0.4823|-2.221e-17|—|
|W8|0.8871|0.6688|1.259e-49|—|
|W9|0.9799|1.0000|-2.447e-183|—|
|W10|0.9119|0.6619|4.109e-58|—|

**W11 strategy:** ATB OVERRIDE to \[0.684200, 0.704200]. GP R2=1.0, EI\~0, flat landscape.
**W11 result:** 8.968e-07 — NEW ATB

\---

### F2 (2D) — Two-zone landscape

|Week|X1|X2|Output|Zone|
|-|-|-|-|-|
|W1|0.7056|1.4879|0.5246|HIGH X2|
|W2|0.7736|0.9639|0.2847|HIGH X2|
|W3|1.0000|1.0000|-0.0298|HIGH X2|
|W4|0.7809|0.9915|0.0188|HIGH X2|
|W5|0.7101|0.1616|**0.6497**|LOW X2 — ATB|
|W6|0.7008|0.1261|0.5844|LOW X2|
|W7|0.6890|0.1688|0.5338|LOW X2|
|W8|0.7128|0.0425|0.4926|LOW X2 (too low)|
|W9|0.6427|0.9384|0.3252|HIGH X2 (drifted)|
|W10|0.6402|0.0402|0.1636|LOW X2 (too low)|

**Module 22 clustering (applied to W1-W10):**

* Zone A HIGH X2 (W1,W2,W3,W4,W9): centroid \[0.730, 0.900], mean=0.224
* Zone B LOW X2 (W5,W6,W7,W8,W10): centroid \[0.694, 0.100], mean=0.474
* Inter-zone distance = 0.804 | Zone B spread = 0.037 | ATB->centroid dist = 0.048

**W11 strategy:** ATB OVERRIDE to \[0.710068, 0.161630] (W5/W9 ATB coords).
**W11 result:** 0.6090 — recovery but below ATB (stochastic component suspected)

\---

### F3 (3D) — Closest-to-zero maximisation

|Week|X1|X2|X3|Output|Note|
|-|-|-|-|-|-|
|W1|0.9660|0.5177|0.4028|-0.01358|Baseline|
|W2|1.0000|0.5366|0.5780|-0.03277|—|
|W3|0.4457|0.0675|0.4788|-0.08337|X1 interior - bad|
|W4|0.9949|0.9230|0.0020|-0.13795|—|
|W5|0.1503|0.4416|0.3353|-0.05900|—|
|W6|0.9981|0.6212|0.4531|-0.00707|ATB W6-W10|
|W7|1.0000|0.5717|0.5040|-0.00534|Near ATB|
|W8|0.9815|0.5406|0.1920|-0.11316|X3 drift|
|W9|0.7504|0.5915|0.4481|-0.01348|X1 drift|
|W10|0.9295|0.6844|0.6214|-0.09015|X1=0.929 regression|

**Key structural finding:** X1 must stay near 1.0. Every submission with X1 < 0.95 regressed.
**W11 strategy:** ATB OVERRIDE to \[0.998126, 0.621218, 0.453080].
**W11 result:** -0.001285 — NEW ATB (closest-to-zero in 11 weeks)

\---

### F4 (4D) — Single isolated positive basin

|Week|X1|X2|X3|X4|Output|Note|
|-|-|-|-|-|-|-|
|W1|0.4141|0.4771|0.4657|0.4741|-2.627|Baseline|
|W2|0.4392|0.4150|0.3847|0.3979|**+0.23759**|Only positive|
|W3|0.4339|0.4014|0.3052|0.3928|-0.962|—|
|W4|0.4169|0.3757|0.3499|0.3077|-0.527|—|
|W5|0.3660|0.5263|0.3948|0.3050|-2.457|—|
|W6|0.4099|0.4383|0.4558|0.3499|-0.129|—|
|W7|0.4518|0.4386|0.4002|0.3951|-0.265|—|
|W8|0.3534|0.4776|0.4233|0.4181|-0.554|—|
|W9|0.5221|0.3899|0.4309|0.3568|-1.405|—|
|W10|0.4769|0.4940|0.4204|0.3467|-1.801|—|

**W2 ATB discovery:** Pure GP EI (xi=0.01, 75 restarts). EI shifted X2/X3/X4 DOWN
from W1 by -0.062/-0.081/-0.076 respectively, crossing the positive threshold.
**W11 strategy:** ATB OVERRIDE to \[0.439249, 0.414994, 0.384687, 0.397917].
**W11 result:** +0.23759 — exact ATB match confirmed. Coords are correct.

\---

### F5 (4D) — Corner maximisation

|Week|Output|X1|X2|X3|X4|Note|
|-|-|-|-|-|-|-|
|W1|60.07|0.1199|0.4986|0.4779|0.4947|Baseline|
|W2|4,062.1|0.2990|0.9683|1.000|1.000|ATB|
|W3|4,890.6|0.8030|0.9455|0.9975|0.9763|ATB|
|W4|2,913.0|0.3547|0.9182|0.9966|0.9454|—|
|W5|24.48|0.4531|0.6716|0.3037|0.7912|Bad — X3 low|
|W6|5,875.1|0.7810|1.000|1.000|1.000|ATB|
|W7|7,596.8|0.9377|1.000|1.000|1.000|ATB|
|W8|8,382.5|0.9851|1.000|1.000|1.000|ATB|
|W9|8,662.48|1.000|1.000|1.000|1.000|ATB — confirmed corner|
|W10|8,471.3|1.000|1.000|0.9899|1.000|X3 perturbation regressed|

**W10 perturbation:** X3=0.9899 confirmed drop to 8471. \[1,1,1,1] = global max.
**W11 strategy:** ATB OVERRIDE to \[1,1,1,1].
**W11 result:** 8662.48 — exact ATB match

\---

### F6 (5D) — X5-threshold landscape

|Week|X1|X2|X3|X4|X5|Output|Note|
|-|-|-|-|-|-|-|-|
|W1|0.0217|0.5626|0.4672|0.5344|0.4237|-1.3389|—|
|W2|0.4096|0.2992|0.5097|0.8141|0.0721|-0.2372|ATB|
|W3|0.2115|0.0611|0.4551|0.9055|0.0040|-0.8835|—|
|W4|0.3897|0.1980|0.5876|0.8263|0.0489|-0.3630|ATB|
|W5|0.0165|0.0224|0.0442|0.8005|0.4569|-1.7662|X5 too high|
|W6|0.4271|0.3258|0.5981|0.7802|0.1439|-0.1727|ATB|
|W7|0.4973|0.2948|0.5631|0.6850|0.1292|-0.3422|—|
|W8|0.4602|0.3015|0.5496|0.8391|0.2007|-0.4006|X5 too high|
|W9|0.4066|0.3395|0.6348|0.7694|**0.1153**|**+0.03602**|ATB — first positive|
|W10|0.3899|0.3338|0.6524|0.7643|0.0787|-0.1443|X5 too low|

**X5 threshold:** X5=0.115 -> positive. X5=0.079 (W10) -> negative. Narrow \[0.10, 0.13] band.
**W9 ATB discovery:** Precision lock (sigma=0.018), RF CV=91.7%, 100% exploit candidates,
GP EI 79.2% exploitation-driven. Submitted point 0.013 from W6 ATB centroid.
**W11 strategy:** ATB OVERRIDE to \[0.406643, 0.339495, 0.634775, 0.769397, 0.115269].
**W11 result:** -0.01024 — regressed (X5 threshold sensitivity confirmed)

\---

### F7 (6D) — Trending cluster

|Week|Output|X1|X6|Step|Note|
|-|-|-|-|-|-|
|W1|0.8085|0.0579|0.4847|—|Baseline|
|W2|1.7392|0.0162|0.6978|—|ATB|
|W3|1.7358|0.0000|0.6372|—|—|
|W4|1.1399|0.1005|0.6665|—|—|
|W5|0.5763|0.2726|0.5496|—|—|
|W6|2.1190|0.0552|0.6850|—|ATB — trend begins|
|W7|2.4134|0.0781|0.6931|0.061|ATB|
|W8|2.5982|0.0964|0.6996|0.049|ATB|
|W9|2.5968|0.0960|0.7000|0.001|Near-stationary|
|W10|2.7201|0.1251|0.7029|0.042|ATB — 5th consecutive|

**Module 22 trending cluster (W6-W10):**

* Step sizes \[0.061, 0.049, 0.001, 0.042] — tight, consistent direction
* X1 rising, X6 rising, X2-X5 declining each week
* Intra-cluster spread = 0.057 (tight — genuine gradient confirmed)
* Dynamic (moving) centroid distinguishes F7 from static attractors

**W11 strategy:** GP PIPELINE — Logistic Regression filter, ANISO\_SIGMA \[0.015,0.012x4,0.015]
**W11 GP output:** mu=2.767 > ATB=2.720 — GP predicted new best
**W11 result:** 2.8501 — NEW ATB (6th consecutive improvement)

\---

### F8 (8D) — Zero-boundary structure

|Week|Output|X1|X3|X7|Note|
|-|-|-|-|-|-|
|W1|9.0093|0.009|0.516|0.579|Baseline|
|W2|**9.8320**|**0.000**|**0.000**|**0.000**|ATB — zero-boundary|
|W3|9.8188|0.012|0.002|0.153|Near-zero — close|
|W4|9.3341|0.069|0.001|0.048|Deviation|
|W5|8.9560|0.124|0.199|0.379|Large deviation|
|W6|9.7741|0.000|0.069|0.292|X1=0, X3/X7 non-zero|
|W7|9.8251|0.040|0.004|0.167|Near ATB|
|W8|9.8021|0.008|0.000|0.167|X3=0, others non-zero|
|W9|9.8115|0.041|0.000|0.162|X3=0, X1/X7 non-zero|
|W10|9.8013|0.044|0.007|0.165|All non-zero|

**Structural finding:** Only W2 had X1=X3=X7=0 exactly. Every deviation from exact zeros
returned below ATB. GP (xi=0.1, 200 restarts, Matern LS=3.59) discovered the zero-boundary
pattern in one step from 41 points in 8D space at W2.
**W11 strategy:** SPARSITY HYPOTHESIS — aniso sigma with X1/X3/X7 sigma=0.006 (near-zero).
GP best\_point was already sparse (X1=0.040, X3=0.004) — no sparsity override triggered.
**W11 result:** 9.8269 — recovery vs W10 but still 0.005 below W2 ATB

\---

## 5\. Module 22 Clustering Analysis (W1-W10 Data)

### Cluster Statistics

|Fn|n (W11)|Top-3 Spread|ATB->Centroid|Cluster Type|Key Insight|
|-|-|-|-|-|-|
|F1|19|0.014|0.007|Tight static|\[0.684, 0.704] basin|
|F2|20|0.037|0.048|Two-zone|LOW-X2 is high-value basin|
|F3|24|0.047|0.024|Tight static|X1=1.0 boundary anchor|
|F4|39|0.062|0.031|Isolated|One positive among negatives|
|F5|30|0.007|0.003|Corner — tightest|Monotonic corner solution|
|F6|29|0.030|0.015|Tight static|X5=0.115 threshold|
|F7|39|0.057|0.043|Trending dynamic|Centroid moving W6->W10|
|F8|49|0.411|0.392|Loose boundary|Zero-boundary is structural key|

### F2 — Two-Zone Analysis (W1-W10 slice)

Applied to the 20 evaluations entering W11:

* **Zone A HIGH X2** (W1,W2,W3,W4,W9 — X2>0.5): centroid \[0.730, 0.900], mean output = 0.224
* **Zone B LOW X2** (W5,W6,W7,W8,W10 — X2<=0.5): centroid \[0.694, 0.100], mean output = 0.474
* Inter-zone distance: 0.804
* Zone B spread: 0.037 — tight attractor confirmed
* ATB (W5) to Zone B centroid distance: 0.048

Note: Zone B centroid shifts slightly compared to full 11-round analysis (0.012 dist at W12)
because W11 adds another LOW-X2 evaluation, pulling the centroid closer to the ATB.

### F7 — Trending Cluster Analysis (W6-W10 slice)

Weekly step sizes for the W6-W10 trending cluster:

|Transition|Step Size (6D)|
|-|-|
|W6 -> W7|0.061|
|W7 -> W8|0.049|
|W8 -> W9|0.001|
|W9 -> W10|0.042|

Intra-cluster spread (W6-W10): 0.057. Consistent direction confirmed.
W11 GP prediction (mu=2.767 > ATB=2.720) validated by cluster trajectory.

\---

## 6\. Data Limitations

|Limitation|Detail|
|-|-|
|Black-box oracle|Function definitions unknown. No gradient available.|
|Small n|n ranges from 19 (F1) to 49 (F8). Borderline for reliable GP in high dimensions.|
|Observed stochasticity|F2: same coords returned 0.6497 (W5) and 0.6090 (W11 replication).|
|No repeated evaluations|Except F2 (W5/W11) and F4 (W2/W11). No noise estimate possible.|
|Boundary evaluations|F5 has multiple \[1,1,1,1] entries. F3 has X1=1.0 entries. GP uncertainty elevated at boundaries.|
|F4 note|W11 npy best is -0.129 at idx=34 before realising W2 result (+0.23759) is at idx=1. Always use np.argmax(Y) not Y\[-1] for ATB detection.|

\---

## 7\. Intended Use

|Property|Value|
|-|-|
|**Primary use**|Training GP/classifier surrogates for BBO Capstone W11 submissions|
|**Secondary use**|Module 22 clustering to validate ATB override and GP trust decisions|
|**Prohibited use**|Any real-world optimisation without independent validation|
|**Licence**|Academic use only — Imperial College BBO Capstone|

\---

*BBO Capstone Data Card — Mike Kennelly — Imperial College — Week 11*

