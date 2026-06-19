import os
import shutil
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt
from pathlib import Path


RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(RANDOM_SEED)
    torch.cuda.manual_seed_all(RANDOM_SEED)


DATA_ROOT = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/archive/training_images"  # Путь к папке с исходными PNG
PROCESSED_ROOT = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/hand_dataset_organized"  # Папка для организованного датасета
IMG_SIZE = (128, 128)
BATCH_SIZE = 32
NUM_CLASSES = 6  # Классы 0-5
NUM_EPOCHS = 30
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")


def organize_dataset(source_dir, target_dir, train_ratio=0.8, val_ratio=0.1):

    # Проверяем, существует ли уже организованный датасет
    if os.path.exists(target_dir):
        print(f"Папка {target_dir} уже существует. Пропускаем организацию данных.")
        return
    
    # Создаем целевую структуру папок (используем просто цифры как имена классов)
    for split in ['train', 'val', 'test']:
        for class_idx in range(NUM_CLASSES):
            class_dir = os.path.join(target_dir, split, str(class_idx))
            os.makedirs(class_dir, exist_ok=True)
    
    # Собираем все PNG файлы по классам
    class_files = {i: [] for i in range(NUM_CLASSES)}
    
    source_path = Path(source_dir)
    # Ищем все PNG файлы
    for file_path in source_path.glob('*.png'):
        filename = file_path.stem  # Имя без расширения
        try:
            # Ожидаем формат: число_число (например, 0_0, 1_5, 2000_3)
            parts = filename.split('_')
            if len(parts) >= 2:
                class_label = int(parts[1])  # Берем второе число как класс
                if 0 <= class_label <= 5:
                    class_files[class_label].append(file_path)
                else:
                    print(f"Пропущен файл с некорректным классом {class_label}: {file_path.name}")
            else:
                print(f"Пропущен файл с неправильным форматом имени: {file_path.name}")
        except (IndexError, ValueError) as e:
            print(f"Пропущен файл с неправильным форматом имени: {file_path.name}")
    
    # Проверяем, что файлы найдены
    total_files = sum(len(files) for files in class_files.values())
    if total_files == 0:
        print("ОШИБКА: Не найдено ни одного PNG файла в указанной директории!")
        print(f"Проверьте путь: {source_dir}")
        return
    
    print(f"Найдено всего {total_files} PNG файлов")
    
    # Для каждого класса разделяем на train/val/test
    for class_idx, files in class_files.items():
        if not files:
            print(f"Предупреждение: Нет файлов для класса {class_idx}")
            continue
            
        random.shuffle(files)
        n_total = len(files)
        n_train = int(n_total * train_ratio)
        n_val = int(n_total * val_ratio)
        
        train_files = files[:n_train]
        val_files = files[n_train:n_train + n_val]
        test_files = files[n_train + n_val:]
        
        # Копируем файлы в соответствующие папки
        for split_name, split_files in [('train', train_files), ('val', val_files), ('test', test_files)]:
            for src_path in split_files:
                dst_path = os.path.join(target_dir, split_name, str(class_idx), src_path.name)
                shutil.copy2(src_path, dst_path)
        
        print(f"Класс {class_idx}: всего {n_total} файлов -> "
              f"train: {len(train_files)}, val: {len(val_files)}, test: {len(test_files)}")


organize_dataset(DATA_ROOT, PROCESSED_ROOT)


train_path = os.path.join(PROCESSED_ROOT, 'train')
if not os.path.exists(train_path):
    print(f"ОШИБКА: Папка {train_path} не создана!")
    print("Проверьте, что в исходной папке есть PNG файлы в правильном формате.")
    exit(1)

# Трансформации для обучения (с аугментацией)

train_transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.RandomRotation(degrees=180,  #  градусов
                              fill=0),      # чем заполнять пустые углы (0 - черным)
    transforms.RandomAffine(degrees=0,  # не поворачиваем (уже повернули выше)
                           translate=(0.3, 0.3),  # сдвиг до 30% по x и y
                           fill=0),                # заполняем пустоты черным
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.3,    # яркость
                          contrast=0.3,       # контраст 
                          saturation=0.3),    # насыщенность 
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.267, 0.267, 0.267], std=[0.438, 0.438, 0.438])
])

# Трансформации для валидации/теста
val_transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.267, 0.267, 0.267], std=[0.438, 0.438, 0.438])
])

# Создаем датасеты
train_dataset = datasets.ImageFolder(os.path.join(PROCESSED_ROOT, 'train'), transform=train_transform)
val_dataset = datasets.ImageFolder(os.path.join(PROCESSED_ROOT, 'val'), transform=val_transform)
test_dataset = datasets.ImageFolder(os.path.join(PROCESSED_ROOT, 'test'), transform=val_transform)

print(f"\nРазмер обучающей выборки: {len(train_dataset)}")
print(f"Размер валидационной выборки: {len(val_dataset)}")
print(f"Размер тестовой выборки: {len(test_dataset)}")
print(f"Классы: {train_dataset.classes}")  # Должны быть ['0','1','2','3','4','5']

# Создаем DataLoader'ы
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)


def visualize_augmentation(dataset, num_samples=4, num_variations=5):

    # Получаем оригинальные изображения (без аугментации)
    orig_dataset = datasets.ImageFolder(
        os.path.join(PROCESSED_ROOT, 'train'),
        transforms.Compose([transforms.Resize(IMG_SIZE), transforms.ToTensor()])
    )
    
    # Выбираем случайные индексы
    indices = random.sample(range(len(orig_dataset)), num_samples)
    
    # Создаем сетку графиков
    _ , axes = plt.subplots(num_samples, num_variations + 1,
                             figsize=(15, 2 * num_samples))
    
    mean_std = torch.tensor([0.267]*3).view(3,1,1), torch.tensor([0.438]*3).view(3,1,1)
    
    for row, idx in enumerate(indices):
        # Оригинал
        img, label = orig_dataset[idx]
        axes[row, 0].imshow(img.permute(1, 2, 0))
        axes[row, 0].set_title(f'Класс {label}')
        axes[row, 0].axis('off')
        
        # Аугментации
        for col in range(num_variations):
            img_aug, _ = dataset[idx]
            img_aug = torch.clamp(img_aug * mean_std[1] + mean_std[0], 0, 1).permute(1, 2, 0)
            axes[row, col+1].imshow(img_aug)
            axes[row, col+1].axis('off')
    
    axes[0, 0].set_title(f'Оригинал\nКласс {label}')
    plt.tight_layout()
    plt.savefig('aug_vis.png', dpi=150, bbox_inches='tight')
    plt.show()

print("\n" + "="*50)
print("ВИЗУАЛИЗАЦИЯ АУГМЕНТАЦИИ")
print("="*50)
visualize_augmentation(train_dataset, num_samples=4, num_variations=5)


class HandGestureCNN(nn.Module):
    def __init__(self, num_classes=6):
        super(HandGestureCNN, self).__init__()
        
        # Первый сверточный блок
        self.conv_block1 = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.BatchNorm2d(32),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 128 -> 64
        )
        
        # Второй сверточный блок
        self.conv_block2 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.BatchNorm2d(64),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 64 -> 32
        )
        
        # Третий сверточный блок
        self.conv_block3 = nn.Sequential(
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.BatchNorm2d(128),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 32 -> 16
        )
        
        # Четвертый сверточный блок
        self.conv_block4 = nn.Sequential(
            nn.Conv2d(128, 256, kernel_size=3, padding=1),
            nn.BatchNorm2d(256),
            nn.ReLU(inplace=True),
            nn.MaxPool2d(kernel_size=2, stride=2)  # 16 -> 8
        )
        
        # Глобальный пулинг для уменьшения количества параметров
        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        
        # Классификатор
        self.classifier = nn.Sequential(
            nn.Dropout(p=0.5),
            nn.Linear(256, 128),
            nn.ReLU(inplace=True),
            nn.Dropout(p=0.3),
            nn.Linear(128, num_classes)
        )
        
    def forward(self, x):
        x = self.conv_block1(x)
        x = self.conv_block2(x)
        x = self.conv_block3(x)
        x = self.conv_block4(x)
        
        x = self.global_pool(x)
        x = x.view(x.size(0), -1)
        x = self.classifier(x)
        return x

# Инициализация модели
model = HandGestureCNN(num_classes=NUM_CLASSES).to(DEVICE)
print("\nМодель создана:")
print(model)

# Подсчет параметров
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Всего параметров: {total_params:,}")
print(f"Обучаемых параметров: {trainable_params:,}")


criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=0.001)

# Scheduler без verbose
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, 
    mode='max', 
    factor=0.5, 
    patience=3,
    min_lr=1e-6
)

# Для early stopping
best_val_acc = 0.0
patience = 5
patience_counter = 0

# Для визуализации
train_losses = []
val_accuracies = []


print("\nНачинаем обучение...")
for epoch in range(NUM_EPOCHS):
    # Training phase
    model.train()
    running_loss = 0.0
    
    for batch_idx, (images, labels) in enumerate(train_loader):
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        
        # Forward pass
        outputs = model(images)
        loss = criterion(outputs, labels)
        
        # Backward and optimize
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        running_loss += loss.item() * images.size(0)
        
        # Прогресс каждые 50 батчей
        if (batch_idx + 1) % 50 == 0:
            print(f'Epoch [{epoch+1}/{NUM_EPOCHS}], Batch [{batch_idx+1}/{len(train_loader)}], Loss: {loss.item():.4f}')
    
    epoch_loss = running_loss / len(train_loader.dataset)
    train_losses.append(epoch_loss)
    
    # Validation phase
    model.eval()
    correct = 0
    total = 0
    
    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()
    
    val_acc = 100 * correct / total
    val_accuracies.append(val_acc)
    
    print(f'Epoch [{epoch+1}/{NUM_EPOCHS}], Loss: {epoch_loss:.4f}, Val Accuracy: {val_acc:.2f}%')
    
    # Update learning rate scheduler
    scheduler.step(val_acc)
    current_lr = optimizer.param_groups[0]['lr']
    print(f'  Current learning rate: {current_lr:.6f}')
    
    # Early stopping check
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        patience_counter = 0
        torch.save({
            'epoch': epoch,
            'model_state_dict': model.state_dict(),
            'optimizer_state_dict': optimizer.state_dict(),
            'best_val_acc': best_val_acc,
        }, 'best_model.pth')
        print(f"  -> New best model saved! Accuracy: {val_acc:.2f}%")
    else:
        patience_counter += 1
        if patience_counter >= patience:
            print(f"Early stopping triggered after {epoch+1} epochs")
            break

# ------------------------------------------------------------------------------
# ШАГ 6: Оценка на тестовом наборе
# ------------------------------------------------------------------------------
# Загружаем лучшую модель
if os.path.exists('best_model.pth'):
    checkpoint = torch.load('best_model.pth')
    model.load_state_dict(checkpoint['model_state_dict'])
    print(f"\nЗагружена лучшая модель с точностью {checkpoint['best_val_acc']:.2f}%")

model.eval()
test_correct = 0
test_total = 0
class_correct = [0] * NUM_CLASSES
class_total = [0] * NUM_CLASSES

with torch.no_grad():
    for images, labels in test_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        outputs = model(images)
        _, predicted = torch.max(outputs, 1)
        test_total += labels.size(0)
        test_correct += (predicted == labels).sum().item()
        
        # Per-class accuracy
        for i in range(len(labels)):
            label = labels[i]
            pred = predicted[i]
            if pred == label:
                class_correct[label] += 1
            class_total[label] += 1

test_acc = 100 * test_correct / test_total
print(f'\nТестовая точность: {test_acc:.2f}%')
print(f'Случайное угадывание: {100/NUM_CLASSES:.2f}%')
print(f'Модель лучше случайной в {test_acc/(100/NUM_CLASSES):.1f} раз')

# Точность по классам
print("\nТочность по классам:")
for i in range(NUM_CLASSES):
    if class_total[i] > 0:
        acc = 100 * class_correct[i] / class_total[i]
        print(f'Класс {i}: {acc:.2f}% ({class_correct[i]}/{class_total[i]})')


plt.figure(figsize=(12, 4))

# График потерь на обучении
plt.subplot(1, 2, 1)
plt.plot(train_losses, label='Train Loss', color='blue', linewidth=2)
plt.xlabel('Epoch')
plt.ylabel('Loss')
plt.title('Training Loss over Epochs')
plt.legend()
plt.grid(True, alpha=0.3)

# График точности на валидации
plt.subplot(1, 2, 2)
plt.plot(val_accuracies, label='Validation Accuracy', color='orange', linewidth=2)
plt.xlabel('Epoch')
plt.ylabel('Accuracy (%)')
plt.title('Validation Accuracy over Epochs')
plt.legend()
plt.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('training_history.png', dpi=150, bbox_inches='tight')
plt.show()

print("\n✅ Обучение завершено!")
print(f"Графики сохранены в 'training_history.png'")
print(f"Лучшая модель сохранена в 'best_model.pth'")