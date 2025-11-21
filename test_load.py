import sys
from unittest.mock import MagicMock

# Mock pyodbc before importing load
sys.modules["pyodbc"] = MagicMock()

import pytest
from unittest.mock import MagicMock, patch
import load

def test_quote_identifier():
    assert load._quote_identifier("col") == "[col]"
    assert load._quote_identifier("col]name") == "[col]]name]"

def test_quote_full_name():
    assert load._quote_full_name("table") == "[table]"
    assert load._quote_full_name("schema.table") == "[schema].[table]"

def test_create_table_from_rows():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    mock_conn.cursor.return_value.__enter__.return_value = mock_cursor

    rows = [{"col1": "val1", "col2": 123}]
    load.create_table_from_rows(mock_conn, "mytable", rows)

    mock_cursor.execute.assert_called_once()
    sql = mock_cursor.execute.call_args[0][0]
    assert "CREATE TABLE [mytable]" in sql
    assert "[col1] NVARCHAR(MAX)" in sql
    assert "[col2] NVARCHAR(MAX)" in sql

def test_load_to_sqlserver_empty():
    # We need to mock load.pyodbc because it was imported inside load.py
    # Actually, since we mocked sys.modules['pyodbc'], load.pyodbc IS that mock

    rows = []
    result = load.load_to_sqlserver(rows, "mytable", "conn_str")
    assert result == 0
    load.pyodbc.connect.assert_not_called()

def test_load_to_sqlserver_success():
    mock_conn = MagicMock()
    mock_cursor = MagicMock()
    load.pyodbc.connect.return_value = mock_conn
    mock_conn.cursor.return_value = mock_cursor
    mock_cursor.rowcount = 10

    rows = [{"col1": "val1"}, {"col1": "val2"}]
    result = load.load_to_sqlserver(rows, "mytable", "conn_str")

    assert result == 10
    load.pyodbc.connect.assert_called_with("conn_str", autocommit=False)

    assert mock_cursor.executemany.called
    args = mock_cursor.executemany.call_args
    sql = args[0][0]
    values = args[0][1]

    assert "INSERT INTO [mytable]" in sql
    assert len(values) == 2
    assert values[0] == ["val1"]
    assert values[1] == ["val2"]
