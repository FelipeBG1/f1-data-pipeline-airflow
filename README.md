# 🏎️ F1 Data Pipeline with Airflow

End-to-end Data Engineering project built with:

- Apache Airflow
- PostgreSQL
- Docker
- Python
- Pandas

The pipeline extracts Formula 1 race results data from an external API, processes nested JSON responses, builds a dimensional data model, creates analytics marts, and loads analytical tables into PostgreSQL.

---

# 📌 Project Goals

This project was created to simulate a real-world Data Engineering workflow:

- Extract data from an external API
- Handle pagination and nested JSON
- Build reusable ETL components
- Store raw and modeled data in PostgreSQL
- Orchestrate pipelines with Airflow
- Create a dimensional model using fact and dimension tables
- Build analytical marts for business insights

---

# 🏗️ Architecture

```text
API
↓
RAW LAYER
(raw_race_results)
↓
DIMENSIONAL MODEL
(dimensions + facts)
↓
ANALYTICS LAYER
(driver_season_stats)
```

---

# 🧰 Tech Stack

| Technology | Purpose |
|---|---|
| Python | Data processing |
| Pandas | Data transformation |
| PostgreSQL | Data warehouse |
| Apache Airflow | Pipeline orchestration |
| Docker | Containerization |
| SQLAlchemy | Database connection |
| dotenv | Environment variables |

---

# 📂 Project Structure

```text
f1_data_pipeline_airflow/
│
├── dags/
│   └── f1_raw_results_pipeline_dag.py
│
├── data/
│   └── raw/
│       ├── csv/
│       └── json/
│
├── src/
│   ├── extract/
│   │   ├── f1_results_api.py
│   │   └── snapshot_utils.py
│   │
│   ├── transform/
│   │   ├── build_dimensional_model.py
│   │   └── build_analytics_marts.py
│   │
│   ├── load/
│   │   ├── save_to_db.py
│   │   ├── read_from_db.py
│   │   └── load_dimensional_model.py
│   │
│   └── utils/
│       └── db_connection.py
│
├── main.py
├── docker-compose.yaml
├── requirements.txt
└── .env

```

---

# 🟤 RAW Layer

## raw_race_results

Stores the raw processed API response before dimensional modeling.

### Main Columns

```text
season
round
race_name
race_date

circuit_id
circuit_name
country
locality

driver_id
driver_code
driver_number
driver_first_name
driver_last_name
driver_nationality

constructor_id
constructor_name
constructor_nationality

grid
position
position_text
points
laps
status

race_time
race_time_millis

fastest_lap_rank
fastest_lap_lap
fastest_lap_time
fastest_lap_avg_speed
```

---

# 🔵 Dimensional Model

## Dimension Tables

### dim_drivers

Stores driver information.

### dim_constructors

Stores constructor/team information.

### dim_circuits

Stores circuit information.

### dim_races

Stores race metadata.

---

# 🟠 Fact Table

## fact_race_results

Stores race results for each driver in each race.

### Grain

```text
1 row = 1 driver result in 1 race
```

---

# 🟢 Analytics Layer

## driver_season_stats

Stores aggregated season statistics for each driver.

### Grain

```text
1 row = 1 driver in 1 season
```

### Columns

```text
season
driver_id
driver_first_name
driver_last_name
total_races
total_points
wins
podiums
dnf_count
average_finish_position
fastest_laps
```

---

# 🔄 Pipeline Flow

## Step 1 — Extract

- API requests
- Pagination handling
- Nested JSON parsing

## Step 2 — Raw Load

- Save raw processed data into PostgreSQL

## Step 3 — Transform

- Create dimensional model
- Standardize inconsistent IDs
- Remove duplicates
- Generate race_id

## Step 4 — Load Modeled Tables

- Save dimensions
- Save fact table

## Step 5 — Build Analytics Marts

- Aggregate season statistics
- Create KPI tables
- Generate analytics-ready datasets

## Step 6 — Load Analytics Tables

- Save analytics marts into PostgreSQL

---

# ⚙️ Airflow DAG

## DAG ID

```text
f1_raw_results_pipeline
```

The DAG orchestrates:

```text
Extract
↓
Load RAW
↓
Build dimensional model
↓
Load dimensions and facts
↓
Build analytics marts
↓
Load analytics tables
```

---

# 📸 Suggested Screenshots

## 1. Airflow DAG

Add a screenshot of the DAG execution success.

Example:

```markdown
![Airflow DAG](images/airflow_dag.png)
```

---

## 2. PostgreSQL Tables

Show created dimensional, fact, and analytics tables.

```text
images/postgres_tables.png
```

---

## 3. Analytics Table Example

```sql
SELECT *
FROM driver_season_stats
ORDER BY total_points DESC;
```

---

## 4. Query Examples

### Dimensional Model Query

Example query using fact and dimension joins.

```sql
SELECT
    d.driver_first_name,
    d.driver_last_name,
    r.race_name,
    f.position,
    f.points
FROM fact_race_results f
JOIN dim_drivers d
    ON f.driver_id = d.driver_id
JOIN dim_races r
    ON f.race_id = r.race_id
LIMIT 10;
```

### Analytics Query

Example query using the analytics layer to retrieve aggregated driver season statistics.

```sql
SELECT
    driver_first_name,
    driver_last_name,
    total_points,
    wins,
    podiums,
    average_finish_position
FROM driver_season_stats
ORDER BY total_points DESC
LIMIT 10;
```

---

# 🚀 Running the Project

## Start containers

```bash
docker compose up -d
```

---

## Run Airflow

Access:

```text
http://localhost:8080
```

---

## Run locally

```bash
python3 main.py
```

---

# 🧪 Data Quality Handling

The pipeline includes:

- Duplicate detection
- Duplicate removal
- ID standardization
- Data normalization
- Logging
- Aggregated analytics marts

---

# 📈 Future Improvements

- Streamlit dashboard
- Incremental loads
- dbt integration
- Metabase integration
- Data tests
- CI/CD
- Historical data (2018-current)
- Championship analytics

---

# 👨‍💻 Author

Data Engineering portfolio project focused on:

- ETL development
- Data modeling
- Pipeline orchestration
- Analytics engineering
- Analytical data preparation
