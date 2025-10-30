const express = require('express');
const router = express.Router();
const pool = require('../database');

router.get("/:team/seasons", async (req, res) => {
  const { team } = req.params;
  try {
    const query = `
      SELECT DISTINCT se.id, se.code
      FROM Seasons se
      JOIN StandardizedMatches sm ON sm.SeasonId = se.id
      WHERE sm.HomeTeam ILIKE $1 OR sm.AwayTeam ILIKE $1
      ORDER BY se.code DESC;
    `;

    const result = await pool.query(query, [`%${team}%`]);

    res.json(result.rows);
  } catch (err) {
    console.error("❌ /:team/seasons error:", err.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

router.get("/:team/seasons/:seasonId/matches", async (req, res) => {
  const { team, seasonId } = req.params;

  try {
    const query = `
      SELECT
        sm.Date AS date,
        sm.HomeTeam AS home_team,
        sm.AwayTeam AS away_team,
        sm.FTHG AS fthg,
        sm.FTAG AS ftag,
        sm.FTR AS ftr,
        se.code AS season
      FROM StandardizedMatches sm
      JOIN Seasons se ON sm.SeasonId = se.id
      WHERE (sm.HomeTeam ILIKE $1 OR sm.AwayTeam ILIKE $1)
      AND sm.SeasonId = $2
      ORDER BY sm.Date ASC;
    `;

    const values = [`%${team}%`, seasonId];

    const result = await pool.query(query, [team, seasonId]);

    res.json(result.rows);
  } catch (err) {
    console.error("❌ /matches error:", err.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

module.exports = router;
