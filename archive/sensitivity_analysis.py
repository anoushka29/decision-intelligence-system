import numpy as np
import matplotlib.pyplot as plt

print("=== Sensitivity Analysis ===")
print("Question: Which variable affects revenue more?")
print()

# Run simulations
n_simulations = 10000

# Scenario 1: Vary ONLY customers (keep order value fixed at average)
customers_vary = np.random.uniform(50, 150, size=n_simulations)
order_value_fixed = 35  # Fixed at midpoint of 20-50
revenue_customer_impact = customers_vary * order_value_fixed * 30

# Scenario 2: Vary ONLY order value (keep customers fixed at average)
customers_fixed = 100  # Fixed at midpoint of 50-150
order_value_vary = np.random.uniform(20, 50, size=n_simulations)
revenue_order_impact = customers_fixed * order_value_vary * 30

# Calculate variance (spread) for each
customer_variance = np.var(revenue_customer_impact)
order_variance = np.var(revenue_order_impact)

print(f"When ONLY customers vary:")
print(f"  Revenue ranges from ${revenue_customer_impact.min():,.0f} to ${revenue_customer_impact.max():,.0f}")
print(f"  Variance: {customer_variance:,.0f}")
print()

print(f"When ONLY order value varies:")
print(f"  Revenue ranges from ${revenue_order_impact.min():,.0f} to ${revenue_order_impact.max():,.0f}")
print(f"  Variance: {order_variance:,.0f}")
print()

# Which matters more?
if customer_variance > order_variance:
    ratio = customer_variance / order_variance
    print(f"🎯 INSIGHT: Customer count has {ratio:.1f}x more impact than order value!")
    print("   → Focus on getting more customers, not raising prices!")
else:
    ratio = order_variance / customer_variance
    print(f"🎯 INSIGHT: Order value has {ratio:.1f}x more impact than customer count!")
    print("   → Focus on upselling, not customer acquisition!")