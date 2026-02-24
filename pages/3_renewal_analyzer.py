import streamlit as st
import plotly.graph_objects as go
from datetime import date, datetime

st.set_page_config(page_title="VMware Renewal Analyzer", layout="wide")
st.title("⏰ VMware Renewal Analyzer")
st.markdown("Quantify the cost of renewal vs. modernization and the urgency of acting now.")

st.divider()

# ── Renewal Inputs ────────────────────────────────────────────────
st.subheader("Current VMware Contract Details")
col1, col2, col3 = st.columns(3)

with col1:
    renewal_date = st.date_input(
        "VMware Renewal Date",
        value=date(2025, 12, 31),
        help="When does the current VMware contract expire?"
    )
    current_annual_spend = st.number_input(
        "Current Annual VMware Spend ($)",
        value=150000,
        step=5000,
        help="Total annual spend on VMware licensing and support"
    )

with col2:
    broadcom_increase = st.slider(
        "Expected Broadcom Price Increase (%)",
        0, 300, 40,
        help="Broadcom has been increasing prices significantly post-acquisition"
    )
    contract_years = st.selectbox(
        "Renewal Term",
        [1, 2, 3],
        index=2,
        help="How many years would you renew for?"
    )

with col3:
    migration_timeline = st.selectbox(
        "Estimated Migration Timeline to Private Cloud",
        ["6 months", "12 months", "18 months", "24 months"],
        index=1
    )
    migration_cost = st.number_input(
        "Estimated Migration / Implementation Cost ($)",
        value=75000,
        step=5000,
        help="One-time cost to migrate to private cloud platform"
    )

st.divider()

# ── Calculations ──────────────────────────────────────────────────
today = date.today()
days_to_renewal = (renewal_date - today).days
months_to_renewal = max(round(days_to_renewal / 30), 0)

# Renewal cost with Broadcom increase
increased_annual_spend = current_annual_spend * (1 + broadcom_increase / 100)
renewal_total_cost = increased_annual_spend * contract_years

# Current spend if they do nothing and renew
do_nothing_cost = current_annual_spend + renewal_total_cost

# Cost of waiting — each month they delay migration
monthly_vmware_cost = increased_annual_spend / 12
migration_months = int(migration_timeline.split()[0])

# Crossover analysis — month by month
months_range = list(range(0, (contract_years * 12) + 1))

# Renew path: pay increased rate for full term
renew_cumulative = [increased_annual_spend / 12 * m for m in months_range]

# Migrate path: pay current rate during migration, then private cloud cost
# Assume private cloud is 20% less than current VMware annually
private_cloud_annual = current_annual_spend * 0.80
private_cloud_monthly = private_cloud_annual / 12

migrate_cumulative = []
for m in months_range:
    if m <= migration_months:
        # During migration still paying VMware
        cost = (current_annual_spend / 12 * m) + (migration_cost * min(m / migration_months, 1))
    else:
        # After migration paying private cloud rate
        migration_period_cost = current_annual_spend / 12 * migration_months + migration_cost
        post_migration_cost = private_cloud_monthly * (m - migration_months)
        cost = migration_period_cost + post_migration_cost
    migrate_cumulative.append(cost)

# Find crossover month
crossover_month = None
for i, (r, m) in enumerate(zip(renew_cumulative, migrate_cumulative)):
    if m < r and i > migration_months:
        crossover_month = i
        break

# Cost of waiting — each month delayed adds to renewal exposure
cost_per_month_delay = monthly_vmware_cost

# ── Summary Metrics ───────────────────────────────────────────────
st.subheader("Renewal Analysis Summary")

col_a, col_b, col_c, col_d = st.columns(4)

col_a.metric(
    "Days Until Renewal",
    f"{max(days_to_renewal, 0)}",
    delta=f"{months_to_renewal} months",
    delta_color="inverse" if months_to_renewal < 6 else "normal"
)

col_b.metric(
    f"Renewal Cost ({contract_years}yr at +{broadcom_increase}%)",
    f"${renewal_total_cost:,.0f}",
    delta=f"+${renewal_total_cost - (current_annual_spend * contract_years):,.0f} vs flat renewal"
)

col_c.metric(
    "Cost Per Month of Delay",
    f"${cost_per_month_delay:,.0f}",
    delta="Each month you wait"
)

if crossover_month:
    col_d.metric(
        "Break-Even Month",
        f"Month {crossover_month}",
        delta=f"Migration pays off at month {crossover_month}"
    )
else:
    col_d.metric(
        "Break-Even",
        "Within term",
        delta="Migration pays off before renewal ends"
    )

st.divider()

# Urgency banner
if months_to_renewal <= 3:
    st.error(f"🚨 **Critical:** Renewal is {months_to_renewal} months away. Immediate action required to avoid automatic renewal at increased rates.")
elif months_to_renewal <= 6:
    st.warning(f"⚠️ **Urgent:** Renewal is {months_to_renewal} months away. Decision window is closing — migration planning should begin now.")
elif months_to_renewal <= 12:
    st.warning(f"📅 **Plan Now:** Renewal is {months_to_renewal} months away. Ideal time to evaluate and plan migration to avoid renewal lock-in.")
else:
    st.info(f"📋 **Strategic Window:** Renewal is {months_to_renewal} months away. Plenty of time to plan a thoughtful migration — but starting now maximizes savings.")

st.divider()

# ── Crossover Chart ───────────────────────────────────────────────
st.subheader("Cost Trajectory: Renew vs. Migrate")

fig = go.Figure()

fig.add_trace(go.Scatter(
    x=months_range,
    y=renew_cumulative,
    mode='lines',
    name='Renew VMware (Broadcom pricing)',
    line=dict(color='#d62728', width=3),
))

fig.add_trace(go.Scatter(
    x=months_range,
    y=migrate_cumulative,
    mode='lines',
    name='Migrate to Private Cloud',
    line=dict(color='#2ca02c', width=3),
))

# Mark migration completion
fig.add_vline(
    x=migration_months,
    line_dash="dash",
    line_color="gray",
    annotation_text=f"Migration complete (month {migration_months})",
    annotation_position="top right"
)

# Mark crossover
if crossover_month:
    fig.add_vline(
        x=crossover_month,
        line_dash="dot",
        line_color="gold",
        annotation_text=f"Break-even (month {crossover_month})",
        annotation_position="top left"
    )

fig.update_layout(
    title="Cumulative Cost: Renew VMware vs. Migrate to Private Cloud",
    xaxis_title="Months",
    yaxis_title="Cumulative Cost ($)",
    height=450,
    legend=dict(orientation="h", yanchor="bottom", y=1.02),
    hovermode='x unified',
)
st.plotly_chart(fig, use_container_width=True)

st.divider()

# ── Scenario Comparison Table ─────────────────────────────────────
st.subheader("Scenario Comparison")

col_s1, col_s2, col_s3 = st.columns(3)

with col_s1:
    st.markdown("### 🔴 Renew As-Is")
    st.markdown(f"**Annual Cost:** ${increased_annual_spend:,.0f}")
    st.markdown(f"**{contract_years}-Year Total:** ${renewal_total_cost:,.0f}")
    st.markdown(f"**Price Increase:** +{broadcom_increase}%")
    st.markdown(f"**Lock-in Period:** {contract_years} years")
    st.markdown("**Strategic Value:** None — same capabilities, higher cost")
    st.error("Not recommended")

with col_s2:
    st.markdown("### 🟡 Delay Decision")
    delay_months = 6
    delay_cost = monthly_vmware_cost * delay_months
    st.markdown(f"**Cost of 6-Month Delay:** ${delay_cost:,.0f}")
    st.markdown(f"**Cost of 12-Month Delay:** ${delay_cost * 2:,.0f}")
    st.markdown(f"**Risk:** May be forced into renewal")
    st.markdown(f"**Opportunity Cost:** ${delay_cost:,.0f} that could fund migration")
    st.markdown("**Strategic Value:** None — just deferred cost")
    st.warning("Evaluate urgency")

with col_s3:
    migrate_3yr = migrate_cumulative[min(contract_years * 12, len(migrate_cumulative)-1)]
    savings_vs_renew = renewal_total_cost - migrate_3yr
    st.markdown("### 🟢 Migrate to Private Cloud")
    st.markdown(f"**Migration Cost:** ${migration_cost:,.0f}")
    st.markdown(f"**{contract_years}-Year Total:** ${migrate_3yr:,.0f}")
    st.markdown(f"**Savings vs Renewal:** ${savings_vs_renew:,.0f}")
    st.markdown(f"**Break-Even:** Month {crossover_month if crossover_month else 'within term'}")
    st.markdown("**Strategic Value:** Modern platform, AI/ML ready, self-service")
    st.success("Recommended path")

st.divider()

# Save renewal data to session state
renewal_data = {
    'renewal_date': str(renewal_date),
    'days_to_renewal': days_to_renewal,
    'months_to_renewal': months_to_renewal,
    'current_annual_spend': current_annual_spend,
    'increased_annual_spend': increased_annual_spend,
    'broadcom_increase': broadcom_increase,
    'renewal_total_cost': renewal_total_cost,
    'migration_cost': migration_cost,
    'migration_timeline': migration_timeline,
    'crossover_month': crossover_month,
    'cost_per_month_delay': cost_per_month_delay,
    'contract_years': contract_years,
}
st.session_state.renewal_data = renewal_data

st.info("👈 Continue to **Current State TCO** in the sidebar to complete the full analysis.")