import os
import random
import numpy as np
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader
from torchvision import datasets, transforms
import matplotlib.pyplot as plt


RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)
torch.manual_seed(RANDOM_SEED)
if torch.cuda.is_available():
    torch.cuda.manual_seed(RANDOM_SEED)
    torch.cuda.manual_seed_all(RANDOM_SEED)


PROCESSED_ROOT = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/animals/dataset"  
IMG_SIZE = (224, 224)
imagenet_mean = [0.485,0.456,0.406]
imagenet_std = [0.229,0.224,0.225]
BATCH_SIZE = 32
NUM_CLASSES = 10
NUM_EPOCHS = 30
results = []
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using device: {DEVICE}")



train_path = os.path.join(PROCESSED_ROOT, 'train')
if not os.path.exists(train_path):
    print(f"ОШИБКА: Папка {train_path} не найдена!")
    exit(1)

# Трансформации для обучения (с аугментацией)


train_transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.RandomRotation(degrees=30,  #  градусов
                              fill=0),      # чем заполнять пустые углы (0 - черным)
    transforms.RandomAffine(degrees=0,  # не поворачиваем (уже повернули выше)
                           translate=(0.1, 0.1),  # сдвиг до 10% по x и y
                           fill=0),                # заполняем пустоты черным
    transforms.RandomHorizontalFlip(p=0.5),
    transforms.ColorJitter(brightness=0.2,    # яркость
                          contrast=0.2,       # контраст 
                          saturation=0.2),    # насыщенность 
    transforms.Lambda(lambda img: img.convert("RGB")),
    transforms.ToTensor(),
    transforms.Normalize(imagenet_mean, imagenet_std)
])

# Трансформации для валидации/теста
val_transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.Lambda(lambda img: img.convert("RGB")),
    transforms.ToTensor(),
    transforms.Normalize(imagenet_mean, imagenet_std)
])


# Создаем датасеты
train_dataset = datasets.ImageFolder(os.path.join(PROCESSED_ROOT, 'train'), transform=train_transform)
val_dataset = datasets.ImageFolder(os.path.join(PROCESSED_ROOT, 'val'), transform=val_transform)
test_dataset = datasets.ImageFolder(os.path.join(PROCESSED_ROOT, 'test'), transform=val_transform)

print(f"\nРазмер обучающей выборки: {len(train_dataset)}")
print(f"Размер валидационной выборки: {len(val_dataset)}")
print(f"Размер тестовой выборки: {len(test_dataset)}")
print(f"Классы: {train_dataset.classes}") 


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
#visualize_augmentation(train_dataset, num_samples=10, num_variations=5)


class AnimalsCNN(nn.Module):
    def __init__(self, num_classes=6):
        super(AnimalsCNN, self).__init__()
        
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
model = AnimalsCNN(num_classes=NUM_CLASSES).to(DEVICE)
print("\nМодель создана:")
#print(model)


# Подсчет параметров
total_params = sum(p.numel() for p in model.parameters())
trainable_params = sum(p.numel() for p in model.parameters() if p.requires_grad)
print(f"Всего параметров: {total_params:,}")
print(f"Обучаемых параметров: {trainable_params:,}")



criterion = nn.CrossEntropyLoss()
optimizer = optim.AdamW(model.parameters(), lr=0.001, weight_decay=0.01)


# Scheduler без verbose
scheduler = optim.lr_scheduler.ReduceLROnPlateau(
    optimizer, 
    mode='max', 
    factor=0.5, 
    patience=3,
    min_lr=1e-6
)




print("\nНачинаем обучение...")
def train_model(model, path_to_save, optimizer, name, mode, scheduler):
    import time
    epoch_times = []
    train_losses = []
    val_accuracies = []

    # Для early stopping
    best_val_acc = 0.0
    patience = 5
    patience_counter = 0

    for epoch in range(NUM_EPOCHS):
        start_time = time.time()
        
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
            }, path_to_save)
            print(f"  -> New best model saved! Accuracy: {val_acc:.2f}%")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"Early stopping triggered after {epoch+1} epochs")
                break
    epoch_time = time.time() - start_time
    print(f"Время вычисления эпохи: {epoch_time}")
    epoch_times.append(epoch_time) 
    avg_epoch_time = sum(epoch_times) / len(epoch_times)
    epochs_done = len(train_losses)  # сколько эпох прошло
    
    # Сохраняем результаты (results должен быть глобальным списком)
    results.append({
        'Модель': name,
        'Режим': mode,
        'Число обучаемых параметров': sum(p.numel() for p in model.parameters() if p.requires_grad),
        'Время обучения (на эпоху)': round(avg_epoch_time, 2),
        'Число эпох до сходимости': epochs_done,
        'Val accuracy': round(max(val_accuracies), 2) if val_accuracies else 0,
        'Test accuracy': 0  # пока 0, обновим после теста
    })

    return train_losses, val_accuracies

#train_losses, val_accuracies = train_model(model, "best_animals_model.pth", optimizer, 'A', "С нуля", scheduler)
train_losses, val_accuracies = [], []
def test_model(model, path: str, name):
    # Загружаем лучшую модель
    if os.path.exists(path):
        checkpoint = torch.load(path)
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
    for item in results:
        if item['Модель'] == name:
            item['Test accuracy'] = round(test_acc, 2)
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
    plt.savefig(f'{path}.png', dpi=150, bbox_inches='tight')
    plt.show()

    print("\n✅ Обучение завершено!")
    print(f"Графики сохранены в '{path}.png'")

    

#test_model(model, "best_animals_model.pth", 'A')
print(results)

import torchvision.models as models


loaded_model = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)

for param in loaded_model.parameters():
    param.requires_grad = False

loaded_model.fc = nn.Sequential(
                                nn.Linear(loaded_model.fc.in_features, 256),    
                                nn.ReLU(),               
                                nn.Dropout(0.5),       
                                nn.Linear(256, NUM_CLASSES)       
                            )

loaded_model = loaded_model.to(DEVICE)

opt = optim.Adam(filter(lambda p: p.requires_grad, loaded_model.parameters()), lr=0.001)
scheduler_B = optim.lr_scheduler.ReduceLROnPlateau(
    opt, 
    mode='max', 
    factor=0.5, 
    patience=3,
    min_lr=1e-6
)

#train_losses, val_accuracies = train_model(loaded_model, "best_animals_loaded_model.pth", opt, 'B', "Предобученная модель с замороженными слоями", scheduler_B)
#test_model(loaded_model, "best_animals_loaded_model.pth", 'B')

print(results)

loaded_model_2 = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)

loaded_model_2.fc = nn.Sequential(
                                nn.Linear(loaded_model_2.fc.in_features, 256),    
                                nn.ReLU(),               
                                nn.Dropout(0.5),       
                                nn.Linear(256, NUM_CLASSES)       
                            )

loaded_model_2 = loaded_model_2.to(DEVICE)

head_params = loaded_model_2.fc.parameters()
backbone_params = [p for name, p in loaded_model_2.named_parameters() if "fc" not in name]

opt_2 = torch.optim.Adam([
                    {'params': backbone_params, 'lr':1e-4}, # малый lr для предобученных слоёв
                    {'params': head_params, 'lr':1e-3}, # нормальный lr для новой головы
                    ])
scheduler_C = optim.lr_scheduler.ReduceLROnPlateau(
    opt_2, 
    mode='max', 
    factor=0.5, 
    patience=3,
    min_lr=1e-6
)

#train_losses, val_accuracies = train_model(loaded_model_2, "best_animals_loaded_model_2.pth", opt_2, 'C', "Fine-tuning", scheduler_C)
#test_model(loaded_model_2,"best_animals_loaded_model_2.pth", 'C')

print(results)

# В конце всего кода
print("\n" + "="*60)
print("ИТОГОВАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
print("="*60)



import pandas as pd
df = pd.DataFrame(results)
print(df.to_string(index=False))
    
# Можно сохранить в CSV
df.to_csv('results_comparison.csv', index=False)
print("\nТаблица сохранена в 'results_comparison.csv'")


















# Время вычисления эпохи: 97.5832211971283

# Загружена лучшая модель с точностью 79.50%

# Тестовая точность: 77.98%
# Случайное угадывание: 10.00%
# Модель лучше случайной в 7.8 раз


# Epoch [11/30], Loss: 0.4030, Val Accuracy: 95.29%
#   Current learning rate: 0.000500
# Early stopping triggered after 11 epochs
# Время вычисления эпохи: 75.3710584640503
# Загружена лучшая модель с точностью 95.70%

# Тестовая точность: 94.92%
# Случайное угадывание: 10.00%
# Модель лучше случайной в 9.5 раз