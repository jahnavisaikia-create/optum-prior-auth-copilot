import streamlit as st
import pandas as pd
import time

# --- STYLING & CONFIGURATION ---
st.set_page_config(
    page_title="Optum Zero-Touch Prior Auth Copilot",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Enterprise Clinical Design System
st.markdown("""
    <style>
    /* Main layout adjustments */
    .reportview-container { background-color: #F8FAFC; }
    
    /* Custom Card Styles */
    .agent-card {
        background-color: #FFFFFF;
        padding: 16px;
        border-radius: 8px;
        border-left: 5px solid #0D9488;
        margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .agent-card-alert {
        border-left: 5px solid #D97706;
    }
    .agent-header {
        font-weight: 600;
        font-size: 1.1rem;
        color: #1E293B;
        margin-bottom: 4px;
    }
    .agent-status {
        font-size: 0.85rem;
        font-weight: 500;
        padding: 2px 8px;
        border-radius: 12px;
        float: right;
    }
    .status-complete { background-color: #CCFBF1; color: #0D9488; }
    .status-alert { background-color: #FEF3C7; color: #D97706; }
    .status-idle { background-color: #E2E8F0; color: #64748B; }
    
    /* Adversarial Box */
    .red-team-box {
        background-color: #FFF5F5;
        border: 1px solid #FEB2B2;
        border-radius: 8px;
        padding: 16px;
        margin-top: 15px;
    }
    </style>
    """, unsafe_allowed_html=True)

# --- MOCK DATA ---
CASES = {
    "Case #8821: Lumbar Fusion Exception": {
        "text": "Patient presents with persistent L4-L5 disc degeneration. Completed 12+ weeks of physical therapy without significant resolution. Visualized narrowing on imaging. Requesting authorization for lumbar fusion inpatient stay (3 days estimated).",
        "codes": [
            {"Type": "ICD-10", "Code": "M51.36", "Description": "Other intervertebral disc degeneration, lumbar region", "Match Confidence": "99%"},
            {"Type": "CPT", "Code": "22612", "Description": "Arthrodesis, posterior technique, single level; lumbar", "Match Confidence": "97%"},
            {"Type": "DRG", "Code": "460", "Description": "Spinal Fusion Except Cervical Without MCC", "Match Confidence": "94%"}
        ],
        "repair_text": "Pre-operative MRI confirms severe L4-L5 disc space narrowing exceeding 25% with associated mechanical instability.",
        "red_team_alert": "Human Payer Reviewer or automated rules engine will likely trigger an automatic denial due to incomplete documentation of precise interspace narrowing thresholds under InterQual criteria #4."
    },
    "Case #4112: Inpatient Cardiology Validation": {
        "text": "65yo male presenting with accelerating exertional chest pain. Stress test shows reversible ischemia in LAD territory. Scheduled for urgent diagnostic cardiac cath with possible PCI. Requesting inpatient tracking window.",
        "codes": [
            {"Type": "ICD-10", "Code": "I20.0", "Description": "Unstable angina pectoris", "Match Confidence": "98%"},
            {"Type": "CPT", "Code": "93454", "Description": "Cardiography injection procedures during cardiac cath", "Match Confidence": "95%"},
            {"Type": "DRG", "Code": "286", "Description": "Circulatory Disorders Except AMI, With Cath", "Match Confidence": "91%"}
        ],
        "repair_text": "EHR extraction confirms dynamic ST-segment depressions on presentation and Troponin I elevation of 0.45 ng/mL.",
        "red_team_alert": "CMS mandate cross-reference flags insufficient documentation of biomarker trending to warrant acute inpatient vs observational care status."
    }
}

# --- SIDEBAR CONTROL PANEL ---
st.sidebar.image("https://www.optum.com/content/dam/optum4/images/logo/optum-logo.svg", width=150)
st.sidebar.markdown("### **EHR Intake & Control Panel**")
st.sidebar.markdown("---")

selected_case_name = st.sidebar.selectbox("Select Target Patient Case File:", list(CASES.keys()))
case_data = CASES[selected_case_name]

st.sidebar.markdown("### **Ingestion Pipeline**")
uploaded_file = st.sidebar.file_uploader("Upload Supporting PDF/Fax Evidence", type=["pdf", "tiff", "png"])
if uploaded_file:
    st.sidebar.success(f"Successfully staged: {uploaded_file.name}")

st.sidebar.markdown("---")
enable_red_team = st.sidebar.toggle("Enable Adversarial Red-Teaming Simulation", value=True)
run_pipeline = st.sidebar.button("Execute Autonomous Copilot Analysis", type="primary", use_container_width=True)

# --- MAIN DASHBOARD INTERFACE ---
st.title("🛡️ Zero-Touch Prior Authorization Copilot")
st.markdown("##### *Autonomous Exception Resolution Framework for Digital Auth Complete*")
st.markdown("---")

# Layout Matrix Configuration
col1, col2, col3 = st.columns([2.5, 4, 3.5])

# --- COLUMN 1: INTAKE CONTEXT & EXTRACTION ---
with col1:
    st.markdown("### 📥 Document Ingest & Mapping")
    st.caption("Ambient intelligence stream and semantic clinical translation.")
    
    st.markdown("**Raw EHR Narrative Extraction:**")
    provider_notes = st.text_area(
        label="Provider Notes Context Window",
        value=case_data["text"],
        height=150,
        label_visibility="collapsed"
    )
    
    st.markdown("**Real-Time Clinical Entity Mapping:**")
    df_codes = pd.DataFrame(case_data["codes"])
    st.dataframe(df_codes, use_container_width=True, hide_index=True)

# --- COLUMN 2: MULTI-AGENT ORCHESTRATION PANEL ---
with col2:
    st.markdown("### ⚙️ Autonomous Agent Orchestration Matrix")
    st.caption("Live agent-swarm evaluating medical necessity policies.")
    
    # Simple state handling for demo simulation
    if run_pipeline:
        with st.spinner("Orchestrating agents and querying policy vectors..."):
            time.sleep(1)
        a1_status, a2_status, a3_status = "complete", "alert", "complete"
    else:
        a1_status, a2_status, a3_status = "idle", "idle", "idle"

    # Agent Card 1: Clinical Reasoning
    c1_class = "status-complete" if a1_status == "complete" else "status-idle"
    st.markdown(f"""
    <div class="agent-card">
        <span class="agent-status {c1_class}">{a1_status.upper()}</span>
        <div class="agent-header">🧠 Clinical Reasoning Agent</div>
        <div style="font-size: 0.9rem; color: #475569;">
            { "Validated criteria met: Failed conservative therapy history documented (>12 weeks)." if a1_status == 'complete' else 'Waiting for execution trigger...' }
        </div>
    </div>
    """, unsafe_allowed_html=True)

    # Agent Card 2: Evidence Validator
    c2_class = "status-alert" if a2_status == "alert" else "status-idle"
    c2_border = "agent-card-alert" if a2_status == "alert" else ""
    st.markdown(f"""
    <div class="agent-card {c2_border}">
        <span class="agent-status {c2_class}">{a2_status.upper()}</span>
        <div class="agent-header">🔍 Evidence Validator Agent</div>
        <div style="font-size: 0.9rem; color: #475569;">
            { "Anomaly Identified: Missing explicit numeric metrics for targeted structural changes in primary chart text." if a2_status == 'alert' else 'Waiting for execution trigger...' }
        </div>
    </div>
    """, unsafe_allowed_html=True)

    # Agent Card 3: Policy Matching
    c3_class = "status-complete" if a3_status == "complete" else "status-idle"
    st.markdown(f"""
    <div class="agent-card">
        <span class="agent-status {c3_class}">{a3_status.upper()}</span>
        <div class="agent-header">📋 Policy Matching Agent</div>
        <div style="font-size: 0.9rem; color: #475569;">
            { "Cross-referencing complete. Mapped to localized InterQual / Medicare Advantage guidelines." if a3_status == 'complete' else 'Waiting for execution trigger...' }
        </div>
    </div>
    """, unsafe_allowed_html=True)

    # Adversarial Red-Teaming Logic Interventions
    if enable_red_team and run_pipeline:
        st.markdown(f"""
        <div class="red-team-box">
            <span style="color: #DC2626; font-weight: bold; font-size: 0.9rem;">⚠️ ADVERSARIAL RED-TEAM PREDICTION</span>
            <p style="font-size: 0.88rem; color: #991B1B; margin-top: 4px; margin-bottom: 8px;">
                {case_data["red_team_alert"]}
            </p>
        </div>
        """, unsafe_allowed_html=True)
        
        st.markdown("<br>", unsafe_allowed_html=True)
        st.markdown("**AI Proposed Autonomous Correction (Pre-submission Repair):**")
        repaired_input = st.text_input(
            "Suggested text injection to prevent downstream denial:",
            value=case_data["repair_text"]
        )
        
        if st.button("Apply Repair & Secure Outcome Guarantee", type="secondary", use_container_width=True):
            st.toast("Clinical narrative reinforced! Security payload re-verified.", icon="✅")

# --- COLUMN 3: AUDIT TRAIL & OPERATIONAL IMPACT ---
with col3:
    st.markdown("### 📊 Metrics & Compliance Ledger")
    st.caption("Defensible analytics tracking audit compliance profiles.")
    
    # Strategic High-Level Metrics Row
    m_col1, m_col2 = st.columns(2)
    with m_col1:
        st.metric(label="First-Pass Approval Rate", value="96.4%", delta="+16.4% vs Baseline")
        st.metric(label="Incomplete Data Denials", value="-80.0%", delta="System Defended")
    with m_col2:
        st.metric(label="Manual Touches Saved", value="65.2%", delta="Autonomous Shift")
        st.metric(label="Reviewer Efficiency", value="+45.0%", delta="Nurse Lift")
        
    st.markdown("---")
    st.markdown("**CMS & Medicare Advantage Traceability Ledger:**")
    
    # Explicit Transaction Ledger DataFrame
    ledger_data = {
        "Lifecycle Phase": ["Entity Extraction", "Criteria Match", "Adversarial Check", "Repair Engine"],
        "Evidence Anchor": ["EHR Page 2 Line 14", "PT Logs Attached", "InterQual Sec 4", "Model Self-Audit Log"],
        "Regulatory Ref": ["CMS-0057 Core", "NCD 150.3", "MA Guidelines", "CMS Compliance Lock"],
        "Human Trigger": ["No", "No", "No", "Yes (Override Approved)"]
    }
    st.dataframe(pd.DataFrame(ledger_data), use_container_width=True, hide_index=True)
    
    st.warning("🔒 **Compliance Operational Lock:** AI is hard-coded to be structurally incapable of issuing an autonomous denial. Low-confidence flags auto-escalate to Human Medical Directors to guarantee litigation defense.")
