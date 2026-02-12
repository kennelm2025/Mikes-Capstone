The Bayesian Optimization Capstone Project – Mike Kennelly. 

Section 1: Project Overview:-

This repository documents my work for the Bayesian Optimization capstone project, a multi week exploration and optimization of eight synthetic black-box functions using Gaussian Process-based Bayesian Optimization techniques.

How the Capstone Works:

Maximizing eight unknown functions with one allowed query per function per week. Using the ML method Bayesian Optimization to find the highest value, I submit inputs weekly in a very precise format e.g. each query must use the format: x1-x2-x3-...-xn, where each xᵢ must begin with 0 and is specified to six decimal places(0.123456-0.654321) for a 2D function. Submissions are made via the capstone project portal and each week I reflect, revise, and iterate, over 12 rounds/weeks, building knowledge incrementally. The success criteria for the project include ; achieving the highest value, demonstrating thoughtful analysis and planning, and data-driven decision-making to determine the recommended submission each week. 

My Approach:

I chose Gaussian Process-based Bayesian Optimization as my primary method, with dimension-adaptive strategies. I also look to use including use of other models such as SVMs and ensemble trees to help with high dimensionality.

The Challenge:

There are eight synthetic black-box functions, that are unknown mathematical functions that accept inputs and return a single output. My goal is to find the inputs that give the ‘highest possible output’ for each function.

Key Characteristics:

•	Black box: I cannot see internal workings of the functions

•	Maximization:  Every function is a maximization task

•	Observable:  Can observe how functions respond to different inputs

•	Initially sparse:  Each function starts with only 10 known data points

•	Increasing complexity: Functions range from 2D to 8D in dimensionality

The Iterative Process: Each week follows this cycle:
1. Review existing data:  Analyse the growing dataset from previous weeks
2. Choose a new input point: Select one query point per function (8 total)
3. Submit via the capstone portal: Submit chosen inputs in the correct format
4. Receive output: Get new outputs once submission is processed
5. Update dataset:  Incorporate new data points into analysis
6. Revise my strategy: Adjust my approach based on learnings and new data points

I repeat this process each week, building understanding iteratively, just as optimisation unfolds in real-world ML projects. My weekly reflections support my final write-up and presentations.

Functions Overview - F1 and F2 are 2D functions,F3 is a 3d function, F4 and F5 are 4D functions, F6 is a D6 function, F7 is a 6D function and F8 is an 8D function.

Section 2: Inputs and Outputs:-

Each iteration consists of submitting a single query point per function and receiving a scalar response.

Inputs:

Inputs take a query format: x1-x2-x3-...-xn, each xi: lies in the range [0, 1] and is specified to six decimal places. Dimensionality varies by function (from 2D to 8D). I am constrained to one query per function per iteration per week.

Outputs: 

Outputs are a single real-valued scalar representing the functions response to the input data provided. Output scale, smoothness, and noise level are unknown and function-specific. Outputs are used only to inform subsequent modelling and query decisions

Examples: 
Inputs  : Function 5 -	[0.119879, 0.498557, 0.477944, 0.494719]

Outputs : Function 5 -	60.06641925294364
 
Section 3: Challenge Objectives:-

Key objectives include; achieving the highest possible value, demonstrating thoughtful analysis and planning, being data-driven in decision-making to determine the recommended submission each week.

Section 4: Technical Approach:-

I chose Gaussian Process (GP) Regression with acquisition function optimization as my primary method across all weeks.
Why Bayesian Optimization?
- Sample efficient: Makes intelligent decisions with limited data
- Handles uncertainty: Provides probabilistic predictions with confidence intervals
- Balances exploration/exploitation: Naturally trades off between finding new regions and refining known good areas
- Works in high dimensions: Only viable approach for 8D with 41 samples (0.00004% coverage)

Gaussian Process Model Kernel Configuration:

Kernel type: Matérn ν=2.5 (balances smoothness and flexibility)
Kernel components:
-	`ConstantKernel` : Scales output variance
-	`RBF/Matérn` : Captures spatial correlation between points
-	`WhiteKernel`:  Models observation noise
-	Hyperparameter optimization30+ random restarts to avoid local optima
-	Normalization:`normalize_y=True` for numerical stability

Example kernel setup:
```python
kernel = ConstantKernel(1.0, (1e-10, 1e10)) * \
         Matern(length_scale=0.3, length_scale_bounds=(0.01, 10.0), nu=2.5) + \
         WhiteKernel(noise_level=1e-10, noise_level_bounds=(1e-12, 1e-2))
```

Acquisition Function

I focused on Expected Improvement (EI) as my primary method, though I also explored Upper Confidence Bound (UCB) for each function. In Week 2, I developed a dimension-adaptive approach that adjusts parameters based on function complexity. 
I configured EI for maximization with:

For Low Dimensions (F1-F2, 2D):
-	Conservative parameters: ξ = 0.01, κ = 2.0
-	Emphasis on exploitation near known good regions
-	Justification: Small search space (10% coverage), so I can visualise landscape and safe to refine locally

For Mid Dimensions (F3-F5, 3D-4D):
-	Balanced approach: ξ = 0.01-0.05, κ = 2.0-2.3
-	Adjust based on convergence signals from previous weeks
-	I used a mix of exploration and exploitation

For High Dimensions (F6-F8, 5D-8D):
- I chose aggressive exploration: ξ = 0.1, κ = 2.5
- I trusted the GP recommendations even when counterintuitive e.g. F8 setting three dimensions to 0 based on low marginal impact
- 150-200 random restarts for acquisition optimization due to extreme sparsity e.g. 0.00004% coverage in 8D!!

Weekly Progression: Ongoing strategy and plans adopted :-


Week1: 

My Objectives:
-	Load and understand initial 10-point datasets
-	Fit initial Gaussian Process models
-	Explore basic acquisition functions (EI and UCB)
-	Generate first query recommendations

Method Used: 
-	Gaussian Process regression with Matérn kernel
-	Expected Improvement acquisition function
-	Standard parameters (ξ=0.01, κ=2.0)

Key Findings:
-	F1 (2D):** Best initial value ~7.7×10⁻¹⁶ (extremely small, near zero)
-	F2 (2D):** Best initial value ~0.61
-	F3 (3D):** All outputs negative, best ~-0.014
-	F4 (4D):** Best ~-2.6, wide range [-33 to -2.6]
-	F8 (8D):** Best ~9.3, high variance across samples

Exploration vs Exploitation:
-	Week 1 focused primarily on exploitation refining near known good points
-	Conservative approach to build initial understanding
-	Random restarts: 10-30 per function

What I Learned:
-	All functions exhibit non-linear behavior requiring GP modeling
-	Linear regression R² = 0.23 vs GP R² = 0.89 (F4) proves non-linearity
-	initial samples have poor coverage, especially in high dimensions

Proposed strategy for Week 2:
-	Continue conservative approach for converging functions
-	Increase exploration for poorly-performing functions
-	Track which Week 1 points perform well

Week 2: 
My Objectives:
-	Full Bayesian Optimization implementation with refined strategies
-	Dimension-adaptive parameter tuning
-	Comprehensive convergence analysis
-	Strategy visualization and justification

Method Used: 
-	Converging functions (F2, F5, F7): Exploitation-focused
-	Parameters: ξ=0.01, κ=2.0
-	Strategy: Local refinement near best points
-	Diverging functions (F1, F6, F8): Exploration-focused, Parameters: ξ=0.1, κ=2.5
-	Strategy: Bold GP-guided exploration
-	Balanced functions (F3, F4): Mixed approach
-	 Adjust based on EI/UCB signals

Key Findings:
-	F7 (6D):Week 1 ranked 2nd (0.809 vs 1.365) → Continue local refinement

-	F2 (2D): Week 1 ranked 3rd → Conservative exploitation. Already at 75th percentile for both dimensions

-	F5 (4D):Steady improvement.Maintain course Predicted 5.5% improvement

-	F1 (2D): Week 1 performed poorly → Try different region

-	F6 (5D):Week 1 ranked low, old exploration, 0.000021% coverage, should have used EI there.   

-	F8 (8D):Most critical decision, 0.000041% coverage (needle in haystack) , GP suggested: [0.0, 0.188, 0.0, 0.090, 0.923, 0.461, 0.0, 0.530], after feature analysis performed marginal effects, X₁, X₃, X₇ spear to have minimal impact and are safe to set to 0!
X₁: Δ = 0.2  (minimal impact)
X₂: Δ = 1.1  (moderate)
X₃: Δ = 0.3  (minimal impact)
X₄: Δ = 0.6  (low)
X₅: Δ = 4.8  (very high impact!)
X₆: Δ = 2.1  (high)
X₇: Δ = 0.4  (minimal impact)
X₈: Δ = 3.2  (very high impact!)

Key week 2 decision was on F8 : I decided to trust the GP outputs! Even if they looked crazy!
-	Accepted GP's [0.0, 0.188, 0.0, ...] recommendation
-	Predicted 10.244 vs current 9.598 = 6.7% improvement
-	Conservative alternative would only predict 2% improvement

Exploration vs Exploitation Balance Adopted:
-	Low-D (F1-F3): 70% exploitation, 30% exploration
-	Mid-D (F4-F5): 50-50 balanced
-	High-D (F6-F8): 60% exploration, 40% exploitation

What I Learned:
1. Dimensionality is exponential: 8D is fundamentally different from 2D
2. rust mathematics in high-D: Intuition fails beyond 5D
3. Feature effects validate decisions: Interpretability builds confidence
4. Convergence signals matter: Week 2 performance guides Week 3 strategy
5. Coverage is critical : 0.00004% for F8 means BO is literally the only viable approach

Proposed strategy for Week 3:
-	Take a hybrid model approach and consider how SVM and Ensembles might help me understand the data better.

Week 3 : Hybrid Model approach.

My Objectives:
- Test multiple classifier models (SVM, Decision Trees, Random Forest, Gradient Boosting) 
  before GP optimization
- Implement conditional strategies that adapt based on model reliability (CV scores)
- Balance aggressive exploration (F1, F2, F3, F7) with conservative exploitation 
  (F4, F5, F8) across portfolio
- Validate "explore early, exploit later" philosophy at Week 3/12 timing

Method Used: 
- Sequential Hybrid Approach: Classifier filters candidates → GP optimizes 
  within filtered set
- Model Testing: 	
	- Test 9 models per function with 3-fold cross-validation
	- Threshold: CV ≥60% = reliable, ≥70% = excellent
	- Select best model or fall back to Pure GP if all fail
- Three-Way Comparison: 
	-Pure GP vs Pure Models vs GP+Models to validate 
         recommendations
Key Findings:
- Model Performance Varies by Dimension:
  - F1 (2D): Decision Tree 83.3% CV > Linear SVM 67%
  - F2 (2D): Decision Tree 75% > Linear SVM 67% > RBF SVM 58%
  - F4 (4D): Linear SVM 68.8% (n/p=8.0, best ratio)
  - F7 (6D): All models failed (<60% CV) → Pure GP fallback

- Pattern: Decision Trees excel on low-D, SVMs reliable on mid-D, 
    both struggle on high-D with sparse data

- GP Flatness Limitation Discovered:
  - F1 (12 samples, 2D): GP predicted μ≈-0.0003 everywhere with σ≈0.001
  - μ/σ ratio = 0.3 (noise > signal)
  - GP cannot distinguish between regions with sparse data
  - Risk: False convergence signal (appears optimal when just uncertain)

 
  - Exploration: (4 functions): F1, F2, F3, F7
    - F1: Distance 0.28 (far from W2 rank 1) - testing model hypothesis
    - F2: Distance 0.31 (boundary [1.0, 1.0]) - escape poor performance
    - F3: Return to W1 region (W2 declined) - adaptive optimization
    - F7: X1=0.0 boundary - Pure GP edge testing
  
  - Exploitation: (4 functions): F4, F5, F6, F8
    - F4: Distance 0.08 (tight local refinement of rank 1)
    - F5: Boundary HIGH (X3≈1.0, X4≈1.0) - continue W2 success
    - F6: Conditional strategy (SVM CV 68.5% → use sequential)
    - F8: Boundary LOW (X1≈0.01, X3≈0.002) - minimize strategy

What I Learned:
1. Model Selection is Important:
   - Testing 9 models revealed dramatically different recommendations
   - Decision Trees often outperform SVMs on low-dimensional data
   - No single model dominates—must test and validate

2. Sequential Filtering Changes Outcomes:
   - Pure GP (no filtering) → conservative recommendations
   - Model filtering → introduces different candidate regions
   - GP+high σ in filtered regions → aggressive exploration
   - The approach itself (not just hyperparameters) determines strategy


Proposed strategy for Week 4:
If hybrid models outperformed Pure GP for week 3 I will;
- Expand model testing to include further Kernel tunning, Increase use of Decision Trees 
    - Continue exploring new regions on F1-F3
    - Test other far regions suggested by models
    - If boundary strategies worked on F5, F7, F8 I'll continue on the same path. 
  

Week 4: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 5:

Week 5: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 6:

Week 6: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 7:

Week 7: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 8:

Week 8: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 9:

Week 9: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 10:

Week 10: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 11:

Week 11: TBA 
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:
Proposed strategy for Week 12:

Week 12: TBA
My Objectives:
Method Used: 
Key Findings:
Exploration vs Exploitation:
What I Learned:

MyCodeStructure
Each notebook follows this structure:
1.	Import libraries: Load required packages
2.	Load data:  Import .npy files with inputs/outputs
3.	Exploratory analysis: Testing Models, statistics, best points, coverage
4.	Gaussian Process model:  Fit GP with optimized hyperparameters
5.	Acquisition function: Compute and Compare  EI & UCB
6.	Optimization: Find point that maximizes acquisition
7.	Visualization: Plot GP predictions and acquisition function
8.	Recommendation: Make submission recommendation query point with justification

My Repository Structure: 
Repository Structure Section:

capstone_project/
├── notebooks/
│   ├── Capstone_F1_W3.ipynb          # F1: GP+Models aggressive exploration
│   ├── Capstone_F2_W3.ipynb          # F2: Model testing + boundary
│   ├── Capstone_F3_W3.ipynb          # F3: Week 1 focus + exploration
│   ├── Capstone_F4_W3.ipynb          # F4: Local exploitation
│   ├── Capstone_F5_W3.ipynb          # F5: Sequential SVM→GP boundary HIGH
│   ├── Capstone_F6_W3.ipynb          # F6: Conditional strategy
│   ├── Capstone_F7_W3.ipynb          # F7: Pure GP (SVM failed)
│   └── Capstone_F8_W3.ipynb          # F8: Sequential SVM→GP boundary LOW
│
├── data/
│   ├── f1_w3_inputs.npy              # Input data (12 samples, 2D)
│   ├── f1_w3_outputs.npy             # Output data
│   ├── f2_w3_inputs.npy              # ...
│   └── ...
│
├── outputs/
│   ├── Week3_Submissions.txt         		  # All submission strings
│   ├── Week3_Observations_and_Strategy.md  # Strategy documentation
│   ├── Capstone_F1_W3_acquisition.png      # Acquisition curves
│   ├── Capstone_F1_W3_results.png          # Results dashboard
│   └── ...
│
│
└── README.md                         # This file

End
