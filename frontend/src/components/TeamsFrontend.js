import React, { useState, useEffect } from "react";

const Teams = () => {
  const [teams, setTeams] = useState([]);

  useEffect(() => {
    fetch("http://localhost:5000/api/teams") // 👈 connects to your backend
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