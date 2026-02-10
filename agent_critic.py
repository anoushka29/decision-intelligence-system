import numpy as np
import matplotlib.pyplot as plt
import json

def sensitivity_analysis(plan, n_simulations=10000):
    """
    Agent #3: The Risk/Critic
    Identifies which variables have the biggest impact on outcomes.
    """
    
    print("🔍 Running sensitivity analysis...")
    print("Testing which variables create the most uncertainty...\n")
    
    sensitivities = {}
    
    # Test each revenue driver
    print("📈 REVENUE DRIVERS:")
    for driver in plan['revenue_drivers']:
        # Vary ONLY this driver, keep others at midpoint
        varied = np.random.uniform(driver['min'], driver['max'], size=n_simulations)
        
        # Build revenue with this varied and others fixed
        revenue_components = []
        for d in plan['revenue_drivers']:
            if d['name'] == driver['name']:
                revenue_components.append(varied)
            else:
                midpoint = (d['min'] + d['max']) / 2
                revenue_components.append(np.full(n_simulations, midpoint))
        
        # Calculate revenue
        # Check if we have subscriber and price pattern
        subscriber_vars = [i for i, d in enumerate(plan['revenue_drivers']) 
                          if 'subscriber' in d['name'].lower() or 'customer' in d['name'].lower()]
        price_vars = [i for i, d in enumerate(plan['revenue_drivers']) 
                     if 'price' in d['name'].lower() or 'value' in d['name'].lower() or 'order' in d['name'].lower()]
        
        if subscriber_vars and price_vars:
            revenue = revenue_components[subscriber_vars[0]] * revenue_components[price_vars[0]]
        else:
            revenue = sum(revenue_components)
        
        variance = np.var(revenue)
        sensitivities[driver['name']] = {
            'variance': variance,
            'type': 'revenue',
            'range': (driver['min'], driver['max'])
        }
        
        print(f"  {driver['name']}")
        print(f"    Variance: {variance:,.0f}")
        print(f"    Range: ${driver['min']:,.0f} - ${driver['max']:,.0f}")
        print()
    
    # Test each cost driver
    print("💰 COST DRIVERS:")
    for driver in plan['cost_drivers']:
        # Vary ONLY this driver
        varied = np.random.uniform(driver['min'], driver['max'], size=n_simulations)
        variance = np.var(varied)
        
        sensitivities[driver['name']] = {
            'variance': variance,
            'type': 'cost',
            'range': (driver['min'], driver['max'])
        }
        
        print(f"  {driver['name']}")
        print(f"    Variance: {variance:,.0f}")
        print(f"    Range: ${driver['min']:,.0f} - ${driver['max']:,.0f}")
        print()
    
    # Rank by impact
    ranked = sorted(sensitivities.items(), key=lambda x: x[1]['variance'], reverse=True)
    
    print("="*60)
    print("🎯 RANKED BY IMPACT (Highest to Lowest):")
    print("="*60)
    for i, (name, data) in enumerate(ranked, 1):
        print(f"{i}. {name}")
        print(f"   Type: {data['type']}")
        print(f"   Variance: {data['variance']:,.0f}")
        print()
    
    # Identify the critical variable
    top_var = ranked[0]
    print("="*60)
    print("💡 KEY INSIGHT:")
    print("="*60)
    print(f"'{top_var[0]}' has the BIGGEST impact on outcomes!")
    print(f"Focus here to reduce risk or improve results.")
    print()
    
    return sensitivities, ranked


def visualize_sensitivity(ranked):
    """Visualize sensitivity analysis results"""
    
    names = [item[0] for item in ranked]
    variances = [item[1]['variance'] for item in ranked]
    colors = ['#2ecc71' if item[1]['type'] == 'revenue' else '#e74c3c' for item in ranked]
    
    plt.figure(figsize=(10, 6))
    bars = plt.barh(names, variances, color=colors, alpha=0.7, edgecolor='black')
    
    plt.xlabel('Variance (Impact on Outcome)', fontsize=12)
    plt.ylabel('Variable', fontsize=12)
    plt.title('Sensitivity Analysis: Which Variables Matter Most?', fontsize=14, fontweight='bold')
    plt.grid(axis='x', alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='#2ecc71', alpha=0.7, label='Revenue Driver'),
        Patch(facecolor='#e74c3c', alpha=0.7, label='Cost Driver')
    ]
    plt.legend(handles=legend_elements)
    
    plt.tight_layout()
    plt.savefig('sensitivity_analysis.png', dpi=150)
    print("📊 Sensitivity graph saved as 'sensitivity_analysis.png'")
    plt.show()


# Test it
if __name__ == "__main__":
    from agent_planner import plan_decision
    
    question = "Should we launch a premium coffee subscription service?"
    plan = plan_decision(question)
    
    print("="*60)
    print("🤖 Agent #3: The Risk Critic")
    print("="*60)
    print()
    
    sensitivities, ranked = sensitivity_analysis(plan)
    visualize_sensitivity(ranked)