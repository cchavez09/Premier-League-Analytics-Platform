const { Pool } = require("pg");
require("dotenv").config({ path: "./pginfo.env" });

// Pool connection to Neon Cloud Database
const pool = new Pool({
  connectionString: process.env.DATABASE_URL,
  ssl: { rejectUnauthorized: false }
});

module.exports = pool;
