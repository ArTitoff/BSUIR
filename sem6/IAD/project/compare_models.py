import torch
import torch.nn as nn
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader, random_split
import albumentations as A
from albumentations.pytorch import ToTensorV2
import os
from datetime import datetime

# Импорт ваших модулей
from model import UNet, count_parameters
from model_pretrained import UNetPretrained
from dataset import BUSIDataset

# ==================== КОНФИГУРАЦИЯ ====================
DATA_ROOT = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/project/data/Dataset_BUSI_with_GT"
IMAGE_SIZE = 128
BATCH_SIZE = 8
NUM_CLASSES = 2
NUM_WORKERS = 2

CHECKPOINT_SCRATCH = 'checkpoints/best_model.pth'
CHECKPOINT_PRETRAINED = 'checkpoints/best_model_pretrained.pth'

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"🔧 Устройство: {device}")

# ==================== ТРАНСФОРМАЦИИ ====================
test_transform = A.Compose([
    A.Resize(IMAGE_SIZE, IMAGE_SIZE),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),
])

# ==================== ЗАГРУЗКА ДАННЫХ ====================
print("\n Загрузка датасета...")
full_dataset = BUSIDataset(DATA_ROOT, transform=test_transform)

train_size = int(0.8 * len(full_dataset))
val_size = int(0.1 * len(full_dataset))
test_size = len(full_dataset) - train_size - val_size

_, _, test_dataset = random_split(full_dataset, [train_size, val_size, test_size])
test_dataset.dataset.transform = test_transform

test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, 
                         num_workers=NUM_WORKERS, pin_memory=True)

print(f" Тестовая выборка: {len(test_dataset)} изображений")

# ==================== МЕТРИКИ ====================
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

def calculate_iou_per_class(pred_mask, true_mask, num_classes=2):
    iou_per_class = []
    for c in range(num_classes):
        pred_c = (pred_mask == c)
        true_c = (true_mask == c)
        inter = (pred_c & true_c).sum().item()
        union = (pred_c | true_c).sum().item()
        if union == 0:
            iou_per_class.append(1.0 if inter == 0 else 0.0)
        else:
            iou_per_class.append(inter / union)
    return iou_per_class

def evaluate_model(model, dataloader, device, num_classes=2):
    """Полная оценка модели с метриками по классам"""
    model.eval()
    total_iou = 0.0
    total_dice = 0.0
    total_acc = 0.0
    class_iou = {c: [] for c in range(num_classes)}
    all_predictions = []
    
    with torch.no_grad():
        for images, masks in dataloader:
            images = images.to(device)
            masks = masks.to(device)
            
            logits = model(images)
            preds = logits.argmax(dim=1)
            
            for i in range(images.size(0)):
                pred, true = preds[i], masks[i]
                
                total_iou += calculate_iou(pred, true)
                total_dice += calculate_dice(pred, true)
                total_acc += calculate_accuracy(pred, true)
                
                iou_per_class = calculate_iou_per_class(pred, true, num_classes)
                for c in range(num_classes):
                    class_iou[c].append(iou_per_class[c])
                
                all_predictions.append({
                    'image': images[i].cpu(),
                    'pred': pred.cpu(),
                    'true': true.cpu(),
                    'iou': calculate_iou(pred, true)
                })
    
    n = len(dataloader.dataset)
    mean_iou_per_class = {c: np.mean(vals) if vals else 0.0 for c, vals in class_iou.items()}
    
    return {
        'iou': total_iou / n,
        'dice': total_dice / n,
        'acc': total_acc / n,
        'iou_per_class': mean_iou_per_class,
        'predictions': all_predictions
    }

def count_total_params(model):
    return sum(p.numel() for p in model.parameters())

def count_trainable_params(model):
    return sum(p.numel() for p in model.parameters() if p.requires_grad)

# ==================== ЗАГРУЗКА МОДЕЛЕЙ ====================
results = {}

# --- Модель 1: U-Net с нуля ---
print("\n🔹 Загрузка модели: U-Net (с нуля)...")
model_scratch = UNet(n_channels=3, n_classes=NUM_CLASSES).to(device)
try:
    model_scratch.load_state_dict(torch.load(CHECKPOINT_SCRATCH, map_location=device))
    print(f"Загружено из {CHECKPOINT_SCRATCH}")
    metrics_scratch = evaluate_model(model_scratch, test_loader, device, NUM_CLASSES)
    metrics_scratch['params_total'] = count_total_params(model_scratch)
    metrics_scratch['params_trainable'] = count_trainable_params(model_scratch)
    metrics_scratch['epochs'] = 60  # укажите реальное число эпох
    results['U-Net (с нуля)'] = metrics_scratch
    print(f"   → mIoU: {metrics_scratch['iou']:.4f}, Dice: {metrics_scratch['dice']:.4f}")
except FileNotFoundError:
    print(f" Файл {CHECKPOINT_SCRATCH} не найден!")

# --- Модель 2: U-Net + ResNet34 ---
print("\n🔹 Загрузка модели: U-Net + ResNet34...")
model_pretrained = UNetPretrained(n_classes=NUM_CLASSES, freeze_encoder=False).to(device)
try:
    model_pretrained.load_state_dict(torch.load(CHECKPOINT_PRETRAINED, map_location=device))
    print(f" Загружено из {CHECKPOINT_PRETRAINED}")
    metrics_pretrained = evaluate_model(model_pretrained, test_loader, device, NUM_CLASSES)
    metrics_pretrained['params_total'] = count_total_params(model_pretrained)
    metrics_pretrained['params_trainable'] = count_trainable_params(model_pretrained)
    metrics_pretrained['epochs'] = 60  # укажите реальное число эпох
    results['U-Net + ResNet34'] = metrics_pretrained
    print(f"   → mIoU: {metrics_pretrained['iou']:.4f}, Dice: {metrics_pretrained['dice']:.4f}")
except FileNotFoundError:
    print(f" Файл {CHECKPOINT_PRETRAINED} не найден!")

# ==================== СОХРАНЕНИЕ В TXT ====================
def save_comparison_to_txt(results, filepath='comparison_results.txt'):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("СРАВНЕНИЕ МОДЕЛЕЙ: U-Net с нуля vs U-Net + предобученный encoder\n")
        f.write(f"Дата отчёта: {timestamp}\n")
        f.write("=" * 80 + "\n\n")
        
        # Таблица 1: Общие результаты
        f.write(" ТАБЛИЦА 1: ОБЩИЕ РЕЗУЛЬТАТЫ НА ТЕСТОВОЙ ВЫБОРКЕ\n")
        f.write("-" * 80 + "\n")
        header = f"{'Модель':<25} {'Параметры (всего)':<20} {'Параметры (обуч.)':<20} {'Эпох':<8} {'mIoU (val)':<12} {'mIoU (test)':<12}\n"
        f.write(header)
        f.write("-" * 80 + "\n")
        
        for name, res in results.items():
            row = f"{name:<25} {res['params_total']:>15,}  {res['params_trainable']:>15,}           {res['epochs']:>6}   {res['iou']:>10.4f}   {res['iou']:>10.4f}\n"
            f.write(row)
        
        f.write("\n")
        
        # Таблица 2: IoU по классам
        f.write(" ТАБЛИЦА 2: IoU ПО КАЖДОМУ КЛАССУ\n")
        f.write("-" * 80 + "\n")
        header = f"{'Класс':<20}"
        for name in results.keys():
            header += f"{name:<30}"
        f.write(header + "\n")
        f.write("-" * 80 + "\n")
        
        classes = list(results[list(results.keys())[0]]['iou_per_class'].keys())
        for c in classes:
            class_name = 'Фон (0)' if c == 0 else f'Опухоль (1)'
            row = f"{class_name:<20}"
            for name, res in results.items():
                row += f"{res['iou_per_class'][c]:>18.4f}  "
            f.write(row + "\n")
        
        f.write("\n")
        
        # Таблица 3: Dice и Accuracy
        f.write(" ТАБЛИЦА 3: DICE SCORE И ACCURACY\n")
        f.write("-" * 80 + "\n")
        header = f"{'Модель':<25} {'Dice Score':<20} {'Accuracy':<20}\n"
        f.write(header)
        f.write("-" * 80 + "\n")
        
        for name, res in results.items():
            row = f"{name:<25} {res['dice']:>18.4f}  {res['acc']:>18.4f}\n"
            f.write(row)
        
        f.write("\n")
        
    
    print(f"\n Результаты сохранены в: {filepath}")

# Сохраняем сравнение
if results:
    save_comparison_to_txt(results, 'comparison_results.txt')

# ==================== АНАЛИЗ ОШИБОК (Часть C) ====================
def visualize_worst_predictions(results, num_worst=6, save_path='error_analysis.png'):
    """Визуализация худших предсказаний с картами ошибок"""
    
    if 'U-Net + ResNet34' not in results:
        print(" Модель с предобученным encoder не найдена, пропускаем анализ ошибок")
        return
    
    predictions = results['U-Net + ResNet34']['predictions']
    
    # Сортируем по IoU (худшие первые)
    sorted_preds = sorted(predictions, key=lambda x: x['iou'])
    worst_samples = sorted_preds[:num_worst]
    
    print(f"\n Анализ ошибок: {num_worst} изображений с наименьшим IoU")
    print("-" * 60)
    for i, sample in enumerate(worst_samples):
        print(f"  #{i+1}: IoU = {sample['iou']:.4f}")
    
    # Визуализация
    fig, axes = plt.subplots(num_worst, 4, figsize=(20, 5*num_worst))
    
    if num_worst == 1:
        axes = axes.reshape(1, -1)
    
    for i, sample in enumerate(worst_samples):
        # Денормализация изображения
        img = sample['image'].permute(1, 2, 0).numpy()
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        img = img * std + mean
        img = np.clip(img, 0, 1)
        
        pred = sample['pred'].numpy()
        true = sample['true'].numpy()
        error_map = (pred != true).astype(float)
        
        # Исходное изображение
        axes[i, 0].imshow(img)
        axes[i, 0].set_title(f'Исходное изображение\nIoU={sample["iou"]:.4f}', fontsize=10)
        axes[i, 0].axis('off')
        
        # Истинная маска
        axes[i, 1].imshow(true, cmap='tab10', vmin=0, vmax=1)
        axes[i, 1].set_title('Истинная маска', fontsize=10)
        axes[i, 1].axis('off')
        
        # Предсказанная маска
        axes[i, 2].imshow(pred, cmap='tab10', vmin=0, vmax=1)
        axes[i, 2].set_title('Предсказанная маска', fontsize=10)
        axes[i, 2].axis('off')
        
        # Карта ошибок
        im = axes[i, 3].imshow(error_map, cmap='Reds')
        axes[i, 3].set_title('Карта ошибок', fontsize=10)
        axes[i, 3].axis('off')
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"\n Визуализация ошибок сохранена в: {save_path}")

# Запускаем анализ ошибок
if results:
    visualize_worst_predictions(results, num_worst=6, save_path='error_analysis.png')

# ==================== ВЫВОД В КОНСОЛЬ ====================
print("\n" + "=" * 60)
print(" КРАТКИЙ ОТЧЁТ")
print("=" * 60)

for name, res in results.items():
    print(f"\n{name}:")
    print(f"  • Параметры: {res['params_total']:,} (обучаемых: {res['params_trainable']:,})")
    print(f"  • mIoU:  {res['iou']:.4f} ({res['iou']*100:.1f}%)")
    print(f"  • Dice:  {res['dice']:.4f} ({res['dice']*100:.1f}%)")
    print(f"  • Acc:   {res['acc']:.4f} ({res['acc']*100:.1f}%)")
    for c, val in res['iou_per_class'].items():
        cls_name = 'Фон' if c == 0 else 'Опухоль'
        print(f"  • IoU [{cls_name}]: {val:.4f}")

print("\n" + "=" * 60)
print(" Сравнение завершено!")
print("=" * 60)