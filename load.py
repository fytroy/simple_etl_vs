"""Loading utilities for SQL Server using pyodbc."""
from typing import List, Dict, Any
import pyodbc


def _quote_identifier(name: str) -> str:
    return f"[{name.replace(']', ']]')}]"


def _quote_full_name(name: str) -> str:
    # support schema.table by quoting each part
    parts = name.split('.')
    return '.'.join(_quote_identifier(p) for p in parts)


def create_table_from_rows(conn: pyodbc.Connection, table: str, rows: List[Dict[str, Any]]):
    """Create a simple table where all columns are NVARCHAR(MAX) to accept incoming data."""
    if not rows:
        raise ValueError("No rows to infer schema from")
    cols = list(rows[0].keys())
    col_defs = ", ".join(f"{_quote_identifier(c)} NVARCHAR(MAX)" for c in cols)
    quoted_table = _quote_full_name(table)
    sql = f"IF OBJECT_ID(N'{table}', N'U') IS NOT NULL DROP TABLE {quoted_table}; CREATE TABLE {quoted_table} ({col_defs});"
    with conn.cursor() as cur:
        cur.execute(sql)
        conn.commit()


def load_to_sqlserver(rows: List[Dict[str, Any]], table: str, conn_str: str):
    """Insert rows into SQL Server table. Creates table (dropping if exists) then bulk inserts.

    All columns are stored as NVARCHAR(MAX) by default to keep type mapping simple.
    """
    if not rows:
        return 0

    conn = pyodbc.connect(conn_str, autocommit=False)
    try:
        create_table_from_rows(conn, table, rows)
        cols = list(rows[0].keys())
        col_list = ", ".join(_quote_identifier(c) for c in cols)
        placeholders = ", ".join("?" for _ in cols)
        quoted_table = _quote_full_name(table)
        insert_sql = f"INSERT INTO {quoted_table} ({col_list}) VALUES ({placeholders})"

        values = [[str(row.get(c)) if row.get(c) is not None else None for c in cols] for row in rows]

        cur = conn.cursor()
        cur.fast_executemany = True
        cur.executemany(insert_sql, values)
        conn.commit()
        return cur.rowcount
    finally:
        conn.close()
