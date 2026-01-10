import pandas as pd

def find_duplicates(
    df: pd.DataFrame, 
    column: str, 
    ignore_case: bool = False,
    trim: bool = False
) -> pd.DataFrame:
    """Find values that appear more than once in the specified column."""
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found. Available: {list(df.columns)}")

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

    return duplicates
