import matplotlib.pyplot as plt
import pandas as pd

def generate_plot(duplicates: pd.DataFrame, columns: str | list[str], output_path: str | None):
    """Generate a bar chart of the top 10 duplicates."""
    top_10 = duplicates.head(10).copy()
    
    if isinstance(columns, str):
        columns = [columns]
        
    # Create a label for the x-axis
    if len(columns) > 1:
        # Combine columns for the label: "Val1 | Val2"
        top_10['label'] = top_10[columns].astype(str).agg(' | '.join, axis=1)
        x_col = 'label'
        xlabel = ' | '.join(columns)
    else:
        x_col = columns[0]
        xlabel = columns[0]
    
    plt.figure(figsize=(10, 6))
    plt.bar(top_10[x_col], top_10['count'], color='skyblue')
    plt.xlabel(xlabel)
    plt.ylabel('Count')
    plt.title(f'Top 10 Duplicates in {xlabel}')
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
