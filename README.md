# Customer Support Data Pipeline

## Overview

This project demonstrates a simple ETL pipeline built in Python.

The goal is to transform raw customer support data into structured tables
that can be used for analysis.

## Architecture

raw CSV → transformation → star schema → SQLite → analytical queries

## Technologies

- Python
- Pandas
- SQLite

## Pipeline Steps

- Load raw CSV data
- Clean and standardize column names
- Convert data types
- Build dimension and fact tables
- Store data in SQLite database

## Data Model

This project uses a simple star schema:

```
orders
│
│ order_id
│
calls
│
│ agent_id
│
agents
```

- **orders** – contains order info like `order_id`, `product_category`, `item_price`, `order_date_time`, `customer_city`  
- **agents** – contains agent info like `agent_id`, `agent_name`, `supervisor`, `manager`, `tenure_bucket`  
- **calls** – contains all call interactions, links to `orders` and `agents`

## Example Analysis

The project includes SQL-based analysis, for example:
- Distribution of customer satisfaction scores (CSAT)
- Percentage of calls with customer feedback
- Aggregations based on call and agent data

## What I learned

- How to design a simple ETL pipeline in Python
- Data cleaning and standardization using pandas
- Building a basic star schema (fact and dimension tables)
- Working with SQLite as a lightweight data warehouse
- Writing SQL queries for analytical use cases

## Future Improvements

- Add data validation (e.g. Great Expectations)
- Containerize pipeline using Docker
- Schedule pipeline using Airflow
- Replace SQLite with a cloud data warehouse (e.g. BigQuery)
- Improve logging and error handling

## Setup

Install dependencies:
```
pip install -r requirements.txt
```

Run ETL pipeline:
```
python src/main.py
```

Run analysis:
```
python src/analysis.py
```
