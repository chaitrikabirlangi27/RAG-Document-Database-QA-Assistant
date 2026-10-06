from src.sql_generation.generator import generate_sql
from src.database.executor import execute_query
from src.visualization.charts import create_chart
from src.visualization.chart_intent import (
    detect_chart_type,
    detect_chart_columns,
)


def validate_user_question(question):
    """
    Check whether the user is requesting a destructive
    database operation.

    This application supports read-only queries only.
    """

    question_lower = question.lower()

    destructive_keywords = [
        "delete",
        "remove",
        "erase",
        "drop",
        "truncate",
        "update",
        "modify",
        "change",
        "insert",
        "add",
        "create table",
        "alter table",
    ]

    for keyword in destructive_keywords:

        if keyword in question_lower:

            raise ValueError(
                "Only read-only database queries are supported. "
                "INSERT, UPDATE, DELETE, DROP, ALTER, and "
                "other write operations are not allowed."
            )

    return True


def run_database_query(question):

    # ====================================================
    # VALIDATE USER INTENT
    # ====================================================

    validate_user_question(question)


    # ====================================================
    # GENERATE SQL
    # ====================================================

    sql = generate_sql(question)

    # ====================================================
# HANDLE UNSUPPORTED QUESTIONS
# ====================================================

    if sql.strip() == "NOT_SUPPORTED":
        raise ValueError(
            "I could not answer this question because "
            "the required information is not available "
            "in the database schema."
        )

    # ====================================================
    # EXECUTE SQL
    # ====================================================

    dataframe = execute_query(sql)


    # ====================================================
    # DETECT CHART REQUEST
    # ====================================================

    chart = None

    chart_type = detect_chart_type(
        question
    )


    if chart_type:

        x_column, y_column = detect_chart_columns(
            dataframe
        )


        if x_column and y_column:

            chart = create_chart(
                dataframe=dataframe,
                chart_type=chart_type,
                x_column=x_column,
                y_column=y_column,
                title=question
            )


    return sql, dataframe, chart