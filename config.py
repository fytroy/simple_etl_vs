"""Configuration helpers for SQL Server connection"""
import os


def build_conn_str(server: str = None, database: str = None, uid: str = None, pwd: str = None, driver: str = None):
    """Build a pyodbc connection string. Values may be taken from env vars if not provided.

    Environment variables used if params are None:
      - SQLSERVER_HOST, SQLSERVER_DB, SQLSERVER_UID, SQLSERVER_PWD, SQLSERVER_DRIVER
    """
    server = server or os.getenv("SQLSERVER_HOST") or "localhost"
    database = database or os.getenv("SQLSERVER_DB") or "master"
    uid = uid or os.getenv("SQLSERVER_UID")
    pwd = pwd or os.getenv("SQLSERVER_PWD")
    driver = driver or os.getenv("SQLSERVER_DRIVER") or "ODBC Driver 18 for SQL Server"

    parts = [f"DRIVER={{{driver}}}", f"SERVER={server}", f"DATABASE={database}"]
    if uid is not None and pwd is not None:
        parts.append(f"UID={uid}")
        parts.append(f"PWD={pwd}")
    else:
        parts.append("Trusted_Connection=yes")

    return ";".join(parts)
