"""Script to find and export duplicate values from a CSV file."""
import argparse

import pandas as pd


def find_duplicates(input_path: str, column: str, output_path: str | None = None) -> pd.DataFrame:
    """Find values that appear more than once in the specified column."""
    df = pd.read_csv(input_path)

    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")

    # Count occurrences and filter to only duplicates (count > 1)
    counts = df[column].value_counts()
    duplicates = counts[counts > 1].reset_index()
    duplicates.columns = [column, 'count']

    print(f"Found {len(duplicates)} values with duplicates:")
    print(duplicates.to_string(index=False))

    if output_path:
        duplicates.to_csv(output_path, index=False)
        print(f"\nSaved to: {output_path}")

    return duplicates


def main():
    parser = argparse.ArgumentParser(description="Find duplicate values in a CSV column")
    parser.add_argument("input", help="Path to input CSV file")
    parser.add_argument("column", help="Column name to check for duplicates")
    parser.add_argument("-o", "--output", help="Path to save results (optional)")

    args = parser.parse_args()

    try:
        find_duplicates(args.input, args.column, args.output)
    except FileNotFoundError:
        print(f"Error: File not found: {args.input}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
