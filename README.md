# freq-checker (CSV Duplicate Counter)

A Python script that counts the frequency of values in a CSV column and exports the results.

## What It Does

- Reads a CSV file
- Counts how many times each unique value appears in a specified column
- Displays the frequency counts
- Saves the results to a new CSV file

## Usage

Run the script from the command line:

```bash
python main.py "path/to/file.csv" "Column name"
```

Optional arguments:
- `-o`, `--output`: Path to save the output CSV.

Example:
```bash
python main.py data.csv "Email" -o duplicates.csv
```

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Example Output

If your CSV has a "City" column with repeated values:

```
City
New York    15
Chicago      8
Boston       3
```
