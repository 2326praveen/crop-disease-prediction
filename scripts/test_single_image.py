"""
Test the trained model on a single image.
"""

import sys
import os
from pathlib import Path
import json

import torch
from PIL import Image

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.model import CropDiseaseClassifier
from src.transforms import ImageTransformer


def test_image(image_path, model_path, class_names_path):
    """Test a single image with the trained model."""
    
    # Load class names
    with open(class_names_path, 'r') as f:
        class_data = json.load(f)
        classes = class_data['classes']
    
    num_classes = len(classes)
    
    # Load model
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = CropDiseaseClassifier(num_classes=num_classes)
    model.load_state_dict(torch.load(model_path, map_location=device))
    model.to(device)
    model.eval()
    
    # Load and transform image
    transformer = ImageTransformer()
    
    image = Image.open(image_path).convert('RGB')
    image_tensor = transformer.transform(image).unsqueeze(0).to(device)
    
    # Make prediction
    with torch.no_grad():
        outputs = model(image_tensor)
        probabilities = torch.nn.functional.softmax(outputs, dim=1)
        confidence, predicted = torch.max(probabilities, 1)
    
    predicted_class = classes[predicted.item()]
    confidence_pct = confidence.item() * 100
    
    # Print results
    print(f"\n{'='*60}")
    print(f"Image: {Path(image_path).name}")
    print(f"Predicted Class: {predicted_class}")
    print(f"Confidence: {confidence_pct:.2f}%")
    print(f"{'='*60}")
    
    # Print all class probabilities
    print("\nAll Class Probabilities:")
    for i, class_name in enumerate(classes):
        prob = probabilities[0][i].item() * 100
        print(f"  {class_name}: {prob:.2f}%")
    print()
    
    return predicted_class, confidence_pct


if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    
    # Test on multiple sample images from different classes
    test_images = [
        base_dir / "datasets" / "rice_leaf_subset" / "test" / "Bacterialblight" / "BACTERIALBLIGHT1_068.jpg",
        base_dir / "datasets" / "rice_leaf_subset" / "test" / "Blast" / "BLAST2_002.jpg",
        base_dir / "datasets" / "rice_leaf_subset" / "test" / "Brownspot" / "BROWNSPOT1_147.jpg"
    ]
    
    model_path = base_dir / "models" / "best_model.pth"
    class_names_path = base_dir / "config" / "class_names.json"
    
    print(f"\nTesting model on {len(test_images)} images...")
    print(f"Model: {model_path}\n")
    
    correct = 0
    for img_path in test_images:
        actual_class = img_path.parent.name
        predicted_class, confidence = test_image(img_path, model_path, class_names_path)
        
        if predicted_class == actual_class:
            print(f"✓ CORRECT - Actual: {actual_class}\n")
            correct += 1
        else:
            print(f"✗ WRONG - Actual: {actual_class}, Predicted: {predicted_class}\n")
    
    print(f"\n{'='*60}")
    print(f"Test Results: {correct}/{len(test_images)} correct ({correct/len(test_images)*100:.1f}%)")
    print(f"{'='*60}\n")
