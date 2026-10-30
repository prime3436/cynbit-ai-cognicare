import streamlit as st
import os
import json
from PIL import Image
import pandas as pd
import plotly.express as px

from core.models import TriageRequest, SeverityLevel, DefectCategory
from core.agent import CogniCareAgent
from core.benchmarks import create_radar_chart, create_cost_latency_chart, get_benchmark_dataframe

st.set_page_config(
    page_title="TenantEase CogniCare",
    page_icon="🏢",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main {
        background-color: #0b0f19;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid #334155;
        border-radius: 12px;
        padding: 16px 20px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.3);
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #38bdf8;
    }
    .metric-label {
        font-size: 13px;
        color: #94a3b8;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    .badge-p1 {
        background-color: #ef4444;
        color: white;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 12px;
    }
    .badge-p2 {
        background-color: #f59e0b;
        color: black;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 12px;
    }
    .badge-p3 {
        background-color: #3b82f6;
        color: white;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 12px;
    }
    .badge-p4 {
        background-color: #10b981;
        color: white;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 12px;
    }
    .hazard-banner {
        background: rgba(239, 68, 68, 0.15);
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 14px;
        color: #fca5a5;
        font-weight: 500;
        margin-bottom: 15px;
    }
    .contractor-card {
        background: #1e293b;
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 14px;
        margin-top: 10px;
    }
</style>
""", unsafe_allow_html=True)

if "agent" not in st.session_state:
    st.session_state.agent = CogniCareAgent()

if "history" not in st.session_state:
    st.session_state.history = [
        {
            "ticket_id": "TICK-20261028-A81F0",
            "timestamp": "2026-10-28 14:12:00",
            "unit_id": "Building-C / Flat 304",
            "tenant_name": "Arjun Sharma",
            "category": "Plumbing",
            "severity": "P1_CRITICAL",
            "summary_title": "Burst Copper Supply Pipe Under Sink",
            "contractor": "Apex Flow Dynamics & Rapid Plumbing",
            "status": "Dispatched (In Progress)",
            "cost_inr": 4800,
            "sla_hours": 2
        },
        {
            "ticket_id": "TICK-20261029-E44C2",
            "timestamp": "2026-10-29 09:35:10",
            "unit_id": "Tower-1 / Penthouse A",
            "tenant_name": "Priya Nair",
            "category": "HVAC / Climate Control",
            "severity": "P2_HIGH",
            "summary_title": "AC Compressor Locked - Error Code E4",
            "contractor": "CoolAir Tech & Climate Services",
            "status": "Resolved (Contractor Signed-off)",
            "cost_inr": 3400,
            "sla_hours": 6
        },
        {
            "ticket_id": "TICK-20261029-B1109",
            "timestamp": "2026-10-29 18:22:45",
            "unit_id": "Building-B / Unit 102",
            "tenant_name": "Rohan Mehta",
            "category": "Electrical",
            "severity": "P1_CRITICAL",
            "summary_title": "Scorched 16A Geyser Socket Arcing",
            "contractor": "VoltGuard High-Voltage Engineering",
            "status": "Resolved",
            "cost_inr": 2900,
            "sla_hours": 2
        },
        {
            "ticket_id": "TICK-20261030-D991A",
            "timestamp": "2026-10-30 08:40:15",
            "unit_id": "Building-A / Unit 205",
            "tenant_name": "Neha Verma",
            "category": "General Maintenance",
            "severity": "P4_LOW",
            "summary_title": "Wardrobe Hinge Loose & Misaligned",
            "contractor": "UrbanFix Handyman Alliance",
            "status": "Scheduled",
            "cost_inr": 850,
            "sla_hours": 72
        }
    ]

with st.sidebar:
    st.image("https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=600&auto=format&fit=crop&q=80", use_container_width=True)
    st.title("TenantEase CogniCare")
    st.caption("Autonomous Property Operations Platform")
    
    st.divider()
    engine_mode = st.selectbox(
        "Inference Runtime",
        ["High-Throughput Reasoning Engine", "Multimodal Cloud API (Gemini 1.5 Flash)"],
        index=0
    )
    
    if "Gemini" in engine_mode:
        api_key_input = st.text_input("Gemini API Key", type="password")
        if api_key_input:
            os.environ["GEMINI_API_KEY"] = api_key_input
            st.session_state.agent = CogniCareAgent(use_llm_if_available=True)
    
    st.divider()
    st.markdown("""
    **Active Subsystems:**
    - Multimodal Defect Recognition
    - Sentinel Safety Isolation
    - Dynamic SLA Enforcement
    - Parts & Labor Scoping
    - Partner Dispatch Routing
    """)
    st.caption("Node: primary-us-east-1 (v2.4.0)")

st.title("TenantEase CogniCare: Autonomous Property Triage & SLA Dispatch")
st.markdown("Automated intake, safety triage, cost scoping, and certified contractor routing.")

tab1, tab2, tab3, tab4 = st.tabs([
    "Triage Portal",
    "Operations Watchtower",
    "Defect Analytics",
    "Benchmarks & System Design"
])

with tab1:
    col_input, col_output = st.columns([1, 1], gap="large")

    preset_cases = {
        "Preset 1: Emergency Burst Pipe Inundation (P1)": {
            "unit": "Tower B, Flat 402",
            "tenant": "Kavita Singhania",
            "desc": "URGENT! The cold water pipe under the kitchen sink burst and is violently spraying pressurized water all over the floor and baseboards! The water level is rising fast and pooling near the refrigerator wall socket!",
            "asset": "burst_pipe_leak.png",
            "urgency": "Emergency"
        },
        "Preset 2: Scorched Arcing Wall Socket (P1)": {
            "unit": "Building A, Suite 108",
            "tenant": "Vikram Seth",
            "desc": "There is a loud buzzing and crackling sound coming from the master bedroom 220V plug point. The plastic faceplate has turned black/brown and there is a burning acrid plastic smell with small sparks visible!",
            "asset": "electrical_sparking_outlet.png",
            "urgency": "Critical Hazard"
        },
        "Preset 3: HVAC Unit Error Code E4 & Warm Air (P2)": {
            "unit": "Penthouse 601",
            "tenant": "Ananya Roy",
            "desc": "The living room split AC has completely stopped blowing cold air during peak afternoon heat. The LED display is blinking error code 'E4' and there is water dripping down the interior wall paint.",
            "asset": "ac_compressor_failure.png",
            "urgency": "High"
        },
        "Preset 4: Bathroom Faucet Aerator Slow Drip (P4)": {
            "unit": "Studio 204",
            "tenant": "Devendra Joshi",
            "desc": "The guest washbasin faucet has a minor continuous drip even when shut tight. About one drop every few seconds. Not flooding, but creating mineral scale in the ceramic basin.",
            "asset": "minor_faucet_drip.png",
            "urgency": "Low / Routine"
        },
        "Custom Input": {
            "unit": "",
            "tenant": "",
            "desc": "",
            "asset": None,
            "urgency": "Normal"
        }
    }

    with col_input:
        st.markdown("#### Ticket Input")
        selected_case_name = st.selectbox("Select Test Scenario", list(preset_cases.keys()))
        selected_case = preset_cases[selected_case_name]

        unit_id = st.text_input("Unit / Apartment ID", value=selected_case["unit"] or "Unit-302, Green Valley")
        tenant_name = st.text_input("Tenant Full Name", value=selected_case["tenant"] or "Siddharth Malhotra")
        
        description = st.text_area(
            "Issue Description",
            value=selected_case["desc"],
            height=130
        )

        uploaded_file = st.file_uploader("Upload Defect Photo (Optional)", type=["png", "jpg", "jpeg"])
        
        loaded_image = None
        if uploaded_file is not None:
            loaded_image = Image.open(uploaded_file)
            st.image(loaded_image, caption="Uploaded Photo", use_container_width=True)
        elif selected_case["asset"]:
            asset_path = os.path.join(r"C:\Users\HP\cynbit-ai-cognicare\assets", selected_case["asset"])
            if os.path.exists(asset_path):
                loaded_image = Image.open(asset_path)
                st.image(loaded_image, caption=f"Preset Image: {selected_case['asset']}", use_container_width=True)

        triage_button = st.button("Run CogniCare Triage", type="primary", use_container_width=True)

    with col_output:
        st.markdown("#### Triage Result & Dispatch Plan")
        
        if triage_button and description:
            with st.spinner("Processing triage, hazard verification, and dispatch assignment..."):
                req = TriageRequest(
                    unit_id=unit_id,
                    tenant_name=tenant_name,
                    description=description,
                    has_image=bool(loaded_image),
                    urgency_claimed_by_tenant=selected_case["urgency"]
                )
                result = st.session_state.agent.triage(req, loaded_image)

                st.session_state.history.insert(0, {
                    "ticket_id": result.ticket_id,
                    "timestamp": result.timestamp,
                    "unit_id": result.unit_id,
                    "tenant_name": result.tenant_name,
                    "category": result.category.value,
                    "severity": result.severity.value,
                    "summary_title": result.summary_title,
                    "contractor": result.contractor_match.recommended_contractor,
                    "status": "Dispatch Triggered",
                    "cost_inr": (result.cost_estimate.min_cost_inr + result.cost_estimate.max_cost_inr) // 2,
                    "sla_hours": result.sla_hours
                })

                badge_class = {
                    SeverityLevel.P1_CRITICAL: "badge-p1",
                    SeverityLevel.P2_HIGH: "badge-p2",
                    SeverityLevel.P3_MEDIUM: "badge-p3",
                    SeverityLevel.P4_LOW: "badge-p4"
                }.get(result.severity, "badge-p3")

                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span style="font-family:monospace; color:#94a3b8;">Ticket #{result.ticket_id}</span>
                    <span class="{badge_class}">{result.severity.value} • SLA: &lt; {result.sla_hours}h</span>
                </div>
                """, unsafe_allow_html=True)

                st.subheader(result.summary_title)
                st.caption(f"Category: **{result.category.value}** | Confidence: **{result.confidence_score * 100:.1f}%**")

                if result.safety_guidance.hazard_detected:
                    st.markdown(f"""
                    <div class="hazard-banner">
                        ⚠️ <b>{result.safety_guidance.hazard_type}</b><br/>
                        {result.safety_guidance.warning_box or 'Immediate precautionary isolation required.'}
                    </div>
                    """, unsafe_allow_html=True)

                    st.markdown("**Required Tenant Actions:**")
                    for idx, step in enumerate(result.safety_guidance.immediate_action_steps, 1):
                        st.checkbox(f"**Step {idx}:** {step}", value=False, key=f"step_{idx}_{result.ticket_id}")

                with st.expander("Root-Cause Hypothesis", expanded=True):
                    st.write(result.root_cause_hypothesis)

                col_c1, col_c2 = st.columns(2)
                with col_c1:
                    st.metric(
                        "Estimated Cost Range",
                        f"₹{result.cost_estimate.min_cost_inr:,} - ₹{result.cost_estimate.max_cost_inr:,}",
                        delta=f"Labor: ~{result.cost_estimate.avg_labor_hours} hrs"
                    )
                with col_c2:
                    st.write("**Parts Required:**")
                    for p in result.cost_estimate.parts_likely_needed:
                        st.markdown(f"- `{p}`")

                st.markdown("#### Matched Contractor")
                st.markdown(f"""
                <div class="contractor-card">
                    <b>{result.contractor_match.recommended_contractor}</b><br/>
                    <span style="color:#94a3b8; font-size:13px;">Specialty: {result.contractor_match.specialty.value}</span><br/>
                    <span>ETA: <b>{result.contractor_match.eta_hours} hours</b> | Rate: <b>₹{result.contractor_match.estimated_rate_per_hour_inr}/hr</b></span><br/>
                    <span style="color:#10b981; font-size:12px;">✓ {result.contractor_match.matched_reason}</span>
                </div>
                """, unsafe_allow_html=True)

                with st.expander("Execution Trace"):
                    for trace in result.reasoning_trace:
                        st.markdown(f"- `{trace}`")
                    st.success(f"Audit Status: {result.audit_verdict}")

                json_str = result.model_dump_json(indent=2)
                st.download_button(
                    label="Export Work Order Payload (JSON)",
                    data=json_str,
                    file_name=f"work_order_{result.ticket_id}.json",
                    mime="application/json",
                    use_container_width=True
                )
        else:
            st.info("Select a test scenario or enter details to execute triage.")

with tab2:
    st.subheader("Operations Watchtower")
    st.markdown("Live queue monitoring across registered properties.")

    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Active Units</div>
            <div class="metric-value">1,420</div>
            <div style="color:#10b981; font-size:12px;">18 Properties Monitored</div>
        </div>
        """, unsafe_allow_html=True)
    with m2:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Avg Triage Latency</div>
            <div class="metric-value">1.4s</div>
            <div style="color:#10b981; font-size:12px;">vs 25m manual baseline</div>
        </div>
        """, unsafe_allow_html=True)
    with m3:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Emergency SLA Rate</div>
            <div class="metric-value">99.8%</div>
            <div style="color:#10b981; font-size:12px;">P1 Compliance</div>
        </div>
        """, unsafe_allow_html=True)
    with m4:
        st.markdown("""
        <div class="metric-card">
            <div class="metric-label">Monthly Savings</div>
            <div class="metric-value">₹3.42 L</div>
            <div style="color:#10b981; font-size:12px;">Preventative Scoping</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Active Tickets")
    df_history = pd.DataFrame(st.session_state.history)
    
    col_f1, col_f2 = st.columns([1, 2])
    with col_f1:
        sev_filter = st.multiselect("Severity Filter", options=df_history["severity"].unique(), default=df_history["severity"].unique())
    
    filtered_df = df_history[df_history["severity"].isin(sev_filter)]
    st.dataframe(
        filtered_df[[
            "ticket_id", "timestamp", "unit_id", "tenant_name", "category", "severity", "summary_title", "contractor", "status", "sla_hours"
        ]],
        use_container_width=True,
        hide_index=True
    )

with tab3:
    st.subheader("Defect Analytics")
    st.markdown("Portfolio maintenance patterns and lifecycle projections.")

    col_g1, col_g2 = st.columns(2)
    with col_g1:
        cat_counts = df_history["category"].value_counts().reset_index()
        cat_counts.columns = ["Category", "Count"]
        fig_pie = px.pie(
            cat_counts,
            values="Count",
            names="Category",
            hole=0.45,
            title="Defect Breakdown by Trade",
            color_discrete_sequence=px.colors.qualitative.Prism,
            template="plotly_dark"
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    with col_g2:
        ages = [1, 2, 3, 5, 7, 10, 12, 15]
        costs = [4500, 5200, 6800, 11500, 18400, 27000, 39500, 58000]
        preventative = [4000, 4200, 4800, 6200, 8100, 11000, 14200, 18500]
        
        df_cost = pd.DataFrame({
            "Building Age (Years)": ages,
            "Unmanaged Maintenance (INR)": costs,
            "CogniCare Preventative (INR)": preventative
        })
        fig_line = px.line(
            df_cost,
            x="Building Age (Years)",
            y=["Unmanaged Maintenance (INR)", "CogniCare Preventative (INR)"],
            markers=True,
            title="Maintenance Cost Over Building Lifecycle",
            template="plotly_dark"
        )
        st.plotly_chart(fig_line, use_container_width=True)

    st.markdown("### Risk Hotspots")
    heatmap_data = {
        "Property Wing": ["Tower A - North", "Tower A - South", "Tower B - East", "Tower B - West", "Clubhouse", "Villas 1-12"],
        "Plumbing Vulnerability": [12, 34, 8, 19, 5, 42],
        "Electrical Risk": [8, 14, 27, 11, 4, 15],
        "HVAC Degradation": [45, 38, 22, 29, 65, 18]
    }
    df_heat = pd.DataFrame(heatmap_data).set_index("Property Wing")
    fig_heat = px.imshow(
        df_heat,
        labels=dict(x="Trade Vulnerability", y="Building Wing", color="Risk Index"),
        x=["Plumbing", "Electrical", "HVAC"],
        y=df_heat.index,
        color_continuous_scale="Reds",
        title="Vulnerability Index Across Facilities",
        template="plotly_dark"
    )
    st.plotly_chart(fig_heat, use_container_width=True)

with tab4:
    st.subheader("Benchmarks & System Design")
    st.markdown("Performance evaluation across architectures.")

    col_b1, col_b2 = st.columns(2)
    with col_b1:
        st.plotly_chart(create_radar_chart(), use_container_width=True)
    with col_b2:
        st.plotly_chart(create_cost_latency_chart(), use_container_width=True)

    st.markdown("### Benchmark Data")
    st.dataframe(get_benchmark_dataframe(), use_container_width=True, hide_index=True)

    st.markdown("### Architecture Pipeline")
    st.markdown("""
    ```mermaid
    flowchart TD
        A["Tenant Issue Intake<br/>(Text, Voice Transcript, Photo)"] --> B["API Gateway / UI<br/>(FastAPI / Webhooks)"]
        B --> C{"Sentinel Agent<br/>(Hazard Verification)"}
        
        C -->|"Hazard Present"| H1["Immediate P1 Protocol<br/>Safety Isolation Steps + Urgent Dispatch"]
        C -->|"Standard Defect"| D["Multimodal Diagnostic Agent<br/>(Defect Detection + Fault Code Analysis)"]
        
        D --> E["Scoping & Cost Agent<br/>(Parts, Labor Hours, INR Bracket)"]
        E --> F["SLA & Dispatch Router<br/>(Proximity, Rating, Trade Specialty)"]
        
        H1 --> G["Database & Queue<br/>(PostgreSQL + WebSockets)"]
        F --> G
        G --> H["Automated Notifications<br/>to Tenant & Contractor"]
    ```
    """)

st.divider()
st.caption("TenantEase CogniCare v2.4 • Property Maintenance & Cognitive Dispatch Engine")
