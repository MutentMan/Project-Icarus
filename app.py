
import streamlit as st
import asyncio
import json
import os
import yaml
from core import IcarusCore
from streamlit_option_menu import option_menu

# Page Config
st.set_page_config(
    page_title="Project Icarus | OSINT Suite",
    page_icon="🦅",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Dark Theme Styling
st.markdown("""
    <style>
    .stApp {
        background-color: #0e1117;
        color: #e0e0e0;
    }
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        color: #ff4b4b;
        margin-bottom: 0;
    }
    .sub-header {
        color: #808495;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        white-space: pre-wrap;
        background-color: #1e2130;
        border-radius: 5px 5px 0 0;
        gap: 1px;
        padding-top: 10px;
        padding-bottom: 10px;
    }
    .stTabs [aria-selected="true"] {
        background-color: #ff4b4b;
    }
    </style>
    """, unsafe_allow_html=True)

# Helper to run async code in Streamlit
def run_async(coro):
    return asyncio.run(coro)

def load_config():
    if os.path.exists("config.yaml"):
        with open("config.yaml", "r") as f:
            return yaml.safe_load(f)
    return {}

def save_config(config):
    with open("config.yaml", "w") as f:
        yaml.safe_dump(config, f)

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/wired/128/ff4b4b/phoenix.png", width=100)
    st.title("Icarus Settings")
    
    config = load_config()
    
    st.subheader("API Configuration")
    hibp_key = st.text_input("HIBP API Key", value=config.get("api_keys", {}).get("haveibeenpwned", ""), type="password")
    numverify_key = st.text_input("NumVerify API Key", value=config.get("api_keys", {}).get("numverify", ""), type="password")
    
    st.subheader("AI Engine")
    ai_enabled = st.checkbox("Enable AI Analyst", value=config.get("ai_engine", {}).get("enabled", False))
    ai_model = st.selectbox("AI Model", ["llama3", "gpt-3.5-turbo", "gpt-4"], index=0)
    
    if st.button("Save Configuration"):
        config["api_keys"] = {"haveibeenpwned": hibp_key, "numverify": numverify_key}
        if "ai_engine" not in config: config["ai_engine"] = {}
        config["ai_engine"]["enabled"] = ai_enabled
        config["ai_engine"]["model"] = ai_model
        save_config(config)
        st.success("Config Saved!")

    st.divider()
    st.info("Project Icarus v2.0 - Developed by MutentMan")

# Main Content
st.markdown('<p class="main-header">Project Icarus 🦅</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Advanced OSINT Intelligence Suite</p>', unsafe_allow_html=True)

col1, col2 = st.columns([4, 1])
with col1:
    target_input = st.text_input("Enter Email, Phone, or Username", placeholder="e.g. target@example.com or +1234567890")
with col2:
    depth = st.number_input("Depth", min_value=1, max_value=3, value=1)

if st.button("Launch Investigation", use_container_width=True):
    if not target_input:
        st.warning("Please enter a target to investigate.")
    else:
        icarus = IcarusCore()
        
        status_text = st.empty()
        progress_bar = st.progress(0)
        
        def update_progress(msg):
            status_text.text(msg)
            # Simple increment for visual feedback
            
        with st.spinner("Investigating..."):
            results = run_async(icarus.run_investigation(target_input, max_depth=depth, progress_callback=update_progress))
            progress_bar.progress(100)
            status_text.text("Investigation Complete!")

        # Tabs for Results
        tab1, tab2, tab3, tab4, tab5 = st.tabs(["📊 Summary", "👤 Social Identity", "📄 Documents", "🌐 Web Mentions", "🧠 AI Insight"])
        
        with tab1:
            st.header("Investigation Summary")
            st.json(results)
            
        with tab2:
            st.header("Social Media Profiles")
            for item in results:
                if item.get("type") in ["social_handle", "url_handle"]:
                    data = item.get("data", [])
                    if isinstance(data, list):
                        for profile in data:
                            if profile.get("exists"):
                                st.write(f"✅ **{profile['site']}**: [{profile['url']}]({profile['url']})")
                
                # Check for social links found via email dorks
                if item.get("type") == "email":
                    conns = item.get("data", {}).get("social_media_connections", [])
                    for conn in conns:
                        st.write(f"🔗 **{conn['platform']}**: [{conn['url']}]({conn['url']})")

        with tab3:
            st.header("Related Documents")
            found_docs = False
            for item in results:
                if "documents" in item:
                    for doc in item["documents"]:
                        st.write(f"📄 **{doc['title']}**")
                        st.write(f"   Link: {doc['href']}")
                        found_docs = True
            if not found_docs:
                st.info("No documents found.")

        with tab4:
            st.header("Web Mentions")
            for item in results:
                # Direct handle web search
                if item.get("type") == "social_handle":
                    mentions = item.get("web_mentions", [])
                    for m in mentions:
                        st.write(f"🌐 **{m['title']}**")
                        st.write(f"   {m['href']}")
                # Phone mentions
                if item.get("type") == "phone":
                    mentions = item.get("data", {}).get("web_mentions", [])
                    for m in mentions:
                        st.write(f"📞 **{m['title']}**")
                        st.write(f"   {m['href']}")

        with tab5:
            st.header("AI Analyst Summary")
            ai_data = next((item["data"] for item in results if item["type"] == "ai_summary"), None)
            if ai_data:
                st.markdown(ai_data)
            else:
                st.info("AI Analysis was not enabled or no data returned.")

        # Download Report
        report_json = json.dumps(results, indent=4)
        st.download_button(
            label="Download Full JSON Report",
            data=report_json,
            file_name=f"icarus_report_{target_input}.json",
            mime="application/json",
        )
