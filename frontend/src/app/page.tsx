"use client";
import { useState } from "react";
import { TopBar, Sidebar } from "@/components/shell";
import {
  Dashboard, TrainsPage, IncidentsPage,
  PredictivePage, NetworkMap, ArchitecturePage
} from "@/components/pages";

const PAGE_MAP: Record<string, React.ReactNode> = {
  dashboard:    <Dashboard />,
  map:          <NetworkMap />,
  trains:       <TrainsPage />,
  predictive:   <PredictivePage />,
  incidents:    <IncidentsPage />,
  architecture: <ArchitecturePage />,
};

const PAGE_TITLES: Record<string, string> = {
  dashboard:    "Operations Dashboard",
  map:          "Network Map",
  trains:       "Train Monitoring",
  predictive:   "Predictive Analysis",
  incidents:    "Incident Control",
  architecture: "System Architecture",
};

export default function Home() {
  const [activePage, setActivePage] = useState("dashboard");

  return (
    <div style={{ display: "flex", flexDirection: "column", height: "100vh", overflow: "hidden" }}>
      <TopBar active={activePage} onChange={setActivePage} />
      <div style={{ display: "flex", flex: 1, overflow: "hidden" }}>
        <Sidebar active={activePage} onChange={setActivePage} />
        <main style={{
          flex: 1,
          overflowY: "auto",
          padding: "14px",
          background: "#050a14",
        }}>
          {/* Page breadcrumb */}
          <div style={{
            fontFamily: "monospace",
            fontSize: "9px",
            letterSpacing: "2px",
            color: "#334155",
            marginBottom: "10px",
          }}>
            RAILINTEL / {PAGE_TITLES[activePage]?.toUpperCase()}
          </div>

          {PAGE_MAP[activePage]}
        </main>
      </div>
    </div>
  );
}
