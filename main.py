"""Script to find and export duplicate values from a CSV file."""
import argparse
import sys
import pandas as pd
import matplotlib.pyplot as plt


def find_duplicates(
    input_path: str, 
    column: str, 
    output_path: str | None = None,
    ignore_case: bool = False,
    trim: bool = False,
    plot: bool = False
) -> pd.DataFrame:
    """Find values that appear more than once in the specified column."""
    try:
        df = pd.read_csv(input_path)
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")
        return pd.DataFrame()
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return pd.DataFrame()

    if column not in df.columns:
        print(f"Error: Column '{column}' not found. Available: {list(df.columns)}")
        return pd.DataFrame()

    # Normalize data
    series = df[column].astype(str)
    
    if trim:
        series = series.str.strip()
    
    if ignore_case:
        series = series.str.lower()

    # Count occurrences
    counts = series.value_counts()
    duplicates = counts[counts > 1].reset_index()
    duplicates.columns = [column, 'count']

    if duplicates.empty:
        print(f"No duplicates found in column '{column}'.")
        return duplicates

    print(f"Found {len(duplicates)} values with duplicates:")
    print(duplicates.to_string(index=False))

    if output_path:
        duplicates.to_csv(output_path, index=False)
        print(f"\nSaved results to: {output_path}")

    if plot:
        generate_plot(duplicates, column, output_path)

    return duplicates


def generate_plot(duplicates: pd.DataFrame, column: str, output_path: str | None):
    """Generate a bar chart of the top 10 duplicates."""
    top_10 = duplicates.head(10)
    
    plt.figure(figsize=(10, 6))
    plt.bar(top_10[column], top_10['count'], color='skyblue')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.title(f'Top 10 Duplicates in {column}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save plot if output path is provided, otherwise show it
    if output_path:
        plot_path = output_path.replace('.csv', '.png')
        if plot_path == output_path: # fallback if no extension
            plot_path += '.png'
        plt.savefig(plot_path)
        print(f"Saved plot to: {plot_path}")
    else:
        print("\nDisplaying plot...")
        plt.show()


def get_interactive_args():
    """Prompt user for input if no arguments are provided."""
    print("--- CSV Duplicate Checker ---")
    input_path = input("Enter path to input CSV file: ").strip()
    column = input("Enter column name to check: ").strip()
    
    output_path = input("Enter path to save results (optional, press Enter to skip): ").strip()
    if not output_path:
        output_path = None
        
    ignore_case_in = input("Ignore case? (y/n): ").lower().strip() == 'y'
    trim_in = input("Trim whitespace? (y/n): ").lower().strip() == 'y'
    plot_in = input("Generate plot? (y/n): ").lower().strip() == 'y'
    
    return input_path, column, output_path, ignore_case_in, trim_in, plot_in


def main():
    parser = argparse.ArgumentParser(description="Find duplicate values in a CSV column")
    parser.add_argument("input", nargs='?', help="Path to input CSV file")
    parser.add_argument("column", nargs='?', help="Column name to check for duplicates")
    parser.add_argument("-o", "--output", help="Path to save results (optional)")
    parser.add_argument("--ignore-case", action="store_true", help="Ignore case when comparing values")
    parser.add_argument("--trim", action="store_true", help="Trim whitespace from values")
    parser.add_argument("--plot", action="store_true", help="Generate a bar chart of top duplicates")

    args = parser.parse_args()

    # Interactive mode if arguments are missing
    if args.input is None or args.column is None:
        input_path, column, output_path, ignore_case, trim, plot = get_interactive_args()
    else:
        input_path = args.input
        column = args.column
        output_path = args.output
        ignore_case = args.ignore_case
        trim = args.trim
        plot = args.plot

    find_duplicates(input_path, column, output_path, ignore_case, trim, plot)


if __name__ == "__main__":
    main()
