"""
Generate graphs from training history
"""
import json
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path

def plot_training_history(history_path=None, output_path=None):
    """
    Plot training and validation metrics from history JSON
    
    Args:
        history_path: Path to training_history.json (default: models/training_history.json)
        output_path: Path to save plot (default: models/training_history.png)
    """
    # Set default paths
    base_dir = Path(__file__).parent.parent
    if history_path is None:
        history_path = base_dir / 'models' / 'training_history.json'
    if output_path is None:
        output_path = base_dir / 'models' / 'training_history.png'
    
    # Load training history
    print(f"Loading training history from: {history_path}")
    with open(history_path, 'r') as f:
        history = json.load(f)
    
    # Extract metrics
    train_loss = history['train_loss']
    train_acc = [acc * 100 for acc in history['train_acc']]  # Convert to percentage
    val_loss = history['val_loss']
    val_acc = [acc * 100 for acc in history['val_acc']]  # Convert to percentage
    epochs = range(1, len(train_loss) + 1)
    
    # Calculate best metrics
    best_train_acc = max(train_acc)
    best_val_acc = max(val_acc)
    best_train_epoch = train_acc.index(best_train_acc) + 1
    best_val_epoch = val_acc.index(best_val_acc) + 1
    
    # Create figure with 2 subplots
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
    fig.suptitle('Training History', fontsize=16, fontweight='bold')
    
    # Plot 1: Loss
    ax1.plot(epochs, train_loss, 'b-o', label='Training Loss', linewidth=2, markersize=4)
    ax1.plot(epochs, val_loss, 'r-s', label='Validation Loss', linewidth=2, markersize=4)
    ax1.set_xlabel('Epoch', fontsize=12)
    ax1.set_ylabel('Loss', fontsize=12)
    ax1.set_title('Model Loss', fontsize=14, fontweight='bold')
    ax1.legend(fontsize=10)
    ax1.grid(True, alpha=0.3)
    
    # Add min loss annotation
    min_train_loss = min(train_loss)
    min_val_loss = min(val_loss)
    ax1.axhline(y=min_train_loss, color='b', linestyle='--', alpha=0.3)
    ax1.axhline(y=min_val_loss, color='r', linestyle='--', alpha=0.3)
    
    # Plot 2: Accuracy
    ax2.plot(epochs, train_acc, 'b-o', label='Training Accuracy', linewidth=2, markersize=4)
    ax2.plot(epochs, val_acc, 'r-s', label='Validation Accuracy', linewidth=2, markersize=4)
    ax2.set_xlabel('Epoch', fontsize=12)
    ax2.set_ylabel('Accuracy (%)', fontsize=12)
    ax2.set_title('Model Accuracy', fontsize=14, fontweight='bold')
    ax2.legend(fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.set_ylim([0, 105])  # Set y-axis from 0 to 100%
    
    # Mark best accuracy points
    ax2.plot(best_train_epoch, best_train_acc, 'b*', markersize=15, label=f'Best Train: {best_train_acc:.1f}%')
    ax2.plot(best_val_epoch, best_val_acc, 'r*', markersize=15, label=f'Best Val: {best_val_acc:.1f}%')
    ax2.legend(fontsize=10)
    
    # Add horizontal lines for best accuracies
    ax2.axhline(y=best_train_acc, color='b', linestyle='--', alpha=0.3)
    ax2.axhline(y=best_val_acc, color='r', linestyle='--', alpha=0.3)
    
    plt.tight_layout()
    
    # Save figure
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Training history plot saved to: {output_path}")
    
    # Print summary statistics
    print("\n" + "=" * 60)
    print("TRAINING SUMMARY")
    print("=" * 60)
    print(f"Total Epochs: {len(epochs)}")
    print(f"\nBest Training Accuracy: {best_train_acc:.2f}% (Epoch {best_train_epoch})")
    print(f"Best Validation Accuracy: {best_val_acc:.2f}% (Epoch {best_val_epoch})")
    print(f"\nFinal Training Accuracy: {train_acc[-1]:.2f}%")
    print(f"Final Validation Accuracy: {val_acc[-1]:.2f}%")
    print(f"\nLowest Training Loss: {min_train_loss:.4f}")
    print(f"Lowest Validation Loss: {min_val_loss:.4f}")
    print(f"\nFinal Training Loss: {train_loss[-1]:.4f}")
    print(f"Final Validation Loss: {val_loss[-1]:.4f}")
    print("=" * 60)
    
    # Show plot
    plt.show()
    
    return fig

def plot_all_histories():
    """Plot all training history files in the models directory"""
    base_dir = Path(__file__).parent.parent
    models_dir = base_dir / 'models'
    
    # Find all training history files
    history_files = list(models_dir.glob('training_history*.json'))
    
    if not history_files:
        print("No training history files found!")
        return
    
    print(f"Found {len(history_files)} training history file(s):")
    for i, file in enumerate(history_files, 1):
        print(f"  {i}. {file.name}")
    
    # Plot each one
    for history_file in history_files:
        output_file = history_file.with_suffix('.png')
        print(f"\n{'='*60}")
        print(f"Processing: {history_file.name}")
        print('='*60)
        plot_training_history(history_file, output_file)

if __name__ == "__main__":
    import sys
    
    # Check if matplotlib is available
    try:
        import matplotlib
        matplotlib.use('TkAgg')  # Use TkAgg backend for interactive display
    except ImportError:
        print("Error: matplotlib is not installed!")
        print("Install it with: pip install matplotlib")
        sys.exit(1)
    
    # Plot all training histories
    plot_all_histories()
