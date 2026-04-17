"use client";
import React from "react";

// --- Logo SVG ---
export function RailIntelLogo({ size = 36 }: { size?: number }) {
  return (
    <svg width={size * 2.8} height={size} viewBox="0 0 140 50" fill="none" xmlns="http://www.w3.org/2000/svg">
      {/* Left rail */}
      <polygon points="8,44 16,8 19,8 11,44" fill="#38bdf8" />
      {/* Right rail */}
      <polygon points="30,44 22,8 25,8 33,44" fill="#fff" />
      {/* Sleepers */}
      <rect x="10" y="38" width="21" height="1.5" fill="#1f2937"/>
      <rect x="12" y="28" width="17" height="1.5" fill="#1f2937"/>
      <rect x="14" y="18" width="13" height="1.5" fill="#1f2937"/>
      {/* Signal waves */}
      <path d="M 20 6 Q 28 -1 38 6 T 52 0" stroke="#38bdf8" strokeWidth="1.8" fill="none"/>
      <path d="M 22 12 Q 30 5 40 12 T 54 6" stroke="#fff" strokeWidth="1.2" fill="none"/>
      {/* Text: RAILINTEL */}
      <text x="62" y="34" fontFamily="monospace" fontSize="20" fontWeight="900" fill="#ffffff" letterSpacing="1">RAIL</text>
      <text x="62" y="34" fontFamily="monospace" fontSize="20" fontWeight="900" fill="transparent" letterSpacing="1">RAIL</text>
      {/* Measure RAIL: ~46px wide at fontSize 20 */}
      <text x="108" y="34" fontFamily="monospace" fontSize="20" fontWeight="900" fill="#38bdf8" letterSpacing="1">INTEL</text>
    </svg>
  );
}

// --- Generic panel wrapper ---
export function Panel({ children, className = "" }: { children: React.ReactNode; className?: string }) {
  return (
    <div
      className={className}
      style={{
        background: "#0b1220",
        border: "1px solid #1f2937",
        padding: "12px 14px",
      }}
    >
      {children}
    </div>
  );
}

// --- Section heading ---
export function SectionTitle({ children }: { children: React.ReactNode }) {
  return (
    <div
      style={{
        fontFamily: "'Space Mono', monospace",
        fontSize: "10px",
        letterSpacing: "2px",
        textTransform: "uppercase",
        color: "#475569",
        borderBottom: "1px solid #1f2937",
        paddingBottom: "6px",
        marginBottom: "10px",
      }}
    >
      {children}
    </div>
  );
}

// --- Status badge ---
export function StatusBadge({ label, color }: { label: string; color: string }) {
  return (
    <span
      style={{
        display: "inline-block",
        padding: "1px 7px",
        border: `1px solid ${color}`,
        color,
        fontSize: "10px",
        fontFamily: "monospace",
        letterSpacing: "1px",
        background: `${color}15`,
      }}
    >
      {label}
    </span>
  );
}

// --- KPI Card ---
export function KpiCard({
  label, value, unit = "", color = "#38bdf8"
}: { label: string; value: string | number; unit?: string; color?: string }) {
  return (
    <div style={{
      background: "#0f1929",
      border: "1px solid #1f2937",
      borderLeft: `3px solid ${color}`,
      padding: "10px 12px",
      marginBottom: "8px",
    }}>
      <div style={{ fontSize: "9px", letterSpacing: "2px", color: "#475569", fontFamily: "monospace", textTransform: "uppercase" }}>{label}</div>
      <div style={{ fontSize: "26px", fontFamily: "'Space Mono', monospace", color, marginTop: "2px", lineHeight: 1.1 }}>
        {value}<span style={{ fontSize: "13px", color: "#64748b", marginLeft: "3px" }}>{unit}</span>
      </div>
    </div>
  );
}
