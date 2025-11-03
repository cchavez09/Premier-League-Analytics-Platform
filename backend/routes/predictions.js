const express = require('express');
const router = express.Router();
const { spawn } = require('child_process');
const path = require('path');
const pool = require('../database');

// Get all seasons
router.get('/seasons', async (req, res) => {
  try {
    const result = await pool.query(`
      SELECT DISTINCT id, code, start_year
      FROM Seasons
      ORDER BY start_year DESC
    `);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching seasons:', error);
    res.status(500).json({ error: 'Failed to fetch seasons' });
  }
});

// Get teams for a specific season
router.get('/seasons/:seasonId/teams', async (req, res) => {
  try {
    const { seasonId } = req.params;
    const result = await pool.query(`
      SELECT DISTINCT t.id, t.name
      FROM Teams t
      WHERE EXISTS (
        SELECT 1 FROM StandardizedMatches sm
        WHERE sm.SeasonId = $1
        AND (sm.HomeTeamId = t.id OR sm.AwayTeamId = t.id)
      )
      ORDER BY t.name
    `, [seasonId]);
    res.json(result.rows);
  } catch (error) {
    console.error('Error fetching teams:', error);
    res.status(500).json({ error: 'Failed to fetch teams' });
  }
});

// Predict match outcome
router.post('/predict', async (req, res) => {
  try {
    const { homeTeam, awayTeam, homeSeasonCode, awaySeasonCode } = req.body;

    // Path to Python script
    const pythonScript = path.join(__dirname, '../MLModelTraining/predict_matches.py');

    // Spawn Python process
    const python = spawn('python3', [
      pythonScript,
      homeTeam,
      awayTeam,
      homeSeasonCode,
      awaySeasonCode
    ]);

    let dataString = '';
    let errorString = '';

    python.stdout.on('data', (data) => {
      dataString += data.toString();
    });

    python.stderr.on('data', (data) => {
      errorString += data.toString();
    });

    python.on('close', (code) => {
      if (code !== 0) {
        console.error('Python error:', errorString);
        return res.status(500).json({ error: 'Prediction failed', details: errorString });
      }

      try {
        // Parse the JSON output from Python
        const result = JSON.parse(dataString);
        res.json(result);
      } catch (parseError) {
        console.error('Parse error:', parseError, 'Data:', dataString);
        res.status(500).json({ error: 'Failed to parse prediction result' });
      }
    });

  } catch (error) {
    console.error('Prediction error:', error);
    res.status(500).json({ error: error.message });
  }
});

module.exports = router;