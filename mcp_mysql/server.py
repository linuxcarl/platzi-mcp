import json
import os
import re

import pymysql
import pymysql.cursors
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv()

mcp = FastMCP("MySQL")


def get_connection():
    """Create a MySQL connection using environment variables."""
    return pymysql.connect(
        host=os.getenv("MYSQL_HOST", "localhost"),
        port=int(os.getenv("MYSQL_PORT", "3306")),
        user=os.getenv("MYSQL_USER", "root"),
        password=os.getenv("MYSQL_PASSWORD", ""),
        database=os.getenv("MYSQL_DATABASE", "testdb"),
        cursorclass=pymysql.cursors.DictCursor,
        read_timeout=30,
    )


def is_read_only(sql: str) -> bool:
    """Check if a SQL statement is read-only."""
    first_word = sql.strip().split()[0].upper() if sql.strip() else ""
    return first_word in ("SELECT", "SHOW", "DESCRIBE", "EXPLAIN")


@mcp.resource("schema://tables")
def get_schema() -> str:
    """List all tables and their columns in the database."""
    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SHOW TABLES")
            tables = [list(row.values())[0] for row in cursor.fetchall()]

            schema = {}
            for table in tables:
                cursor.execute(f"DESCRIBE `{table}`")
                schema[table] = cursor.fetchall()

        return json.dumps(schema, default=str)
    except pymysql.Error as e:
        return json.dumps({"error": str(e)})
    finally:
        connection.close()


@mcp.tool()
def query(sql: str) -> str:
    """Execute a SQL query against the MySQL database.

    For SELECT queries, returns the result rows as a JSON array.
    For INSERT/UPDATE/DELETE, returns the number of affected rows.
    Set MYSQL_ALLOW_WRITE=true in .env to enable write operations.
    """
    allow_write = os.getenv("MYSQL_ALLOW_WRITE", "false").lower() == "true"

    if not allow_write and not is_read_only(sql):
        return json.dumps({
            "error": "Write operations are disabled. Set MYSQL_ALLOW_WRITE=true in .env to enable."
        })

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql)

            if cursor.description:
                rows = cursor.fetchall()
                return json.dumps(rows, default=str)
            else:
                connection.commit()
                return json.dumps({"rows_affected": cursor.rowcount})
    except pymysql.Error as e:
        return json.dumps({"error": str(e)})
    finally:
        connection.close()


@mcp.tool()
def describe_table(table_name: str) -> str:
    """Get the column details for a specific table."""
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", table_name):
        return json.dumps({"error": "Invalid table name"})

    connection = get_connection()
    try:
        with connection.cursor() as cursor:
            cursor.execute(f"DESCRIBE `{table_name}`")
            rows = cursor.fetchall()
            return json.dumps(rows, default=str)
    except pymysql.Error as e:
        return json.dumps({"error": str(e)})
    finally:
        connection.close()


if __name__ == "__main__":
    mcp.run()
