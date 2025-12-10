"""
Prepare a subset of rice leaf dataset with 3 classes of 50 images each
"""
import os
import shutil
import random
from pathlib import Path

def prepare_rice_50_subset():
    # Source directory
    source_dir = Path("datasets/praveen_kumar_reddy/rice_leaf")
    
    # Target directory for subset
    target_dir = Path("datasets/rice_leaf_subset")
    
    # Create train/val/test splits
    train_dir = target_dir / "train"
    val_dir = target_dir / "val"
    test_dir = target_dir / "test"
    
    # Clean up if exists
    if target_dir.exists():
        shutil.rmtree(target_dir)
    
    # Select 3 classes
    selected_classes = ['Bacterialblight', 'Blast', 'Brownspot']
    
    print("Preparing rice leaf subset dataset...")
    print(f"Selected classes: {selected_classes}")
    
    for class_name in selected_classes:
        source_class_dir = source_dir / class_name
        
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
    
    print(f"\nDataset prepared at: {target_dir}")
    print("\nDirectory structure:")
    for split in ['train', 'val', 'test']:
        split_dir = target_dir / split
        total = 0
        for class_dir in split_dir.iterdir():
            count = len(list(class_dir.glob("*")))
            total += count
            print(f"  {split}/{class_dir.name}: {count} images")
        print(f"  {split} Total: {total} images")
    
    return target_dir

if __name__ == "__main__":
    random.seed(42)  # For reproducibility
    prepare_rice_50_subset()
