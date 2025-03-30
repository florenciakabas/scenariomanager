import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

import pandas as pd
from basemodel import BaseModel

class LinearRegressionModel(BaseModel):
    """Simple linear regression implementation"""
    
    def __init__(self, name: str, slope: float = 1.0, intercept: float = 0.0):
        super().__init__(name, "Simple linear regression model")
        self.set_parameters(slope=slope, intercept=intercept)
    
    def fit(self, data: pd.DataFrame) -> None:
        """
        Train the model using simple linear regression
        Expects 'x' and 'y' columns in the dataframe
        """
        if 'x' not in data.columns or 'y' not in data.columns:
            raise ValueError("Data must contain 'x' and 'y' columns")
            
        x = data['x'].values
        y = data['y'].values
        
        # Simple linear regression formula
        x_mean = x.mean()
        y_mean = y.mean()
        
        numerator = sum((x_i - x_mean) * (y_i - y_mean) for x_i, y_i in zip(x, y))
        denominator = sum((x_i - x_mean) ** 2 for x_i in x)
        
        if denominator == 0:
            raise ValueError("Cannot fit model: x values have zero variance")
        
        slope = numerator / denominator
        intercept = y_mean - slope * x_mean
        
        self.set_parameters(slope=slope, intercept=intercept)
        self._is_fitted = True
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate predictions using y = mx + b"""
        if 'x' not in data.columns:
            raise ValueError("Data must contain an 'x' column")
        
        result = data.copy()
        result['predicted_y'] = result['x'] * self.parameters['slope'] + self.parameters['intercept']
        return result