# Fixed version of F1 acquisition function optimization
# Add this code to make your results reproducible

import numpy as np

# ===================================================================
# ADD THIS AT THE TOP OF YOUR "OPTIMIZE EI" CELL (before line 363)
# ===================================================================
np.random.seed(42)  # Set seed for reproducible random starting points

# Then your existing code continues...
bounds = [(0.0, 1.0), (0.0, 1.6)]
y_best = Y.min()

print("="*70)
print("OPTIMIZING EXPECTED IMPROVEMENT (EI)")
print("="*70)

def neg_ei(x):
    """Negative EI for minimization"""
    return -expected_improvement(x.reshape(1, -1), gp, y_best, xi=0.01)[0]

best_ei = np.inf
x_next_ei = None

# Multiple random restarts - now deterministic!
for i in range(25):
    x0 = np.array([np.random.uniform(b[0], b[1]) for b in bounds])
    result = minimize(neg_ei, x0, bounds=bounds, method='L-BFGS-B')
    
    if result.fun < best_ei:
        best_ei = result.fun
        x_next_ei = result.x

# Predict at EI suggestion
mu_ei, sigma_ei = gp.predict(x_next_ei.reshape(1, -1), return_std=True)

print(f"EI suggests: [{x_next_ei[0]:.6f}, {x_next_ei[1]:.6f}]")
print(f"Predicted value: {mu_ei[0]:.6e} ± {sigma_ei[0]:.6e}")
print(f"Expected Improvement: {-best_ei:.6e}")

# ===================================================================
# ALSO ADD THIS BEFORE YOUR UCB OPTIMIZATION CELL
# ===================================================================
np.random.seed(42)  # Reset seed for UCB optimization

# Then continue with your UCB code...
