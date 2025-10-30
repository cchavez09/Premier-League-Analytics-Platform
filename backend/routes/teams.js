const express = require("express");
const router = express.Router();
const pool = require("../database");

// ======================================================
//  GET SEASONS FOR A TEAM (Uses TeamId instead of name)
// ======================================================
router.get("/:team/seasons", async (req, res) => {
  const { team } = req.params;

  try {
    // 1) Get TeamId from Teams table
    const teamResult = await pool.query(
      `SELECT id FROM Teams WHERE name ILIKE $1 LIMIT 1`,
      [team]
    );

    if (teamResult.rowCount === 0) {
      return res.json([]); // team not found
    }

    const teamId = teamResult.rows[0].id;

    // 2) Get distinct seasons where this team played
    const seasonsQuery = `
      SELECT DISTINCT se.id, se.code, se.start_year
      FROM Seasons se
      JOIN StandardizedMatches sm ON sm.SeasonId = se.id
      WHERE sm.HomeTeamId = $1 OR sm.AwayTeamId = $1
      ORDER BY se.start_year DESC;
    `;

    const seasons = await pool.query(seasonsQuery, [teamId]);
    res.json(seasons.rows);

  } catch (err) {
    console.error("❌ /:team/seasons error:", err.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

// ======================================================
//  GET MATCHES FOR TEAM IN A SEASON (Uses TeamId & SeasonId)
// ======================================================
router.get("/:team/seasons/:seasonId/matches", async (req, res) => {
  const { team, seasonId } = req.params;

  try {
    // 1) Get TeamId from Teams table
    const teamResult = await pool.query(
      `SELECT id FROM Teams WHERE name ILIKE $1 LIMIT 1`,
      [team]
    );

    if (teamResult.rowCount === 0) {
      return res.json([]);
    }

    const teamId = teamResult.rows[0].id;

    // 2) Get matches using TeamId & SeasonId
    const matchQuery = `
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
      WHERE sm.SeasonId = $1
      AND (sm.HomeTeamId = $2 OR sm.AwayTeamId = $2)
      ORDER BY sm.Date ASC;
    `;

    const result = await pool.query(matchQuery, [seasonId, teamId]);
    res.json(result.rows);

  } catch (err) {
    console.error("❌ /matches error:", err.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

module.exports = router;
