"""
Prepare a mixed dataset with rice leaf diseases and pulse crops
3 rice leaf classes: 50 images each
1 pulse class: 100 images
"""
import os
import shutil
import random
from pathlib import Path

def prepare_mixed_dataset():
    # Source directories
    rice_source = Path("datasets/praveen_kumar_reddy/rice_leaf")
    pulse_source = Path("datasets/praveen_kumar_reddy/pluses")
    
    # Target directory for mixed dataset
    target_dir = Path("datasets/mixed_dataset")
    
    # Create train/val/test splits
    train_dir = target_dir / "train"
    val_dir = target_dir / "val"
    test_dir = target_dir / "test"
    
    # Clean up if exists
    if target_dir.exists():
        shutil.rmtree(target_dir)
    
    # Select 3 rice leaf disease classes (50 images each)
    rice_classes = ['Bacterialblight', 'Blast', 'Brownspot']
    
    # Select 1 pulse class (100 images) - let's use black_gram healthy
    pulse_class = 'black_gram_healthy'
    pulse_class_path = pulse_source / 'black_gram' / 'healthy'
    
    print("Preparing mixed dataset...")
    print(f"Rice classes: {rice_classes} (50 images each)")
    print(f"Pulse class: {pulse_class} (100 images)")
    
    # Process rice leaf classes
    for class_name in rice_classes:
        source_class_dir = rice_source / class_name
        
        # Get all images from this class
        image_files = list(source_class_dir.glob("*.jpg")) + \
                     list(source_class_dir.glob("*.jpeg")) + \
                     list(source_class_dir.glob("*.png")) + \
                     list(source_class_dir.glob("*.JPG"))
        
        print(f"\n{class_name}: Found {len(image_files)} images")
        
        # Randomly select 50 images
        if len(image_files) >= 50:
            selected_images = random.sample(image_files, 50)
        else:
            print(f"Warning: Only {len(image_files)} images available for {class_name}")
            selected_images = image_files
        
        # Split: 35 train, 8 val, 7 test
        train_images = selected_images[:35]
        val_images = selected_images[35:43]
        test_images = selected_images[43:50]
        
        # Create directories
        (train_dir / class_name).mkdir(parents=True, exist_ok=True)
        (val_dir / class_name).mkdir(parents=True, exist_ok=True)
        (test_dir / class_name).mkdir(parents=True, exist_ok=True)
        
        # Copy images
        for img in train_images:
            shutil.copy2(img, train_dir / class_name / img.name)
        for img in val_images:
            shutil.copy2(img, val_dir / class_name / img.name)
        for img in test_images:
            shutil.copy2(img, test_dir / class_name / img.name)
        
        print(f"  Train: {len(train_images)}, Val: {len(val_images)}, Test: {len(test_images)}")
    
    # Process pulse class (100 images)
    if pulse_class_path.exists():
        image_files = list(pulse_class_path.glob("*.jpg")) + \
                     list(pulse_class_path.glob("*.jpeg")) + \
                     list(pulse_class_path.glob("*.png")) + \
                     list(pulse_class_path.glob("*.JPG"))
        
        print(f"\n{pulse_class}: Found {len(image_files)} images")
        
        # Randomly select 100 images
        if len(image_files) >= 100:
            selected_images = random.sample(image_files, 100)
        else:
            print(f"Warning: Only {len(image_files)} images available for {pulse_class}")
            selected_images = image_files
        
        # Split: 70 train, 15 val, 15 test
        train_images = selected_images[:70]
        val_images = selected_images[70:85]
        test_images = selected_images[85:100]
        
        # Create directories
        (train_dir / pulse_class).mkdir(parents=True, exist_ok=True)
        (val_dir / pulse_class).mkdir(parents=True, exist_ok=True)
        (test_dir / pulse_class).mkdir(parents=True, exist_ok=True)
        
        # Copy images
        for img in train_images:
            shutil.copy2(img, train_dir / pulse_class / img.name)
        for img in val_images:
            shutil.copy2(img, val_dir / pulse_class / img.name)
        for img in test_images:
            shutil.copy2(img, test_dir / pulse_class / img.name)
        
        print(f"  Train: {len(train_images)}, Val: {len(val_images)}, Test: {len(test_images)}")
    else:
        print(f"\nError: Pulse class directory not found: {pulse_class_path}")
        return
    
    print(f"\nMixed dataset prepared at: {target_dir}")
    print("\nDirectory structure:")
    for split in ['train', 'val', 'test']:
        split_dir = target_dir / split
        total = 0
        for class_dir in sorted(split_dir.iterdir()):
            if class_dir.is_dir():
                count = len(list(class_dir.glob("*")))
                total += count
                print(f"  {split}/{class_dir.name}: {count} images")
        print(f"  {split} Total: {total} images")
    
    return target_dir

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    prepare_mixed_dataset()
