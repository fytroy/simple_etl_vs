import pytest
import transform

def test_transform_rows_basic():
    rows = [
        {"a": " 1 ", "b": "2.5", "c": "text"},
        {"a": "", "b": None, "c": "  cleaned  "}
    ]
    expected = [
        {"a": 1, "b": 2.5, "c": "text"},
        {"a": None, "b": None, "c": "cleaned"}
    ]
    result = transform.transform_rows(rows)
    assert result == expected

def test_transform_rows_integers():
    rows = [{"val": "123"}, {"val": "-5"}]
    result = transform.transform_rows(rows)
    assert result[0]["val"] == 123
    assert result[1]["val"] == -5

def test_transform_rows_floats():
    rows = [{"val": "1.23"}, {"val": "-5.67"}, {"val": "1e-5"}]
    result = transform.transform_rows(rows)
    assert result[0]["val"] == 1.23
    assert result[1]["val"] == -5.67
    assert result[2]["val"] == 1e-5

def test_transform_rows_mixed_types():
    rows = [{"val": "123"}, {"val": "abc"}, {"val": "12.34"}]
    result = transform.transform_rows(rows)
    assert result[0]["val"] == 123
    assert result[1]["val"] == "abc"
    assert result[2]["val"] == 12.34

def test_transform_rows_none_handling():
    rows = [{"val": None}]
    result = transform.transform_rows(rows)
    assert result[0]["val"] is None

def test_transform_rows_empty_string_handling():
    rows = [{"val": ""}, {"val": "   "}]
    result = transform.transform_rows(rows)
    assert result[0]["val"] is None
    assert result[1]["val"] is None
