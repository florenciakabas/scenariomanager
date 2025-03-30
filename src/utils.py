from typing import Dict

import math
import pandas as pd

def load_dataset(path: str) -> pd.DataFrame:
    """Load a dataset from a CSV or Excel file"""
    if path.endswith('.csv'):
        return pd.read_csv(path)
    elif path.endswith(('.xlsx', '.xls')):
        return pd.read_excel(path)
    else:
        raise ValueError(f"Unsupported file format: {path}")

def evaluate_model(actual: pd.Series, predicted: pd.Series) -> Dict[str, float]:
    """Calculate common evaluation metrics"""
    errors = actual - predicted
    absolute_errors = errors.abs()
    squared_errors = errors ** 2
    
    return {
        "mae": absolute_errors.mean(),
        "mse": squared_errors.mean(),
        "rmse": math.sqrt(squared_errors.mean()),
        "r2": 1 - (squared_errors.sum() / ((actual - actual.mean()) ** 2).sum())
    }