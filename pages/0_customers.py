import streamlit as st
from datetime import datetime
from calculator.sessions import save_session, load_session, list_sessions, delete_session

st.set_page_config(page_title="Customer Manager", layout="wide")
st.title("👥 Customer Manager")
st.markdown("Save, load, and manage customer analyses.")

st.divider()

# ── Save Current Session ──────────────────────────────────────────
st.subheader("💾 Save Current Analysis")

if not st.session_state.get('parsed_data'):
    st.info("No active analysis to save — upload an RVTools file on the Environment Analysis page first.")
else:
    parsed = st.session_state.parsed_data
    col1, col2 = st.columns([3, 1])
    with col1:
        save_name = st.text_input(
            "Customer Name for Save",
            value=st.session_state.get('customer_name', ''),
            placeholder="Enter customer name"
        )
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("💾 Save Analysis", type="primary"):
            if save_name:
                session_data = {
                    'parsed_data': st.session_state.get('parsed_data'),
                    'current_tco': st.session_state.get('current_tco'),
                    'scenario_results': st.session_state.get('scenario_results'),
                    'selected_platforms': st.session_state.get('selected_platforms'),
                    'assumptions': st.session_state.get('assumptions'),
                    'discovery': st.session_state.get('discovery'),
                    'renewal_data': st.session_state.get('renewal_data'),
                    'recommendation_override': st.session_state.get('recommendation_override'),
                    'quotes': st.session_state.get('quotes'),
                }
                filename = save_session(save_name, session_data)
                st.success(f"✅ Analysis saved for {save_name}!")
                st.caption(f"Saved as: {filename}")
            else:
                st.warning("Please enter a customer name before saving.")

    # Current session summary
    st.markdown("**Current Session:**")
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Total VMs", parsed.get('total_vms', 0))
    col_b.metric("Total Hosts", parsed.get('total_hosts', 0))
    col_c.metric("Health", parsed.get('health', {}).get('overall', 'N/A'))
    col_d.metric("Scenarios Run", len(st.session_state.get('scenario_results', {})))

st.divider()

# ── Saved Sessions ────────────────────────────────────────────────
st.subheader("📂 Saved Customer Analyses")

sessions = list_sessions()

if not sessions:
    st.info("No saved analyses yet. Complete an analysis and save it above.")
else:
    # Search
    search = st.text_input("🔍 Search customers", placeholder="Type to filter...")
    if search:
        sessions = [s for s in sessions if search.lower() in s['customer_name'].lower()]

    for session in sessions:
        with st.container():
            col1, col2, col3, col4, col5 = st.columns([3, 1, 2, 1, 1])

            with col1:
                st.markdown(f"**{session['customer_name']}**")
                saved_dt = session['saved_at'][:16].replace('T', ' ') if session['saved_at'] else 'Unknown'
                st.caption(f"Saved: {saved_dt}")

            with col2:
                st.metric("VMs", session['total_vms'])

            with col3:
                rec = session['recommendation']
                if rec and rec != 'N/A':
                    st.markdown(f"**Recommendation:**")
                    st.caption(rec)
                else:
                    st.caption("No recommendation yet")

            with col4:
                if st.button("📂 Load", key=f"load_{session['filename']}"):
                    data = load_session(session['filename'])
                    if data:
                        st.session_state.parsed_data = data.get('parsed_data')
                        st.session_state.current_tco = data.get('current_tco')
                        st.session_state.scenario_results = data.get('scenario_results', {})
                        st.session_state.selected_platforms = data.get('selected_platforms', [])
                        st.session_state.assumptions = data.get('assumptions', {})
                        st.session_state.discovery = data.get('discovery', {})
                        st.session_state.renewal_data = data.get('renewal_data', {})
                        st.session_state.recommendation_override = data.get('recommendation_override')
                        st.session_state.quotes = data.get('quotes', {})
                        st.session_state.customer_name = data.get('customer_name', '')
                        st.success(f"✅ Loaded {data.get('customer_name')}!")
                        st.rerun()
                    else:
                        st.error("Could not load session.")

            with col5:
                if st.button("🗑️ Delete", key=f"delete_{session['filename']}"):
                    if delete_session(session['filename']):
                        st.success("Deleted!")
                        st.rerun()

            st.divider()

st.divider()

# ── Start New Analysis ────────────────────────────────────────────
st.subheader("🆕 Start New Analysis")
st.caption("This will clear the current session and start fresh.")
if st.button("Clear Session & Start New", type="secondary"):
    for key in ['parsed_data', 'current_tco', 'scenario_results', 'selected_platforms',
                'assumptions', 'discovery', 'renewal_data', 'recommendation_override', 'quotes']:
        if key in st.session_state:
            del st.session_state[key]
    st.success("Session cleared! Go to Environment Analysis to upload a new RVTools file.")
    st.rerun()

