"""Tests for the writio module.
"""
import pandas as pd
from pandas.testing import assert_frame_equal

from writio import load, dump


def test_yaml(data, tmp_path):
    yaml_d = load(data / "test.yaml")
    json_d = load(data / "test.json")
    assert yaml_d == json_d
    dump(yaml_d, tmp_path / "test.json")
    dump(json_d, tmp_path / "test.yaml")
    assert load(tmp_path / "test.yaml") == load(tmp_path / "test.json")


def test_pandas(data, tmp_path):
    csv_df = load(data / "test.csv")
    tsv_df = load(data / "test.tsv")
    assert_frame_equal(csv_df, tsv_df)
    csv_dict = load(data / "test.csv", mode="csv2dict")
    assert list(csv_dict.keys()) == ["rec1", "rec2"]
    dump(csv_dict, tmp_path / "test2.csv")
    print(tsv_df, load(tmp_path / "test2.csv"))
    assert_frame_equal(tsv_df, load(tmp_path / "test2.csv"))


def test_index(data, tmp_path):
    df = load(data / "test.csv", index_col="id")
    assert df.index.name == "id"
    dump(df, tmp_path / "t.csv", index=True)
    dump(df, tmp_path / "t1.tsv")
    assert_frame_equal(load(tmp_path / "t.csv", index_col="id"), df)
    assert "id" not in load(tmp_path / "t1.tsv").columns


def test_rec(data, tmp_path):
    df = load(data / "test.csv")
    dump(df, tmp_path / "test.yaml")
    recs = load(tmp_path / "test.yaml")
    assert_frame_equal(df, pd.DataFrame.from_dict(recs))
    dump(recs, tmp_path / "test2.csv")
    assert_frame_equal(df, load(tmp_path / "test2.csv"))


def test_raw(data, tmp_path):
    d = load(data / "test.txt")
    assert d == "Plain text."
    dump(d, tmp_path / "t.txt")
    assert load(tmp_path / "t.txt") == d


def test_none(data):
    assert load(data / "none.txt") is None
