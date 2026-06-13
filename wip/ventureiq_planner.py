import ollama
import json

def plan_startup(startup_idea):
    """
    VentureIQ Planner Agent (Ollama version)
    Structures a startup idea into simulatable variables
    """
    
    prompt = f"""You are a startup analyst and venture capitalist.

A founder has this startup idea: {startup_idea}

Return ONLY this exact JSON structure with realistic numbers:
{{
  "startup_name": "catchy name for this startup",
  "decision": "one line description",
  "revenue_drivers": [
    {{"name": "monthly_customers", "min": 10, "max": 200, "description": "paying customers per month"}},
    {{"name": "revenue_per_customer", "min": 50, "max": 200, "description": "monthly revenue per customer in dollars"}}
  ],
  "cost_drivers": [
    {{"name": "monthly_fixed_costs", "min": 2000, "max": 8000, "description": "rent utilities tools per month"}},
    {{"name": "customer_acquisition_cost", "min": 20, "max": 100, "description": "cost to acquire one customer"}}
  ],
  "assumptions": [
    "assumption 1",
    "assumption 2",
    "assumption 3"
  ],
  "industry": "industry name",
  "target_market": "who the customers are"
}}

Return ONLY valid JSON, nothing else."""

    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )
    
    text = response['message']['content']
    
    # Clean up response
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0]
    elif '```' in text:
        text = text.split('```')[1].split('```')[0]
    
    text = text.strip()
    
    # Fix common JSON errors
    if text.count('[') > text.count(']'):
        text = text + ']' * (text.count('[') - text.count(']'))
    if text.count('{') > text.count('}'):
        text = text + '}' * (text.count('{') - text.count('}'))
    
    try:
        result = json.loads(text)
        return result
    except json.JSONDecodeError:
        print("⚠️ Using default structure...")
        return {
            "startup_name": "Your Startup",
            "decision": startup_idea,
            "revenue_drivers": [
                {"name": "monthly_customers", "min": 10, "max": 200, "description": "paying customers per month"},
                {"name": "revenue_per_customer", "min": 50, "max": 200, "description": "monthly revenue per customer"}
            ],
            "cost_drivers": [
                {"name": "monthly_fixed_costs", "min": 2000, "max": 8000, "description": "fixed costs per month"},
                {"name": "customer_acquisition_cost", "min": 20, "max": 100, "description": "cost per customer acquired"}
            ],
            "assumptions": [
                "Market demand is stable",
                "No major competitors enter market",
                "Team executes effectively"
            ],
            "industry": "General",
            "target_market": "General consumers"
        }


if __name__ == "__main__":
    idea = "A tutoring app for college students in Phoenix"
    print("🚀 VentureIQ Planner Agent")
    print(f"Idea: {idea}\n")
    
    plan = plan_startup(idea)
    print(json.dumps(plan, indent=2))