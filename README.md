# Analytical Pipeline

This project implements a small analytical pipeline that ingests data from CSV, JSON, and Excel, cleans and validates it, transforms and enriches it using pandas, and performs analytical questions using SQL.

## Folder Structure

```
── data/                   # Input data files
       ── customers.csv
       ── orders.json
       ── payments.xlsx
── src/                    # Source code
      ── __init__.py
      ── ingestion.py      # Data loading logic
      ── cleaning.py       # Data cleaning and validation
      ── transformation.py # Merging, aggregation, and pivoting
      ── run_sqlite.py     # SQLite execution and querying
      ── sql_analysis.sql  # SQL queries (reference)
      ── main.py           # Orchestration script
── outputs/                # Cleaned data and final datasets
      ── customers_clean.csv
      ── orders_clean.csv
      ── payments_clean.csv
      ── final_fact_orders.csv
      ── analysis.db       # SQLite database
      ── aggregates/       # Aggregated CSV reports
            ── revenue_by_country.csv
            ── avg_order_value_by_customer.csv
            ── monthly_revenue_trend.csv
            ── pivot_revenue_country_status.csv
── README.md
── requirements.txt
```

## Setup and Run

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Pipeline**:
    ```bash
    python src/main.py
    ```

## Approach & Assumptions

### Part 1: Ingestion
- Loaded data using `pandas`.
- Handled potential encoding issues (tried `utf-8` then `latin1`).
- Converted date columns to datetime objects immediately after loading.

### Part 2: Cleaning
- **Customers**: 
  - Standardized country names to Title Case.
  - Filled missing emails with 'MISSING'.
  - Removed duplicate customer records.
- **Orders**: 
  - Flagged invalid amounts (<= 0).
  - Identified outliers using IQR method.
  - Normalized status to Title Case.
- **Payments**: 
  - Removed duplicate payment records.

### Part 3: Transformation
- Left joined Orders with Customers and Payments to create a master `final_fact_orders` dataset.
- Calculated `payment_delay_days`.
- Determined `is_fully_paid` by comparing `paid_amount` vs `amount`.
- Created aggregations for revenue and order values.

### Part 4: SQL Analysis
- Loaded cleaned dataframes into a SQLite database (`outputs/analysis.db`).
- Executed SQL queries to answer business questions (Top customers, Unpaid orders by country, etc.).


