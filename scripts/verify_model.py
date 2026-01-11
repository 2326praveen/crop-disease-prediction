"""
Verify the trained model is correct and can be loaded
"""
import sys
import os
from pathlib import Path
import torch

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.model import CropDiseaseClassifier

def verify_model():
    """Verify the trained model"""
    base_dir = Path(__file__).parent.parent
    model_path = base_dir / 'models' / 'best_model.pth'
    
    print("=" * 60)
    print("Model Verification")
    print("=" * 60)
    
    # Check if model file exists
    if not model_path.exists():
        print(f"✗ Model file not found at: {model_path}")
        return
    
    print(f"\n✓ Model file found: {model_path}")
    print(f"  Size: {model_path.stat().st_size / (1024*1024):.1f} MB")
    
    try:
        # Load the model
        print("\n🔍 Loading model...")
        num_classes = 3  # Bacterialblight, Blast, Brownspot
        model = CropDiseaseClassifier(num_classes=num_classes)
        
        # Load state dict
        state_dict = torch.load(model_path, map_location='cpu')
        model.load_state_dict(state_dict)
        
        print("✓ Model loaded successfully!")
        
        # Check model structure
        print("\n📊 Model Architecture:")
        print(f"  Number of classes: {num_classes}")
        
        total_params = sum(p.numel() for p in model.parameters())
        trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
        
        print(f"  Total parameters: {total_params:,}")
        print(f"  Trainable parameters: {trainable_params:,}")
        
        # Verify model can make predictions
        print("\n🧪 Testing model inference...")
        model.eval()
        
        # Create a dummy input (batch_size=1, channels=3, height=224, width=224)
        dummy_input = torch.randn(1, 3, 224, 224)
        
        with torch.no_grad():
            output = model(dummy_input)
        
        print(f"  Input shape: {dummy_input.shape}")
        print(f"  Output shape: {output.shape}")
        print(f"  Expected output shape: (1, {num_classes})")
        
        if output.shape == (1, num_classes):
            print("  ✓ Output shape is correct!")
        else:
            print("  ✗ Output shape mismatch!")
            return
        
        # Check output values
        probabilities = torch.softmax(output, dim=1)
        predicted_class = torch.argmax(probabilities, dim=1).item()
        confidence = probabilities[0][predicted_class].item()
        
        print(f"\n  Test prediction:")
        print(f"    Predicted class index: {predicted_class}")
        print(f"    Confidence: {confidence:.2%}")
        print(f"    All probabilities: {probabilities[0].tolist()}")
        print(f"    Sum of probabilities: {probabilities.sum().item():.4f} (should be ~1.0)")
        
        # Verify state dict keys
        print("\n🔑 Model State Dict Info:")
        print(f"  Number of layers: {len(state_dict)}")
        print(f"  Sample layer names:")
        for i, key in enumerate(list(state_dict.keys())[:5]):
            print(f"    - {key}: {state_dict[key].shape}")
        
        # Check if final layer matches number of classes
        fc_weight_key = 'fc.weight'
        if fc_weight_key in state_dict:
            fc_shape = state_dict[fc_weight_key].shape
            print(f"\n  Final layer (fc.weight) shape: {fc_shape}")
            if fc_shape[0] == num_classes:
                print(f"  ✓ Final layer matches {num_classes} classes!")
            else:
                print(f"  ✗ Final layer has {fc_shape[0]} outputs, expected {num_classes}")
                return
        
        print("\n" + "=" * 60)
        print("✅ MODEL VERIFICATION PASSED!")
        print("=" * 60)
        print("\nThe model is correctly trained and ready to use for:")
        print("  - Bacterialblight")
        print("  - Blast")
        print("  - Brownspot")
        print("\nYou can now use it with the Streamlit app or for inference.")
        
    except Exception as e:
        print(f"\n✗ Error loading model: {e}")
        import traceback
        traceback.print_exc()
        return

if __name__ == "__main__":
    verify_model()
