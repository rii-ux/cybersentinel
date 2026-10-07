"""
CyberSentinel - Consumer Link Safety Checker
Simple, fast, and transparent link safety inspection.
"""

import os
import sys
import re
from urllib.parse import urlparse
import streamlit as st

# Ensure project root is in sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.predict import predict_url

# ==============================================================================
# STREAMLIT PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="CyberSentinel — Don't click. Check first.",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Initialize session state early so container layout can respond dynamically
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"

def render_html(content: str):
    """
    Renders HTML cleanly in Streamlit without CommonMark code-block indentation bugs.
    Strips leading whitespace from every line so CommonMark never triggers pre/code blocks.
    """
    cleaned = "\n".join(line.strip() for line in content.splitlines() if line.strip())
    st.markdown(cleaned, unsafe_allow_html=True)

# Determine container width based on active page
_is_wide = st.session_state.get("active_page") == "safety_tips"
_max_width = "1200px" if _is_wide else "860px"

st.markdown(f"""
<style>
    /* Force Streamlit to center the block container at all viewport sizes */
    section[data-testid="stMain"] > div.main > div.block-container,
    .main > div.block-container,
    .main .block-container {{
        max-width: {_max_width} !important;
        width: 100% !important;
        padding-top: 2rem !important;
        padding-bottom: 4rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}
    /* Streamlit wraps content in stMainBlockContainer in newer versions */
    [data-testid="stMainBlockContainer"] {{
        max-width: {_max_width} !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        margin-left: auto !important;
        margin-right: auto !important;
    }}
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# CONSUMER DESIGN SYSTEM (Black + Yellow CyberSentinel Identity)
# ==============================================================================
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    /* Hide Streamlit default chrome */
    #MainMenu, footer, header {
        visibility: hidden;
        height: 0;
    }
    .stDeployButton {
        display: none;
    }

    /* Global reset & typography */
    html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #0A0A0A !important;
        color: #F5F5F5 !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    }

    [data-testid="stVerticalBlock"] {
        gap: 1rem;
    }

    /* CyberSentinel Header / Brand */
    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.75rem 0 2rem 0;
        border-bottom: 1px solid #1E1E1E;
        margin-bottom: 2.25rem;
    }

    .brand-logo {
        font-size: 1.35rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        color: #F5F5F5;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        cursor: pointer;
    }

    .brand-dot {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #FFD21F;
        border-radius: 50%;
    }

    /* Hero Typography */
    .hero-eyebrow {
        font-size: 1rem;
        font-weight: 700;
        color: #A6A6A6;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.6rem;
    }

    .hero-title-main {
        font-size: clamp(3rem, 6vw, 4.5rem);
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
        color: #F5F5F5;
        margin-bottom: 0.2rem;
    }

    .hero-title-yellow {
        font-size: clamp(3rem, 6vw, 4.5rem);
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
        color: #FFD21F;
        margin-bottom: 1.35rem;
    }

    .hero-subhead {
        font-size: 1.5rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 0.4rem;
    }

    .hero-body {
        font-size: 1.15rem;
        color: #A6A6A6;
        margin-bottom: 2rem;
        line-height: 1.55;
    }

    /* Streamlit Form Container */
    [data-testid="stForm"] {
        background-color: #111111 !important;
        border: 1.5px solid #282828 !important;
        border-radius: 20px !important;
        padding: 2rem 2.25rem !important;
        box-shadow: 0 16px 48px rgba(0, 0, 0, 0.45) !important;
        margin-bottom: 0.5rem !important;
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #171717 !important;
        border: 1.5px solid #333333 !important;
        border-radius: 14px !important;
        color: #F5F5F5 !important;
        font-size: 1.2rem !important;
        padding: 1.1rem 1.4rem !important;
        height: 62px !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #FFD21F !important;
        box-shadow: 0 0 0 2px #FFD21F33 !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #666666 !important;
    }

    /* Primary Buttons */
    button[kind="primary"],
    button[kind="primaryFormSubmit"],
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    [data-testid*="primary"] {
        background-color: #FFD21F !important;
        color: #0A0A0A !important;
        border: none !important;
        border-radius: 14px !important;
        font-size: 1.15rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.04em !important;
        padding: 1rem 2rem !important;
        height: 58px !important;
        width: 100% !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
    }

    button[kind="primary"]:hover,
    button[kind="primaryFormSubmit"]:hover,
    .stButton > button[kind="primary"]:hover,
    .stFormSubmitButton > button:hover,
    [data-testid*="primary"]:hover {
        background-color: #FFE45C !important;
        color: #0A0A0A !important;
        transform: translateY(-1px) !important;
    }

    /* Secondary Buttons / Nav Buttons */
    button[kind="secondary"], .stButton > button[kind="secondary"], .stButton > button {
        background-color: #171717 !important;
        color: #F5F5F5 !important;
        border: 1px solid #2C2C2C !important;
        border-radius: 12px !important;
        font-size: 1rem !important;
        font-weight: 700 !important;
        padding: 0.75rem 1.25rem !important;
        min-height: 46px !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
    }

    button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover, .stButton > button:hover {
        background-color: #222222 !important;
        border-color: #FFD21F66 !important;
        color: #FFD21F !important;
    }

    /* Minimal Example Link Chips */
    .example-title {
        font-size: 0.92rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: #888888;
        margin-top: 1.75rem;
        margin-bottom: 0.75rem;
    }

    /* Input helper note */
    .input-helper {
        font-size: 0.9rem;
        color: #777777;
        margin-top: 0.6rem;
        text-align: center;
    }

    /* Card Containers */
    .consumer-card {
        background-color: #111111;
        border: 1px solid #292929;
        border-radius: 16px;
        padding: 1.5rem;
        margin-bottom: 1.25rem;
    }

    .url-checked-box {
        background-color: #111111;
        border: 1px solid #292929;
        border-radius: 12px;
        padding: 0.85rem 1.15rem;
        margin-bottom: 1.5rem;
    }

    .url-checked-label {
        font-size: 0.78rem;
        font-weight: 700;
        color: #A6A6A6;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem;
    }

    .url-checked-value {
        font-size: 0.98rem;
        color: #F5F5F5;
        word-break: break-all;
        font-family: -apple-system, BlinkMacSystemFont, monospace;
        line-height: 1.4;
    }

    /* Result State Banners */
    .result-banner {
        border-radius: 20px;
        padding: 2.25rem 2rem;
        margin-bottom: 1.75rem;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.85rem;
    }

    .result-banner-safe {
        background-color: #0C1E14;
        border: 1.5px solid #1E5032;
    }

    .result-banner-suspicious {
        background-color: #211A04;
        border: 1.5px solid #54430D;
    }

    .result-banner-dangerous {
        background-color: #210C0F;
        border: 1.5px solid #571C23;
    }

    .result-icon-badge {
        font-size: 2.6rem;
        line-height: 1;
        margin-bottom: 0.25rem;
    }

    .result-heading-safe {
        font-size: clamp(2rem, 4.5vw, 2.7rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #22C55E;
        line-height: 1.15;
    }

    .result-heading-suspicious {
        font-size: clamp(2rem, 4.5vw, 2.7rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #FFD21F;
        line-height: 1.15;
    }

    .result-heading-dangerous {
        font-size: clamp(2rem, 4.5vw, 2.7rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #EF4444;
        line-height: 1.15;
    }

    .result-subheading {
        font-size: 1.3rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-top: -0.2rem;
    }

    .result-explainer {
        font-size: 1.15rem;
        color: #D4D4D4;
        line-height: 1.55;
        margin-top: 0.25rem;
    }

    /* Score Bar */
    .score-container {
        background-color: #111111;
        border: 1px solid #292929;
        border-radius: 18px;
        padding: 1.5rem 1.75rem;
        margin-bottom: 1.75rem;
    }

    .score-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.85rem;
    }

    .score-label {
        font-size: 0.9rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #A6A6A6;
    }

    .score-num {
        font-size: 1.85rem;
        font-weight: 900;
        color: #F5F5F5;
    }

    .score-max {
        font-size: 1.05rem;
        font-weight: 600;
        color: #777777;
    }

    .score-track {
        width: 100%;
        height: 14px;
        background-color: #1F1F1F;
        border-radius: 999px;
        overflow: hidden;
    }

    .score-fill-safe {
        height: 100%;
        background-color: #22C55E;
        border-radius: 999px;
        transition: width 0.4s ease;
    }

    .score-fill-suspicious {
        height: 100%;
        background-color: #FFD21F;
        border-radius: 999px;
        transition: width 0.4s ease;
    }

    .score-fill-dangerous {
        height: 100%;
        background-color: #EF4444;
        border-radius: 999px;
        transition: width 0.4s ease;
    }

    /* Why Section Items */
    .section-title {
        font-size: 0.95rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #A6A6A6;
        margin-bottom: 1rem;
        margin-top: 1.75rem;
    }

    .signal-item {
        background-color: #141414;
        border: 1px solid #242424;
        border-radius: 14px;
        padding: 1.15rem 1.35rem;
        margin-bottom: 0.75rem;
    }

    .signal-title-safe {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .signal-title-warn {
        font-size: 1.05rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 0.25rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .signal-desc {
        font-size: 0.95rem;
        color: #A6A6A6;
        line-height: 1.5;
    }

    /* Recommended Action Box */
    .action-box {
        background-color: #181818;
        border-left: 5px solid #FFD21F;
        border-radius: 0 14px 14px 0;
        padding: 1.35rem 1.6rem;
        margin-top: 1.75rem;
        margin-bottom: 2.25rem;
    }

    .action-box-dangerous {
        background-color: #181818;
        border-left: 5px solid #EF4444;
        border-radius: 0 14px 14px 0;
        padding: 1.35rem 1.6rem;
        margin-top: 1.75rem;
        margin-bottom: 2.25rem;
    }

    .action-label {
        font-size: 0.85rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #A6A6A6;
        margin-bottom: 0.4rem;
    }

    .action-text {
        font-size: 1.12rem;
        font-weight: 600;
        color: #F5F5F5;
        line-height: 1.5;
    }

    /* Consumer Education Cards */
    .edu-card {
        background-color: #111111;
        border: 1px solid #292929;
        border-radius: 16px;
        padding: 1.6rem;
        margin-bottom: 1.25rem;
    }

    .edu-num {
        font-size: 0.9rem;
        font-weight: 800;
        color: #FFD21F;
        margin-bottom: 0.4rem;
    }

    .edu-title {
        font-size: 1.25rem;
        font-weight: 800;
        color: #F5F5F5;
        margin-bottom: 0.4rem;
    }

    .edu-desc {
        font-size: 1.05rem;
        color: #A6A6A6;
        line-height: 1.55;
    }

    /* Disclaimer */
    .simple-footer {
        text-align: center;
        font-size: 0.82rem;
        color: #555555;
        margin-top: 3rem;
        line-height: 1.5;
    }

    /* Error Banner */
    .error-banner {
        background-color: #1F1012;
        border: 1px solid #4D1E25;
        border-radius: 10px;
        color: #F87171;
        padding: 0.85rem 1.15rem;
        font-size: 0.95rem;
        font-weight: 600;
        margin-bottom: 1.25rem;
    }
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# HUMAN TRANSLATION HELPER FOR THREAT SIGNALS
# ==============================================================================
def humanize_threat_indicator(indicator: str, description: str) -> dict:
    """
    Translates raw technical finding into simple, friendly consumer language.
    Does not expose technical feature names.
    """
    ind_lower = indicator.lower()

    if "raw ip" in ind_lower or "ip address" in ind_lower:
        return {
            "title": "Number-only website address",
            "desc": "This link uses a raw number address instead of a recognized website name."
        }
    elif "shortening" in ind_lower or "shortener" in ind_lower:
        return {
            "title": "Hidden destination",
            "desc": "This link uses a shortening service that hides where it actually leads."
        }
    elif "@ symbol" in ind_lower or "@" in ind_lower:
        return {
            "title": "Deceptive address masking",
            "desc": "Contains an '@' symbol, which can hide the real destination you are being sent to."
        }
    elif "double slash" in ind_lower:
        return {
            "title": "Hidden address redirection",
            "desc": "Contains redirect markers in the address path that may send you to an unexpected page."
        }
    elif "hyphen" in ind_lower or "prefix" in ind_lower:
        return {
            "title": "Suspicious website name",
            "desc": "The website name contains hyphens, a pattern often used to mimic trusted brands."
        }
    elif "multiple subdomain" in ind_lower or "subdomain" in ind_lower:
        return {
            "title": "Unusual address structure",
            "desc": "The web address has multiple sub-names stacked together to appear authentic."
        }
    elif "excessive url length" in ind_lower or "length" in ind_lower:
        return {
            "title": "Unusually long link",
            "desc": "This web address is unusually long, which can be used to hide the true destination."
        }
    elif "non-standard port" in ind_lower or "port" in ind_lower:
        return {
            "title": "Unusual network port",
            "desc": "The link connects through an unusual port rather than normal website traffic."
        }
    elif "fake 'https'" in ind_lower or "https token" in ind_lower:
        return {
            "title": "Deceptive 'https' in name",
            "desc": "The letters 'https' are placed inside the website name itself to create a false impression of security."
        }
    elif "malformed" in ind_lower or "abnormal" in ind_lower:
        return {
            "title": "Unrecognized address format",
            "desc": "The web address structure doesn't match standard website naming rules."
        }
    elif "insecure http" in ind_lower or "http protocol" in ind_lower:
        return {
            "title": "Unsecured connection",
            "desc": "This link does not use secure HTTPS encryption, so data could be intercepted."
        }
    elif "keyword" in ind_lower:
        return {
            "title": "Deceptive words",
            "desc": "The link contains words commonly used to make fake login or account verification pages look official."
        }
    elif "tld" in ind_lower:
        return {
            "title": "High-risk domain ending",
            "desc": "The link ends in a domain extension frequently associated with spam or scam websites."
        }
    elif "punycode" in ind_lower or "homograph" in ind_lower:
        return {
            "title": "Lookalike character disguise",
            "desc": "Uses special character encoding that visually impersonates another website."
        }
    elif "entropy" in ind_lower:
        return {
            "title": "Scrambled character string",
            "desc": "Contains a scrambled sequence of random characters often used in automated attack links."
        }
    else:
        return {
            "title": "Unusual web address pattern",
            "desc": description if description else "This web address exhibits structural patterns commonly seen in suspicious links."
        }


def validate_input_url(url: str) -> tuple[bool, str]:
    """Basic validation for consumer input URL."""
    cleaned = url.strip()
    if not cleaned:
        return False, "Paste a link to check it."

    # Reject whitespace-only or single weird characters
    if len(cleaned) < 3 or " " in cleaned:
        return False, "That doesn't look like a valid web address. Check the link and try again."

    # Basic dot or scheme presence check
    if "." not in cleaned and not cleaned.startswith("http"):
        return False, "That doesn't look like a valid web address. Check the link and try again."

    return True, ""


# ==============================================================================
# SESSION STATE INITIALIZATION
# ==============================================================================
if "active_page" not in st.session_state:
    st.session_state.active_page = "home"

if "scanned_result" not in st.session_state:
    st.session_state.scanned_result = None

if "scanned_url" not in st.session_state:
    st.session_state.scanned_url = ""

if "input_url" not in st.session_state:
    st.session_state.input_url = ""

if "error_message" not in st.session_state:
    st.session_state.error_message = None


def navigate_to(page: str):
    st.session_state.active_page = page
    st.session_state.error_message = None
    if page == "home":
        st.session_state.scanned_result = None
        st.session_state.input_url = ""


def run_url_check(url_to_check: str):
    valid, err = validate_input_url(url_to_check)
    if not valid:
        st.session_state.error_message = err
        st.session_state.scanned_result = None
        return

    st.session_state.error_message = None
    try:
        with st.spinner("CHECKING LINK..."):
            report = predict_url(url_to_check)
        st.session_state.scanned_result = report
        st.session_state.scanned_url = url_to_check
        st.session_state.active_page = "home"
    except Exception:
        st.session_state.error_message = "Something went wrong while checking this link. Please try again."
        st.session_state.scanned_result = None


# ==============================================================================
# MINIMAL BRAND HEADER & NAVIGATION
# ==============================================================================
col_logo, col_nav1, col_nav2, col_nav3 = st.columns([3.2, 1.2, 1.6, 1.4])

with col_logo:
    st.markdown("""
    <div class="brand-logo">
        <span class="brand-dot"></span> CYBERSENTINEL
    </div>
    """, unsafe_allow_html=True)

with col_nav1:
    if st.button("Home", key="nav_home", use_container_width=True):
        navigate_to("home")

with col_nav2:
    if st.button("How It Works", key="nav_how", use_container_width=True):
        navigate_to("how_it_works")

with col_nav3:
    if st.button("Safety Tips", key="nav_tips", use_container_width=True):
        navigate_to("safety_tips")

st.markdown('<div style="height: 1px; background-color: #1A1A1A; margin-bottom: 1.75rem;"></div>', unsafe_allow_html=True)


# ==============================================================================
# PAGE 1: HOW IT WORKS
# ==============================================================================
if st.session_state.active_page == "how_it_works":
    st.markdown('<div class="hero-eyebrow">SIMPLE & TRANSPARENT</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title-main">HOW IT WORKS</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-body">Three simple steps to keep yourself safe before clicking unknown links.</div>', unsafe_allow_html=True)

    st.markdown("""
    <div class="edu-card">
        <div class="edu-num">STEP 01</div>
        <div class="edu-title">PASTE YOUR LINK</div>
        <div class="edu-desc">Copy the link you want to check from your text message, email, or social media.</div>
    </div>

    <div class="edu-card">
        <div class="edu-num">STEP 02</div>
        <div class="edu-title">CHECK IT</div>
        <div class="edu-desc">CyberSentinel analyzes the web address looking for warning signs, hidden destinations, and deceptive tricks.</div>
    </div>

    <div class="edu-card">
        <div class="edu-num">STEP 03</div>
        <div class="edu-title">UNDERSTAND THE RESULT</div>
        <div class="edu-desc">We explain what the result means in plain English, give you an easy-to-read Safety Score, and tell you what you should do next.</div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    if st.button("CHECK A LINK NOW", type="primary", key="how_btn"):
        navigate_to("home")


# ==============================================================================
# PAGE 2: SAFETY TIPS
# ==============================================================================
elif st.session_state.active_page == "safety_tips":
    # Wide layout override for Safety Tips page
    st.markdown("""
    <style>
        section[data-testid="stMain"] > div.main > div.block-container,
        .main > div.block-container,
        .main .block-container {
            max-width: 1200px !important;
            width: 100% !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }
        [data-testid="stMainBlockContainer"] {
            max-width: 1200px !important;
            margin-left: auto !important;
            margin-right: auto !important;
        }

        /* ---- Safety Tips Page ---- */
        .st-hero-split {
            display: grid;
            grid-template-columns: 1.15fr 0.85fr;
            gap: 3rem;
            align-items: center;
            padding: 2rem 0 3.5rem 0;
        }

        .st-hero-left h1 {
            font-size: clamp(2.8rem, 5.5vw, 4.2rem);
            font-weight: 900;
            line-height: 1.06;
            letter-spacing: -0.035em;
            color: #F5F5F5;
            margin: 0 0 1.25rem 0;
        }

        .st-hero-left h1 span {
            color: #FFD21F;
        }

        .st-hero-left p {
            font-size: 1.2rem;
            color: #A6A6A6;
            line-height: 1.6;
            max-width: 480px;
        }

        .st-hero-right {
            position: relative;
            display: flex;
            justify-content: center;
            align-items: flex-end;
        }

        /* Speech bubble styling */
        .speech-bubble-grandpa {
            position: absolute;
            top: 10px;
            right: 12px;
            background: #1A1A1A;
            border: 2px solid #FFD21F;
            border-radius: 14px 14px 4px 14px;
            padding: 0.7rem 1.1rem;
            font-size: 0.95rem;
            font-weight: 800;
            color: #FFD21F;
            letter-spacing: 0.02em;
            white-space: nowrap;
            z-index: 10;
        }

        .speech-bubble-grandpa::after {
            content: '';
            position: absolute;
            bottom: -10px;
            right: 16px;
            border: 6px solid transparent;
            border-top-color: #FFD21F;
        }

        .speech-bubble-grandma {
            position: absolute;
            top: 18px;
            left: 10px;
            background: #1A1A1A;
            border: 2px solid #A6A6A6;
            border-radius: 14px 14px 14px 4px;
            padding: 0.7rem 1.1rem;
            font-size: 0.95rem;
            font-weight: 700;
            color: #F5F5F5;
            letter-spacing: 0.01em;
            max-width: 220px;
            line-height: 1.45;
            z-index: 10;
        }

        /* Section dividers */
        .tip-section-divider {
            width: 100%;
            height: 1px;
            background: linear-gradient(90deg, transparent, #292929, transparent);
            margin: 3.5rem 0;
        }

        /* Grandpa Warning Section */
        .grandpa-warning-section {
            display: grid;
            grid-template-columns: 0.9fr 1.3fr;
            gap: 3.5rem;
            align-items: center;
            padding: 2.5rem 0;
        }

        .grandpa-char-col {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .grandpa-warning-text h2 {
            font-size: clamp(1.8rem, 3.5vw, 2.5rem);
            font-weight: 900;
            letter-spacing: -0.025em;
            color: #F5F5F5;
            margin: 0 0 0.4rem 0;
        }

        .grandpa-warning-text .grandpa-quote {
            font-size: clamp(1.3rem, 2.5vw, 1.8rem);
            font-weight: 800;
            color: #FFD21F;
            font-style: italic;
            margin-bottom: 1.75rem;
        }

        .grandpa-warning-text p {
            font-size: 1.15rem;
            color: #A6A6A6;
            line-height: 1.65;
        }

        /* Warning sign visual */
        .warning-sign-visual {
            display: flex;
            align-items: center;
            gap: 1rem;
            background: #181818;
            border: 1.5px solid #FFD21F33;
            border-radius: 14px;
            padding: 1.15rem 1.4rem;
            margin-bottom: 1.35rem;
        }

        .warning-sign-visual .warn-icon {
            font-size: 1.85rem;
            flex-shrink: 0;
        }

        .warning-sign-visual .warn-text {
            font-size: 1.05rem;
            font-weight: 600;
            color: #F5F5F5;
            line-height: 1.45;
        }

        /* Grandma Section */
        .grandma-tips-section {
            display: grid;
            grid-template-columns: 1.35fr 0.85fr;
            gap: 3.5rem;
            align-items: start;
            padding: 2.5rem 0;
        }

        .grandma-tips-col h2 {
            font-size: clamp(1.6rem, 3vw, 2.3rem);
            font-weight: 900;
            letter-spacing: -0.025em;
            color: #F5F5F5;
            margin: 0 0 0.4rem 0;
        }

        .grandma-tips-col .grandma-quote {
            font-size: 1.15rem;
            color: #A6A6A6;
            font-style: italic;
            margin-bottom: 2rem;
            line-height: 1.55;
        }

        /* Tip Cards */
        .tip-card {
            display: flex;
            gap: 1.25rem;
            background: #111111;
            border: 1px solid #282828;
            border-radius: 16px;
            padding: 1.35rem 1.5rem;
            margin-bottom: 1rem;
            align-items: flex-start;
            transition: border-color 0.2s ease;
        }

        .tip-card:hover {
            border-color: #FFD21F44;
        }

        .tip-num {
            font-size: 0.85rem;
            font-weight: 900;
            color: #FFD21F;
            letter-spacing: 0.06em;
            text-transform: uppercase;
            padding-top: 0.2rem;
            min-width: 30px;
        }

        .tip-body h3 {
            font-size: 1.08rem;
            font-weight: 800;
            color: #F5F5F5;
            margin: 0 0 0.35rem 0;
            letter-spacing: 0.01em;
        }

        .tip-body p {
            font-size: 0.98rem;
            color: #A6A6A6;
            line-height: 1.55;
            margin: 0;
        }

        .grandma-char-col {
            position: relative;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        /* Final CTA Section */
        .final-cta-section {
            text-align: center;
            padding: 4rem 0 2.5rem 0;
            border-top: 1px solid #1E1E1E;
        }

        .final-cta-section .cta-eyebrow {
            font-size: 0.92rem;
            font-weight: 700;
            letter-spacing: 0.1em;
            text-transform: uppercase;
            color: #A6A6A6;
            margin-bottom: 0.6rem;
        }

        .final-cta-section h2 {
            font-size: clamp(2.2rem, 4.5vw, 3.2rem);
            font-weight: 900;
            letter-spacing: -0.03em;
            color: #F5F5F5;
            margin: 0 0 0.5rem 0;
        }

        .final-cta-section h2 span {
            color: #FFD21F;
        }

        .final-cta-section p {
            font-size: 1.15rem;
            color: #A6A6A6;
            margin: 0 0 2.5rem 0;
        }

        /* Grandpa says callout */
        .grandpa-final-callout {
            display: inline-flex;
            align-items: center;
            gap: 0.85rem;
            background: #181818;
            border: 1.5px solid #FFD21F33;
            border-radius: 50px;
            padding: 0.75rem 1.6rem;
            margin-bottom: 1.75rem;
        }

        .grandpa-final-callout .callout-label {
            font-size: 0.85rem;
            font-weight: 800;
            text-transform: uppercase;
            letter-spacing: 0.08em;
            color: #FFD21F;
        }

        .grandpa-final-callout .callout-text {
            font-size: 1.05rem;
            color: #F5F5F5;
            font-weight: 600;
            font-style: italic;
        }

        /* Responsive mobile adjustments */
        @media (max-width: 768px) {
            .st-hero-split,
            .grandpa-warning-section,
            .grandma-tips-section {
                grid-template-columns: 1fr !important;
            }
            .st-hero-right,
            .grandpa-char-col,
            .grandma-char-col {
                order: -1;
            }
        }
    </style>
    """, unsafe_allow_html=True)

    # ==================================================================
    # GRANDPA SVG CHARACTER — Dark CyberSentinel style
    # ==================================================================
    GRANDPA_SVG = """
    <svg viewBox="0 0 320 420" xmlns="http://www.w3.org/2000/svg" width="260" style="filter: drop-shadow(0 20px 60px rgba(0,0,0,0.85));">
      <!-- Subtle spotlight glow behind character -->
      <defs>
        <radialGradient id="gpSpot" cx="50%" cy="40%" r="50%">
          <stop offset="0%" stop-color="#FFD21F" stop-opacity="0.08"/>
          <stop offset="100%" stop-color="#000" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="skinG" cx="40%" cy="35%" r="60%">
          <stop offset="0%" stop-color="#f5c8a8"/>
          <stop offset="100%" stop-color="#d49070"/>
        </radialGradient>
        <radialGradient id="cheekG" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#e8a080" stop-opacity="0.6"/>
          <stop offset="100%" stop-color="#e8a080" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <!-- Background glow -->
      <ellipse cx="160" cy="180" rx="140" ry="160" fill="url(#gpSpot)"/>

      <!-- BODY / DARK OUTFIT -->
      <!-- Torso dark charcoal jacket -->
      <ellipse cx="160" cy="360" rx="90" ry="70" fill="#1A1A1A"/>
      <rect x="80" y="300" width="160" height="100" rx="18" fill="#1C1C1C"/>
      <!-- Shirt collar / white shirt peek -->
      <path d="M145 302 Q160 295 175 302 L172 320 Q160 315 148 320 Z" fill="#EBEBEB"/>
      <!-- Dark jacket lapels -->
      <path d="M145 302 L110 340 L130 340 L148 320 Z" fill="#252525"/>
      <path d="M175 302 L210 340 L190 340 L172 320 Z" fill="#252525"/>
      <!-- Bow tie (dark with tiny yellow) -->
      <path d="M148 310 L160 318 L172 310 L165 303 L160 307 L155 303 Z" fill="#1a1a1a"/>
      <circle cx="160" cy="312" r="3" fill="#FFD21F"/>
      <!-- Dark suspenders -->
      <rect x="143" y="305" width="7" height="75" rx="3" fill="#2A2A2A" transform="rotate(-5, 143 305)"/>
      <rect x="170" y="305" width="7" height="75" rx="3" fill="#2A2A2A" transform="rotate(5, 177 305)"/>
      <!-- Yellow suspender clips -->
      <rect x="139" y="340" width="14" height="8" rx="2" fill="#FFD21F"/>
      <rect x="167" y="340" width="14" height="8" rx="2" fill="#FFD21F"/>
      <!-- Yellow shield badge on chest -->
      <path d="M152 330 L160 326 L168 330 L168 340 Q160 345 152 340 Z" fill="#FFD21F"/>
      <path d="M155 334 L158 338 L165 331" stroke="#0A0A0A" stroke-width="2" fill="none" stroke-linecap="round"/>

      <!-- STOP HAND (raised right arm) -->
      <!-- Upper arm -->
      <rect x="205" y="295" width="35" height="55" rx="17" fill="#f0b896" transform="rotate(-25 222 322)"/>
      <!-- Forearm / stop hand rotated up -->
      <g transform="translate(225, 225) rotate(15)">
        <!-- Palm -->
        <rect x="-22" y="-10" width="44" height="50" rx="14" fill="#f0b896"/>
        <!-- Fingers spread slightly -->
        <rect x="-20" y="-30" width="10" height="32" rx="5" fill="#f0b896"/>
        <rect x="-8" y="-36" width="10" height="34" rx="5" fill="#f0b896"/>
        <rect x="4" y="-34" width="10" height="32" rx="5" fill="#f0b896"/>
        <rect x="16" y="-28" width="9" height="28" rx="4" fill="#f0b896"/>
        <!-- Knuckle lines -->
        <line x1="-19" y1="-2" x2="-19" y2="2" stroke="#c89070" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="-7" y1="-4" x2="-7" y2="0" stroke="#c89070" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="5" y1="-3" x2="5" y2="1" stroke="#c89070" stroke-width="1.5" stroke-linecap="round"/>
        <line x1="16" y1="-1" x2="16" y2="3" stroke="#c89070" stroke-width="1.5" stroke-linecap="round"/>
      </g>
      <!-- Left arm relaxed -->
      <rect x="75" y="295" width="33" height="52" rx="16" fill="#1C1C1C" transform="rotate(15 91 321)"/>

      <!-- NECK -->
      <rect x="148" y="272" width="24" height="35" rx="10" fill="#e0a880"/>

      <!-- HEAD -->
      <!-- Head shape - rounded square, mature -->
      <rect x="105" y="155" width="110" height="125" rx="38" fill="url(#skinG)"/>
      <!-- Forehead wrinkle lines -->
      <path d="M125 175 Q140 170 155 173" stroke="#c49070" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      <path d="M165 172 Q175 169 185 173" stroke="#c49070" stroke-width="1.5" fill="none" stroke-linecap="round"/>
      <!-- Jowls / cheeks -->
      <ellipse cx="118" cy="225" rx="14" ry="16" fill="#e09878" opacity="0.5"/>
      <ellipse cx="202" cy="225" rx="14" ry="16" fill="#e09878" opacity="0.5"/>
      <!-- Cheek flush -->
      <ellipse cx="122" cy="228" rx="10" ry="7" fill="url(#cheekG)"/>
      <ellipse cx="198" cy="228" rx="10" ry="7" fill="url(#cheekG)"/>

      <!-- GRUMPY FURROWED BROW -->
      <!-- Brow shadow -->
      <rect x="108" y="190" width="104" height="22" rx="11" fill="#c08060" opacity="0.3"/>
      <!-- Left brow — furrowed down-inward -->
      <path d="M112 200 Q130 188 148 196" stroke="#4a3020" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <!-- Right brow — furrowed down-inward -->
      <path d="M172 196 Q188 188 205 200" stroke="#4a3020" stroke-width="5.5" fill="none" stroke-linecap="round"/>
      <!-- Brow crease between brows -->
      <path d="M152 198 L160 202 L168 198" stroke="#b07850" stroke-width="2" fill="none" stroke-linecap="round"/>

      <!-- EYES -->
      <!-- Left eye socket shadow -->
      <ellipse cx="138" cy="215" rx="17" ry="13" fill="#c09070" opacity="0.2"/>
      <!-- Left eyeball -->
      <ellipse cx="138" cy="216" rx="12" ry="11" fill="white"/>
      <ellipse cx="139" cy="217" rx="7" ry="7" fill="#3a6090"/>
      <circle cx="140" cy="216" r="4.5" fill="#1a2030"/>
      <circle cx="142" cy="214" r="1.5" fill="white"/>
      <!-- Left eyelid (half-closed, skeptical) -->
      <path d="M126 212 Q138 206 150 212" fill="#e0a880" stroke="#e0a880" stroke-width="0.5"/>
      <!-- Right eye socket shadow -->
      <ellipse cx="182" cy="215" rx="17" ry="13" fill="#c09070" opacity="0.2"/>
      <!-- Right eyeball -->
      <ellipse cx="182" cy="216" rx="12" ry="11" fill="white"/>
      <ellipse cx="183" cy="217" rx="7" ry="7" fill="#3a6090"/>
      <circle cx="184" cy="216" r="4.5" fill="#1a2030"/>
      <circle cx="186" cy="214" r="1.5" fill="white"/>
      <!-- Right eyelid (half-closed) -->
      <path d="M170 212 Q182 206 194 212" fill="#e0a880" stroke="#e0a880" stroke-width="0.5"/>

      <!-- THICK BLACK GLASSES — distinctive feature -->
      <!-- Left lens frame -->
      <rect x="118" y="205" width="42" height="28" rx="6" fill="none" stroke="#1a1a1a" stroke-width="6"/>
      <!-- Right lens frame -->
      <rect x="160" y="205" width="42" height="28" rx="6" fill="none" stroke="#1a1a1a" stroke-width="6"/>
      <!-- Bridge between lenses -->
      <rect x="158" y="215" width="6" height="6" rx="1" fill="#1a1a1a"/>
      <!-- Left temple arm -->
      <line x1="118" y1="218" x2="105" y2="222" stroke="#1a1a1a" stroke-width="5" stroke-linecap="round"/>
      <!-- Right temple arm -->
      <line x1="202" y1="218" x2="215" y2="222" stroke="#1a1a1a" stroke-width="5" stroke-linecap="round"/>
      <!-- Lens tint (slightly dark, subtle) -->
      <rect x="121" y="208" width="36" height="22" rx="4" fill="#111122" opacity="0.12"/>
      <rect x="163" y="208" width="36" height="22" rx="4" fill="#111122" opacity="0.12"/>

      <!-- NOSE — large bulbous -->
      <ellipse cx="160" cy="238" rx="14" ry="12" fill="#d49878"/>
      <circle cx="153" cy="242" r="5" fill="#c48868"/>
      <circle cx="167" cy="242" r="5" fill="#c48868"/>

      <!-- MOUTH — grumpy frown -->
      <path d="M138 260 Q148 255 160 257 Q172 255 182 260" stroke="#9a6040" stroke-width="3" fill="none" stroke-linecap="round"/>
      <!-- Chin crease -->
      <path d="M150 270 Q160 275 170 270" stroke="#c09070" stroke-width="1.5" fill="none" stroke-linecap="round"/>

      <!-- WHITE HAIR -->
      <!-- Main hair mass -->
      <ellipse cx="160" cy="155" rx="58" ry="32" fill="#E8E8E8"/>
      <!-- Side tufts -->
      <ellipse cx="108" cy="175" rx="22" ry="30" fill="#E0E0E0"/>
      <ellipse cx="212" cy="175" rx="22" ry="30" fill="#E0E0E0"/>
      <!-- Top fluffy section -->
      <path d="M120 155 Q130 130 145 140 Q155 125 175 140 Q190 130 200 155" fill="#EBEBEB"/>
      <!-- Hair highlight -->
      <path d="M138 143 Q155 133 175 143" stroke="white" stroke-width="4" fill="none" stroke-linecap="round" opacity="0.6"/>

      <!-- Ear left -->
      <ellipse cx="106" cy="220" rx="10" ry="14" fill="#d4946a"/>
      <ellipse cx="107" cy="220" rx="6" ry="9" fill="#c48060"/>
      <!-- Ear right -->
      <ellipse cx="214" cy="220" rx="10" ry="14" fill="#d4946a"/>
      <ellipse cx="213" cy="220" rx="6" ry="9" fill="#c48060"/>
    </svg>
    """

    # ==================================================================
    # GRANDMA SVG CHARACTER — Dark CyberSentinel style
    # ==================================================================
    GRANDMA_SVG = """
    <svg viewBox="0 0 300 440" xmlns="http://www.w3.org/2000/svg" width="240" style="filter: drop-shadow(0 20px 50px rgba(0,0,0,0.8));">
      <defs>
        <radialGradient id="gmSpot" cx="50%" cy="40%" r="50%">
          <stop offset="0%" stop-color="#E8E8E8" stop-opacity="0.06"/>
          <stop offset="100%" stop-color="#000" stop-opacity="0"/>
        </radialGradient>
        <radialGradient id="gmSkin" cx="40%" cy="30%" r="60%">
          <stop offset="0%" stop-color="#f8d0b0"/>
          <stop offset="100%" stop-color="#e0a888"/>
        </radialGradient>
        <radialGradient id="gmCheek" cx="50%" cy="50%" r="50%">
          <stop offset="0%" stop-color="#f09090" stop-opacity="0.55"/>
          <stop offset="100%" stop-color="#f09090" stop-opacity="0"/>
        </radialGradient>
      </defs>
      <ellipse cx="150" cy="200" rx="130" ry="180" fill="url(#gmSpot)"/>

      <!-- BODY — dark elegant outfit -->
      <ellipse cx="150" cy="380" rx="80" ry="65" fill="#181818"/>
      <rect x="78" y="315" width="144" height="90" rx="20" fill="#1E1E1E"/>
      <!-- Pearl necklace -->
      <path d="M118 308 Q150 318 182 308" stroke="none" fill="none"/>
      <circle cx="122" cy="310" r="4" fill="#E8E6E0"/>
      <circle cx="132" cy="313" r="4.5" fill="#F0EEEA"/>
      <circle cx="142" cy="315" r="4.5" fill="#E8E6E0"/>
      <circle cx="152" cy="316" r="5" fill="#F0EEEA"/>
      <circle cx="162" cy="315" r="4.5" fill="#E8E6E0"/>
      <circle cx="172" cy="313" r="4.5" fill="#F0EEEA"/>
      <circle cx="181" cy="310" r="4" fill="#E8E6E0"/>
      <!-- Elegant dark blouse details -->
      <path d="M140 316 Q150 322 160 316 L157 335 Q150 330 143 335 Z" fill="#EBEBEB" opacity="0.9"/>
      <!-- Yellow brooch / pin -->
      <circle cx="150" cy="326" r="7" fill="#FFD21F"/>
      <circle cx="150" cy="326" r="4" fill="#0A0A0A"/>
      <circle cx="150" cy="326" r="2" fill="#FFD21F"/>

      <!-- Arm holding phone — left arm -->
      <rect x="60" y="315" width="30" height="55" rx="15" fill="#1E1E1E" transform="rotate(20 75 342)"/>
      <!-- Phone being held -->
      <rect x="42" y="340" width="40" height="65" rx="8" fill="#1a1a1a"/>
      <rect x="45" y="344" width="34" height="56" rx="5" fill="#0f0f1a"/>
      <!-- Small screen glow on phone -->
      <rect x="47" y="347" width="30" height="28" rx="3" fill="#1a3a5c"/>
      <rect x="49" y="350" width="26" height="4" rx="2" fill="#4080c0" opacity="0.7"/>
      <rect x="49" y="357" width="20" height="3" rx="2" fill="#2060a0" opacity="0.5"/>
      <!-- Right arm -->
      <rect x="210" y="315" width="30" height="50" rx="14" fill="#1E1E1E" transform="rotate(-15 225 340)"/>
      <!-- Right hand gesture (gentle wave) -->
      <ellipse cx="232" cy="358" rx="15" ry="13" fill="#f0c09a"/>
      <rect x="225" y="338" width="10" height="26" rx="5" fill="#f0c09a" transform="rotate(-10 230 351)"/>
      <rect x="235" y="335" width="9" height="26" rx="5" fill="#f0c09a" transform="rotate(5 239 348)"/>

      <!-- NECK -->
      <rect x="138" y="283" width="24" height="38" rx="11" fill="#e8b890"/>

      <!-- HEAD — round cute shape -->
      <ellipse cx="150" cy="210" rx="68" ry="78" fill="url(#gmSkin)"/>
      <!-- Extra round cheeks -->
      <ellipse cx="100" cy="230" rx="22" ry="20" fill="#f0b090" opacity="0.4"/>
      <ellipse cx="200" cy="230" rx="22" ry="20" fill="#f0b090" opacity="0.4"/>
      <!-- Cheek blush -->
      <ellipse cx="104" cy="233" rx="14" ry="9" fill="url(#gmCheek)"/>
      <ellipse cx="196" cy="233" rx="14" ry="9" fill="url(#gmCheek)"/>

      <!-- FRIENDLY RAISED BROWS -->
      <path d="M106 188 Q120 180 135 186" stroke="#6a4030" stroke-width="4" fill="none" stroke-linecap="round"/>
      <path d="M165 186 Q180 180 194 188" stroke="#6a4030" stroke-width="4" fill="none" stroke-linecap="round"/>

      <!-- BIG ROUND EYES — wide awake, friendly -->
      <!-- Left eye area -->
      <ellipse cx="125" cy="215" rx="20" ry="19" fill="white"/>
      <ellipse cx="126" cy="216" rx="12" ry="12" fill="#4a90c8"/>
      <circle cx="127" cy="215" r="8" fill="#1a2a3a"/>
      <circle cx="130" cy="212" r="2.5" fill="white"/>
      <circle cx="124" cy="219" r="1.5" fill="white" opacity="0.6"/>
      <!-- Right eye area -->
      <ellipse cx="175" cy="215" rx="20" ry="19" fill="white"/>
      <ellipse cx="176" cy="216" rx="12" ry="12" fill="#4a90c8"/>
      <circle cx="177" cy="215" r="8" fill="#1a2a3a"/>
      <circle cx="180" cy="212" r="2.5" fill="white"/>
      <circle cx="174" cy="219" r="1.5" fill="white" opacity="0.6"/>
      <!-- Eyelashes top -->
      <path d="M106 208 Q115 200 124 207" stroke="#3a2520" stroke-width="2.5" fill="none" stroke-linecap="round"/>
      <path d="M157 207 Q165 200 174 208" stroke="#3a2520" stroke-width="2.5" fill="none" stroke-linecap="round"/>

      <!-- BIG ROUND GLASSES — gold/yellow frames -->
      <circle cx="125" cy="215" r="24" fill="none" stroke="#C8A020" stroke-width="5"/>
      <circle cx="175" cy="215" r="24" fill="none" stroke="#C8A020" stroke-width="5"/>
      <!-- Bridge -->
      <line x1="149" y1="215" x2="151" y2="215" stroke="#C8A020" stroke-width="5"/>
      <!-- Temple arms -->
      <line x1="102" y1="210" x2="87" y2="217" stroke="#C8A020" stroke-width="4" stroke-linecap="round"/>
      <line x1="198" y1="210" x2="213" y2="217" stroke="#C8A020" stroke-width="4" stroke-linecap="round"/>
      <!-- Lens subtle tint -->
      <circle cx="125" cy="215" r="20" fill="#ffd21f" opacity="0.04"/>
      <circle cx="175" cy="215" r="20" fill="#ffd21f" opacity="0.04"/>

      <!-- SMALL NOSE -->
      <ellipse cx="150" cy="240" rx="8" ry="6" fill="#dda88a"/>
      <!-- Cute small nostrils -->
      <circle cx="146" cy="242" r="3" fill="#cc9878"/>
      <circle cx="154" cy="242" r="3" fill="#cc9878"/>

      <!-- WARM SMILE -->
      <path d="M126 258 Q150 276 174 258" stroke="#c07060" stroke-width="3" fill="none" stroke-linecap="round"/>
      <path d="M130 260 Q150 273 170 260" stroke="#e09080" stroke-width="1.5" fill="#f0a890" opacity="0.4"/>
      <!-- Small smile dimples -->
      <circle cx="124" cy="258" r="3" fill="#e09888"/>
      <circle cx="176" cy="258" r="3" fill="#e09888"/>

      <!-- ELEGANT GREY HAIR in updo -->
      <!-- Main bun on top -->
      <ellipse cx="150" cy="148" rx="40" ry="34" fill="#C8C8C8"/>
      <ellipse cx="150" cy="145" rx="30" ry="26" fill="#D8D8D8"/>
      <!-- Bun highlight -->
      <ellipse cx="143" cy="139" rx="12" ry="8" fill="white" opacity="0.3"/>
      <!-- Side hair swept back -->
      <path d="M83 215 Q88 165 115 155 Q100 200 102 230 Z" fill="#C0C0C0"/>
      <path d="M217 215 Q212 165 185 155 Q200 200 198 230 Z" fill="#C0C0C0"/>
      <!-- Hair wavy detail -->
      <path d="M95 195 Q105 188 115 195" stroke="#B0B0B0" stroke-width="2" fill="none" stroke-linecap="round"/>
      <path d="M185 195 Q195 188 205 195" stroke="#B0B0B0" stroke-width="2" fill="none" stroke-linecap="round"/>

      <!-- Gold hair tiara accent with yellow gem (CyberSentinel yellow) -->
      <path d="M120 153 Q150 138 180 153" stroke="#C8A020" stroke-width="3.5" fill="none" stroke-linecap="round"/>
      <circle cx="150" cy="140" r="6" fill="#FFD21F"/>
      <circle cx="135" cy="146" r="4" fill="#C8A020"/>
      <circle cx="165" cy="146" r="4" fill="#C8A020"/>

      <!-- EARRINGS — small gold hoops -->
      <ellipse cx="83" cy="226" rx="7" ry="9" fill="none" stroke="#C8A020" stroke-width="3"/>
      <ellipse cx="217" cy="226" rx="7" ry="9" fill="none" stroke="#C8A020" stroke-width="3"/>

      <!-- Ears -->
      <ellipse cx="83" cy="220" rx="10" ry="14" fill="#e8b080"/>
      <ellipse cx="217" cy="220" rx="10" ry="14" fill="#e8b080"/>
    </svg>
    """

    # ==================================================================
    # WARNING SIGN SVG (Grandpa's prop)
    # ==================================================================
    WARNING_SVG = """
    <svg viewBox="0 0 100 90" xmlns="http://www.w3.org/2000/svg" width="90" style="filter: drop-shadow(0 4px 20px rgba(255,210,31,0.3));">
      <polygon points="50,5 95,82 5,82" fill="#FFD21F" stroke="#0A0A0A" stroke-width="2"/>
      <polygon points="50,15 87,78 13,78" fill="#FFD21F"/>
      <text x="50" y="65" text-anchor="middle" font-size="38" font-weight="900" fill="#0A0A0A" font-family="sans-serif">!</text>
      <rect x="44" y="30" width="12" height="24" rx="4" fill="#0A0A0A"/>
      <circle cx="50" cy="63" r="6" fill="#0A0A0A"/>
    </svg>
    """

    # ==================================================================
    # HERO SECTION — 2-column desktop layout
    # ==================================================================
    render_html(f"""
    <div class="st-hero-split">
      <div class="st-hero-left">
        <div style="font-size:0.88rem;font-weight:700;letter-spacing:0.1em;text-transform:uppercase;color:#A6A6A6;margin-bottom:0.75rem;">SCAM AWARENESS</div>
        <h1 style="font-size: clamp(2.4rem, 5vw, 3.8rem); line-height: 1.1; font-weight: 900; color: #F5F5F5; margin: 0 0 1rem 0;">SAFETY<br/>STARTS WITH<br/>A <span style="color:#FFD21F;">SECOND LOOK.</span></h1>
        <p style="font-size:1.1rem;color:#A6A6A6;line-height:1.6;max-width:440px;">Scammers only need one click. Learn how to spot the warning signs before you open an unknown link.</p>
      </div>
      <div class="st-hero-right" style="position:relative; min-height: 320px; display:flex; justify-content:center; align-items:flex-end;">
        <div class="speech-bubble-grandpa">WAIT A MINUTE...</div>
        {GRANDPA_SVG}
        <div style="position:absolute;bottom:8px;right:20px;">{WARNING_SVG}</div>
      </div>
    </div>
    """)

    # ==================================================================
    # DIVIDER
    # ==================================================================
    render_html('<div class="tip-section-divider"></div>')

    # ==================================================================
    # GRANDPA WARNING SECTION
    # ==================================================================
    render_html(f"""
    <div class="grandpa-warning-section">
      <div class="grandpa-char-col">
        {GRANDPA_SVG}
        <div style="margin-top:1rem; background:#1A1A1A; border:1.5px solid #FFD21F; border-radius:12px 12px 4px 12px; padding:0.7rem 1rem; text-align:center; max-width:220px;">
          <span style="font-size:0.95rem;font-weight:800;color:#FFD21F;font-style:italic;">"That link looks suspicious to me."</span>
        </div>
      </div>
      <div class="grandpa-warning-text">
        <h2>GRANDPA SAYS:</h2>
        <div class="grandpa-quote">"STOP. LOOK FIRST."</div>
        <p style="margin-bottom:1.5rem;">Grandpa has seen every trick in the book. From fake bank alerts to prize-winning emails — he's not fooled. And neither should you be.</p>

        <div class="warning-sign-visual">
          <div class="warn-icon">⚠️</div>
          <div class="warn-text"><strong style="color:#FFD21F;">You only need to get tricked once.</strong><br/>One wrong click can hand over your password, your money, or your identity.</div>
        </div>
        <div class="warning-sign-visual">
          <div class="warn-icon">🔍</div>
          <div class="warn-text"><strong style="color:#FFD21F;">The warning signs are always there.</strong><br/>Scammers leave footprints. You just need to know where to look.</div>
        </div>
        <div class="warning-sign-visual">
          <div class="warn-icon">⏸️</div>
          <div class="warn-text"><strong style="color:#FFD21F;">Pause before you click.</strong><br/>A second of hesitation can protect your entire digital life.</div>
        </div>
      </div>
    </div>
    """)

    # ==================================================================
    # DIVIDER
    # ==================================================================
    render_html('<div class="tip-section-divider"></div>')

    # ==================================================================
    # GRANDMA TIPS SECTION
    # ==================================================================
    tips_html = ""
    tips = [
        ("01", "CHECK THE WEBSITE NAME",
         "Scammers often use names that look almost like the real thing — like paypa1.com instead of paypal.com. Always read the address carefully."),
        ("02", "DON'T TRUST URGENT MESSAGES",
         "Messages telling you to \"act immediately\" or \"your account is suspended\" are designed to panic you into clicking without thinking."),
        ("03", "BE CAREFUL WITH LOGIN LINKS",
         "Before entering your password, make sure you are really on the website you intended to visit — not a fake copy."),
        ("04", "DON'T SHARE SENSITIVE INFORMATION",
         "Never enter your passwords, payment card details, or personal ID through an unfamiliar or unsolicited link."),
        ("05", "WATCH FOR STRANGE WEB ADDRESSES",
         "Long, confusing, or garbled web addresses deserve a closer look. Check the link before you open it."),
        ("06", "WHEN IN DOUBT, DON'T CLICK",
         "If something feels even slightly off, stop. Trust your instincts and verify through an official app or phone number."),
    ]
    for num, title, desc in tips:
        tips_html += f"""
        <div class="tip-card">
          <div class="tip-num">{num}</div>
          <div class="tip-body">
            <h3>{title}</h3>
            <p>{desc}</p>
          </div>
        </div>"""

    render_html(f"""
    <div class="grandma-tips-section">
      <div class="grandma-tips-col">
        <h2>HERE'S WHAT GRANDMA RECOMMENDS.</h2>
        <div class="grandma-quote">"Come on, dear. Let me show you how to stay safe online."</div>
        {tips_html}
      </div>
      <div class="grandma-char-col">
        <div style="background:#1A1A1A; border:1.5px solid #555; border-radius:14px 14px 4px 14px; padding:0.7rem 1rem; text-align:center; max-width:210px; margin-bottom:1.25rem;">
          <span style="font-size:0.9rem;font-weight:700;color:#F5F5F5;font-style:italic;">"Let me show you what to look for."</span>
        </div>
        {GRANDMA_SVG}
      </div>
    </div>
    """)

    # ==================================================================
    # FINAL CTA SECTION
    # ==================================================================
    render_html('<div class="tip-section-divider"></div>')

    render_html("""
    <div class="final-cta-section">
      <div class="grandpa-final-callout">
        <span class="callout-label">GRANDPA SAYS:</span>
        <span class="callout-text">"Still unsure? Check the link before you click."</span>
      </div>
      <h2>CHECK BEFORE<br/>YOU <span>CLICK.</span></h2>
      <p>CyberSentinel helps you decide in seconds. Paste any link and see what we find.</p>
    </div>
    """)

    if st.button("CHECK A LINK NOW →", type="primary", key="tips_cta_btn"):
        navigate_to("home")
        st.rerun()

    render_html("""
    <div class="simple-footer">
        CyberSentinel · Simple, private, instant link safety checks.
    </div>
    """)


# ==============================================================================
# PAGE 3: HOME / SCANNER & RESULT PAGE
# ==============================================================================
else:
    # --------------------------------------------------------------------------
    # VIEW A: SHOW SCAN RESULT (If a link was checked)
    # --------------------------------------------------------------------------
    if st.session_state.scanned_result is not None:
        report = st.session_state.scanned_result
        checked_url = st.session_state.scanned_url

        # Back / New check action
        if st.button("← Check another link", key="btn_back_top"):
            st.session_state.scanned_result = None
            st.session_state.scanned_url = ""
            st.rerun()

        # 1. Link you checked card
        st.markdown(f"""
        <div class="url-checked-box">
            <div class="url-checked-label">LINK YOU CHECKED</div>
            <div class="url-checked-value">{checked_url}</div>
        </div>
        """, unsafe_allow_html=True)

        # Compute consumer Safety Score (0 - 100, where 100 is cleanest)
        risk = report.get("risk_score", 0.0)
        safety_score = max(0, min(100, int(round(100.0 - risk))))
        verdict = report.get("verdict", "")

        # 2. Result State Display
        if verdict == "Legitimate / Safe":
            # SAFE STATE
            st.markdown(f"""
            <div class="result-banner result-banner-safe">
                <div class="result-icon-badge">🛡️</div>
                <div class="result-heading-safe">THIS LINK LOOKS SAFE</div>
                <div class="result-explainer">We didn't find obvious warning signs in this web address.</div>
            </div>
            """, unsafe_allow_html=True)

            # Safety Score Card
            st.markdown(f"""
            <div class="score-container">
                <div class="score-header">
                    <span class="score-label">SAFETY SCORE</span>
                    <span><span class="score-num">{safety_score}</span><span class="score-max"> / 100</span></span>
                </div>
                <div class="score-track">
                    <div class="score-fill-safe" style="width: {safety_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Why does it look safe?
            st.markdown('<div class="section-title">WHY DOES IT LOOK SAFE?</div>', unsafe_allow_html=True)

            safe_signals = [
                ("No suspicious symbols detected", "Does not contain misleading characters like '@' or hidden redirects."),
                ("Website address has a familiar structure", "The address follows recognized domain naming conventions."),
                ("Direct destination", "Not hidden behind a temporary link shortening service."),
                ("No deceptive hyphens or lookalike names", "Does not use deceptive hyphens to imitate another brand."),
                ("No obvious warning signs found", "The address structure appears standard and consistent.")
            ]

            for s_title, s_desc in safe_signals:
                st.markdown(f"""
                <div class="signal-item">
                    <div class="signal-title-safe">✓ {s_title}</div>
                    <div class="signal-desc">{s_desc}</div>
                </div>
                """, unsafe_allow_html=True)

            # Buttons
            st.write("")
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if st.button("CHECK ANOTHER LINK", type="primary", key="safe_btn_another"):
                    st.session_state.scanned_result = None
                    st.session_state.scanned_url = ""
                    st.rerun()
            with col_b2:
                if st.button("LEARN HOW TO STAY SAFE", type="secondary", key="safe_btn_learn"):
                    navigate_to("safety_tips")
                    st.rerun()

        elif verdict == "Suspicious":
            # SUSPICIOUS STATE (CyberSentinel Yellow)
            st.markdown(f"""
            <div class="result-banner result-banner-suspicious">
                <div class="result-icon-badge">⚠️</div>
                <div class="result-heading-suspicious">BE CAREFUL</div>
                <div class="result-subheading">This link looks suspicious.</div>
                <div class="result-explainer">We found some warning signs in this web address. Check it carefully before opening it.</div>
            </div>
            """, unsafe_allow_html=True)

            # Safety Score Card
            st.markdown(f"""
            <div class="score-container">
                <div class="score-header">
                    <span class="score-label">SAFETY SCORE</span>
                    <span><span class="score-num">{safety_score}</span><span class="score-max"> / 100</span></span>
                </div>
                <div class="score-track">
                    <div class="score-fill-suspicious" style="width: {safety_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Why are we warning you?
            st.markdown('<div class="section-title">WHY ARE WE WARNING YOU?</div>', unsafe_allow_html=True)

            red_flags = report.get("red_flags", [])
            if red_flags:
                for rf in red_flags:
                    item = humanize_threat_indicator(rf.get("indicator", ""), rf.get("description", ""))
                    st.markdown(f"""
                    <div class="signal-item">
                        <div class="signal-title-warn">⚠ {item['title']}</div>
                        <div class="signal-desc">{item['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="signal-item">
                    <div class="signal-title-warn">⚠ Unusual address characteristics</div>
                    <div class="signal-desc">Parts of this web address structure differ from standard legitimate websites.</div>
                </div>
                """, unsafe_allow_html=True)

            # Recommended Action
            st.markdown("""
            <div class="action-box">
                <div class="action-label">RECOMMENDED ACTION</div>
                <div class="action-text">Don't enter passwords, payment details, or personal information unless you are certain the website is genuine.</div>
            </div>
            """, unsafe_allow_html=True)

            # Buttons
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if st.button("CHECK ANOTHER LINK", type="primary", key="susp_btn_another"):
                    st.session_state.scanned_result = None
                    st.session_state.scanned_url = ""
                    st.rerun()
            with col_b2:
                if st.button("LEARN HOW TO SPOT SUSPICIOUS LINKS", type="secondary", key="susp_btn_learn"):
                    navigate_to("safety_tips")
                    st.rerun()

        else:
            # DANGEROUS STATE (Restrained Red)
            st.markdown(f"""
            <div class="result-banner result-banner-dangerous">
                <div class="result-icon-badge">🚫</div>
                <div class="result-heading-dangerous">THIS LINK LOOKS DANGEROUS</div>
                <div class="result-explainer">We found several warning signs in this web address. We recommend not opening it.</div>
            </div>
            """, unsafe_allow_html=True)

            # Safety Score Card
            st.markdown(f"""
            <div class="score-container">
                <div class="score-header">
                    <span class="score-label">SAFETY SCORE</span>
                    <span><span class="score-num">{safety_score}</span><span class="score-max"> / 100</span></span>
                </div>
                <div class="score-track">
                    <div class="score-fill-dangerous" style="width: {safety_score}%;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Why are we warning you?
            st.markdown('<div class="section-title">WHY ARE WE WARNING YOU?</div>', unsafe_allow_html=True)

            red_flags = report.get("red_flags", [])
            if red_flags:
                for rf in red_flags:
                    item = humanize_threat_indicator(rf.get("indicator", ""), rf.get("description", ""))
                    st.markdown(f"""
                    <div class="signal-item">
                        <div class="signal-title-warn" style="color: #F87171;">⚠ {item['title']}</div>
                        <div class="signal-desc">{item['desc']}</div>
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div class="signal-item">
                    <div class="signal-title-warn" style="color: #F87171;">⚠ High risk address patterns detected</div>
                    <div class="signal-desc">This web address matches structural techniques frequently used in phishing attacks.</div>
                </div>
                """, unsafe_allow_html=True)

            # Recommended Action (Strict: No proceed anyway)
            st.markdown("""
            <div class="action-box-dangerous">
                <div class="action-label" style="color: #F87171;">RECOMMENDED ACTION</div>
                <div class="action-text">Don't open this link or enter any personal information.</div>
            </div>
            """, unsafe_allow_html=True)

            # Buttons
            col_b1, col_b2 = st.columns([1, 1])
            with col_b1:
                if st.button("CHECK ANOTHER LINK", type="primary", key="dang_btn_another"):
                    st.session_state.scanned_result = None
                    st.session_state.scanned_url = ""
                    st.rerun()
            with col_b2:
                if st.button("LEARN HOW TO STAY SAFE", type="secondary", key="dang_btn_learn"):
                    navigate_to("safety_tips")
                    st.rerun()

        # Education footer
        st.markdown("""
        <div class="simple-footer">
            CyberSentinel inspects web address structure to help you make informed decisions.<br/>
            Always verify unfamiliar links before sharing personal data.
        </div>
        """, unsafe_allow_html=True)

    # --------------------------------------------------------------------------
    # VIEW B: HOME HERO & SEARCH INPUT (Default State)
    # --------------------------------------------------------------------------
    else:
        st.markdown('<div class="hero-title-main">DON\'T CLICK.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-title-yellow">CHECK FIRST.</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-subhead">Is this link safe?</div>', unsafe_allow_html=True)
        st.markdown('<div class="hero-body">Check a link before you open it.</div>', unsafe_allow_html=True)

        # Show error message if any
        if st.session_state.error_message:
            st.markdown(f'<div class="error-banner">{st.session_state.error_message}</div>', unsafe_allow_html=True)

        # Search Form
        with st.form("check_link_form", clear_on_submit=False):
            url_input = st.text_input(
                label="Enter URL to check",
                value=st.session_state.input_url,
                placeholder="Paste a link here...",
                label_visibility="collapsed"
            )

            submit_clicked = st.form_submit_button("CHECK LINK", type="primary")

        st.markdown('<div class="input-helper">Don\'t click it yet. Check it first.</div>', unsafe_allow_html=True)

        if submit_clicked:
            run_url_check(url_input)
            st.rerun()

        # Quick Example Chips
        st.markdown('<div class="example-title">Try an example</div>', unsafe_allow_html=True)
        ex_col1, ex_col2, ex_col3 = st.columns(3)

        with ex_col1:
            if st.button("google.com", key="ex_google", use_container_width=True):
                st.session_state.input_url = "https://www.google.com"
                run_url_check("https://www.google.com")
                st.rerun()

        with ex_col2:
            if st.button("bit.ly/secure-account", key="ex_bitly", use_container_width=True):
                st.session_state.input_url = "https://bit.ly/secure-account"
                run_url_check("https://bit.ly/secure-account")
                st.rerun()

        with ex_col3:
            if st.button("paypal-security.com", key="ex_paypal", use_container_width=True):
                st.session_state.input_url = "http://paypal-security-update.com/verify"
                run_url_check("http://paypal-security-update.com/verify")
                st.rerun()

        # Simple Footer
        st.markdown("""
        <div class="simple-footer">
            CyberSentinel is designed to protect people from deceptive links.<br/>
            Simple, private, and instant.
        </div>
        """, unsafe_allow_html=True)
