import pytest
import pandas as pd
from freq_checker.io import load_data, save_data

def test_load_csv(tmp_path):
    csv_file = tmp_path / "test.csv"
    csv_file.write_text("col1,col2\n1,2")
    
    df = load_data(str(csv_file))
    assert len(df) == 1
    assert df.iloc[0]['col1'] == 1

def test_load_excel(tmp_path):
    xlsx_file = tmp_path / "test.xlsx"
    df_in = pd.DataFrame({"col1": [1, 2]})
    df_in.to_excel(xlsx_file, index=False)
    
    df = load_data(str(xlsx_file))
    assert len(df) == 2
    assert df.iloc[0]['col1'] == 1

def test_save_excel(tmp_path):
    df = pd.DataFrame({"col1": [1, 2]})
    output = tmp_path / "out.xlsx"
    
    save_data(df, str(output))
    
    assert output.exists()
    # Verify we can read it back
    df_read = pd.read_excel(output)
    assert len(df_read) == 2

def test_file_not_found():
    with pytest.raises(FileNotFoundError):
        load_data("imaginary.csv")

def test_unsupported_extension(tmp_path):
    bad_file = tmp_path / "test.txt"
    bad_file.write_text("content")
    
    with pytest.raises(ValueError):
        load_data(str(bad_file))
