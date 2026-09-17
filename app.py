import random
import datetime
import streamlit as st
import pandas as pd

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
        <p>BSIT student building toward a Cloud Engineering/Architecture career. CloudGenie is my hands-on portfolio project combining SecOps and FinOps AI tools, built with Python + Streamlit.</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("**Skills I'm building:** Cloud fundamentals · Python · AWS basics · Security auditing · Cost optimization")
    st.info("This app is currently running on demo/mock data. Real Claude AI integration coming soon.")

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

# --- SecOps Auditor ---
elif page == "SecOps Auditor":
    st.markdown("<div class='hero'><h1>SecOps Auditor</h1><p>Upload a config or log file to scan for vulnerabilities.</p></div>", unsafe_allow_html=True)
    uploaded_file = st.file_uploader("Upload a file (mock scan)", type=["txt", "json", "log"])

    if uploaded_file is not None:
        st.write(f"File received: **{uploaded_file.name}**")
        st.markdown("""
        <div class="risk-card risk-high">🔴 <b>HIGH RISK</b> — Open SSH port found (mock)<br><span style="color:#9FB3CC;">Port 22 open to 0.0.0.0/0. Restrict to specific IP ranges.</span></div>
        <div class="risk-card risk-med">🟠 <b>MEDIUM RISK</b> — Outdated IAM policy (mock)<br><span style="color:#9FB3CC;">Policy grants broader permissions than needed. Apply least privilege.</span></div>
        <div class="risk-card risk-low">🟢 <b>LOW RISK</b> — Unused security group (mock)<br><span style="color:#9FB3CC;">No attached resources. Remove if unused.</span></div>
        """, unsafe_allow_html=True)
        if st.button("🛠️ Fix with AI"):
            st.code("resource \"aws_security_group_rule\" \"fix\" {\n  # Example Terraform fix (mock output)\n}", language="hcl")
    else:
        st.caption("No file uploaded yet.")

# --- FinOps Optimizer ---
elif page == "FinOps Optimizer":
    st.markdown("<div class='hero'><h1>FinOps Optimizer</h1><p>Analyze cloud billing to find savings opportunities.</p></div>", unsafe_allow_html=True)
    st.markdown("""
    <div class="card-grid">
        <div class="card"><div class="label">Idle EC2 Instance</div><div class="value glow">$120/mo</div></div>
        <div class="card"><div class="label">Oversized Database</div><div class="value glow">$90/mo</div></div>
        <div class="card"><div class="label">Total Potential Savings</div><div class="value glow">$210/mo</div></div>
    </div>
    """, unsafe_allow_html=True)

    chart_data = pd.DataFrame({
        "Category": ["Idle EC2", "Oversized DB", "Other"],
        "Savings ($)": [120, 90, 30]
    })
    st.bar_chart(chart_data.set_index("Category"))