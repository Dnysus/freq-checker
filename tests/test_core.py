import pytest
import pandas as pd
from freq_checker.core import find_duplicates

@pytest.fixture
def sample_df():
    data = {
        "Name": ["John Doe", "Jane Smith", "john doe", "Bob Jones", "John Doe ", "Alice"],
        "Email": ["john@example.com", "jane@example.com", "JOHN@EXAMPLE.COM", "bob@example.com", "john@example.com", "alice@example.com"],
        "City": ["New York", "Chicago", "New York", "Boston", " New York ", "Chicago"]
    }
    return pd.DataFrame(data)

def test_find_duplicates_basic(sample_df):
    """Test finding exact duplicates without normalization."""
    # In City: "New York" (row 0, 2) matches exactly. " New York " (row 4) does not.
    results = find_duplicates(sample_df, "City")
    
    assert len(results) == 2
    assert results[results['City'] == 'New York']['count'].iloc[0] == 2
    assert results[results['City'] == 'Chicago']['count'].iloc[0] == 2

def test_find_duplicates_normalization(sample_df):
    """Test with trim and ignore_case."""
    # In Name: "John Doe", "john doe", "John Doe " -> All should be "john doe" -> count 3.
    results = find_duplicates(sample_df, "Name", ignore_case=True, trim=True)
    
    assert len(results) == 1
    assert results['Name'].iloc[0] == 'john doe'
    assert results['count'].iloc[0] == 3

def test_column_not_found(sample_df):
    with pytest.raises(ValueError):
        find_duplicates(sample_df, "NonExistent")
