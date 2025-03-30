import matplotlib.pyplot as plt
import numpy as np

class LocalDashboard:
    """Simple local implementation of a dashboard using matplotlib"""
    
    def __init__(self, name, tables=None, storage_provider=None):
        self.name = name
        self.tables = tables or []
        self.storage_provider = storage_provider
        self.visualizations = []
    
    def add_visualization(self, viz_type, table_name, x_column, y_column, title=None):
        """Add a visualization to the dashboard"""
        self.visualizations.append({
            "type": viz_type,
            "table": table_name,
            "x": x_column,
            "y": y_column,
            "title": title or f"{y_column} vs {x_column}"
        })
        return self
    
    def display(self):
        """Display the dashboard using matplotlib"""
        num_viz = len(self.visualizations)
        if num_viz == 0:
            print("No visualizations to display")
            return
        
        # Create a grid of subplots
        cols = min(num_viz, 3)
        rows = (num_viz + cols - 1) // cols
        
        fig, axes = plt.subplots(rows, cols, figsize=(cols*5, rows*4))
        if rows * cols == 1:
            axes = np.array([axes])
        axes = axes.flatten()
        
        for i, viz in enumerate(self.visualizations):
            if i >= len(axes):
                break
                
            # Get data
            data = self.storage_provider.read_table(viz["table"])
            
            # Create visualization
            if viz["type"] == "line":
                data.plot(x=viz["x"], y=viz["y"], kind="line", ax=axes[i], title=viz["title"])
            elif viz["type"] == "bar":
                data.plot(x=viz["x"], y=viz["y"], kind="bar", ax=axes[i], title=viz["title"])
            elif viz["type"] == "scatter":
                data.plot(x=viz["x"], y=viz["y"], kind="scatter", ax=axes[i], title=viz["title"])
            
            axes[i].set_xlabel(viz["x"])
            axes[i].set_ylabel(viz["y"])
        
        # Hide unused subplots
        for i in range(num_viz, len(axes)):
            axes[i].axis("off")
        
        plt.tight_layout()
        plt.show()
        
        return fig