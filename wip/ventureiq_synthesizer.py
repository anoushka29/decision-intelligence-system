import ollama

def synthesize_venture_recommendation(
    plan, simulation_results, sensitivity_ranked,
    market_research="", raw_research=None
):
    """
    VentureIQ Synthesizer - Deep Analysis Version
    Uses comprehensive research + simulation for accurate verdicts
    """
    
    mean_profit  = simulation_results['mean_profit']
    prob_profit  = simulation_results['probability_profitable']
    worst_case   = simulation_results['percentile_5']
    best_case    = simulation_results['percentile_95']
    std_dev      = simulation_results['std_dev']
    
    # Auto-determine verdict signal based on hard rules
    if prob_profit == 0:
        verdict_signal = "VERDICT MUST BE NO-GO. Zero probability of profit across 10,000 scenarios."
    elif prob_profit < 15:
        verdict_signal = "VERDICT SHOULD BE NO-GO. Extremely low probability of profit."
    elif prob_profit < 40:
        verdict_signal = "VERDICT SHOULD BE CONDITIONAL GO. Significant risks present."
    elif prob_profit < 65:
        verdict_signal = "VERDICT COULD BE CONDITIONAL GO. Moderate risk."
    else:
        verdict_signal = "VERDICT COULD BE GO. Strong probability of profit."
    
    prompt = f"""You are a senior venture capitalist and business strategy expert.
You have DEEP knowledge of markets, geography, economics, and startup dynamics.
You have just received comprehensive market research AND simulation data.
Your job: Give the MOST ACCURATE, SPECIFIC, BRUTALLY HONEST verdict possible.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
STARTUP OVERVIEW
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Idea: {plan['decision']}
Industry: {plan.get('industry', 'General')}
Target Market: {plan.get('target_market', 'General')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
SIMULATION RESULTS (10,000 Monte Carlo Scenarios)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Average Monthly Profit: USD {mean_profit:,.0f}
Probability of Profit: {prob_profit:.1f}%
Best Case (95th percentile): USD {best_case:,.0f}/month
Worst Case (5th percentile): USD {worst_case:,.0f}/month
Volatility (Std Dev): USD {std_dev:,.0f}
{verdict_signal}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
TOP RISK FACTORS BY IMPACT
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. {sensitivity_ranked[0][0]} - {sensitivity_ranked[0][1]['type']} driver (variance: {sensitivity_ranked[0][1]['variance']:,.0f})
2. {sensitivity_ranked[1][0]} - {sensitivity_ranked[1][1]['type']} driver (variance: {sensitivity_ranked[1][1]['variance']:,.0f})
3. {sensitivity_ranked[2][0]} - {sensitivity_ranked[2][1]['type']} driver (variance: {sensitivity_ranked[2][1]['variance']:,.0f})

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
COMPREHENSIVE MARKET RESEARCH
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{market_research}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
KEY ASSUMPTIONS IN MODEL
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
{chr(10).join('- ' + a for a in plan['assumptions'])}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
CRITICAL RULES FOR YOUR ANALYSIS:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. If probability of profit is 0%, verdict is NO-GO. Period.
2. Consider geographic reality FIRST. Is this location physically/logically viable?
3. Use specific facts from the research - not generic advice
4. If the idea is fundamentally impossible (wrong location, no market), say so immediately
5. Reference actual data points from the research in your analysis
6. Be specific about THIS location - mention actual facts
7. Consider ALL 10 research dimensions in your analysis
8. Give realistic cost estimates based on research findings
9. Be harsh but constructive
10. NO GENERIC ADVICE. Everything must be specific to this exact idea.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
FORMAT YOUR RESPONSE EXACTLY:
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

**VERDICT:** [NO-GO 🔴 / CONDITIONAL GO 🟡 / GO 🟢]

**THE REALITY CHECK:**
[3-4 sentences. Be brutally specific. Reference actual facts from research.
Mention the specific location, its actual characteristics, and why they matter.
If Phoenix is a desert - say it. If there's no market - say it. Be direct.]

**GEOGRAPHIC & MARKET ANALYSIS:**
[2-3 sentences specifically about location viability and market conditions.
Use actual statistics or facts from research. This should be the most
location-specific section of your analysis.]

**CRITICAL FAILURE POINTS:**
- **[Factor 1]:** [Specific reason with data reference why this kills the business]
- **[Factor 2]:** [Specific reason with data reference why this is a major risk]  
- **[Factor 3]:** [Specific reason with data reference why this matters]
- **[Factor 4]:** [Regulatory, legal, or operational challenge specific to this]

**FINANCIAL REALITY:**
[Compare the simulation numbers against industry benchmarks from research.
What do real businesses in this industry actually make? How does that compare?]

**IF NO-GO - PIVOT SUGGESTIONS:**
[2 alternative ideas that ARE viable given the location and market conditions]

**IF CONDITIONAL GO - ACTION PLAN:**
[3 very specific actions with measurable targets]

**BOTTOM LINE:**
[One sentence. Brutal. Specific. Memorable. No corporate speak.]"""

    response = ollama.chat(
        model='llama3.2',
        messages=[{'role': 'user', 'content': prompt}]
    )
    
    return response['message']['content']


if __name__ == "__main__":
    from ventureiq_planner import plan_startup
    from agent_simulator import run_monte_carlo_simulation
    from agent_critic import sensitivity_analysis
    from ventureiq_researcher import research_startup_comprehensively
    
    idea = "A luxury yacht rental service in Phoenix Arizona"
    
    print("="*60)
    print("🚀 VentureIQ Deep Analysis Test")
    print("="*60)
    
    print("\n📋 Step 1: Planning...")
    plan = plan_startup(idea)
    
    print("\n🎲 Step 2: Simulating 10,000 scenarios...")
    results = run_monte_carlo_simulation(plan)
    
    print("\n🔍 Step 3: Sensitivity analysis...")
    sensitivities, ranked = sensitivity_analysis(plan)
    
    print("\n🌐 Step 4: Deep market research...")
    research_formatted, research_raw = research_startup_comprehensively(idea, plan)
    
    print("\n✅ Research complete! Sample:")
    print(research_formatted[:1000])
    
    print("\n" + "="*60)
    print("🎤 GENERATING DEEP ANALYSIS RECOMMENDATION...")
    print("="*60 + "\n")
    
    recommendation = synthesize_venture_recommendation(
        plan, results, ranked,
        research_formatted, research_raw
    )
    
    print(recommendation)