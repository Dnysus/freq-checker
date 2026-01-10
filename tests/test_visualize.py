import pytest
from unittest.mock import patch
import pandas as pd
from freq_checker.visualize import generate_plot

@pytest.fixture
def sample_duplicates():
    return pd.DataFrame({
        'City': ['New York', 'Chicago'],
        'count': [10, 5]
    })

@patch("freq_checker.visualize.plt")
def test_plot_generation(mock_plt, sample_duplicates):
    """Test that plt functions are called."""
    generate_plot(sample_duplicates, "City", output_path=None)
    
    mock_plt.figure.assert_called_once()
    mock_plt.bar.assert_called_once()
    mock_plt.show.assert_called_once()

@patch("freq_checker.visualize.plt")
def test_plot_save(mock_plt, sample_duplicates, tmp_path):
    output_png = str(tmp_path / "plot.csv")
    generate_plot(sample_duplicates, "City", output_path=output_png)
    
    expected_png = str(tmp_path / "plot.png")
    mock_plt.savefig.assert_called_with(expected_png)
