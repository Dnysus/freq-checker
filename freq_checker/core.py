import pandas as pd

def find_duplicates(
    df: pd.DataFrame, 
    columns: str | list[str], 
    ignore_case: bool = False,
    trim: bool = False
) -> pd.DataFrame:
    """Find values that appear more than once in the specified column(s)."""
    if isinstance(columns, str):
        columns = [columns]
        
    missing = [col for col in columns if col not in df.columns]
    if missing:
        raise ValueError(f"Column(s) '{', '.join(missing)}' not found. Available: {list(df.columns)}")

    # Normalize data
    # Create a copy to minimize side effects on the original df
    subset = df[columns].astype(str)
    
    if trim:
        for col in columns:
            subset[col] = subset[col].str.strip()
    
    if ignore_case:
        for col in columns:
            subset[col] = subset[col].str.lower()

    # Count occurrences
    counts = subset.groupby(columns).size().reset_index(name='count')
    duplicates = counts[counts['count'] > 1]
    
    return duplicates.sort_values('count', ascending=False)
