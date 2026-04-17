"use client";
import { useState, useEffect } from "react";
import { RailIntelLogo } from "@/components/ui";

const NAV_ITEMS = [
  { icon: "🚆", label: "Operations Dashboard", id: "dashboard" },
  { icon: "🗺️", label: "Network Map",          id: "map" },
  { icon: "📡", label: "Train Monitoring",     id: "trains" },
  { icon: "🔮", label: "Predictive Analysis",  id: "predictive" },
  { icon: "🚨", label: "Incident Control",     id: "incidents" },
  { icon: "⚙️", label: "System Architecture",  id: "architecture" },
];

interface Props {
  active: string;
  onChange: (id: string) => void;
}

export function TopBar({ active, onChange }: Props) {
  const [time, setTime] = useState("");

  useEffect(() => {
    const tick = () => setTime(new Date().toLocaleTimeString("en-ZA", { hour12: false }));
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  return (
    <header style={{
      background: "#050a14",
      borderBottom: "1px solid #1f2937",
      padding: "0 20px",
      height: "48px",
      display: "flex",
      alignItems: "center",
      justifyContent: "space-between",
      position: "sticky",
      top: 0,
      zIndex: 100,
    }}>
      <div style={{ display: "flex", alignItems: "center", gap: "12px" }}>
        <RailIntelLogo size={28} />
        <span style={{ borderLeft: "1px solid #1f2937", paddingLeft: "12px", fontFamily: "monospace", fontSize: "11px", color: "#475569", letterSpacing: "2px" }}>
          INTELLIGENT RAIL OPERATIONS SYSTEM
        </span>
      </div>

      <div style={{ display: "flex", gap: "24px", alignItems: "center" }}>
        <Pill label="SYSTEM" value="STABLE" color="#22c55e" />
        <Pill label="NETWORK" value="ONLINE" color="#22c55e" />
        <Pill label="LATENCY" value="14ms" color="#38bdf8" />
        <Pill label="LAST SYNC" value={time} color="#94a3b8" />
      </div>
    </header>
  );
}

function Pill({ label, value, color }: { label: string; value: string; color: string }) {
  return (
    <div style={{ fontFamily: "monospace", fontSize: "10px" }}>
      <span style={{ color: "#475569", marginRight: "5px" }}>{label}:</span>
      <span style={{ color }}>{value}</span>
    </div>
  );
}

export function Sidebar({ active, onChange }: Props) {
  return (
    <aside style={{
      width: "216px",
      minWidth: "216px",
      background: "#050a14",
      borderRight: "1px solid #1f2937",
      display: "flex",
      flexDirection: "column",
      paddingTop: "12px",
    }}>
      {NAV_ITEMS.map((item) => {
        const isActive = active === item.id;
        return (
          <button
            key={item.id}
            onClick={() => onChange(item.id)}
            style={{
              display: "flex",
              alignItems: "center",
              gap: "10px",
              padding: "9px 16px",
              background: isActive ? "#0b1a2e" : "transparent",
              borderLeft: isActive ? "2px solid #38bdf8" : "2px solid transparent",
              border: "none",
              color: isActive ? "#f8fafc" : "#475569",
              fontFamily: "monospace",
              fontSize: "11px",
              letterSpacing: "0.5px",
              cursor: "pointer",
              textAlign: "left",
              width: "100%",
              transition: "all 0.15s",
            }}
          >
            <span style={{ fontSize: "14px" }}>{item.icon}</span>
            <span>{item.label}</span>
          </button>
        );
      })}

      <div style={{ marginTop: "auto", padding: "16px", borderTop: "1px solid #111827" }}>
        <div style={{ fontFamily: "monospace", fontSize: "9px", color: "#334155", lineHeight: "1.8" }}>
          <div>USER: LOG-992</div>
          <div>ROLE: DISTRICT_CTRL</div>
          <div>SERVER: GP-NODE-01</div>
          <div style={{ display: "flex", alignItems: "center", gap: "5px" }}>
            <span className="blink" style={{ width: "5px", height: "5px", borderRadius: "50%", background: "#22c55e", display: "inline-block" }} />
            <span>LIVE</span>
          </div>
        </div>
      </div>
    </aside>
  );
}
