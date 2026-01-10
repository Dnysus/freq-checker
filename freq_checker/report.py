import pandas as pd

def generate_html_report(
    duplicates: pd.DataFrame, 
    column: str, 
    output_path: str
):
    """Generate a standalone HTML report."""
    
    total_dupes = duplicates['count'].sum() if 'count' in duplicates.columns else len(duplicates)
    unique_dupes = len(duplicates)
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Duplicate Report: {column}</title>
        <style>
            body {{ font-family: sans-serif; margin: 2rem; }}
            table {{ border-collapse: collapse; width: 100%; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #f2f2f2; }}
            .summary {{ background: #e9f7ef; padding: 1rem; border-radius: 8px; margin-bottom: 2rem; }}
        </style>
    </head>
    <body>
        <h1>Duplicate Analysis Report</h1>
        
        <div class="summary">
            <h2>Summary</h2>
            <p><strong>Column Analyzed:</strong> {column}</p>
            <p><strong>Unique Duplicate Values:</strong> {unique_dupes}</p>
            <p><strong>Total Duplicate Rows:</strong> {total_dupes}</p>
        </div>

        <h2>Detailed Duplicates</h2>
        {duplicates.to_html(index=False)}
    </body>
    </html>
    """
    
    # Ensure correct extension
    if not output_path.endswith('.html'):
        output_path += '.html'
        
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"Saved HTML report to: {output_path}")
