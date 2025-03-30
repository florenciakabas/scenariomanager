import os
import pandas as pd
from pyspark.sql import SparkSession
from utils import LocalDashboard

def create_spark_session():
    
    return SparkSession.builder \
        .appName("ScenarioManager") \
        .master("local[*]") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()

class StorageProvider:
    """Abstract storage provider that works both locally and in Databricks"""
    
    @staticmethod
    def get_provider(environment="local", **kwargs):
        """Factory method to get the appropriate storage provider"""
        if environment.lower() == "databricks":
            return DatabricksStorageProvider(**kwargs)
        else:
            return LocalStorageProvider(**kwargs)


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

