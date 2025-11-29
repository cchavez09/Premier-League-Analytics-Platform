import React, { useState, useEffect } from "react";

export default function HistoricalData() {
  const [selectedTeam, setSelectedTeam] = useState(null);
  const [seasons, setSeasons] = useState([]);
  const [loadingSeasons, setLoadingSeasons] = useState(false);
  const [loadingMatches, setLoadingMatches] = useState(false);
  const [selectedSeason, setSelectedSeason] = useState("");
  const [matches, setMatches] = useState([]);

  // ===== Back to Top state =====
  const [showButton, setShowButton] = useState(false);

  // Show/hide Back to Top button on scroll
  useEffect(() => {
    const handleScroll = () => {
      setShowButton(window.scrollY > 300);
    };

    window.addEventListener("scroll", handleScroll);
    return () => window.removeEventListener("scroll", handleScroll);
  }, []);

  // === Premier League teams ===
  const teams = [
    { name: "Arsenal", stadium: "Emirates Stadium, London" },
    { name: "Aston Villa", stadium: "Villa Park, Birmingham" },
    { name: "Blackburn Rovers", stadium: "Ewood Park, Blackburn" },
    { name: "Blackpool", stadium: "Bloomfield Road, Blackpool" },
    { name: "Bolton Wanderers", stadium: "University of Bolton Stadium" },
    { name: "Bournemouth", stadium: "Vitality Stadium, Bournemouth" },
    { name: "Brentford", stadium: "Gtech Community Stadium, London" },
    { name: "Brighton", stadium: "Amex Stadium, Brighton" },
    { name: "Burnley", stadium: "Turf Moor, Burnley" },
    { name: "Cardiff City", stadium: "Cardiff City Stadium, Cardiff" },
    { name: "Charlton Athletic", stadium: "The Valley, London" },
    { name: "Chelsea", stadium: "Stamford Bridge, London" },
    { name: "Coventry City", stadium: "Coventry Building Society Arena" },
    { name: "Crystal Palace", stadium: "Selhurst Park, London" },
    { name: "Derby County", stadium: "Pride Park, Derby" },
    { name: "Everton", stadium: "Goodison Park, Liverpool" },
    { name: "Fulham", stadium: "Craven Cottage, London" },
    { name: "Huddersfield Town", stadium: "John Smith’s Stadium, Huddersfield" },
    { name: "Hull City", stadium: "MKM Stadium, Hull" },
    { name: "Ipswich Town", stadium: "Portman Road, Ipswich" },
    { name: "Leeds United", stadium: "Elland Road, Leeds" },
    { name: "Leicester City", stadium: "King Power Stadium, Leicester" },
    { name: "Liverpool", stadium: "Anfield, Liverpool" },
    { name: "Luton Town", stadium: "Kenilworth Road, Luton" },
    { name: "Man City", stadium: "Etihad Stadium, Manchester" },
    { name: "Manchester United", stadium: "Old Trafford, Manchester" },
    { name: "Middlesbrough", stadium: "Riverside Stadium, Middlesbrough" },
    { name: "Newcastle United", stadium: "St James’ Park, Newcastle" },
    { name: "Norwich City", stadium: "Carrow Road, Norwich" },
    { name: "Nottingham Forest", stadium: "City Ground, Nottingham" },
    { name: "Portsmouth", stadium: "Fratton Park, Portsmouth" },
    { name: "Queens Park Rangers", stadium: "Loftus Road, London" },
    { name: "Reading", stadium: "Select Car Leasing Stadium, Reading" },
    { name: "Sheffield United", stadium: "Bramall Lane, Sheffield" },
    { name: "Sheffield Wednesday", stadium: "Hillsborough, Sheffield" },
    { name: "Southampton", stadium: "St Mary’s Stadium, Southampton" },
    { name: "Stoke City", stadium: "bet365 Stadium, Stoke-on-Trent" },
    { name: "Sunderland", stadium: "Stadium of Light, Sunderland" },
    { name: "Swansea City", stadium: "Liberty Stadium, Swansea" },
    { name: "Tottenham Hotspur", stadium: "Tottenham Hotspur Stadium, London" },
    { name: "Watford", stadium: "Vicarage Road, Watford" },
    { name: "West Bromwich Albion", stadium: "The Hawthorns, West Bromwich" },
    { name: "West Ham United", stadium: "London Stadium, London" },
    { name: "Wigan Athletic", stadium: "DW Stadium, Wigan" },
    { name: "Wolverhampton Wanderers", stadium: "Molineux Stadium, Wolverhampton" },
  ].sort((a, b) => a.name.localeCompare(b.name));

  const BACKEND_URL = process.env.REACT_APP_API_URL;

  // === Select Team ===
  const handleSelect = async (team) => {
    setSelectedTeam(team);
    setSelectedSeason("");
    setMatches([]);
    setLoadingSeasons(true);

    try {
      const response = await fetch(`${BACKEND_URL}/${team.name}/seasons`);
      const data = await response.json();
      setSeasons(data);
    } catch (err) {
      console.error("Error:", err);
    }

    setLoadingSeasons(false);
  };

  // === Select Season ===
  const handleSeasonSelect = async (value) => {
    if (!value) return;
    const [id, code] = value.split("|");

    setSelectedSeason(code);
    setMatches([]);
    setLoadingMatches(true);

    try {
      const response = await fetch(
        `${BACKEND_URL}/api/teams/${selectedTeam.name}/seasons/${id}/matches`
      );
      const data = await response.json();
      setMatches(data);
    } catch (err) {
      console.error("Error:", err);
    }

    setLoadingMatches(false);
  };

  // === Reset ===
  const handleReset = () => {
    setSelectedTeam(null);
    setSeasons([]);
    setSelectedSeason("");
    setMatches([]);
  };

  return (
    <div
      style={{
        backgroundColor: "#0D1117",
        color: "#E5E7EB",
        minHeight: "100vh",
        padding: "2rem",
        fontFamily: "'Inter', sans-serif",
      }}
    >
      {/* HEADER */}
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
        <h1 style={{ margin: 0, color: "#00FF87" }}>Historical Team Data</h1>

        {selectedTeam && (
          <button
            onClick={handleReset}
            style={{
              backgroundColor: "#00FF87",
              color: "#0D1117",
              border: "none",
              padding: "0.5rem 1rem",
              borderRadius: "8px",
              fontWeight: "600",
              cursor: "pointer",
              transition: "background-color 0.3s",
            }}
            onMouseEnter={(e) => (e.target.style.backgroundColor = "#00cc6f")}
            onMouseLeave={(e) => (e.target.style.backgroundColor = "#00FF87")}
          >
            Select Another Team
          </button>
        )}
      </div>

      {/* GRID VIEW */}
      {!selectedTeam ? (
        <div
          style={{
            marginTop: "2rem",
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)",
            gap: "1.5rem",
          }}
        >
          {teams.map((team) => (
            <div
              key={team.name}
              onClick={() => handleSelect(team)}
              style={{
                backgroundColor: "#111827",
                padding: "1.5rem",
                borderRadius: "12px",
                textAlign: "center",
                cursor: "pointer",
                transition: "transform 0.3s, background-color 0.3s",
              }}
              onMouseEnter={(e) => (e.currentTarget.style.backgroundColor = "#1F2937")}
              onMouseLeave={(e) => (e.currentTarget.style.backgroundColor = "#111827")}
            >
              <div
                style={{
                  width: "45px",
                  height: "45px",
                  margin: "0 auto 0.8rem",
                  borderRadius: "50%",
                  backgroundColor: "#00FF87",
                }}
              ></div>
              <h3 style={{ margin: "0.2rem 0", fontSize: "1.05rem" }}>{team.name}</h3>
              <p
                style={{
                  fontSize: "0.85rem",
                  color: "#9CA3AF",
                  margin: "0.5rem 0 0",
                  backgroundColor: "#0F172A",
                  borderRadius: "8px",
                  padding: "0.5rem",
                }}
              >
                {team.stadium}
              </p>
            </div>
          ))}
        </div>
      ) : (
        // SELECTED TEAM VIEW
        <div style={{ display: "flex", justifyContent: "center", marginTop: "4rem" }}>
          <div
            style={{
              backgroundColor: "#111827",
              padding: "2rem 3rem",
              borderRadius: "16px",
              textAlign: "center",
              boxShadow: "0 0 20px rgba(0, 255, 135, 0.3)",
              maxWidth: "600px",
              width: "100%",
            }}
          >
            <div
              style={{
                width: "60px",
                height: "60px",
                borderRadius: "50%",
                backgroundColor: "#00FF87",
                margin: "0 auto 1rem",
              }}
            ></div>
            <h2>{selectedTeam.name}</h2>
            <p style={{ color: "#9CA3AF" }}>{selectedTeam.stadium}</p>

            {loadingSeasons ? (
              <p>Loading seasons...</p>
            ) : seasons.length > 0 ? (
              <div style={{ marginTop: "1.5rem" }}>
                <label style={{ color: "#D1D5DB" }}>Select a Premier League season:</label>
                <br />
                <select
                  value={selectedSeason}
                  onChange={(e) => handleSeasonSelect(e.target.value)}
                  style={{
                    marginTop: "0.5rem",
                    padding: "0.5rem",
                    borderRadius: "8px",
                    backgroundColor: "#0F172A",
                    color: "#E5E7EB",
                    border: "none",
                  }}
                >
                  <option value="">-- Select --</option>
                  {seasons.map((s) => (
                    <option key={s.id} value={`${s.id}|${s.code}`}>
                      {s.code}
                    </option>
                  ))}
                </select>
              </div>
            ) : (
              <p>No Premier League seasons found.</p>
            )}

            {loadingMatches && <p>Loading matches...</p>}

            {selectedSeason && matches.length > 0 && !loadingMatches && (
              <div style={{ marginTop: "2rem", textAlign: "left" }}>
                <h3 style={{ textAlign: "center", color: "#00FF87" }}>
                  {selectedTeam.name} – {selectedSeason} Matches
                </h3>

                <table style={{ width: "100%", marginTop: "1rem", borderCollapse: "collapse" }}>
                  <thead>
                    <tr style={{ backgroundColor: "#1F2937" }}>
                      <th style={{ padding: "0.75rem" }}>Date</th>
                      <th style={{ padding: "0.75rem" }}>Home</th>
                      <th style={{ padding: "0.75rem" }}>Away</th>
                      <th style={{ padding: "0.75rem" }}>Score</th>
                      <th style={{ padding: "0.75rem" }}>Result</th>
                    </tr>
                  </thead>
                  <tbody>
                    {matches.map((m, idx) => {
                      const isHome = m.home_team === selectedTeam.name;
                      let resultLabel =
                        m.ftr === "D"
                          ? "Draw"
                          : (m.ftr === "H" && isHome) || (m.ftr === "A" && !isHome)
                          ? "Win"
                          : "Loss";

                      return (
                        <tr
                          key={idx}
                          style={{
                            backgroundColor: idx % 2 === 0 ? "#0F172A" : "#111827",
                          }}
                        >
                          <td style={{ padding: "0.75rem" }}>
                            {new Date(m.date).toLocaleDateString("en-GB", {
                              day: "2-digit",
                              month: "short",
                              year: "numeric",
                            })}
                          </td>
                          <td style={{ padding: "0.75rem", color: isHome ? "#00FF87" : "#E5E7EB" }}>
                            {m.home_team}
                          </td>
                          <td style={{ padding: "0.75rem", color: !isHome ? "#00FF87" : "#E5E7EB" }}>
                            {m.away_team}
                          </td>
                          <td style={{ padding: "0.75rem" }}>
                            {m.fthg ?? 0} - {m.ftag ?? 0}
                          </td>
                          <td
                            style={{
                              padding: "0.75rem",
                              color:
                                resultLabel === "Win"
                                  ? "#00FF87"
                                  : resultLabel === "Loss"
                                  ? "#FF4D4D"
                                  : "#E5E7EB",
                            }}
                          >
                            {resultLabel}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}

            {selectedSeason && matches.length === 0 && !loadingMatches && (
              <p>No match data found for this season.</p>
            )}
          </div>
        </div>
      )}

      {/* ===== BACK TO TOP BUTTON ===== */}
      {showButton && (
        <button
          onClick={() => window.scrollTo({ top: 0, behavior: "smooth" })}
          style={{
            position: "fixed",
            bottom: "30px",
            right: "30px",
            width: "50px",
            height: "50px",
            borderRadius: "50%",
            backgroundColor: "#00FF87",
            color: "#0D1117",
            border: "none",
            cursor: "pointer",
            fontSize: "1.3rem",
            fontWeight: "bold",
            boxShadow: "0 0 12px rgba(0,255,135,0.6)",
            transition: "transform 0.25s ease, box-shadow 0.25s ease",
          }}
          onMouseEnter={(e) => {
            e.currentTarget.style.transform = "scale(1.2)";
            e.currentTarget.style.boxShadow = "0 0 16px rgba(0,255,135,0.9)";
          }}
          onMouseLeave={(e) => {
            e.currentTarget.style.transform = "scale(1)";
            e.currentTarget.style.boxShadow = "0 0 12px rgba(0,255,135,0.6)";
          }}
        >
          ⮝
        </button>
      )}
    </div>
  );
}
