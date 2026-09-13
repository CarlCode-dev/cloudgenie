import streamlit as st
import pandas as pd

st.set_page_config(page_title="CloudGenie", page_icon="☁️", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;700&display=swap');

html, body, [class*="css"] { font-family: 'Space Grotesk', sans-serif; }

.stApp {
    background: radial-gradient(circle at 20% 0%, #0F1B33 0%, #0A0F1E 45%, #060910 100%);
}

[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D1526 0%, #0A0F1E 100%);
    border-right: 1px solid rgba(56, 225, 255, 0.15);
}

.nav-btn {
    display: block;
    padding: 12px 16px;
    margin-bottom: 8px;
    border-radius: 10px;
    color: #9FB3CC;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.2s ease;
}
.nav-btn:hover { background: rgba(56,225,255,0.08); color: #38E1FF; }
.nav-active { background: rgba(56,225,255,0.12); color: #38E1FF !important; border-left: 3px solid #38E1FF; }

.hero {
    padding: 40px 0 20px 0;
}
.hero h1 {
    font-size: 42px;
    background: linear-gradient(90deg, #E6F1FF, #38E1FF);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 4px;
}
.hero p { color: #9FB3CC; font-size: 16px; }

.card-grid {
    display: flex;
    gap: 20px;
    flex-wrap: wrap;
    margin-top: 24px;
}
.card {
    flex: 1;
    min-width: 220px;
    background: linear-gradient(145deg, rgba(56,225,255,0.06), rgba(17,26,46,0.9));
    border: 1px solid rgba(56, 225, 255, 0.18);
    border-radius: 18px;
    padding: 24px;
    box-shadow: 0 8px 30px rgba(0,0,0,0.35);
}
.card .label { color: #9FB3CC; font-size: 13px; text-transform: uppercase; letter-spacing: 1px; }
.card .value { color: #E6F1FF; font-size: 32px; font-weight: 700; margin-top: 6px; }
.card .glow { color: #38E1FF; text-shadow: 0 0 14px rgba(56,225,255,0.5); }

.risk-card {
    background: #0F1830;
    border-left: 4px solid;
    border-radius: 10px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.risk-high { border-color: #FF5C6C; }
.risk-med { border-color: #FFB020; }
.risk-low { border-color: #38E1FF; }

.stButton>button {
    background: linear-gradient(90deg, #1B8FD1, #38E1FF);
    color: #06121F;
    border: none;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.55em 1.6em;
    transition: all 0.25s ease;
}
.stButton>button:hover {
    box-shadow: 0 0 24px rgba(56, 225, 255, 0.55);
    transform: translateY(-2px);
}

[data-testid="stFileUploaderDropzone"] {
    background: #0D1526;
    border: 2px dashed rgba(56, 225, 255, 0.3);
    border-radius: 14px;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("<h2 style='text-align:center; color:#38E1FF;'>☁️ CloudGenie</h2>", unsafe_allow_html=True)
page = st.sidebar.radio("Go to", ["About Me", "Dashboard", "SecOps Auditor", "FinOps Optimizer"], label_visibility="collapsed")
st.sidebar.markdown("---")
st.sidebar.write("Built by **Carlito Dignos**")
st.sidebar.write("[GitHub](https://github.com/CarlCode-dev)")

# --- About Me ---
if page == "About Me":
    st.markdown("""
    <div class="hero">
        <h1>Hi, I'm Carlito 👋</h1>
        <p>BSIT student building toward a Cloud Engineering career. CloudGenie is my hands-on portfolio project combining SecOps and FinOps AI tools, built with Python + Streamlit.</p>
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