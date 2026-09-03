import pandas as pd
import pytest

from python_analytics.load import load_csv


def test_load_csv_returns_dataframe(tmp_path):
    path = tmp_path / "data.csv"
    path.write_text("a,b\n1,2\n3,4\n", encoding="utf-8")
    df = load_csv(path)
    assert isinstance(df, pd.DataFrame)
    assert df.shape == (2, 2)


def test_load_csv_missing_file_raises(tmp_path):
    with pytest.raises(FileNotFoundError):
        load_csv(tmp_path / "nope.csv")


def test_load_csv_empty_file_raises(tmp_path):
    path = tmp_path / "empty.csv"
    path.write_text("", encoding="utf-8")
    with pytest.raises(ValueError):
        load_csv(path)


def test_load_csv_cp1251_encoding(tmp_path):
    path = tmp_path / "data.csv"
    path.write_bytes("имя,возраст\nАнна,30\n".encode("cp1251"))
    df = load_csv(path, encoding="cp1251")
    assert df.loc[0, "имя"] == "Анна"
