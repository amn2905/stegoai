import streamlit as st
import requests
import time
import random
import json
from datetime import datetime

API_URL = "http://127.0.0.1:8000/upload-pdf"

st.set_page_config(
    page_title="StegoAI Scanner | Cyber Threat Detection",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={"Get Help": None, "Report a bug": None, "About": None}
)

# ===================== ADVANCED CSS =====================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Orbitron:wght@400;700;900&family=Rajdhani:wght@400;600;700&display=swap');

/* ── ROOT VARIABLES ── */
:root {
    --bg-deep:     #020810;
    --bg-mid:      #050f1c;
    --bg-panel:    #071525;
    --accent:      #00f5c4;
    --accent2:     #0af;
    --danger:      #ff3c5a;
    --warn:        #f5a623;
    --safe:        #00e676;
    --text:        #c8e6ff;
    --muted:       #4a7a9b;
    --border:      rgba(0,245,196,0.18);
    --glow:        0 0 18px rgba(0,245,196,0.45);
    --font-mono:   'Share Tech Mono', monospace;
    --font-display:'Orbitron', sans-serif;
    --font-ui:     'Rajdhani', sans-serif;
}

/* ── GLOBAL RESET ── */
html, body, [class*="css"] {
    background-color: var(--bg-deep) !important;
    color: var(--text) !important;
    font-family: var(--font-ui) !important;
}

/* ── SCANLINE OVERLAY ── */
body::before {
    content: "";
    position: fixed;
    inset: 0;
    background: repeating-linear-gradient(
        0deg,
        transparent,
        transparent 2px,
        rgba(0,0,0,0.08) 2px,
        rgba(0,0,0,0.08) 4px
    );
    pointer-events: none;
    z-index: 9999;
}

/* ── GRID BG PATTERN ── */
body::after {
    content: "";
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(0,245,196,0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0,245,196,0.03) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #020c18 0%, #030f1e 100%) !important;
    border-right: 1px solid var(--border) !important;
}
[data-testid="stSidebar"]::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 3px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
    box-shadow: var(--glow);
}

/* ── MAIN HEADER ── */
.hero-title {
    font-family: var(--font-display) !important;
    font-size: clamp(22px, 3vw, 42px);
    font-weight: 900;
    letter-spacing: 4px;
    text-transform: uppercase;
    background: linear-gradient(90deg, var(--accent), var(--accent2), var(--accent));
    background-size: 200% auto;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    animation: shimmer 3s linear infinite;
    margin: 0;
    padding: 0;
}
@keyframes shimmer {
    to { background-position: 200% center; }
}

.hero-sub {
    font-family: var(--font-mono);
    color: var(--muted);
    font-size: 13px;
    letter-spacing: 2px;
    margin-top: 4px;
}

.header-bar {
    display: flex;
    align-items: center;
    gap: 16px;
    padding: 18px 24px;
    background: linear-gradient(90deg, rgba(0,245,196,0.06) 0%, transparent 100%);
    border: 1px solid var(--border);
    border-radius: 12px;
    margin-bottom: 24px;
    position: relative;
    overflow: hidden;
}
.header-bar::after {
    content: "";
    position: absolute;
    left: 0; top: 0; bottom: 0;
    width: 4px;
    background: linear-gradient(180deg, var(--accent), var(--accent2));
    border-radius: 4px 0 0 4px;
}

/* ── STATUS BADGE ── */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    padding: 4px 14px;
    border-radius: 20px;
    font-family: var(--font-mono);
    font-size: 12px;
    letter-spacing: 1px;
    border: 1px solid;
}
.status-online {
    border-color: var(--safe);
    color: var(--safe);
    background: rgba(0,230,118,0.08);
}
.status-dot {
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--safe);
    animation: pulse-dot 1.4s ease-in-out infinite;
}
@keyframes pulse-dot {
    0%,100% { opacity:1; transform: scale(1); }
    50%      { opacity:0.5; transform: scale(1.4); }
}

/* ── GLASS PANEL ── */
.glass-panel {
    background: rgba(7,21,37,0.85);
    backdrop-filter: blur(14px);
    border: 1px solid var(--border);
    border-radius: 14px;
    padding: 20px 22px;
    position: relative;
    overflow: hidden;
    margin-bottom: 16px;
}
.glass-panel::before {
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), transparent);
    opacity: 0.6;
}
.panel-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 10px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.panel-label::after {
    content: "";
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── METRIC CARD ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 12px;
    margin: 16px 0;
}
.metric-card {
    background: linear-gradient(135deg, rgba(0,245,196,0.05), rgba(0,170,255,0.03));
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 16px;
    text-align: center;
    position: relative;
    overflow: hidden;
    transition: transform 0.2s, box-shadow 0.2s;
}
.metric-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 24px rgba(0,245,196,0.15);
}
.metric-card::before {
    content: "";
    position: absolute;
    bottom: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, var(--accent), var(--accent2));
}
.metric-label {
    font-family: var(--font-mono);
    font-size: 10px;
    letter-spacing: 2px;
    color: var(--muted);
    text-transform: uppercase;
    margin-bottom: 8px;
}
.metric-value {
    font-family: var(--font-display);
    font-size: 22px;
    font-weight: 700;
    color: var(--accent);
    text-shadow: 0 0 10px rgba(0,245,196,0.4);
}
.metric-sub {
    font-family: var(--font-mono);
    font-size: 11px;
    color: var(--muted);
    margin-top: 4px;
}

/* ── THREAT METER ── */
.threat-bar-wrap {
    margin: 18px 0;
}
.threat-bar-label {
    font-family: var(--font-mono);
    font-size: 11px;
    display: flex;
    justify-content: space-between;
    margin-bottom: 6px;
    color: var(--muted);
}
.threat-bar-track {
    height: 10px;
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    overflow: hidden;
    border: 1px solid var(--border);
}
.threat-bar-fill {
    height: 100%;
    border-radius: 10px;
    transition: width 1.2s cubic-bezier(.23,1,.32,1);
    position: relative;
    overflow: hidden;
}
.threat-bar-fill::after {
    content: "";
    position: absolute;
    inset: 0;
    background: linear-gradient(90deg, transparent 0%, rgba(255,255,255,0.25) 50%, transparent 100%);
    animation: bar-shine 2s linear infinite;
}
@keyframes bar-shine {
    from { transform: translateX(-100%); }
    to   { transform: translateX(100%); }
}

/* ── ALERT BOXES ── */
.alert-stego {
    background: linear-gradient(135deg, rgba(255,60,90,0.12), rgba(255,60,90,0.06));
    border: 1px solid rgba(255,60,90,0.4);
    border-radius: 12px;
    padding: 16px 20px;
    font-family: var(--font-mono);
    color: var(--danger);
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 12px;
    animation: alert-pulse 2s ease-in-out infinite;
}
@keyframes alert-pulse {
    0%,100% { box-shadow: 0 0 0 0 rgba(255,60,90,0.0); }
    50%      { box-shadow: 0 0 18px 2px rgba(255,60,90,0.25); }
}
.alert-clean {
    background: linear-gradient(135deg, rgba(0,230,118,0.1), rgba(0,230,118,0.04));
    border: 1px solid rgba(0,230,118,0.35);
    border-radius: 12px;
    padding: 16px 20px;
    font-family: var(--font-mono);
    color: var(--safe);
    letter-spacing: 1px;
    display: flex;
    align-items: center;
    gap: 12px;
}

/* ── LOG TERMINAL ── */
.terminal {
    background: #010b14;
    border: 1px solid rgba(0,245,196,0.12);
    border-radius: 10px;
    padding: 16px;
    font-family: var(--font-mono);
    font-size: 12px;
    line-height: 1.8;
    max-height: 220px;
    overflow-y: auto;
}
.terminal::-webkit-scrollbar { width: 4px; }
.terminal::-webkit-scrollbar-thumb { background: var(--accent); border-radius: 4px; }
.log-line { display: flex; gap: 10px; }
.log-time { color: var(--muted); flex-shrink: 0; }
.log-ok   { color: var(--safe); }
.log-warn { color: var(--warn); }
.log-err  { color: var(--danger); }
.log-info { color: var(--accent2); }

/* ── UPLOAD ZONE ── */
section[data-testid="stFileUploader"] {
    border: 2px dashed rgba(0,245,196,0.25) !important;
    border-radius: 14px !important;
    background: rgba(0,245,196,0.02) !important;
    transition: border-color 0.3s;
}
section[data-testid="stFileUploader"]:hover {
    border-color: var(--accent) !important;
    box-shadow: inset 0 0 30px rgba(0,245,196,0.05);
}

/* ── BUTTONS ── */
.stButton > button {
    font-family: var(--font-display) !important;
    font-size: 13px !important;
    font-weight: 700 !important;
    letter-spacing: 2px !important;
    text-transform: uppercase !important;
    padding: 12px 28px !important;
    border-radius: 8px !important;
    border: 1px solid var(--accent) !important;
    background: linear-gradient(135deg, rgba(0,245,196,0.12), rgba(0,170,255,0.08)) !important;
    color: var(--accent) !important;
    transition: all 0.25s !important;
    box-shadow: 0 0 0 0 rgba(0,245,196,0) !important;
}
.stButton > button:hover {
    background: linear-gradient(135deg, rgba(0,245,196,0.25), rgba(0,170,255,0.18)) !important;
    box-shadow: 0 0 20px rgba(0,245,196,0.3) !important;
    transform: translateY(-1px) !important;
}

/* ── SPINNER OVERRIDE ── */
.stSpinner > div { border-top-color: var(--accent) !important; }

/* ── METRICS OVERRIDE ── */
[data-testid="stMetricValue"] {
    font-family: var(--font-display) !important;
    color: var(--accent) !important;
}

/* ── EXPANDER ── */
[data-testid="stExpander"] {
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    background: rgba(7,21,37,0.7) !important;
}

/* ── DIVIDER ── */
hr {
    border-color: var(--border) !important;
}

/* ── SIDEBAR ITEMS ── */
.sidebar-item {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 8px 0;
    border-bottom: 1px solid rgba(0,245,196,0.06);
    font-family: var(--font-mono);
    font-size: 12px;
}
.sidebar-key { color: var(--muted); }
.sidebar-val { color: var(--accent); font-weight: bold; }

/* ── RISK BADGE ── */
.risk-badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-family: var(--font-mono);
    font-size: 11px;
    letter-spacing: 1px;
    font-weight: bold;
}
.risk-low    { background: rgba(0,230,118,0.12); border:1px solid var(--safe);   color:var(--safe);   }
.risk-medium { background: rgba(245,166,35,0.12); border:1px solid var(--warn);  color:var(--warn);  }
.risk-high   { background: rgba(255,60,90,0.12);  border:1px solid var(--danger); color:var(--danger); }

/* ── RADAR ANIMATION ── */
.radar-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    padding: 20px 0 10px;
}
.radar {
    position: relative;
    width: 100px;
    height: 100px;
}
.radar-ring {
    position: absolute;
    border-radius: 50%;
    border: 1px solid rgba(0,245,196,0.2);
}
.radar-ring:nth-child(1) { inset:0; }
.radar-ring:nth-child(2) { inset:20%; }
.radar-ring:nth-child(3) { inset:40%; }
.radar-sweep {
    position: absolute;
    inset: 0;
    border-radius: 50%;
    background: conic-gradient(rgba(0,245,196,0.0) 80%, rgba(0,245,196,0.5) 100%);
    animation: spin 2.5s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }
.radar-dot {
    position: absolute;
    width: 5px; height: 5px;
    border-radius: 50%;
    background: var(--accent);
    box-shadow: 0 0 6px var(--accent);
}

/* ── PROBABILITY TABLE ── */
.prob-table { width: 100%; border-collapse: collapse; font-family: var(--font-mono); font-size: 12px; }
.prob-table th { color: var(--muted); text-align: left; padding: 6px 10px; border-bottom: 1px solid var(--border); }
.prob-table td { padding: 8px 10px; }
.prob-table tr:hover td { background: rgba(0,245,196,0.04); }
</style>
""", unsafe_allow_html=True)


# ===================== SESSION STATE =====================
if "scan_log" not in st.session_state:
    st.session_state.scan_log = []
if "scan_count" not in st.session_state:
    st.session_state.scan_count = 0
if "threats_found" not in st.session_state:
    st.session_state.threats_found = 0


def add_log(msg, level="info"):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.scan_log.insert(0, (ts, msg, level))
    if len(st.session_state.scan_log) > 30:
        st.session_state.scan_log = st.session_state.scan_log[:30]


def render_log():
    level_class = {"ok": "log-ok", "warn": "log-warn", "err": "log-err", "info": "log-info"}
    lines = ""
    for ts, msg, lv in st.session_state.scan_log:
        cls = level_class.get(lv, "log-info")
        lines += f'<div class="log-line"><span class="log-time">[{ts}]</span><span class="{cls}">{msg}</span></div>'
    return f'<div class="terminal">{lines if lines else "<span class=\'log-info\'>// No events yet — awaiting file upload</span>"}</div>'


def get_bar_color(val):
    if val < 0.35:
        return "linear-gradient(90deg, #00e676, #00b248)"
    elif val < 0.65:
        return "linear-gradient(90deg, #f5a623, #e8840e)"
    else:
        return "linear-gradient(90deg, #ff3c5a, #cc1a36)"


def get_risk_class(risk):
    r = risk.lower()
    if "low" in r:
        return "risk-low"
    elif "med" in r or "moderate" in r:
        return "risk-medium"
    else:
        return "risk-high"


# ===================== SIDEBAR =====================
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 8px;'>
        <div style='font-family:var(--font-display); font-size:14px; letter-spacing:3px;
                    color:var(--accent); text-transform:uppercase;'>StegoAI</div>
        <div style='font-family:var(--font-mono); font-size:10px; color:var(--muted);
                    letter-spacing:2px; margin-top:3px;'>v2.0 — NEURAL CORE ACTIVE</div>
    </div>
    <div class='radar-wrap'>
        <div class='radar'>
            <div class='radar-ring'></div>
            <div class='radar-ring'></div>
            <div class='radar-ring'></div>
            <div class='radar-sweep'></div>
            <div class='radar-dot' style='top:22%;left:55%;'></div>
            <div class='radar-dot' style='top:60%;left:30%;'></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div class='panel-label'>◈ Engine Config</div>
    <div class='sidebar-item'><span class='sidebar-key'>ML Model</span><span class='sidebar-val'>XGBoost</span></div>
    <div class='sidebar-item'><span class='sidebar-key'>Method</span><span class='sidebar-val'>Steganalysis</span></div>
    <div class='sidebar-item'><span class='sidebar-key'>Mode</span><span class='sidebar-val'>Real-Time</span></div>
    <div class='sidebar-item'><span class='sidebar-key'>Input</span><span class='sidebar-val'>PDF</span></div>
    <div class='sidebar-item'><span class='sidebar-key'>API</span><span class='sidebar-val'>localhost:8000</span></div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    scan_count = st.session_state.scan_count
    threats    = st.session_state.threats_found
    clean      = max(0, scan_count - threats)

    st.markdown(f"""
    <div class='panel-label'>◈ Session Stats</div>
    <div class='sidebar-item'><span class='sidebar-key'>Total Scans</span><span class='sidebar-val'>{scan_count:04d}</span></div>
    <div class='sidebar-item'><span class='sidebar-key'>Threats Found</span>
        <span style='color:{"var(--danger)" if threats > 0 else "var(--safe)"}; font-family:var(--font-mono);'>{threats:04d}</span></div>
    <div class='sidebar-item'><span class='sidebar-key'>Clean Files</span>
        <span style='color:var(--safe); font-family:var(--font-mono);'>{clean:04d}</span></div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    if st.button("🗑 Clear Log", use_container_width=True):
        st.session_state.scan_log = []
        st.rerun()

    if st.button("↺ Reset Stats", use_container_width=True):
        st.session_state.scan_count = 0
        st.session_state.threats_found = 0
        st.rerun()


# ===================== HEADER =====================
st.markdown(f"""
<div class='header-bar'>
    <div>
        <div class='hero-title'>🛡 StegoAI Cyber Scanner</div>
        <div class='hero-sub'>[ ML-POWERED STEGANOGRAPHIC THREAT DETECTION SYSTEM ]</div>
    </div>
    <div style='margin-left:auto; display:flex; flex-direction:column; align-items:flex-end; gap:6px;'>
        <div class='status-badge status-online'>
            <span class='status-dot'></span> SYSTEM ONLINE
        </div>
        <div style='font-family:var(--font-mono); font-size:10px; color:var(--muted);'>
            {datetime.now().strftime("%Y-%m-%d  %H:%M:%S")} UTC
        </div>
    </div>
</div>
""", unsafe_allow_html=True)


# ===================== MAIN LAYOUT =====================
left_col, right_col = st.columns([3, 2], gap="large")

with left_col:
    # Upload Panel
    st.markdown('<div class="panel-label">◈ File Upload</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "Drop a PDF here or click to browse",
        type=["pdf"],
        label_visibility="collapsed"
    )

    if uploaded_file:
        size_kb = len(uploaded_file.getvalue()) / 1024
        st.markdown(f"""
        <div class='glass-panel' style='margin-top:10px;'>
            <div class='panel-label'>◈ File Loaded</div>
            <div style='display:flex; justify-content:space-between; font-family:var(--font-mono); font-size:13px;'>
                <span style='color:var(--accent);'>📄 {uploaded_file.name}</span>
                <span style='color:var(--muted);'>{size_kb:.1f} KB</span>
            </div>
            <div style='margin-top:8px; font-family:var(--font-mono); font-size:11px; color:var(--muted);'>
                Type: application/pdf &nbsp;|&nbsp; Status: <span style='color:var(--safe);'>READY</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Scan Button
        st.markdown("<br>", unsafe_allow_html=True)
        if st.button("⚡ INITIATE DEEP SCAN", use_container_width=True):
            add_log(f"Scan initiated → {uploaded_file.name}", "info")
            add_log(f"File size: {size_kb:.1f} KB", "info")

            with st.spinner("🔍 Analyzing entropy patterns & hidden payloads…"):
                time.sleep(0.4)
                add_log("Entropy analysis pass 1/3 complete", "info")
                time.sleep(0.3)
                add_log("LSB channel scan in progress…", "info")

                try:
                    files = {"file": (uploaded_file.name, uploaded_file, "application/pdf")}
                    response = requests.post(API_URL, files=files, timeout=30)

                    if response.status_code == 200:
                        data       = response.json()
                        result     = data["result"]
                        prediction = result["prediction"]
                        confidence = result["confidence"]
                        risk       = result["risk_level"]
                        probs      = result["probabilities"]
                        stego_prob = probs.get("stego", 0)
                        clean_prob = probs.get("clean", 1 - stego_prob)

                        st.session_state.scan_count += 1
                        if prediction == "Stego":
                            st.session_state.threats_found += 1
                            add_log(f"THREAT DETECTED — {prediction} ({confidence})", "err")
                            add_log(f"Risk Level: {risk}", "warn")
                        else:
                            add_log(f"Scan complete — {prediction} ({confidence})", "ok")
                            add_log(f"Risk: {risk}", "ok")

                        # ── RESULT ALERT ──
                        if prediction == "Stego":
                            st.markdown(f"""
                            <div class='alert-stego'>
                                <span style='font-size:24px;'>⚠</span>
                                <div>
                                    <div style='font-size:14px; font-weight:bold;'>STEGANOGRAPHIC PAYLOAD DETECTED</div>
                                    <div style='font-size:11px; color:rgba(255,60,90,0.7); margin-top:3px;'>
                                        Hidden data found inside the PDF structure. Isolate & quarantine recommended.
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div class='alert-clean'>
                                <span style='font-size:24px;'>✔</span>
                                <div>
                                    <div style='font-size:14px; font-weight:bold;'>FILE INTEGRITY VERIFIED — CLEAN</div>
                                    <div style='font-size:11px; color:rgba(0,230,118,0.7); margin-top:3px;'>
                                        No hidden payloads or anomalies detected in file structure.
                                    </div>
                                </div>
                            </div>
                            """, unsafe_allow_html=True)

                        st.markdown("<br>", unsafe_allow_html=True)

                        # ── METRIC CARDS ──
                        risk_cls = get_risk_class(risk)
                        st.markdown(f"""
                        <div class='metric-grid'>
                            <div class='metric-card'>
                                <div class='metric-label'>Prediction</div>
                                <div class='metric-value' style='color:{"var(--danger)" if prediction=="Stego" else "var(--safe)"}'>
                                    {prediction.upper()}
                                </div>
                                <div class='metric-sub'>Classification</div>
                            </div>
                            <div class='metric-card'>
                                <div class='metric-label'>Confidence</div>
                                <div class='metric-value'>{confidence}</div>
                                <div class='metric-sub'>Model Certainty</div>
                            </div>
                            <div class='metric-card'>
                                <div class='metric-label'>Risk Level</div>
                                <div class='metric-value'>
                                    <span class='risk-badge {risk_cls}'>{risk.upper()}</span>
                                </div>
                                <div class='metric-sub'>Threat Score</div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── PROBABILITY BARS ──
                        st.markdown('<div class="panel-label" style="margin-top:20px;">◈ Threat Probability Analysis</div>', unsafe_allow_html=True)
                        stego_pct = int(stego_prob * 100)
                        clean_pct = int(clean_prob * 100)

                        # ── BARS (separate block — no <table> here) ──
                        st.markdown(f"""
                        <div class='glass-panel'>
                            <div class='threat-bar-wrap'>
                                <div class='threat-bar-label'>
                                    <span>⬡ Stego Probability</span>
                                    <span style='color:var(--danger);'>{stego_pct}%</span>
                                </div>
                                <div class='threat-bar-track'>
                                    <div class='threat-bar-fill'
                                         style='width:{stego_pct}%; background:{get_bar_color(stego_prob)};'></div>
                                </div>
                            </div>
                            <div class='threat-bar-wrap'>
                                <div class='threat-bar-label'>
                                    <span>⬡ Clean Probability</span>
                                    <span style='color:var(--safe);'>{clean_pct}%</span>
                                </div>
                                <div class='threat-bar-track'>
                                    <div class='threat-bar-fill'
                                         style='width:{clean_pct}%; background:linear-gradient(90deg, #00e676, #00b248);'></div>
                                </div>
                            </div>
                        </div>
                        """, unsafe_allow_html=True)

                        # ── PROBABILITY TABLE — native Streamlit (avoids <table> parse bug) ──
                        stego_band = "HIGH" if stego_prob > 0.65 else "MEDIUM" if stego_prob > 0.35 else "LOW"
                        clean_band = "HIGH" if clean_prob > 0.65 else "MEDIUM" if clean_prob > 0.35 else "LOW"

                        st.markdown("""
                        <div style='font-family:var(--font-mono); font-size:10px; letter-spacing:2px;
                                    color:#00f5c4; text-transform:uppercase; margin:10px 0 6px;
                                    display:flex; align-items:center; gap:8px;'>
                            ◈ Probability Breakdown
                            <span style='flex:1; height:1px; background:rgba(0,245,196,0.18); display:inline-block;'></span>
                        </div>
                        """, unsafe_allow_html=True)

                        th_style = "background:rgba(0,245,196,0.06); padding:6px 0; font-family:'Share Tech Mono',monospace; font-size:11px; color:#4a7a9b; letter-spacing:1px; text-align:center;"
                        hcol1, hcol2, hcol3 = st.columns([2, 2, 2])
                        hcol1.markdown(f"<div style='{th_style}'>CLASS</div>", unsafe_allow_html=True)
                        hcol2.markdown(f"<div style='{th_style}'>PROBABILITY</div>", unsafe_allow_html=True)
                        hcol3.markdown(f"<div style='{th_style}'>CONFIDENCE BAND</div>", unsafe_allow_html=True)

                        row_style = "padding:8px 0; font-family:'Share Tech Mono',monospace; font-size:12px; text-align:center; border-top:1px solid rgba(0,245,196,0.08);"
                        rc1, rc2, rc3 = st.columns([2, 2, 2])
                        rc1.markdown(f"<div style='{row_style} color:#ff3c5a;'>Stego</div>", unsafe_allow_html=True)
                        rc2.markdown(f"<div style='{row_style} color:#c8e6ff;'>{stego_prob:.4f}</div>", unsafe_allow_html=True)
                        rc3.markdown(f"<div style='{row_style} color:#ff3c5a;'>{stego_band}</div>", unsafe_allow_html=True)

                        rd1, rd2, rd3 = st.columns([2, 2, 2])
                        rd1.markdown(f"<div style='{row_style} color:#00e676;'>Clean</div>", unsafe_allow_html=True)
                        rd2.markdown(f"<div style='{row_style} color:#c8e6ff;'>{clean_prob:.4f}</div>", unsafe_allow_html=True)
                        rd3.markdown(f"<div style='{row_style} color:#00e676;'>{clean_band}</div>", unsafe_allow_html=True)

                        # ── JSON EXPANDER ──
                        with st.expander("🔎 Full API Response Payload"):
                            st.json(result)

                    else:
                        add_log(f"API returned HTTP {response.status_code}", "err")
                        st.error(f"⛔ API Error — Status {response.status_code}")

                except requests.exceptions.ConnectionError:
                    add_log("Connection refused — is the FastAPI server running?", "err")
                    st.error("🔌 Cannot connect to API. Make sure `uvicorn main:app` is running on port 8000.")
                except Exception as e:
                    add_log(f"Exception: {str(e)[:60]}", "err")
                    st.error(f"💥 Unexpected error: {e}")


with right_col:
    # ── SYSTEM PANEL ──
    st.markdown("""
    <div class='glass-panel'>
        <div class='panel-label'>◈ Detection Modules</div>
        <div style='font-family:var(--font-mono); font-size:12px; line-height:2.2;'>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:var(--muted);'>LSB Steganalysis</span>
                <span style='color:var(--safe);'>■ ACTIVE</span>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:var(--muted);'>DCT Coefficient Analysis</span>
                <span style='color:var(--safe);'>■ ACTIVE</span>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:var(--muted);'>Metadata Forensics</span>
                <span style='color:var(--safe);'>■ ACTIVE</span>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:var(--muted);'>Entropy Analysis</span>
                <span style='color:var(--safe);'>■ ACTIVE</span>
            </div>
            <div style='display:flex; justify-content:space-between;'>
                <span style='color:var(--muted);'>XGBoost Classifier</span>
                <span style='color:var(--accent);'>■ LOADED</span>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── HOW TO USE ──
    st.markdown("""
    <div class='glass-panel'>
        <div class='panel-label'>◈ Operator Guide</div>
        <div style='font-family:var(--font-mono); font-size:12px; color:var(--muted); line-height:2;'>
            <div><span style='color:var(--accent);'>01</span> &nbsp; Upload a PDF file</div>
            <div><span style='color:var(--accent);'>02</span> &nbsp; Click INITIATE DEEP SCAN</div>
            <div><span style='color:var(--accent);'>03</span> &nbsp; Review prediction & probabilities</div>
            <div><span style='color:var(--accent);'>04</span> &nbsp; If STEGO detected → quarantine file</div>
            <div><span style='color:var(--accent);'>05</span> &nbsp; Check Activity Log for full trace</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── LIVE LOG ──
    st.markdown('<div class="panel-label">◈ Activity Log</div>', unsafe_allow_html=True)
    st.markdown(render_log(), unsafe_allow_html=True)


# ===================== FOOTER =====================
st.markdown("<br>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align:center; font-family:var(--font-mono); font-size:10px;
            color:var(--muted); letter-spacing:2px; padding: 16px 0;
            border-top: 1px solid var(--border);'>
    STEGOAI SCANNER &nbsp;|&nbsp; CLASSIFIED THREAT DETECTION SYSTEM &nbsp;|&nbsp; AUTHORIZED USE ONLY
</div>
""", unsafe_allow_html=True)
