"""
Test predictor to debug prediction issues
"""
import torch
from src.predictor import Predictor
from pathlib import Path
import numpy as np

def test_predictor():
    """Test the predictor with various inputs"""
    print("="*60)
    print("PREDICTOR DIAGNOSTIC TEST")
    print("="*60)
    
    # Initialize predictor
    print("\n1. Loading predictor...")
    predictor = Predictor()
    print(f"   ✓ Model loaded from: {predictor.model_path}")
    print(f"   ✓ Classes: {predictor.classes}")
    print(f"   ✓ Number of classes: {predictor.num_classes}")
    print(f"   ✓ Device: {predictor.device}")
    
    # Test with actual test images
    print("\n2. Testing with actual test images...")
    test_dirs = [
        Path('datasets/rice_leaf_subset/test/Bacterialblight'),
        Path('datasets/rice_leaf_subset/test/Blast'),
        Path('datasets/rice_leaf_subset/test/Brownspot'),
    ]
    
    for test_dir in test_dirs:
        if test_dir.exists():
            images = list(test_dir.glob('*.jpg'))[:3]  # Get first 3 images
            print(f"\n   Testing {test_dir.name}:")
            for img_path in images:
                result = predictor.predict_image(str(img_path))
                print(f"      {img_path.name}")
                print(f"      → Predicted: {result['predicted_class']} ({result['confidence']:.1f}%)")
                print(f"      → All probabilities: {', '.join([f'{k}: {v:.1f}%' for k, v in result['all_probabilities'].items()])}")
                
    # Test model directly with random input
    print("\n3. Testing model with random input...")
    dummy_input = torch.randn(1, 3, 224, 224).to(predictor.device)
    predictor.model.eval()
    with torch.no_grad():
        output = predictor.model(dummy_input)
        probs = torch.nn.functional.softmax(output, dim=1)
        print(f"   Output shape: {output.shape}")
        print(f"   Raw output: {output[0].cpu().numpy()}")
        print(f"   Probabilities: {probs[0].cpu().numpy()}")
        print(f"   Predicted class: {predictor.classes[torch.argmax(probs, dim=1).item()]}")
    
    # Check model parameters
    print("\n4. Checking model architecture...")
    total_params = sum(p.numel() for p in predictor.model.parameters())
    trainable_params = sum(p.numel() for p in predictor.model.parameters() if p.requires_grad)
    print(f"   Total parameters: {total_params:,}")
    print(f"   Trainable parameters: {trainable_params:,}")
    
    # Check if model weights are actually loaded
    print("\n5. Checking model weights...")
    first_conv_weights = None
    for name, param in predictor.model.named_parameters():
        if 'conv1.weight' in name or 'features.0.weight' in name:
            first_conv_weights = param
            print(f"   First layer: {name}")
            print(f"   Shape: {param.shape}")
            print(f"   Mean: {param.mean().item():.6f}")
            print(f"   Std: {param.std().item():.6f}")
            print(f"   Min: {param.min().item():.6f}, Max: {param.max().item():.6f}")
            break
    
    print("\n" + "="*60)

if __name__ == "__main__":
    test_predictor()
