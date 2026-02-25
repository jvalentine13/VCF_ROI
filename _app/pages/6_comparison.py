import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from calculator.roadmaps import get_roadmap

st.set_page_config(page_title="Comparison & Recommendation", layout="wide")
st.title("📊 Comparison & Recommendation")
st.markdown("Side-by-side analysis with a data-driven platform recommendation.")

if not st.session_state.get('parsed_data'):
    st.warning("Please upload an RVTools file on the Environment Analysis page first.")
    st.stop()

if not st.session_state.get('scenario_results'):
    st.warning("Please complete the Scenario Builder page first.")
    st.stop()

parsed = st.session_state.parsed_data
current_tco = st.session_state.current_tco
scenario_results = st.session_state.scenario_results
selected_platforms = st.session_state.selected_platforms
years = st.session_state.assumptions.get('years', 3)

# Determine recommended platform based on fit score + ROI
def get_recommendation(scenario_results):
    scores = {}
    for platform, r in scenario_results.items():
        fit_score = r['fit']['fit_score']
        roi_score = min(r['roi_pct'] / 2, 50)  # Cap ROI contribution at 50 points
        combined = (fit_score * 0.6) + (roi_score * 0.4)
        scores[platform] = round(combined, 1)
    return max(scores, key=scores.get), scores

recommended, combined_scores = get_recommendation(scenario_results)
override = st.session_state.get('recommendation_override')
final_recommendation = override if override else recommended

# Recommendation banner
st.subheader("🏆 Recommendation")
col_rec, col_override = st.columns([3, 1])

with col_rec:
    r = scenario_results[final_recommendation]
    if not override:
        st.success(f"**Recommended Platform: {final_recommendation}**")
    else:
        st.info(f"**Selected Platform: {final_recommendation}** *(manually selected)*")

    st.markdown(f"Combined Score: **{combined_scores[final_recommendation]}/100**")
    st.markdown(f"{years}-Year TCO: **${r['total']:,.0f}**")
    st.markdown(f"Savings vs Current: **${r['savings']:,.0f}** ({r['roi_pct']}% ROI)")
    st.markdown(f"Payback Period: **{r['payback_months']} months**")

    st.markdown("**Why this recommendation:**")
    fit_reasons = r['fit'].get('fit_reasons', [])
    if fit_reasons:
        for reason in fit_reasons:
            st.caption(f"📊 {reason}")
    strengths = r['fit'].get('strengths', [])
    for s in strengths[:3]:
        st.caption(f"✅ {s}")

with col_override:
    st.markdown("**Override Recommendation**")
    st.caption("You have the final call — select a different platform if needed.")
    override_choice = st.selectbox(
        "Select Platform",
        ["Auto (Recommended)"] + selected_platforms,
        index=0
    )
    if override_choice == "Auto (Recommended)":
        st.session_state.recommendation_override = None
    else:
        st.session_state.recommendation_override = override_choice

    if st.session_state.recommendation_override:
        st.warning(f"Override active: {st.session_state.recommendation_override}")
    else:
        st.success("Using data-driven recommendation")

st.divider()

# Combined scores radar-style bar chart
st.subheader("Platform Scoring Breakdown")
col_scores, col_savings = st.columns(2)

with col_scores:
    fig_scores = go.Figure(go.Bar(
        x=selected_platforms,
        y=[combined_scores[p] for p in selected_platforms],
        marker_color=['#2ca02c' if p == final_recommendation else '#1f77b4' for p in selected_platforms],
        text=[f"{combined_scores[p]}/100" for p in selected_platforms],
        textposition='outside',
    ))
    fig_scores.update_layout(
        title="Combined Fit + ROI Score",
        yaxis_title="Score",
        yaxis_range=[0, 110],
        height=350,
        showlegend=False,
    )
    st.plotly_chart(fig_scores, use_container_width=True)

with col_savings:
    fig_savings = go.Figure(go.Bar(
        x=selected_platforms,
        y=[scenario_results[p]['savings'] for p in selected_platforms],
        marker_color=['#2ca02c' if scenario_results[p]['savings'] > 0 else '#d62728' for p in selected_platforms],
        text=[f"${scenario_results[p]['savings']:,.0f}" for p in selected_platforms],
        textposition='outside',
    ))
    fig_savings.update_layout(
        title=f"{years}-Year Savings vs Current State",
        yaxis_title="Savings ($)",
        height=350,
        showlegend=False,
    )
    st.plotly_chart(fig_savings, use_container_width=True)

st.divider()

# Full side by side comparison table
st.subheader("Full Side-by-Side Comparison")

comparison_data = {
    'Metric': [
        f'{years}-Year TCO',
        'Annual Average Cost',
        f'Savings vs Current ({years}yr)',
        'ROI %',
        'Payback Period',
        'Effective Hosts',
        'Fit Score',
        'Licensing Model',
    ]
}

for platform in selected_platforms:
    r = scenario_results[platform]
    from pricing.defaults import PLATFORMS
    comparison_data[platform] = [
        f"${r['total']:,.0f}",
        f"${r['annual_average']:,.0f}",
        f"${r['savings']:,.0f}",
        f"{r['roi_pct']}%",
        f"{r['payback_months']} months",
        str(r['effective_hosts']),
        f"{r['fit']['fit_score']}/100",
        PLATFORMS[platform]['model'].replace('_', ' ').title(),
    ]

import pandas as pd
comparison_df = pd.DataFrame(comparison_data)
st.dataframe(comparison_df, hide_index=True, use_container_width=True)

st.divider()

# Payback period timeline
st.subheader("Payback Period Timeline")
fig_payback = go.Figure()

for platform in selected_platforms:
    r = scenario_results[platform]
    payback = r['payback_months']
    impl_cost = r['implementation']
    monthly_savings = r['savings'] / max(years * 12, 1)

    months = list(range(0, years * 12 + 1))
    cumulative = [-impl_cost + (monthly_savings * m) for m in months]

    fig_payback.add_trace(go.Scatter(
        x=months,
        y=cumulative,
        mode='lines',
        name=platform,
        line=dict(width=2),
    ))

fig_payback.add_hline(y=0, line_dash="dash", line_color="gray", annotation_text="Break Even")
fig_payback.update_layout(
    title="Cumulative Savings Over Time",
    xaxis_title="Months",
    yaxis_title="Cumulative Savings ($)",
    height=400,
    legend=dict(orientation="h", yanchor="bottom", y=1.02)
)
st.plotly_chart(fig_payback, use_container_width=True)

st.divider()

# Risk of doing nothing
st.subheader("⚠️ Risk of Doing Nothing")
col_r1, col_r2, col_r3 = st.columns(3)
annual_current = current_tco['annual_average']
col_r1.metric("Annual Cost of Status Quo", f"${annual_current:,.0f}")
col_r2.metric("5-Year Cost of Inaction", f"${annual_current * 5:,.0f}")
col_r3.metric("Opportunity Cost vs Best Option",
    f"${max(r['savings'] for r in scenario_results.values()):,.0f}")

health = parsed.get('health', {})
flags = health.get('flags', [])
if flags:
    st.markdown("**Unresolved environment risks if no action is taken:**")
    for flag in flags:
        st.warning(f"🔴 {flag}")
st.divider()

# ── Platform Roadmap ─────────────────────────────────────────────
st.subheader("🗺️ Your Private Cloud Journey")

roadmap_platform = st.selectbox(
    "View roadmap for:",
    selected_platforms,
    index=selected_platforms.index(final_recommendation) if final_recommendation in selected_platforms else 0
)

roadmap = get_roadmap(roadmap_platform)
if roadmap:
    if roadmap_platform == final_recommendation:
        st.success(f"⭐ Recommended platform — {roadmap['tagline']}")
    else:
        st.info(f"{roadmap['tagline']}")

    st.divider()

    for phase in roadmap['phases']:
        with st.expander(
            f"Phase {phase['number']} — {phase['name']}  |  {phase['timeline']}",
            expanded=(phase['number'] == 1)
        ):
            st.markdown(f"**Objective:** {phase['objective']}")
            col_act, col_exit = st.columns(2)
            with col_act:
                st.markdown("**Key Activities & Outputs**")
                for activity in phase['activities']:
                    st.caption(f"• {activity}")
            with col_exit:
                st.markdown("**Exit Criteria**")
                for criterion in phase['exit_criteria']:
                    st.caption(f"✅ {criterion}")

    st.divider()

    # Phase timeline visual
    st.markdown("**Journey Timeline**")
    phase_cols = st.columns(5)
    colors = ['#1F4E79', '#2E75B6', '#4472C4', '#70AD47', '#ED7D31']
    for i, phase in enumerate(roadmap['phases']):
        with phase_cols[i]:
            st.markdown(
                f"""<div style='background-color:{colors[i]};padding:12px;border-radius:8px;text-align:center;color:white;'>
                <strong>Phase {phase['number']}</strong><br/>
                <small>{phase['name'].split('—')[0].strip()}</small><br/>
                <small><em>{phase['timeline']}</em></small>
                </div>""",
                unsafe_allow_html=True
            )

st.divider()
st.info("👈 Continue to **Export & Proposal** in the sidebar to generate your customer deliverables.")