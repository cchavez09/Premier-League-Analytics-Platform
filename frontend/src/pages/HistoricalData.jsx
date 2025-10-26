import React, { useState } from "react";

export default function HistoricalData() {
  const [selectedTeam, setSelectedTeam] = useState(null);

  // === List of 44 Premier League teams (with stadiums for demo) ===
  const teams = [
    { name: "Arsenal", stadium: "Emirates Stadium, London" },
    { name: "Aston Villa", stadium: "Villa Park, Birmingham" },
    { name: "Bournemouth", stadium: "Vitality Stadium, Bournemouth" },
    { name: "Brentford", stadium: "Gtech Community Stadium, London" },
    { name: "Brighton", stadium: "Amex Stadium, Brighton" },
    { name: "Burnley", stadium: "Turf Moor, Burnley" },
    { name: "Chelsea", stadium: "Stamford Bridge, London" },
    { name: "Crystal Palace", stadium: "Selhurst Park, London" },
    { name: "Everton", stadium: "Goodison Park, Liverpool" },
    { name: "Fulham", stadium: "Craven Cottage, London" },
    { name: "Ipswich Town", stadium: "Portman Road, Ipswich" },
    { name: "Leeds United", stadium: "Elland Road, Leeds" },
    { name: "Leicester City", stadium: "King Power Stadium, Leicester" },
    { name: "Liverpool", stadium: "Anfield, Liverpool" },
    { name: "Luton Town", stadium: "Kenilworth Road, Luton" },
    { name: "Manchester City", stadium: "Etihad Stadium, Manchester" },
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
    { name: "Coventry City", stadium: "Coventry Building Society Arena" },
    { name: "Hull City", stadium: "MKM Stadium, Hull" },
    { name: "Derby County", stadium: "Pride Park, Derby" },
    { name: "Charlton Athletic", stadium: "The Valley, London" },
    { name: "Blackburn Rovers", stadium: "Ewood Park, Blackburn" },
    { name: "Bolton Wanderers", stadium: "University of Bolton Stadium" },
    { name: "Cardiff City", stadium: "Cardiff City Stadium, Cardiff" },
    { name: "Huddersfield Town", stadium: "John Smith’s Stadium, Huddersfield" },
    { name: "Blackpool", stadium: "Bloomfield Road, Blackpool" },
  ];

  const handleSelect = (team) => setSelectedTeam(team);
  const handleReset = () => setSelectedTeam(null);

  return (
    <div
      style={{
        backgroundColor: "#0D1117",
        color: "#E5E7EB",
        minHeight: "100vh",
        marginLeft: "250px",
        padding: "2rem 3rem",
        fontFamily: "'Inter', sans-serif",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Header */}
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <h1 style={{ margin: 0 }}>Historical Team Data</h1>
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

      {/* === Grid View === */}
      {!selectedTeam ? (
        <div
          style={{
            marginTop: "2rem",
            display: "grid",
            gridTemplateColumns: "repeat(4, 1fr)", // ✅ 4 cards per row
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
              onMouseEnter={(e) =>
                (e.currentTarget.style.backgroundColor = "#1F2937")
              }
              onMouseLeave={(e) =>
                (e.currentTarget.style.backgroundColor = "#111827")
              }
            >
              {/* Placeholder logo circle */}
              <div
                style={{
                  width: "45px",
                  height: "45px",
                  margin: "0 auto 0.8rem",
                  borderRadius: "50%",
                  backgroundColor: "#00FF87",
                  opacity: 0.9,
                }}
              ></div>

              {/* Team title */}
              <h3 style={{ margin: "0.2rem 0", fontSize: "1.05rem" }}>
                {team.name}
              </h3>

              {/* Description */}
              <p
                style={{
                  fontSize: "0.85rem",
                  color: "#9CA3AF",
                  margin: "0.5rem 0 0 0",
                  backgroundColor: "#0F172A",
                  borderRadius: "8px",
                  padding: "0.5rem",
                  lineHeight: "1.3",
                }}
              >
                {team.stadium}
              </p>
            </div>
          ))}
        </div>
      ) : (
        // === Selected team view ===
        <div
          style={{
            display: "flex",
            justifyContent: "center",
            alignItems: "center",
            marginTop: "4rem",
          }}
        >
          <div
            style={{
              backgroundColor: "#111827",
              padding: "2rem 3rem",
              borderRadius: "16px",
              textAlign: "center",
              boxShadow: "0 0 20px rgba(0, 255, 135, 0.3)",
              transform: "scale(1.05)",
              transition: "transform 0.4s ease",
              maxWidth: "600px",
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
            <h2 style={{ marginBottom: "0.5rem" }}>{selectedTeam.name}</h2>
            <p style={{ color: "#9CA3AF" }}>{selectedTeam.stadium}</p>
            <p style={{ color: "#D1D5DB", marginTop: "1rem" }}>
              Detailed season-by-season analytics for{" "}
              <strong>{selectedTeam.name}</strong> will appear here.
            </p>
          </div>
        </div>
      )}
    </div>
  );
}
