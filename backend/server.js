const express = require('express');
const cors = require('cors');
require('dotenv').config({ path: './pginfo.env' });

console.log('🚀 Starting server...');
console.log('📝 Environment:', {
  DB_USER: process.env.DB_USER,
  DB_HOST: process.env.DB_HOST,
  DB_NAME: process.env.DB_NAME,
  DB_PORT: process.env.DB_PORT,
  PORT: process.env.PORT
});

const app = express();
app.use(cors());
app.use(express.json());

const pool = require('./database');

// Make this synchronous to prevent early exit
async function startServer() {
  try {
    console.log('🔌 Testing database connection...');
    await pool.query('SELECT NOW()');
    console.log('✅ Database connected successfully');

    // Import routes
    console.log('📦 Loading routes...');
    const teamRoutes = require('./routes/teams');
    const fixtureRoutes = require('./routes/fixtures');
    const predictionsRoutes = require('./routes/predictions');

    app.use('/api/teams', teamRoutes);
    app.use('/api/fixtures', fixtureRoutes);
    app.use('/api/predictions', predictionsRoutes);
    console.log('✅ Routes loaded');

    // Test endpoint
    app.get('/api/test-db', async (req, res) => {
      try {
        const tables = await pool.query(`
          SELECT table_name
          FROM information_schema.tables
          WHERE table_schema = 'public'
        `);
        const teams = await pool.query('SELECT COUNT(*) as count FROM "Teams"');
        const matches = await pool.query('SELECT COUNT(*) as count FROM "StandardizedMatches"');
        const seasons = await pool.query('SELECT COUNT(*) as count FROM "Seasons"');

        res.json({
          tables: tables.rows.map(r => r.table_name),
          counts: {
            teams: teams.rows[0].count,
            matches: matches.rows[0].count,
            seasons: seasons.rows[0].count
          }
        });
      } catch (error) {
        console.error('❌ Test DB error:', error);
        res.status(500).json({ error: error.message });
      }
    });

    app.get('/', (req, res) => {
      res.send('Soccer App Backend is running ⚽');
    });

    // Error handler
    app.use((err, req, res, next) => {
      console.error('❌ Error:', err);
      res.status(500).json({ error: err.message });
    });

    const PORT = process.env.PORT || 5001;
    const server = app.listen(PORT, () => {
      console.log(`✅ Server running on http://localhost:${PORT}`);
      console.log('🎯 Endpoints available:');
      console.log(`   GET  http://localhost:${PORT}/`);
      console.log(`   GET  http://localhost:${PORT}/api/test-db`);
    });

    // Prevent premature exit
    process.stdin.resume();

  } catch (error) {
    console.error('❌ Fatal error during startup:', error);
    process.exit(1);
  }
}

// Global error handlers
process.on('uncaughtException', (err) => {
  console.error('❌ Uncaught exception:', err);
});

process.on('unhandledRejection', (err) => {
  console.error('❌ Unhandled rejection:', err);
});

// Start the server
startServer().catch(err => {
  console.error('❌ Failed to start server:', err);
  process.exit(1);
});