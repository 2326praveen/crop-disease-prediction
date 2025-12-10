"""
Transfer Learning Training script for the Crop Disease Classifier.

This script uses a pre-trained ResNet18 model for better accuracy on small datasets.
"""

import sys
import os
import json
import time
from pathlib import Path
from datetime import datetime

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
from PIL import Image
import matplotlib.pyplot as plt
import torchvision.models as models

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.transforms import ImageTransformer


class RiceLeafDataset(Dataset):
    """Dataset class for rice leaf disease images."""
    
    def __init__(self, root_dir, transform=None):
        """
        Args:
            root_dir (str): Directory with disease class subdirectories
            transform (callable, optional): Optional transform to be applied on images
        """
        self.root_dir = Path(root_dir)
        self.transform = transform
        
        # Get class names from subdirectories
        self.classes = sorted([d.name for d in self.root_dir.iterdir() if d.is_dir()])
        self.class_to_idx = {cls_name: idx for idx, cls_name in enumerate(self.classes)}
        
        # Collect all image paths and labels
        self.samples = []
        for class_name in self.classes:
            class_dir = self.root_dir / class_name
            for img_path in class_dir.glob('*.jpg'):
                self.samples.append((str(img_path), self.class_to_idx[class_name]))
            for img_path in class_dir.glob('*.JPG'):
                self.samples.append((str(img_path), self.class_to_idx[class_name]))
            for img_path in class_dir.glob('*.jpeg'):
                self.samples.append((str(img_path), self.class_to_idx[class_name]))
            for img_path in class_dir.glob('*.png'):
                self.samples.append((str(img_path), self.class_to_idx[class_name]))
    
    def __len__(self):
        return len(self.samples)
    
    def __getitem__(self, idx):
        img_path, label = self.samples[idx]
        image = Image.open(img_path).convert('RGB')
        
        if self.transform:
            image = self.transform(image)
        
        return image, label


def get_image_transformer(config):
    """Get image transformer from config."""
    img_size = config.get('img_size', 224)
    return ImageTransformer(
        target_size=(img_size, img_size),
        mean=config.get('mean', [0.485, 0.456, 0.406]),
        std=config.get('std', [0.229, 0.224, 0.225])
    )


def train_epoch(model, dataloader, criterion, optimizer, device):
    """Train for one epoch."""
    model.train()
    running_loss = 0.0
    correct = 0
    total = 0
    
    for inputs, labels in dataloader:
        inputs, labels = inputs.to(device), labels.to(device)
        
        # Zero gradients
        optimizer.zero_grad()
        
        # Forward pass
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        
        # Backward pass and optimize
        loss.backward()
        # Gradient clipping for stability
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        optimizer.step()
        
        # Statistics
        running_loss += loss.item() * inputs.size(0)
        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    
    return epoch_loss, epoch_acc


def validate(model, dataloader, criterion, device):
    """Validate the model."""
    model.eval()
    running_loss = 0.0
    correct = 0
    total = 0
    
    with torch.no_grad():
        for inputs, labels in dataloader:
            inputs, labels = inputs.to(device), labels.to(device)
            
            # Forward pass
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            
            # Statistics
            running_loss += loss.item() * inputs.size(0)
            _, predicted = torch.max(outputs, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    epoch_loss = running_loss / total
    epoch_acc = correct / total
    
    return epoch_loss, epoch_acc


def save_training_plot(history, save_path):
    """Save training history plots."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Plot loss
    ax1.plot(history['train_loss'], label='Train Loss')
    ax1.plot(history['val_loss'], label='Val Loss')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Loss')
    ax1.set_title('Training and Validation Loss')
    ax1.legend()
    ax1.grid(True)
    
    # Plot accuracy
    ax2.plot(history['train_acc'], label='Train Acc')
    ax2.plot(history['val_acc'], label='Val Acc')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Accuracy')
    ax2.set_title('Training and Validation Accuracy')
    ax2.legend()
    ax2.grid(True)
    
    plt.tight_layout()
    plt.savefig(save_path)
    print(f"Training history plot saved to: {save_path}")


def train_model():
    """Main training function with transfer learning."""
    
    # Load configuration
    base_dir = Path(__file__).parent.parent
    config_path = base_dir / 'config' / 'model_config.json'
    
    with open(config_path, 'r') as f:
        config = json.load(f)
    
    print("=" * 60)
    print("Crop Disease Classifier - Transfer Learning Training")
    print("=" * 60)
    
    # Training hyperparameters - Optimized for small dataset
    BATCH_SIZE = 16
    NUM_EPOCHS = 30
    LEARNING_RATE = 0.001
    
    # Device configuration
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"\nDevice: {device}")
    
    # Load dataset
    print("\nLoading dataset...")
    dataset_path = base_dir / 'datasets' / 'rice_leaf_subset' / 'train'
    val_dataset_path = base_dir / 'datasets' / 'rice_leaf_subset' / 'val'
    
    # Create ImageTransformer
    image_transformer = get_image_transformer(config)
    
    # Get transforms from ImageTransformer
    train_transform = image_transformer.get_training_transforms()
    val_transform = image_transformer.get_inference_transforms()
    
    # Create train and validation datasets
    train_dataset = RiceLeafDataset(dataset_path, transform=train_transform)
    val_dataset = RiceLeafDataset(val_dataset_path, transform=val_transform)
    
    print(f"Training samples: {len(train_dataset)}")
    print(f"Validation samples: {len(val_dataset)}")
    print(f"Classes: {train_dataset.classes}")
    print(f"Number of classes: {len(train_dataset.classes)}")
    
    # Create data loaders
    train_loader = DataLoader(
        train_dataset,
        batch_size=BATCH_SIZE,
        shuffle=True,
        num_workers=0,
        pin_memory=False
    )
    
    val_loader = DataLoader(
        val_dataset,
        batch_size=BATCH_SIZE,
        shuffle=False,
        num_workers=0,
        pin_memory=False
    )
    
    # Initialize model with transfer learning
    print("\nInitializing ResNet18 model with transfer learning...")
    num_classes = len(train_dataset.classes)
    
    # Load pre-trained ResNet18
    model = models.resnet18(weights=models.ResNet18_Weights.IMAGENET1K_V1)
    
    # Freeze early layers (only train last few layers)
    for param in model.parameters():
        param.requires_grad = False
    
    # Replace final layer for our number of classes
    num_ftrs = model.fc.in_features
    model.fc = nn.Sequential(
        nn.Dropout(0.5),
        nn.Linear(num_ftrs, num_classes)
    )
    
    model = model.to(device)
    
    # Count trainable parameters
    trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
    total_params = sum(p.numel() for p in model.parameters())
    print(f"Trainable parameters: {trainable_params:,} / {total_params:,}")
    
    # Loss function and optimizer
    criterion = nn.CrossEntropyLoss()
    # Only optimize the classifier parameters
    optimizer = optim.Adam(model.fc.parameters(), lr=LEARNING_RATE, weight_decay=1e-4)
    # Learning rate scheduling
    scheduler = optim.lr_scheduler.StepLR(optimizer, step_size=10, gamma=0.1)
    
    # Training history
    history = {
        'train_loss': [],
        'train_acc': [],
        'val_loss': [],
        'val_acc': []
    }
    
    best_val_acc = 0.0
    best_model_path = base_dir / 'models' / 'best_model.pth'
    
    print("\n" + "=" * 60)
    print("Starting training...")
    print("=" * 60)
    
    start_time = time.time()
    
    for epoch in range(NUM_EPOCHS):
        epoch_start = time.time()
        
        # Train
        train_loss, train_acc = train_epoch(model, train_loader, criterion, optimizer, device)
        
        # Validate
        val_loss, val_acc = validate(model, val_loader, criterion, device)
        
        # Update learning rate
        scheduler.step()
        
        # Save history
        history['train_loss'].append(train_loss)
        history['train_acc'].append(train_acc)
        history['val_loss'].append(val_loss)
        history['val_acc'].append(val_acc)
        
        epoch_time = time.time() - epoch_start
        
        # Print progress
        print(f"\nEpoch [{epoch+1}/{NUM_EPOCHS}] ({epoch_time:.1f}s)")
        print(f"  Train Loss: {train_loss:.4f} | Train Acc: {train_acc:.4f}")
        print(f"  Val Loss:   {val_loss:.4f} | Val Acc:   {val_acc:.4f}")
        
        # Save best model
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'val_acc': val_acc,
                'val_loss': val_loss,
                'classes': train_dataset.classes,
                'num_classes': num_classes,
                'config': config
            }, best_model_path)
            print(f"  ✓ New best model saved! (Val Acc: {val_acc:.4f})")
    
    training_time = time.time() - start_time
    
    print("\n" + "=" * 60)
    print("Training completed!")
    print("=" * 60)
    print(f"Total training time: {training_time/60:.1f} minutes")
    print(f"Best validation accuracy: {best_val_acc:.4f}")
    print(f"Best model saved to: {best_model_path}")
    
    # Save training history plot
    plot_path = base_dir / 'models' / f'training_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.png'
    save_training_plot(history, plot_path)
    
    # Save training history as JSON
    history_path = base_dir / 'models' / f'training_history_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
    with open(history_path, 'w') as f:
        json.dump(history, f, indent=2)
    print(f"Training history saved to: {history_path}")


if __name__ == '__main__':
    train_model()
