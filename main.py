"""Script to find and export duplicate values from a CSV or Excel file."""
import argparse
import sys
import pandas as pd
from freq_checker.core import find_duplicates
from freq_checker.visualize import generate_plot
from freq_checker.fuzzy import find_fuzzy_duplicates, find_phonetic_duplicates
from freq_checker.io import load_data, save_data
from freq_checker.report import generate_html_report

def get_interactive_args():
    """Prompt user for input if no arguments are provided."""
    print("--- CSV/Excel Duplicate Checker ---")
    input_path = input("Enter path to input file (csv/xlsx): ").strip()
    column = input("Enter column name to check: ").strip()
    
    output_path = input("Enter path to save results (optional, press Enter to skip): ").strip()
    if not output_path:
        output_path = None
        
    ignore_case_in = input("Ignore case? (y/n): ").lower().strip() == 'y'
    trim_in = input("Trim whitespace? (y/n): ").lower().strip() == 'y'
    plot_in = input("Generate plot? (y/n): ").lower().strip() == 'y'
    report_in = input("Generate HTML report? (y/n): ").lower().strip() == 'y'
    
    return input_path, column, output_path, ignore_case_in, trim_in, plot_in, report_in


def main():
    parser = argparse.ArgumentParser(description="Find duplicate values in a CSV/Excel column")
    parser.add_argument("input", nargs='?', help="Path to input file")
    parser.add_argument("column", nargs='?', help="Column name to check for duplicates")
    parser.add_argument("-o", "--output", help="Path to save results (optional)")
    
    # Exact match options
    parser.add_argument("--ignore-case", action="store_true", help="Ignore case (exact match)")
    parser.add_argument("--trim", action="store_true", help="Trim whitespace (exact match)")
    
    # Advanced options
    parser.add_argument("--fuzzy", action="store_true", help="Use fuzzy matching")
    parser.add_argument("--threshold", type=int, default=90, help="Fuzzy match threshold (0-100)")
    parser.add_argument("--phonetic", action="store_true", help="Use phonetic matching (Soundex/Metaphone)")
    
    parser.add_argument("--plot", action="store_true", help="Generate a bar chart")
    parser.add_argument("--report", action="store_true", help="Generate HTML report")

    args = parser.parse_args()

    # Interactive mode if arguments are missing
    if args.input is None or args.column is None:
        input_path, column, output_path, ignore_case, trim, plot, report = get_interactive_args()
        # Defaults for interactive
        fuzzy = False
        threshold = 90
        phonetic = False
    else:
        input_path = args.input
        column = args.column
        output_path = args.output
        ignore_case = args.ignore_case
        trim = args.trim
        plot = args.plot
        report = args.report
        fuzzy = args.fuzzy
        threshold = args.threshold
        phonetic = args.phonetic

    try:
        df = load_data(input_path)
    except FileNotFoundError:
        print(f"Error: File not found: {input_path}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return

    # Parse columns (allow comma separation)
    columns = [c.strip() for c in column.split(',')]
    
    # 1. Exact Duplicates
    if not fuzzy and not phonetic:
        try:
            results = find_duplicates(df, columns, ignore_case, trim)
        except ValueError as e:
            print(f"Error: {e}")
            return
            
        if results.empty:
            print(f"No duplicates found in columns '{column}'.")
        else:
            print(f"Found {len(results)} values with duplicates:")
            print(results.to_string(index=False))
            
            if plot:
                generate_plot(results, columns, output_path)
            
            if report and output_path:
                # Basic report might need tweaking for multi-col, but dataframe to_html should work fine
                generate_html_report(results, column, output_path)

    # 2. Fuzzy Duplicates (Single column only for now)
    elif fuzzy:
        if len(columns) > 1:
            print("Error: Fuzzy matching currently supports only one column at a time.")
            return
            
        print(f"Running fuzzy matching on '{columns[0]}' with threshold {threshold}...")
        results = find_fuzzy_duplicates(df, columns[0], threshold)
        if results.empty:
            print("No fuzzy duplicates found.")
        else:
            print(f"Found {len(results)} potential matches:")
            print(results.to_string(index=False))

    # 3. Phonetic Duplicates (Single column only for now)
    elif phonetic:
        if len(columns) > 1:
            print("Error: Phonetic matching currently supports only one column at a time.")
            return

        print(f"Running phonetic matching on '{columns[0]}'...")
        results = find_phonetic_duplicates(df, columns[0])

        if results.empty:
            print("No phonetic duplicates found.")
        else:
            print("Found phonetic duplicates:")
            print(results.to_string(index=False))

    # Save results
    if output_path and not results.empty:
        save_data(results, output_path)
        print(f"\nSaved results to: {output_path}")

if __name__ == "__main__":
    main()
