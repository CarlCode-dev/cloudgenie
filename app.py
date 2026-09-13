import streamlit as st

st.set_page_config(page_title="CloudGenie", page_icon="☁️")

st.sidebar.title("☁️ CloudGenie")
page = st.sidebar.radio("Go to", ["Dashboard", "SecOps Auditor", "FinOps Optimizer"])

# --- Dashboard ---
if page == "Dashboard":
    st.title("Dashboard")
    st.write("Welcome to CloudGenie — your AI-powered cloud engineering portfolio.")
    col1, col2 = st.columns(2)
    col1.metric("Mock Security Score", "82/100")
    col2.metric("Mock Monthly Savings Found", "$340")

# --- SecOps Auditor ---
elif page == "SecOps Auditor":
    st.title("SecOps Auditor")
    st.write("Upload a config or log file to scan for vulnerabilities.")
    uploaded_file = st.file_uploader("Upload a file (mock scan — no real analysis yet)", type=["txt", "json", "log"])

    if uploaded_file is not None:
        st.write(f"File received: **{uploaded_file.name}**")
        st.warning("HIGH RISK: Open SSH port found (mock result)")
        st.info("MEDIUM RISK: Outdated IAM policy (mock result)")
        st.success("LOW RISK: Unused security group (mock result)")
        if st.button("🛠️ Fix with AI"):
            st.code("resource \"aws_security_group_rule\" \"fix\" {\n  # Example Terraform fix (mock output)\n}", language="hcl")
    else:
        st.caption("No file uploaded yet.")

# --- FinOps Optimizer ---
elif page == "FinOps Optimizer":
    st.title("FinOps Optimizer")
    st.write("Analyze cloud billing to find savings opportunities.")
    st.success("💰 Idle EC2 instance found — potential savings: $120/month (mock)")
    st.success("💰 Oversized database detected — potential savings: $90/month (mock)")
    st.metric("Total Potential Monthly Savings", "$210")