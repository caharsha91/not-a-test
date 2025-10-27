import argparse
import sys

import pandas as pd

# The on_bad_lines parameter requires pandas version 1.3.0 or later.
def read_csv_with_delimiter(file_path, delimiter):
  """
  Reads a CSV file into a pandas DataFrame with a specified delimiter.

  Args:
    file_path: The path to the CSV file.
    delimiter: The delimiter to use.

  Returns:
    A pandas DataFrame, or None if an error occurs.
  """
  try:
    # It's good practice to use the `engine='python'` when using a custom delimiter
    # as the C engine doesn't support all custom delimiters.
    # The 'on_bad_lines' parameter tells pandas to 'warn' and continue processing
    # when it encounters a line with a different number of fields than expected.
    # You can also use 'skip' to ignore these lines silently.
    df = pd.read_csv(file_path, delimiter=delimiter, engine='python', on_bad_lines='warn')
    return df
  except FileNotFoundError:
    print(f"Error: File not found at {file_path}", file=sys.stderr)
    return None
  except pd.errors.ParserError as e:
    print(f"Error parsing the file: {e}", file=sys.stderr)
  except Exception as e:
    print(f"An error occurred: {e}", file=sys.stderr)
    return None

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="Read a CSV file with a specified delimiter into a pandas DataFrame.")
  parser.add_argument("--file_path", required=True, help="The path to the CSV file.")
  parser.add_argument("-d", "--delimiter", default=",", help="The delimiter used in the CSV file. Defaults to a comma.")

  args = parser.parse_args()

  dataframe = read_csv_with_delimiter(args.file_path, args.delimiter)

  if dataframe is None:
    sys.exit(1)

  print("DataFrame created successfully:")
  print(dataframe)
