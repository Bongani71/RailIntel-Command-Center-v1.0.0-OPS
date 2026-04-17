"use client";
import { useState } from "react";
import {
  LineChart, Line, BarChart, Bar, AreaChart, Area,
  XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from "recharts";
import { Panel, SectionTitle, KpiCard, StatusBadge } from "@/components/ui";
import { DELAY_HISTORY, CONGESTION, FORECAST, INCIDENTS, TRAINS } from "@/lib/data";

// ─────────────────────────────────────────────
// OPERATIONS DASHBOARD
// ─────────────────────────────────────────────
export function Dashboard() {
  const hasCritical = INCIDENTS.some(i => i.severity === "CRITICAL" && i.status === "ACTIVE");

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
      {hasCritical && (
        <div className="critical-banner font-mono" style={{
          padding: "8px 14px",
          fontFamily: "monospace",
          fontSize: "12px",
          letterSpacing: "2px",
          textAlign: "center",
          fontWeight: "bold",
        }}>
          ⚠ CRITICAL NETWORK CONDITION — IMMEDIATE ACTION REQUIRED — INC-001: TRACK BLOCKAGE LINE A
        </div>
      )}

      <div style={{ display: "grid", gridTemplateColumns: "200px 1fr 240px", gap: "10px" }}>
        {/* LEFT: KPIs */}
        <div>
          <SectionTitle>Live Metrics</SectionTitle>
          <KpiCard label="Active Trains"     value={142}   color="#38bdf8" />
          <KpiCard label="Avg Delay"         value="4.2"   unit="min" color="#facc15" />
          <KpiCard label="Network Load"      value="78"    unit="%" color="#f97316" />
          <KpiCard label="Active Incidents"  value={3}     color="#ef4444" />
        </div>

        {/* CENTER: Charts */}
        <div style={{ display: "flex", flexDirection: "column", gap: "10px" }}>
          <Panel>
            <SectionTitle>Delay Trend — Past 12 Hours (minutes)</SectionTitle>
            <ResponsiveContainer width="100%" height={160}>
              <LineChart data={DELAY_HISTORY}>
                <CartesianGrid strokeDasharray="2 4" stroke="#1f2937" />
                <XAxis dataKey="time" tick={{ fill: "#475569", fontSize: 9 }} />
                <YAxis tick={{ fill: "#475569", fontSize: 9 }} />
                <Tooltip contentStyle={{ background: "#0b1220", border: "1px solid #1f2937", color: "#f8fafc", fontSize: 11 }} />
                <Line type="monotone" dataKey="delay" stroke="#38bdf8" strokeWidth={1.5} dot={false} />
              </LineChart>
            </ResponsiveContainer>
          </Panel>

          <Panel>
            <SectionTitle>Sector Congestion Load (%)</SectionTitle>
            <ResponsiveContainer width="100%" height={140}>
              <BarChart data={CONGESTION}>
                <CartesianGrid strokeDasharray="2 4" stroke="#1f2937" />
                <XAxis dataKey="sector" tick={{ fill: "#475569", fontSize: 9 }} />
                <YAxis tick={{ fill: "#475569", fontSize: 9 }} domain={[0, 100]} />
                <Tooltip contentStyle={{ background: "#0b1220", border: "1px solid #1f2937", color: "#f8fafc", fontSize: 11 }} />
                <Bar dataKey="load" fill="#0ea5e9" radius={0}
                  label={false}
                  // Color critical sectors red
                  className="congestion-bar"
                />
              </BarChart>
            </ResponsiveContainer>
          </Panel>
        </div>

        {/* RIGHT: AI Panel */}
        <Panel>
          <SectionTitle>AI Decision Support</SectionTitle>
          <AiCard type="REROUTE" color="#facc15" text="Reroute Train A12 via Line 3 to reduce delay by 8 minutes." action="APPROVE" />
          <AiCard type="SPEED"   color="#ef4444" text="Reduce speed on Line A — congestion at sector SND detected." action="ENFORCE" />
          <AiCard type="COMMS"   color="#38bdf8" text="Notify Sandton Station Manager of expected platform overflow." action="SEND" />
          <AiCard type="SIGNAL"  color="#f97316" text="Dispatch maintenance to Centurion Node — signal fault detected." action="DISPATCH" />
        </Panel>
      </div>
    </div>
  );
}

function AiCard({ type, color, text, action }: { type: string; color: string; text: string; action: string }) {
  return (
    <div style={{
      borderLeft: `3px solid ${color}`,
      padding: "8px 10px",
      marginBottom: "8px",
      background: "#0f1929",
    }}>
      <div style={{ fontFamily: "monospace", fontSize: "9px", color, letterSpacing: "1px", marginBottom: "3px" }}>[{type}]</div>
      <div style={{ fontSize: "11px", color: "#cbd5e1", marginBottom: "6px" }}>{text}</div>
      <button style={{
        border: `1px solid ${color}`,
        background: "transparent",
        color,
        padding: "2px 8px",
        fontFamily: "monospace",
        fontSize: "9px",
        cursor: "pointer",
        letterSpacing: "1px",
      }}>{action}</button>
    </div>
  );
}

// ─────────────────────────────────────────────
// TRAIN MONITORING
// ─────────────────────────────────────────────
export function TrainsPage() {
  const [selected, setSelected] = useState<string | null>(null);
  const train = TRAINS.find(t => t.id === selected);

  const statusColor = (s: string) =>
    s === "On Time" ? "#22c55e" : s === "Delayed" ? "#facc15" : "#ef4444";

  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: "10px" }}>
      <Panel>
        <SectionTitle>Train Monitoring System — Live Feed</SectionTitle>
        <table style={{ width: "100%", borderCollapse: "collapse", fontFamily: "monospace", fontSize: "11px" }}>
          <thead>
            <tr style={{ borderBottom: "1px solid #1f2937" }}>
              {["TRAIN ID", "ROUTE", "SPEED (KM/H)", "DELAY (MIN)", "STATUS"].map(h => (
                <th key={h} style={{ padding: "6px 8px", color: "#475569", textAlign: "left", fontSize: "9px", letterSpacing: "1px" }}>{h}</th>
              ))}
            </tr>
          </thead>
          <tbody>
            {TRAINS.map(t => (
              <tr key={t.id}
                onClick={() => setSelected(t.id)}
                style={{
                  cursor: "pointer",
                  borderBottom: "1px solid #111827",
                  background: selected === t.id ? "#0b1a2e" : "transparent",
                  transition: "background 0.1s",
                }}>
                <td style={{ padding: "7px 8px", color: "#38bdf8" }}>{t.id}</td>
                <td style={{ padding: "7px 8px", color: "#cbd5e1" }}>{t.route}</td>
                <td style={{ padding: "7px 8px", color: "#94a3b8" }}>{t.speed > 0 ? t.speed : "—"}</td>
                <td style={{ padding: "7px 8px", color: t.delay > 10 ? "#ef4444" : t.delay > 0 ? "#facc15" : "#22c55e" }}>{t.delay}</td>
                <td style={{ padding: "7px 8px" }}>
                  <StatusBadge label={t.status.toUpperCase()} color={statusColor(t.status)} />
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </Panel>

      <Panel>
        <SectionTitle>Train Telemetry</SectionTitle>
        {train ? (
          <>
            <div style={{ fontFamily: "monospace", fontSize: "16px", color: "#38bdf8", marginBottom: "10px" }}>{train.id}</div>
            <InfoRow label="Route"       value={train.route} />
            <InfoRow label="Speed"       value={`${train.speed} km/h`} />
            <InfoRow label="Curr Station" value={train.currentStation} />
            <InfoRow label="Next Station" value={train.nextStation} />
            <InfoRow label="Status"      value={train.status} color={statusColor(train.status)} />
            <InfoRow label="Delay Pred." value={train.delayPrediction} color={train.delay > 10 ? "#ef4444" : "#94a3b8"} />
            <div style={{ marginTop: "12px" }}>
              <SectionTitle>Velocity History (simulated)</SectionTitle>
              <ResponsiveContainer width="100%" height={100}>
                <LineChart data={[145,152,148,155,158,150,145,110,80,0].map((v,i)=>({ t: i, v }))}>
                  <XAxis dataKey="t" hide />
                  <YAxis hide domain={[0, 180]} />
                  <Line type="monotone" dataKey="v" stroke="#38bdf8" strokeWidth={1.5} dot={false} />
                </LineChart>
              </ResponsiveContainer>
            </div>
          </>
        ) : (
          <div style={{ color: "#334155", fontFamily: "monospace", fontSize: "11px", marginTop: "20px", textAlign: "center" }}>
            SELECT A TRAIN TO VIEW TELEMETRY
          </div>
        )}
      </Panel>
    </div>
  );
}

function InfoRow({ label, value, color = "#cbd5e1" }: { label: string; value: string | number; color?: string }) {
  return (
    <div style={{ display: "flex", justifyContent: "space-between", padding: "4px 0", borderBottom: "1px solid #111827", fontSize: "11px" }}>
      <span style={{ color: "#475569", fontFamily: "monospace" }}>{label}</span>
      <span style={{ color }}>{value}</span>
    </div>
  );
}

// ─────────────────────────────────────────────
// INCIDENT CONTROL
// ─────────────────────────────────────────────
const SEV_COLOR: Record<string, string> = {
  CRITICAL: "#ef4444",
  HIGH:     "#f97316",
  MEDIUM:   "#facc15",
  LOW:      "#22c55e",
};

const ACTIONS = [
  { label: "🔧 Dispatch Maintenance — Line A",   type: "primary" },
  { label: "🔄 Reroute Trains Away from PTA",    type: "warn" },
  { label: "📞 Notify National Control Center",  type: "info" },
  { label: "🚨 Escalate INC-001 to Level 3",     type: "danger" },
];

export function IncidentsPage() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 280px", gap: "10px" }}>
      <Panel>
        <SectionTitle>Active Incident Log</SectionTitle>
        {INCIDENTS.map(inc => {
          const color = SEV_COLOR[inc.severity];
          return (
            <div key={inc.id} style={{
              borderLeft: `4px solid ${color}`,
              background: `${color}0d`,
              padding: "10px 12px",
              marginBottom: "8px",
            }}>
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                <span style={{ fontFamily: "monospace", fontSize: "10px", color, letterSpacing: "1px" }}>
                  [{inc.severity}] {inc.id}
                </span>
                <span style={{ fontFamily: "monospace", fontSize: "10px", color: "#475569" }}>{inc.timestamp}</span>
              </div>
              <div style={{ fontFamily: "monospace", fontSize: "13px", color: "#f8fafc", marginTop: "4px" }}>{inc.type}</div>
              <div style={{ fontSize: "11px", color: "#94a3b8", marginTop: "2px" }}>TARGET: {inc.target}</div>
              <div style={{ fontSize: "10px", color: "#334155", marginTop: "4px", fontFamily: "monospace" }}>
                STATUS: <span style={{ color: inc.status === "ACTIVE" ? "#ef4444" : "#22c55e" }}>{inc.status}</span>
              </div>
            </div>
          );
        })}
      </Panel>

      <Panel>
        <SectionTitle>Recommended Actions</SectionTitle>
        <div style={{ fontSize: "10px", color: "#334155", fontFamily: "monospace", marginBottom: "10px" }}>
          AI-GENERATED — CONFIRM BEFORE EXECUTING
        </div>
        {ACTIONS.map((a, i) => {
          const color = a.type === "danger" ? "#ef4444" : a.type === "warn" ? "#facc15" : a.type === "info" ? "#38bdf8" : "#22c55e";
          return (
            <button key={i} style={{
              display: "block",
              width: "100%",
              marginBottom: "7px",
              padding: "8px 10px",
              background: "transparent",
              border: `1px solid ${color}`,
              color,
              fontFamily: "monospace",
              fontSize: "11px",
              textAlign: "left",
              cursor: "pointer",
            }}>{a.label}</button>
          );
        })}
      </Panel>
    </div>
  );
}

// ─────────────────────────────────────────────
// PREDICTIVE ANALYSIS
// ─────────────────────────────────────────────
const INSIGHTS = [
  { risk: "HIGH",   color: "#ef4444", text: "Train TRN-803 likely delayed 45 min at Park Station — cascading network load at 19:00." },
  { risk: "MEDIUM", color: "#facc15", text: "Peak congestion expected on Line 3 corridor. Estimated 10–15 min delays across central network." },
  { risk: "LOW",    color: "#22c55e", text: "Northern network remains stable. No anomalies detected in current forecast window." },
];

export function PredictivePage() {
  return (
    <div style={{ display: "grid", gridTemplateColumns: "1fr 300px", gap: "10px" }}>
      <Panel>
        <SectionTitle>12-Hour Delay Risk Forecast</SectionTitle>
        <ResponsiveContainer width="100%" height={320}>
          <AreaChart data={FORECAST}>
            <defs>
              <linearGradient id="riskGrad" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%"  stopColor="#38bdf8" stopOpacity={0.25} />
                <stop offset="95%" stopColor="#38bdf8" stopOpacity={0} />
              </linearGradient>
            </defs>
            <CartesianGrid strokeDasharray="2 4" stroke="#1f2937" />
            <XAxis dataKey="time" tick={{ fill: "#475569", fontSize: 9 }} />
            <YAxis tick={{ fill: "#475569", fontSize: 9 }} domain={[0, 80]} label={{ value: "risk %", angle: -90, position: "insideLeft", fill: "#334155", fontSize: 9 }} />
            <Tooltip contentStyle={{ background: "#0b1220", border: "1px solid #1f2937", color: "#f8fafc", fontSize: 11 }} />
            <Area type="monotone" dataKey="risk" stroke="#38bdf8" strokeWidth={1.5} fill="url(#riskGrad)" />
          </AreaChart>
        </ResponsiveContainer>
      </Panel>

      <Panel>
        <SectionTitle>Intelligence Insights</SectionTitle>
        {INSIGHTS.map((ins, i) => (
          <div key={i} style={{
            borderLeft: `4px solid ${ins.color}`,
            background: `${ins.color}0d`,
            padding: "10px 12px",
            marginBottom: "8px",
          }}>
            <div style={{ fontFamily: "monospace", fontSize: "10px", color: ins.color, letterSpacing: "1px", marginBottom: "4px" }}>
              [{ins.risk} RISK]
            </div>
            <div style={{ fontSize: "12px", color: "#cbd5e1" }}>{ins.text}</div>
          </div>
        ))}
      </Panel>
    </div>
  );
}

// ─────────────────────────────────────────────
// NETWORK MAP (placeholder)
// ─────────────────────────────────────────────
export function NetworkMap() {
  return (
    <Panel>
      <SectionTitle>Network Geo-Map — GP-NODE-01</SectionTitle>
      <div style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        height: "400px",
        color: "#1f2937",
        fontFamily: "monospace",
        fontSize: "12px",
        letterSpacing: "2px",
        border: "1px dashed #1f2937",
      }}>
        <div style={{ fontSize: "40px", marginBottom: "12px", opacity: 0.3 }}>🗺️</div>
        <div>GIS MODULE OFFLINE</div>
        <div style={{ fontSize: "10px", marginTop: "6px", color: "#1f2937" }}>
          CONTACT: sysadmin@railintel.co.za — REF: GIS-ERR-04
        </div>
      </div>
    </Panel>
  );
}

// ─────────────────────────────────────────────
// SYSTEM ARCHITECTURE
// ─────────────────────────────────────────────
export function ArchitecturePage() {
  const layers = [
    { layer: "FRONTEND",    tech: "Next.js 16 + TailwindCSS v4",     status: "ONLINE",  color: "#22c55e" },
    { layer: "API GATEWAY", tech: "FastAPI — uvicorn (ASGI)",         status: "ONLINE",  color: "#22c55e" },
    { layer: "WEBSOCKETS",  tech: "FastAPI WebSocket — /ws/telemetry",status: "ONLINE",  color: "#22c55e" },
    { layer: "DATABASE",    tech: "PostgreSQL 15",                    status: "ONLINE",  color: "#22c55e" },
    { layer: "MESSAGE BUS", tech: "Kafka (simulated)",                status: "SIMULATED",color: "#facc15" },
    { layer: "ML ENGINE",   tech: "LightGBM / XGBoost — delay pred.", status: "PENDING", color: "#f97316" },
    { layer: "CACHE",       tech: "Redis (planned)",                  status: "OFFLINE", color: "#ef4444" },
  ];

  return (
    <Panel>
      <SectionTitle>System Architecture — Node: GP-NODE-01</SectionTitle>
      <table style={{ width: "100%", borderCollapse: "collapse", fontFamily: "monospace", fontSize: "11px" }}>
        <thead>
          <tr style={{ borderBottom: "1px solid #1f2937" }}>
            {["LAYER", "TECHNOLOGY", "STATUS"].map(h => (
              <th key={h} style={{ padding: "6px 10px", color: "#334155", fontSize: "9px", letterSpacing: "1px", textAlign: "left" }}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {layers.map(row => (
            <tr key={row.layer} style={{ borderBottom: "1px solid #111827" }}>
              <td style={{ padding: "8px 10px", color: "#94a3b8" }}>{row.layer}</td>
              <td style={{ padding: "8px 10px", color: "#cbd5e1" }}>{row.tech}</td>
              <td style={{ padding: "8px 10px" }}>
                <StatusBadge label={row.status} color={row.color} />
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </Panel>
  );
}
