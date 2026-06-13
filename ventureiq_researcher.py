from ddgs import DDGS
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

def search_single(query, max_results=2):
    """Run a single search query"""
    try:
        with DDGS() as ddgs:
            results = list(ddgs.text(query, max_results=max_results))
            return query, [
                r.get('body', '')[:300]
                for r in results if r.get('body')
            ]
    except Exception:
        return query, []


def research_startup_comprehensively(startup_idea, plan):
    """
    Deep Research Agent - FAST parallel version
    Researches 6 critical dimensions simultaneously
    """
    
    print("🔎 Running parallel market research...")
    
    industry = plan.get('industry', 'business')
    location = extract_location(startup_idea)
    target   = plan.get('target_market', 'general consumers')
    
    # ── 6 FOCUSED DIMENSIONS (reduced from 10) ────────────────────
    # Each has ONE focused query instead of 3
    research_queries = {
        "geographic_viability": 
            f"is {industry} business viable in {location} geography climate",
        
        "market_size_demand":   
            f"{industry} market size demand {location} 2024 statistics",
        
        "competition_landscape":
            f"{industry} competition market saturation {location}",
        
        "startup_costs":        
            f"cost to start {industry} business monthly expenses 2024",
        
        "failure_reasons":      
            f"why {industry} startups fail common challenges",
        
        "target_demographic":   
            f"{target} spending habits demographics {location}",
    }
    
    # ── RUN ALL SEARCHES IN PARALLEL ──────────────────────────────
    print(f"   Running {len(research_queries)} searches simultaneously...")
    
    all_research = {}
    
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Submit all searches at once
        future_to_dim = {
            executor.submit(search_single, query): dim
            for dim, query in research_queries.items()
        }
        
        # Collect results as they complete
        for future in as_completed(future_to_dim):
            dim = future_to_dim[future]
            try:
                query, findings = future.result(timeout=10)
                all_research[dim] = [
                    {'query': query, 'finding': f}
                    for f in findings
                ]
            except Exception:
                all_research[dim] = []
    
    print("   ✅ Research complete!")
    
    # Format results
    formatted = format_research(all_research, startup_idea, location, industry)
    return formatted, all_research


def extract_location(startup_idea):
    """Extract location from startup idea"""
    locations = [
        'phoenix', 'scottsdale', 'tempe', 'mesa',
        'new york', 'los angeles', 'chicago', 'houston',
        'miami', 'seattle', 'boston', 'denver', 'dallas',
        'san francisco', 'austin', 'nashville', 'atlanta',
        'arizona', 'california', 'texas', 'florida',
        'nevada', 'colorado', 'india', 'mumbai', 'delhi',
        'bangalore', 'uk', 'london', 'canada', 'toronto',
        'australia', 'dubai', 'singapore'
    ]
    
    idea_lower = startup_idea.lower()
    found = [loc.title() for loc in locations if loc in idea_lower]
    return ', '.join(found) if found else "the specified location"


def format_research(all_research, startup_idea, location, industry):
    """Format research into structured context"""
    
    labels = {
        "geographic_viability": ("📍", "Geographic Viability"),
        "market_size_demand":   ("📊", "Market Size & Demand"),
        "competition_landscape":("⚔️",  "Competition Landscape"),
        "startup_costs":        ("💰", "Startup Cost Benchmarks"),
        "failure_reasons":      ("⚠️",  "Common Failure Reasons"),
        "target_demographic":   ("👥", "Target Demographic"),
    }
    
    formatted = f"""
COMPREHENSIVE MARKET RESEARCH
Startup: {startup_idea}
Location: {location}
Industry: {industry}
{'='*50}
"""
    
    for dim, findings in all_research.items():
        icon, label = labels.get(dim, ("📌", dim))
        formatted += f"\n{icon} {label.upper()}\n{'-'*40}\n"
        
        if findings:
            for item in findings[:2]:
                formatted += f"• {item['finding'][:250]}\n\n"
        else:
            formatted += "• No data found.\n\n"
    
    return formatted


if __name__ == "__main__":
    plan = {
        'industry': 'Luxury Yacht Rental',
        'target_market': 'Affluent individuals in Phoenix',
        'decision': 'Luxury yacht rental service in Phoenix Arizona'
    }
    
    idea = "A luxury yacht rental service in Phoenix Arizona"
    
    start = time.time()
    formatted, raw = research_startup_comprehensively(idea, plan)
    elapsed = time.time() - start
    
    print(f"\n⏱️  Completed in {elapsed:.1f} seconds")
    print(formatted[:2000])