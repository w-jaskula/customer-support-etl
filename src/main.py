import pandas as pd
import sqlite3
import logging

logging.basicConfig(level=logging.INFO, format="%(levelname)s:%(message)s")


def load_data(path):
    logging.info(f"Loading data from {path}")
    return pd.read_csv(path)


def transform_data(df):
    logging.info("Standardizing column names")
    df = df.rename(columns={
        "Unique id": "call_id",
        "Sub-category": "sub_category",
        "Customer Remarks": "customer_remarks",
        "Order_id": "order_id",
        "Issue_reported at": "issue_reported_at",
        "Survey_response_Date": "survey_response_date",
        "Customer_City": "customer_city",
        "Product_category": "product_category",
        "Item_price": "item_price",
        "Agent_name": "agent_name",
        "Supervisor": "supervisor",
        "Manager": "manager",
        "Tenure Bucket": "tenure_bucket",
        "Agent Shift": "agent_shift",
        "CSAT Score": "csat_score"
    })

    # Convert date/time
    for col in ["order_date_time", "issue_reported_at", "issue_responded"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format="%d/%m/%Y %H:%M", errors="coerce")

    df["survey_response_date"] = pd.to_datetime(df["survey_response_date"], format="%d-%b-%y", errors="coerce")
    df["item_price"] = pd.to_numeric(df["item_price"], errors="coerce")
    df["connected_handling_time"] = pd.to_numeric(df["connected_handling_time"], errors="coerce")
    df["csat_score"] = pd.to_numeric(df["csat_score"], errors="coerce")

    return df


def build_tables(df):
    logging.info("Building dimension and fact tables")

    orders_df = df[["order_id", "product_category", "item_price", "order_date_time", "customer_city"]].drop_duplicates(
        subset=["order_id"])

    agents_df = df[["agent_name", "supervisor", "manager", "tenure_bucket"]].drop_duplicates(
        subset=["agent_name", "supervisor", "manager", "tenure_bucket"])
    agents_df = agents_df.reset_index(drop=True)
    agents_df["agent_id"] = agents_df.index + 1
    agents_df = agents_df[["agent_id", "agent_name", "supervisor", "manager", "tenure_bucket"]]

    calls_df = df[[
        "call_id", "category", "sub_category", "issue_reported_at",
        "order_id", "customer_remarks", "survey_response_date", "csat_score",
        "issue_responded", "connected_handling_time", "agent_shift",
        "channel_name", "agent_name"
    ]].drop_duplicates(subset=["call_id"])

    calls_df = calls_df.merge(agents_df[["agent_name", "agent_id"]], on="agent_name", how="left")

    return orders_df, agents_df, calls_df


def save_to_db(orders_df, agents_df, calls_df, db_path="../customer_contact.db"):
    logging.info(f"Saving tables to {db_path}")
    conn = sqlite3.connect(db_path)
    orders_df.to_sql("orders", conn, if_exists="replace", index=False)
    agents_df.to_sql("agents", conn, if_exists="replace", index=False)
    calls_df.to_sql("calls", conn, if_exists="replace", index=False)
    conn.close()
    logging.info("Database saved successfully")


def main():
    df = load_data("../data/customer_data.csv")
    df = transform_data(df)
    orders_df, agents_df, calls_df = build_tables(df)
    save_to_db(orders_df, agents_df, calls_df)


if __name__ == "__main__":
    main()