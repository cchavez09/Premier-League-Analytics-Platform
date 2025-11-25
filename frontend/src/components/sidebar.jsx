import React from "react";

export default function Sidebar({ active = "Home", onSelect, collapsed }) {
  const menuItems = [
    { label: "Home", icon: "🏠" },
    { label: "Predictions", icon: "📈" },
    { label: "Historical Data", icon: "📜" },
    { label: "Settings", icon: "⚙️" },
  ];

  return (
    <aside
      style={{
        width: collapsed ? "80px" : "250px",
        height: "100vh",
        background: "#0D1117",
        color: "#E5E7EB",
        borderRight: "1px solid #1F2937",
        padding: collapsed ? "1.5rem 0.5rem" : "1.5rem 1rem",
        boxSizing: "border-box",
        position: "fixed",
        left: 0,
        top: 0,
        transition: "width 0.3s ease, padding 0.3s ease",
        display: "flex",
        flexDirection: "column",
        fontFamily: "'Inter', system-ui, -apple-system, sans-serif",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: "10px",
          marginBottom: "1.5rem",
        }}
      >
        <div
          style={{
            width: collapsed ? "26px" : "30px",
            height: collapsed ? "26px" : "30px",
            background: "#00FF87",
            borderRadius: "50%",
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            color: "#022c22",
            fontWeight: 700,
            fontSize: collapsed ? "0.85rem" : "1rem",
            flexShrink: 0,
            transition: "all 0.25s ease",
          }}
        >
          F
        </div>

        {!collapsed && (
          <div style={{ overflow: "hidden" }}>
            <h2
              style={{
                fontSize: "1.2rem",
                fontWeight: 600,
                margin: 0,
                color: "#E5E7EB",
              }}
            >
              FutStat
            </h2>
            <p
              style={{
                margin: 0,
                marginTop: "0.15rem",
                fontSize: "0.75rem",
                color: "#9CA3AF",
              }}
            >
              Premier League Analytics
            </p>
          </div>
        )}
      </div>

      {/* Divider */}
      <div
        style={{
          height: "1px",
          width: "100%",
          background: "#1F2937",
          marginBottom: "1.25rem",
        }}
      />

      {/* Menu */}
      <nav style={{ flexGrow: 1 }}>
        {menuItems.map((item) => {
          const isActive = active === item.label;

          return (
            <button
              key={item.label}
              onClick={() => onSelect && onSelect(item.label)}
              style={{
                width: "100%",
                display: "flex",
                alignItems: "center",
                gap: "12px",
                padding: collapsed ? "0.65rem 0.5rem" : "0.7rem 0.9rem",
                background: isActive ? "#0F3A28" : "transparent",
                color: isActive ? "#00FF87" : "#D1D5DB",
                border: "none",
                textAlign: "left",
                borderRadius: "10px",
                cursor: "pointer",
                marginBottom: "0.45rem",
                transition: "background 0.2s ease, color 0.2s ease",
              }}
            >
              <span style={{ fontSize: "1.05rem" }}>{item.icon}</span>

              {!collapsed && (
                <span
                  style={{
                    fontSize: "0.95rem",
                    whiteSpace: "nowrap",
                    overflow: "hidden",
                    textOverflow: "ellipsis",
                  }}
                >
                  {item.label}
                </span>
              )}
            </button>
          );
        })}
      </nav>

      {/* Floating collapse toggle */}
      <button
        onClick={() => onSelect("toggleSidebar")}
        onMouseEnter={(e) => {
          e.currentTarget.style.boxShadow = "0 0 12px #00FF87";
          e.currentTarget.style.background = "#10241D";
        }}
        onMouseLeave={(e) => {
          e.currentTarget.style.boxShadow = "none";
          e.currentTarget.style.background = "#0D1117";
        }}
        style={{
          position: "absolute",
          top: "50%",
          right: "-16px",
          transform: "translateY(-50%)",
          width: "32px",
          height: "32px",
          borderRadius: "50%",
          border: "2px solid #00FF87",
          background: "#0D1117",
          color: "#00FF87",
          cursor: "pointer",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          fontSize: "1.1rem",
          fontWeight: "bold",
          transition: "all 0.25s ease",
          userSelect: "none",
        }}
      >
        {collapsed ? "❯" : "❮"}
      </button>
    </aside>
  );
}
