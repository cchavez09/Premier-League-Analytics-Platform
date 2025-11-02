import React, { useState } from "react";

export default function Predictions() {
  const teams = [
    "Liverpool",
    "Man City",
    "Arsenal",
    "Chelsea",
    "Tottenham",
    "Manchester United",
    "Newcastle",
    "Aston Villa",
  ];

  // default selected teams
  const [teamA, setTeamA] = useState("Liverpool");
  const [teamB, setTeamB] = useState("Man City");

  // static last 5 results
  const teamForm = {
    Liverpool: ["W", "W", "L", "D", "W"],
    "Man City": ["W", "W", "W", "D", "L"],
    Arsenal: ["W", "L", "W", "W", "D"],
    Chelsea: ["D", "W", "L", "L", "W"],
    Tottenham: ["W", "D", "L", "W", "W"],
    "Manchester United": ["L", "W", "W", "D", "W"],
    Newcastle: ["W", "L", "D", "W", "L"],
    "Aston Villa": ["D", "W", "W", "L", "W"],
  };

  // team badge colors
  const teamColors = {
    Liverpool: "radial-gradient(circle, #ff3b3b, #b02020)",
    "Man City": "radial-gradient(circle, #4b6fff, #2b4bd6)",
    Arsenal: "radial-gradient(circle, #ff2626, #a81818)",
    Chelsea: "radial-gradient(circle, #1e40af, #1d4ed8)",
    Tottenham: "radial-gradient(circle, #f5f5f5, #9ca3af)",
    "Manchester United": "radial-gradient(circle, #e11d48, #7f1d1d)",
    Newcastle: "radial-gradient(circle, #1f2937, #0f172a)",
    "Aston Villa": "radial-gradient(circle, #7e22ce, #581c87)",
  };

  return (
    <div
      style={{
        marginLeft: "250px",
        padding: "2.5rem",
        fontFamily: "'Inter', sans-serif",
        minHeight: "100vh",
        backgroundColor: "#0D1117",
        color: "#E5E7EB",
        boxSizing: "border-box",
      }}
    >
      {/* ===== HEADER ===== */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: "2rem",
        }}
      >
        <div>
          <h1
            style={{
              fontSize: "2rem",
              fontWeight: "700",
              color: "#00FF87",
              marginBottom: "0.3rem",
            }}
          >
            Predictions
          </h1>
          <p style={{ color: "#9CA3AF", fontSize: "0.95rem" }}>
            Analyze team stats and match probabilities
          </p>
        </div>
      </div>

      {/* ===== ROW 1: TEAM INSIGHTS ===== */}
      <div
        style={{
          backgroundColor: "#111827",
          borderRadius: "1rem",
          padding: "2rem",
          border: "1px solid #1F2937",
          marginBottom: "2.5rem",
        }}
      >
        <h2 style={{ color: "#FFFFFF", fontSize: "1.5rem", marginBottom: "1.5rem" }}>
          Team Insights
        </h2>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            gap: "2rem",
          }}
        >
          {[{ id: "A", team: teamA, setTeam: setTeamA },
            { id: "B", team: teamB, setTeam: setTeamB }].map(({ id, team, setTeam }) => (
            <div
              key={id}
              style={{
                flex: 1,
                backgroundColor: "#0F1623",
                borderRadius: "0.8rem",
                padding: "1.5rem",
                position: "relative",
              }}
            >
              {/* Dropdown to change team */}
              <select
                value=""
                onChange={(e) => {
                  const val = e.target.value;
                  if (val) setTeam(val);
                }}
                style={{
                  position: "absolute",
                  top: "1rem",
                  right: "1rem",
                  backgroundColor: "#1E2635",
                  color: "#E5E7EB",
                  border: "1px solid #1F2937",
                  borderRadius: "0.4rem",
                  padding: "0.35rem 0.6rem",
                  fontSize: "0.85rem",
                  cursor: "pointer",
                }}
              >
                <option value="" disabled hidden>
                  Select Other Team
                </option>
                {teams.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>

              <div style={{ textAlign: "center", marginBottom: "1rem" }}>
                <div
                  style={{
                    width: "50px",
                    height: "50px",
                    borderRadius: "50%",
                    margin: "0 auto 0.8rem",
                    background: teamColors[team],
                  }}
                ></div>
                <h3
                  style={{
                    color: "#FFFFFF",
                    margin: 0,
                    fontSize: "1.3rem",
                    fontWeight: "600",
                  }}
                >
                  {team}
                </h3>
              </div>

              {/* Last 5 games */}
              <div
                style={{
                  marginTop: "1rem",
                  backgroundColor: "#1E2635",
                  padding: "0.7rem",
                  borderRadius: "0.6rem",
                  display: "flex",
                  justifyContent: "center",
                  gap: "0.4rem",
                }}
              >
                {teamForm[team].map((res, i) => (
                  <span
                    key={i}
                    style={{
                      backgroundColor:
                        res === "W"
                          ? "#22c55e"
                          : res === "L"
                          ? "#ef4444"
                          : "#eab308",
                      color: "#0D1117",
                      fontWeight: 700,
                      padding: "0.4rem 0.7rem",
                      borderRadius: "0.4rem",
                    }}
                  >
                    {res}
                  </span>
                ))}
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* ===== ROW 2: MATCH PREDICTIONS ===== */}
      <div
        style={{
          backgroundColor: "#111827",
          borderRadius: "1rem",
          padding: "2rem",
          border: "1px solid #1F2937",
        }}
      >
        <h2 style={{ color: "#FFFFFF", fontSize: "1.5rem", marginBottom: "0.3rem" }}>
          Match Predictions
        </h2>
        <p style={{ color: "#9CA3AF", fontSize: "0.9rem", marginBottom: "1.5rem" }}>
          Predicted outcome probabilities (static for now)
        </p>

        <div style={{ marginBottom: "1.2rem" }}>
          <h3 style={{ color: "#E5E7EB", marginBottom: "0.8rem" }}>
            {teamA} vs {teamB}
          </h3>

          {[
            { label: `${teamA} Win`, color: "#22c55e", value: 55 },
            { label: "Draw", color: "#eab308", value: 25 },
            { label: `${teamB} Win`, color: "#ef4444", value: 20 },
          ].map((bar, i) => (
            <div key={i} style={{ marginBottom: "1rem" }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  fontSize: "0.95rem",
                  marginBottom: "0.4rem",
                  color: "#E5E7EB",
                }}
              >
                <span>{bar.label}</span>
                <span style={{ color: bar.color }}>{bar.value}%</span>
              </div>
              <div
                style={{
                  backgroundColor: "#1E2635",
                  borderRadius: "1rem",
                  height: "14px",
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${bar.value}%`,
                    height: "100%",
                    backgroundColor: bar.color,
                    borderRadius: "1rem",
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
