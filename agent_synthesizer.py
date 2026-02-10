import ollama
import json

def synthesize_recommendation(plan, simulation_results, sensitivity_ranked):
    """
    Agent #4: The Synthesizer
    Interprets all results and creates a final recommendation.
    """
    
    print("🎤 Agent #4: The Synthesizer")
    print("Generating final recommendation based on all analysis...\n")
    
    # Prepare context for LLM
    context = f"""You are a senior business analyst presenting findings to executives.

BUSINESS DECISION: {plan['decision']}

MONTE CARLO SIMULATION RESULTS (10,000 scenarios):
- Mean monthly profit: ${simulation_results['mean_profit']:,.0f}
- Probability of being profitable: {simulation_results['probability_profitable']:.1f}%
- Best case (95th percentile): ${simulation_results['percentile_95']:,.0f}
- Worst case (5th percentile): ${simulation_results['percentile_5']:,.0f}

SENSITIVITY ANALYSIS (Variables ranked by impact):
1. {sensitivity_ranked[0][0]} - {sensitivity_ranked[0][1]['type']} (variance: {sensitivity_ranked[0][1]['variance']:,.0f})
2. {sensitivity_ranked[1][0]} - {sensitivity_ranked[1][1]['type']} (variance: {sensitivity_ranked[1][1]['variance']:,.0f})
3. {sensitivity_ranked[2][0]} - {sensitivity_ranked[2][1]['type']} (variance: {sensitivity_ranked[2][1]['variance']:,.0f})

KEY ASSUMPTIONS:
{chr(10).join('- ' + a for a in plan['assumptions'])}

Provide a clear, concise executive recommendation with:
1. Clear GO/NO-GO recommendation
2. Key reasoning (2-3 sentences)
3. If NO-GO: what would need to change to make it viable
4. Top priority action item

Keep it professional but concise. No jargon."""

    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'user', 'content': context}
        ]
    )
    
    recommendation = response['message']['content']
    return recommendation


# Test it
if __name__ == "__main__":
    from agent_planner import plan_decision
    from agent_simulator import run_monte_carlo_simulation
    from agent_critic import sensitivity_analysis
    
    print("="*70)
    print("🤖 MULTI-AGENT DECISION INTELLIGENCE SYSTEM")
    print("="*70)
    print()
    
    # Run all agents
    question = "Should we launch a premium coffee subscription service?"
    
    print("📋 Question:", question)
    print()
    
    # Agent 1: Plan
    print("Agent #1: Planning...")
    plan = plan_decision(question)
    print("✅ Plan created\n")
    
    # Agent 2: Simulate
    print("Agent #2: Simulating...")
    results = run_monte_carlo_simulation(plan)
    print("✅ Simulation complete\n")
    
    # Agent 3: Analyze risk
    print("Agent #3: Analyzing risk...")
    sensitivities, ranked = sensitivity_analysis(plan)
    print("✅ Sensitivity analysis complete\n")
    
    # Agent 4: Synthesize
    print("="*70)
    recommendation = synthesize_recommendation(plan, results, ranked)
    print("="*70)
    print()
    print(recommendation)
    print()
    print("="*70)