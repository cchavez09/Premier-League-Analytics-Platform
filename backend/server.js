// backend/server.js
// =====================================================
// FUTSTAT BACKEND SERVER
// =====================================================
const express = require("express");
const cors = require("cors");
const path = require("path");
 
// ✅ Load environment variables from pginfo.env
require("dotenv").config({ path: path.resolve(__dirname, "pginfo.env") });
 
// ✅ Use native fetch (Node 18+ supports it natively)
const fetch = (...args) =>
  import("node-fetch").then(({ default: fetch }) => fetch(...args));
 
const app = express();
app.use(cors());
app.use(express.json());
 
// =====================================================
// ROUTES IMPORTS (Team + Fixtures)
// =====================================================
const teamRoutes = require("./routes/teams");
const fixtureRoutes = require("./routes/fixtures");
 
app.use("/api/teams", teamRoutes);
app.use("/api/fixtures", fixtureRoutes);
 
// =====================================================
// HEALTH CHECK
// =====================================================
app.get("/", (req, res) => {
  res.send("✅ Futstat Backend is running ⚽");
});
 
// =====================================================
// LIVE PREMIER LEAGUE DATA ROUTE
// =====================================================
app.get("/api/live", async (req, res) => {
  try {
    console.log("📡 Fetching Premier League live data...");
 
    const apiKey = process.env.HOME_API_KEY;
    if (!apiKey) {
      console.error("❌ Missing HOME_API_KEY in pginfo.env");
      return res.status(500).json({ error: "Missing API key" });
    }
 
    const response = await fetch(
      "https://api.football-data.org/v4/competitions/PL/matches",
      {
        headers: { "X-Auth-Token": apiKey },
      }
    );
 
    if (!response.ok) {
      const errorText = await response.text();
      console.error("⚠️ API error:", response.status, errorText);
      return res
        .status(response.status)
        .json({ error: "Failed to fetch Premier League data" });
    }
 
    const data = await response.json();
    res.json(data);
  } catch (err) {
    console.error("💥 Server Error fetching live PL data:", err);
    res.status(500).json({ error: "Internal Server Error" });
  }
});
 
// =====================================================
// SERVER STARTUP
// =====================================================
const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`🚀 Server running on http://localhost:${PORT}`);
});
 
 
// ===== LEAGUE TABLE =====
app.get("/api/table", async (req, res) => {
  try {
    const response = await fetch(
      "https://api.football-data.org/v4/competitions/PL/standings",
      {
        headers: { "X-Auth-Token": process.env.HOME_API_KEY },
      }
    );
 
    if (!response.ok) {
      return res.status(response.status).json({ error: "Failed to fetch standings" });
    }
 
    const data = await response.json();
    res.json(data.standings?.[0]?.table || []);
  } catch (err) {
    console.error("Error fetching table:", err);
    res.status(500).json({ error: "Server error fetching table" });
  }
});