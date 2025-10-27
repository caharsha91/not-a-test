import pathlib

import pandas as pd
from pandas.testing import assert_frame_equal

from csv_reader import read_csv_with_delimiter


def test_read_csv_with_delimiter_success():
  repo_root = pathlib.Path(__file__).resolve().parents[1]
  df = read_csv_with_delimiter(repo_root / "data.csv", delimiter=";")
  expected = pd.DataFrame(
    [
      {"name": "Alice", "age": 30, "city": "New York"},
      {"name": "Bob", "age": 25, "city": "Los Angeles"},
    ]
  )

  assert_frame_equal(df.reset_index(drop=True), expected)


def test_read_csv_with_delimiter_missing_file(tmp_path):
  missing_file = tmp_path / "missing.csv"
  result = read_csv_with_delimiter(missing_file, delimiter=";")
  assert result is None
