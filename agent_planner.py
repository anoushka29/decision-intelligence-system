import ollama
import json
import re

def plan_decision(business_question):
    """
    Agent #1: The Planner
    Takes a vague business question and structures it into simulation variables.
    """
    
    prompt = f"""You are a business analyst. Structure this decision for Monte Carlo simulation.

Business Question: {business_question}

Create a valid JSON with revenue drivers, cost drivers, and assumptions.
Each driver needs: name, min value, max value, and description.

Example format:
{{
  "decision": "description here",
  "revenue_drivers": [
    {{"name": "monthly_subscribers", "min": 100, "max": 500, "description": "number of paying subscribers"}}
  ],
  "cost_drivers": [
    {{"name": "monthly_operations", "min": 3000, "max": 8000, "description": "operational costs per month"}}
  ],
  "assumptions": ["assumption 1", "assumption 2"]
}}

Return ONLY valid JSON."""
    
    response = ollama.chat(
        model='llama3.2',
        messages=[
            {'role': 'user', 'content': prompt}
        ]
    )
    
    # Extract JSON from response
    text = response['message']['content']
    
    # Clean up common issues
    if '```json' in text:
        text = text.split('```json')[1].split('```')[0]
    elif '```' in text:
        text = text.split('```')[1].split('```')[0]
    
    text = text.strip()
    
    # Try to fix common JSON errors
    # Fix missing closing brackets
    if text.count('[') > text.count(']'):
        text = text + ']' * (text.count('[') - text.count(']'))
    if text.count('{') > text.count('}'):
        text = text + '}' * (text.count('{') - text.count('}'))
    
    try:
        result = json.loads(text)
        return result
    except json.JSONDecodeError as e:
        print("❌ JSON parsing failed!")
        print(f"Error: {e}")
        print(f"Raw response:\n{text}\n")
        
        # Return a simple default structure
        print("⚠️  Using default structure instead...")
        return {
            "decision": business_question,
            "revenue_drivers": [
                {"name": "customers_per_day", "min": 50, "max": 150, "description": "daily customers"},
                {"name": "avg_order_value", "min": 20, "max": 50, "description": "average order in dollars"}
            ],
            "cost_drivers": [
                {"name": "fixed_monthly_costs", "min": 5000, "max": 15000, "description": "monthly fixed costs"},
                {"name": "variable_cost_per_unit", "min": 5, "max": 15, "description": "cost per order"}
            ],
            "assumptions": [
                "Market demand remains stable",
                "No major competitors enter market",
                "Operating costs don't spike"
            ]
        }


# Test it
if __name__ == "__main__":
    question = "Should we launch a premium coffee subscription service?"
    
    print("🤖 Agent #1: The Planner")
    print(f"Question: {question}")
    print("\n" + "="*60 + "\n")
    
    plan = plan_decision(question)
    
    print("✅ STRUCTURED PLAN:")
    print(json.dumps(plan, indent=2))