import torch
import matplotlib.pyplot as plt
import numpy as np
from torch.utils.data import DataLoader
import albumentations as A
from albumentations.pytorch import ToTensorV2

# Импорт ваших модулей
from model import UNet
from dataset import BUSIDataset

# ==================== ЗАГРУЗКА МОДЕЛИ ====================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")
DATA_ROOT = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/project/data/Dataset_BUSI_with_GT"

# Создаём модель с 2 классами
model = UNet(n_channels=3, n_classes=2)
model.load_state_dict(torch.load('checkpoints/best_model.pth', map_location=device))
model.to(device)
model.eval()
print("Модель загружена")

# ==================== ЗАГРУЗКА ДАННЫХ ====================
# Трансформации для валидации (без аугментаций)
val_transform = A.Compose([
    A.Resize(128, 128),
    A.Normalize(mean=(0.485, 0.456, 0.406),
                std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# Загружаем датасет
dataset = BUSIDataset(DATA_ROOT, transform=val_transform)

# Создаём валидационную выборку (20% от датасета)
from torch.utils.data import random_split
val_size = int(0.2 * len(dataset))
train_size = len(dataset) - val_size
_, val_dataset = random_split(dataset, [train_size, val_size])

print(f"Всего изображений: {len(dataset)}")
print(f"Валидационная выборка: {len(val_dataset)}")

# Создаём DataLoader для валидации
val_loader = DataLoader(val_dataset, batch_size=1, shuffle=False)
print(f"Готово к визуализации")

# ==================== ВИЗУАЛИЗАЦИЯ ====================
def denormalize(image):
    """Денормализация изображения для отображения"""
    mean = np.array([0.485, 0.456, 0.406])
    std = np.array([0.229, 0.224, 0.225])
    image = image * std + mean
    image = np.clip(image, 0, 1)
    return image

# Выбираем 6 изображений из валидационной выборки
num_samples = 6
images_to_show = []

with torch.no_grad():
    for i, (image, mask) in enumerate(val_loader):
        if i >= num_samples:
            break
        
        # Предсказание
        image_tensor = image.to(device)
        logits = model(image_tensor)
        pred_mask = logits.argmax(dim=1).squeeze(0).cpu().numpy()
        
        # Денормализация изображения для отображения
        img_display = image.squeeze(0).permute(1, 2, 0).numpy()
        img_display = denormalize(img_display)
        
        # Истинная маска
        true_mask = mask.squeeze(0).cpu().numpy()
        
        images_to_show.append((img_display, true_mask, pred_mask))

# ==================== ПОСТРОЕНИЕ ГРАФИКОВ ====================
fig, axes = plt.subplots(num_samples, 3, figsize=(15, 5*num_samples))

for i, (img, true_mask, pred_mask) in enumerate(images_to_show):
    # Исходное изображение
    axes[i, 0].imshow(img)
    axes[i, 0].set_title(f'Исходное изображение {i+1}', fontsize=12)
    axes[i, 0].axis('off')
    
    # Истинная маска
    im1 = axes[i, 1].imshow(true_mask, cmap='tab10', vmin=0, vmax=1)
    axes[i, 1].set_title(f'Истинная маска {i+1}', fontsize=12)
    axes[i, 1].axis('off')
    
    # Предсказанная маска
    im2 = axes[i, 2].imshow(pred_mask, cmap='tab10', vmin=0, vmax=1)
    axes[i, 2].set_title(f'Предсказанная маска {i+1}', fontsize=12)
    axes[i, 2].axis('off')

# Добавляем общий цветовой бар
cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
plt.colorbar(im2, cax=cbar_ax, ticks=[0, 1])
cbar_ax.set_yticklabels(['Фон (0)', 'Опухоль (1)'])

plt.suptitle('Результаты сегментации на валидационной выборке', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig('segmentation_results.png', dpi=150, bbox_inches='tight')
plt.subplots_adjust(hspace=0.5)
plt.show()

print("Визуализация сохранена в: segmentation_results.png")

# ==================== ДОПОЛНИТЕЛЬНО: ВЫВОД МЕТРИК ДЛЯ КАЖДОГО ИЗОБРАЖЕНИЯ ====================
print("\n" + "="*60)
print("Метрики для каждого изображения:")
print("="*60)

def calculate_iou(pred, true):
    intersection = ((pred == 1) & (true == 1)).sum()
    union = ((pred == 1) | (true == 1)).sum()
    if union == 0:
        return 1.0 if intersection == 0 else 0.0
    return intersection / union

def calculate_dice(pred, true):
    intersection = ((pred == 1) & (true == 1)).sum()
    pred_sum = (pred == 1).sum()
    true_sum = (true == 1).sum()
    if pred_sum + true_sum == 0:
        return 1.0
    return 2 * intersection / (pred_sum + true_sum)

for i, (_, true_mask, pred_mask) in enumerate(images_to_show):
    iou = calculate_iou(pred_mask, true_mask)
    dice = calculate_dice(pred_mask, true_mask)
    print(f"Изображение {i+1}: IoU = {iou:.4f}, Dice = {dice:.4f}")

print("="*60)