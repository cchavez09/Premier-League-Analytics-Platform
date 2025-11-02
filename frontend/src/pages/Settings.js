import React from "react";

export default function Settings() {
  return (
    <div
      style={{
        marginLeft: "250px", // ✅ space for sidebar
        padding: "2rem",
        fontFamily: "'Inter', sans-serif",
        minHeight: "100vh",
        backgroundColor: "#0D1117", // ✅ match sidebar background
        color: "#E5E7EB", // ✅ match text color
        boxSizing: "border-box",
      }}
    >
      <h1
        style={{
          fontSize: "2rem",
          fontWeight: "700",
          color: "#00FF87", // ✅ Futstat accent color
          marginBottom: "1rem",
        }}
      >
        ⚙️ Settings
      </h1>

      <p
        style={{
          fontSize: "1.1rem",
          color: "#9CA3AF", // muted gray text
        }}
      >
        This is the Settings page for Futstat.
      </p>

      <div
        style={{
          marginTop: "2rem",
          padding: "1.5rem",
          borderRadius: "0.75rem",
          backgroundColor: "#111827", // slightly lighter dark section
          border: "1px solid #1F2937",
          maxWidth: "600px",
        }}
      >
        <p style={{ color: "#9CA3AF" }}>
          (Here you can later add options for appearance, notifications, or
          data preferences.)
        </p>
      </div>
    </div>
  );
}