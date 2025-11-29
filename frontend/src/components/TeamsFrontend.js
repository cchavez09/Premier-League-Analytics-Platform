import React, { useState, useEffect } from "react";

// frontend deployment with backend for transition to cloud
const API_BASE_URL = import.meta.env.VITE_API_URL;

const Teams = () => {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/teams`) // 👈 connects to your backend
      .then((res) => res.json())
      .then((data) => setTeams(data))
      .catch((err) => console.error("Error fetching teams:", err));
  }, []);

  return (
    <div>
      <h2>Teams</h2>
      <ul>
        {teams.map((team, index) => (
          <li key={index}>{team.hometeam}</li>
        ))}
      </ul>
    </div>
  );
};

export default Teams;