import sqlite3
import pandas as pd

DB_PATH = "../customer_contact.db"

def main():
    conn = sqlite3.connect(DB_PATH)

    # Count call with feedback vs no feedback
    query = """
    SELECT
        csat_score,
        COUNT(*) AS total_calls,
        SUM(CASE WHEN customer_remarks IS NOT NULL THEN 1 ELSE 0 END) AS feedback_calls,
        SUM(CASE WHEN customer_remarks IS NULL THEN 1 ELSE 0 END) AS no_feedback_calls,
        ROUND(100.0 * SUM(CASE WHEN customer_remarks IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS feedback_pct
    FROM calls
    GROUP BY csat_score
    ORDER BY csat_score
    """

    df = pd.read_sql_query(query, conn)
    conn.close()

    print(df)

if __name__ == "__main__":
    main()