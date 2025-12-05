# CSV Duplicate Counter

A Python script that counts the frequency of values in a CSV column and exports the results.

## What It Does

- Reads a CSV file
- Counts how many times each unique value appears in a specified column
- Displays the frequency counts
- Saves the results to a new CSV file

## Requirements

```
pandas
```

## Usage

1. Open `main.py` and update the following:

   | Placeholder | Replace With |
   |-------------|--------------|
   | `"path of file.csv"` | Path to your input CSV |
   | `"Column name"` | The column to count duplicates in |
   | `"path where to save csv\name for file.csv"` | Path for the output CSV |

2. Run the script:
   ```bash
   python main.py
   ```

## Example Output

If your CSV has a "City" column with repeated values:

```
City
New York    15
Chicago      8
Boston       3
```
