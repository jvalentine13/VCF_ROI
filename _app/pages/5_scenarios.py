import streamlit as st
import plotly.graph_objects as go
from calculator.tco import calculate_platform_tco, calculate_roi
from calculator.platforms.vcf import get_vcf_tco
from calculator.platforms.nutanix import get_nutanix_tco
from calculator.platforms.openshift import get_openshift_tco
from calculator.platforms.azure_stack import get_azure_stack_tco
from pricing.defaults import PLATFORMS, HARDWARE, FTE
from calculator.validation import validate_quote_inputs, validate_discovery

def _get_pricing_override(platform, manual_overrides, quotes, parsed):
    """Resolve pricing — actual quote takes priority over manual override over defaults."""
    override = manual_overrides.get(platform, {}).copy()
    quote = quotes.get(platform, {})
    
    if not quote or quote.get('value', 0) == 0:
        return override

    value = quote['value']
    quote_type = quote.get('type', '')
    hosts = parsed.get('total_hosts', 1)
    cores = parsed.get('total_physical_cores', hosts * 20)
    nodes = hosts

    from pricing.defaults import PLATFORMS
    model = PLATFORMS[platform]['model']

    if 'Total Contract Value' in quote_type:
        if model == 'per_core':
            override['cost_per_core_per_year'] = round(value / max(cores, 1), 2)
        elif model == 'per_node':
            override['cost_per_node_per_year'] = round(value / max(nodes, 1), 2)
    else:
        if model == 'per_core':
            override['cost_per_core_per_year'] = value
        elif model == 'per_node':
            override['cost_per_node_per_year'] = value

    return override

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

# ── Quote Input Section ───────────────────────────────────────────
st.subheader("💼 Vendor Quote Inputs")
st.info("💡 Have actual vendor quotes? Enter them here to override default list pricing and get the most accurate TCO. Leave blank to use industry defaults.")

with st.expander("Enter Actual Vendor Quotes (optional but recommended)", expanded=True):
    q1, q2 = st.columns(2)
    with q1:
        st.markdown("**VMware VCF**")
        vcf_quote_type = st.selectbox("Quote Type", ["Per Core/Year", "Total Contract Value"], key="vcf_quote_type")
        vcf_quote_value = st.number_input("VCF Quote Amount ($)", value=0, step=1000, key="vcf_quote_amount",
            help="Enter 0 to use default pricing of $150/core/year")
        vcf_quote_ref = st.text_input("Quote Reference #", key="vcf_quote_ref", placeholder="e.g. Q-2025-12345")
        vcf_quote_expiry = st.date_input("Quote Expiry Date", key="vcf_quote_expiry")

        st.markdown("**Nutanix**")
        nutanix_quote_type = st.selectbox("Quote Type", ["Per Node/Year", "Total Contract Value"], key="nutanix_quote_type")
        nutanix_quote_value = st.number_input("Nutanix Quote Amount ($)", value=0, step=1000, key="nutanix_quote_amount",
            help="Enter 0 to use default pricing of $8,000/node/year")
        nutanix_quote_ref = st.text_input("Quote Reference #", key="nutanix_quote_ref", placeholder="e.g. Q-2025-67890")
        nutanix_quote_expiry = st.date_input("Quote Expiry Date", key="nutanix_quote_expiry")

    with q2:
        st.markdown("**Red Hat OpenShift**")
        openshift_quote_type = st.selectbox("Quote Type", ["Per Core/Year", "Total Contract Value"], key="openshift_quote_type")
        openshift_quote_value = st.number_input("OpenShift Quote Amount ($)", value=0, step=1000, key="openshift_quote_amount",
            help="Enter 0 to use default pricing of $120/core/year")
        openshift_quote_ref = st.text_input("Quote Reference #", key="openshift_quote_ref", placeholder="e.g. Q-2025-11111")
        openshift_quote_expiry = st.date_input("Quote Expiry Date", key="openshift_quote_expiry")

        st.markdown("**Azure Stack HCI**")
        azure_quote_type = st.selectbox("Quote Type", ["Per Core/Year", "Total Contract Value"], key="azure_quote_type")
        azure_quote_value = st.number_input("Azure Stack HCI Quote Amount ($)", value=0, step=1000, key="azure_quote_amount",
            help="Enter 0 to use default pricing of $100/core/year")
        azure_quote_ref = st.text_input("Quote Reference #", key="azure_quote_ref", placeholder="e.g. Q-2025-22222")
        azure_quote_expiry = st.date_input("Quote Expiry Date", key="azure_quote_expiry")

    # Store quote data in session state
    st.session_state.quotes = {
        'VMware VCF': {
            'type': vcf_quote_type,
            'value': vcf_quote_value,
            'ref': vcf_quote_ref,
            'expiry': str(vcf_quote_expiry),
        },
        'Nutanix': {
            'type': nutanix_quote_type,
            'value': nutanix_quote_value,
            'ref': nutanix_quote_ref,
            'expiry': str(nutanix_quote_expiry),
        },
        'Red Hat OpenShift': {
            'type': openshift_quote_type,
            'value': openshift_quote_value,
            'ref': openshift_quote_ref,
            'expiry': str(openshift_quote_expiry),
        },
        'Azure Stack HCI': {
            'type': azure_quote_type,
            'value': azure_quote_value,
            'ref': azure_quote_ref,
            'expiry': str(azure_quote_expiry),
        },
    }

# Validate quotes
    quote_warnings = validate_quote_inputs(st.session_state.quotes, parsed)
    for w in quote_warnings:
        st.warning(f"⚠️ {w}")

    # Validate discovery completeness
    completion_pct, disc_warnings = validate_discovery(st.session_state.get('discovery', {}))
    if disc_warnings:
        for w in disc_warnings:
            st.info(f"💡 {w}")
    else:
        st.success(f"✅ Discovery {completion_pct}% complete — recommendation confidence is high.")

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
        'pricing': _get_pricing_override(platform, platform_overrides,
                                          st.session_state.get('quotes', {}),
                                          parsed),
    }
    tco = calculate_platform_tco(parsed, platform, overrides)
    roi = calculate_roi(current_tco, tco)
    fit = platform_fit_funcs[platform](parsed)

    # Apply discovery fit adjustments if available
    discovery = st.session_state.get('discovery', {})
    fit_adjustments = discovery.get('fit_adjustments', {})
    if platform in fit_adjustments:
        raw_score = fit['fit_score'] + fit_adjustments[platform]
        fit['fit_score'] = max(0, min(raw_score, 100))
        if fit_adjustments[platform] > 0:
            fit['fit_reasons'].append(f"Discovery responses added +{fit_adjustments[platform]} points")
        elif fit_adjustments[platform] < 0:
            fit['fit_reasons'].append(f"Discovery responses adjusted {fit_adjustments[platform]} points")

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