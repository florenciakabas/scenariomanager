import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

from utils import load_dataset, evaluate_model
from pyspark.sql import SparkSession

from basemodel import Model, DataSource
from typing import Dict

import pandas as pd

from datetime import datetime

class ScenarioManager:
    """
    Manages multiple modeling scenarios, runs them, and tracks results
    Works both locally and in Databricks
    """
    
    def __init__(self, environment="local", storage_path=None):
        self.scenarios = {}
        self.environment = environment
        
        # Create appropriate storage provider
        self.storage = StorageProvider.get_provider(
            environment=environment, 
            base_path=storage_path or "./data/delta",
            delta_path=storage_path or "/path/to/delta"
        )
    
    def register_scenario(self, name, model, data_source, parameters=None):
        """Register a new scenario with a model and data source"""
        self.scenarios[name] = {
            "model": model,
            "data_source": data_source,
            "parameters": parameters or {},
            "results": None,
            "created_at": datetime.now()
        }
        return self
    
    def run_scenario(self, name):
        """Run a specific scenario"""
        # Same implementation as before
        # ...
        
    def save_to_delta(self):
        """Save all scenario results to Delta tables"""
        for name, scenario in self.scenarios.items():
            if scenario["results"] is None:
                continue
                
            # Prepare results dataframe
            results_df = scenario["results"].copy()
            results_df["scenario_name"] = name
            results_df["run_at"] = scenario["run_at"]
            results_df["parameters"] = str(scenario["model"].get_parameters())
            
            # Use the storage provider to save
            self.storage.save_table(results_df, f"scenario_results_{name}")
    
    def create_dashboard(self, name="Scenario Comparison"):
        """Create a dashboard for scenario comparison"""
        dashboard = self.storage.create_dashboard(name)
        
        # Add visualizations for each scenario
        for name, scenario in self.scenarios.items():
            if scenario["results"] is None:
                continue
            
            # Save results if not already saved
            table_name = f"scenario_results_{name}"
            self.storage.save_table(scenario["results"], table_name, mode="overwrite")
            
            # Add visualizations
            dashboard.add_visualization(
                "line", table_name, "x", "predicted_y", 
                f"Predictions for {name}"
            )
            
            if "y" in scenario["results"].columns:
                dashboard.add_visualization(
                    "scatter", table_name, "predicted_y", "y", 
                    f"Predicted vs Actual for {name}"
                )
        
        return dashboard