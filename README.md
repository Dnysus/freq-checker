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

### Supported Formats
- **Input**: `.csv` and `.xlsx` (Excel)
- **Output**: `.csv`, `.xlsx`, `.png` (plot), `.html` (report)

### Options

#### 1. Basic Options
- `-o`, `--output`: Path to save the results.
- `--ignore-case`: Treat "Apple" and "apple" as duplicates.
- `--trim`: Treat " Apple " and "Apple" as duplicates.

#### 2. Advanced Matching
- `--fuzzy`: Find similar strings (e.g., "John Doe" vs "Jon Doe").
  - `--threshold <0-100>`: Set similarity threshold (default: 90).
- `--phonetic`: Find similarly sounding strings (e.g., "Smith" vs "Smyth").

#### 3. Reporting & Visualization
- `--plot`: Generate a bar chart of top duplicates (saved as `.png` if output path provided).
- `--report`: Generate a detailed HTML report (saved as `.html` if output path provided).

### Examples

**Exact Match (Cleaned):**
```bash
python main.py data.csv "Email" --ignore-case --trim -o results.csv
```

**Fuzzy Match (Typos):**
```bash
python main.py data.xlsx "Name" --fuzzy --threshold 85 -o fuzzy_results.xlsx
```

**Phonetic Match (Sound-alike):**
```bash
python main.py data.csv "LastName" --phonetic -o phonetic.csv
```

**Full Report (Excel + HTML Report + Plot):**
```bash
python main.py data.xlsx "City" --report --plot -o analysis.xlsx
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
