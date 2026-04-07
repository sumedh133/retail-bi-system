# 🛒 Retail Sales Intelligence System
> A full Business Intelligence ecosystem — ETL pipeline, PostgreSQL data warehouse, Metabase dashboards, and ML analytics.

---

## 📁 Repository Structure

```
retail-bi-system/
├── etl/
│   ├── extract.py          # Load raw CSVs
│   ├── transform.py        # Clean & derive fields (revenue, month, year)
│   └── load.py             # Push to PostgreSQL
├── sql/
│   ├── schema.sql          # Star schema DDL (fact + dimension tables)
│   └── analytics/
│       ├── revenue_by_region.sql
│       ├── monthly_trends.sql
│       ├── top_customers.sql
│       └── product_performance.sql
├── ml/
│   ├── clustering.ipynb    # K-Means customer segmentation
│   └── forecasting.ipynb   # Sales trend forecasting
├── data/
│   └── raw/                # Raw CSV files (Sales, Customers, Products)
├── docker-compose.yml      # PostgreSQL + Metabase
├── pyproject.toml          # Python dependencies (uv)
├── .env.example            # Environment variable template
└── README.md
```

---

## 🏗️ System Architecture

```
Raw CSVs (data/raw/)
       ↓
ETL Pipeline (Python + Pandas)
       ↓
PostgreSQL — Star Schema (Docker on Compute engine)
       ↓
Metabase Dashboards (Docker on Compute engine)

+

ML Notebooks (run locally, pushed to GitHub)
```

---

## ⚙️ Prerequisites

### On EC2
- Docker
- Docker Compose

### Locally
- Python 3.9+
- [uv](https://docs.astral.sh/uv/) — install with `curl -Ls https://astral.sh/uv/install.sh | sh`
- Jupyter Notebook (for ML)

---

## 🚀 Setup & Running From Scratch

### 1. Clone the repository
```bash
git clone https://github.com/yourteam/retail-bi-system.git
cd retail-bi-system
```

### 2. Configure environment variables
```bash
cp .env.example .env
```
Open `.env` and fill in your values:

### 3. Start infrastructure (run on EC2)
```bash
docker-compose up -d
```
This starts:
- PostgreSQL on port `5432`
- Metabase on port `3000`

### 4. Initialize the database schema
```bash
psql -h your-ec2-ip -U admin -d retail_dw -f sql/schema.sql
```

### 5. Install Python dependencies
```bash
uv sync
```
This reads `pyproject.toml`, creates a virtual environment, and installs everything automatically.

### 6. Run the ETL pipeline
```bash
python etl/extract.py
python etl/transform.py
python etl/load.py
```

### 7. Open Metabase
Go to `http://your-ec2-ip:3000` in your browser.
- Connect to PostgreSQL using your `.env` credentials
- Import or recreate dashboards

### 8. Run ML notebooks (locally)
```bash
jupyter notebook ml/clustering.ipynb
jupyter notebook ml/forecasting.ipynb
```
Notebooks connect to EC2 PostgreSQL to pull data.

---

## 🗃️ Data Warehouse Schema (Star Schema)

```
fact_sales
├── sale_id (PK)
├── customer_id (FK → dim_customer)
├── product_id  (FK → dim_product)
├── region_id   (FK → dim_region)
├── date_id     (FK → dim_date)
├── quantity
└── revenue

dim_customer    dim_product     dim_region      dim_date
───────────     ───────────     ──────────      ────────
customer_id     product_id      region_id       date_id
name            name            name            date
segment         category        country         month
region          sub_category                    year
                                                quarter
```

---

## 📊 Dashboards (Metabase)

| Dashboard | Description |
|---|---|
| Sales Overview | Total revenue, trends over time |
| Customer Insights | Top customers, segmentation |
| Product Performance | Best-selling products by category |
| Regional Analysis | Revenue breakdown by region |
| Time Trends | Monthly and yearly growth |

---

## 🤖 ML Models

### Customer Segmentation (`clustering.ipynb`)
- Algorithm: K-Means Clustering
- Features: purchase frequency, total spend, recency
- Output: customer segments (high/mid/low value)

### Sales Forecasting (`forecasting.ipynb`)
- Algorithm: ARIMA / statsmodels
- Input: monthly revenue time series
- Output: next 3–6 month sales prediction

---

## 💡 Business Insights
- Identify high-performing regions and replicate strategies
- Detect declining product categories early
- Target high-value customer segments for retention campaigns
- Forecast revenue for inventory and budget planning

---

## 🐳 Docker Services

| Service | Port | Description |
|---|---|---|
| PostgreSQL | 5432 | Data warehouse |
| Metabase | 3000 | BI dashboards |

> Make sure ports **5432** and **3000** are open in your EC2 Security Group.

---

## 👥 Team

| Member | Responsibility |
|---|---|
| Member 1 | EC2 setup, Docker, ETL pipeline |
| Member 2 | Star schema design, SQL analytics |
| Member 3 | Metabase dashboards, ML models |

---

## 📦 Dependencies

Managed via `pyproject.toml` using [uv](https://docs.astral.sh/uv/).

```
pandas
sqlalchemy
psycopg2-binary
scikit-learn
statsmodels
jupyter
python-dotenv
```

To install everything:
```bash
uv sync
```

To add a new package:
```bash
uv add <package-name>
```

---

## ⚠️ Notes
- Never commit your `.env` file — it's in `.gitignore`
- Use `.env.example` as a template for teammates
- Postgres data is persisted via Docker volume — container restarts won't wipe the database
- ML notebooks require a live connection to EC2 PostgreSQL to fetch data