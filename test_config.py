import pytest
import config
import os

def test_build_conn_str_defaults():
    # Ensure no env vars interfere
    env_vars = ["SQLSERVER_HOST", "SQLSERVER_DB", "SQLSERVER_UID", "SQLSERVER_PWD", "SQLSERVER_DRIVER"]
    old_env = {}
    for var in env_vars:
        if var in os.environ:
            old_env[var] = os.environ[var]
            del os.environ[var]

    try:
        conn_str = config.build_conn_str()
        assert "SERVER=localhost" in conn_str
        assert "DATABASE=master" in conn_str
        assert "Trusted_Connection=yes" in conn_str
        assert "DRIVER={ODBC Driver 18 for SQL Server}" in conn_str
    finally:
        for var, val in old_env.items():
            os.environ[var] = val

def test_build_conn_str_params():
    conn_str = config.build_conn_str(server="myserver", database="mydb", uid="user", pwd="pass")
    assert "SERVER=myserver" in conn_str
    assert "DATABASE=mydb" in conn_str
    assert "UID=user" in conn_str
    assert "PWD=pass" in conn_str
    assert "Trusted_Connection=yes" not in conn_str

def test_build_conn_str_env_vars():
    os.environ["SQLSERVER_HOST"] = "envserver"
    os.environ["SQLSERVER_DB"] = "envdb"
    os.environ["SQLSERVER_UID"] = "envuser"
    os.environ["SQLSERVER_PWD"] = "envpass"
    os.environ["SQLSERVER_DRIVER"] = "SQL Server Native Client 11.0"

    try:
        conn_str = config.build_conn_str()
        assert "SERVER=envserver" in conn_str
        assert "DATABASE=envdb" in conn_str
        assert "UID=envuser" in conn_str
        assert "PWD=envpass" in conn_str
        assert "DRIVER={SQL Server Native Client 11.0}" in conn_str
    finally:
         del os.environ["SQLSERVER_HOST"]
         del os.environ["SQLSERVER_DB"]
         del os.environ["SQLSERVER_UID"]
         del os.environ["SQLSERVER_PWD"]
         del os.environ["SQLSERVER_DRIVER"]
