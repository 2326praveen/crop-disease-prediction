"""
Prediction interfaces following SOLID principles.

These interfaces demonstrate:
- Interface Segregation Principle: Separate concerns
- Open/Closed Principle: Easy to extend with new models or processors
- Dependency Inversion Principle: High-level modules depend on abstractions
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List
from PIL import Image


class IModelLoader(ABC):
    """
    Interface for loading ML models.
    
    ISP: Focused only on model loading logic.
    OCP: Different model types (PyTorch, TensorFlow, ONNX) can implement this.
    SRP: Only responsible for loading models.
    """
    
    @abstractmethod
    def load_model(self, model_path: str) -> Any:
        """Load a model from file."""
        pass
    
    @abstractmethod
    def get_device(self) -> Any:
        """Get computation device (CPU/GPU)."""
        pass


class IImagePreprocessor(ABC):
    """
    Interface for image preprocessing.
    
    ISP: Separate interface for preprocessing logic.
    OCP: New preprocessing strategies can be added by implementing this.
    SRP: Only handles image transformation.
    """
    
    @abstractmethod
    def preprocess(self, image: Image.Image) -> Any:
        """Preprocess an image for model input."""
        pass


class IPredictionService(ABC):
    """
    Interface for prediction operations.
    
    ISP: Focused only on making predictions.
    DIP: UI and other modules depend on this abstraction.
    SRP: Only handles prediction logic.
    """
    
    @abstractmethod
    def predict(self, image: Any) -> Dict[str, Any]:
        """
        Make prediction on a single image.
        
        Returns:
            Dictionary with prediction results.
        """
        pass
    
    @abstractmethod
    def predict_batch(self, images: List[Any]) -> List[Dict[str, Any]]:
        """Make predictions on multiple images."""
        pass


class IDiseaseInfoProvider(ABC):
    """
    Interface for disease information retrieval.
    
    ISP: Separate interface for disease information.
    OCP: Can be extended with database, API, or file-based implementations.
    SRP: Only provides disease information.
    """
    
    @abstractmethod
    def get_disease_info(self, disease_name: str) -> Dict[str, str]:
        """Get information about a disease."""
        pass
    
    @abstractmethod
    def get_all_diseases(self) -> List[str]:
        """Get list of all supported diseases."""
        pass


class IClassNameProvider(ABC):
    """
    Interface for providing class names.
    
    ISP: Separate interface for class name retrieval.
    OCP: Can load from JSON, database, or hardcoded values.
    SRP: Only manages class names.
    """
    
    @abstractmethod
    def get_class_names(self) -> List[str]:
        """Get list of class names."""
        pass
    
    @abstractmethod
    def get_class_count(self) -> int:
        """Get number of classes."""
        pass
