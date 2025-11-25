import React, { useState } from "react";
import Sidebar from "./components/sidebar";
import Home from "./pages/Home";
import HistoricalData from "./pages/HistoricalData";
import Settings from "./pages/Settings";
import Predictions from "./pages/Predictions";

export default function App() {
  const [activePage, setActivePage] = useState("Home");
  const [collapsed, setCollapsed] = useState(false);

  const handleSelect = (item) => {
    if (item === "toggleSidebar") {
      setCollapsed((prev) => !prev);
      return;
    }
    setActivePage(item);
  };

  return (
    <div style={{ display: "flex" }}>
      <Sidebar
        active={activePage}
        collapsed={collapsed}
        onSelect={handleSelect}
      />
      <div
        style={{
          flex: 1,
          background: "#0D1117",
          minHeight: "100vh",
          marginLeft: collapsed ? "80px" : "250px",
          transition: "margin-left 0.3s ease",
          padding: "2rem",
        }}
      >
        {activePage === "Home" && <Home />}
        {activePage === "Historical Data" && <HistoricalData />}
        {activePage === "Settings" && <Settings />}
        {activePage === "Predictions" && <Predictions />}
      </div>
    </div>
  );
}
