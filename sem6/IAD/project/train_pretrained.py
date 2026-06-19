import os
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, random_split
import albumentations as A
from albumentations.pytorch import ToTensorV2
import matplotlib.pyplot as plt
from tqdm import tqdm
import numpy as np
from sklearn.utils.class_weight import compute_class_weight

# Импорт ваших модулей
from dataset import BUSIDataset
from model_pretrained import UNetPretrained  # Новая модель с ResNet34


# ==================== КОНФИГУРАЦИЯ ====================
DATA_ROOT = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/project/data/Dataset_BUSI_with_GT"
IMAGE_SIZE = 128
BATCH_SIZE = 8
NUM_EPOCHS = 60
NUM_CLASSES = 2
NUM_WORKERS = 2

#  Ключевое отличие: раздельные learning rate
ENCODER_LR = 1e-4   # Пониженный LR для предобученных весов
DECODER_LR = 1e-3   # Обычный LR для нового decoder'а

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Устройство: {device}")

# ==================== ТРАНСФОРМАЦИИ ====================
train_transform = A.Compose([
    A.Resize(IMAGE_SIZE, IMAGE_SIZE),
    A.HorizontalFlip(p=0.5),
    A.VerticalFlip(p=0.5),
    A.RandomRotate90(p=0.5),
    A.RandomBrightnessContrast(p=0.3),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(), # Меняет формат с (H, W, C) на (C, H, W)
])

val_transform = A.Compose([
    A.Resize(IMAGE_SIZE, IMAGE_SIZE),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# ==================== ЗАГРУЗКА ДАННЫХ ====================
print("\nЗагрузка датасета BUSI...")
full_dataset = BUSIDataset(DATA_ROOT, transform=train_transform)

image, mask = full_dataset[0]
print(f"image shape: {image.shape}") # ожидается: [3, 128, 128]
print(f"mask shape: {mask.shape}") # ожидается: [128, 128]
print(f"mask dtype: {mask.dtype}") # ожидается: torch.int64
print(f"mask classes: {mask.unique()}") # значения от 0 до num_classes-1

train_size = int(0.8 * len(full_dataset))
val_size = int(0.1 * len(full_dataset))
test_size = len(full_dataset) - train_size - val_size

train_dataset, val_dataset, test_dataset = random_split(
    full_dataset, [train_size, val_size, test_size]
)

# Применяем val-трансформации к валидации и тесту
val_dataset.dataset.transform = val_transform
test_dataset.dataset.transform = val_transform

train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True,
                          num_workers=NUM_WORKERS, pin_memory=True)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False,
                        num_workers=NUM_WORKERS, pin_memory=True)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False,
                         num_workers=NUM_WORKERS, pin_memory=True)

print(f"✅ Train: {len(train_dataset)} | Val: {len(val_dataset)} | Test: {len(test_dataset)}")

# ==================== СОЗДАНИЕ МОДЕЛИ ====================
print("\n Создание модели U-Net + ResNet34...")
model = UNetPretrained(n_classes=NUM_CLASSES, freeze_encoder=False)  # freeze_encoder=True если хотите заморозить encoder
model = model.to(device)

# Подсчёт параметров
def count_params(model):
    total = sum(p.numel() for p in model.parameters())
    trainable = sum(p.numel() for p in model.parameters() if p.requires_grad)
    return total, trainable

total_params, trainable_params = count_params(model)
print(f"Всего параметров: {total_params:,} | Обучаемых: {trainable_params:,}")

# ==================== РАЗДЕЛЬНЫЕ LEARNING RATE ====================
print("\n Настройка оптимизатора с раздельными LR...")

# Разделяем параметры на encoder (предобученный) и decoder (новый)
encoder_params = []
decoder_params = []

for name, param in model.named_parameters():
    if any(x in name for x in ['enc1', 'enc2', 'enc3', 'enc4', 'bottleneck']):
        # Параметры из предобученного ResNet34
        if param.requires_grad:
            encoder_params.append(param)
    else:
        # Параметры нового decoder'а
        decoder_params.append(param)

print(f"   • Encoder параметров: {sum(p.numel() for p in encoder_params):,}")
print(f"   • Decoder параметров: {sum(p.numel() for p in decoder_params):,}")

optimizer = torch.optim.Adam([
    {'params': encoder_params, 'lr': ENCODER_LR},
    {'params': decoder_params, 'lr': DECODER_LR},
])

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
scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode='min', patience=5, factor=0.5)

# ==================== ОБУЧЕНИЕ ====================
print("\n Начало обучения...")
os.makedirs('checkpoints', exist_ok=True)

train_losses = []
val_ious = []
val_accs = []
best_val_iou = 0.0
patience_counter = 0

def calculate_iou(pred_mask, true_mask):
    intersection = ((pred_mask == 1) & (true_mask == 1)).sum().item()
    union = ((pred_mask == 1) | (true_mask == 1)).sum().item()
    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    return intersection / union

def calculate_dice(pred_mask, true_mask):
    intersection = ((pred_mask == 1) & (true_mask == 1)).sum().item()
    pred_sum = (pred_mask == 1).sum().item()
    true_sum = (true_mask == 1).sum().item()
    if pred_sum + true_sum == 0:
        return 1.0
    return 2 * intersection / (pred_sum + true_sum)

def calculate_accuracy(pred_mask, true_mask):
    correct = (pred_mask == true_mask).sum().item()
    total = pred_mask.numel()
    return correct / total

def evaluate(model, dataloader, device):
    model.eval()
    total_iou = 0.0
    total_dice = 0.0
    total_acc = 0.0
    with torch.no_grad():
        for images, masks in dataloader:
            images = images.to(device)
            masks = masks.to(device)
            logits = model(images)
            preds = logits.argmax(dim=1)
            for i in range(images.size(0)):
                total_iou += calculate_iou(preds[i], masks[i])
                total_dice += calculate_dice(preds[i], masks[i])
                total_acc += calculate_accuracy(preds[i], masks[i])
    n_samples = len(dataloader.dataset)
    return total_iou / n_samples, total_dice / n_samples, total_acc / n_samples

for epoch in range(NUM_EPOCHS):
    # ===== TRAINING =====
    model.train()
    epoch_loss = 0.0
    progress_bar = tqdm(train_loader, desc=f'Epoch {epoch+1}/{NUM_EPOCHS} [Train]')
    
    for images, masks in progress_bar:
        images = images.to(device)
        masks = masks.to(device)
        
        logits = model(images)  # [B, num_classes, H, W]
        loss = criterion(logits, masks)  # masks: [B, H, W], long
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        epoch_loss += loss.item()
        progress_bar.set_postfix({'loss': f'{loss.item():.4f}'})
    
    avg_train_loss = epoch_loss / len(train_loader)
    train_losses.append(avg_train_loss)
    
    # ===== VALIDATION =====
    model.eval()
    val_iou, val_dice, val_acc = evaluate(model, val_loader, device)
    val_ious.append(val_iou)
    val_accs.append(val_acc)
    
    # ===== SAVE BEST =====
    if val_iou > best_val_iou:
        best_val_iou = val_iou
        torch.save(model.state_dict(), 'checkpoints/best_model_pretrained.pth')
        patience_counter = 0
        print(f"\n💾 Сохранена лучшая модель! Val IoU: {val_iou:.4f}")
    else:
        patience_counter += 1
    
    scheduler.step(avg_train_loss)
    
    # ===== LOG =====
    print(f"\n Epoch {epoch+1}/{NUM_EPOCHS}")
    print(f"   Train Loss: {avg_train_loss:.4f}")
    print(f"   Val IoU:    {val_iou:.4f} | Dice: {val_dice:.4f} | Acc: {val_acc:.4f}")
    print(f"   Best IoU:   {best_val_iou:.4f} | Patience: {patience_counter}/10")
    print("-" * 60)
    
    # Early stopping
    if patience_counter >= 10:
        print(f" Ранняя остановка на эпохе {epoch+1}")
        break

# ==================== ФИНАЛЬНАЯ ОЦЕНКА ====================
print("\nЗагрузка лучшей модели для финальной оценки...")
model.load_state_dict(torch.load('checkpoints/best_model_pretrained.pth', map_location=device))
test_iou, test_dice, test_acc = evaluate(model, test_loader, device)

print(f"\n{'='*50}")
print(f"ФИНАЛЬНЫЕ РЕЗУЛЬТАТЫ (U-Net + ResNet34)")
print(f"{'='*50}")
print(f"Test IoU:       {test_iou:.4f} ({test_iou*100:.1f}%)")
print(f"Test Dice:      {test_dice:.4f} ({test_dice*100:.1f}%)")
print(f"Test Accuracy:  {test_acc:.4f} ({test_acc*100:.1f}%)")
print(f"{'='*50}")

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
plt.savefig('training_curves_pretrained.png', dpi=150)
plt.show()

print("\nОбучение завершено!")
print(f" Модель сохранена: checkpoints/best_model_pretrained.pth")
print(f"Графики: training_curves_pretrained.png")