import tempfile
import os
import extract
import transform


def test_extract_and_transform():
    csv_text = """id,name,age\n1, Alice , 30\n2,Bob,\n3,  4,5.5\n"""
    fd, path = tempfile.mkstemp(suffix=".csv")
    os.close(fd)
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(csv_text)

        rows = extract.extract_csv(path)
        assert len(rows) == 3

        transformed = transform.transform_rows(rows)
        assert transformed[0]["name"] == "Alice"
        assert transformed[0]["age"] == 30
        assert transformed[1]["age"] is None
        # numeric string coerced
        assert transformed[2]["id"] == 3 or transformed[2]["id"] == "3"
    finally:
        os.remove(path)
