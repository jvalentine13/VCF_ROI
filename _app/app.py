import streamlit as st

st.set_page_config(
    page_title="Private Cloud ROI Calculator",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Session state initialization
if 'parsed_data' not in st.session_state:
    st.session_state.parsed_data = None
if 'current_tco' not in st.session_state:
    st.session_state.current_tco = None
if 'scenario_results' not in st.session_state:
    st.session_state.scenario_results = {}
if 'selected_platforms' not in st.session_state:
    st.session_state.selected_platforms = []
if 'recommendation_override' not in st.session_state:
    st.session_state.recommendation_override = None
if 'assumptions' not in st.session_state:
    st.session_state.assumptions = {}

st.title("☁️ Private Cloud ROI & TCO Calculator")
st.markdown("---")

if st.session_state.parsed_data is None:
    st.info("👈 Start by uploading an RVTools export on the **Environment Analysis** page in the sidebar.")
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Step 1", "Upload RVTools")
        st.caption("Parse your current environment")
    with col2:
        st.metric("Step 2", "Review TCO")
        st.caption("Understand current state costs")
    with col3:
        st.metric("Step 3", "Model Scenarios")
        st.caption("Compare private cloud options")
    with col4:
        st.metric("Step 4", "Export")
        st.caption("PDF, Excel, and slide-ready charts")
else:
    parsed = st.session_state.parsed_data
    st.success("✅ Environment loaded — navigate the pages in the sidebar to continue.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total VMs", parsed.get('total_vms', 0))
    col2.metric("Total Hosts", parsed.get('total_hosts', 0))
    col3.metric("Total vCPU", parsed.get('total_vcpu', 0))
    col4.metric("Health Score", f"{parsed.get('health', {}).get('overall_pct', 0)}%")