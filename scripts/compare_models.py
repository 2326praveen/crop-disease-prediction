"""
Compare both model files to find the better one
"""
import torch
from pathlib import Path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))
from src.model import CropDiseaseClassifier
from src.transforms import ImageTransformer
from PIL import Image

def test_model(model_path, test_images):
    """Test a model on test images"""
    print(f"\n{'='*60}")
    print(f"Testing: {model_path.name}")
    print('='*60)
    
    # Load model
    model = CropDiseaseClassifier(num_classes=3)
    model.load_state_dict(torch.load(model_path, map_location='cpu'))
    model.eval()
    
    classes = ['Bacterialblight', 'Blast', 'Brownspot']
    transformer = ImageTransformer()
    
    correct = 0
    total = 0
    
    for class_idx, (class_name, img_paths) in enumerate(test_images.items()):
        print(f"\nTesting {class_name} images:")
        class_correct = 0
        
        for img_path in img_paths:
            image = Image.open(img_path).convert('RGB')
            image_tensor = transformer.transform(image).unsqueeze(0)
            
            with torch.no_grad():
                output = model(image_tensor)
                probs = torch.nn.functional.softmax(output, dim=1)
                pred_idx = torch.argmax(probs, dim=1).item()
                confidence = probs[0][pred_idx].item() * 100
            
            predicted_class = classes[pred_idx]
            is_correct = (pred_idx == class_idx)
            
            if is_correct:
                class_correct += 1
                correct += 1
            total += 1
            
            symbol = "✓" if is_correct else "✗"
            print(f"  {symbol} {img_path.name[:30]:30} → {predicted_class:15} ({confidence:5.1f}%)")
        
        class_acc = (class_correct / len(img_paths)) * 100
        print(f"  Class Accuracy: {class_acc:.1f}% ({class_correct}/{len(img_paths)})")
    
    overall_acc = (correct / total) * 100
    print(f"\n{'='*60}")
    print(f"OVERALL ACCURACY: {overall_acc:.1f}% ({correct}/{total})")
    print('='*60)
    
    return overall_acc

def main():
    # Collect test images
    test_images = {
        'Bacterialblight': list(Path('datasets/rice_leaf_subset/test/Bacterialblight').glob('*.jpg'))[:5],
        'Blast': list(Path('datasets/rice_leaf_subset/test/Blast').glob('*.jpg'))[:5],
        'Brownspot': list(Path('datasets/rice_leaf_subset/test/Brownspot').glob('*.jpg'))[:5],
    }
    
    print("\n" + "="*60)
    print("MODEL COMPARISON TEST")
    print("="*60)
    print(f"Testing with {sum(len(imgs) for imgs in test_images.values())} images (5 per class)")
    
    # Test both models
    models_dir = Path('models')
    best_model_acc = test_model(models_dir / 'best_model.pth', test_images)
    crop_model_acc = test_model(models_dir / 'crop_disease_model.pth', test_images)
    
    # Recommendation
    print("\n" + "="*60)
    print("RECOMMENDATION")
    print("="*60)
    if crop_model_acc > best_model_acc:
        print(f"✓ Use crop_disease_model.pth ({crop_model_acc:.1f}% accuracy)")
        print(f"  It performs better than best_model.pth ({best_model_acc:.1f}% accuracy)")
    elif best_model_acc > crop_model_acc:
        print(f"✓ Use best_model.pth ({best_model_acc:.1f}% accuracy)")
        print(f"  It performs better than crop_disease_model.pth ({crop_model_acc:.1f}% accuracy)")
    else:
        print(f"Both models have similar accuracy ({best_model_acc:.1f}%)")
    print("="*60)

if __name__ == "__main__":
    main()
