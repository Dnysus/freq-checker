from main import find_duplicates, get_interactive_args
import os
import sys
import pandas as pd
import pytest
from unittest.mock import patch, MagicMock
from io import StringIO

# Add parent directory to path to import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


@pytest.fixture
def sample_csv(tmp_path):
    d = tmp_path / "data.csv"
    content = "Name,Email,City\n" \
              "John Doe,john@example.com,New York\n" \
              "Jane Smith,jane@example.com,Chicago\n" \
              "john doe,JOHN@EXAMPLE.COM,New York\n" \
              "Bob Jones,bob@example.com,Boston\n" \
              "John Doe ,john@example.com , New York \n" \
              "Alice,alice@example.com,Chicago"
    d.write_text(content)
    return str(d)


def test_find_duplicates_basic(sample_csv):
    """Test finding exact duplicates without normalization."""
    # "New York" appears twice exactly? No, wait:
    # "New York"
    # "New York"
    # " New York " (with spaces)
    # The sample data has:
    # 1. New York
    # 2. New York
    # 3.  New York

    # Actually, looking at the sample content provided:
    # "John Doe,john@example.com,New York"
    # "john doe,JOHN@EXAMPLE.COM,New York" -> This is a second "New York"
    # "John Doe ,john@example.com , New York " -> The csv reader might parse " New York " with spaces depending on quotechar/skipinitialspace.
    # Default pandas read_csv doesn't trim whitespace after delimiter.

    df = find_duplicates(sample_csv, "City")

    # "New York" (exact) appears in row 1 and 3. row 5 has spaces.
    # So "New York" count should be 2.
    # "Chicago" appears in row 2 and 6. count = 2.

    assert len(df) == 2
    assert df[df['City'] == 'New York']['count'].iloc[0] == 2
    assert df[df['City'] == 'Chicago']['count'].iloc[0] == 2


def test_find_duplicates_normalization(sample_csv):
    """Test with trim and ignore_case."""
    # With normalization:
    # Name: "John Doe", "john doe", "John Doe " -> All should be "john doe" -> count 3.

    df = find_duplicates(sample_csv, "Name", ignore_case=True, trim=True)

    assert len(df) == 1
    # Check that "john doe" is the index key (normalized) or however the function returns it.
    # The function converts to string, lowers and trims.
    # The returned df has the normalized values.

    assert df['Name'].iloc[0] == 'john doe'
    assert df['count'].iloc[0] == 3


def test_column_not_found(sample_csv, capsys):
    df = find_duplicates(sample_csv, "NonExistentColumn")
    assert df.empty
    captured = capsys.readouterr()
    assert "Error: Column 'NonExistentColumn' not found" in captured.out


def test_file_not_found(capsys):
    df = find_duplicates("non_existent_file.csv", "Column")
    assert df.empty
    captured = capsys.readouterr()
    assert "Error: File not found" in captured.out


def test_output_csv(sample_csv, tmp_path):
    output_file = tmp_path / "results.csv"
    find_duplicates(sample_csv, "City", output_path=str(output_file))

    assert output_file.exists()
    df_out = pd.read_csv(output_file)
    assert len(df_out) == 2


@patch("main.plt")
def test_plot_generation(mock_plt, sample_csv):
    """Test that plt functions are called when plot=True."""
    find_duplicates(sample_csv, "City", plot=True)

    mock_plt.figure.assert_called_once()
    mock_plt.bar.assert_called_once()
    mock_plt.show.assert_called_once()  # No output path, so show()


@patch("main.plt")
def test_plot_save(mock_plt, sample_csv, tmp_path):
    output_png = str(tmp_path / "plot.csv")  # Logic replaces .csv with .png
    find_duplicates(sample_csv, "City", output_path=output_png, plot=True)

    expected_png = str(tmp_path / "plot.png")
    mock_plt.savefig.assert_called_with(expected_png)


@patch("builtins.input", side_effect=["data.csv", "Email", "", "y", "n", "n"])
def test_interactive_args(mock_input):
    """Test interactive input gathering."""
    args = get_interactive_args()
    assert args == ("data.csv", "Email", None, True, False, False)
