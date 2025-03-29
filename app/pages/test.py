import pandas as pd
import numpy as np

def analyze_dataset(df: pd.DataFrame, sample_size: int = 3) -> dict:
    """Comprehensive data analysis report with key statistics"""
    analysis = {
        'overview': {
            'total_records': len(df),
            'total_columns': len(df.columns),
            'memory_usage': df.memory_usage(deep=True).sum() // (1024 ** 2)  # in MB
        },
        'data_types': df.dtypes.astype(str).to_dict(),
        'missing_values': df.isna().sum().to_dict(),
        'missing_percentage': (df.isna().mean() * 100).round(2).to_dict(),
        'unique_values': df.nunique().to_dict(),
        'numeric_stats': {},
        'date_stats': {},
        'categorical_stats': {},
        'column_samples': {}
    }

    # Numeric columns analysis
    numeric_cols = df.select_dtypes(include=np.number).columns
    for col in numeric_cols:
        analysis['numeric_stats'][col] = {
            'min': df[col].min(),
            'max': df[col].max(),
            'mean': df[col].mean(),
            'median': df[col].median(),
            'std': df[col].std(),
            'zeros': (df[col] == 0).sum(),
            'negative': (df[col] < 0).sum()
        }

    # Date columns analysis
    date_cols = df.select_dtypes(include=['datetime', 'datetimetz']).columns
    for col in date_cols:
        analysis['date_stats'][col] = {
            'min_date': df[col].min().strftime('%Y-%m-%d'),
            'max_date': df[col].max().strftime('%Y-%m-%d'),
            'invalid_dates': df[col].isna().sum()
        }

    # Categorical columns analysis
    categorical_cols = df.select_dtypes(include='object').columns
    for col in categorical_cols:
        analysis['categorical_stats'][col] = {
            'top_values': df[col].value_counts().head(5).to_dict(),
            'unique_ratio': df[col].nunique() / len(df)
        }

    # Column samples
    for col in df.columns:
        analysis['column_samples'][col] = {
            'sample_values': df[col].dropna().head(sample_size).tolist(),
            'value_lengths': df[col].astype(str).str.len().value_counts().head(3).to_dict()
        }

    return analysis

def print_analysis_report(analysis: dict) -> None:
    """Human-readable report formatting"""
    print(f"{'='*40} Data Analysis Report {'='*40}")
    
    # Basic Info
    print(f"\n{' Basic Dataset Info ':-^80}")
    print(f"Total Records: {analysis['overview']['total_records']:,}")
    print(f"Total Columns: {analysis['overview']['total_columns']}")
    print(f"Memory Usage: {analysis['overview']['memory_usage']} MB")

    # Data Quality
    print(f"\n{' Data Quality Assessment ':-^80}")
    quality_table = []
    for col in analysis['missing_percentage']:
        quality_table.append([
            col,
            analysis['data_types'][col],
            f"{analysis['missing_percentage'][col]}%",
            analysis['unique_values'][col],
            len(analysis['column_samples'][col]['sample_values'])
        ])
    
    print(pd.DataFrame(
        quality_table,
        columns=['Column', 'Data Type', 'Missing %', 'Unique Values', 'Valid Samples']
    ).to_string(index=False))

    # Key Findings
    print(f"\n{' Key Findings ':-^80}")
    # Add custom insights based on your data
    # Example: Find columns with >50% missing values
    high_missing = [k for k,v in analysis['missing_percentage'].items() if v > 50]
    if high_missing:
        print(f"⚠️  High missing values (>50%): {', '.join(high_missing)}")

if __name__ == "__main__":
    # Load your dataset
    df = pd.read_excel('/home/ubuntu/app/utils/MONTHEND_MIS_12MAR2025.xlsx')
    
    # Generate analysis
    analysis = analyze_dataset(df)
    
    # Print report
    print_analysis_report(analysis)
    
    # Optional: Save full analysis to JSON
    import json
    with open('data_analysis_report.json', 'w') as f:
        json.dump(analysis, f, indent=2)