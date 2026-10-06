from sqlalchemy import inspect

from src.database.connection import engine


def get_database_schema():
    inspector = inspect(engine)

    schema = {}

    tables = inspector.get_table_names()

    for table in tables:
        columns = inspector.get_columns(table)
        foreign_keys = inspector.get_foreign_keys(table)

        schema[table] = {
            "columns": [
                column["name"]
                for column in columns
            ],
            "foreign_keys": [
                {
                    "column": foreign_key["constrained_columns"],
                    "references_table": foreign_key["referred_table"],
                    "references_column": foreign_key["referred_columns"],
                }
                for foreign_key in foreign_keys
            ],
        }

    return schema


def format_schema_for_rag(schema):
    formatted_schema = []

    for table, details in schema.items():
        text = f"Table: {table}\n"
        text += f"Columns: {', '.join(details['columns'])}\n"

        for foreign_key in details["foreign_keys"]:
            text += (
                f"Relationship: {foreign_key['column'][0]} → "
                f"{foreign_key['references_table']}."
                f"{foreign_key['references_column'][0]}\n"
            )

        formatted_schema.append(text)

    return "\n".join(formatted_schema)