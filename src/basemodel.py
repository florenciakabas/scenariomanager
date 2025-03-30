import json
import pandas as pd

from abc import ABC, abstractmethod
from typing import Protocol, Dict, Any, Optional, runtime_checkable
from datetime import datetime

@runtime_checkable
class DataSource(Protocol):
    def get_data(self) -> pd.DataFrame:
        """Retrieve data for model input"""
        ...

@runtime_checkable
class Model(Protocol):
    def set_parameters(self, **kwargs) -> None:
        """Configure model parameters"""
        ...
    
    def fit(self, data: pd.DataFrame) -> None:
        """Train the model if needed"""
        ...
    
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate predictions"""
        ...
    
    def get_parameters(self) -> Dict[str, Any]:
        """Return current parameter settings"""
        ...


class BaseModel(ABC):
    """Base implementation of a model with common functionality"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.created_at = datetime.now()
        self.parameters = {}
        self._is_fitted = False
    
    def set_parameters(self, **kwargs) -> None:
        """Set model parameters"""
        self.parameters.update(kwargs)
    
    def get_parameters(self) -> Dict[str, Any]:
        """Get current model parameters"""
        return self.parameters.copy()
    
    @abstractmethod
    def fit(self, data: pd.DataFrame) -> None:
        """Train the model - must be implemented by subclasses"""
        pass
    
    @abstractmethod
    def predict(self, data: pd.DataFrame) -> pd.DataFrame:
        """Generate predictions - must be implemented by subclasses"""
        pass
    
    def to_json(self) -> str:
        """Serialize model metadata to JSON"""
        return json.dumps({
            "name": self.name,
            "description": self.description,
            "created_at": self.created_at.isoformat(),
            "parameters": self.parameters,
            "is_fitted": self._is_fitted
        })