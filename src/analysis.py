import sqlite3
import pandas as pd

DB_PATH = "../customer_contact.db"

# Distribution of customer satisfaction scores
query_csat_distribution = """
SELECT
    csat_score,
    COUNT(*) AS total_calls
FROM calls
GROUP BY csat_score
ORDER BY csat_score
"""

# Percentage of calls with customer feedback
query_feedback = """
SELECT
    COUNT(*) AS total_calls,
    SUM(CASE WHEN customer_remarks IS NOT NULL THEN 1 ELSE 0 END) AS feedback_calls,
    ROUND(100.0 * SUM(CASE WHEN customer_remarks IS NOT NULL THEN 1 ELSE 0 END) / COUNT(*), 1) AS feedback_pct
FROM calls
"""

# Average CSAT per agent
query_agent_performance = """
SELECT
    agent_id,
    AVG(csat_score) AS avg_csat,
    COUNT(*) AS total_calls
FROM calls
GROUP BY agent_id
ORDER BY avg_csat DESC
"""


def main():
    conn = sqlite3.connect(DB_PATH)

    queries = {
        "CSAT Distribution": query_csat_distribution,
        "Feedback Percentage": query_feedback,
        "Agent Performance": query_agent_performance
    }

    for name, query in queries.items():
        print(f"\n--- {name} ---")
        df = pd.read_sql_query(query, conn)
        print(df)

    conn.close()


if __name__ == "__main__":
    main()
