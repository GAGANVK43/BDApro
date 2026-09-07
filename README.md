# 🎬 Netflix & Movie Big Data Analytics Platform
### *Enterprise Big Data Analytics Web Application using Python, Flask, MongoDB Atlas, Apache Hadoop HDFS, Apache Hive, and Chart.js*
#### *Optimized for Vercel Serverless Deployment & GitHub CI/CD*

---

## 📌 Project Overview
The **Netflix & Movie Data Analytics Platform** is a college Big Data engineering and analytics web application. The platform processes, analyzes, and visualizes large-scale entertainment datasets to extract deep insights into global streaming and entertainment trends:

1. **Genre Dominance & Distribution**
2. **Maturity & Content Rating Patterns**
3. **Historical Release Velocity & Production Trajectory**
4. **Movie vs. TV Show Catalog Composition**
5. **Geographic & Country-wise Production Share**
6. **Top-Rated & Acclaimed Title Rankings**
7. **Longitudinal Platform Catalog Expansion**

---

## 🏗️ System Architecture

```mermaid
flowchart TD
    subgraph Big Data Data Lake & Processing (Local / Cluster)
        A[Raw Netflix / Movie Dataset] -->|1. Ingestion| B[Python Data Cleaning Engine]
        B -->|2. Standardization & Imputation| C[Cleaned Standardized CSV]
        C -->|3. Distributed Storage| D[Hadoop HDFS /netflix-analytics]
        D -->|4. SQL-on-Hadoop Analytics| E[Apache Hive Data Warehouse]
        E -->|5. ORC Partitioned Tables| F[Hive Big Data Aggregations]
    end

    subgraph Operational Cloud NoSQL Store
        F -->|6. Ingestion Pipeline| G[MongoDB Atlas Cluster]
    end

    subgraph Production Cloud Deployment (Vercel)
        G -->|7. PyMongo Query Layer| H[Flask REST API Backend]
        H -->|8. JSON Endpoints| I[HTML5 / CSS3 / JavaScript Frontend]
        I -->|9. Hardware-Accelerated Rendering| J[Interactive Chart.js Visualizations]
    end

    style A fill:#1E293B,stroke:#E50914,stroke-width:2px,color:#FFF
    style B fill:#1E293B,stroke:#06B6D4,stroke-width:2px,color:#FFF
    style C fill:#1E293B,stroke:#06B6D4,stroke-width:2px,color:#FFF
    style D fill:#1E293B,stroke:#F59E0B,stroke-width:2px,color:#FFF
    style E fill:#1E293B,stroke:#F59E0B,stroke-width:2px,color:#FFF
    style F fill:#1E293B,stroke:#F59E0B,stroke-width:2px,color:#FFF
    style G fill:#1E293B,stroke:#10B981,stroke-width:2px,color:#FFF
    style H fill:#1E293B,stroke:#E50914,stroke-width:2px,color:#FFF
    style I fill:#1E293B,stroke:#06B6D4,stroke-width:2px,color:#FFF
    style J fill:#1E293B,stroke:#E50914,stroke-width:2px,color:#FFF
```

---

## 🛠️ Technology Stack & Role Justification

| Technology | Role | Purpose & Academic Rationale |
| :--- | :--- | :--- |
| **Python 3.x** | Preprocessing & Pipeline Glue | Data cleansing, regex duration parsing, PyMongo bridging, Flask API. |
| **Flask** | REST API & Web Backend | Lightweight, modular WSGI microframework optimized for Vercel serverless deployment. |
| **MongoDB Atlas** | Cloud NoSQL Document Store | Stores nested JSON arrays (`genres`, `country`) and pre-computed analytical statistics. |
| **PyMongo** | Python-MongoDB Driver | Connection pooling, index management, and aggregation pipeline execution. |
| **Apache Hadoop (HDFS)** | Distributed Storage | Fault-tolerant, distributed block storage for raw and cleaned big datasets. |
| **Apache Hive** | SQL Data Warehouse | Executes map-reduce/Tez aggregations using `LATERAL VIEW explode()` and window functions. |
| **HTML5 / CSS3 / Vanilla JS** | Web UI & Frontend | Responsive dark analytics interface with sidebar navigation, live status pills, and modals. |
| **Chart.js** | Interactive Visualizations | Hardware-accelerated canvas charts for real-time multi-filter slicing without page reloads. |
| **Vercel** | Cloud Serverless Hosting | Hosts the Flask backend and static assets globally with instant scaling. |

---

## 📂 Project Structure

```
netflix-movie-analytics/
│
├── app.py                          # Main Flask Application & Vercel WSGI entry point
├── main.py                         # Master local Python entry point
├── run.py                          # Alias local runner
├── vercel.json                     # Vercel serverless deployment config
├── .env.example                    # Template environment variables
├── .env                            # Local environment configuration (gitignored)
├── .gitignore                      # Git ignore rules
├── requirements.txt                # Production Python dependencies
│
├── api/
│   ├── __init__.py
│   ├── routes.py                   # View routes (HTML templates)
│   └── analytics_routes.py         # REST JSON API routes (/api/...)
│
├── services/
│   ├── __init__.py
│   ├── mongodb_service.py          # MongoDB Atlas data layer with PyMongo
│   ├── analytics_service.py        # Analytics aggregation & dynamic insights
│   └── pipeline_service.py         # Big data infrastructure & health check service
│
├── templates/
│   ├── base.html                   # Master layout with sidebar, navbar & status badges
│   ├── dashboard.html              # Main Executive Analytics Dashboard
│   ├── genres.html                 # Genre Analysis & Distribution
│   ├── ratings.html                # Content & Maturity Rating Patterns
│   ├── releases.html               # Historical Release Trends
│   ├── countries.html              # Geographic Distribution
│   ├── movies.html                 # Interactive Movie Explorer & Metadata Modal
│   ├── pipeline.html               # Big Data Pipeline & System Health
│   ├── database.html               # MongoDB Architecture & Live Collections
│   └── about.html                  # Project Architecture & Viva Voce Guide
│
├── static/
│   ├── css/
│   │   └── style.css               # Professional dark analytics styling
│   └── js/
│       ├── main.js                 # Global utilities, filters & live status polling
│       ├── dashboard.js            # Executive dashboard charts & KPIs
│       ├── genres.js               # Genre charts & tables
│       ├── ratings.js              # Rating charts
│       ├── releases.js             # Release trend charts
│       ├── countries.js            # Country distribution charts
│       ├── movies.js               # Movie explorer, search, pagination & modal
│       ├── pipeline.js             # Pipeline live status & trigger actions
│       └── database.js             # MongoDB live status & collections inspector
│
├── data/
│   ├── raw/
│   │   └── netflix_titles.csv      # Raw input dataset
│   └── cleaned/
│       └── netflix_cleaned.csv     # Normalized, cleaned dataset
│
├── python/
│   ├── data_cleaning.py            # Preprocessing & deduplication engine
│   ├── mongodb_connection.py       # MongoDB Atlas connection handler
│   ├── load_mongodb.py             # Ingestion pipeline into MongoDB collections
│   ├── analytics.py                # Hybrid analytics & dynamic narrative insights
│   └── utils.py                    # Live infrastructure health checker
│
├── hive/
│   ├── create_tables.hql           # External & ORC partitioned table DDL
│   ├── genre_analysis.hql          # Multi-genre explosion and frequency queries
│   ├── rating_analysis.hql         # Maturity rating distribution & proportions
│   ├── release_analysis.hql        # Annual velocity & YoY growth rate queries
│   ├── country_analysis.hql        # Multi-country co-production analytics
│   └── complete_analysis.hql       # Master Hive analytical query suite
│
├── hadoop/
│   ├── upload_to_hdfs.sh           # HDFS upload script (Linux/Mac)
│   ├── upload_to_hdfs.bat          # HDFS upload script (Windows)
│   ├── run_pipeline.sh             # End-to-end Big Data pipeline orchestrator
│   └── run_pipeline.bat            # Windows pipeline orchestrator
│
├── mongodb/
│   └── aggregation_queries.js      # Production MongoDB aggregation pipelines
│
├── run_project.bat                 # Windows one-click runner (python app.py)
└── run_project.sh                  # Linux one-click runner
```

---

## 🚀 Local Quick Start Guide

### 1. Installation
Clone or navigate to the repository directory and install dependencies:
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Copy `.env.example` to `.env`:
```env
MONGODB_URI=mongodb+srv://<username>:<password>@cluster0.example.mongodb.net/?retryWrites=true&w=majority
MONGODB_DB_NAME=netflix_analytics
SECRET_KEY=netflix-big-data-secret-2026
PORT=5000
```
> **Note:** If MongoDB is offline, the platform automatically switches to local dataset fallback mode with zero downtime, displaying the connection state on the top navbar.

### 3. Run Locally
**Windows:**
```cmd
run_project.bat
```
*or*
```bash
python app.py
```

**Linux / Mac / WSL:**
```bash
chmod +x run_project.sh
./run_project.sh
```

Open your browser and navigate to: **http://127.0.0.1:5000**

---

## 🌐 Deploying to Vercel

The application is pre-configured with `vercel.json` for Python serverless hosting.

### Method 1: Deploy with Vercel CLI
```bash
# 1. Install Vercel CLI
npm install -g vercel

# 2. Deploy
vercel
```

### Method 2: Deploy via GitHub
1. Push your repository to GitHub (see instructions below).
2. Go to [vercel.com](https://vercel.com) and click **"Add New Project"**.
3. Import your GitHub repository.
4. Under **Environment Variables**, add:
   - `MONGODB_URI` = your MongoDB Atlas connection string
   - `MONGODB_DB_NAME` = `netflix_analytics`
   - `SECRET_KEY` = your secret key
5. Click **Deploy**.

---

## 🐙 Pushing to GitHub

```bash
# 1. Initialize git (if not already initialized)
git init

# 2. Add files
git add .

# 3. Commit
git commit -m "feat: Netflix Big Data Analytics Platform with Flask, MongoDB Atlas & Vercel deployment"

# 4. Set remote repository & push
git branch -M main
git remote add origin https://github.com/<your-username>/netflix-movie-analytics.git
git push -u origin main
```

---

## 🔌 REST API Endpoints

| Endpoint | Method | Description |
| :--- | :--- | :--- |
| `/api/summary` | GET | Top KPI cards and dynamic natural language insights. |
| `/api/genres` | GET | Genre distribution, Movie/TV format split, and average rating scores. |
| `/api/ratings` | GET | Content maturity rating proportions and format breakdown. |
| `/api/releases` | GET | Annual release timeline statistics and cumulative catalog expansion. |
| `/api/countries` | GET | Top producing nations and geographic rankings. |
| `/api/top-movies` | GET | Highest-rated titles ordered by calculated quality score. |
| `/api/movies` | GET | Paginated title explorer with search, multi-filter slicing, and sorting. |
| `/api/movie/<show_id>` | GET | Complete title metadata inspector (director, cast, genres, synopsis). |
| `/api/filters` | GET | Unique filter metadata (years, genres, countries, ratings, types). |
| `/api/pipeline-status` | GET | Live infrastructure status across Hadoop, Hive, MongoDB, Python, Datasets. |
| `/api/database-status` | GET | Live MongoDB Atlas status, collections, and document counts. |
| `/api/pipeline/clean` | POST | Triggers Python data cleaning pipeline in real-time. |
| `/api/pipeline/sync-mongodb` | POST | Ingests cleaned dataset and pre-calculated aggregations into MongoDB Atlas. |

---

## 🎓 Faculty Viva Voce Questions & Answers

**Q1: Why use Hadoop HDFS instead of storing raw CSVs directly in MongoDB?**  
> *Answer:* HDFS is engineered for high-throughput batch writes, multi-node replication, and immutable long-term storage of multi-gigabyte/terabyte data lakes. MongoDB is an OLTP document database optimized for low-latency web queries. HDFS acts as the data lake single source of truth, while MongoDB stores processed application documents.

**Q2: How does Apache Hive handle multi-valued columns like comma-separated genres?**  
> *Answer:* In `hive/genre_analysis.hql`, we utilize Hive's `LATERAL VIEW explode(split(listed_in, ','))` syntax. This pivots the comma-separated strings into discrete rows, enabling standard SQL `GROUP BY` and `COUNT()` aggregations.

**Q3: How does the local Big Data processing environment link with the Vercel cloud deployment?**  
> *Answer:* Hadoop and Hive run in the local data engineering environment to clean and aggregate the massive raw catalog. The resulting processed records and statistics are loaded into MongoDB Atlas. The Flask application hosted on Vercel queries MongoDB Atlas directly via PyMongo without needing heavy Hadoop binaries on the serverless web tier.

---

## 📄 License
This project is open-source and built for academic presentation and educational purposes.
