import streamlit as st
import plotly.graph_objects as go
from calculator.tco import calculate_current_tco
from pricing.defaults import HARDWARE, FTE

st.set_page_config(page_title="Current State TCO", layout="wide")
st.title("💰 Current State TCO")
st.markdown("Model the true cost of your existing infrastructure over time.")

if not st.session_state.get('parsed_data'):
    st.warning("Please upload an RVTools file on the Environment Analysis page first.")
    st.stop()

parsed = st.session_state.parsed_data

st.subheader("Adjust Assumptions")
st.caption("All values are editable — dial these in with your customer for accuracy.")

col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("**Infrastructure**")
    avg_host_cost = st.number_input("Avg Host Cost ($)", value=HARDWARE['avg_host_cost'], step=1000)
    refresh_years = st.number_input("Hardware Refresh Cycle (Years)", value=HARDWARE['refresh_cycle_years'], step=1)
    power_cost = st.number_input("Power Cost per kWh ($)", value=HARDWARE['power_cost_per_kwh'], step=0.01, format="%.2f")
    dc_cost = st.number_input("Datacenter Cost per Host/Year ($)", value=HARDWARE['datacenter_cost_per_host'], step=100)

with col2:
    st.markdown("**Labor**")
    fte_count = st.number_input("FTEs Managing Environment", value=3, step=1)
    fte_cost = st.number_input("Fully Loaded FTE Cost ($)", value=FTE['avg_fully_loaded_cost'], step=5000)

with col3:
    st.markdown("**Analysis Period**")
    years = st.selectbox("Analysis Period (Years)", [1, 2, 3, 5], index=2)
    st.markdown("**Licensing**")
    vsphere_per_core = st.number_input("Current vSphere Cost per Core/Year ($)", value=50, step=5)

overrides = {
    'hardware': {
        'avg_host_cost': avg_host_cost,
        'refresh_cycle_years': refresh_years,
        'power_cost_per_kwh': power_cost,
        'datacenter_cost_per_host': dc_cost,
    },
    'fte': {
        'avg_fully_loaded_cost': fte_cost,
    },
    'fte_count': fte_count,
    'years': years,
}

results = calculate_current_tco(parsed, overrides)
st.session_state.current_tco = results
st.session_state.assumptions = overrides

st.divider()

# Results summary
st.subheader(f"Current State {years}-Year TCO")

col1, col2, col3 = st.columns(3)
col1.metric(f"{years}-Year Total Cost", f"${results['total']:,.0f}")
col2.metric("Annual Average", f"${results['annual_average']:,.0f}")
col3.metric("Cost per VM per Year", f"${round(results['annual_average'] / max(parsed.get('total_vms', 1), 1)):,.0f}")

st.divider()

# Cost breakdown chart
st.subheader("Cost Breakdown")

col_chart, col_table = st.columns([2, 1])

with col_chart:
    categories = ['Hardware Refresh', 'Facilities & Power', 'Labor (FTE)', 'Licensing', 'Support & Maintenance']
    values = [
        results['hardware_refresh'],
        results['facilities'],
        results['fte'],
        results['licensing'],
        results['support'],
    ]

    fig = go.Figure(go.Bar(
        x=categories,
        y=values,
        marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd'],
        text=[f"${v:,.0f}" for v in values],
        textposition='outside',
    ))
    fig.update_layout(
        title=f"{years}-Year Cost by Category",
        yaxis_title="Cost ($)",
        showlegend=False,
        height=400,
    )
    st.plotly_chart(fig, use_container_width=True)

with col_table:
    st.markdown("**Cost Detail**")
    st.markdown(f"Hardware Refresh: **${results['hardware_refresh']:,.0f}**")
    st.markdown(f"Facilities & Power: **${results['facilities']:,.0f}**")
    st.markdown(f"Labor (FTE): **${results['fte']:,.0f}**")
    st.markdown(f"Licensing: **${results['licensing']:,.0f}**")
    st.markdown(f"Support: **${results['support']:,.0f}**")
    st.markdown("---")
    st.markdown(f"**Total: ${results['total']:,.0f}**")

st.divider()
st.info("👈 Continue to **Scenario Builder** in the sidebar to model private cloud options.")