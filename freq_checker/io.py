import pandas as pd
import os

def load_data(path: str) -> pd.DataFrame:
    """
    Load data from CSV or Excel file.
    Note: Chunking is not implemented for now as it requires significant logic changes 
    to the core duplicate counting (merging counts across chunks).
    Currently just loads the full file.
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"File not found: {path}")
    
    ext = os.path.splitext(path)[1].lower()
    
    if ext == '.csv':
        return pd.read_csv(path)
    elif ext in ['.xls', '.xlsx']:
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file extension: {ext}")

def save_data(df: pd.DataFrame, path: str):
    """Save DataFrame to CSV or Excel."""
    ext = os.path.splitext(path)[1].lower()
    
    if ext == '.csv':
        df.to_csv(path, index=False)
    elif ext in ['.xls', '.xlsx']:
        df.to_excel(path, index=False)
    else:
        # Fallback to CSV if unknown
        new_path = path + '.csv'
        df.to_csv(new_path, index=False)
        print(f"Warning: Unknown extension '{ext}'. Saved as CSV to {new_path}")
