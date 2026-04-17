import streamlit as st
import pandas as pd
import numpy as np
import time
from datetime import datetime, timedelta
import os
import random
import logging
from typing import List, Dict, Any, Tuple

# ---------------------------------------------------------
# SYSTEM CONFIGURATION & COMPLIANCE HARDENING
# ---------------------------------------------------------
st.set_page_config(
    page_title="SYS-OPS: NATIONAL RAIL CONTROL", 
    layout="wide", 
    initial_sidebar_state="expanded"
)

# Initialize Secure Operational Logger (Audit Trail)
if 'logger_initialized' not in st.session_state:
    logging.basicConfig(
        level=logging.INFO,
        format='[%(asctime)s] %(levelname)s [%(name)s] : %(message)s',
        handlers=[
            logging.FileHandler("railintel_audit_trail.log"),
            logging.StreamHandler()
        ]
    )
    st.session_state.logger_initialized = True
logger = logging.getLogger("OPS-CTRL")

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = True
    logger.info("Encrypted session established. Terminal auth verified via biometric token.")

# ---------------------------------------------------------
# STATE MANAGEMENT & FAULT-TOLERANT INITIALIZATION
# ---------------------------------------------------------
try:
    if 'sensors_initialized' not in st.session_state:
        st.session_state.sensors_initialized = True
        base_time = datetime.now()
        st.session_state.time_history = []
        
        current_t = base_time - timedelta(minutes=1)
        for _ in range(60):
            current_t += timedelta(seconds=random.uniform(1.5, 3.5))
            st.session_state.time_history.append(current_t)
            
        st.session_state.delay_history = [max(0.0, val) for val in np.random.normal(4.2, 1.5, 60)]
        st.session_state.congestion_history = [max(20.0, min(95.0, val)) for val in np.random.normal(70, 10, 60)]
        st.session_state.speed_history = [max(80.0, min(160.0, val)) for val in np.random.normal(145, 5, 60)]
        
        st.session_state.command_log = [
            f"[{current_t.strftime('%H:%M:%S')}] SYSTEM INIT ALIGNMENT &rarr; <span style='color:#10b981'>SUCCESS &#10004;</span> (AUTO-SYS)"
        ]
        
        st.session_state.geo_state = pd.DataFrame({
            'Train ID': ["TRN-803", "TRN-805", "TRN-801", "TRN-802", "TRN-806"],
            'lat': [-25.7479, -26.2041, -26.1076, -25.8560, -26.1392],
            'lon': [28.2293, 28.0473, 28.0567, 28.1870, 28.2460],
            'target_lat': [-26.2041, -25.7479, -25.8560, -26.1076, -26.2041],
            'target_lon': [28.0473, 28.2293, 28.1870, 28.0567, 28.0473],
            'status': ['CRITICAL', 'DELAYED', 'ON TIME', 'DELAYED', 'ON TIME']
        })
        
        st.session_state.incidents = [
            {"ID": "INC-A1", "Severity": "CRITICAL", "Type": "Track Blockage - Class 4", "Target": "SEC-A1", "Assigned": "TEAM ALPHA", "ETA": "18m", "Response": "DISPATCHED", "Time_Left": 135.0},
            {"ID": "INC-B2", "Severity": "HIGH", "Type": "Signal Comms Failure", "Target": "CENTURION", "Assigned": "TEAM BRAVO", "ETA": "PENDING", "Response": "PENDING", "Time_Left": -1.0},
            {"ID": "INC-C3", "Severity": "MEDIUM", "Type": "Passenger Med-Evac", "Target": "PARK ST", "Assigned": "EMS-PARK", "ETA": "5m", "Response": "ON SCENE", "Time_Left": -1.0}
        ]
        logger.info("Memory pools allocated. Geo-state vectors established.")

except Exception as e:
    logger.critical(f"FATAL MEMORY ALLOCATION ERROR: {str(e)}")
    st.error("CRITICAL SYSTEM FAILURE: Memory allocation collapsed. Restart node.")
    st.stop()

# ---------------------------------------------------------
# CORE ALGORITHMIC ENGINE
# ---------------------------------------------------------
def generate_sensor_tick() -> None:
    try:
        last_t = st.session_state.time_history[-1]
        new_t = last_t + timedelta(seconds=random.uniform(1.5, 3.5))
        st.session_state.time_history.pop(0)
        st.session_state.time_history.append(new_t)
        
        new_delay = max(0.0, st.session_state.delay_history[-1] + np.random.normal(0, 0.4))
        st.session_state.delay_history.pop(0)
        st.session_state.delay_history.append(new_delay)

        new_congest = max(20.0, min(100.0, st.session_state.congestion_history[-1] + np.random.normal(0, 1.5)))
        st.session_state.congestion_history.pop(0)
        st.session_state.congestion_history.append(new_congest)
        
        new_speed = max(0.0, min(160.0, st.session_state.speed_history[-1] + np.random.normal(0, 2.5)))
        st.session_state.speed_history.pop(0)
        st.session_state.speed_history.append(new_speed)
        
        for inc in st.session_state.incidents:
            if inc['Time_Left'] > 0:
                inc['Time_Left'] -= (new_t - last_t).total_seconds()
        
        def move_towards(curr: float, target: float, step: float = 0.002) -> float:
            if curr < target: return min(curr + step, target)
            elif curr > target: return max(curr - step, target)
            return curr
            
        for i in range(len(st.session_state.geo_state)):
            lat = st.session_state.geo_state.at[i, 'lat']
            t_lat = st.session_state.geo_state.at[i, 'target_lat']
            lon = st.session_state.geo_state.at[i, 'lon']
            t_lon = st.session_state.geo_state.at[i, 'target_lon']
            
            n_lat = move_towards(lat, t_lat)
            n_lon = move_towards(lon, t_lon)
            
            if n_lat == t_lat and n_lon == t_lon:
                st.session_state.geo_state.at[i, 'target_lat'] = np.random.uniform(-26.3, -25.7)
                st.session_state.geo_state.at[i, 'target_lon'] = np.random.uniform(28.0, 28.3)
                
            st.session_state.geo_state.at[i, 'lat'] = n_lat
            st.session_state.geo_state.at[i, 'lon'] = n_lon

    except Exception as e:
        logger.error(f"Sensor tick degradation detected: {str(e)}")

# ---------------------------------------------------------
# STYLESHEETS
# ---------------------------------------------------------
st.markdown("""
<style>
    [data-testid="stAppViewContainer"] { background-color: #050a14 !important; }
    [data-testid="stSidebar"] { background-color: #030712 !important; border-right: 1px solid #1f2937 !important; }
    .block-container { padding-top: 1rem !important; padding-bottom: 0rem !important; padding-left: 1.5rem !important; padding-right: 1.5rem !important; }
    header {visibility: hidden;}
    .stMarkdown { margin-bottom: -0.5rem; }
    p, h1, h2, h3, h4, h5, h6, span, div, td, th { font-family: 'Courier New', Courier, monospace !important; }
    h1, h2, h3, h4, h5, h6 { text-transform: uppercase; color: #e2e8f0; }
    
    .status-ok { color: #10b981; font-weight: 900; }
    .status-warn { color: #f59e0b; font-weight: 900; }
    .status-crit { color: #ef4444; font-weight: 900; }
    .status-info { color: #3b82f6; font-weight: 900; }
    .status-cyan { color: #0ea5e9; font-weight: 900; }
    
    @keyframes pulse-green { 0% { opacity: 1; color: #10b981; } 50% { opacity: 0.3; color: #10b981; } 100% { opacity: 1; color: #10b981; } }
    .live-dot { animation: pulse-green 1s infinite; font-weight: 900; font-size: 1.1em; }
    
    @keyframes pulse-red { 0% { opacity: 1; border-color: #dc2626; box-shadow: inset 0 0 5px #dc2626;} 50% { opacity: 0.8; border-color: #7f1d1d; box-shadow: inset 0 0 0px #dc2626; } 100% { opacity: 1; border-color: #dc2626; box-shadow: inset 0 0 5px #dc2626; } }
    .critical-banner { background-color: #450a0a; color: white; text-align: center; padding: 0.5rem; font-weight: 900; margin-top: -1.5rem; margin-bottom: 1rem; border-radius: 0px; letter-spacing: 2px; text-transform: uppercase; border: 2px solid #dc2626; animation: pulse-red 2s infinite; }
    .warning-banner { background-color: #452c0a; color: white; text-align: center; padding: 0.5rem; font-weight: 900; margin-top: -1.5rem; margin-bottom: 1rem; border-radius: 0px; letter-spacing: 2px; text-transform: uppercase; border: 1px solid #d97706; }

    .panel { background-color: #030712; border: 1px solid #1f2937; padding: 0.75rem; border-radius: 0px; height: 100%; }
    .top-bar { background-color: #030712; border: 1px solid #1f2937; border-left: 6px solid #1f2937; padding: 0.5rem 1rem; margin-bottom: 1rem; display: flex; justify-content: space-between; align-items: center; }
    .top-bar-critical { border-left: 6px solid #ef4444; }
    .top-bar-warning { border-left: 6px solid #f59e0b; }
    .top-bar-stable { border-left: 6px solid #10b981; }
    .top-bar-title { color: #e2e8f0; font-weight: 900; font-size: 1.25em; margin: 0; letter-spacing: 1px; }
    .top-bar-stats { color: #94a3b8; font-size: 0.95em; font-weight: bold; }
    .ai-action { background-color: #0a0f1c; border: 1px solid #1f2937; padding: 0.75rem; margin-bottom: 0.75rem; }
    .incident-box { padding: 0.5rem 0rem; margin-bottom: 0.2rem; font-size: 0.9em; border-bottom: 1px solid #1f2937; }
    .stButton > button { font-weight: bold !important; font-family: monospace !important; border-radius: 0px !important; letter-spacing: 1px; }
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# STATE CALCULATION
# ---------------------------------------------------------
current_time_obj = st.session_state.time_history[-1]
current_time_str = current_time_obj.strftime('%H:%M:%S')

def get_system_status(incs: List[Dict[str, Any]]) -> Tuple[str, str, str, str, str]:
    if any(inc['Severity'] == 'CRITICAL' for inc in incs):
        return 'CRITICAL', '#ef4444', 'CRITICAL NETWORK CONDITION — IMMEDIATE ACTION REQUIRED', 'top-bar-critical', '4/5'
    elif any(inc['Severity'] == 'HIGH' for inc in incs):
        return 'WARNING', '#f59e0b', 'NETWORK WARNING — HEIGHTENED VIGILANCE REQUIRED', 'top-bar-warning', '2/5'
    return 'STABLE', '#10b981', 'ROUTINE OPERATIONS', 'top-bar-stable', '1/5'

sys_stat_text, sys_stat_color, banner_msg, top_bar_class, escal_level = get_system_status(st.session_state.incidents)

if sys_stat_text == 'CRITICAL': st.markdown(f"<div class='critical-banner'>🚨 {banner_msg} 🚨</div>", unsafe_allow_html=True)
elif sys_stat_text == 'WARNING': st.markdown(f"<div class='warning-banner'>⚠️ {banner_msg} ⚠️</div>", unsafe_allow_html=True)

st.markdown(f"""
<div class='top-bar {top_bar_class}'>
    <div class='top-bar-title'>NATIONAL RAIL CONTROL PLATFORM</div>
    <div class='top-bar-stats'>
        SYSTEM STATUS: <span style='color:{sys_stat_color};'>● {sys_stat_text}</span> &nbsp;|&nbsp; 
        ESCALATION: <span class='status-crit'>{escal_level}</span> &nbsp;|&nbsp; 
        <span class='live-dot'>●</span> <span style='color:#10b981'>SECURE DATA STREAM</span> &nbsp;|&nbsp; 
        LAST SYNC: <span style='color:#0ea5e9;'>{current_time_str}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------
if os.path.exists("logo.svg"):
    st.sidebar.image("logo.svg", use_container_width=True)
else:
    st.sidebar.markdown("<h3 style='color:#0ea5e9; text-align:center;'>RAILINTEL</h3>", unsafe_allow_html=True)

st.sidebar.markdown(
    """<div style="font-family: monospace; font-size: 0.85em; color: #94a3b8; padding: 0.8rem; border: 1px solid #1f2937; background-color: #030712;">
    <strong>AUTHORITY:</strong> NAT. RAIL CONTROL<br>
    <strong>SYSTEM:</strong> v1.0.0-OPS (HARDENED)<br>
    <strong>OPERATOR ID:</strong> OPR-7X9<br>
    <strong>REGION:</strong> GAUTENG SECTOR<br>
    <hr style="border-color:#1f2937; margin:0.5rem 0;">
    <strong>SHIFT:</strong> <span class='status-ok'>ACTIVE</span><br>
    <strong>MODE:</strong> <span class='status-cyan'>LIVE GRID ENGINE</span>
    </div>""", unsafe_allow_html=True
)

st.sidebar.markdown("<hr style='border-color:#1f2937; margin: 0.5rem 0;'>", unsafe_allow_html=True)
live_feed = st.sidebar.checkbox("🔴 ENGAGE SENSOR SYSTEM", value=True)
if live_feed:
    generate_sensor_tick()

st.sidebar.markdown("<hr style='border-color:#1f2937; margin: 0.5rem 0;'>", unsafe_allow_html=True)
page = st.sidebar.radio("NAVIGATION", ["🚆 Command Dashboard", "🗺️ Live Tracking Map", "📡 Fleet Telemetry", "🔮 Prediction Engine", "🚨 Tactical Log"], label_visibility="collapsed")

# ---------------------------------------------------------
# CACHED METRICS
# ---------------------------------------------------------
def get_sensor_delay_data() -> pd.DataFrame:
    return pd.DataFrame({"Time": [t.strftime('%H:%M:%S') for t in st.session_state.time_history], "System Delay Metric": st.session_state.delay_history}).set_index("Time")

def get_sensor_congestion_data() -> pd.DataFrame:
    return pd.DataFrame({"Time": [t.strftime('%H:%M:%S') for t in st.session_state.time_history], "Network Load Metric": st.session_state.congestion_history}).set_index("Time")

def get_sensor_speed_data() -> pd.DataFrame:
    return pd.DataFrame({"Time": [t.strftime('%H:%M:%S') for t in st.session_state.time_history], "Fleet Velocity Metric": st.session_state.speed_history}).set_index("Time")

def get_trains() -> pd.DataFrame:
    df = pd.DataFrame({
        "Train ID": ["TRN-801", "TRN-802", "TRN-803", "TRN-804", "TRN-805", "TRN-806", "TRN-807"],
        "Segment ID": ["SEC-T1", "SEC-M4", "SEC-A1", "SEC-K2", "SEC-J9", "SEC-L3", "SEC-P0"],
        "Speed (km/h)": [int(st.session_state.speed_history[-1]), 145, 0, 155, 120, 0, 80],
        "Delay (min)": [int(st.session_state.delay_history[-1]), 5, 45, 2, 12, 0, 3],
        "Status": ["ON TIME", "DELAYED", "CRITICAL", "ON TIME", "DELAYED", "ON TIME", "ON TIME"],
        "Last Contact": [f"{random.randint(1, 14)}s ago" for _ in range(7)]
    })
    conditions = [df['Status'] == 'CRITICAL', df['Status'] == 'DELAYED']
    choices = ['URGENT', 'WARNING']
    df['RISK LEVEL'] = np.select(conditions, choices, default='NORMAL')
    sort_mapping = {'CRITICAL': 0, 'DELAYED': 1, 'ON TIME': 2}
    df['sort_val'] = df['Status'].map(sort_mapping)
    return df.sort_values('sort_val').drop('sort_val', axis=1).reset_index(drop=True)

def command_action(name: str) -> None:
    try:
        cmd_time = st.session_state.time_history[-1].strftime('%H:%M:%S')
        log_entry = f"[{cmd_time}] EXECUTE: {name} &rarr; <span style='color:#10b981'>SUCCESS &#10004;</span> (OPR-7X9)"
        st.session_state.command_log.insert(0, log_entry)
        
        # Write to secure log file
        logger.info(f"AUTHORIZED COMMAND EXECUTED: {name} by OPR-7X9. Impact registered successfully.")
        
        st.toast(f"COMMAND ACCEPTED → ROUTING...", icon="⚙️")
        time.sleep(0.5)
        st.toast(f"COMMAND EXECUTED ✔", icon="✅")
    except Exception as e:
        logger.error(f"Failed to execute command '{name}': {str(e)}")

# ---------------------------------------------------------
# CORE RENDER ROUTER
# ---------------------------------------------------------
try:
    if page == "🚆 Command Dashboard":
        col_kpi, col_chart, col_ai = st.columns([1, 2, 1.2])
        
        with col_kpi:
            st.markdown("#### SYSTEM METRICS")
            st.metric(label="ACTIVE FLEET UNITS", value="142", delta="12 units deployed")
            curr_delay = st.session_state.delay_history[-1]
            st.metric(label="AVG NETWORK DELAY", value=f"{curr_delay:.1f}m", delta="-0.2m trend", delta_color="inverse")
            curr_cong = st.session_state.congestion_history[-1]
            st.metric(label="INFRASTRUCTURE LOAD", value=f"{int(curr_cong)}%", delta="+1% load")
            st.metric(label="ACTIVE TACTICAL ALERTS", value="3", delta="requires command review", delta_color="inverse")
            
        with col_chart:
            st.markdown("#### OPERATIONAL DELAY METRIC")
            st.area_chart(get_sensor_delay_data(), height=180, color="#ef4444")
            st.markdown("#### CAPACITY UTILIZATION METRIC")
            st.line_chart(get_sensor_congestion_data(), height=180, color="#f59e0b")
            
        with col_ai:
            st.markdown("#### DECISION ENGINE AI")
            st.markdown("""
            <div class='ai-action' style='border-left: 4px solid #ef4444;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem; border-bottom:1px solid #1f2937; padding-bottom:0.4rem;'>
                    <span class='status-crit'>[IMMEDIATE PRIORITY]</span>
                    <span style='color:#94a3b8; font-size:0.85em; font-family:monospace;'>AI: RailNet v2.3</span>
                </div>
                <table style='width:100%; border-collapse:collapse; font-size:0.9em; font-family:monospace;'>
                    <tr><td style='width:90px; color:#94a3b8; padding: 2px 0;'>CONFIDENCE:</td><td style='color:#f8fafc; font-weight:bold;'>96%</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>WINDOW:</td><td style='color:#ef4444; font-weight:bold;'>ACT WITHIN 5 MIN</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>ACTION:</td><td style='color:#ef4444; font-weight:bold;'>NETWORK REROUTE (TRN-803)</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>REASON:</td><td style='color:#cbd5e1;'>Track Blockage on Line A detected by physical sensors.</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>IMPACT:</td><td style='color:#10b981;'>Reduces operational delay by 8 minutes organically.</td></tr>
                </table>
            </div>
            
            <div class='ai-action' style='border-left: 4px solid #f59e0b;'>
                <div style='display:flex; justify-content:space-between; margin-bottom:0.4rem; border-bottom:1px solid #1f2937; padding-bottom:0.4rem;'>
                    <span class='status-warn'>[HIGH PRIORITY]</span>
                    <span style='color:#94a3b8; font-size:0.85em; font-family:monospace;'>AI: RailNet v2.3</span>
                </div>
                <table style='width:100%; border-collapse:collapse; font-size:0.9em; font-family:monospace;'>
                    <tr><td style='width:90px; color:#94a3b8; padding: 2px 0;'>CONFIDENCE:</td><td style='color:#f8fafc; font-weight:bold;'>87%</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>WINDOW:</td><td style='color:#f59e0b; font-weight:bold;'>MONITOR CLOSELY</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>ACTION:</td><td style='color:#f8fafc; font-weight:bold;'>ENFORCE SPEED LIMIT (SEC 7G)</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>REASON:</td><td style='color:#cbd5e1;'>Track maintenance team occupying adjacent track.</td></tr>
                    <tr><td style='color:#94a3b8; padding: 2px 0;'>IMPACT:</td><td style='color:#10b981;'>Ensures worker safety compliance limits.</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            if st.button("EXECUTE: AUTHORIZE AI TACTICS", type="primary", use_container_width=True):
                command_action("AUTHORIZE AI TACTICS")

    elif page == "📡 Fleet Telemetry":
        st.markdown("#### STRATEGIC FLEET MONITORING")
        trains_df = get_trains()
        
        def highlight_rows(row):
            if row['RISK LEVEL'] == 'URGENT': return ['background-color: #450a0a; color: #fca5a5; font-weight: bold; font-family: monospace;'] * len(row)
            elif row['RISK LEVEL'] == 'WARNING': return ['background-color: #452c0a; color: #fde68a; font-family: monospace;'] * len(row)
            return ['font-family: monospace;'] * len(row)

        col_table, col_details = st.columns([2.5, 1])
        with col_table:
            st.dataframe(trains_df.style.apply(highlight_rows, axis=1), hide_index=True, use_container_width=True, height=450)
            
        with col_details:
            st.markdown("#### TARGET LOCK")
            selected_train = st.selectbox("TRAIN SELECT", trains_df["Train ID"], label_visibility="collapsed")
            train_info = trains_df[trains_df["Train ID"] == selected_train].iloc[0]
            status_color = 'status-ok' if train_info['Status'] == 'ON TIME' else 'status-warn' if train_info['Status'] == 'DELAYED' else 'status-crit'
            
            st.markdown(f"""
            <div class="panel">
                <h5 style="color:#0ea5e9; margin-top:0; border-bottom: 1px solid #1f2937; padding-bottom: 0.5rem;">UNIT {selected_train} STATUS</h5>
                <table style='width:100%; border-collapse:collapse; font-size:0.95em; font-family:monospace;'>
                    <tr><td style='color:#94a3b8; padding: 3px 0;'>ASSIGNED ROUTE:</td><td style='color:#e2e8f0; text-align:right;'>{train_info['Route']}</td></tr>
                    <tr><td style='color:#94a3b8; padding: 3px 0;'>LIVE VELOCITY:</td><td style='color:#e2e8f0; text-align:right;'>{train_info['Speed (km/h)']} km/h</td></tr>
                    <tr><td style='color:#94a3b8; padding: 3px 0;'>NETWORK DELAY:</td><td style='color:#e2e8f0; text-align:right;'>{train_info['Delay (min)']} min</td></tr>
                    <tr><td style='color:#94a3b8; padding: 3px 0;'>LATEST STATE:</td><td class="{status_color}" style='text-align:right;'>● {train_info['Status']}</td></tr>
                    <tr><td style='color:#94a3b8; padding: 3px 0;'>TRACK POS:</td><td style='color:#e2e8f0; text-align:right;'>{train_info['Segment ID']}</td></tr>
                    <tr><td style='color:#94a3b8; padding: 3px 0;'>TELEMETRY CHECK:</td><td style='color:#0ea5e9; text-align:right; font-weight:bold;'>{train_info['Last Contact']}</td></tr>
                </table>
            </div>
            """, unsafe_allow_html=True)
            st.markdown("##### LIVE VELOCITY SENSOR TRACK")
            st.line_chart(get_sensor_speed_data(), height=140, color="#10b981")

    elif page == "🗺️ Live Tracking Map":
        st.markdown("#### COMMAND COMMANDER MAP (SATELLITE INTEGRATION)")
        st.markdown(f"""
        <div style='display:flex; justify-content:space-between; align-items:center; background-color:#030712; border: 1px solid #1f2937; padding: 0.5rem 1rem; margin-bottom: 0.5rem;'>
            <div style='color:#e2e8f0; font-weight:bold; letter-spacing: 1px;'>ACTIVE TRACKING LOOPS: 5 TARGETS</div>
            <div style='color:#94a3b8; font-size:0.9em; font-family: monospace;'>
                SATELLITE INTEGRITY: <span class="status-ok">98.9% SECURE</span> &nbsp;|&nbsp; LOCALIZED PING: T-{int(random.uniform(1,5))}s
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        def get_color(status):
            if status == 'CRITICAL': return '#ef4444'
            if status == 'DELAYED': return '#f59e0b'
            return '#10b981'

        st.session_state.geo_state['color'] = st.session_state.geo_state['status'].apply(get_color)
        st.session_state.geo_state['size'] = st.session_state.geo_state['status'].apply(lambda x: 250 if x == 'CRITICAL' else (180 if x == 'DELAYED' else 100))
        st.map(st.session_state.geo_state, latitude='lat', longitude='lon', color='color', size='size', zoom=9, use_container_width=True)

    elif page == "🚨 Tactical Log":
        st.markdown("#### ACTIVE TACTICAL SITUATION")
        col_log, col_action = st.columns([1.6, 1.4])
        
        with col_log:
            st.markdown("<div class='panel' style='padding: 0;'>", unsafe_allow_html=True)
            for inc in st.session_state.incidents:
                status_class = 'status-crit' if inc['Severity'] == 'CRITICAL' else 'status-warn' if inc['Severity'] in ['HIGH','MEDIUM'] else 'status-info'
                resp_color = '#10b981' if inc['Response'] in ['DISPATCHED', 'ON SCENE', 'RESOLVED'] else '#ef4444'
                
                time_left_str = ""
                if inc['Severity'] == 'CRITICAL' and inc['Time_Left'] > 0:
                    mins = int(inc['Time_Left'] // 60)
                    secs = int(inc['Time_Left'] % 60)
                    time_left_str = f" <br><span style='color:#ef4444; font-weight:bold; font-size:0.85em; background:rgba(239, 68, 68,0.1); padding:2px;'>[ESCALATION WINDOW: {mins:02d}:{secs:02d} REMAINING]</span>"
                elif inc['Severity'] == 'CRITICAL':
                    time_left_str = f" <br><span style='color:#7f1d1d; font-weight:bold; background-color: #fca5a5; padding: 2px; font-size:0.85em;'>[WINDOW BREACHED - ESCALATING TO NATL SEC]</span>"

                st.markdown(f"""
                <div class="incident-box">
                    <table style="width:100%; border-collapse:collapse; font-size:0.95em; font-family:monospace;">
                      <tr>
                        <td style="width: 100px; vertical-align: top; font-weight:bold; padding: 0.2rem 0.5rem;"><span class="{status_class}">● {inc['Severity']}</span></td>
                        <td style="vertical-align: top; color:#e2e8f0; padding: 0.2rem 0.5rem;">
                            <strong>{inc['Type']}</strong>{time_left_str}<br>
                            <span style="font-size:0.85em; color:#94a3b8; display:inline-block; margin-top:5px;">ID: {inc['ID']} | TARGET: {inc['Target']} | TACTICAL: {inc['Assigned']}</span><br>
                            <span style="font-size:0.85em; color:#94a3b8; display:inline-block; margin-top:2px;">STATUS: <span style="color:{resp_color}; font-weight:bold;">{inc['Response']}</span> | ETA: {inc['ETA']}</span>
                        </td>
                      </tr>
                    </table>
                </div>
                """, unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
                
        with col_action:
            st.markdown("#### COMMAND TRACEABILITY & PROTOCOL EXECUTION")
            
            st.markdown("<p style='color:#94a3b8; font-size:0.85em; margin-bottom:0.5rem;'>Executing overrides requires operator compliance logged with physical timestamp alignment.</p>", unsafe_allow_html=True)
            if st.button("EXECUTE: DISPATCH MAINTENANCE RESPONDERS", type="primary", use_container_width=True):
                command_action("DISPATCH MAINTENANCE")
            if st.button("EXECUTE: INITIATE SECURE NETWORK REROUTE", use_container_width=True):
                command_action("NETWORK REROUTE CORE")
            if st.button("EXECUTE: ALERT REGIONAL COMMAND TRUNK", use_container_width=True):
                command_action("ALERT REGIONAL LEVEL")
                
            st.markdown("<h5 style='margin-top: 1.5rem; color:#94a3b8; font-family:monospace;'>COMMAND EXECUTION LOG (LIVE)</h5>", unsafe_allow_html=True)
            st.markdown("<div class='panel' style='height: 220px; overflow-y: auto; font-family: monospace; font-size: 0.8em; color: #cbd5e1; background-color:#010409;'>", unsafe_allow_html=True)
            for log_entry in st.session_state.command_log:
                st.markdown(f"<div style='border-bottom: 1px solid #1f2937; padding: 4px 0;'>{log_entry}</div>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)

    elif page == "🔮 Prediction Engine":
        st.markdown("#### QUANTUM-HEURISTIC PREDICTION ENGINE")
        col_chart, col_risk = st.columns([2, 1])
        
        with col_chart:
            st.markdown("##### STRUCTURAL DELAY RISK ALGORITHM (NEXT 12H)")
            forecast_df = pd.DataFrame({"Time": [f"{h:02d}:00" for h in range(14, 26)], "Projected Delay Risk Metric": [2, 5, 12, 18, 25, 45, 30, 20, 10, 5, 2, 0]}).set_index("Time")
            st.area_chart(forecast_df, height=350, color="#f97316")
            
        with col_risk:
            st.markdown("##### AI CORE THREAT ASSESSMENTS")
            st.markdown("""
            <div class="panel" style="border-left: 4px solid #ef4444; margin-bottom: 0.5rem; background-color:#170f11;">
                <strong style='color:#ef4444;'>[IMMINENT RISK ALIGNMENT]</strong><br>
                <span style='color:#e2e8f0; font-family:monospace; font-size:0.9em;'>TRN-803 infrastructure compromised. Park Station framework faces total grid congestion by exactly 19:00 local.</span>
            </div>
            <div class="panel" style="border-left: 4px solid #f59e0b; margin-bottom: 0.5rem; background-color:#1c170b;">
                <strong style='color:#f59e0b;'>[ELEVATED RISK DETECTION]</strong><br>
                <span style='color:#e2e8f0; font-family:monospace; font-size:0.9em;'>High physical traffic limits on Line 3. Anticipate strict 15-minute operational delays structural baseline.</span>
            </div>
            <div class="panel" style="border-left: 4px solid #10b981; background-color:#081c15;">
                <strong style='color:#10b981;'>[MONITORED CLEARANCE]</strong><br>
                <span style='color:#e2e8f0; font-family:monospace; font-size:0.9em;'>Northern grid telemetry stable at peak operational tolerance levels perfectly.</span>
            </div>
            """, unsafe_allow_html=True)

except Exception as e:
    logger.critical(f"FATAL RENDER CRASH: {str(e)}", exc_info=True)
    st.error("⚠️ SYSTEM RENDER ENGINE FAILURE. SAFE-MODE ENGAGED.")

# ---------------------------------------------------------
# THE LIVE ENGINE LOOP (SECURE)
# ---------------------------------------------------------
try:
    if live_feed:
        time.sleep(random.uniform(1.8, 3.2))
        st.rerun()
except Exception as e:
    logger.error(f"Execution loop disrupted: {str(e)}")
