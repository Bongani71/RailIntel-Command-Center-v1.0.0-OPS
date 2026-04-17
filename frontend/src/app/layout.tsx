import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "RAILINTEL — Intelligent Rail Operations System",
  description: "Enterprise-grade railway control system for national rail operations.",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <head>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossOrigin="anonymous" />
        {/* eslint-disable-next-line @next/next/no-page-custom-font */}
        <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet" />
      </head>
      <body style={{ background: "#050a14", minHeight: "100vh" }}>{children}</body>
    </html>
  );
}
