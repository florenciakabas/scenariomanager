import os
import pandas as pd
from pyspark.sql import SparkSession
from localdashboard import LocalDashboard

def create_spark_session():
    
    return SparkSession.builder \
        .appName("ScenarioManager") \
        .master("local[*]") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

    
class StorageProvider:
    """Abstract storage provider factory"""
    
    @staticmethod
    def get_provider(environment="local", **kwargs):
        """Factory method to get the appropriate storage provider"""
        if environment.lower() == "databricks":
            from storageprovider import DatabricksStorageProvider
            return DatabricksStorageProvider(**kwargs)
        elif environment.lower() == "simple":
            return SimpleStorageProvider(base_path=kwargs.get('base_path', './data/simple'))
        else:
            try:
                # Try to import and use the PySpark-based provider
                from storageprovider import LocalStorageProvider
                return LocalStorageProvider(base_path=kwargs.get('base_path', './data/delta'))
            except Exception as e:
                print(f"Error initializing LocalStorageProvider: {e}")
                print("Falling back to SimpleStorageProvider")
                return SimpleStorageProvider(base_path=kwargs.get('base_path', './data/simple'))

class LocalStorageProvider:
    """Local storage provider that mimics Databricks Delta functionality"""
    def __init__(self, base_path="./data/delta"):
        import os
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
        self.spark = create_spark_session()
        
    def save_table(self, df, table_name, mode="append"):
        # Convert pandas DataFrame to Spark DataFrame if needed
        if isinstance(df, pd.DataFrame):
            spark_df = self.spark.createDataFrame(df)
        else:
            spark_df = df
            
        # Save as Delta table
        table_path = os.path.join(self.base_path, table_name)
        spark_df.write.format("delta").mode(mode).save(table_path)
        
        return table_path
    
    def read_table(self, table_name, version=None):
        """Read from a local Delta table, with optional time travel"""
        table_path = os.path.join(self.base_path, table_name)
        
        if version is not None:
            return self.spark.read.format("delta").option("versionAsOf", version).load(table_path)
        else:
            return self.spark.read.format("delta").load(table_path)
    
    def create_dashboard(self, name, tables=None):
        """Create a simple local visualization dashboard"""
        # In local mode, we'll create a simple matplotlib dashboard
        return LocalDashboard(name, tables, self)


class DatabricksStorageProvider:
    """Databricks-specific storage provider - implement when in Databricks"""

    def __init__(self, delta_path="/path/to/delta"):
        self.delta_path = delta_path
        # In Databricks, spark session is already available
        # This would use the Databricks spark session
        
    def save_table(self, df, table_name, mode="append"):
        """Save a DataFrame to a Databricks Delta table"""
        # Convert pandas DataFrame to Spark DataFrame if needed
        if isinstance(df, pd.DataFrame):
            spark_df = spark.createDataFrame(df)
        else:
            spark_df = df
            
        # Save as Delta table
        table_path = f"{self.delta_path}/{table_name}"
        spark_df.write.format("delta").mode(mode).save(table_path)
        
        return table_path
    
    def read_table(self, table_name, version=None):
        """Read from a Databricks Delta table"""
        table_path = f"{self.delta_path}/{table_name}"
        
        if version is not None:
            return spark.read.format("delta").option("versionAsOf", version).load(table_path)
        else:
            return spark.read.format("delta").load(table_path)
    
    def create_dashboard(self, name, tables=None):
        """In Databricks, this would create a proper dashboard"""
        # This would be implemented when in Databricks
        raise NotImplementedError("Databricks dashboards can only be created in Databricks")

class SimpleStorageProvider:
    """A simple storage provider that doesn't use PySpark for local testing"""
    
    def __init__(self, base_path="./data/simple"):
        self.base_path = base_path
        os.makedirs(base_path, exist_ok=True)
    
    def save_table(self, df, table_name, mode="append"):
        """Save a DataFrame to a CSV file"""
        # Ensure we have a pandas DataFrame
        if not isinstance(df, pd.DataFrame):
            raise ValueError("DataFrame must be a pandas DataFrame")
            
        # Save as CSV
        table_path = os.path.join(self.base_path, f"{table_name}.csv")
        
        if mode == "overwrite" or not os.path.exists(table_path):
            df.to_csv(table_path, index=False)
        else:  # append mode
            if os.path.exists(table_path):
                existing_df = pd.read_csv(table_path)
                combined_df = pd.concat([existing_df, df], ignore_index=True)
                combined_df.to_csv(table_path, index=False)
            else:
                df.to_csv(table_path, index=False)
        
        return table_path
    
    def read_table(self, table_name, version=None):
        """Read from a CSV file"""
        # Version parameter is ignored in this simple implementation
        table_path = os.path.join(self.base_path, f"{table_name}.csv")
        
        if not os.path.exists(table_path):
            raise FileNotFoundError(f"Table {table_name} not found")
            
        return pd.read_csv(table_path)
    
    def create_dashboard(self, name, tables=None):
        """Create a simple local visualization dashboard"""
        return LocalDashboard(name, tables, self)