# ══════════════════════════════════════════════════════════════════
# STEP 11B — PROMPT ENGINEERING DESIGN NOTE
# F6 W10 | Ollama llama3.1 | Module 20 Learning Exercise
# ══════════════════════════════════════════════════════════════════
#
# PROMPT DESIGN RATIONALE
# ───────────────────────
# This prompt was structured using the same principles applied in our
# Ollama Llama deployment project, where we learned that prompt
# architecture significantly affects output reliability and relevance.
#
# PRINCIPLE 1 — ROLE DEFINITION
#   We open with "You are a Bayesian optimisation analyst..."
#   rather than diving straight into the data. This grounds the
#   model in the correct reasoning frame before it sees any numbers.
#   In our SmartDog work we found that role-less prompts produced
#   generic responses; role-anchored prompts produced domain-specific
#   reasoning. The same principle applies here.
#
# PRINCIPLE 2 — TASK CONTEXT BEFORE DATA
#   We explain WHAT the function is (black-box, 5D, maximisation)
#   and WHAT the numbers mean (sensitivity = GP mean change per unit)
#   before presenting the data table. This mirrors the few-shot
#   learning pattern from Module 20: models perform better when
#   the task structure is established before the examples arrive.
#
# PRINCIPLE 3 — STRUCTURED DATA FORMAT
#   Sensitivity scores are presented as a labelled table rather than
#   a flat list. LLMs handle structured, consistently formatted input
#   more reliably than unstructured prose — the model can parse
#   column relationships rather than inferring them from context.
#
# PRINCIPLE 4 — CONSTRAINED OUTPUT FORMAT
#   We ask for exactly 4 numbered answers rather than open-ended
#   commentary. This is the delimiting context principle from
#   Module 19/20 — constraining the output format reduces entropy
#   in the response and makes the output directly usable in the
#   notebook without post-processing.
#
# PRINCIPLE 5 — ONE-SHOT EXAMPLE (ANCHORING)
#   We include a single worked example of the reasoning style we want.
#   This is few-shot learning in practice — showing the model what
#   good analytical reasoning looks like before asking it to produce
#   its own. Without this anchor, Llama3.1 tends toward verbose
#   general statements rather than specific coordinate-level analysis.
#
# PRINCIPLE 6 — LOW TEMPERATURE (0.3)
#   Analytical tasks require precision over creativity. A temperature
#   of 0.3 concentrates probability mass on the most likely correct
#   tokens — the same principle as the low-temperature precision
#   sampling strategy we applied to F2 and F5 in the BBO pipeline
#   itself. High temperature here would produce plausible-sounding
#   but unreliable recommendations.
#
# ══════════════════════════════════════════════════════════════════

def build_f6_prompt(sensitivities, best_point, submission, atb_value, w9_result):
    """
    Structured prompt for Ollama llama3.1 to interpret F6 per-dimension
    GP sensitivity scores and recommend W10 search strategy.
    
    Prompt architecture follows SmartDog deployment principles:
    role → context → data → example → constrained questions
    """
    
    dim_names = ['X1', 'X2', 'X3', 'X4', 'X5']
    
    # ── Format sensitivity table ──────────────────────────────────
    sens_lines = []
    for name, s, bp, sp in zip(dim_names, sensitivities, best_point, submission):
        drift = abs(bp - sp)
        flag = ' ← DRIFT WARNING' if drift > 0.05 else ''
        sens_lines.append(
            f"  {name}: sensitivity={s:.4f} | ATB_coord={bp:.4f} | "
            f"W9_submitted={sp:.4f} | drift={drift:.4f}{flag}"
        )
    sens_table = '\n'.join(sens_lines)
    
    # ── Build prompt using SmartDog principles ────────────────────
    prompt = f"""You are a Bayesian optimisation analyst reviewing the results \
of a Gaussian Process surrogate model fitted to an unknown 5-dimensional \
black-box function. Your role is to interpret per-dimension sensitivity \
scores and provide precise, actionable search recommendations.

TASK CONTEXT:
- Function: unknown, 5-dimensional, domain [0,1]^5, being MAXIMISED
- Training samples: 28 observations
- All-time best score: {atb_value:.6f} (achieved at coordinates below)
- Most recent result (W9): {w9_result:.6f} — this IS the new all-time best
- Next query budget: 1 point (sequential optimisation, one query per week)

DEFINITION:
Sensitivity score = magnitude of GP mean change per unit movement in that \
dimension, evaluated at the current best point. Higher = more influential. \
Lower = near optimal or less important.

PER-DIMENSION DATA:
{sens_table}

ATB COORDINATES (the point that produced the best score):
  X1={best_point[0]:.6f}, X2={best_point[1]:.6f}, X3={best_point[2]:.6f}, \
X4={best_point[3]:.6f}, X5={best_point[4]:.6f}

EXAMPLE OF THE REASONING STYLE I WANT:
If X3 had sensitivity=1.8 and the W9 submission drifted 0.08 from the ATB \
coordinate, you would say: "X3 is the highest sensitivity dimension and shows \
meaningful drift — tighten sigma to 0.010 and anchor close to ATB coordinate \
0.598. Priority: HIGH."

Now answer these four questions about the actual F6 data above:

1. TIGHTEN OR FREE: For each dimension X1-X5, state whether sigma should be \
tightened (exploit) or left moderately free (explore), and suggest a sigma value \
between 0.008 and 0.025.

2. HIGHEST IMPROVEMENT POTENTIAL: Which dimension offers the most scope for \
finding a better value than the current ATB, and why?

3. DRIFT RISK: Flag any dimension where the W9 submission drifted meaningfully \
from the ATB coordinate and explain the risk this poses.

4. LANDSCAPE SUMMARY: In exactly one sentence, describe what the overall \
sensitivity pattern suggests about the shape of this function's landscape.

Be specific. Use dimension names (X1-X5) and exact coordinate values throughout. \
Keep total response under 300 words."""

    return prompt

# ── Prompt engineering summary for notebook commentary ───────────
PROMPT_COMMENTARY = """
STEP 11B COMMENTARY — WHY WE BUILT THE PROMPT THIS WAY
═══════════════════════════════════════════════════════

This Ollama call demonstrates the same prompt engineering principles
we developed in our Llama deployment project, applied to a new domain.

The prompt has five deliberate structural layers:

1. ROLE ANCHOR
   Opening with a defined analyst role before presenting any data.
   Without this, Llama3.1 responds generically. With it, responses
   are domain-specific and use appropriate terminology.

2. TASK CONTEXT BEFORE DATA
   Explaining what the numbers mean before showing them — mirroring
   the few-shot principle from Module 20 where establishing task
   structure before examples improves model performance.

3. STRUCTURED DATA TABLE
   Consistently formatted, labelled columns with drift flags computed
   in Python before the prompt is built. Structured input produces
   more reliable structured output than prose descriptions.

4. ONE-SHOT EXAMPLE
   A single worked example of the reasoning style anchors the output
   format. This is few-shot learning in practice — the model follows
   the pattern rather than inventing its own.

5. CONSTRAINED OUTPUT
   Four numbered questions with explicit format requirements and a
   word limit. This is the delimiting context principle — reducing
   output entropy to make the response directly actionable.

Temperature 0.3 was chosen deliberately — the same low-temperature
logic we apply to precision exploitation in the BBO pipeline itself.
High temperature here would produce confident but unreliable analysis.

The LLM response is advisory only. The GP/EI pipeline remains the
primary decision mechanism. The value of this cell is interpretability
— translating quantitative sensitivity scores into plain-English
reasoning that can be reviewed, challenged, and documented.
"""

print(PROMPT_COMMENTARY)
