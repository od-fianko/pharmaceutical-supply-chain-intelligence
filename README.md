# Pharmaceutical Supply Chain Intelligence System

An end-to-end data engineering and analytics project exploring pharmaceutical supply chain verification, anomaly detection and operational risk monitoring using synthetic data.

## 1. Project Overview

Pharmaceutical supply chains require reliable product verification and traceability. Large volumes of verification events can make it difficult to identify unusual patterns, repeated scans and potentially suspicious product movements.

This project develops a simulated pharmaceutical supply chain intelligence system that:

- Generates synthetic pharmaceutical verification data.
- Stores structured data in PostgreSQL.
- Cleans and transforms data through a Python ETL pipeline.
- Performs exploratory data analysis and feature engineering.
- Applies machine learning and rule-based anomaly detection.
- Classifies serial numbers into risk categories.
- Presents analytical findings through an interactive Streamlit dashboard.

**Important:** This is an educational prototype built with synthetic data. It is not connected to a real pharmaceutical verification network and does not establish counterfeit activity or regulatory non-compliance.

## 2. Project Objectives

1. Build a structured pharmaceutical supply chain database.
2. Develop a reproducible data ingestion and cleaning pipeline.
3. Analyse pharmaceutical verification outcomes and geographical activity.
4. Engineer features that describe serial-number verification behaviour.
5. Explore anomaly detection using Isolation Forest.
6. Combine machine learning outputs with interpretable business rules.
7. Communicate findings through an interactive analytical dashboard.

## 3. Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python |
| Data processing | Pandas, NumPy |
| Database | PostgreSQL |
| Database integration | SQLAlchemy, psycopg2 |
| Exploratory analysis | Jupyter Notebook, Matplotlib, Seaborn |
| Machine learning | Scikit-learn, Isolation Forest |
| Visualisation | Plotly |
| Dashboard | Streamlit |
| Development | Visual Studio Code |

## 4. System Architecture

The project follows a data pipeline architecture:

1. **Data generation:** Synthetic products, batches, locations and verification events are generated.
2. **Data storage:** PostgreSQL stores the structured datasets in relational tables.
3. **ETL:** Python cleans, validates and loads the generated data.
4. **Exploratory analysis:** Verification outcomes, geographical activity and repeated serial numbers are examined.
5. **Feature engineering:** Serial-number behaviour is converted into analytical features.
6. **Anomaly detection:** Isolation Forest and rule-based detection identify patterns requiring investigation.
7. **Risk classification:** Detection outputs are combined into High, Medium and Low risk categories.
8. **Dashboard:** Streamlit and Plotly present the results interactively.

## 5. Database Design

The PostgreSQL database contains four main tables:

- `products`: Product identifiers, names, manufacturers and categories.
- `batches`: Product batch information, manufacture dates, expiry dates and quantities.
- `locations`: Verification locations, countries and location types.
- `verification_events`: Serial numbers, timestamps, verification outcomes and related product, batch and location identifiers.

The schema uses primary keys, foreign keys, constraints and indexes to support data integrity and analytical queries.

## 6. Dataset

The project generates synthetic data containing:

| Dataset | Records |
|---|---:|
| Products | 50 |
| Batches | 200 |
| Locations after ETL | 101 |
| Original verification events after cleaning | 50,000 |
| Additional synthetic test events | 27 |

The original verification dataset contains 50,000 records after removing five duplicate event records.

Five missing location references are handled using an `Unknown Location` record.

Additional controlled test scenarios are used to evaluate the detection logic separately from the original dataset.

## 7. Analytical Approach

### Exploratory Data Analysis

The analysis examines:

- Verification outcome distributions.
- Verification activity by country.
- Daily verification activity.
- Repeated serial-number activity.
- Expiry-date comparisons.

### Feature Engineering

Serial-number features include:

- Total scan count.
- Number of distinct verification locations.
- Number of distinct countries.
- Average and minimum time between scans.
- Maximum estimated distance between consecutive scans.
- Maximum estimated travel speed.
- Number and proportion of failed verifications.
- Scans per hour.

Geographical distance and speed calculations use approximate country-centre coordinates. These are screening estimates, not actual pharmacy-to-pharmacy travel measurements.

### Machine Learning

Isolation Forest is used as an unsupervised anomaly detection method.

The model evaluates aggregated serial-number behaviour and produces anomaly scores and classifications.

The initial model uses 200 estimators and a contamination parameter of 0.01.

### Rule-Based Detection

Four detection rules are implemented:

1. Rapid scanning.
2. Excessive local scanning.
3. High verification failure rate.
4. Rapid cross-border movement.

The thresholds are experimental assumptions selected for this synthetic prototype. They are not official pharmaceutical industry standards.

### Hybrid Risk Classification

Machine learning and rule-based outputs are combined:

- **High:** Two or more rule-based flags.
- **Medium:** One rule-based flag or a machine-learning anomaly without two rule flags.
- **Low:** No detection flags.

These classifications prioritise patterns for further investigation; they do not establish fraud or counterfeit products.

## 8. Interactive Dashboard

The Streamlit dashboard provides:

- Verification outcome analytics.
- Geographic verification activity.
- Risk distribution monitoring.
- An investigation table containing flagged serial numbers.
- Serial-number event history.

The dashboard distinguishes original synthetic records from controlled synthetic test scenarios.

## 9. Project Structure

```text
pharmaceutical-supply-chain-intelligence/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│   └── 01_data_exploration.ipynb
│
├── src/
│   ├── generate_data.py
│   └── clean_load.py
│
├── sql/
│   ├── schema.sql
│   └── analysis_queries.sql
│
├── dashboard/
│   └── app.py
│
├── reports/
│
├── requirements.txt
└── README.md
```

## 10. Installation and Execution

### Prerequisites

- Python 3.11 or compatible version.
- PostgreSQL.
- Git.
- Visual Studio Code (recommended).

### Clone the repository

```bash
git clone <YOUR_GITHUB_REPOSITORY_URL>
cd pharmaceutical-supply-chain-intelligence
```

### Create and activate a virtual environment

```bash
python3.11 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Create the database

Create a PostgreSQL database named:

```sql
CREATE DATABASE pharma_intelligence;
```

### Generate synthetic data

```bash
python src/generate_data.py
```

### Create the database schema

```bash
psql -v ON_ERROR_STOP=1 -d pharma_intelligence -f sql/schema.sql
```

### Run the ETL pipeline

```bash
python src/clean_load.py
```

### Explore the data

Open `notebooks/01_data_exploration.ipynb` in Jupyter or VS Code and select the project virtual environment as the kernel.

Run the notebook cells in order.

### Launch the dashboard

```bash
streamlit run dashboard/app.py
```

Open:

```text
http://localhost:8501
```

## 11. Limitations and Future Improvements

This prototype has several limitations:

- The dataset is synthetic and does not represent actual pharmaceutical supply chain activity.
- Verification outcomes are generated probabilistically and are not fully reconciled with batch expiry dates.
- Country-centre coordinates are approximations and cannot establish actual travel distances.
- Isolation Forest performance has not been validated against a labelled real-world dataset.
- Detection thresholds are experimental and require calibration.
- An anomaly flag indicates an unusual pattern, not confirmed fraud.

Potential future improvements include:

- Integration with validated real-world datasets.
- More precise geographical coordinates.
- Temporal anomaly detection.
- Model evaluation using labelled test data.
- Automated investigation alerts.
- More comprehensive SQL analytics.
- Improved monitoring of batches and product expiry.

## 12. Disclaimer

This project is an independent educational and portfolio prototype. It is not affiliated with EMVO, CTDI or any pharmaceutical verification authority. It does not process real patient information or confidential pharmaceutical verification records.

---

**Author:** Worlasi Odei Fianko

**Project:** Pharmaceutical Supply Chain Intelligence System

**Purpose:** Data Engineering, Analytics and Anomaly Detection Portfolio Project
