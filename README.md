# Customer Support Data Pipeline

This project demonstrates a simple ETL pipeline for customer support data.

## Project Goal

Transform raw customer support data into structured tables that can be used for analysis.

## Pipeline Steps

1. Load raw CSV data
2. Clean and standardize column names
3. Convert data types
4. Build dimension and fact tables
5. Store the data in SQLite database

## Tech Stack

- Python
- Pandas
- SQLite

## Project Structure

```
customer-support-etl/
├── data/
│   └── customer_data.csv
│
├── src/
│   ├── main.py
│   └── analysis.py
│
├── requirements.txt
└── README.md
```

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

## Running the project

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