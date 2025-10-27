# CSV Reader

Simple CLI helper that uses pandas to read a delimited file and dump the resulting DataFrame.

## Setup

1. Create a virtual environment (optional but recommended):
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

```
python csv_reader.py --file_path data.csv -d ';'
```

- `--file_path` (required): path to the CSV/TSV/etc file.
- `-d/--delimiter` (optional): delimiter character, defaults to comma.

## Troubleshooting

If you see `ModuleNotFoundError: No module named 'pandas'`, double-check that your virtual environment is active and that you ran `pip install -r requirements.txt`. For missing input files, the script reports `Error: File not found` and exits with a non-zero status so you can catch it in automated scripts.
