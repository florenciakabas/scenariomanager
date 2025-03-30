import ipdb
import numpy as np
import pandas as pd

import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from scenariomanager import ScenarioManager
from linearmodel import LinearRegressionModel
from functionbasedmodel import FunctionBasedModel

# Set up local scenario manager
manager = ScenarioManager(environment="simple")

# manager = ScenarioManager(environment="databricks", storage_path="/path/to/delta")

# Create data source
class SimpleDataSource:
    def get_data(self):
        return pd.DataFrame({
            "x": np.linspace(0, 10, 100),
            "y": np.linspace(0, 10, 100) + np.random.normal(0, 1, 100)
        })

# Create models
linear_model = LinearRegressionModel("linear", slope=1.0, intercept=0.0)
quadratic_model = FunctionBasedModel(
    lambda row, a=1, b=0, c=0: a * row['x']**2 + b * row['x'] + c,
    {"a": 1, "b": 0, "c": 0}
)

# Register scenarios
manager.register_scenario("linear", linear_model, SimpleDataSource())
manager.register_scenario("quadratic", quadratic_model, SimpleDataSource(), 
                         {"a": 0.1, "b": 1, "c": 0})

# Run scenarios
manager.run_all_scenarios()

# Save to local Delta tables
manager.save_to_delta()

# Create and display dashboard
dashboard = manager.create_dashboard("Model Comparison")
dashboard.display()