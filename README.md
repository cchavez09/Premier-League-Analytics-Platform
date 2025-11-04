# COMP-330-Group-Project
This is a group Software Engineering Project for COMP 330 at Loyola University Chicago. 

**Futstat** is a full-stack Premier League analytics platform that provides live match scores, intelligent predictions, and rich historical team statistics — all in one modern dashboard.

# Overview
Futstat helps football fans and analysts explore real-time and historical Premier League data.  
It combines predictive modeling, interactive charts, and team-by-team insights built with modern web technologies.

# Tech Stack
- **Frontend:** React.js  
- **Backend:** Flask (Python)  
- **Database:** PostgreSQL  
- **APIs:** Football data feeds (live scores, match stats, and fixtures)

# Project Structure
frontend/     → React.js app (UI & dashboards)
backend/      → Flask API for match data and predictions
data/         → Datasets and scripts for ETL and analysis
docs/         → Documentation and reports

# Setup Instructions

# 1️⃣ Clone the Repository
```bash
git clone https://github.com/yourusername/COMP-330-Group-Project.git
cd COMP-330-Group-Project

Backend setup - 
cd backend
npm install 
npm install pg
pip install -r requirements.txt
pip install pandas
pip install psycopg2-binary
npm install node-fetch@2

Frontend setup -
cd frontend
npm install 
npm install -r requirements.txt

Database Setup- 
Create a new database named futstat
Go into the folder cd data/scripts
Run 1- pullAllData.py 2- createTableData.py
Change your Database password in the env file. 

Run the app
Frontend → http://localhost:3000
Backend API → http://localhost:5000
```

# Features
- **Live Match Scores** – Displays up-to-date Premier League scores recent games, upcoming fixtures.
- **Match Predictions** – Predictive models analyze past performance to forecast outcomes. 
- **Historical Team Data** – Explore season-by-season statistics for every team for last 25 years.
- **Visual Dashboards** – Interactive charts and team comparisons.
- **Fast & Lightweight** – Flask API with optimized PostgreSQL queries for quick responses.

# How It Works
- The **Flask backend** retrieves match and team data from football APIs and the PostgreSQL database.  
- The **React frontend** fetches this data and displays it as tables, graphs, and predictions.  
- The **data scripts** (`pullAllData.py`, `createTableData.py`) collect and structure CSV data into database tables.  
- The **prediction engine** (inside backend) uses statistical models and historical trends to compute win probabilities.  


# Contributors
This project was developed as part of **COMP 330 – Software Engineering** at **Loyola University Chicago**.

- Oscar Sanchez
- Christian Chavez
- Syed Moosa Aleem
- Joel Mesa
- Abdul Rehman Shad

# Future Improvements
- Add a feature to collect the latest csv files through automation and remove the dependency on the API for live and recent match fixtures data
