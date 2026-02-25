import streamlit as st

st.set_page_config(page_title="Discovery Questionnaire", layout="wide")
st.title("🔍 Discovery Questionnaire")
st.markdown("Help us understand your strategy and goals to build the most accurate recommendation.")

if not st.session_state.get('parsed_data'):
    st.warning("Please upload an RVTools file on the Environment Analysis page first.")
    st.stop()

st.info("Answer as many questions as you can. Unanswered questions will use neutral defaults and won't skew the recommendation.")

# Initialize discovery state
if 'discovery' not in st.session_state:
    st.session_state.discovery = {}

st.divider()

# ── Section 1: Strategic Direction ──────────────────────────────
st.subheader("1️⃣ Strategic Direction")
col1, col2 = st.columns(2)

with col1:
    primary_driver = st.selectbox(
        "What is the primary driver for this conversation?",
        ["-- Select --", "VMware renewal / cost pressure", "Infrastructure modernization",
         "Security and compliance", "Business growth / new workloads",
         "Developer agility / speed to market", "AI/ML initiative"],
        key="primary_driver"
    )

    app_strategy = st.selectbox(
        "What is the 3-year application strategy?",
        ["-- Select --", "Lift and shift — move as-is",
         "Modernize selectively — some refactoring",
         "Cloud-native first — containers and microservices",
         "Mixed — depends on the workload"],
        key="app_strategy"
    )

with col2:
    time_horizon = st.selectbox(
        "What is the decision timeline?",
        ["-- Select --", "Immediate (0-3 months)",
         "Near term (3-6 months)",
         "Planning phase (6-12 months)",
         "Exploratory (12+ months)"],
        key="time_horizon"
    )

    vendor_consolidation = st.selectbox(
        "How important is vendor consolidation?",
        ["-- Select --", "Critical — we want fewer vendors",
         "Important — but not a dealbreaker",
         "Neutral — best tool for the job",
         "Not a priority"],
        key="vendor_consolidation"
    )

st.divider()

# ── Section 2: Workload Profile ──────────────────────────────────
st.subheader("2️⃣ Workload Profile")
col3, col4 = st.columns(2)

with col3:
    kubernetes = st.selectbox(
        "Are you running or planning Kubernetes/containers?",
        ["-- Select --", "Yes — already running in production",
         "Yes — actively planning deployment",
         "Evaluating — interested but not committed",
         "No — not on the roadmap"],
        key="kubernetes"
    )

    dev_methodology = st.selectbox(
        "What is the primary development methodology?",
        ["-- Select --", "Traditional IT ops — tickets and manual processes",
         "DevOps — some automation and pipelines",
         "DevSecOps — security integrated into pipelines",
         "Platform engineering — internal developer platform"],
        key="dev_methodology"
    )

with col4:
    ai_ml = st.selectbox(
        "Are there AI/ML workload plans on-premises?",
        ["-- Select --", "Yes — active AI/ML initiative needing on-prem GPU",
         "Yes — planning private AI for data sovereignty",
         "Evaluating — interested in private AI",
         "No — using public cloud for AI"],
        key="ai_ml"
    )

    workload_sensitivity = st.selectbox(
        "How sensitive are workloads to data sovereignty / compliance?",
        ["-- Select --", "Highly sensitive — regulated industry (finance, health, gov)",
         "Moderately sensitive — some compliance requirements",
         "Low sensitivity — standard commercial workloads"],
        key="workload_sensitivity"
    )

st.divider()

# ── Section 3: Existing Investments ──────────────────────────────
st.subheader("3️⃣ Existing Technology Investments")
col5, col6 = st.columns(2)

with col5:
    current_hypervisor = st.selectbox(
        "What is the current hypervisor environment?",
        ["-- Select --", "VMware vSphere — all in",
         "VMware vSphere — primary with some Hyper-V",
         "Mixed — VMware, Hyper-V, and/or KVM",
         "Hyper-V primary",
         "KVM / other"],
        key="current_hypervisor"
    )

    microsoft_investment = st.selectbox(
        "How deeply invested is the organization in Microsoft?",
        ["-- Select --", "Heavy — Azure, M365, SQL Server, Active Directory everywhere",
         "Moderate — M365 and some Azure usage",
         "Light — primarily on-prem Microsoft products",
         "Minimal — mostly non-Microsoft stack"],
        key="microsoft_investment"
    )

with col6:
    redhat_investment = st.selectbox(
        "Is Red Hat already in the environment?",
        ["-- Select --", "Yes — RHEL is the primary Linux distro",
         "Yes — RHEL plus Ansible automation",
         "Yes — OpenShift already running",
         "Minimal — some RHEL but not strategic",
         "No — not a Red Hat shop"],
        key="redhat_investment"
    )

    nutanix_investment = st.selectbox(
        "Is Nutanix already in the environment?",
        ["-- Select --", "Yes — Nutanix is already deployed",
         "Yes — evaluating Nutanix alongside other options",
         "No — not currently in use"],
        key="nutanix_investment"
    )

st.divider()

# ── Section 4: Operational Profile ───────────────────────────────
st.subheader("4️⃣ Operational Profile")
col7, col8 = st.columns(2)

with col7:
    team_skillset = st.selectbox(
        "What best describes the infrastructure team's skill set?",
        ["-- Select --", "VMware admins — strong vSphere, limited Linux/containers",
         "Mixed — VMware plus some Linux and scripting",
         "Linux/DevOps focused — comfortable with CLI and automation",
         "Microsoft focused — Windows, PowerShell, Azure",
         "Generalist — broad but not deep in any one area"],
        key="team_skillset"
    )

    change_appetite = st.selectbox(
        "What is the appetite for operational change?",
        ["-- Select --", "Minimal — prefer familiar tools and low disruption",
         "Moderate — willing to retrain but want a clear path",
         "High — open to significant change if the outcome is better",
         "Aggressive — want to modernize everything"],
        key="change_appetite"
    )

with col8:
    managed_services = st.selectbox(
        "Is there interest in managed services?",
        ["-- Select --", "Yes — prefer fully managed private cloud",
         "Yes — co-managed model (we do some, partner does some)",
         "No — want to own and operate internally",
         "Undecided"],
        key="managed_services"
    )

    security_priority = st.selectbox(
        "How important is integrated security and compliance?",
        ["-- Select --", "Critical — zero trust, microsegmentation, audit trails required",
         "Important — need better security than we have today",
         "Standard — basic compliance requirements",
         "Low — not a primary driver"],
        key="security_priority"
    )

st.divider()

# ── Section 5: Budget & Timeline ─────────────────────────────────
st.subheader("5️⃣ Budget & Timeline")
col9, col10 = st.columns(2)

with col9:
    capex_opex = st.selectbox(
        "What is the preferred spending model?",
        ["-- Select --", "CapEx preferred — own the hardware",
         "OpEx preferred — subscription / as-a-service",
         "Flexible — open to either",
         "Hybrid — CapEx for core, OpEx for flex capacity"],
        key="capex_opex"
    )

    budget_awareness = st.selectbox(
        "Is there budget awareness for this initiative?",
        ["-- Select --", "Yes — budget is approved and available",
         "Yes — budget is in planning for next fiscal year",
         "Needs justification — ROI must be demonstrated first",
         "No formal budget — exploratory only"],
        key="budget_awareness"
    )

with col10:
    vmware_renewal = st.selectbox(
        "Is there an upcoming VMware renewal driving urgency?",
        ["-- Select --", "Yes — renewal within 3 months",
         "Yes — renewal within 6 months",
         "Yes — renewal within 12 months",
         "No — renewal is 12+ months away",
         "No VMware renewal — greenfield or different hypervisor"],
        key="vmware_renewal"
    )

    decision_maker = st.selectbox(
        "Who is the primary decision maker for this initiative?",
        ["-- Select --", "CIO / CTO — board-level initiative",
         "VP / Director of Infrastructure",
         "IT Manager — operational decision",
         "CFO involved — primarily financial decision",
         "Committee — multiple stakeholders"],
        key="decision_maker"
    )

st.divider()

# ── Maturity Assessment ───────────────────────────────────────────
st.subheader("6️⃣ Private Cloud Maturity Assessment")
st.caption("Rate your current state honestly — this shapes the roadmap recommendation.")

col11, col12 = st.columns(2)

with col11:
    maturity_automation = st.slider(
        "Infrastructure automation maturity",
        1, 5, 2,
        help="1 = fully manual, 5 = fully automated IaC"
    )
    maturity_security = st.slider(
        "Security and compliance posture",
        1, 5, 2,
        help="1 = reactive, 5 = proactive zero trust"
    )
    maturity_monitoring = st.slider(
        "Monitoring and observability",
        1, 5, 2,
        help="1 = basic alerts, 5 = full stack observability"
    )

with col12:
    maturity_selfservice = st.slider(
        "Self-service and developer experience",
        1, 5, 1,
        help="1 = all manual tickets, 5 = full self-service portal"
    )
    maturity_lifecycle = st.slider(
        "Lifecycle management discipline",
        1, 5, 2,
        help="1 = ad hoc patching, 5 = automated lifecycle pipelines"
    )
    maturity_cost = st.slider(
        "Cost visibility and chargeback",
        1, 5, 1,
        help="1 = no visibility, 5 = full showback/chargeback"
    )

overall_maturity = round((maturity_automation + maturity_security +
                          maturity_monitoring + maturity_selfservice +
                          maturity_lifecycle + maturity_cost) / 6, 1)

if overall_maturity < 2:
    maturity_label = "Foundation — significant modernization opportunity"
    maturity_color = "error"
elif overall_maturity < 3.5:
    maturity_label = "Developing — good baseline, ready to accelerate"
    maturity_color = "warning"
else:
    maturity_label = "Advanced — ready for private cloud acceleration"
    maturity_color = "success"

if maturity_color == "error":
    st.error(f"Overall Maturity Score: {overall_maturity}/5 — {maturity_label}")
elif maturity_color == "warning":
    st.warning(f"Overall Maturity Score: {overall_maturity}/5 — {maturity_label}")
else:
    st.success(f"Overall Maturity Score: {overall_maturity}/5 — {maturity_label}")

st.divider()

# ── Save and Score ────────────────────────────────────────────────
if st.button("Save Discovery & Calculate Fit Scores", type="primary"):

    discovery = {
        'primary_driver': primary_driver,
        'app_strategy': app_strategy,
        'time_horizon': time_horizon,
        'vendor_consolidation': vendor_consolidation,
        'kubernetes': kubernetes,
        'dev_methodology': dev_methodology,
        'ai_ml': ai_ml,
        'workload_sensitivity': workload_sensitivity,
        'current_hypervisor': current_hypervisor,
        'microsoft_investment': microsoft_investment,
        'redhat_investment': redhat_investment,
        'nutanix_investment': nutanix_investment,
        'team_skillset': team_skillset,
        'change_appetite': change_appetite,
        'managed_services': managed_services,
        'security_priority': security_priority,
        'capex_opex': capex_opex,
        'budget_awareness': budget_awareness,
        'vmware_renewal': vmware_renewal,
        'decision_maker': decision_maker,
        'maturity': {
            'automation': maturity_automation,
            'security': maturity_security,
            'monitoring': maturity_monitoring,
            'selfservice': maturity_selfservice,
            'lifecycle': maturity_lifecycle,
            'cost': maturity_cost,
            'overall': overall_maturity,
            'label': maturity_label,
        }
    }

    # ── Fit scoring adjustments based on discovery ────────────────
    fit_adjustments = {
        'VMware VCF': 0,
        'Nutanix': 0,
        'Red Hat OpenShift': 0,
        'Azure Stack HCI': 0,
    }

    # Current hypervisor
    if current_hypervisor == "VMware vSphere — all in":
        fit_adjustments['VMware VCF'] += 30
        fit_adjustments['Nutanix'] -= 10
    elif current_hypervisor == "Hyper-V primary":
        fit_adjustments['Azure Stack HCI'] += 20

    # Kubernetes/containers
    if kubernetes in ["Yes — already running in production",
                      "Yes — actively planning deployment"]:
        fit_adjustments['Red Hat OpenShift'] += 35
        fit_adjustments['VMware VCF'] += 10
    elif kubernetes == "Evaluating — interested but not committed":
        fit_adjustments['Red Hat OpenShift'] += 15

    # Microsoft investment
    if microsoft_investment == "Heavy — Azure, M365, SQL Server, Active Directory everywhere":
        fit_adjustments['Azure Stack HCI'] += 30
        fit_adjustments['VMware VCF'] += 5
    elif microsoft_investment == "Moderate — M365 and some Azure usage":
        fit_adjustments['Azure Stack HCI'] += 15

    # Red Hat investment
    if redhat_investment == "Yes — OpenShift already running":
        fit_adjustments['Red Hat OpenShift'] += 40
    elif redhat_investment in ["Yes — RHEL is the primary Linux distro",
                               "Yes — RHEL plus Ansible automation"]:
        fit_adjustments['Red Hat OpenShift'] += 20

    # Nutanix investment
    if nutanix_investment == "Yes — Nutanix is already deployed":
        fit_adjustments['Nutanix'] += 35
    elif nutanix_investment == "Yes — evaluating Nutanix alongside other options":
        fit_adjustments['Nutanix'] += 15

    # Team skillset
    if team_skillset == "VMware admins — strong vSphere, limited Linux/containers":
        fit_adjustments['VMware VCF'] += 25
        fit_adjustments['Red Hat OpenShift'] -= 15
    elif team_skillset == "Linux/DevOps focused — comfortable with CLI and automation":
        fit_adjustments['Red Hat OpenShift'] += 20
        fit_adjustments['Nutanix'] += 10
    elif team_skillset == "Microsoft focused — Windows, PowerShell, Azure":
        fit_adjustments['Azure Stack HCI'] += 25

    # Change appetite
    if change_appetite == "Minimal — prefer familiar tools and low disruption":
        fit_adjustments['VMware VCF'] += 20
        fit_adjustments['Red Hat OpenShift'] -= 20
    elif change_appetite in ["High — open to significant change if the outcome is better",
                             "Aggressive — want to modernize everything"]:
        fit_adjustments['Red Hat OpenShift'] += 15
        fit_adjustments['Nutanix'] += 10

    # Dev methodology
    if dev_methodology in ["DevSecOps — security integrated into pipelines",
                           "Platform engineering — internal developer platform"]:
        fit_adjustments['Red Hat OpenShift'] += 25
    elif dev_methodology == "DevOps — some automation and pipelines":
        fit_adjustments['Red Hat OpenShift'] += 10
        fit_adjustments['Nutanix'] += 5

    # AI/ML
    if ai_ml in ["Yes — active AI/ML initiative needing on-prem GPU",
                 "Yes — planning private AI for data sovereignty"]:
        fit_adjustments['VMware VCF'] += 15
        fit_adjustments['Nutanix'] += 10
        fit_adjustments['Red Hat OpenShift'] += 10

    # App strategy
    if app_strategy == "Cloud-native first — containers and microservices":
        fit_adjustments['Red Hat OpenShift'] += 25
        fit_adjustments['VMware VCF'] -= 10
    elif app_strategy == "Lift and shift — move as-is":
        fit_adjustments['VMware VCF'] += 20
        fit_adjustments['Nutanix'] += 10

    # CapEx/OpEx
    if capex_opex == "OpEx preferred — subscription / as-a-service":
        fit_adjustments['Azure Stack HCI'] += 10
        fit_adjustments['Red Hat OpenShift'] += 10

    # VMware renewal urgency
    if vmware_renewal in ["Yes — renewal within 3 months",
                          "Yes — renewal within 6 months"]:
        fit_adjustments['VMware VCF'] += 15
        discovery['renewal_urgency'] = 'high'
    elif vmware_renewal == "Yes — renewal within 12 months":
        fit_adjustments['VMware VCF'] += 8
        discovery['renewal_urgency'] = 'medium'
    else:
        discovery['renewal_urgency'] = 'low'

    discovery['fit_adjustments'] = fit_adjustments
    st.session_state.discovery = discovery

    st.success("✅ Discovery saved! Fit scores updated based on your responses.")

    # Show score adjustments
    st.subheader("Fit Score Adjustments from Discovery")
    cols = st.columns(4)
    platforms = ['VMware VCF', 'Nutanix', 'Red Hat OpenShift', 'Azure Stack HCI']
    for i, platform in enumerate(platforms):
        adj = fit_adjustments[platform]
        with cols[i]:
            if adj > 0:
                st.success(f"**{platform}**\n\n+{adj} points")
            elif adj < 0:
                st.error(f"**{platform}**\n\n{adj} points")
            else:
                st.info(f"**{platform}**\n\nNeutral")

    st.divider()
    st.info("👈 Continue to **VMware Renewal Analyzer** or skip to **Current State TCO** in the sidebar.")

elif st.session_state.discovery:
    st.success("✅ Discovery previously saved. Scroll down to review or update your answers and re-save.")