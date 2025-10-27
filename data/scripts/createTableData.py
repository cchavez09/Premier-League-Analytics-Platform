import os
import pandas as pd
import psycopg2

print("CWD:", os.getcwd())
print("SCRIPT DIR:", os.path.dirname(os.path.abspath(__file__)))

# --- Connect to PostgreSQL ---
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

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(SCRIPT_DIR, "..", "files")

TEAMFILES_DIR = os.path.join(DATA_DIR, "TeamFiles")
STANDINGS_DIR = os.path.join(DATA_DIR, "Standings")
STANDARDIZED_DIR = os.path.join(DATA_DIR, "StandardizedSeasonMatches")

# --- Helper: drop duplicate columns (case-insensitive) ---
def drop_duplicate_columns_for_pg(df):
    seen = set()
    keep_cols = []
    for col in df.columns:
        col_lower = col.lower()
        if col_lower not in seen:
            keep_cols.append(col)
            seen.add(col_lower)
    return df[keep_cols]

# --- Helper: load CSVs from folder into a table (with debugging) ---
def load_folder_to_table(folder_path, table_name):
    if not os.path.exists(folder_path):
        print(f"❌ Folder not found: {folder_path}")
        return

    print(f"📂 Loading data from: {folder_path}")
    for file in os.listdir(folder_path):
        if not file.endswith(".csv"):
            continue

        file_path = os.path.join(folder_path, file)
        print(f"\n→ Inserting {file} into {table_name}...")

        try:
            df = pd.read_csv(file_path)
        except Exception as e:
            print(f"❌ Failed to read {file}: {e}")
            continue

        df.rename(columns={"AS": "AS_"}, inplace=True)
        df = drop_duplicate_columns_for_pg(df)

        # 🧹 Clean data automatically
        # Only drop based on these IDs if they exist in this file
        for col_set in [["HomeTeamId", "AwayTeamId", "MatchID"], ["MatchID"]]:
            existing = [c for c in col_set if c in df.columns]
            if existing:
                df.dropna(subset=existing, inplace=True)
                break  # stop after using the most complete set

        # Replace remaining NaN with None for psycopg2
        df = df.where(pd.notnull(df), None)


        columns = ', '.join(df.columns)
        placeholders = ', '.join(['%s'] * len(df.columns))
        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        for idx, row in df.iterrows():
            try:
                cur.execute(sql, tuple(row))
            except Exception as e:
                print(f"\n❌ ERROR in file: {file}")
                print(f"   → Row number: {idx + 2}")  # +2 accounts for header + 0-index
                print(f"   → Error: {e}")
                print(f"   → Row data:\n{row}\n")
                conn.rollback()  # undo partial inserts from this row
                break  # stop this file, continue with others

        conn.commit()
        print(f"✅ Finished inserting {file}")

# --- Load all CSVs ---
load_folder_to_table(TEAMFILES_DIR, "TeamMatches")
load_folder_to_table(STANDINGS_DIR, "Standings")
load_folder_to_table(STANDARDIZED_DIR, "StandardizedMatches")

# --- Done ---
cur.close()
conn.close()
print("✅ All CSV data successfully loaded into PostgreSQL!")
