import os
import pandas as pd
import psycopg2
 
print("CWD:", os.getcwd())
print("SCRIPT DIR:", os.path.dirname(os.path.abspath(__file__)))
 
# --- Connect to PostgreSQL ---
# PERSONAL INFORMATION: Update these details as necessary
conn = psycopg2.connect(
    dbname="soccerdata_db",
    user="postgres",
    password="HalaMadrid1!",
    host="localhost",
    port="5432"
)
cur = conn.cursor()
cur.execute("SET datestyle TO 'DMY';")
 
# --- Create the tables (only once) ---
cur.execute("""
CREATE TABLE IF NOT EXISTS TeamMatches (
    id SERIAL PRIMARY KEY,
    homeTeamID BIGINT,
    awayTeamID INT,
    MatchID VARCHAR(50),
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
    B365A FLOAT
);
""")
 
cur.execute("""
CREATE TABLE IF NOT EXISTS Standings (
    id SERIAL PRIMARY KEY,
    TeamId INT,
    Team VARCHAR(100),
    Season VARCHAR(20),
    MatchesPlayed INT,
    Wins INT,
    Draws INT,
    Losses INT,
    Points INT,
    AvgB365H FLOAT,
    AvgB365D FLOAT,
    AvgB365A FLOAT,
    AvgB365Overall FLOAT,
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
    PerGameAR FLOAT
);
""")
 
cur.execute("""
CREATE TABLE IF NOT EXISTS StandardizedMatches (
    id SERIAL PRIMARY KEY,
    HomeTeamId BIGINT,
    AwayTeamId BIGINT,
    MatchID BIGINT,
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
    Season VARCHAR(20)
);
""")
 
conn.commit()
 
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))  # ...\data\scripts
 
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "files")       # ...\data\files
 
TEAMFILES_DIR = os.path.join(DATA_DIR, "TeamFiles")
 
STANDINGS_DIR = os.path.join(DATA_DIR, "Standings")
 
STANDARDIZED_DIR = os.path.join(DATA_DIR, "StandardizedSeasonMatches")
 
# --- Helper to drop duplicate columns for PostgreSQL ---
def drop_duplicate_columns_for_pg(df):
    """
    Drop duplicate columns that would conflict in PostgreSQL (case-insensitive).
    Keeps the first occurrence.
    """
    seen = set()
    keep_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if col_lower not in seen:
            keep_cols.append(col)
            seen.add(col_lower)
    return df[keep_cols]
 
# --- Helper to load any folder full of CSVs into one table ---
def load_folder_to_table(folder_path, table_name):
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return
 
    print(f"📂 Loading data from: {folder_path}")
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):
            file_path = os.path.join(folder_path, file)
            print(f"  → Inserting {file} into {table_name}...")
           
            # Load CSV
            df = pd.read_csv(file_path)
 
            # Force rename for safety (existing in your code)
            df.rename(columns={"AS": "AS_"}, inplace=True)
           
            # Drop duplicate columns that PostgreSQL would see as duplicates
            df = drop_duplicate_columns_for_pg(df)
 
            # Replace NaN with None for psycopg2
            df = df.where(pd.notnull(df), None)
 
            # Prepare SQL insert
            columns = ', '.join(df.columns)
            placeholders = ', '.join(['%s'] * len(df.columns))
            sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
 
            # Insert row by row
            for _, row in df.iterrows():
                cur.execute(sql, tuple(row))
 
            conn.commit()
 
# --- Load CSVs ---
load_folder_to_table(TEAMFILES_DIR, "TeamMatches")
load_folder_to_table(STANDINGS_DIR, "Standings")
load_folder_to_table(STANDARDIZED_DIR, "StandardizedMatches")
 
# --- Done ---
cur.close()
conn.close()
print("✅ All CSV data successfully loaded into PostgreSQL!")