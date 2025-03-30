import pandas as pd

class FunctionBasedModel:
    """Turns simple prediction functions into Protocol-compatible models"""
    
    def __init__(self, predict_func, param_dict=None):
        self.predict_func = predict_func
        self.parameters = param_dict or {}
    
    def set_parameters(self, **kwargs):
        self.parameters.update(kwargs)
    
    def fit(self, data: pd.DataFrame):
        # Many function-based models don't need fitting
        pass
    
    def predict(self, data: pd.DataFrame):
        result = data.copy()
        result['predicted_y'] = data.apply(
            lambda row: self.predict_func(row, **self.parameters), 
            axis=1
        )
        return result
    
    def get_parameters(self):
        return self.parameters.copy()

# Now even simple functions can be used as models
def simple_power_model(row, exponent=2, coefficient=1):
    return coefficient * (row['x'] ** exponent)

power_model = FunctionBasedModel(simple_power_model, {'exponent': 2, 'coefficient': 3})

# power_model now satisfies the Model Protocol!