import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
import albumentations as A
from albumentations.pytorch import ToTensorV2
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np

from dataset import BUSIDataset, visualize_sample
from model import UNet, count_parameters

# ==================== КОНФИГУРАЦИЯ ====================
# Путь к датасету 
DATA_ROOT = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/project/data/Dataset_BUSI_with_GT"

IMAGE_SIZE = 128      # можно увеличить до 256, если хватит памяти
BATCH_SIZE = 8        # для RTX 3050 Ti 4GB
NUM_EPOCHS = 60
LEARNING_RATE = 0.001
NUM_CLASSES = 2
NUM_WORKERS = 2

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")
if device.type == 'cuda':
    print(f"GPU: {torch.cuda.get_device_name(0)}")
    print(f"VRAM: {torch.cuda.get_device_properties(0).total_memory / 1024**3:.1f} GB")

# ==================== МЕТРИКИ ====================
def calculate_iou(pred_mask, true_mask):
    """IoU для бинарной сегментации"""
    intersection = ((pred_mask == 1) & (true_mask == 1)).sum().item()
    union = ((pred_mask == 1) | (true_mask == 1)).sum().item()
    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    return intersection / union

def calculate_dice(pred_mask, true_mask):
    """Dice coefficient для бинарной сегментации"""
    intersection = ((pred_mask == 1) & (true_mask == 1)).sum().item()
    pred_sum = (pred_mask == 1).sum().item()
    true_sum = (true_mask == 1).sum().item()
    if pred_sum + true_sum == 0:
        return 1.0
    return 2 * intersection / (pred_sum + true_sum)

def calculate_accuracy(pred_mask, true_mask):
    """Accuracy (процент правильно предсказанных пикселей)"""
    correct = (pred_mask == true_mask).sum().item()
    total = pred_mask.numel()
    return correct / total

def evaluate(model, dataloader, device):
    """Оценка модели на датасете"""
    model.eval()
    total_iou = 0.0
    total_dice = 0.0
    total_acc = 0.0
    
    with torch.no_grad():
        for images, masks in dataloader:
            images = images.to(device)
            masks = masks.to(device)
            
            logits = model(images)
            probs = torch.softmax(logits, dim=1)[:, 1, :, :]
            preds = (probs > 0.5).long()
            
            for i in range(images.size(0)):
                total_iou += calculate_iou(preds[i], masks[i])
                total_dice += calculate_dice(preds[i], masks[i])
                total_acc += calculate_accuracy(preds[i], masks[i])
    
    n_samples = len(dataloader.dataset)
    return total_iou / n_samples, total_dice / n_samples, total_acc / n_samples

# ==================== ТРАНСФОРМАЦИИ ====================
train_transform = A.Compose([
    A.Resize(IMAGE_SIZE, IMAGE_SIZE),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.Normalize(mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

val_transform = A.Compose([
    A.Resize(IMAGE_SIZE, IMAGE_SIZE),
    A.Normalize(mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# ==================== ЗАГРУЗКА ДАННЫХ ====================
print("\nЗагрузка датасета BUSI...")
full_dataset = BUSIDataset(DATA_ROOT, transform=train_transform)
visualize_sample(full_dataset, 0)

train_size = int(0.8 * len(full_dataset))
val_size = int(0.1 * len(full_dataset))
test_size = len(full_dataset) - train_size - val_size

train_dataset, val_dataset, test_dataset = random_split(
    full_dataset, [train_size, val_size, test_size]
)

# Для валидации используем transform без аугментаций
val_dataset.dataset.transform = val_transform
test_dataset.dataset.transform = val_transform

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True,
                          num_workers=NUM_WORKERS, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False,
                        num_workers=NUM_WORKERS, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False,
                         num_workers=NUM_WORKERS, pin_memory=True)

print(f"Train: {len(train_dataset)} изображений")
print(f"Val: {len(val_dataset)} изображений")
print(f"Test: {len(test_dataset)} изображений")

# ==================== ПРОВЕРКА ДАННЫХ ====================
print("\nПроверка данных...")
image, mask = train_dataset[0]
print(f"Image shape: {image.shape}")
print(f"Mask shape: {mask.shape}")
print(f"Уникальные классы: {torch.unique(mask)}")

# ==================== СОЗДАНИЕ МОДЕЛИ ====================
print("\nСоздание модели...")
model = UNet(n_channels=3, n_classes=2)
x = torch.randn(1, 3, 128, 128)
y = model(x)
print(x.shape, "→", y.shape)

model = UNet(n_channels=3, n_classes=NUM_CLASSES)
model = model.to(device)
print(f"Параметров: {count_parameters(model):,}")

# ==================== ФУНКЦИЯ ПОТЕРЬ ====================
# Взвешенная loss для борьбы с дисбалансом классов
from sklearn.utils.class_weight import compute_class_weight

# Собираем пиксели из тренировочного датасета
all_pixels = []
for i in range(len(train_dataset)):  # Лучше по всем маскам
    _, mask = train_dataset[i]
    all_pixels.extend(mask.flatten().cpu().numpy())  # flatten() превращает в 1D

class_weights = compute_class_weight(
    'balanced',
    classes=np.array([0, 1]),
    y=np.array(all_pixels)  
)
class_weights = torch.tensor(class_weights, dtype=torch.float).to(device)
print(f"Веса классов: {class_weights}")

criterion = nn.CrossEntropyLoss(weight=class_weights)
optimizer = torch.optim.Adam(model.parameters(), lr=LEARNING_RATE)
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)

# ==================== ОБУЧЕНИЕ ====================
print("\nНачало обучения...")
os.makedirs('checkpoints', exist_ok=True)

train_losses = []
val_ious = []
val_accs = []
best_val_iou = 0.0
patience_counter = 0



for epoch in range(NUM_EPOCHS):
    # Training
    model.train()
    epoch_loss = 0.0
    progress_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{NUM_EPOCHS}')
    
    for images, masks in progress_bar:
        images = images.to(device)
        masks = masks.to(device)
        
        logits = model(images)
        loss = criterion(logits, masks)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        epoch_loss += loss.item()
        progress_bar.set_postfix({'loss': loss.item()})
    
    avg_train_loss = epoch_loss / len(train_loader)
    train_losses.append(avg_train_loss)
    
    # Validation
    val_iou, val_dice, val_acc = evaluate(model, val_loader, device)
    val_ious.append(val_iou)
    val_accs.append(val_acc)
    
    # Save best model
    if val_iou > best_val_iou:
        best_val_iou = val_iou
        torch.save(model.state_dict(), 'checkpoints/best_model.pth')
        patience_counter = 0
        print(f"\n*** Сохранена лучшая модель! Val IoU: {val_iou:.4f}, Val Acc: {val_acc:.4f} ***")
    else:
        patience_counter += 1
    
    scheduler.step(avg_train_loss)
    
    print(f"\nEpoch {epoch+1}/{NUM_EPOCHS}")
    print(f"Train Loss: {avg_train_loss:.4f}")
    print(f"Val IoU: {val_iou:.4f}, Val Dice: {val_dice:.4f}, Val Acc: {val_acc:.4f}")
    print(f"Лучший Val IoU: {best_val_iou:.4f}")
    print("-" * 60)
    
    # Ранняя остановка
    if patience_counter >= 10:
        print(f"Ранняя остановка на эпохе {epoch+1}")
        break

# ==================== ФИНАЛЬНАЯ ОЦЕНКА ====================
print("\nЗагрузка лучшей модели для финальной оценки...")
model.load_state_dict(torch.load('checkpoints/best_model.pth'))

test_iou, test_dice, test_acc = evaluate(model, test_loader, device)
print(f"\n{'='*40}")
print(f"ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ НА ТЕСТОВОЙ ВЫБОРКЕ")
print(f"{'='*40}")
print(f"Test IoU:       {test_iou:.4f} ({test_iou*100:.1f}%)")
print(f"Test Dice:      {test_dice:.4f} ({test_dice*100:.1f}%)")
print(f"Test Accuracy:  {test_acc:.4f} ({test_acc*100:.1f}%)")
print(f"{'='*40}")

# ==================== ГРАФИКИ ====================
plt.figure(figsize=(15, 5))

plt.subplot(1, 3, 1)
plt.plot(train_losses, label='Train Loss', color='blue')
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss')
plt.legend()
plt.grid(True)

plt.subplot(1, 3, 2)
plt.plot(val_ious, label='Val IoU', color='green')
plt.xlabel('Epoch')
plt.ylabel('IoU')
plt.title('Validation IoU')
plt.legend()
plt.grid(True)

plt.subplot(1, 3, 3)
plt.plot(val_accs, label='Val Accuracy', color='red')
plt.xlabel('Epoch')
plt.ylabel('Accuracy')
plt.title('Validation Accuracy')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.savefig('training_curves.png', dpi=150)
plt.show()

print("\n Обучение завершено!")
print(f"Модель сохранена в: checkpoints/best_model.pth")
print(f"Графики сохранены в: training_curves.png")