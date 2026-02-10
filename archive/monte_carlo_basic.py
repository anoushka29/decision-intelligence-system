import numpy as np
import matplotlib.pyplot as plt

# Step 1: Understanding random sampling
print("=== Learning Random Numbers ===")
print()

# Simulate customers per day (between 50 and 150)
# Let's generate just 5 random samples first to understand
random_customers = np.random.uniform(50, 150, size=5)
print("5 random customer counts:")
print(random_customers)
print()

# Now let's generate 5 random order values (between $20 and $50)
random_orders = np.random.uniform(20, 50, size=5)
print("5 random order values:")
print(random_orders)
print()

# Step 2: Calculate revenue for ONE scenario
print("=== Single Scenario Revenue Calculation ===")
print()

# One random day
customers = np.random.uniform(50, 150)
order_value = np.random.uniform(20, 50)

# Calculate monthly revenue (30 days)
monthly_revenue = customers * order_value * 30

print(f"Customers per day: {customers:.1f}")
print(f"Average order value: ${order_value:.2f}")
print(f"Monthly revenue: ${monthly_revenue:,.2f}")
print()

# Step 3: Monte Carlo Simulation - 10,000 scenarios!
print("=== Monte Carlo Simulation (10,000 scenarios) ===")
print()

# Run 10,000 simulations
n_simulations = 10000

# Generate 10,000 random customer counts
customers_array = np.random.uniform(50, 150, size=n_simulations)

# Generate 10,000 random order values  
order_values_array = np.random.uniform(20, 50, size=n_simulations)

# Calculate revenue for all 10,000 scenarios at once
revenues = customers_array * order_values_array * 30

# Show statistics
print(f"Mean (average) revenue: ${revenues.mean():,.0f}")
print(f"Median revenue: ${np.median(revenues):,.0f}")
print(f"Minimum revenue: ${revenues.min():,.0f}")
print(f"Maximum revenue: ${revenues.max():,.0f}")
print(f"5th percentile (bad scenario): ${np.percentile(revenues, 5):,.0f}")
print(f"95th percentile (good scenario): ${np.percentile(revenues, 95):,.0f}")
print()

# Create visualization
plt.figure(figsize=(10, 6))
plt.hist(revenues, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
plt.xlabel('Monthly Revenue ($)', fontsize=12)
plt.ylabel('Frequency', fontsize=12)
plt.title('Monte Carlo Simulation: 10,000 Possible Revenue Outcomes', fontsize=14, fontweight='bold')
plt.axvline(revenues.mean(), color='red', linestyle='--', linewidth=2, label=f'Mean: ${revenues.mean():,.0f}')
plt.axvline(np.percentile(revenues, 5), color='orange', linestyle='--', linewidth=2, label=f'5th percentile: ${np.percentile(revenues, 5):,.0f}')
plt.axvline(np.percentile(revenues, 95), color='green', linestyle='--', linewidth=2, label=f'95th percentile: ${np.percentile(revenues, 95):,.0f}')
plt.legend()
plt.grid(axis='y', alpha=0.3)
plt.tight_layout()
plt.savefig('monte_carlo_revenue.png', dpi=150)
print("📊 Graph saved as 'monte_carlo_revenue.png'")
plt.show()