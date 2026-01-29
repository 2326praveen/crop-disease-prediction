"""
Prediction service implementations following SOLID principles.
"""

import json
import torch
from pathlib import Path
from PIL import Image
from typing import Any, Dict, List
import torchvision.models as models

from src.interfaces.prediction_interfaces import (
    IModelLoader,
    IImagePreprocessor,
    IPredictionService,
    IDiseaseInfoProvider,
    IClassNameProvider
)


class PyTorchModelLoader(IModelLoader):
    """
    PyTorch model loader implementation.
    
    SOLID Principles Applied:
    - SRP: Only responsible for loading PyTorch models
    - OCP: Can be extended for different model architectures
    - DIP: Implements IModelLoader interface
    """
    
    def __init__(self, num_classes: int):
        self.num_classes = num_classes
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    
    def load_model(self, model_path: str) -> Any:
        """Load ResNet18 model from checkpoint."""
        # Create model architecture
        model = models.resnet18(weights=None)
        
        # Modify final layer (same structure as training)
        num_ftrs = model.fc.in_features
        model.fc = torch.nn.Sequential(
            torch.nn.Dropout(0.5),
            torch.nn.Linear(num_ftrs, self.num_classes)
        )
        
        # Load weights
        checkpoint = torch.load(model_path, map_location=self.device)
        if isinstance(checkpoint, dict) and 'model_state_dict' in checkpoint:
            model.load_state_dict(checkpoint['model_state_dict'])
        else:
            model.load_state_dict(checkpoint)
        
        model.to(self.device)
        model.eval()
        
        return model
    
    def get_device(self) -> Any:
        """Get computation device."""
        return self.device


class ImagePreprocessor(IImagePreprocessor):
    """
    Image preprocessing for model input.
    
    SOLID Principles Applied:
    - SRP: Only handles image transformation
    - DIP: Implements IImagePreprocessor interface
    - LSP: Can be replaced with different preprocessing strategies
    """
    
    def __init__(self, transformer):
        """
        Initialize with image transformer.
        
        DIP: Depends on transformer abstraction.
        """
        self.transformer = transformer
    
    def preprocess(self, image: Image.Image) -> Any:
        """Preprocess image to tensor."""
        if not isinstance(image, Image.Image):
            if isinstance(image, (str, Path)):
                image = Image.open(image).convert('RGB')
            elif hasattr(image, 'read'):
                image = Image.open(image).convert('RGB')
        
        return self.transformer.transform(image)


class JSONClassNameProvider(IClassNameProvider):
    """
    Class name provider that loads from JSON file.
    
    SOLID Principles Applied:
    - SRP: Only manages class names
    - OCP: Can be extended to load from database or API
    - DIP: Implements IClassNameProvider interface
    """
    
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self._load_classes()
    
    def _load_classes(self):
        """Load class names from JSON file."""
        with open(self.config_path, 'r') as f:
            class_data = json.load(f)
            self.classes = class_data['classes']
    
    def get_class_names(self) -> List[str]:
        """Get list of class names."""
        return self.classes
    
    def get_class_count(self) -> int:
        """Get number of classes."""
        return len(self.classes)


class StaticDiseaseInfoProvider(IDiseaseInfoProvider):
    """
    Static disease information provider.
    
    SOLID Principles Applied:
    - SRP: Only provides disease information
    - OCP: Can be extended to load from database or external API
    - DIP: Implements IDiseaseInfoProvider interface
    """
    
    def __init__(self):
        self.disease_data = {
            'Bacterialblight': {
                'description': 'Bacterial blight is a serious disease affecting rice crops.',
                'symptoms': 'Water-soaked lesions on leaves, wilting, and yellowing.',
                'treatment': 'Use resistant varieties, proper water management, and copper-based bactericides.'
            },
            'Blast': {
                'description': 'Rice blast is caused by a fungal pathogen and is one of the most destructive rice diseases.',
                'symptoms': 'Diamond-shaped lesions with gray centers and brown margins on leaves.',
                'treatment': 'Use resistant varieties, fungicide application, and proper field sanitation.'
            },
            'Brownspot': {
                'description': 'Brown spot is a fungal disease that affects rice plants.',
                'symptoms': 'Circular or oval brown spots on leaves, stems, and grains.',
                'treatment': 'Seed treatment, balanced fertilization, and fungicide application.'
            }
        }
    
    def get_disease_info(self, disease_name: str) -> Dict[str, str]:
        """Get information about a disease."""
        return self.disease_data.get(disease_name, {
            'description': 'Disease information not available.',
            'symptoms': 'N/A',
            'treatment': 'Please consult an agricultural expert.'
        })
    
    def get_all_diseases(self) -> List[str]:
        """Get list of all supported diseases."""
        return list(self.disease_data.keys())


class PredictionService(IPredictionService):
    """
    Prediction service implementation.
    
    SOLID Principles Applied:
    - SRP: Only handles prediction logic
    - DIP: Depends on abstractions (interfaces) for all dependencies
    - OCP: Closed for modification, open for extension
    """
    
    def __init__(
        self,
        model: Any,
        preprocessor: IImagePreprocessor,
        class_provider: IClassNameProvider,
        device: Any
    ):
        """
        Initialize with injected dependencies.
        
        DIP: All dependencies are abstractions.
        """
        self.model = model
        self.preprocessor = preprocessor
        self.class_provider = class_provider
        self.device = device
    
    def predict(self, image: Any) -> Dict[str, Any]:
        """
        Make prediction on a single image.
        
        SRP: Only makes predictions, delegates preprocessing and class resolution.
        """
        # Preprocess image
        image_tensor = self.preprocessor.preprocess(image).unsqueeze(0).to(self.device)
        
        # Make prediction
        with torch.no_grad():
            outputs = self.model(image_tensor)
            probabilities = torch.nn.functional.softmax(outputs, dim=1)
            confidence, predicted = torch.max(probabilities, 1)
        
        # Get results
        classes = self.class_provider.get_class_names()
        predicted_class = classes[predicted.item()]
        confidence_pct = confidence.item() * 100
        
        # Get all class probabilities
        all_probs = {}
        for i, class_name in enumerate(classes):
            all_probs[class_name] = probabilities[0][i].item() * 100
        
        return {
            'predicted_class': predicted_class,
            'confidence': confidence_pct,
            'all_probabilities': all_probs
        }
    
    def predict_batch(self, images: List[Any]) -> List[Dict[str, Any]]:
        """
        Make predictions on multiple images.
        
        SRP: Delegates to single prediction method.
        """
        return [self.predict(image) for image in images]
