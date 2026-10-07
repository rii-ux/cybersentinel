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
    layout="centered",
    initial_sidebar_state="collapsed"
)

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
        gap: 0.75rem;
    }

    .main .block-container {
        max-width: 720px !important;
        padding-top: 1.5rem !important;
        padding-bottom: 3.5rem !important;
        padding-left: 1.25rem !important;
        padding-right: 1.25rem !important;
    }

    /* CyberSentinel Header / Brand */
    .brand-bar {
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 0.5rem 0 1.75rem 0;
        border-bottom: 1px solid #181818;
        margin-bottom: 2rem;
    }

    .brand-logo {
        font-size: 1.15rem;
        font-weight: 900;
        letter-spacing: 0.08em;
        color: #F5F5F5;
        text-transform: uppercase;
        display: flex;
        align-items: center;
        gap: 0.4rem;
        cursor: pointer;
    }

    .brand-dot {
        display: inline-block;
        width: 8px;
        height: 8px;
        background-color: #FFD21F;
        border-radius: 50%;
    }

    /* Hero Typography */
    .hero-eyebrow {
        font-size: 0.95rem;
        font-weight: 600;
        color: #A6A6A6;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        margin-bottom: 0.5rem;
    }

    .hero-title-main {
        font-size: clamp(2.4rem, 6vw, 3.5rem);
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
        color: #F5F5F5;
        margin-bottom: 0.1rem;
    }

    .hero-title-yellow {
        font-size: clamp(2.4rem, 6vw, 3.5rem);
        font-weight: 900;
        line-height: 1.05;
        letter-spacing: -0.03em;
        color: #FFD21F;
        margin-bottom: 1.25rem;
    }

    .hero-subhead {
        font-size: 1.35rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 0.35rem;
    }

    .hero-body {
        font-size: 1.05rem;
        color: #A6A6A6;
        margin-bottom: 2rem;
        line-height: 1.5;
    }

    /* Input Field Styling */
    .stTextInput > div > div > input {
        background-color: #111111 !important;
        border: 1.5px solid #292929 !important;
        border-radius: 12px !important;
        color: #F5F5F5 !important;
        font-size: 1.1rem !important;
        padding: 0.95rem 1.2rem !important;
        transition: all 0.2s ease !important;
    }

    .stTextInput > div > div > input:focus {
        border-color: #FFD21F !important;
        box-shadow: 0 0 0 1px #FFD21F !important;
        outline: none !important;
    }

    .stTextInput > div > div > input::placeholder {
        color: #666666 !important;
    }

    /* Buttons */
    button[kind="primary"],
    button[kind="primaryFormSubmit"],
    .stButton > button[kind="primary"],
    .stFormSubmitButton > button,
    [data-testid*="primary"] {
        background-color: #FFD21F !important;
        color: #0A0A0A !important;
        border: none !important;
        border-radius: 12px !important;
        font-size: 1.05rem !important;
        font-weight: 800 !important;
        letter-spacing: 0.04em !important;
        padding: 0.85rem 1.75rem !important;
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

    button[kind="secondary"], .stButton > button[kind="secondary"] {
        background-color: #181818 !important;
        color: #F5F5F5 !important;
        border: 1px solid #292929 !important;
        border-radius: 10px !important;
        font-size: 0.95rem !important;
        font-weight: 600 !important;
        padding: 0.6rem 1rem !important;
        transition: all 0.15s ease !important;
        cursor: pointer !important;
    }

    button[kind="secondary"]:hover, .stButton > button[kind="secondary"]:hover {
        background-color: #222222 !important;
        border-color: #383838 !important;
    }

    /* Minimal Example Link Chips */
    .example-title {
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
        color: #777777;
        margin-top: 1.5rem;
        margin-bottom: 0.6rem;
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
        border-radius: 16px;
        padding: 1.75rem 1.5rem;
        margin-bottom: 1.5rem;
        display: flex;
        flex-direction: column;
        align-items: flex-start;
        gap: 0.75rem;
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
        font-size: 2.2rem;
        line-height: 1;
        margin-bottom: 0.25rem;
    }

    .result-heading-safe {
        font-size: clamp(1.6rem, 4vw, 2.1rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #22C55E;
        line-height: 1.15;
    }

    .result-heading-suspicious {
        font-size: clamp(1.6rem, 4vw, 2.1rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #FFD21F;
        line-height: 1.15;
    }

    .result-heading-dangerous {
        font-size: clamp(1.6rem, 4vw, 2.1rem);
        font-weight: 900;
        letter-spacing: -0.02em;
        color: #EF4444;
        line-height: 1.15;
    }

    .result-subheading {
        font-size: 1.15rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-top: -0.25rem;
    }

    .result-explainer {
        font-size: 1.05rem;
        color: #D4D4D4;
        line-height: 1.5;
        margin-top: 0.2rem;
    }

    /* Score Bar */
    .score-container {
        background-color: #111111;
        border: 1px solid #292929;
        border-radius: 14px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 1.5rem;
    }

    .score-header {
        display: flex;
        justify-content: space-between;
        align-items: baseline;
        margin-bottom: 0.75rem;
    }

    .score-label {
        font-size: 0.82rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #A6A6A6;
    }

    .score-num {
        font-size: 1.5rem;
        font-weight: 900;
        color: #F5F5F5;
    }

    .score-max {
        font-size: 0.95rem;
        font-weight: 600;
        color: #777777;
    }

    .score-track {
        width: 100%;
        height: 10px;
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
        font-size: 0.88rem;
        font-weight: 800;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        color: #A6A6A6;
        margin-bottom: 0.85rem;
        margin-top: 1.25rem;
    }

    .signal-item {
        background-color: #141414;
        border: 1px solid #242424;
        border-radius: 12px;
        padding: 1rem 1.2rem;
        margin-bottom: 0.65rem;
    }

    .signal-title-safe {
        font-size: 0.98rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .signal-title-warn {
        font-size: 0.98rem;
        font-weight: 700;
        color: #F5F5F5;
        margin-bottom: 0.2rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }

    .signal-desc {
        font-size: 0.9rem;
        color: #A6A6A6;
        line-height: 1.45;
    }

    /* Recommended Action Box */
    .action-box {
        background-color: #181818;
        border-left: 4px solid #FFD21F;
        border-radius: 0 12px 12px 0;
        padding: 1.15rem 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }

    .action-box-dangerous {
        background-color: #181818;
        border-left: 4px solid #EF4444;
        border-radius: 0 12px 12px 0;
        padding: 1.15rem 1.3rem;
        margin-top: 1.5rem;
        margin-bottom: 2rem;
    }

    .action-label {
        font-size: 0.78rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        text-transform: uppercase;
        color: #A6A6A6;
        margin-bottom: 0.4rem;
    }

    .action-text {
        font-size: 1.02rem;
        font-weight: 600;
        color: #F5F5F5;
        line-height: 1.45;
    }

    /* Consumer Education Cards */
    .edu-card {
        background-color: #111111;
        border: 1px solid #292929;
        border-radius: 14px;
        padding: 1.3rem;
        margin-bottom: 1rem;
    }

    .edu-num {
        font-size: 0.85rem;
        font-weight: 800;
        color: #FFD21F;
        margin-bottom: 0.35rem;
    }

    .edu-title {
        font-size: 1.1rem;
        font-weight: 800;
        color: #F5F5F5;
        margin-bottom: 0.35rem;
    }

    .edu-desc {
        font-size: 0.95rem;
        color: #A6A6A6;
        line-height: 1.5;
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
    st.markdown('<div class="hero-eyebrow">PRACTICAL HABITS</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-title-main">STAY SAFER ONLINE</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-body">Simple habits to protect your accounts, money, and personal information.</div>', unsafe_allow_html=True)

    tips = [
        ("CHECK THE WEBSITE NAME", "Always look closely at the actual website name before the first forward slash. Beware of extra hyphens or misspelled words (like paypal-security.com instead of paypal.com)."),
        ("DON'T TRUST URGENT MESSAGES", "Scammers create artificial panic claiming your account is suspended or a package failed delivery to force you to act without thinking."),
        ("BE CAREFUL WITH LOGIN LINKS", "Never enter your password through links sent in text messages or emails. Open your browser and navigate to the official website directly."),
        ("DON'T SHARE SENSITIVE INFORMATION", "Legitimate banks and services will never ask you for your password, PIN, or one-time verification code through a random link."),
        ("WHEN IN DOUBT, DON'T CLICK", "If a message feels even slightly unusual, pause. Don't open the link. Verify through an independent phone number or official app.")
    ]

    for title, desc in tips:
        st.markdown(f"""
        <div class="edu-card">
            <div class="edu-title">{title}</div>
            <div class="edu-desc">{desc}</div>
        </div>
        """, unsafe_allow_html=True)

    st.write("")
    if st.button("CHECK A LINK NOW", type="primary", key="tips_btn"):
        navigate_to("home")


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
