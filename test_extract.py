import pytest
import extract
import tempfile
import os

def test_extract_csv_basic():
    csv_content = "col1,col2\nval1,val2\nval3,val4"
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        rows = extract.extract_csv(tmp_path)
        assert len(rows) == 2
        assert rows[0] == {"col1": "val1", "col2": "val2"}
        assert rows[1] == {"col1": "val3", "col2": "val4"}
    finally:
        os.remove(tmp_path)

def test_extract_csv_empty():
    csv_content = ""
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        rows = extract.extract_csv(tmp_path)
        assert len(rows) == 0
    finally:
        os.remove(tmp_path)

def test_extract_csv_header_only():
    csv_content = "col1,col2\n"
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        rows = extract.extract_csv(tmp_path)
        assert len(rows) == 0
    finally:
        os.remove(tmp_path)

def test_extract_csv_with_quoting():
    csv_content = 'id,desc\n1,"Hello, World"'
    with tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".csv") as tmp:
        tmp.write(csv_content)
        tmp_path = tmp.name

    try:
        rows = extract.extract_csv(tmp_path)
        assert len(rows) == 1
        assert rows[0]["desc"] == "Hello, World"
    finally:
        os.remove(tmp_path)

def test_extract_csv_file_not_found():
    with pytest.raises(FileNotFoundError):
        extract.extract_csv("non_existent_file.csv")
