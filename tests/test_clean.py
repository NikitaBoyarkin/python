import pandas as pd
import pytest

from python_analytics.clean import clean_missing, coerce_types, deduplicate


def test_clean_missing_drop():
    df = pd.DataFrame({"a": [1, None, 3]})
    assert len(clean_missing(df, strategy="drop")) == 2


def test_clean_missing_fill():
    df = pd.DataFrame({"a": [1.0, None, 3.0]})
    result = clean_missing(df, strategy="fill")
    assert result["a"].isna().sum() == 0
    assert result["a"].iloc[1] == 2.0  # медиана


def test_clean_missing_unknown_strategy():
    with pytest.raises(ValueError):
        clean_missing(pd.DataFrame({"a": [1, 2]}), strategy="bogus")


def test_deduplicate():
    df = pd.DataFrame({"a": [1, 1, 2]})
    assert len(deduplicate(df)) == 2


def test_coerce_types():
    df = pd.DataFrame({"age": ["1", "2"]})
    assert coerce_types(df, {"age": "int64"})["age"].dtype == "int64"


def test_coerce_types_missing_column():
    with pytest.raises(KeyError):
        coerce_types(pd.DataFrame({"age": [1, 2]}), {"nope": "int64"})


def test_functions_do_not_mutate_input():
    df = pd.DataFrame({"a": [1, None, 1, 3]})
    original = df.copy()
    clean_missing(df, strategy="drop")
    deduplicate(df)
    coerce_types(df, {"a": "float64"})
    pd.testing.assert_frame_equal(df, original)
