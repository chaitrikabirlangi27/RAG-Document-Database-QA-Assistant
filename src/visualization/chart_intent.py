import pandas as pd


def detect_chart_type(question):
    question_lower = question.lower()

    if "bar chart" in question_lower or "bar graph" in question_lower:
        return "bar"

    if "pie chart" in question_lower or "pie graph" in question_lower:
        return "pie"

    if "line chart" in question_lower or "line graph" in question_lower:
        return "line"

    if "scatter plot" in question_lower or "scatter chart" in question_lower:
        return "scatter"

    return None


def detect_chart_columns(dataframe):

    if dataframe.empty or len(dataframe.columns) < 2:
        return None, None

    columns = list(dataframe.columns)

    # First column is normally the category/X-axis
    x_column = columns[0]

    # Find a column that can be converted to numeric
    for column in columns[1:]:

        numeric_values = pd.to_numeric(
            dataframe[column],
            errors="coerce"
        )

        if numeric_values.notna().any():

            dataframe[column] = numeric_values

            return x_column, column

    return None, None