import os
import pandas as pd

# Define the folder containing the season files
input_folder = "./data/files/SeasonMatches"
output_folder = "./data/files/StandardizedSeasonMatches"

# Ensure the output folder exists
os.makedirs(output_folder, exist_ok=True)

# Columns to keep in the output files
columns_to_keep = [
    "Date", "HomeTeam", "AwayTeam", "FTHG", "FTAG", "FTR", "HTHG", "HTAG", "HTR",
    "Referee", "HS", "AS", "HST", "AST", "HF", "AF", "HC", "AC", "HY", "AY",
    "HR", "AR", "B365H", "B365D", "B365A"
]

# Function to generate the output file name based on the input file name
def generate_output_filename(input_filename):
    year = ''.join(filter(str.isdigit, input_filename))[:6]  # Extract first 6 digits (e.g., 200304)
    return f"EPLS{year}.csv"

# Function to process a single CSV file
def process_csv(file_path, output_path):
    try:
        # Load CSV with error handling for malformed rows
        df = pd.read_csv(
            file_path,
            encoding='latin1',  # Handle non-UTF-8 characters
            on_bad_lines='skip'  # Skip problematic rows (pandas >= 1.3.0)
        )
        
        # Standardize the Date column if it exists
        if 'Date' in df.columns:
            df['Date'] = pd.to_datetime(df['Date'], errors='coerce').dt.strftime('%d/%m/%Y')
        
        # Keep only the specified columns
        df = df[[col for col in columns_to_keep if col in df.columns]]
        
        # Save the cleaned and standardized DataFrame to the output folder
        df.to_csv(output_path, index=False)
        print(f"Processed {file_path} -> {output_path}")
    except Exception as e:
        print(f"Error processing file {file_path}: {e}")

# Loop through all files in the input folder
for filename in os.listdir(input_folder):
    if filename.endswith(".csv"):
        file_path = os.path.join(input_folder, filename)
        output_filename = generate_output_filename(filename)
        output_path = os.path.join(output_folder, output_filename)
        
        # Process the file
        process_csv(file_path, output_path)