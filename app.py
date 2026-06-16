
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
    ai_provider = st.selectbox("AI Provider", ["ollama", "nvidia"], index=0 if config.get("ai_engine", {}).get("provider") == "ollama" else 1)
    
    if ai_provider == "ollama":
        default_url = "http://localhost:11434/v1"
        default_model = "llama3"
        ai_key = "ollama"
    else:
        default_url = "https://integrate.api.nvidia.com/v1"
        default_model = "nvidia/nemotron-3-ultra-550b-a55b"
        ai_key = config.get("ai_engine", {}).get("api_key", "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")

    ai_base_url = st.text_input("AI Base URL", value=config.get("ai_engine", {}).get("base_url", default_url))
    ai_key = st.text_input("AI API Key", value=ai_key, type="password")
    ai_model = st.text_input("AI Model", value=config.get("ai_engine", {}).get("model", default_model))
    
    if st.button("Save Configuration"):
        config["api_keys"] = {"haveibeenpwned": hibp_key, "numverify": numverify_key}
        if "ai_engine" not in config: config["ai_engine"] = {}
        config["ai_engine"]["enabled"] = ai_enabled
        config["ai_engine"]["provider"] = ai_provider
        config["ai_engine"]["base_url"] = ai_base_url
        config["ai_engine"]["api_key"] = ai_key
        config["ai_engine"]["model"] = ai_model
        config["ai_engine"]["max_tokens"] = 16384
        config["ai_engine"]["reasoning_budget"] = 16384
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
        tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
            "📊 Summary", "👤 Social Identity", "📄 Documents", 
            "🌐 Identity Graph", "🧠 AI Insight", "🛠️ Manual Toolkit"
        ])
        
        with tab1:
            st.header("Investigation Summary")
            st.json(results)
            
        with tab2:
            st.header("Social Identities")
            social_entries = [r for r in results if r["type"] == "handle"]
            if social_entries:
                for entry in social_entries:
                    st.subheader(f"Handle: {entry['entity']}")
                    for site in entry["data"]:
                        if site["exists"]:
                            st.success(f"**[{site['site']}]({site['url']})** - {site.get('title', 'N/A')}")
            else:
                st.info("No social handles discovered in this search.")

        with tab3:
            st.header("Discovered Documents")
            all_docs = []
            for r in results:
                if "documents" in r:
                    all_docs.extend(r["documents"])
            
            if all_docs:
                for doc in all_docs:
                    st.write(f"### [{doc['title']}]({doc['href']})")
                    st.write(doc['body'])
                    st.divider()
            else:
                st.info("No documents found for this target.")

        with tab4:
            st.header("Identity Relationship Graph")
            st.write("Target -> Entities Connected")
            nodes = {r["entity"]: r["type"] for r in results if r["type"] in ["email", "phone", "handle"]}
            st.write(nodes)
            st.info("Tip: More advanced graph visualizations are coming soon.")

        with tab5:
            st.header("AI Analyst Summary")
            ai_data = next((item["data"] for item in results if item["type"] == "ai_summary"), None)
            if ai_data:
                st.markdown(ai_data)
            else:
                st.info("AI Analysis was not enabled or no data returned.")

        with tab6:
            st.header("Manual Investigation Toolkit")
            st.write("Launch manual deep-dives without requiring API keys.")
            
            t_type = icarus.detect_type(target_input)
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Target-Specific Tools")
                if t_type == "email":
                    st.link_button("HIBP Manual Search", f"https://haveibeenpwned.com/account/{target_input}")
                    st.link_button("Epieos Tracer", f"https://epieos.com/?q={target_input}")
                    st.link_button("Intelligence X Search", f"https://intelx.io/?s={target_input}")
                    st.link_button("LeakCheck Profile", f"https://leakcheck.io/profiles/{target_input}")
                elif t_type == "phone":
                    st.link_button("Sync.me Search", f"https://sync.me/search/?number={target_input}")
                    st.link_button("Truecaller Search", f"https://www.truecaller.com/search/in/{target_input}")
                elif t_type == "handle":
                    st.link_button("WhatsMyName.app", f"https://whatsmyname.app/?q={target_input}")
                    st.link_button("NameCheckup", f"https://namecheckup.com/search?q={target_input}")
                    st.link_button("Social-Searcher", f"https://www.social-searcher.com/search-users/?q={target_input}")

            with col2:
                st.subheader("Global OSINT Links")
                st.link_button("OSINT Framework", "https://osintframework.com/")
                st.link_button("IntelTechniques", "https://inteltechniques.com/tools/index.html")
                st.link_button("Shodan Search", f"https://www.shodan.io/search?query={target_input}")

            st.divider()
            st.info("🕵️‍♂️ **Tip**: Always use a VPN or dedicated browser profile for manual OSINT work.")

        # Download Report
        st.divider()
        report_json = json.dumps(results, indent=4)
        st.download_button(
            label="💾 Download Full JSON Report",
            data=report_json,
            file_name=f"icarus_report_{target_input}.json",
            mime="application/json",
            use_container_width=True
        )

else:
    st.info("Enter a target above and click 'Launch Investigation' to start.")

