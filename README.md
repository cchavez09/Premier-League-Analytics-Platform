# COMP-330-Group-Project
This is a group Software Engineering Project for COMP 330 at Loyola University Chicago. 

**Futstat** is a full-stack Premier League analytics platform that provides live match scores, intelligent predictions, and rich historical team statistics — all in one modern dashboard.

# Overview
Futstat helps football fans and analysts explore real-time and historical Premier League data.  
It combines predictive modeling, interactive charts, and team-by-team insights built with modern web technologies.

# Tech Stack
- **Frontend:** React.js  
- **Backend:** Node.js + Express  
- **Database:** PostgreSQL  
- **APIs:** Football data feeds (live scores, match stats, and fixtures). Link - "https://www.football-data.org/"

# Project Structure
frontend/     → React.js app (UI & dashboards)
backend/      → Express API for match data and predictions
data/         → Datasets and scripts for ETL and analysis
docs/         → Documentation and reports

# System Requirements
- **Node.js:** v16 or higher  
- **Python:** 3.8 or higher  
- **PostgreSQL:** v12+  
- **npm** or **yarn** package manager  


# Setup Instructions

**This is a step-by-step format for the setup. Alternatively, you can run all installations automatically using the unified requirements.txt file located in the project root.**

# 1️⃣ Clone the Repository - 
```bash
git clone https://github.com/yourusername/COMP-330-Group-Project.git
cd COMP-330-Group-Project
pip install -r requirements.txt

Backend setup - 
cd backend
Create a file named pginfo.env: 
HOME_API_KEY=your_football_data_api_key
DB_HOST=localhost
DB_PORT=5432
DB_NAME=futstat
DB_USER=postgres
DB_PASSWORD=your_password
PORT=5001 || 5000  # change if 5000 is unavailable
npm install
npm run dev

Frontend setup -
cd frontend
Create env file and add: REACT_APP_API_URL=http://localhost:5001
npm install 
npm start

Database Setup- 
Create a new database named futstat
cd data/scripts
python pullAllData.py
python createTableData.py
Change your Database password in the env file. 

# Environment Variables
- **Backend:** `backend/pginfo.env`  
- **Frontend:** `frontend/.env`  

These files contain API keys, database credentials, and server URLs required for the app to run.  
They are not included in the repo for security reasons.

Run the app
Frontend → http://localhost:3000
Backend API → http://localhost:5001
```

# Features
- **Live Match Scores** – Displays up-to-date Premier League scores recent games, upcoming fixtures.
- **Match Predictions** – Predictive models analyze past performance to forecast outcomes. 
- **Historical Team Data** – Explore season-by-season statistics for every team for last 25 years.
- **Visual Dashboards** – Interactive charts and team comparisons.
- **Fast & Lightweight** – Express API with optimized PostgreSQL queries for quick responses.

# How It Works
- The **Express backend** retrieves match and team data from football APIs and the PostgreSQL database.  
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
