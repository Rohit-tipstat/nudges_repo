import pandas as pd
from typing import List

def remove_outliers_iqr_specific_columns(data: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    """
    Remove outliers using the IQR method for specified columns.

    Args:
        data (pd.DataFrame): The input DataFrame.
        columns (List[str]): List of column names to check for outliers.

    Returns:
        pd.DataFrame: Filtered DataFrame without outliers.
    """
    # First handle Total COE specifically
    if 'Total COE' in data.columns:
        # Convert to numeric and remove empty/missing values
        data['Total COE'] = pd.to_numeric(data['Total COE'], errors='coerce')
        data = data.dropna(subset=['Total COE'])
        
        
    Q1 = data[columns].quantile(0.25)
    Q3 = data[columns].quantile(0.75)
    IQR = Q3 - Q1

    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    filtered_data = data[~((data[columns] < lower_bound) | (data[columns] > upper_bound)).any(axis=1)]
    
    filtered_data.to_csv('app/data/output.csv', index=False, header=True)

    return filtered_data


def indian_human_readable(value: float) -> str:
    """
    Convert large numbers to human-readable format in the Indian numbering system.

    Args:
        value (float): The numeric value to format.

    Returns:
        str: Human-readable formatted value.
    """
    if value >= 1e7:
        return f"{value / 1e7:.2f} Crore Rupees"
    elif value >= 1e5:
        return f"{value / 1e5:.2f} Lakh Rupees"
    elif value >= 1e3:
        return f"{value / 1e3:.2f} thousand Rupees"
    else:
        return str(value)