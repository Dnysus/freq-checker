import pandas as pd
from thefuzz import process, fuzz
import jellyfish

def find_fuzzy_duplicates(
    df: pd.DataFrame, 
    column: str, 
    threshold: int = 90
) -> pd.DataFrame:
    """
    Find fuzzy duplicates in a column.
    
    Returns a DataFrame with columns: [Original, Match, Score]
    """
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found.")

    unique_values = df[column].dropna().unique().astype(str)
    
    matches = []
    # Compare each value against all others
    # (Note: This is O(N^2) and very slow for large datasets, 
    # we should optimize this later with blocking or rapidfuzz cdist)
    
    # Simple implementation: compare each unique value to finding a match in the rest
    # Ideally we find "clusters". 
    # For now, let's just find things that look like each other.
    
    checked = set()
    
    for val in unique_values:
        if val in checked:
            continue
            
        # exclude exact self match from extraction if possible, or filter later
        # process.extract returns list of (match, score)
        candidates = process.extract(val, unique_values, limit=10, scorer=fuzz.token_sort_ratio)
        
        for match, score in candidates:
            if score >= threshold and match != val:
                # We found a duplicate!
                matches.append({
                    'Value': val,
                    'Match': match,
                    'Score': score
                })
                checked.add(match) # Don't re-check if we found it as a match?
        
        checked.add(val)

    return pd.DataFrame(matches)

def find_phonetic_duplicates(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Find values that sound similar using Metaphone."""
    if column not in df.columns:
        raise ValueError(f"Column '{column}' not found.")
        
    df = df.copy()
    # Apply metaphone
    df['phonetic'] = df[column].astype(str).apply(jellyfish.metaphone)
    
    # Find duplicates in phonetic column
    counts = df['phonetic'].value_counts()
    dupes = counts[counts > 1].index
    
    # Filter original df to show these groups
    results = df[df['phonetic'].isin(dupes)].sort_values('phonetic')
    return results[[column, 'phonetic']]
