import streamlit as st
import tempfile
import os
from parser.rvtools import parse_rvtools

st.set_page_config(page_title="Environment Analysis", layout="wide")
st.title("📊 Environment Analysis")
st.markdown("Upload your RVTools export to analyze your current infrastructure.")

uploaded_file = st.file_uploader("Upload RVTools Excel Export (.xlsx)", type=["xlsx"])

if uploaded_file:
    with st.spinner("Parsing RVTools data..."):
        with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
            tmp.write(uploaded_file.read())
            tmp_path = tmp.name
        parsed = parse_rvtools(tmp_path)
        os.unlink(tmp_path)

    if "error" in parsed:
        st.error(f"Error parsing file: {parsed['error']}")
    else:
        st.session_state.parsed_data = parsed
        st.success("✅ RVTools file parsed successfully!")

if st.session_state.parsed_data:
    parsed = st.session_state.parsed_data
    health = parsed.get('health', {})

    # Environment summary
    st.subheader("Environment Summary")
    col1, col2, col3, col4, col5 = st.columns(5)
    col1.metric("Total VMs", parsed.get('total_vms', 0))
    col2.metric("Powered On", parsed.get('powered_on_vms', 0))
    col3.metric("Powered Off", parsed.get('powered_off_vms', 0))
    col4.metric("Total Hosts", parsed.get('total_hosts', 0))
    col5.metric("Total Clusters", parsed.get('total_clusters', 0))

    col6, col7, col8, col9, col10 = st.columns(5)
    col6.metric("Total vCPU", parsed.get('total_vcpu', 0))
    col7.metric("Total vRAM (GB)", parsed.get('total_vram_gb', 0))
    col8.metric("Storage (GB)", parsed.get('total_storage_gb', 0))
    col9.metric("vCPU:pCPU Ratio", f"{parsed.get('vcpu_pcpu_ratio', 0)}:1")
    col10.metric("VM Density", f"{parsed.get('vm_density', 0)}/host")

    st.divider()

    # Health scorecard
    st.subheader("Environment Health Scorecard")

    overall = health.get('overall', 'Unknown')
    overall_pct = health.get('overall_pct', 0)

    if overall == 'Healthy':
        st.success(f"Overall Health: {overall} ({overall_pct}%)")
    elif overall == 'Needs Attention':
        st.warning(f"Overall Health: {overall} ({overall_pct}%)")
    else:
        st.error(f"Overall Health: {overall} ({overall_pct}%)")

    scores = health.get('scores', {})
    score_cols = st.columns(len(scores))
    icons = {'good': '✅', 'warning': '⚠️', 'critical': '🔴'}
    labels = {
        'vm_waste': 'VM Waste',
        'cpu_ratio': 'CPU Ratio',
        'os_currency': 'OS Currency',
        'storage': 'Storage',
        'density': 'VM Density'
    }
    for i, (key, val) in enumerate(scores.items()):
        score_cols[i].metric(labels.get(key, key), f"{icons.get(val, '')} {val.title()}")

    st.divider()

    # Flags and recommendations
    col_flags, col_recs = st.columns(2)

    with col_flags:
        st.subheader("⚠️ Flags")
        flags = health.get('flags', [])
        if flags:
            for flag in flags:
                st.warning(flag)
        else:
            st.success("No critical flags found!")

    with col_recs:
        st.subheader("💡 Recommendations")
        recs = health.get('recommendations', [])
        if recs:
            for rec in recs:
                st.info(rec)
        else:
            st.success("Environment looks clean — ready for migration planning!")

    st.divider()

    # OS breakdown
    st.subheader("OS Breakdown")
    col_os1, col_os2 = st.columns(2)
    with col_os1:
        st.metric("Windows VMs", parsed.get('windows_vms', 0))
        st.metric("Linux VMs", parsed.get('linux_vms', 0))
        st.metric("Windows Ratio", f"{round(parsed.get('windows_ratio', 0) * 100)}%")
    with col_os2:
        os_breakdown = parsed.get('os_breakdown', {})
        if os_breakdown:
            import pandas as pd
            os_df = pd.DataFrame(list(os_breakdown.items()), columns=['OS', 'Count'])
            os_df = os_df.sort_values('Count', ascending=False).head(10)
            st.dataframe(os_df, hide_index=True, use_container_width=True)

    st.divider()
    st.info("👈 Continue to **Current State TCO** in the sidebar to model your existing costs.")
