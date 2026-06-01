import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import time

# --- STYLING & CONFIGURATION ---
st.set_page_config(
    page_title="Optum Next-Gen Core Infrastructure Platforms",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Integrated BFSI/Healthcare Platform
st.markdown("""
    <style>
    .reportview-container { background-color: #F8FAFC; }
    .agent-card {
        background-color: #FFFFFF; padding: 16px; border-radius: 8px;
        border-left: 5px solid #0D9488; margin-bottom: 12px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }
    .agent-card-alert { border-left: 5px solid #D97706; }
    .agent-card-critical { border-left: 5px solid #EF4444; }
    .agent-header { font-weight: 600; font-size: 1.1rem; color: #1E293B; margin-bottom: 4px; }
    .agent-status { font-size: 0.85rem; font-weight: 500; padding: 2px 8px; border-radius: 12px; float: right; }
    .status-complete { background-color: #CCFBF1; color: #0D9488; }
    .status-alert { background-color: #FEF3C7; color: #D97706; }
    .status-critical { background-color: #FEE2E2; color: #EF4444; }
    .status-idle { background-color: #E2E8F0; color: #64748B; }
    .red-team-box { background-color: #FFF5F5; border: 1px solid #FEB2B2; border-radius: 8px; padding: 16px; margin-top: 15px; }
    .negotiation-box { background-color: #EFF6FF; border: 1px solid #BFDBFE; border-radius: 8px; padding: 20px; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# Initialize global state variables
if "repair_applied" not in st.session_state:
    st.session_state["repair_applied"] = False
if "negotiation_settled" not in st.session_state:
    st.session_state["negotiation_settled"] = False

# --- SHARED REPOSITORY MOCK DATA ---
CASES = {
    "Case #8821: Lumbar Fusion Exception / Mercy General": {
        "text": "Patient presents with persistent L4-L5 disc degeneration. Completed 12+ weeks of physical therapy without significant resolution. Visualized narrowing on imaging. Requesting authorization for lumbar fusion inpatient stay (3 days estimated).",
        "codes": [
            {"Type": "ICD-10", "Code": "M51.36", "Description": "Other disc degeneration, lumbar", "Confidence": "99%"},
            {"Type": "CPT", "Code": "22612", "Description": "Arthrodesis, posterior single level; lumbar", "Confidence": "97%"},
            {"Type": "DRG", "Code": "460", "Description": "Spinal Fusion Except Cervical", "Confidence": "94%"}
        ],
        "repair_text": "Pre-operative MRI confirms severe L4-L5 disc space narrowing exceeding 25% with associated mechanical instability.",
        "red_team_alert": "Human Payer Reviewer or automated rules engine will likely trigger an automatic denial due to incomplete documentation of precise interspace narrowing thresholds under InterQual criteria #4.",
        "billing_total": 24500.00,
        "corrected_total": 18450.00,
        "integrity_issue": "High-cost specialty infusion billed as an unbundled asset without localized supporting historical markers."
    }
}

# --- UNIFIED SIDEBAR NAVIGATION ---
st.sidebar.image("https://www.optum.com/content/dam/optum4/images/logo/optum-logo.svg", width=150)
st.sidebar.markdown("### **Optum Platform Navigator**")

# The Core Integration Switch
app_mode = st.sidebar.radio(
    "Select Operational Workflow Suite:",
    ["1. Zero-Touch Prior Auth Copilot (Provider-Side)", "2. Claims Integrity War Room (Payer-Side)"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### **Active Ingestion Layer**")
selected_case_name = st.sidebar.selectbox("Active Case Target:", list(CASES.keys()))
case_data = CASES[selected_case_name]

# ==========================================
# MODULE 1: PRIOR AUTHORIZATION COPILOT
# ==========================================
if "1." in app_mode:
    st.title("🛡️ Zero-Touch Prior Authorization Copilot")
    st.markdown("##### *EHR-Embedded Pre-Submission Autonomy & Litigation Shield*")
    st.markdown("---")
    
    enable_red_team = st.sidebar.toggle("Activate Adversarial Simulation", value=True)
    run_auth = st.sidebar.button("Run Pre-Auth Analysis Pipeline", type="primary", use_container_width=True)
    
    col1, col2, col3 = st.columns([2.5, 4, 3.5])
    
    with col1:
        st.markdown("### 📥 Document Ingest & Mapping")
        st.caption("Ambient notes translation stream.")
        provider_notes = st.text_area("Narrative Context Extract", value=case_data["text"], height=160)
        st.dataframe(pd.DataFrame(case_data["codes"]), use_container_width=True, hide_index=True)
        
    with col2:
        st.markdown("### ⚙️ Autonomous Agent Swarm")
        auth_status = "complete" if run_auth else "idle"
        
        st.markdown(f'<div class="agent-card"><span class="agent-status status-{auth_status}">{auth_status.upper()}</span><div class="agent-header">🧠 Clinical Reasoning Agent</div><div style="font-size:0.9rem; color:#475569;">Verified conservative therapy durations (>12 weeks).</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agent-card agent-card-alert"><span class="agent-status {"status-alert" if run_auth else "status-idle"}">{"ALERT" if run_auth else "IDLE"}</span><div class="agent-header">🔍 Evidence Validator Agent</div><div style="font-size:0.9rem; color:#475569;">Flagged structural variance gap in raw documentation text template.</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agent-card"><span class="agent-status status-{auth_status}">{auth_status.upper()}</span><div class="agent-header">📋 Policy Matching Agent</div><div style="font-size:0.9rem; color:#475569;">Aligned criteria payloads with active InterQual Lumbar Fusion guidelines.</div></div>', unsafe_allow_html=True)
        
        if enable_red_team and run_auth:
            st.markdown(f'<div class="red-team-box"><span style="color:#DC2626; font-weight:bold; font-size:0.9rem;">⚠️ ADVERSARIAL RED-TEAM PREDICTION</span><p style="font-size:0.88rem; color:#991B1B; margin-top:4px;">{case_data["red_team_alert"]}</p></div>', unsafe_allow_html=True)
            repaired_input = st.text_input("AI Proposed Autonomous Narrative Correction:", value=case_data["repair_text"])
            
            if st.button("Apply Repair & Secure Outcome Guarantee", type="secondary", use_container_width=True):
                st.session_state["repair_applied"] = True
                
            if st.session_state["repair_applied"]:
                st.toast("✅ Clinical narrative reinforced! Security payload re-verified.")
                st.success("Prior-Authorization target submission package fortified against downstream denial risk patterns.")
                st.session_state["repair_applied"] = False

    with col3:
        st.markdown("### 📊 Pre-Auth Metrics Matrix")
        m1, m2 = st.columns(2)
        m1.metric("First-Pass Approval Guarantee", "96.4%", "+16% Lift")
        m2.metric("Manual Touch Reduction", "65%", "Autonomous")
        st.markdown("---")
        ledger_data = {
            "Lifecycle Phase": ["Entity Extraction", "Criteria Match", "Adversarial Check"],
            "Evidence Anchor": ["EHR Page 2 Line 14", "PT Logs Attached", "InterQual Sec 4"],
            "Human Override": ["No", "No", "No"]
        }
        st.dataframe(pd.DataFrame(ledger_data), use_container_width=True, hide_index=True)
        st.warning("🔒 **Compliance Operational Lock:** AI platform cannot execute silent absolute denials. Fallbacks drop cleanly to Human Reviewers.")

# ==========================================
# MODULE 2: CLAIMS INTEGRITY WAR ROOM
# ==========================================
else:
    st.title("🛰️ Claims Integrity War Room")
    st.markdown("##### *Upstream Payment Leakage Defense & Real-Time Collaborative Adjudication*")
    st.markdown("---")
    
    run_integrity = st.sidebar.button("Execute Upstream Claim Scans", type="primary", use_container_width=True)
    
    # Financial Leakage Macro Metric Banner
    b1, b2, b3, b4 = st.columns(4)
    b1.metric("Financial Leakage Prevented", "$4.2M YTD", "+34.2% Savings")
    b2.metric("Provider Appeals Lowered", "-58.0%", "Upstream Correction")
    b3.metric("Payer Processing Latency", "1.4 Mins", "Real-Time Adjudication")
    b4.metric("Provider Friction Index", "Low Risk", "Collaboration Model")
    st.markdown("---")
    
    col1_claim, col2_claim = st.columns([5, 5])
    
    with col1_claim:
        st.markdown("### 🕸️ Live Clinical Truth Graph")
        st.caption("Reconstructed relational data node maps analyzed prior to checkout validation.")
        
        # Render a Live Interactive Plotly Node Chart to model technical depth
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=[1, 2, 2.5, 1.5, 3], y=[2, 3.5, 2, 1, 3],
            mode='markers+text',
            marker=dict(size=[30, 40, 45, 30, 40], color=['#0F172A', '#0D9488', '#EF4444', '#64748B', '#D97706']),
            text=['Patient', 'Hospital: Mercy', 'Anomalous Infusion', 'Diagnosis: Spine', 'Modifier 25'],
            textposition="top center"
        ))
        fig.update_layout(showlegend=False, height=240, margin=dict(b=0,l=0,r=0,t=0), xaxis=dict(visible=False), yaxis=dict(visible=False))
        st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("**Swarm Intelligence Inspection Stream:**")
        int_status = "critical" if run_integrity else "idle"
        st.markdown(f'<div class="agent-card agent-card-critical"><span class="agent-status status-{int_status}">{int_status.upper()}</span><div class="agent-header">⛓️ Clinical Consistency Agent</div><div style="font-size:0.9rem; color:#475569;">{case_data["integrity_issue"] if run_integrity else "Awaiting platform validation trigger..."}</div></div>', unsafe_allow_html=True)
        st.markdown(f'<div class="agent-card"><span class="agent-status {"status-complete" if run_integrity else "status-idle"}">{"COMPLETE" if run_integrity else "IDLE"}</span><div class="agent-header">💳 Payment Integrity Agent</div><div style="font-size:0.9rem; color:#475569;">Unbundling detection routines finalized across submitted line arrays.</div></div>', unsafe_allow_html=True)

    with col2_claim:
        st.markdown("### 🤝 Real-Time AI Negotiation Interface")
        st.caption("Resolving transactional billing conflicts via transparent structural corrections.")
        
        if run_integrity:
            st.markdown(f"""
            <div class="negotiation-box">
                <h4 style="color:#1E3A8A; margin-top:0;">Optum Interactive Correction Proposal</h4>
                <p style="font-size:0.92rem; color:#1E40AF;">Anomalous line items matching compliance failure patterns detected under CMS Code Guideline Mandate Section 12.</p>
                <hr style="border:0; border-top:1px solid #93C5FD; margin:12px 0;">
                <table style="width:100%; font-size:0.9rem; color:#1E40AF;">
                    <tr><td><b>Original Gross Submission:</b></td><td style="text-align:right; color:#EF4444; font-weight:bold;">${case_data["billing_total"]:,.2f}</td></tr>
                    <tr><td><b>Automated Structural Alignment (Bundled Valuation):</b></td><td style="text-align:right; color:#10B981; font-weight:bold;">${case_data["corrected_total"]:,.2f}</td></tr>
                </table>
                <p style="font-size:0.82rem; color:#1E40AF; margin-top:10px;">💡 <b>Value Proposition:</b> Accepting this auto-correction updates remittances immediately, fast-tracking payments within 24 hours while dropping processing appeal constraints to 0%.</p>
            </div>
            """, unsafe_allow_html=True)
            
            nb1, nb2 = st.columns(2)
            if nb1.button("Accept Corrected Remittance", type="primary", use_container_width=True):
                st.session_state["negotiation_settled"] = True
            nb2.button("Escalate to SIU Investigator Pool", type="secondary", use_container_width=True)
            
            if st.session_state["negotiation_settled"]:
                st.success(f"Transaction successfully adjudicated at adjusted settlement tier of ${case_data['corrected_total']:,.2f}. Ledger updated.")
                st.session_state["negotiation_settled"] = False
        else:
            st.info("Trigger the upstream claim scan inside the control panel to populate real-time integrity assessments and launch peer resolution loops.")
