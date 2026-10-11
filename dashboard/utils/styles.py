"""
RetailSync - Professional Dark Mode Styles
Glassmorphism + Neon accents for high-end dashboard UI.
"""

import streamlit as st


def apply_custom_styles():
    """Inject custom CSS for professional dark mode UI."""
    st.markdown("""
    <style>
    /* ========== GLOBAL ========== */
    .stApp {
        background: linear-gradient(135deg, #0E1117 0%, #131824 100%);
        color: #FAFAFA;
        font-family: 'Inter', 'SF Pro', 'Roboto', sans-serif;
    }

    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    /* ========== METRIC CARDS (Glassmorphism) ========== */
    div[data-testid="stMetric"] {
        background: rgba(30, 30, 40, 0.6);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 170, 0.15);
        border-radius: 14px;
        padding: 20px 24px;
        box-shadow: 0 4px 20px rgba(0, 0, 0, 0.4);
        transition: all 0.3s ease;
    }

    div[data-testid="stMetric"]:hover {
        border: 1px solid rgba(0, 255, 170, 0.5);
        box-shadow: 0 6px 30px rgba(0, 255, 170, 0.25);
        transform: translateY(-2px);
    }

    div[data-testid="stMetricLabel"] {
        color: #A0A0B0 !important;
        font-size: 0.85rem !important;
        font-weight: 500 !important;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    div[data-testid="stMetricValue"] {
        color: #00FFAA !important;
        font-size: 2rem !important;
        font-weight: 700 !important;
        text-shadow: 0 0 15px rgba(0, 255, 170, 0.4);
    }

    div[data-testid="stMetricDelta"] {
        font-size: 0.85rem !important;
    }

    /* ========== TABS ========== */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(20, 20, 30, 0.5);
        padding: 8px;
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.05);
    }

    .stTabs [data-baseweb="tab"] {
        height: 48px;
        background-color: transparent;
        border-radius: 8px;
        color: #A0A0B0;
        font-weight: 500;
        padding: 0 20px;
        transition: all 0.25s ease;
    }

    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(0, 255, 170, 0.08);
        color: #FAFAFA;
    }

    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.15), rgba(0, 150, 255, 0.1)) !important;
        color: #00FFAA !important;
        border-bottom: 2px solid #00FFAA !important;
        box-shadow: 0 0 15px rgba(0, 255, 170, 0.2);
    }

    /* ========== BUTTONS ========== */
    .stButton > button {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.1), rgba(0, 150, 255, 0.05));
        color: #00FFAA;
        border: 1px solid rgba(0, 255, 170, 0.3);
        border-radius: 10px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
        width: 100%;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, rgba(0, 255, 170, 0.25), rgba(0, 150, 255, 0.15));
        border: 1px solid rgba(0, 255, 170, 0.6);
        box-shadow: 0 0 20px rgba(0, 255, 170, 0.4);
        transform: translateY(-1px);
    }

    /* ========== SIDEBAR ========== */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0A0D14 0%, #0E1117 100%);
        border-right: 1px solid rgba(0, 255, 170, 0.1);
    }

    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #00FFAA;
        text-shadow: 0 0 10px rgba(0, 255, 170, 0.3);
    }

    /* ========== DATAFRAMES ========== */
    div[data-testid="stDataFrame"] {
        background: rgba(20, 20, 30, 0.4);
        border: 1px solid rgba(0, 255, 170, 0.1);
        border-radius: 12px;
        overflow: hidden;
    }

    /* ========== CODE BLOCKS ========== */
    .stCodeBlock {
        background: rgba(10, 10, 15, 0.8) !important;
        border: 1px solid rgba(0, 255, 170, 0.2);
        border-radius: 10px;
    }

    /* ========== ALERTS ========== */
    div[data-testid="stAlert"] {
        background: rgba(30, 30, 40, 0.6);
        backdrop-filter: blur(8px);
        border-radius: 12px;
        border-left: 4px solid #00FFAA;
    }

    /* ========== HEADINGS ========== */
    h1 {
        color: #FAFAFA;
        text-shadow: 0 0 20px rgba(0, 255, 170, 0.2);
        font-weight: 700;
        letter-spacing: -0.5px;
    }

    h2, h3 {
        color: #E0E0E8;
        font-weight: 600;
    }

    /* ========== DIVIDER ========== */
    hr {
        border-color: rgba(0, 255, 170, 0.15);
        margin: 24px 0;
    }

    /* ========== TOGGLE SWITCH ========== */
    div[data-testid="stToggle"] label {
        color: #E0E0E8;
        font-weight: 500;
    }

    /* ========== CHART CONTAINERS ========== */
    .js-plotly-plot {
        border-radius: 12px;
        overflow: hidden;
    }
    </style>
    """, unsafe_allow_html=True)


def status_badge(status: str) -> str:
    """Return colored status badge HTML."""
    colors = {
        "healthy": "#00FFAA",
        "warning": "#FFB800",
        "error": "#FF4B4B",
        "active": "#00FFAA",
        "streaming": "#00FFAA",
        "connected": "#00FFAA",
    }
    color = colors.get(status.lower(), "#A0A0B0")
    return f"""
    <span style="
        background: {color}20;
        color: {color};
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.75rem;
        font-weight: 600;
        border: 1px solid {color}60;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    ">{status}</span>
    """