import streamlit as st
import plotly.graph_objects as go
from ventureiq_planner import plan_startup
from agent_simulator import run_monte_carlo_simulation
from agent_critic import sensitivity_analysis
from ventureiq_synthesizer import synthesize_venture_recommendation
from ventureiq_researcher import research_startup_comprehensively

# ── PAGE CONFIG ───────────────────────────────────────────────────
st.set_page_config(
    page_title="VentureIQ - Startup Viability Analyzer",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ── STYLES ────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=DM+Mono:wght@300;400;500&display=swap');

* { font-family: 'DM Mono', monospace; }

.stApp {
    background: #0a0a0a;
    color: #e8e8e8;
}

.block-container {
    padding: 2rem 3rem !important;
    max-width: 1200px !important;
}

/* Hero */
.hero {
    text-align: center;
    padding: 3rem 2rem 1rem;
}

.hero-badge {
    display: inline-block;
    background: #0a0a0a;
    border: 1px solid #00ff88;
    color: #00ff88;
    font-size: 0.72rem;
    letter-spacing: 0.2em;
    padding: 6px 18px;
    border-radius: 20px;
    margin-bottom: 1.5rem;
}

.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: 5rem;
    font-weight: 800;
    line-height: 1;
    margin: 0;
    background: linear-gradient(135deg, #ffffff 0%, #00ff88 50%, #00d4ff 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-subtitle {
    font-size: 1.05rem;
    color: #888;
    margin: 1rem 0 0.4rem;
    letter-spacing: 0.05em;
}

.hero-desc {
    font-size: 0.88rem;
    color: #444;
    margin-bottom: 2.5rem;
}

/* Stats Bar */
.stats-bar {
    display: flex;
    justify-content: center;
    gap: 3rem;
    padding: 1.5rem 0;
    border-top: 1px solid #1a1a1a;
    border-bottom: 1px solid #1a1a1a;
    margin-bottom: 2.5rem;
}

.stat-item { text-align: center; }

.stat-number {
    font-family: 'Syne', sans-serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #00ff88;
}

.stat-label {
    font-size: 0.68rem;
    color: #444;
    letter-spacing: 0.18em;
    text-transform: uppercase;
}

/* Example label */
.examples-label {
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #444;
    margin-bottom: 0.8rem;
}

/* Inputs */
.stTextArea textarea {
    background: #111 !important;
    border: 1px solid #222 !important;
    border-radius: 8px !important;
    color: #e8e8e8 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.95rem !important;
    padding: 1rem !important;
}

.stTextArea textarea:focus {
    border-color: #00ff88 !important;
    box-shadow: 0 0 0 1px #00ff88 !important;
}

/* Buttons */
.stButton button {
    background: #111 !important;
    border: 1px solid #2a2a2a !important;
    color: #888 !important;
    border-radius: 6px !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.78rem !important;
    transition: all 0.2s !important;
    width: 100% !important;
}

.stButton button:hover {
    border-color: #00ff88 !important;
    color: #00ff88 !important;
    background: #0a1a0f !important;
}

div[data-testid="stButton"] button[kind="primary"] {
    background: #00ff88 !important;
    border: none !important;
    color: #0a0a0a !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 0.75rem !important;
    border-radius: 8px !important;
    letter-spacing: 0.04em !important;
}

div[data-testid="stButton"] button[kind="primary"]:hover {
    background: #00d4ff !important;
}

/* Metric Cards */
.metric-box {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 12px;
    padding: 1.4rem;
    text-align: center;
    height: 100%;
    transition: border-color 0.2s;
}

.metric-box:hover { border-color: #333; }

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.9rem;
    font-weight: 700;
    color: #00ff88;
    line-height: 1.1;
}

.metric-value.negative { color: #ff4d6d; }
.metric-value.warning  { color: #ffd700; }

.metric-label {
    font-size: 0.65rem;
    color: #444;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.metric-delta {
    font-size: 0.72rem;
    margin-top: 0.3rem;
}

.delta-good  { color: #00ff88; }
.delta-bad   { color: #ff4d6d; }
.delta-warn  { color: #ffd700; }

/* Section Headers */
.section-header {
    font-family: 'Syne', sans-serif;
    font-size: 1.3rem;
    font-weight: 700;
    color: #fff;
    margin: 2rem 0 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1a1a1a;
}

/* Verdict Boxes */
.verdict-go {
    background: linear-gradient(135deg, #071a0f, #0a2a14);
    border: 1px solid #00ff88;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
}

.verdict-nogo {
    background: linear-gradient(135deg, #1a0707, #2a0a0a);
    border: 1px solid #ff4d6d;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
}

.verdict-conditional {
    background: linear-gradient(135deg, #1a1407, #2a1e0a);
    border: 1px solid #ffd700;
    border-radius: 12px;
    padding: 2rem;
    margin: 1rem 0;
}

/* Research Box */
.research-box {
    background: #0d0d0d;
    border: 1px solid #1a1a1a;
    border-radius: 8px;
    padding: 1.2rem;
    margin: 0.5rem 0;
    font-size: 0.8rem;
    color: #666;
    line-height: 1.6;
}

.research-dimension {
    color: #00ff88;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.3rem;
}

/* Startup Badge */
.startup-badge {
    display: inline-block;
    background: #0a1a0f;
    border: 1px solid #00ff88;
    color: #00ff88;
    font-size: 0.85rem;
    padding: 8px 20px;
    border-radius: 20px;
    margin: 0.5rem 0;
}

.tag-pill {
    display: inline-block;
    background: #111;
    border: 1px solid #222;
    color: #555;
    font-size: 0.68rem;
    padding: 3px 10px;
    border-radius: 20px;
    margin: 2px;
}

/* Pipeline Steps */
.pipeline-step {
    background: #111;
    border: 1px solid #1e1e1e;
    border-radius: 8px;
    padding: 1rem 1.2rem;
    margin: 0.4rem 0;
    font-size: 0.82rem;
    color: #666;
    display: flex;
    align-items: center;
    gap: 0.8rem;
}

.pipeline-step.active {
    border-color: #00ff88;
    color: #00ff88;
    background: #071a0f;
}

.pipeline-step.done {
    border-color: #1e3a2a;
    color: #2a5a3a;
}

/* Progress */
.stProgress > div > div > div {
    background: linear-gradient(90deg, #00ff88, #00d4ff) !important;
}

/* Divider */
hr { border-color: #1a1a1a !important; }

/* Expander */
.streamlit-expanderHeader {
    background: #111 !important;
    border: 1px solid #1e1e1e !important;
    border-radius: 8px !important;
    color: #666 !important;
    font-size: 0.82rem !important;
}

/* Alert */
.stAlert {
    background: #111 !important;
    border: 1px solid #2a2a00 !important;
    border-radius: 8px !important;
}

/* Footer */
.footer {
    text-align: center;
    padding: 3rem 0 1rem;
    color: #2a2a2a;
    font-size: 0.72rem;
    letter-spacing: 0.1em;
}

.footer a { color: #00ff88; text-decoration: none; }
.footer a:hover { color: #00d4ff; }

/* Scrollbar */
::-webkit-scrollbar { width: 4px; }
::-webkit-scrollbar-track { background: #0a0a0a; }
::-webkit-scrollbar-thumb { background: #222; border-radius: 4px; }
</style>
""", unsafe_allow_html=True)


# ── HERO SECTION ──────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-badge">⚡ POWERED BY MONTE CARLO + MULTI-AGENT AI + LIVE RESEARCH</div>
    <h1 class="hero-title">VentureIQ</h1>
    <p class="hero-subtitle">AI-Powered Startup Viability Analyzer</p>
    <p class="hero-desc">Know if your startup idea will survive — before spending a single dollar.</p>
</div>
""", unsafe_allow_html=True)

# Stats Bar
st.markdown("""
<div class="stats-bar">
    <div class="stat-item">
        <div class="stat-number">10K</div>
        <div class="stat-label">Scenarios Simulated</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">4</div>
        <div class="stat-label">AI Agents</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">10</div>
        <div class="stat-label">Research Dimensions</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">30+</div>
        <div class="stat-label">Data Points</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">100%</div>
        <div class="stat-label">Data Driven</div>
    </div>
</div>
""", unsafe_allow_html=True)


# ── EXAMPLE BUTTONS ───────────────────────────────────────────────
st.markdown('<p class="examples-label">→ Try a quick example</p>', unsafe_allow_html=True)

col1, col2, col3, col4 = st.columns(4)
example_idea = ""

with col1:
    if st.button("☕  Coffee Shop\nPhoenix, AZ"):
        example_idea = "A specialty coffee shop in Phoenix Arizona targeting young professionals"
with col2:
    if st.button("📱  Tutoring App\nCollege Students"):
        example_idea = "A tutoring app for college students in Phoenix Arizona"
with col3:
    if st.button("🛍️  Online Boutique\nGen Z Fashion"):
        example_idea = "An online clothing boutique targeting Gen Z women aged 18-25 in the US"
with col4:
    if st.button("🍱  Healthy Meals\nDelivery Service"):
        example_idea = "A healthy meal delivery startup targeting gym-goers in Phoenix Arizona"


# ── INPUT ─────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)

startup_idea = st.text_area(
    "📝  Describe your startup idea:",
    value=example_idea,
    height=110,
    placeholder="e.g., A mobile app connecting freelance designers with small businesses in Chicago, targeting companies with under 50 employees..."
)

st.caption("💡 Be specific — include location, target market, and what problem you're solving for best results.")

analyze_clicked = st.button(
    "⚡  Analyze My Startup",
    type="primary",
    use_container_width=True
)


# ── ANALYSIS PIPELINE ─────────────────────────────────────────────
if analyze_clicked:
    if not startup_idea.strip():
        st.warning("⚠️  Please describe your startup idea above.")
    else:
        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        # Pipeline display
        st.markdown('<div class="section-header">⚙️ Analysis Pipeline</div>', unsafe_allow_html=True)

        pipeline_placeholder = st.empty()

        def show_pipeline(step):
            steps = [
                ("🤖", "Agent #1 — Planner",      "Structuring startup into financial variables"),
                ("🎲", "Agent #2 — Simulator",    "Running 10,000 Monte Carlo scenarios"),
                ("🔍", "Agent #3 — Risk Critic",  "Sensitivity analysis across all variables"),
                ("🌐", "Research Agent",           "Deep market research across 10 dimensions"),
                ("🎤", "Agent #4 — Synthesizer",  "Generating data-driven VC recommendation"),
            ]
            html = ""
            for i, (icon, name, desc) in enumerate(steps):
                if i < step:
                    css = "pipeline-step done"
                    status = "✓"
                elif i == step:
                    css = "pipeline-step active"
                    status = "▶"
                else:
                    css = "pipeline-step"
                    status = "○"
                html += f"""
                <div class="{css}">
                    <span>{status}</span>
                    <span>{icon} <strong>{name}</strong> — {desc}</span>
                </div>"""
            pipeline_placeholder.markdown(html, unsafe_allow_html=True)

        progress = st.progress(0)

        # ── AGENT 1: PLAN ──────────────────────────────────────────
        show_pipeline(0)
        progress.progress(8)
        plan = plan_startup(startup_idea)
        progress.progress(20)

        # ── AGENT 2: SIMULATE ──────────────────────────────────────
        show_pipeline(1)
        results = run_monte_carlo_simulation(plan)
        progress.progress(38)

        # ── AGENT 3: RISK ──────────────────────────────────────────
        show_pipeline(2)
        sensitivities, ranked = sensitivity_analysis(plan)
        progress.progress(52)

        # ── RESEARCH AGENT ─────────────────────────────────────────
        show_pipeline(3)
        research_formatted, research_raw = research_startup_comprehensively(
            startup_idea, plan
        )
        progress.progress(78)

        # ── AGENT 4: SYNTHESIZE ────────────────────────────────────
        show_pipeline(4)
        recommendation = synthesize_venture_recommendation(
            plan, results, ranked,
            research_formatted, research_raw
        )
        progress.progress(100)
        show_pipeline(5)  # All done

        progress.empty()

        st.divider()

        # ── STARTUP IDENTITY ───────────────────────────────────────
        startup_name = plan.get('startup_name', 'Your Startup')
        industry     = plan.get('industry', '')
        target       = plan.get('target_market', '')

        st.markdown(f"""
        <div style='text-align:center; margin: 1.5rem 0 2rem'>
            <div class="startup-badge">🚀 {startup_name}</div><br>
            <span class="tag-pill">📊 {industry}</span>
            <span class="tag-pill">👥 {target}</span>
        </div>
        """, unsafe_allow_html=True)


        # ── KEY METRICS ────────────────────────────────────────────
        st.markdown('<div class="section-header">📊 Simulation Results</div>', unsafe_allow_html=True)

        mean_profit = results['mean_profit']
        prob        = results['probability_profitable']
        best        = results['percentile_95']
        worst       = results['percentile_5']
        std_dev     = results['std_dev']
        median      = results['median_profit']

        col1, col2, col3, col4, col5, col6 = st.columns(6)

        def metric_card(value_str, label, delta_str="", delta_type=""):
            val_class = "metric-value"
            if "-" in value_str and "$" in value_str:
                val_class = "metric-value negative"
            elif "0.0%" in value_str:
                val_class = "metric-value negative"

            delta_html = ""
            if delta_str:
                delta_class = f"metric-delta delta-{delta_type}"
                delta_html = f'<div class="{delta_class}">{delta_str}</div>'

            return f"""
            <div class="metric-box">
                <div class="{val_class}">{value_str}</div>
                <div class="metric-label">{label}</div>
                {delta_html}
            </div>"""

        with col1:
            d_type = "good" if mean_profit > 0 else "bad"
            d_str  = "profitable" if mean_profit > 0 else "loss-making"
            st.markdown(metric_card(f"${mean_profit:,.0f}", "Avg Monthly Profit", d_str, d_type), unsafe_allow_html=True)

        with col2:
            d_type = "good" if prob >= 50 else ("warn" if prob >= 20 else "bad")
            d_str  = "strong" if prob >= 50 else ("borderline" if prob >= 20 else "very risky")
            st.markdown(metric_card(f"{prob:.1f}%", "Probability of Profit", d_str, d_type), unsafe_allow_html=True)

        with col3:
            st.markdown(metric_card(f"${median:,.0f}", "Median Profit", "50th percentile", "warn"), unsafe_allow_html=True)

        with col4:
            st.markdown(metric_card(f"${best:,.0f}", "Best Case", "95th percentile", "good"), unsafe_allow_html=True)

        with col5:
            st.markdown(metric_card(f"${worst:,.0f}", "Worst Case", "5th percentile", "bad"), unsafe_allow_html=True)

        with col6:
            st.markdown(metric_card(f"${std_dev:,.0f}", "Volatility", "std deviation", "warn"), unsafe_allow_html=True)


        # ── CHARTS ─────────────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        col_left, col_right = st.columns([3, 2])

        with col_left:
            st.markdown('<div class="section-header">📈 Profit Distribution</div>', unsafe_allow_html=True)

            profits = results['all_simulations']

            fig = go.Figure()

            # Shade profitable area
            profitable = profits[profits > 0]
            losing     = profits[profits <= 0]

            if len(losing) > 0:
                fig.add_trace(go.Histogram(
                    x=losing, nbinsx=40,
                    marker=dict(color='#ff4d6d', opacity=0.5),
                    name='Loss scenarios'
                ))
            if len(profitable) > 0:
                fig.add_trace(go.Histogram(
                    x=profitable, nbinsx=40,
                    marker=dict(color='#00ff88', opacity=0.5),
                    name='Profit scenarios'
                ))

            fig.add_vline(x=mean_profit, line_dash="dash", line_color="#ff4d6d",
                         line_width=2,
                         annotation_text=f"Mean ${mean_profit:,.0f}",
                         annotation_font_color="#ff4d6d",
                         annotation_font_size=11)
            fig.add_vline(x=best, line_dash="dot", line_color="#00d4ff",
                         line_width=1.5,
                         annotation_text=f"95th ${best:,.0f}",
                         annotation_font_color="#00d4ff",
                         annotation_font_size=10)
            fig.add_vline(x=worst, line_dash="dot", line_color="#ffd700",
                         line_width=1.5,
                         annotation_text=f"5th ${worst:,.0f}",
                         annotation_font_color="#ffd700",
                         annotation_font_size=10)
            fig.add_vline(x=0, line_color="#ffffff", line_width=1.5, opacity=0.15)

            fig.update_layout(
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#0d0d0d',
                font=dict(color='#555', family='DM Mono'),
                xaxis=dict(
                    title='Monthly Profit (USD)',
                    gridcolor='#151515',
                    color='#444',
                    title_font_color='#444'
                ),
                yaxis=dict(
                    title='Number of Scenarios',
                    gridcolor='#151515',
                    color='#444',
                    title_font_color='#444'
                ),
                legend=dict(
                    font=dict(color='#666', size=11),
                    bgcolor='rgba(0,0,0,0)'
                ),
                barmode='overlay',
                height=380,
                margin=dict(l=10, r=10, t=20, b=10)
            )
            st.plotly_chart(fig, width='stretch')

        with col_right:
            st.markdown('<div class="section-header">🎯 Risk Factors</div>', unsafe_allow_html=True)

            names      = [item[0].replace('_', ' ').title() for item in ranked]
            variances  = [item[1]['variance'] for item in ranked]
            colors     = ['#00ff88' if item[1]['type'] == 'revenue' else '#ff4d6d' for item in ranked]
            types      = [item[1]['type'] for item in ranked]

            fig2 = go.Figure(go.Bar(
                x=variances,
                y=names,
                orientation='h',
                marker=dict(color=colors, opacity=0.75),
                text=[t.upper() for t in types],
                textposition='inside',
                textfont=dict(color='#0a0a0a', size=9)
            ))

            fig2.update_layout(
                paper_bgcolor='#0a0a0a',
                plot_bgcolor='#0d0d0d',
                font=dict(color='#555', family='DM Mono'),
                xaxis=dict(
                    title='Impact on Outcome',
                    gridcolor='#151515',
                    color='#444',
                    title_font_color='#444'
                ),
                yaxis=dict(color='#aaa'),
                height=380,
                margin=dict(l=10, r=10, t=20, b=10),
                showlegend=False
            )
            st.plotly_chart(fig2, use_container_width=True)

        st.markdown("""
        <div style='text-align:right; margin-top:-0.5rem; margin-bottom:1rem'>
            <span style='color:#00ff88; font-size:0.72rem'>■ Revenue Driver</span>
            &nbsp;&nbsp;
            <span style='color:#ff4d6d; font-size:0.72rem'>■ Cost Driver</span>
        </div>
        """, unsafe_allow_html=True)


        # ── RESEARCH SUMMARY ───────────────────────────────────────
        st.markdown('<div class="section-header">🌐 Market Research Summary</div>', unsafe_allow_html=True)

        dimension_labels = {
            "geographic_viability":     ("📍", "Geographic Viability"),
            "market_size_demand":       ("📊", "Market Size & Demand"),
            "competition_landscape":    ("⚔️",  "Competition Landscape"),
            "startup_costs_benchmarks": ("💰", "Startup Cost Benchmarks"),
            "revenue_benchmarks":       ("📈", "Revenue Benchmarks"),
            "failure_reasons":          ("⚠️",  "Common Failure Reasons"),
            "regulatory_legal":         ("⚖️",  "Regulatory & Legal"),
            "target_demographic":       ("👥", "Target Demographic"),
            "economic_conditions":      ("🏙️",  "Local Economic Conditions"),
            "seasonal_factors":         ("🌤️",  "Seasonal Factors"),
        }

        if research_raw:
            cols = st.columns(2)
            items = list(research_raw.items())
            for i, (dim, findings) in enumerate(items):
                col = cols[i % 2]
                icon, label = dimension_labels.get(dim, ("📌", dim.replace("_", " ").title()))
                with col:
                    if findings:
                        snippet = findings[0]['finding'][:220] if findings else "No data found."
                        st.markdown(f"""
                        <div class="research-box">
                            <div class="research-dimension">{icon} {label}</div>
                            {snippet}...
                        </div>""", unsafe_allow_html=True)
                    else:
                        st.markdown(f"""
                        <div class="research-box">
                            <div class="research-dimension">{icon} {label}</div>
                            No specific data found for this dimension.
                        </div>""", unsafe_allow_html=True)

        with st.expander("📋  View Full Research Report"):
            st.text(research_formatted)


        # ── STRUCTURED VARIABLES ───────────────────────────────────
        with st.expander("🔬  View Structured Financial Variables"):
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**📈 Revenue Drivers**")
                for d in plan['revenue_drivers']:
                    st.markdown(f"- `{d['name']}` → ${d['min']:,} – ${d['max']:,}/month")
                    st.caption(f"  {d.get('description', '')}")
            with col2:
                st.markdown("**💸 Cost Drivers**")
                for d in plan['cost_drivers']:
                    st.markdown(f"- `{d['name']}` → ${d['min']:,} – ${d['max']:,}/month")
                    st.caption(f"  {d.get('description', '')}")
            st.markdown("**🎯 Key Assumptions**")
            for a in plan['assumptions']:
                st.markdown(f"- {a}")


        # ── VC VERDICT ─────────────────────────────────────────────
        st.markdown('<div class="section-header">🎤 VC Verdict</div>', unsafe_allow_html=True)

        rec_lower = recommendation.lower()
        if 'no-go' in rec_lower or 'no go' in rec_lower:
            verdict_class = "verdict-nogo"
            verdict_emoji = "🔴"
        elif 'conditional' in rec_lower:
            verdict_class = "verdict-conditional"
            verdict_emoji = "🟡"
        else:
            verdict_class = "verdict-go"
            verdict_emoji = "🟢"

        st.markdown(f'<div class="{verdict_class}">', unsafe_allow_html=True)
        st.markdown(recommendation)
        st.markdown('</div>', unsafe_allow_html=True)


        # ── HOW IT WORKS ───────────────────────────────────────────
        st.markdown("<br>", unsafe_allow_html=True)
        with st.expander("⚙️  How does VentureIQ work?"):
            st.markdown("""
**VentureIQ uses a 5-step AI pipeline** to evaluate your startup:

| Step | Agent | What It Does | Technology |
|------|-------|-------------|-----------|
| 1 | 🤖 Planner | Converts your idea into financial variables with min/max ranges | LLM (Llama 3.2) |
| 2 | 🎲 Simulator | Runs 10,000 random scenarios, calculates profit for each | Monte Carlo + NumPy |
| 3 | 🔍 Risk Critic | Tests each variable individually to find what matters most | Sensitivity Analysis |
| 4 | 🌐 Researcher | Searches real market data across 10 critical dimensions | DuckDuckGo Search |
| 5 | 🎤 Synthesizer | Combines all data into an honest VC-style recommendation | LLM (Llama 3.2) |

**Why Monte Carlo simulation?**
Instead of guessing one outcome, we run 10,000 different scenarios — each with randomly sampled values for every variable. This gives you a realistic probability distribution, not just a single optimistic guess.

**What are the 10 research dimensions?**
Geographic Viability · Market Size · Competition · Startup Costs · Revenue Benchmarks · Failure Reasons · Regulatory Requirements · Target Demographics · Economic Conditions · Seasonal Factors
            """)


        # ── FOOTER ─────────────────────────────────────────────────
        st.markdown("""
        <div class="footer">
            Built by <strong style="color:#555">Anoushka Dighe</strong>
            &nbsp;·&nbsp;
            <a href="https://github.com/anoushka29/decision-intelligence-system" target="_blank">GitHub</a>
            &nbsp;·&nbsp;
            Monte Carlo Simulation + Multi-Agent AI + Live Market Research
        </div>
        """, unsafe_allow_html=True)