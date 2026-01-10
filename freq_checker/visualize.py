import matplotlib.pyplot as plt
import pandas as pd

def generate_plot(duplicates: pd.DataFrame, column: str, output_path: str | None):
    """Generate a bar chart of the top 10 duplicates."""
    top_10 = duplicates.head(10)
    
    plt.figure(figsize=(10, 6))
    plt.bar(top_10[column], top_10['count'], color='skyblue')
    plt.xlabel(column)
    plt.ylabel('Count')
    plt.title(f'Top 10 Duplicates in {column}')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save plot if output path is provided, otherwise show it
    if output_path:
        plot_path = output_path.replace('.csv', '.png')
        if plot_path == output_path: # fallback if no extension
            plot_path += '.png'
        plt.savefig(plot_path)
        print(f"Saved plot to: {plot_path}")
    else:
        print("\nDisplaying plot...")
        plt.show()
