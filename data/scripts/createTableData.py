import os
import pandas as pd
import psycopg2
import urllib.parse as up 
from dotenv import load_dotenv

print("CWD:", os.getcwd())
print("SCRIPT DIR:", os.path.dirname(os.path.abspath(__file__)))

# --- Locate pginfo.env relative to this script ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))          # .../data/scripts
ROOT_DIR = os.path.abspath(os.path.join(SCRIPT_DIR, "..", "..")) # .../project root
ENV_PATH = os.path.join(ROOT_DIR, "backend", "pginfo.env")       # .../backend/pginfo.env

print("🔍 Looking for pginfo.env at:", ENV_PATH)

# --- Load environment variables ---
load_dotenv(ENV_PATH)

DATABASE_URL = os.getenv("DATABASE_URL")

print("DATABASE_URL from env:", DATABASE_URL)

if not DATABASE_URL:
    raise ValueError("❌ DATABASE_URL not found in pginfo.env")

# --- Connect to Neon database ---
conn = psycopg2.connect(DATABASE_URL)
cur = conn.cursor()
cur.execute("SET datestyle TO 'DMY';")
print("✅ Connected to Neon")

# ==========================================================
# 🧹 RESET DATABASE STATE
# ==========================================================
print("🧹 Dropping old tables...")
cur.execute("DROP TABLE IF EXISTS StandardizedMatches CASCADE;")
cur.execute("DROP TABLE IF EXISTS TeamMatches CASCADE;")
cur.execute("DROP TABLE IF EXISTS Standings CASCADE;")
cur.execute("DROP TABLE IF EXISTS Seasons CASCADE;")
conn.commit()
print("✅ Tables dropped.")

# ==========================================================
# 🏗️ RECREATE TABLES CLEAN
# ==========================================================

# --- Create Seasons table ---
cur.execute("""
CREATE TABLE IF NOT EXISTS Seasons (
    id SERIAL PRIMARY KEY,
    code VARCHAR(20) UNIQUE,
    start_year INT,
    end_year INT,
    notes TEXT
);
""")

# --- Create StandardizedMatches (MatchID is the real primary key) ---
cur.execute("""
CREATE TABLE IF NOT EXISTS StandardizedMatches (
    MatchID BIGINT PRIMARY KEY,
    HomeTeamId BIGINT,
    AwayTeamId BIGINT,
    Date DATE,
    HomeTeam VARCHAR(100),
    AwayTeam VARCHAR(100),
    FTHG INT,
    FTAG INT,
    FTR VARCHAR(5),
    HTHG INT,
    HTAG INT,
    HTR VARCHAR(5),
    Referee VARCHAR(100),
    HS INT,
    AS_ INT,
    HST INT,
    AST INT,
    HF INT,
    AF INT,
    HC INT,
    AC INT,
    HY INT,
    AY INT,
    HR INT,
    AR INT,
    B365H FLOAT,
    B365D FLOAT,
    B365A FLOAT,
    Season VARCHAR(20),
    SeasonId INT REFERENCES Seasons(id)
);
""")

# Create Teams table if not exists
cur.execute("""
CREATE TABLE IF NOT EXISTS Teams (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) UNIQUE
);
""")

# --- Create TeamMatches (weak entity referencing StandardizedMatches) ---
cur.execute("""
CREATE TABLE IF NOT EXISTS TeamMatches (
    MatchID BIGINT PRIMARY KEY REFERENCES StandardizedMatches(MatchID),
    homeTeamID BIGINT,
    awayTeamID INT,
    Date DATE,
    HomeTeam VARCHAR(100),
    AwayTeam VARCHAR(100),
    FTHG INT,
    FTAG INT,
    FTR VARCHAR(5),
    HTHG INT,
    HTAG INT,
    HTR VARCHAR(5),
    Referee VARCHAR(100),
    HS INT,
    AS_ INT,
    HST INT,
    AST INT,
    HF INT,
    AF INT,
    HC INT,
    AC INT,
    HY INT,
    AY INT,
    HR INT,
    AR INT,
    B365H FLOAT,
    B365D FLOAT,
    B365A FLOAT,
    Season VARCHAR(20),
    SeasonId INT REFERENCES Seasons(id)
);
""")

# --- Create Standings (league table summary per season/team) ---
cur.execute("""
CREATE TABLE IF NOT EXISTS Standings (
    id SERIAL PRIMARY KEY,
    TeamId INT,
    Rank INT,
    Team VARCHAR(100),
    Season VARCHAR(20),
    MatchesPlayed INT,
    Wins INT,
    Draws INT,
    Losses INT,
    Points INT,
    GoalsScored INT,
    GoalsConceded INT,
    GoalDifference INT,
    TotalHS INT,
    PerGameHS FLOAT,
    TotalAS INT,
    PerGameAS FLOAT,
    TotalHST INT,
    PerGameHST FLOAT,
    TotalAST INT,
    PerGameAST FLOAT,
    TotalHC INT,
    PerGameHC FLOAT,
    TotalAC INT,
    PerGameAC FLOAT,
    TotalHF INT,
    PerGameHF FLOAT,
    TotalAF INT,
    PerGameAF FLOAT,
    TotalHY INT,
    PerGameHY FLOAT,
    TotalAY INT,
    PerGameAY FLOAT,
    TotalHR INT,
    PerGameHR FLOAT,
    TotalAR INT,
    PerGameAR FLOAT,
    SeasonId INT REFERENCES Seasons(id)
);
""")

conn.commit()

# ==========================================================
# 📁 Folder paths
# ==========================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "files")

TEAMFILES_DIR = os.path.join(DATA_DIR, "TeamFiles")
STANDINGS_DIR = os.path.join(DATA_DIR, "Standings")
STANDARDIZED_DIR = os.path.join(DATA_DIR, "StandardizedSeasonMatches")

# ==========================================================
# 🧽 Helpers
# ==========================================================

def drop_duplicate_columns_for_pg(df):
    seen = set()
    keep_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if col_lower not in seen:
            keep_cols.append(col)
            seen.add(col_lower)
    return df[keep_cols]

def load_folder_to_table(folder_path, table_name):
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    print(f"📂 Loading data from: {folder_path}")
    for file in os.listdir(folder_path):
        if not file.endswith(".csv"):
            continue

        print(f"→ Inserting: {file}")
        df = pd.read_csv(os.path.join(folder_path, file))

        df.rename(columns={"AS": "AS_"}, inplace=True)
        df = drop_duplicate_columns_for_pg(df)  
        # Remove duplicate match rows inside TeamMatches CSVs
        if table_name == "TeamMatches" and "MatchID" in df.columns:
            df = df.drop_duplicates(subset=["MatchID"])
        df = df.where(pd.notnull(df), None)

        cols = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({cols}) VALUES ({placeholders})"

        for idx, row in df.iterrows():
          try:
              cur.execute(sql, tuple(row))
          except Exception as e:
              # ✅ Skip duplicates automatically
              if "duplicate key value violates unique constraint" in str(e):
                  continue
              print(f"\n❌ ERROR in file: {file}")
              print(f"   → Row number: {idx + 2}")
              print(f"   → Error: {e}")
              print(f"   → Row data:\n{row}\n")
              conn.rollback()
              conn.commit()
              break

        conn.commit()
        print(f"✅ Done: {file}")
# ==========================================================
# 🚚 Load Data
# ==========================================================
# --- Load Standardized match data first (this defines MatchID) ---
load_folder_to_table(STANDARDIZED_DIR, "StandardizedMatches")

# --- Then load the TeamMatches (which references MatchID) ---
load_folder_to_table(TEAMFILES_DIR, "TeamMatches")

# --- Finally load Standings ---
load_folder_to_table(STANDINGS_DIR, "Standings")

# ==========================================================
# 🏗️ Build & Assign Team IDs
# ==========================================================
print("\n🏗️ Populating Teams table from StandardizedMatches...")

cur.execute("""
INSERT INTO Teams (name)
SELECT DISTINCT TRIM(HomeTeam)
FROM StandardizedMatches
WHERE HomeTeam IS NOT NULL
ON CONFLICT (name) DO NOTHING;
""")

cur.execute("""
INSERT INTO Teams (name)
SELECT DISTINCT TRIM(AwayTeam)
FROM StandardizedMatches
WHERE AwayTeam IS NOT NULL
ON CONFLICT (name) DO NOTHING;
""")

conn.commit()
print("✅ Teams inserted")

print("\n🔗 Assigning TeamId to StandardizedMatches and TeamMatches...")

cur.execute("""
UPDATE StandardizedMatches sm
SET HomeTeamId = t.id
FROM Teams t
WHERE sm.HomeTeam = t.name;
""")

cur.execute("""
UPDATE StandardizedMatches sm
SET AwayTeamId = t.id
FROM Teams t
WHERE sm.AwayTeam = t.name;
""")

cur.execute("""
UPDATE TeamMatches tm
SET HomeTeamId = t.id
FROM Teams t
WHERE tm.HomeTeam = t.name;
""")

cur.execute("""
UPDATE TeamMatches tm
SET AwayTeamId = t.id
FROM Teams t
WHERE tm.AwayTeam = t.name;
""")

conn.commit()
print("✅ TeamIds assigned successfully")

# ==========================================================
# 🧼 Normalize seasons, derive missing seasons from Date, and link SeasonId
# ==========================================================
print("\n🧼 Normalizing seasons and linking SeasonId...")

# 0) Make sure helper columns exist where needed
cur.execute("ALTER TABLE StandardizedMatches ADD COLUMN IF NOT EXISTS Season VARCHAR(20);")
cur.execute("ALTER TABLE StandardizedMatches ADD COLUMN IF NOT EXISTS SeasonId INT;")
cur.execute("ALTER TABLE Standings ADD COLUMN IF NOT EXISTS SeasonId INT;")
cur.execute("ALTER TABLE TeamMatches ADD COLUMN IF NOT EXISTS Season VARCHAR(20);")
cur.execute("ALTER TABLE TeamMatches ADD COLUMN IF NOT EXISTS SeasonId INT;")
conn.commit()

# 1) Fix reversed season formatting '2019/2018' → '2018/2019'
cur.execute("""
UPDATE Standings
SET Season = CONCAT(
      LEAST(LEFT(Season,4)::INT, RIGHT(Season,4)::INT),
      '/',
      GREATEST(LEFT(Season,4)::INT, RIGHT(Season,4)::INT)
    )
WHERE Season IS NOT NULL
  AND Season ~ '^[0-9]{4}/[0-9]{4}$'
  AND LEFT(Season,4)::INT > RIGHT(Season,4)::INT;
""")
conn.commit()

# 2) Derive Season for StandardizedMatches
cur.execute("""
UPDATE StandardizedMatches
SET Season =
    CASE
      WHEN Date IS NULL THEN NULL
      WHEN EXTRACT(MONTH FROM Date) >= 7
        THEN CONCAT(EXTRACT(YEAR FROM Date)::INT, '/', (EXTRACT(YEAR FROM Date)::INT + 1))
      ELSE CONCAT((EXTRACT(YEAR FROM Date)::INT - 1), '/', EXTRACT(YEAR FROM Date)::INT)
    END
WHERE Season IS NULL
   OR Season !~ '^[0-9]{4}/[0-9]{4}$';
""")
conn.commit()

# 3) Derive Season for TeamMatches
cur.execute("""
UPDATE TeamMatches
SET Season =
    CASE
      WHEN Date IS NULL THEN NULL
      WHEN EXTRACT(MONTH FROM Date) >= 7
        THEN CONCAT(EXTRACT(YEAR FROM Date)::INT, '/', (EXTRACT(YEAR FROM Date)::INT + 1))
      ELSE CONCAT((EXTRACT(YEAR FROM Date)::INT - 1), '/', EXTRACT(YEAR FROM Date)::INT)
    END
WHERE Season IS NULL
   OR Season !~ '^[0-9]{4}/[0-9]{4}$';
""")
conn.commit()

# 4) Insert Seasons into Season table
cur.execute("""
INSERT INTO Seasons (code, start_year, end_year)
SELECT code, LEFT(code,4)::INT, RIGHT(code,4)::INT
FROM (
  SELECT DISTINCT Season AS code FROM Standings WHERE Season IS NOT NULL
  UNION
  SELECT DISTINCT Season FROM StandardizedMatches WHERE Season IS NOT NULL
  UNION
  SELECT DISTINCT Season FROM TeamMatches WHERE Season IS NOT NULL
) s
WHERE code ~ '^[0-9]{4}/[0-9]{4}$'
ON CONFLICT (code) DO NOTHING;
""")
conn.commit()

# 5) Link SeasonId everywhere
cur.execute("""
UPDATE Standings s
SET SeasonId = se.id
FROM Seasons se
WHERE s.Season = se.code;
""")

cur.execute("""
UPDATE StandardizedMatches sm
SET SeasonId = se.id
FROM Seasons se
WHERE sm.Season = se.code;
""")

cur.execute("""
UPDATE TeamMatches tm
SET SeasonId = se.id
FROM Seasons se
WHERE tm.Season = se.code;
""")
conn.commit()

# 6) Sanity checks
cur.execute("SELECT COUNT(*) FROM StandardizedMatches WHERE SeasonId IS NULL;")
print("StandardizedMatches missing SeasonId:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM TeamMatches WHERE SeasonId IS NULL;")
print("TeamMatches missing SeasonId:", cur.fetchone()[0])
cur.execute("SELECT COUNT(*) FROM Standings WHERE SeasonId IS NULL;")
print("Standings missing SeasonId:", cur.fetchone()[0])
