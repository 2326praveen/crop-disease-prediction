"""
Prediction module for crop disease classification.

REFACTORED following SOLID principles:
- SRP: Separates model loading, preprocessing, prediction, and info retrieval
- OCP: Easy to extend with new models or preprocessing strategies
- DIP: Depends on abstractions through interfaces
- ISP: Uses focused interfaces for each responsibility

Maintains backward compatibility with existing code.
"""

import sys
import os
from pathlib import Path

from src.transforms import ImageTransformer
from src.services.prediction_services import (
    PyTorchModelLoader,
    ImagePreprocessor,
    JSONClassNameProvider,
    StaticDiseaseInfoProvider,
    PredictionService
)


class Predictor:
    """
    Predictor class refactored with SOLID principles.
    
    SOLID Principles Applied:
    - SRP (Single Responsibility): Delegates to specialized services:
      * PyTorchModelLoader: loads ML models
      * ImagePreprocessor: preprocesses images
      * JSONClassNameProvider: manages class names
      * StaticDiseaseInfoProvider: provides disease information
      * PredictionService: makes predictions
    
    - OCP (Open/Closed): Closed for modification, open for extension.
      New model types or preprocessing can be added by implementing
      the appropriate interfaces.
    
    - DIP (Dependency Inversion): Uses dependency injection with
      interfaces, not concrete implementations.
    
    - ISP (Interface Segregation): Each service implements a focused
      interface (IModelLoader, IImagePreprocessor, etc.)
    
    - LSP (Liskov Substitution): Any implementation of the interfaces
      can be substituted without breaking functionality.
    """
    
    def __init__(
        self,
        model_path='models/best_model.pth',
        config_path='config/class_names.json'
    ):
        """
        Initialize predictor with dependency injection.
        
        DIP: Creates and injects dependencies based on interfaces.
        SRP: Each component has a single responsibility.
        """
        # Get the project root directory (parent of src)
        self.base_dir = Path(__file__).parent.parent
        model_full_path = str(self.base_dir / model_path)
        config_full_path = str(self.base_dir / config_path)
        
        # Create class name provider (SRP: only manages class names)
        # OCP: Could easily switch to database or API-based provider
        self.class_provider = JSONClassNameProvider(config_full_path)
        
        # Create model loader (SRP: only loads models)
        # DIP: Depends on IModelLoader interface
        model_loader = PyTorchModelLoader(self.class_provider.get_class_count())
        
        # Load model
        self.model = model_loader.load_model(model_full_path)
        self.device = model_loader.get_device()
        
        # Create image preprocessor (SRP: only preprocesses images)
        # DIP: Depends on ImageTransformer abstraction
        transformer = ImageTransformer()
        self.preprocessor = ImagePreprocessor(transformer)
        
        # Create prediction service (SRP: only makes predictions)
        # DIP: All dependencies injected through interfaces
        self.prediction_service = PredictionService(
            model=self.model,
            preprocessor=self.preprocessor,
            class_provider=self.class_provider,
            device=self.device
        )
        
        # Create disease info provider (SRP: only provides disease info)
        # OCP: Can be extended to use database or API without modifying this class
        self.disease_info_provider = StaticDiseaseInfoProvider()
        
        # Backward compatibility: expose classes and other attributes
        self.classes = self.class_provider.get_class_names()
        self.num_classes = self.class_provider.get_class_count()
        self.model_path = self.base_dir / model_path
        self.config_path = self.base_dir / config_path
        self.transformer = transformer
    
    def predict_image(self, image):
        """
        Predict disease class for a single image.
        
        Args:
            image: PIL Image, file path, or file-like object
            
        Returns:
            Dictionary with prediction results:
                - predicted_class: Name of predicted class
                - confidence: Confidence score (0-100)
                - all_probabilities: Dictionary of all class probabilities
        
        SOLID:
        - SRP: Delegates to prediction service
        - DIP: Uses interface-based service
        """
        return self.prediction_service.predict(image)
    
    def predict_batch(self, images):
        """
        Predict disease classes for multiple images.
        
        Args:
            images: List of PIL Images or file paths
            
        Returns:
            List of prediction dictionaries
        
        SOLID:
        - SRP: Delegates to prediction service
        - DIP: Uses interface-based service
        """
        return self.prediction_service.predict_batch(images)
    
    def get_disease_info(self, disease_name):
        """
        Get information about a specific disease.
        
        Args:
            disease_name: Name of the disease
            
        Returns:
            Dictionary with disease information
        
        SOLID:
        - SRP: Delegates to disease info provider
        - DIP: Uses interface-based provider
        - OCP: Can be extended to use database or API without modifying this method
        """
        return self.disease_info_provider.get_disease_info(disease_name)
