const express = require('express');
const cors = require('cors');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5000;

app.use(cors());
app.use(express.json());

// Import routes
const teamRoutes = require('./routes/teams');
const playerRoutes = require('./routes/players');
const fixtureRoutes = require('./routes/fixtures');

// Use routes
app.use('/api/teams', teamRoutes);
app.use('/api/players', playerRoutes);
app.use('/api/fixtures', fixtureRoutes);

app.get('/', (req, res) => {
  res.send('Soccer App Backend is running ⚽');
});

app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});
