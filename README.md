# RailIntel Command Center 🚆

**Validation Status:** PRODUCTION READY (v1.0.0-OPS)  
**Authority Level:** National Rail Control & Grid Execution  

Refined, hardened, and built for **mission-critical rail intelligence**. RailIntel is a strictly engineered, real-time command, control, and analytical dashboard natively modeling highly continuous kinetic telemetry, predictive algorithmic threat risk scaling, and hardware overriding infrastructure.

![Validation](https://img.shields.io/badge/Status-HARDENED-10b981?style=for-the-badge)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit)

## 👁️ System Interface Previews

| Command Dashboard | Live Tracking Map |
| :---: | :---: |
| <img src="docs/dashboard.png" width="100%"> | <img src="docs/map.png" width="100%"> |
| **Fleet Telemetry** | **Tactical Escalation Log** |
| <img src="docs/telemetry.png" width="100%"> | <img src="docs/tactical_log.png" width="100%"> |

---

## 🎯 Architecture Overview

RailIntel completely decouples the telemetry pipeline from rendering bounds utilizing **Strict Try/Except Matrices** and heavily governed physical routing logic. 

1. **AI Decision Engine (RailNet v2.3):** Evaluates live infrastructure load mapping outputting direct physical resolution actions tied to predictive `Action/Tolerance` mappings.
2. **Kinetic Fleet Map (Live Tracking):** Deeply binds internal Streamlit matrix charting variables capturing active tracking, ping statuses, and delay ratios autonomously mapping to coordinate vectors.
3. **Escalation Bounds (Incident Protocols):** Features explicit dynamic countdown parameters evaluating risk mathematically against physical network variables, actively breaching boundaries across physical GUI parameters automatically.
4. **Command Engine Persistence:** Natively writes command tracking physically into a locally locked `railintel_audit_trail.log` mimicking standard government audit traceability standards.

## 🚀 Execution & Deployment Protocol

### Local Initialisation Setup

Ensure Python `3.11+` is enabled. Set up your secure dependencies:
```bash
python -m venv venv
venv\Scripts\activate      # Windows Environment
source venv/bin/activate   # MacOS/Unix Deployment

pip install -r requirements.txt
```

### Engaging Systems
Launch the Command Interface exclusively rendering on port `8501`.
```bash
streamlit run app.py
```
*(An automated secure session log will boot tracking `OPR-7X9` telemetry overrides internally via standard terminal logging).*

### Backend Interface Deployment (API Nodes)
For full integration into the real infrastructure (if executing across physical servers), deploy the backend API engine safely:
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

## 🧪 Testing Matrices
Run algorithmic validations explicitly checking FastAPI endpoints, SQL Injection blocks, and Risk Engines natively through the pre-packaged command:
```bash
python test_system.py
```

## 🛡️ Enterprise Security Notice
**Note:** `.gitignore` enforces exclusion of local `.env` caches or operational data leaks. Never upload internal execution files (`railintel_audit_trail.log`) globally unless explicitly migrating environments.
