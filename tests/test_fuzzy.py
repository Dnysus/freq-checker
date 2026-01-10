import pytest
import pandas as pd
from freq_checker.fuzzy import find_fuzzy_duplicates, find_phonetic_duplicates

@pytest.fixture
def fuzzy_df():
    return pd.DataFrame({
        "Name": ["John Doe", "Jon Doe", "Jane Smith", "Jame Smith", "Alice", "Bob"]
    })

def test_fuzzy_matching(fuzzy_df):
    """Test finding fuzzy duplicates."""
    # "John Doe" vs "Jon Doe" should match high
    results = find_fuzzy_duplicates(fuzzy_df, "Name", threshold=80)
    
    # We expect matches. 
    # results df cols: [Value, Match, Score]
    
    # Let's check if "John Doe" matched "Jon Doe"
    match = results[(results['Value'] == 'John Doe') & (results['Match'] == 'Jon Doe')]
    assert not match.empty
    assert match['Score'].iloc[0] > 80

def test_phonetic_matching(fuzzy_df):
    """Test phonetic matching."""
    # "John" and "Jon" sound alike? Maybe.
    # "Smith" and "Smyth" are better examples.
    # From sample: "Jane Smith", "Jame Smith" -> might sound similar depending on algo.
    
    # Let's add explicit phonetic dupes
    df = pd.DataFrame({"Name": ["Smith", "Smyth", "Schmidt"]})
    
    results = find_phonetic_duplicates(df, "Name")
    
    # Smith and Smyth usually same metaphone
    assert len(results) >= 2 
