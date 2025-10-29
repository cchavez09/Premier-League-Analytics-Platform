const express = require('express');
const router = express.Router();
const pool = require('../database');

router.get("/:team/seasons", async (req, res) => {
  const { team } = req.params;
  try {
    const result = await pool.query(
      `SELECT DISTINCT Season
       FROM StandardizedMatches
       WHERE HomeTeam = $1 OR AwayTeam = $1
       ORDER BY Season DESC`,
      [team]
    );
    // Convert "EPLS200506" → "2005-2006"
    const formatted = result.rows.map(r => {
      const digits = r.season.match(/\d+/)?.[0] || "";
      const start = "20" + digits.slice(0, 2);
      const end = "20" + digits.slice(2, 4);
      return { season: `${start}-${end}`, code: r.season };
    });
    
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    console.error("❌ SQL Error:", err);
  }
});

router.get("/:team/seasons/:season/matches", async (req, res) => {
  const { team, season } = req.params;
  try {
    // Normalize: remove non-digits from season (e.g., "2021-2022" → "202122")
    const seasonDigits = season.replace(/\D/g, "").slice(0, 6); 

    // SQL Query to fetch matches and avoid repetitions
    const query = `
      SELECT DISTINCT
        date AS "date",
        hometeam AS "home_team",
        awayteam AS "away_team",
        fthg AS "fthg",
        ftag AS "ftag",
        ftr AS "ftr",
        season AS "season"
      FROM standardizedmatches
      WHERE (hometeam ILIKE $1 OR awayteam ILIKE $1)
      AND season ILIKE $2
      ORDER BY date ASC;
    `;

    const values = [`%${team}%`, `%${seasonDigits}%`];
    const result = await pool.query(query, values);

    console.log("📊 SQL:", query, values);
    console.log(`✅ Rows found: ${result.rows.length}`);
    if (result.rows.length > 0) console.log("🎯 Example row:", result.rows[0]);

    res.json(result.rows);
  } catch (err) {
    console.error("❌ SQL Error:", err.message);
    res.status(500).json({ error: "Internal Server Error" });
  }
});

module.exports = router;
