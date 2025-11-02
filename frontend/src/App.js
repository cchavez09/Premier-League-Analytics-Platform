import React, { useState } from "react";
import Sidebar from "./components/Sidebar";
import Home from "./pages/Home";
import HistoricalData from "./pages/HistoricalData";
import Settings from "./pages/Settings";
import Predictions from "./pages/Predictions";

export default function App() {
  const [activePage, setActivePage] = useState("Home");

  return (
    <div style={{ display: "flex" }}>
      <Sidebar active={activePage} onSelect={setActivePage} />
      <div style={{ flex: 1 }}>
        {activePage === "Home" && <Home />}
        {activePage === "Historical Data" && <HistoricalData />}
        {activePage === "Settings" && <Settings />}
        {activePage === "Predictions" && <Predictions />}
      
      </div>
    </div>
  );
}
