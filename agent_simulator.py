import numpy as np
import matplotlib.pyplot as plt
import json

def run_monte_carlo_simulation(plan, n_simulations=10000):
    """
    Agent #2: The Simulator
    Runs Monte Carlo simulation based on the structured plan.
    """
    
    print(f"🎲 Running {n_simulations:,} Monte Carlo simulations...")
    print()
    
    # Extract variables
    revenue_vars = {}
    for driver in plan['revenue_drivers']:
        revenue_vars[driver['name']] = np.random.uniform(
            driver['min'], 
            driver['max'], 
            size=n_simulations
        )
    
    cost_vars = {}
    for driver in plan['cost_drivers']:
        cost_vars[driver['name']] = np.random.uniform(
            driver['min'], 
            driver['max'], 
            size=n_simulations
        )
    
    # Calculate total revenue (sum all revenue drivers)
    total_revenue = np.zeros(n_simulations)
    for name, values in revenue_vars.items():
        total_revenue += values
    
    # If we have subscriber-type and price-type variables, multiply them
    # Look for common patterns
    subscriber_keys = [k for k in revenue_vars.keys() if 'subscriber' in k.lower() or 'customer' in k.lower()]
    price_keys = [k for k in revenue_vars.keys() if 'price' in k.lower() or 'value' in k.lower() or 'order' in k.lower()]
    
    if subscriber_keys and price_keys:
        # Revenue = subscribers * price
        total_revenue = revenue_vars[subscriber_keys[0]] * revenue_vars[price_keys[0]]
    
    # Calculate total costs (sum all cost drivers)
    total_costs = np.zeros(n_simulations)
    for name, values in cost_vars.items():
        total_costs += values
    
    # Profit = Revenue - Costs
    monthly_profit = total_revenue - total_costs
    
    # Calculate statistics
    results = {
        'mean_profit': float(np.mean(monthly_profit)),
        'median_profit': float(np.median(monthly_profit)),
        'std_dev': float(np.std(monthly_profit)),
        'min_profit': float(np.min(monthly_profit)),
        'max_profit': float(np.max(monthly_profit)),
        'percentile_5': float(np.percentile(monthly_profit, 5)),
        'percentile_25': float(np.percentile(monthly_profit, 25)),
        'percentile_75': float(np.percentile(monthly_profit, 75)),
        'percentile_95': float(np.percentile(monthly_profit, 95)),
        'probability_profitable': float(np.sum(monthly_profit > 0) / n_simulations * 100),
        'all_simulations': monthly_profit
    }
    
    return results


def visualize_results(results, plan):
    """Create visualization of simulation results"""
    
    profits = results['all_simulations']
    
    plt.figure(figsize=(12, 6))
    
    # Histogram
    plt.hist(profits, bins=50, edgecolor='black', alpha=0.7, color='steelblue')
    
    # Add vertical lines for key statistics
    plt.axvline(results['mean_profit'], color='red', linestyle='--', linewidth=2, 
                label=f"Mean: ${results['mean_profit']:,.0f}")
    plt.axvline(results['percentile_5'], color='orange', linestyle='--', linewidth=2,
                label=f"5th percentile: ${results['percentile_5']:,.0f}")
    plt.axvline(results['percentile_95'], color='green', linestyle='--', linewidth=2,
                label=f"95th percentile: ${results['percentile_95']:,.0f}")
    plt.axvline(0, color='black', linestyle='-', linewidth=1, alpha=0.5)
    
    plt.xlabel('Monthly Profit ($)', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    plt.title(f'Monte Carlo Simulation: {plan["decision"][:50]}...', fontsize=14, fontweight='bold')
    plt.legend()
    plt.grid(axis='y', alpha=0.3)
    plt.tight_layout()
    
    plt.savefig('simulation_results.png', dpi=150)
    print("📊 Graph saved as 'simulation_results.png'")
    plt.show()


# Test it
if __name__ == "__main__":
    # Load the plan from Agent #1
    from agent_planner import plan_decision
    
    question = "Should we launch a premium coffee subscription service?"
    plan = plan_decision(question)
    
    print("="*60)
    print("🤖 Agent #2: The Simulator")
    print("="*60)
    print()
    
    # Run simulation
    results = run_monte_carlo_simulation(plan)
    
    # Print results
    print("\n📊 SIMULATION RESULTS:")
    print(f"  Mean monthly profit: ${results['mean_profit']:,.0f}")
    print(f"  Median monthly profit: ${results['median_profit']:,.0f}")
    print(f"  Standard deviation: ${results['std_dev']:,.0f}")
    print()
    print(f"  Best case (95th percentile): ${results['percentile_95']:,.0f}")
    print(f"  Worst case (5th percentile): ${results['percentile_5']:,.0f}")
    print()
    print(f"  Probability of being profitable: {results['probability_profitable']:.1f}%")
    print()
    
    # Visualize
    visualize_results(results, plan)