const express = require('express');
const router = express.Router();
const pool = require('../database');

// Example endpoint: get all teams
router.get('/', async (req, res) => {
  try {
    const result = await pool.query('SELECT DISTINCT hometeam FROM teammatches ORDER BY hometeam');
    res.json(result.rows);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server Error');
  }
});

module.exports = router;
