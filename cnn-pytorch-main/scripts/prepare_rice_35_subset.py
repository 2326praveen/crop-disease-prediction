"""
Prepare rice leaf dataset with 3 classes of 35 images each
"""
import shutil
import random
from pathlib import Path

def prepare_rice_35_subset():
    source_dir = Path("datasets/praveen_kumar_reddy/rice_leaf")
    target_dir = Path("datasets/rice_leaf_subset")

    train_dir = target_dir / "train"
    val_dir = target_dir / "val"
    test_dir = target_dir / "test"

    if target_dir.exists():
        shutil.rmtree(target_dir)

    selected_classes = ['Bacterialblight', 'Blast', 'Brownspot']
    print("Preparing rice leaf subset dataset (35 images/class)...")
    print(f"Selected classes: {selected_classes}")

    for class_name in selected_classes:
        source_class_dir = source_dir / class_name
        image_files = list(source_class_dir.glob("*.jpg")) + \
                      list(source_class_dir.glob("*.jpeg")) + \
                      list(source_class_dir.glob("*.png")) + \
                      list(source_class_dir.glob("*.JPG"))

        print(f"\n{class_name}: Found {len(image_files)} images")

        if len(image_files) >= 35:
            selected_images = random.sample(image_files, 35)
        else:
            print(f"Warning: Only {len(image_files)} images available for {class_name}")
            selected_images = image_files

        # Split: 24 train, 6 val, 5 test (total 35)
        train_images = selected_images[:24]
        val_images = selected_images[24:30]
        test_images = selected_images[30:35]

        (train_dir / class_name).mkdir(parents=True, exist_ok=True)
        (val_dir / class_name).mkdir(parents=True, exist_ok=True)
        (test_dir / class_name).mkdir(parents=True, exist_ok=True)

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
    random.seed(42)
    prepare_rice_35_subset()
