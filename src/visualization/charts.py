import plotly.express as px


def create_chart(
    dataframe,
    chart_type,
    x_column,
    y_column,
    title
):

    if dataframe.empty:
        return None

    if x_column not in dataframe.columns:
        raise ValueError(
            f"Column not found: {x_column}"
        )

    if y_column not in dataframe.columns:
        raise ValueError(
            f"Column not found: {y_column}"
        )


    if chart_type == "bar":

        figure = px.bar(
            dataframe,
            x=x_column,
            y=y_column,
            title=title
        )


    elif chart_type == "line":

        figure = px.line(
            dataframe,
            x=x_column,
            y=y_column,
            title=title,
            markers=True
        )


    elif chart_type == "pie":

        figure = px.pie(
            dataframe,
            names=x_column,
            values=y_column,
            title=title
        )


    elif chart_type == "scatter":

        figure = px.scatter(
            dataframe,
            x=x_column,
            y=y_column,
            title=title
        )


    else:

        raise ValueError(
            f"Unsupported chart type: {chart_type}"
        )


    return figure