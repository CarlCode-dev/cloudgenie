import json
import streamlit as st
import pandas as pd
import random
import datetime
import textwrap
import google.generativeai as genai

genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel("gemini-3.6-flash")

st.set_page_config(page_title="CloudGenie", page_icon="☁️", layout="wide")

st.markdown("""
<style>

@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 0%, #0F1B33 0%, #0A0F1E 45%, #060910 100%);
    background-size: 200% 200%;
    animation: bgShift 15s ease infinite;
}
@keyframes bgShift {
    0% { background-position: 0% 0%; }
    50% { background-position: 100% 100%; }
    100% { background-position: 0% 0%; }
}

/* --- Sidebar glass panel --- */
[data-testid="stSidebar"] {
    background: rgba(13, 21, 38, 0.55);
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    border-right: 1px solid rgba(56, 225, 255, 0.15);
}

.sidebar-logo {
    font-size: 22px;
    font-weight: 700;
    color: #E6F1FF;
    padding: 8px 4px 24px 4px;
    animation: floaty 3s ease-in-out infinite;
}
.sidebar-logo span { color: #38E1FF; text-shadow: 0 0 14px rgba(56,225,255,0.5); }
@keyframes floaty {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-4px); }
}

/* Nav buttons: inactive state */
[data-testid="stSidebar"] .stButton>button {
    width: 100%;
    text-align: left;
    background: transparent;
    color: #9FB3CC;
    border: 1px solid transparent;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: 500;
    margin-bottom: 4px;
    box-shadow: none;
    transition: all 0.25s ease;
}
[data-testid="stSidebar"] .stButton>button:hover {
    background: rgba(56,225,255,0.08);
    color: #38E1FF;
    transform: translateX(4px);
    box-shadow: none;
}

/* Nav buttons: active state (Streamlit "primary" type) */
[data-testid="stSidebar"] .stButton>button[kind="primary"] {
    background: linear-gradient(90deg, rgba(56,225,255,0.15), rgba(56,225,255,0.03));
    color: #38E1FF;
    border-left: 3px solid #38E1FF;
    border-radius: 10px;
    box-shadow: 0 0 18px rgba(56,225,255,0.15);
}
[data-testid="stSidebar"] .stButton>button[kind="primary"]:hover {
    transform: none;
}

.sidebar-footer {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 14px;
    margin-top: 24px;
    border-radius: 14px;
    background: rgba(56,225,255,0.05);
    border: 1px solid rgba(56,225,255,0.12);
}
.sidebar-footer .avatar {
    width: 34px; height: 34px;
    border-radius: 50%;
    background: linear-gradient(135deg, #1B8FD1, #38E1FF);
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; color: #06121F;
}
.sidebar-footer .name { color: #E6F1FF; font-weight: 600; font-size: 14px; }
.sidebar-footer .link { color: #38E1FF; font-size: 12px; text-decoration: none; }

/* --- Hero + cards --- */
.hero { animation: fadeInUp 0.7s ease both; padding: 40px 0 20px 0; }
.hero h1 {
    font-size: 42px;
    background: linear-gradient(90deg, #E6F1FF, #38E1FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.hero p { color: #9FB3CC; font-size: 16px; }
@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(16px); }
    to { opacity: 1; transform: translateY(0); }
}

.card-grid { display: flex; gap: 20px; flex-wrap: wrap; margin-top: 24px; }
.card {
    flex: 1; min-width: 220px;
    background: linear-gradient(145deg, rgba(56,225,255,0.06), rgba(17,26,46,0.9));
    border: 1px solid rgba(56, 225, 255, 0.18);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
    animation: fadeInUp 0.7s ease both, cardGlow 4s ease-in-out infinite;
}
@keyframes cardGlow {
    0%, 100% { box-shadow: 0 8px 30px rgba(0,0,0,0.35), 0 0 0px rgba(56,225,255,0); }
    50% { box-shadow: 0 8px 30px rgba(0,0,0,0.35), 0 0 20px rgba(56,225,255,0.25); }
}
.card .label { color: #9FB3CC; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }
.card .value { color: #E6F1FF; font-size: 32px; font-weight: 700; margin-top: 6px; }
.card .glow { color: #38E1FF; text-shadow: 0 0 14px rgba(56,225,255,0.5); }

.risk-card { background: #0F1830; border-left: 4px solid; border-radius: 10px; padding: 16px 20px; margin-bottom: 12px; animation: fadeInUp 0.5s ease both; }
.risk-high { border-color: #FF5C6C; }
.risk-med { border-color: #FFB020; }
.risk-low { border-color: #38E1FF; }

/* Main-area buttons (Fix with AI etc.) stay bold/gradient */
[data-testid="stAppViewContainer"] .stButton>button {
    background: linear-gradient(90deg, #1B8FD1, #38E1FF);
    color: #06121F;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.55em 1.6em;
}
[data-testid="stAppViewContainer"] .stButton>button:hover {
    box-shadow: 0 0 24px rgba(56, 225, 255, 0.55);
    transform: translateY(-2px);
}

[data-testid="stFileUploaderDropzone"] {
    background: #0D1526;
    border: 2px dashed rgba(56, 225, 255, 0.3);
    border-radius: 14px;
}

.incident-card {
    background: #0F1830;
    border-left: 4px solid;
    border-radius: 10px;
    padding: 14px 20px;
    margin-bottom: 12px;
    display: flex;
    justify-content: space-between;
    align-items: center;
    animation: fadeInUp 0.5s ease both;
}
.incident-open { border-color: #FF5C6C; }
.incident-resolved { border-color: #38E1FF; opacity: 0.7; }
.badge {
    padding: 4px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.5px;
}
.badge-open { background: rgba(255,92,108,0.15); color: #FF5C6C; }
.badge-resolved { background: rgba(56,225,255,0.15); color: #38E1FF; }

</style>
""", unsafe_allow_html=True)

# --- Sidebar navigation (icon-led, glowing active state) ---
if "page" not in st.session_state:
    st.session_state.page = "About Me"

nav_items = [
    ("About Me", "👤"),
    ("Dashboard", "📊"),
    ("Monitoring", "📈"),
    ("Incidents", "🚨"),
    ("Status", "✅"),
    ("Architecture", "🧩"),
    ("SecOps Auditor", "🛡️"),
    ("FinOps Optimizer", "💰"),
]

st.sidebar.markdown("<div class='sidebar-logo'>☁️ <span>CloudGenie</span></div>", unsafe_allow_html=True)

for label, icon in nav_items:
    is_active = st.session_state.page == label
    if st.sidebar.button(f"{icon}   {label}", key=f"nav_{label}",
                          use_container_width=True,
                          type="primary" if is_active else "secondary"):
        st.session_state.page = label

st.sidebar.markdown("""
<div class="sidebar-footer">
    <div class="avatar">CD</div>
    <div>
        <div class="name">Carlito Dignos</div>
        <a class="link" href="https://github.com/CarlCode-dev" target="_blank">github.com/CarlCode-dev</a>
    </div>
</div>
""", unsafe_allow_html=True)

page = st.session_state.page

# --- About Me ---
if page == "About Me":
    st.markdown("""
    <div class="hero">
        <h1>Hi, I'm Carlito 👋</h1>
        <p>3rd-year BSIT student building toward a Cloud Engineering career. CloudGenie is my hands-on portfolio project — a simulated cloud operations platform combining security auditing, cost optimization, monitoring, and incident response into one working app.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("**Skills I'm building:** Cloud fundamentals · Python · AWS basics · Security auditing · Cost optimization")
    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("What this project demonstrates")
    st.markdown("""
    <div class="card-grid">
        <div class="card"><div class="label">🛡️ SecOps Auditor</div><div style="color:#9FB3CC; margin-top:8px;">Scans uploaded files for security risks and suggests fixes.</div></div>
        <div class="card"><div class="label">💰 FinOps Optimizer</div><div style="color:#9FB3CC; margin-top:8px;">Analyzes cloud billing trends to find cost savings.</div></div>
        <div class="card"><div class="label">📈 Monitoring & Status</div><div style="color:#9FB3CC; margin-top:8px;">Live system health metrics with auto-logged incidents.</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("Built end-to-end: coded in Python, version-controlled with Git/GitHub, and deployed live on Streamlit Community Cloud — a full working deployment pipeline, not just a design mockup.")

    st.info("This app is currently running on simulated/mock data. Real Claude AI integration is the next milestone.")

# --- Dashboard ---
elif page == "Dashboard":
    st.markdown("<div class='hero'><h1>Dashboard</h1><p>Welcome to CloudGenie — your AI-powered cloud engineering portfolio.</p></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card-grid">
        <div class="card"><div class="label">Security Score</div><div class="value glow">82/100</div></div>
        <div class="card"><div class="label">Monthly Savings Found</div><div class="value glow">$340</div></div>
    </div>
    """, unsafe_allow_html=True)

# --- Monitoring ---
elif page == "Monitoring":
    st.markdown("<div class='hero'><h1>Monitoring</h1><p>Live system health metrics (simulated).</p></div>", unsafe_allow_html=True)

    if "metrics_history" not in st.session_state:
        st.session_state.metrics_history = pd.DataFrame({
            "Time": [], "CPU (%)": [], "Memory (%)": [], "Network (Mbps)": []
        })

    if st.button("🔄 Refresh Metrics"):
        new_row = pd.DataFrame({
            "Time": [datetime.datetime.now().strftime("%H:%M:%S")],
            "CPU (%)": [random.randint(20, 95)],
            "Memory (%)": [random.randint(30, 90)],
            "Network (Mbps)": [random.randint(10, 500)],
        })
        st.session_state.metrics_history = pd.concat(
            [st.session_state.metrics_history, new_row], ignore_index=True
        ).tail(20)

    if len(st.session_state.metrics_history) == 0:
        st.info("Click 'Refresh Metrics' to start monitoring.")
    else:
        latest = st.session_state.metrics_history.iloc[-1]
        st.markdown(f"""
        <div class="card-grid">
            <div class="card"><div class="label">CPU Usage</div><div class="value glow">{latest['CPU (%)']}%</div></div>
            <div class="card"><div class="label">Memory Usage</div><div class="value glow">{latest['Memory (%)']}%</div></div>
            <div class="card"><div class="label">Network Throughput</div><div class="value glow">{latest['Network (Mbps)']} Mbps</div></div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)
        chart_df = st.session_state.metrics_history.set_index("Time")
        st.line_chart(chart_df)

        if latest["CPU (%)"] > 85:
            st.warning("⚠️ High CPU usage detected — potential scaling event.")
            if "incidents" not in st.session_state:
                st.session_state.incidents = []
            already_logged = any(
                inc["time"] == latest["Time"] for inc in st.session_state.incidents
            )
            if not already_logged:
                st.session_state.incidents.append({
                    "time": latest["Time"],
                    "description": f"High CPU usage detected ({latest['CPU (%)']}%)",
                    "status": "Open"
                })

# --- Incidents ---
elif page == "Incidents":
    st.markdown("<div class='hero'><h1>Incident Timeline</h1><p>Auto-logged incidents from live monitoring.</p></div>", unsafe_allow_html=True)

    if "incidents" not in st.session_state:
        st.session_state.incidents = []

    if len(st.session_state.incidents) == 0:
        st.info("No incidents logged yet. Trigger high CPU usage on the Monitoring page to generate one.")
    else:
        for i, incident in enumerate(reversed(st.session_state.incidents)):
            real_index = len(st.session_state.incidents) - 1 - i
            status_class = "incident-open" if incident["status"] == "Open" else "incident-resolved"
            badge_class = "badge-open" if incident["status"] == "Open" else "badge-resolved"

            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div class="incident-card {status_class}">
                    <div>
                        <b>{incident['description']}</b><br>
                        <span style="color:#9FB3CC; font-size:13px;">{incident['time']}</span>
                    </div>
                    <span class="badge {badge_class}">{incident['status']}</span>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if incident["status"] == "Open":
                    if st.button("Resolve", key=f"resolve_{real_index}"):
                        st.session_state.incidents[real_index]["status"] = "Resolved"
                        st.rerun()

# --- Status ---
elif page == "Status":
    st.markdown("<div class='hero'><h1>System Status</h1><p>Live operational status overview.</p></div>", unsafe_allow_html=True)

    open_incidents = [i for i in st.session_state.get("incidents", []) if i["status"] == "Open"]
    overall_status = "🟠 Degraded Performance" if open_incidents else "🟢 All Systems Operational"

    st.markdown(f"""
    <div class="card-grid">
        <div class="card" style="flex:2;">
            <div class="label">Overall Status</div>
            <div class="value glow">{overall_status}</div>
        </div>
        <div class="card">
            <div class="label">Open Incidents</div>
            <div class="value glow">{len(open_incidents)}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("Components")

    components = [
        ("SecOps Auditor", "Operational"),
        ("FinOps Optimizer", "Operational"),
        ("Monitoring Engine", "Degraded" if open_incidents else "Operational"),
        ("Incident Tracker", "Operational"),
    ]
    for name, status in components:
        badge_class = "badge-resolved" if status == "Operational" else "badge-open"
        dot = "🟢" if status == "Operational" else "🟠"
        st.markdown(f"""
        <div class="incident-card incident-resolved">
            <div>{dot} <b>{name}</b></div>
            <span class="badge {badge_class}">{status}</span>
        </div>
        """, unsafe_allow_html=True)

    if open_incidents:
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("Active Incidents")
        for inc in open_incidents:
            st.markdown(f"""
            <div class="incident-card incident-open">
                <div><b>{inc['description']}</b><br><span style="color:#9FB3CC; font-size:13px;">{inc['time']}</span></div>
                <span class="badge badge-open">Open</span>
            </div>
            """, unsafe_allow_html=True)

# --- Architecture ---
elif page == "Architecture":
    st.markdown("<div class='hero'><h1>Architecture</h1><p>How CloudGenie's fictional system is structured.</p></div>", unsafe_allow_html=True)

    svg_code = """<div class="card" style="padding:30px;">
<svg viewBox="0 0 900 520" xmlns="http://www.w3.org/2000/svg" style="width:100%; height:auto;">
<defs>
<marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="3" orient="auto" markerUnits="strokeWidth">
<path d="M0,0 L0,6 L9,3 z" fill="#38E1FF"/>
</marker>
<filter id="glow">
<feGaussianBlur stdDeviation="3" result="blur"/>
<feMerge>
<feMergeNode in="blur"/>
<feMergeNode in="SourceGraphic"/>
</feMerge>
</filter>
</defs>
<line x1="450" y1="90" x2="450" y2="150" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="450" y1="210" x2="250" y2="280" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="450" y1="210" x2="650" y2="280" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="250" y1="340" x2="440" y2="410" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<line x1="650" y1="340" x2="460" y2="410" stroke="#38E1FF" stroke-width="2" marker-end="url(#arrow)"/>
<rect x="360" y="30" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="450" y="65" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Users / CDN</text>
<rect x="360" y="150" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="450" y="185" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Load Balancer</text>
<rect x="160" y="280" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="250" y="315" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Web Server 1</text>
<rect x="560" y="280" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="650" y="315" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Web Server 2</text>
<rect x="360" y="410" width="180" height="60" rx="12" fill="#111A2E" stroke="#38E1FF" stroke-width="1.5" filter="url(#glow)"/>
<text x="450" y="445" fill="#E6F1FF" font-size="16" font-family="sans-serif" text-anchor="middle" font-weight="700">Database</text>
</svg>
</div>"""
    st.markdown(svg_code, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.markdown("**Users / CDN**")
        st.caption("Entry point for traffic; caches static content close to users for speed.")
    with col2:
        st.markdown("**Load Balancer**")
        st.caption("Distributes incoming requests evenly across available web servers.")
    with col3:
        st.markdown("**Web Servers**")
        st.caption("Run the application logic; multiple instances allow redundancy and scaling.")
    with col4:
        st.markdown("**Database**")
        st.caption("Stores and retrieves persistent application data.")

# --- SecOps Auditor ---
elif page == "SecOps Auditor":
    st.markdown("<div class='hero'><h1>SecOps Auditor</h1><p>Upload a config or log file to scan for vulnerabilities.</p></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a file for AI security analysis", type=["txt", "json", "log"])

    if uploaded_file is not None:
        st.write(f"File received: **{uploaded_file.name}**")

        file_content = uploaded_file.read().decode("utf-8", errors="ignore")

        if st.button("🔍 Scan with AI"):
            with st.spinner("Analyzing file for security risks..."):
                prompt = f"""You are a cloud security auditor. Analyze the following file content for security vulnerabilities, misconfigurations, or risks.

Return ONLY a valid JSON array (no markdown, no extra text) where each item has this exact structure:
{{"risk": "High" or "Medium" or "Low", "title": "short title", "description": "1-2 sentence explanation and recommendation"}}

If there are no notable risks, return an empty array: []

File content:
{file_content[:4000]}
"""
                try:
                    response = model.generate_content(prompt)
                    raw_text = response.text.strip()
                    raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                    findings = json.loads(raw_text)
                except Exception as e:
                    findings = None
                    st.error(f"Couldn't parse AI response. Raw output shown below.")
                    st.code(response.text if 'response' in dir() else str(e))

            if findings is not None:
                if len(findings) == 0:
                    st.success("✅ No significant risks detected in this file.")
                else:
                    risk_class_map = {"High": "risk-high", "Medium": "risk-med", "Low": "risk-low"}
                    risk_emoji_map = {"High": "🔴", "Medium": "🟠", "Low": "🟢"}
                    for finding in findings:
                        risk = finding.get("risk", "Low")
                        css_class = risk_class_map.get(risk, "risk-low")
                        emoji = risk_emoji_map.get(risk, "🟢")
                        st.markdown(f"""
                        <div class="risk-card {css_class}">{emoji} <b>{risk.upper()} RISK</b> — {finding.get('title','')}<br><span style="color:#9FB3CC;">{finding.get('description','')}</span></div>
                        """, unsafe_allow_html=True)

                    if st.button("🛠️ Fix with AI"):
                        st.code("resource \"aws_security_group_rule\" \"fix\" {\n  # Example Terraform fix (mock output)\n}", language="hcl")
    else:
        st.caption("No file uploaded yet.")

# --- FinOps Optimizer ---
elif page == "FinOps Optimizer":
    st.markdown("<div class='hero'><h1>FinOps Optimizer</h1><p>Analyze cloud billing to find savings opportunities.</p></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("6-Month Cost Trend")
    st.caption("Monthly cloud spend before optimization recommendations were applied.")

    months = ["Apr", "May", "Jun", "Jul", "Aug", "Sep"]
    monthly_cost = [1450, 1580, 1390, 1240, 1180, 1020]

    trend_df = pd.DataFrame({
        "Month": months,
        "Cloud Spend ($)": monthly_cost
    })
    st.line_chart(trend_df.set_index("Month"))

    total_saved = monthly_cost[0] - monthly_cost[-1]
    pct_saved = round((total_saved / monthly_cost[0]) * 100, 1)
    st.success(f"📉 Spend down **{pct_saved}%** since April — roughly **${total_saved}/month** saved through ongoing optimization.")

    st.markdown("<br>", unsafe_allow_html=True)
    st.subheader("AI Cost Optimization Recommendations")

    mock_billing_data = """
Monthly Cloud Billing Summary (September):
- EC2 instance web-prod-02: running 24/7 at m5.xlarge, average CPU utilization 8%
- RDS database db-main: db.r5.2xlarge, average connections 12, storage 500GB (200GB used)
- S3 bucket 'old-backups-2023': 800GB, no access in 90+ days, no lifecycle policy
- Elastic IP allocated but unattached: 3 addresses
- EBS volumes: 5 unattached volumes totaling 200GB
Total monthly spend: $1,020
"""

    if st.button("💡 Get AI Recommendations"):
        with st.spinner("Analyzing billing data for cost savings..."):
            prompt = f"""You are a FinOps cost optimization specialist. Analyze this mock cloud billing data and identify specific cost-saving opportunities.

Return ONLY a valid JSON array (no markdown, no extra text) where each item has this exact structure:
{{"title": "short title", "description": "1-2 sentence explanation of the issue and fix", "estimated_savings": "$XX/month"}}

Billing data:
{mock_billing_data}
"""
            try:
                response = model.generate_content(prompt)
                raw_text = response.text.strip()
                raw_text = raw_text.replace("```json", "").replace("```", "").strip()
                recommendations = json.loads(raw_text)
            except Exception as e:
                recommendations = None
                st.error("Couldn't parse AI response. Raw output shown below.")
                st.code(response.text if 'response' in dir() else str(e))

        if recommendations is not None:
            if len(recommendations) == 0:
                st.info("No additional optimization opportunities found.")
            else:
                cards_html = '<div class="card-grid">'
                for rec in recommendations:
                    cards_html += f"""
<div class="card">
<div class="label">{rec.get('title','')}</div>
<div class="value glow" style="font-size:22px;">{rec.get('estimated_savings','')}</div>
<div style="color:#9FB3CC; margin-top:8px; font-size:14px;">{rec.get('description','')}</div>
</div>
"""
                cards_html += '</div>'
                st.markdown(cards_html, unsafe_allow_html=True)