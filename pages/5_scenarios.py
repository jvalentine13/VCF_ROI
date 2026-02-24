import streamlit as st
import plotly.graph_objects as go
from calculator.tco import calculate_platform_tco, calculate_roi
from calculator.platforms.vcf import get_vcf_tco
from calculator.platforms.nutanix import get_nutanix_tco
from calculator.platforms.openshift import get_openshift_tco
from calculator.platforms.azure_stack import get_azure_stack_tco
from pricing.defaults import PLATFORMS, HARDWARE, FTE

st.set_page_config(page_title="Scenario Builder", layout="wide")
st.title("🔧 Scenario Builder")
st.markdown("Select platforms to model and adjust assumptions to match real-world quotes.")

if not st.session_state.get('parsed_data'):
    st.warning("Please upload an RVTools file on the Environment Analysis page first.")
    st.stop()

if not st.session_state.get('current_tco'):
    st.warning("Please complete the Current State TCO page first.")
    st.stop()

parsed = st.session_state.parsed_data
current_tco = st.session_state.current_tco
years = st.session_state.assumptions.get('years', 3)

# Platform selection
st.subheader("Select Platforms to Compare")
col1, col2, col3, col4 = st.columns(4)
with col1:
    vcf_selected = st.checkbox("VMware VCF", value=True)
with col2:
    nutanix_selected = st.checkbox("Nutanix", value=True)
with col3:
    openshift_selected = st.checkbox("Red Hat OpenShift", value=True)
with col4:
    azure_selected = st.checkbox("Azure Stack HCI", value=True)

selected_platforms = []
if vcf_selected:
    selected_platforms.append("VMware VCF")
if nutanix_selected:
    selected_platforms.append("Nutanix")
if openshift_selected:
    selected_platforms.append("Red Hat OpenShift")
if azure_selected:
    selected_platforms.append("Azure Stack HCI")

st.session_state.selected_platforms = selected_platforms

if not selected_platforms:
    st.warning("Please select at least one platform.")
    st.stop()

st.divider()

# Global assumptions
st.subheader("Global Assumptions")
col_a, col_b, col_c = st.columns(3)
with col_a:
    fte_reduction = st.slider("FTE Reduction with Private Cloud (%)", 0, 60, 40)
with col_b:
    hardware_efficiency = st.slider("Hardware Consolidation Efficiency (%)", 60, 100, 80)
with col_c:
    fte_count = st.session_state.assumptions.get('fte_count', 3)
    st.metric("FTEs (from TCO page)", fte_count)

st.divider()

# Per-platform pricing overrides
st.subheader("Platform Pricing Overrides")
st.caption("Override default pricing with actual quotes from vendors.")

platform_overrides = {}
override_cols = st.columns(len(selected_platforms))

for i, platform in enumerate(selected_platforms):
    with override_cols[i]:
        st.markdown(f"**{platform}**")
        defaults = PLATFORMS[platform]
        if defaults['model'] == 'per_core':
            custom_price = st.number_input(
                f"Cost per Core/Year ($)",
                value=float(defaults['cost_per_core_per_year']),
                step=10.0,
                key=f"price_{platform}"
            )
            platform_overrides[platform] = {'cost_per_core_per_year': custom_price}
        elif defaults['model'] == 'per_node':
            custom_price = st.number_input(
                f"Cost per Node/Year ($)",
                value=float(defaults['cost_per_node_per_year']),
                step=500.0,
                key=f"price_{platform}"
            )
            platform_overrides[platform] = {'cost_per_node_per_year': custom_price}

st.divider()

# Calculate scenarios
st.subheader("Scenario Results")

scenario_results = {}
platform_fits = {}

platform_fit_funcs = {
    "VMware VCF": get_vcf_tco,
    "Nutanix": get_nutanix_tco,
    "Red Hat OpenShift": get_openshift_tco,
    "Azure Stack HCI": get_azure_stack_tco,
}

for platform in selected_platforms:
    overrides = {
        'hardware': st.session_state.assumptions.get('hardware', {}),
        'fte': st.session_state.assumptions.get('fte', {}),
        'fte_count': fte_count,
        'fte_reduction': fte_reduction / 100,
        'hardware_efficiency': hardware_efficiency / 100,
        'years': years,
        'pricing': platform_overrides.get(platform, {}),
    }
    tco = calculate_platform_tco(parsed, platform, overrides)
    roi = calculate_roi(current_tco, tco)
    fit = platform_fit_funcs[platform](parsed)

    scenario_results[platform] = {**tco, **roi, 'fit': fit}
    platform_fits[platform] = fit

st.session_state.scenario_results = scenario_results

# Results metrics
result_cols = st.columns(len(selected_platforms))
for i, platform in enumerate(selected_platforms):
    r = scenario_results[platform]
    with result_cols[i]:
        st.markdown(f"**{platform}**")
        st.metric(f"{years}-Year TCO", f"${r['total']:,.0f}")
        savings_color = "normal" if r['savings'] > 0 else "inverse"
        st.metric("Savings vs Current", f"${r['savings']:,.0f}", delta=f"{r['roi_pct']}% ROI")
        st.metric("Payback Period", f"{r['payback_months']} months")
        st.metric("Fit Score", f"{r['fit']['fit_score']}/100")

st.divider()

# TCO comparison chart
st.subheader("TCO Comparison")

fig = go.Figure()
cost_categories = ['licensing', 'support', 'hardware_refresh', 'facilities', 'fte', 'implementation']
category_labels = ['Licensing', 'Support', 'Hardware', 'Facilities', 'Labor', 'Implementation']
colors = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c', '#98df8a']

for cat, label, color in zip(cost_categories, category_labels, colors):
    fig.add_trace(go.Bar(
        name=label,
        x=selected_platforms,
        y=[scenario_results[p][cat] for p in selected_platforms],
        marker_color=color,
    ))

fig.update_layout(
    barmode='stack',
    title=f"{years}-Year TCO by Platform and Cost Category",
    yaxis_title="Cost ($)",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02)
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# Platform fit scores
st.subheader("Platform Fit Analysis")
fit_cols = st.columns(len(selected_platforms))
for i, platform in enumerate(selected_platforms):
    fit = platform_fits[platform]
    with fit_cols[i]:
        st.markdown(f"**{platform}**")
        score = fit['fit_score']
        if score >= 70:
            st.success(f"Fit Score: {score}/100")
        elif score >= 50:
            st.warning(f"Fit Score: {score}/100")
        else:
            st.error(f"Fit Score: {score}/100")

        st.markdown("**Strengths:**")
        for s in fit['strengths'][:3]:
            st.caption(f"✅ {s}")

        st.markdown("**Considerations:**")
        for c in fit['considerations'][:2]:
            st.caption(f"⚠️ {c}")

        if fit['fit_reasons']:
            st.markdown("**Why this score:**")
            for r in fit['fit_reasons']:
                st.caption(f"📊 {r}")

st.divider()
st.info("👈 Continue to **Comparison Dashboard** in the sidebar to see the full recommendation.")