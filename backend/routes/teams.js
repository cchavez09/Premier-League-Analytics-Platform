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
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    console.error("❌ SQL Error:", err);
  }
});

module.exports = router;
