import pandas as pd
from sqlalchemy import text

from src.database.connection import engine


def validate_sql(sql):
    sql_clean = sql.strip().lower()

    if not sql_clean.startswith("select"):
        raise ValueError("Only SELECT queries are allowed.")

    forbidden_keywords = [
        "insert",
        "update",
        "delete",
        "drop",
        "alter",
        "truncate",
        "create",
        "replace",
    ]

    for keyword in forbidden_keywords:
        if keyword in sql_clean:
            raise ValueError(
                f"Unsafe SQL detected: {keyword.upper()}"
            )

    return True


def execute_query(sql):
    validate_sql(sql)

    with engine.connect() as connection:
        result = connection.execute(text(sql))

        rows = result.fetchall()
        columns = result.keys()

    return pd.DataFrame(rows, columns=columns)