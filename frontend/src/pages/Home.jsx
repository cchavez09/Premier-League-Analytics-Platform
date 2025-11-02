import React, { useEffect, useState } from "react";

export default function Home() {
  const [table, setTable] = useState([]);
  const [upcoming, setUpcoming] = useState([]);
  const [recent, setRecent] = useState([]);
  const [loading, setLoading] = useState(true);
  const [corsError, setCorsError] = useState(false);

  // ✅ Import API key from .env (Vite syntax)
const API_KEY = process.env.REACT_APP_HOME_API_KEY; 
 const PROXY = "https://cors-anywhere.herokuapp.com/";

  // === Fetch Premier League Table ===
  useEffect(() => {
    async function fetchPLTable() {
      try {
        const response = await fetch(
          `${PROXY}https://api.football-data.org/v4/competitions/PL/standings`,
          { headers: { "X-Auth-Token": API_KEY } }
        );
        if (!response.ok) throw new Error("CORS or network error");
        const data = await response.json();
        setTable(data.standings?.[0]?.table || []);
      } catch (err) {
        console.error("Error fetching table:", err);
        setCorsError(true);
      } finally {
        setLoading(false);
      }
    }
    fetchPLTable();
  }, [API_KEY]);

  // === Fetch Upcoming & Recent Matches ===
  useEffect(() => {
    async function fetchMatches() {
      try {
        const upcomingRes = await fetch(
          `${PROXY}https://api.football-data.org/v4/competitions/PL/matches?status=SCHEDULED`,
          { headers: { "X-Auth-Token": API_KEY } }
        );
        const recentRes = await fetch(
          `${PROXY}https://api.football-data.org/v4/competitions/PL/matches?status=FINISHED`,
          { headers: { "X-Auth-Token": API_KEY } }
        );

        if (!upcomingRes.ok || !recentRes.ok)
          throw new Error("CORS or network error");

        const upcomingData = await upcomingRes.json();
        const recentData = await recentRes.json();

        setUpcoming(upcomingData.matches.slice(0, 5));
        const lastFive = recentData.matches.slice(-5).reverse();
        setRecent(lastFive);
      } catch (err) {
        console.error("Error fetching matches:", err);
        setCorsError(true);
      }
    }
    fetchMatches();
  }, [API_KEY]);

  const predictions = [
    { team: "Liverpool", percent: 78 },
    { team: "Man City", percent: 65 },
    { team: "Arsenal", percent: 62 },
  ];

  const openCorsDemo = () => {
    window.open("https://cors-anywhere.herokuapp.com/corsdemo", "_blank");
  };

  if (corsError) {
    return (
      <div
        style={{
          backgroundColor: "#0D1117",
          color: "#E5E7EB",
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          flexDirection: "column",
          textAlign: "center",
          fontFamily: "'Inter', sans-serif",
          padding: "2rem",
          boxSizing: "border-box",
        }}
      >
        <h2 style={{ color: "#FF4D4D" }}>⚠️ Request for Temporary Access</h2>
        <p style={{ color: "#9CA3AF", maxWidth: "480px", marginBottom: "1rem" }}>
          This app uses <b>cors-anywhere.herokuapp.com</b> to fetch live Premier
          League data. Please click below to request temporary access.
        </p>
        <button
          onClick={openCorsDemo}
          style={{
            backgroundColor: "#00FF87",
            color: "#0D1117",
            border: "none",
            padding: "0.7rem 1.5rem",
            borderRadius: "8px",
            fontWeight: "600",
            cursor: "pointer",
            fontSize: "1rem",
          }}
          onMouseEnter={(e) => (e.target.style.backgroundColor = "#00cc6f")}
          onMouseLeave={(e) => (e.target.style.backgroundColor = "#00FF87")}
        >
          Request Temporary Access
        </button>
      </div>
    );
  }

  return (
    <div
      style={{
        backgroundColor: "#0D1117",
        color: "#E5E7EB",
        minHeight: "100vh",
        marginLeft: "250px",
        padding: "2rem",
        fontFamily: "'Inter', sans-serif",
        overflowX: "hidden",
      }}
    >
      {/* === Header === */}
      <div style={{ marginBottom: "2rem" }}>
        <h1 style={{ margin: 0, fontSize: "2rem", fontWeight: "700" }}>
          Dashboard
        </h1>
        <p style={{ margin: 0, color: "#9CA3AF" }}>
          Premier League 2024/25 Analytics
        </p>
      </div>

      {/* === GRID LAYOUT === */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(2, minmax(0, 1fr))",
          gap: "2rem",
          justifyItems: "center",
          alignItems: "start",
        }}
      >
        {/* === League Table (Only scrollable one) === */}
        <div
          style={{
            backgroundColor: "#111827",
            borderRadius: "12px",
            padding: "1.5rem",
            maxHeight: "400px",
            overflowY: "auto",
            overflowX: "hidden",
            width: "95%",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: "1rem" }}>League Table</h3>
          {loading ? (
            <p style={{ color: "#9CA3AF" }}>Loading Premier League table...</p>
          ) : (
            <table
              style={{
                width: "100%",
                borderCollapse: "collapse",
                textAlign: "left",
              }}
            >
              <thead>
                <tr style={{ color: "#9CA3AF", fontSize: "0.9rem" }}>
                  <th style={{ padding: "0.5rem" }}>#</th>
                  <th style={{ padding: "0.5rem" }}>Team</th>
                  <th style={{ padding: "0.5rem", textAlign: "right" }}>P</th>
                  <th style={{ padding: "0.5rem", textAlign: "right" }}>W</th>
                  <th style={{ padding: "0.5rem", textAlign: "right" }}>D</th>
                  <th style={{ padding: "0.5rem", textAlign: "right" }}>L</th>
                  <th style={{ padding: "0.5rem", textAlign: "right" }}>GD</th>
                  <th style={{ padding: "0.5rem", textAlign: "right" }}>Pts</th>
                </tr>
              </thead>
              <tbody>
                {table.map((team) => (
                  <tr
                    key={team.team.id}
                    style={{
                      borderBottom: "1px solid #1F2937",
                      fontSize: "0.9rem",
                    }}
                  >
                    <td style={{ padding: "0.5rem" }}>{team.position}</td>
                    <td
                      style={{
                        padding: "0.5rem",
                        display: "flex",
                        alignItems: "center",
                        gap: "0.5rem",
                      }}
                    >
                      <img
                        src={team.team.crest}
                        alt={team.team.name}
                        style={{ width: 20, height: 20 }}
                      />
                      {team.team.name}
                    </td>
                    <td style={{ padding: "0.5rem", textAlign: "right" }}>
                      {team.playedGames}
                    </td>
                    <td style={{ padding: "0.5rem", textAlign: "right" }}>
                      {team.won}
                    </td>
                    <td style={{ padding: "0.5rem", textAlign: "right" }}>
                      {team.draw}
                    </td>
                    <td style={{ padding: "0.5rem", textAlign: "right" }}>
                      {team.lost}
                    </td>
                    <td style={{ padding: "0.5rem", textAlign: "right" }}>
                      {team.goalDifference}
                    </td>
                    <td
                      style={{
                        padding: "0.5rem",
                        textAlign: "right",
                        fontWeight: 600,
                        color: "#00FF87",
                      }}
                    >
                      {team.points}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          )}
        </div>

        {/* === Recent Matches === */}
        <div
          style={{
            backgroundColor: "#111827",
            borderRadius: "12px",
            padding: "1.5rem",
            height: "400px",
            width: "95%",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: "1rem" }}>Recent Matches</h3>
          {recent.length === 0 ? (
            <p style={{ color: "#9CA3AF" }}>Loading recent matches...</p>
          ) : (
            recent.map((m, i) => (
              <div
                key={i}
                style={{
                  backgroundColor: "#0F172A",
                  borderRadius: "10px",
                  padding: "0.8rem 1rem",
                  marginBottom: "0.7rem",
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <span>
                  {m.homeTeam.name} vs {m.awayTeam.name}
                </span>
                <strong>
                  {m.score.fullTime.home} - {m.score.fullTime.away}
                </strong>
              </div>
            ))
          )}
        </div>

        {/* === Upcoming Fixtures === */}
        <div
          style={{
            backgroundColor: "#111827",
            borderRadius: "12px",
            padding: "1.5rem",
            height: "400px",
            width: "95%",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: "1rem" }}>
            Upcoming Fixtures
          </h3>
          {upcoming.length === 0 ? (
            <p style={{ color: "#9CA3AF" }}>Loading upcoming fixtures...</p>
          ) : (
            upcoming.map((f, i) => (
              <div
                key={i}
                style={{
                  backgroundColor: "#0F172A",
                  borderRadius: "10px",
                  padding: "1rem",
                  marginBottom: "0.8rem",
                  display: "flex",
                  justifyContent: "space-between",
                }}
              >
                <div>
                  <p
                    style={{
                      margin: 0,
                      fontSize: "0.8rem",
                      color: "#9CA3AF",
                      marginBottom: "0.3rem",
                    }}
                  >
                    {new Date(f.utcDate).toLocaleDateString("en-GB", {
                      weekday: "short",
                      month: "short",
                      day: "numeric",
                    })}
                  </p>
                  <p style={{ margin: 0, fontWeight: 500 }}>
                    {f.homeTeam.name} vs {f.awayTeam.name}
                  </p>
                </div>
                <span style={{ color: "#00FF87", fontWeight: 600 }}>
                  GW {f.matchday}
                </span>
              </div>
            ))
          )}
        </div>

        {/* === Predictions === */}
        <div
          style={{
            backgroundColor: "#111827",
            borderRadius: "12px",
            padding: "1.5rem",
            height: "400px",
            width: "95%",
          }}
        >
          <h3 style={{ marginTop: 0, marginBottom: "1rem" }}>
            Next Gameweek Predictions
          </h3>
          {predictions.map((p) => (
            <div key={p.team} style={{ marginBottom: "1rem" }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  marginBottom: "0.3rem",
                }}
              >
                <span>{p.team}</span>
                <span style={{ color: "#00FF87", fontWeight: 600 }}>
                  {p.percent}%
                </span>
              </div>
              <div
                style={{
                  height: "8px",
                  backgroundColor: "#1F2937",
                  borderRadius: "5px",
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${p.percent}%`,
                    height: "100%",
                    backgroundColor: "#00FF87",
                    borderRadius: "5px",
                    transition: "width 0.5s ease",
                  }}
                ></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
