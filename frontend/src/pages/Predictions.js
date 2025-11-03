import React, { useState, useEffect } from "react";

export default function Predictions() {
  const [seasons, setSeasons] = useState([]);
  const [homeSeasonId, setHomeSeasonId] = useState("");
  const [awaySeasonId, setAwaySeasonId] = useState("");
  const [homeSeasonCode, setHomeSeasonCode] = useState("");
  const [awaySeasonCode, setAwaySeasonCode] = useState("");
  const [homeTeams, setHomeTeams] = useState([]);
  const [awayTeams, setAwayTeams] = useState([]);
  const [homeTeam, setHomeTeam] = useState("");
  const [awayTeam, setAwayTeam] = useState("");
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  // Fetch all seasons on mount
  useEffect(() => {
    async function fetchSeasons() {
      try {
        const response = await fetch('http://localhost:5001/api/predictions/seasons');
        const data = await response.json();
        setSeasons(data);
      } catch (err) {
        console.error('Error fetching seasons:', err);
        setError('Failed to load seasons');
      }
    }
    fetchSeasons();
  }, []);

  // Fetch home teams when home season changes
  useEffect(() => {
    if (homeSeasonId) {
      async function fetchHomeTeams() {
        try {
          const response = await fetch(
            `http://localhost:5001/api/predictions/seasons/${homeSeasonId}/teams`
          );
          const data = await response.json();
          setHomeTeams(data);
          setHomeTeam("");
        } catch (err) {
          console.error('Error fetching home teams:', err);
        }
      }
      fetchHomeTeams();
    }
  }, [homeSeasonId]);

  // Fetch away teams when away season changes
  useEffect(() => {
    if (awaySeasonId) {
      async function fetchAwayTeams() {
        try {
          const response = await fetch(
            `http://localhost:5001/api/predictions/seasons/${awaySeasonId}/teams`
          );
          const data = await response.json();
          setAwayTeams(data);
          setAwayTeam("");
        } catch (err) {
          console.error('Error fetching away teams:', err);
        }
      }
      fetchAwayTeams();
    }
  }, [awaySeasonId]);

  const handlePredict = async () => {
    if (!homeTeam || !awayTeam || !homeSeasonCode || !awaySeasonCode) {
      setError("Please select both teams and seasons");
      return;
    }

    setLoading(true);
    setError(null);
    setPrediction(null);

    try {
      const response = await fetch('http://localhost:5001/api/predictions/predict', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          homeTeam,
          awayTeam,
          homeSeasonCode,
          awaySeasonCode,
        }),
      });

      const data = await response.json();

      if (response.ok) {
        setPrediction(data);
      } else {
        setError(data.error || 'Prediction failed');
      }
    } catch (err) {
      console.error('Error predicting match:', err);
      setError('Failed to get prediction');
    } finally {
      setLoading(false);
    }
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
      <div style={{ marginBottom: "2rem" }}>
        <h1
          style={{
            fontSize: "2rem",
            fontWeight: "700",
            color: "#00FF87",
            marginBottom: "0.3rem",
          }}
        >
          Match Predictions
        </h1>
        <p style={{ color: "#9CA3AF", fontSize: "0.95rem" }}>
          Compare teams across different seasons using ML predictions
        </p>
      </div>

      {/* Selection Panel */}
      <div
        style={{
          backgroundColor: "#111827",
          borderRadius: "1rem",
          padding: "2rem",
          border: "1px solid #1F2937",
          marginBottom: "2rem",
        }}
      >
        <div
          style={{
            display: "grid",
            gridTemplateColumns: "1fr 1fr",
            gap: "2rem",
          }}
        >
          {/* Home Team Selection */}
          <div>
            <h3 style={{ color: "#FFFFFF", marginBottom: "1rem" }}>Home Team</h3>

            <label style={{ display: "block", color: "#9CA3AF", marginBottom: "0.5rem" }}>
              Season:
            </label>
            <select
              value={homeSeasonId}
              onChange={(e) => {
                const selectedSeason = seasons.find(s => s.id === parseInt(e.target.value));
                setHomeSeasonId(e.target.value);
                setHomeSeasonCode(selectedSeason?.code || "");
              }}
              style={{
                width: "100%",
                padding: "0.75rem",
                backgroundColor: "#0F1623",
                color: "#E5E7EB",
                border: "1px solid #1F2937",
                borderRadius: "0.5rem",
                marginBottom: "1rem",
                cursor: "pointer",
              }}
            >
              <option value="">Select Season</option>
              {seasons.map((season) => (
                <option key={season.id} value={season.id}>
                  {season.code}
                </option>
              ))}
            </select>

            <label style={{ display: "block", color: "#9CA3AF", marginBottom: "0.5rem" }}>
              Team:
            </label>
            <select
              value={homeTeam}
              onChange={(e) => setHomeTeam(e.target.value)}
              disabled={!homeSeasonId}
              style={{
                width: "100%",
                padding: "0.75rem",
                backgroundColor: "#0F1623",
                color: "#E5E7EB",
                border: "1px solid #1F2937",
                borderRadius: "0.5rem",
                cursor: homeSeasonId ? "pointer" : "not-allowed",
              }}
            >
              <option value="">Select Team</option>
              {homeTeams.map((team) => (
                <option key={team.id} value={team.name}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>

          {/* Away Team Selection */}
          <div>
            <h3 style={{ color: "#FFFFFF", marginBottom: "1rem" }}>Away Team</h3>

            <label style={{ display: "block", color: "#9CA3AF", marginBottom: "0.5rem" }}>
              Season:
            </label>
            <select
              value={awaySeasonId}
              onChange={(e) => {
                const selectedSeason = seasons.find(s => s.id === parseInt(e.target.value));
                setAwaySeasonId(e.target.value);
                setAwaySeasonCode(selectedSeason?.code || "");
              }}
              style={{
                width: "100%",
                padding: "0.75rem",
                backgroundColor: "#0F1623",
                color: "#E5E7EB",
                border: "1px solid #1F2937",
                borderRadius: "0.5rem",
                marginBottom: "1rem",
                cursor: "pointer",
              }}
            >
              <option value="">Select Season</option>
              {seasons.map((season) => (
                <option key={season.id} value={season.id}>
                  {season.code}
                </option>
              ))}
            </select>

            <label style={{ display: "block", color: "#9CA3AF", marginBottom: "0.5rem" }}>
              Team:
            </label>
            <select
              value={awayTeam}
              onChange={(e) => setAwayTeam(e.target.value)}
              disabled={!awaySeasonId}
              style={{
                width: "100%",
                padding: "0.75rem",
                backgroundColor: "#0F1623",
                color: "#E5E7EB",
                border: "1px solid #1F2937",
                borderRadius: "0.5rem",
                cursor: awaySeasonId ? "pointer" : "not-allowed",
              }}
            >
              <option value="">Select Team</option>
              {awayTeams.map((team) => (
                <option key={team.id} value={team.name}>
                  {team.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        <button
          onClick={handlePredict}
          disabled={loading || !homeTeam || !awayTeam}
          style={{
            marginTop: "1.5rem",
            width: "100%",
            padding: "0.75rem",
            backgroundColor: loading || !homeTeam || !awayTeam ? "#374151" : "#00FF87",
            color: "#0D1117",
            border: "none",
            borderRadius: "0.5rem",
            fontWeight: "600",
            fontSize: "1rem",
            cursor: loading || !homeTeam || !awayTeam ? "not-allowed" : "pointer",
            transition: "background-color 0.3s",
          }}
          onMouseEnter={(e) => {
            if (!loading && homeTeam && awayTeam) {
              e.target.style.backgroundColor = "#00cc6f";
            }
          }}
          onMouseLeave={(e) => {
            if (!loading && homeTeam && awayTeam) {
              e.target.style.backgroundColor = "#00FF87";
            }
          }}
        >
          {loading ? "Predicting..." : "Predict Match"}
        </button>

        {error && (
          <p style={{ color: "#FF4D4D", marginTop: "1rem", textAlign: "center" }}>
            {error}
          </p>
        )}
      </div>

      {/* Prediction Results */}
      {prediction && (
        <div
          style={{
            backgroundColor: "#111827",
            borderRadius: "1rem",
            padding: "2rem",
            border: "1px solid #1F2937",
          }}
        >
          <h2 style={{ color: "#FFFFFF", fontSize: "1.5rem", marginBottom: "1rem" }}>
            Prediction Results
          </h2>

          <h3 style={{ color: "#E5E7EB", marginBottom: "1.5rem", textAlign: "center" }}>
            {prediction.home_team} ({prediction.home_season}) vs{" "}
            {prediction.away_team} ({prediction.away_season})
          </h3>

          {[
            {
              label: `${prediction.home_team} Win`,
              color: "#22c55e",
              value: (prediction.probabilities.home_win * 100).toFixed(1),
            },
            {
              label: "Draw",
              color: "#eab308",
              value: (prediction.probabilities.draw * 100).toFixed(1),
            },
            {
              label: `${prediction.away_team} Win`,
              color: "#ef4444",
              value: (prediction.probabilities.away_win * 100).toFixed(1),
            },
          ].map((bar, i) => (
            <div key={i} style={{ marginBottom: "1.5rem" }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  fontSize: "1rem",
                  marginBottom: "0.5rem",
                  color: "#E5E7EB",
                }}
              >
                <span>{bar.label}</span>
                <span style={{ color: bar.color, fontWeight: "600" }}>
                  {bar.value}%
                </span>
              </div>
              <div
                style={{
                  backgroundColor: "#1E2635",
                  borderRadius: "1rem",
                  height: "16px",
                  overflow: "hidden",
                }}
              >
                <div
                  style={{
                    width: `${bar.value}%`,
                    height: "100%",
                    backgroundColor: bar.color,
                    borderRadius: "1rem",
                    transition: "width 0.5s ease",
                  }}
                ></div>
              </div>
            </div>
          ))}

          <div
            style={{
              marginTop: "2rem",
              padding: "1rem",
              backgroundColor: "#0F1623",
              borderRadius: "0.75rem",
              textAlign: "center",
            }}
          >
            <p style={{ color: "#9CA3AF", margin: 0 }}>Predicted Outcome:</p>
            <p
              style={{
                fontSize: "1.5rem",
                fontWeight: "700",
                color: "#00FF87",
                margin: "0.5rem 0 0 0",
                textTransform: "uppercase",
              }}
            >
              {prediction.prediction.replace("_", " ")}
            </p>
          </div>
        </div>
      )}
    </div>
  );
}