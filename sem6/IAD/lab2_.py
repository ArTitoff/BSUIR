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
import pandas as pd
from datetime import datetime
import json

# Фиксируем random_seed для воспроизводимости
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


class ExperimentTracker:    
    def __init__(self, filename='experiments_results.csv'):
        self.filename = filename
        self.results = []
        
        # Проверяем, существует ли уже файл с результатами
        if os.path.exists(filename):
            self.df = pd.read_csv(filename)
        else:
            # Создаем новый DataFrame
            self.df = pd.DataFrame(columns=[
                'exp_id', 'timestamp', 'description', 
                'architecture', 'optimizer', 'lr', 'batch_size',
                'epochs', 'val_acc', 'test_acc', 'notes'
            ])
    
    def add_experiment(self, exp_id, description, architecture, optimizer_name, 
                       lr, batch_size, epochs, val_acc, test_acc=None, notes=''):
        """Добавляет результат эксперимента"""
        
        new_row = {
            'exp_id': exp_id,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'description': description,
            'architecture': architecture,
            'optimizer': optimizer_name,
            'lr': lr,
            'batch_size': batch_size,
            'epochs': epochs,
            'val_acc': f'{val_acc:.2f}%',
            'test_acc': f'{test_acc:.2f}%' if test_acc else '-',
            'notes': notes
        }
        
        # Добавляем в DataFrame
        self.df = pd.concat([self.df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Сохраняем в CSV
        self.df.to_csv(self.filename, index=False)
        
        # Выводим красиво
        print("\n" + "="*60)
        print(f"ЭКСПЕРИМЕНТ #{exp_id} ЗАПИСАН")
        print("="*60)
        print(f"Описание: {description}")
        print(f"Архитектура: {architecture}")
        print(f"Оптимизатор: {optimizer_name}, lr={lr}")
        print(f"Val Acc: {val_acc:.2f}%")
        if test_acc:
            print(f"Test Acc: {test_acc:.2f}%")
        print("="*60 + "\n")
    
    def show_summary(self):
        """Показывает сводку всех экспериментов"""
        print("\n" + "="*70)
        print("СВОДКА ЭКСПЕРИМЕНТОВ")
        print("="*70)
        print(self.df[['exp_id', 'description', 'optimizer', 'val_acc', 'test_acc']].to_string(index=False))
        print("="*70 + "\n")
        
    def get_best_model(self, metric='val_acc'):
        """Возвращает лучшую модель по метрике"""
        # Преобразуем строки в числа для сравнения
        self.df['val_acc_num'] = self.df['val_acc'].str.replace('%', '').astype(float)
        best_idx = self.df['val_acc_num'].idxmax()
        return self.df.iloc[best_idx]


# ------------------------------------------------------------------------------
# ФУНКЦИЯ ДЛЯ ОБУЧЕНИЯ МОДЕЛИ (универсальная)
# ------------------------------------------------------------------------------
def train_model(model, train_loader, val_loader, criterion, optimizer, scheduler, 
                num_epochs, patience, experiment_desc="", experiment_id=None):

    best_val_acc = 0.0
    patience_counter = 0
    train_losses = []
    val_accuracies = []
    
    print(f"\n🚀 Начинаем обучение: {experiment_desc}")
    print("="*60)
    
    for epoch in range(num_epochs):
        # Training phase
        model.train()
        running_loss = 0.0
        
        for batch_idx, (images, labels) in enumerate(train_loader):
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            
            outputs = model(images)
            loss = criterion(outputs, labels)
            
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            
            running_loss += loss.item() * images.size(0)
        
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
        
        print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {epoch_loss:.4f}, Val Accuracy: {val_acc:.2f}%')
        
        # Update scheduler
        if scheduler:
            scheduler.step(val_acc)
        
        # Early stopping
        if val_acc > best_val_acc:
            best_val_acc = val_acc
            patience_counter = 0
            # Сохраняем лучшую модель для этого эксперимента
            torch.save({
                'epoch': epoch,
                'model_state_dict': model.state_dict(),
                'optimizer_state_dict': optimizer.state_dict(),
                'best_val_acc': best_val_acc,
                'experiment_desc': experiment_desc
            }, f'best_model_exp{experiment_id}.pth' if experiment_id else 'best_model_temp.pth')
            print(f"  🏆 Новая лучшая модель! Accuracy: {val_acc:.2f}%")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print(f"⏹️ Early stopping на эпохе {epoch+1}")
                break
    
    return best_val_acc, train_losses, val_accuracies


# ------------------------------------------------------------------------------
# ФУНКЦИЯ ДЛЯ ТЕСТИРОВАНИЯ МОДЕЛИ
# ------------------------------------------------------------------------------
def test_model(model, test_loader, num_classes):
    model.eval()
    test_correct = 0
    test_total = 0
    class_correct = [0] * num_classes
    class_total = [0] * num_classes
    
    with torch.no_grad():
        for images, labels in test_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            test_total += labels.size(0)
            test_correct += (predicted == labels).sum().item()
            
            for i in range(len(labels)):
                label = labels[i]
                pred = predicted[i]
                if pred == label:
                    class_correct[label] += 1
                class_total[label] += 1
    
    test_acc = 100 * test_correct / test_total
    
    print(f"\n📊 ТЕСТИРОВАНИЕ МОДЕЛИ")
    print(f"Тестовая точность: {test_acc:.2f}%")
    print(f"Случайное угадывание: {100/num_classes:.2f}%")
    print(f"Модель лучше случайной в {test_acc/(100/num_classes):.1f} раз")
    
    print("\nТочность по классам:")
    for i in range(num_classes):
        if class_total[i] > 0:
            acc = 100 * class_correct[i] / class_total[i]
            print(f'Класс {i}: {acc:.2f}% ({class_correct[i]}/{class_total[i]})')
    
    return test_acc


# ------------------------------------------------------------------------------
# ФУНКЦИЯ ДЛЯ СОЗДАНИЯ РАЗНЫХ АРХИТЕКТУР
# ------------------------------------------------------------------------------
def create_model_variant(variant_name, num_classes=6):
    """
    Создает различные варианты архитектуры для экспериментов
    """
    
    if variant_name == 'baseline':
        # Базовая модель из Задания 1
        class BaselineCNN(nn.Module):
            def __init__(self):
                super(BaselineCNN, self).__init__()
                self.conv_block1 = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    nn.BatchNorm2d(32),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block2 = nn.Sequential(
                    nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block3 = nn.Sequential(
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.BatchNorm2d(128),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block4 = nn.Sequential(
                    nn.Conv2d(128, 256, kernel_size=3, padding=1),
                    nn.BatchNorm2d(256),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
                self.classifier = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Dropout(0.3),
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
        return BaselineCNN()
    
    elif variant_name == 'more_filters':
        # Увеличиваем количество фильтров
        class MoreFiltersCNN(nn.Module):
            def __init__(self):
                super(MoreFiltersCNN, self).__init__()
                self.conv_block1 = nn.Sequential(
                    nn.Conv2d(3, 64, kernel_size=3, padding=1),  # 32 -> 64
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block2 = nn.Sequential(
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),  # 64 -> 128
                    nn.BatchNorm2d(128),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block3 = nn.Sequential(
                    nn.Conv2d(128, 256, kernel_size=3, padding=1),  # 128 -> 256
                    nn.BatchNorm2d(256),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block4 = nn.Sequential(
                    nn.Conv2d(256, 512, kernel_size=3, padding=1),  # 256 -> 512
                    nn.BatchNorm2d(512),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
                self.classifier = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(512, 256),
                    nn.ReLU(),
                    nn.Dropout(0.3),
                    nn.Linear(256, num_classes)
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
        return MoreFiltersCNN()
    
    elif variant_name == 'kernel_5':
        # Используем ядра 5x5
        class Kernel5CNN(nn.Module):
            def __init__(self):
                super(Kernel5CNN, self).__init__()
                self.conv_block1 = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=5, padding=2),  # kernel=5
                    nn.BatchNorm2d(32),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block2 = nn.Sequential(
                    nn.Conv2d(32, 64, kernel_size=5, padding=2),
                    nn.BatchNorm2d(64),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block3 = nn.Sequential(
                    nn.Conv2d(64, 128, kernel_size=5, padding=2),
                    nn.BatchNorm2d(128),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block4 = nn.Sequential(
                    nn.Conv2d(128, 256, kernel_size=5, padding=2),
                    nn.BatchNorm2d(256),
                    nn.ReLU(inplace=True),
                    nn.MaxPool2d(2)
                )
                self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
                self.classifier = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(256, 128),
                    nn.ReLU(),
                    nn.Dropout(0.3),
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
        return Kernel5CNN()
    
    elif variant_name == 'leaky_relu':
        # Используем LeakyReLU вместо ReLU
        class LeakyReLUCNN(nn.Module):
            def __init__(self):
                super(LeakyReLUCNN, self).__init__()
                self.conv_block1 = nn.Sequential(
                    nn.Conv2d(3, 32, kernel_size=3, padding=1),
                    nn.BatchNorm2d(32),
                    nn.LeakyReLU(0.1, inplace=True),  # LeakyReLU
                    nn.MaxPool2d(2)
                )
                self.conv_block2 = nn.Sequential(
                    nn.Conv2d(32, 64, kernel_size=3, padding=1),
                    nn.BatchNorm2d(64),
                    nn.LeakyReLU(0.1, inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block3 = nn.Sequential(
                    nn.Conv2d(64, 128, kernel_size=3, padding=1),
                    nn.BatchNorm2d(128),
                    nn.LeakyReLU(0.1, inplace=True),
                    nn.MaxPool2d(2)
                )
                self.conv_block4 = nn.Sequential(
                    nn.Conv2d(128, 256, kernel_size=3, padding=1),
                    nn.BatchNorm2d(256),
                    nn.LeakyReLU(0.1, inplace=True),
                    nn.MaxPool2d(2)
                )
                self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
                self.classifier = nn.Sequential(
                    nn.Dropout(0.5),
                    nn.Linear(256, 128),
                    nn.LeakyReLU(0.1),
                    nn.Dropout(0.3),
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
        return LeakyReLUCNN()
    
    else:
        raise ValueError(f"Unknown variant: {variant_name}")


# ------------------------------------------------------------------------------
# ОСНОВНОЙ КОД ДЛЯ ЗАПУСКА ЭКСПЕРИМЕНТОВ
# ------------------------------------------------------------------------------
def run_experiments():
    """Запускает серию экспериментов"""
    

    tracker = ExperimentTracker('experiments_results.csv')
    
    
    # Подготавливаем данные (трансформации и загрузчики)
    train_transform = transforms.Compose([
        transforms.Resize(IMG_SIZE),
        transforms.RandomRotation(degrees=180, fill=0),
        transforms.RandomAffine(degrees=0, translate=(0.3, 0.3), fill=0),
        transforms.RandomHorizontalFlip(p=0.5),
        transforms.ColorJitter(brightness=0.3, contrast=0.3, saturation=0.3),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.267, 0.267, 0.267], std=[0.438, 0.438, 0.438])
    ])
    
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
    
    # --------------------------------------------------------------------------
    # ЭКСПЕРИМЕНТ 0: Baseline (как в Задании 1)
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ЭКСПЕРИМЕНТ 0: Baseline модель")
    print("="*70)
    
    # Создаем загрузчики для этого эксперимента
    train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True, num_workers=2)
    val_loader = DataLoader(val_dataset, batch_size=32, shuffle=False, num_workers=2)
    test_loader = DataLoader(test_dataset, batch_size=32, shuffle=False, num_workers=2)
    
    # Создаем baseline модель
    model0 = create_model_variant('baseline').to(DEVICE)
    
    # Настройки обучения
    criterion = nn.CrossEntropyLoss()
    optimizer0 = optim.Adam(model0.parameters(), lr=0.001)
    scheduler0 = optim.lr_scheduler.ReduceLROnPlateau(optimizer0, mode='max', factor=0.5, patience=3)
    
    # Обучаем
    val_acc0, losses0, accs0 = train_model(
        model0, train_loader, val_loader, criterion, optimizer0, scheduler0,
        num_epochs=20, patience=5,
        experiment_desc="Baseline модель (32→64→128→256 фильтров)",
        experiment_id=0
    )
    
    # Тестируем
    test_acc0 = test_model(model0, test_loader, NUM_CLASSES)
    
    # Записываем результат
    tracker.add_experiment(
        exp_id=0,
        description="Baseline (Задание 1)",
        architecture="32→64→128→256, kernel=3, ReLU",
        optimizer_name="Adam",
        lr=0.001,
        batch_size=32,
        epochs=20,
        val_acc=val_acc0,
        test_acc=test_acc0,
        notes="Базовая модель с 4 сверточными блоками"
    )
    
    # --------------------------------------------------------------------------
    # ЭКСПЕРИМЕНТ 1: Увеличиваем количество фильтров
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ЭКСПЕРИМЕНТ 1: Увеличение фильтров (64→128→256→512)")
    print("="*70)
    
    model1 = create_model_variant('more_filters').to(DEVICE)
    optimizer1 = optim.Adam(model1.parameters(), lr=0.001)
    scheduler1 = optim.lr_scheduler.ReduceLROnPlateau(optimizer1, mode='max', factor=0.5, patience=3)
    
    val_acc1, losses1, accs1 = train_model(
        model1, train_loader, val_loader, criterion, optimizer1, scheduler1,
        num_epochs=20, patience=5,
        experiment_desc="Увеличенные фильтры (64→128→256→512)",
        experiment_id=1
    )
    
    tracker.add_experiment(
        exp_id=1,
        description="Больше фильтров",
        architecture="64→128→256→512, kernel=3, ReLU",
        optimizer_name="Adam",
        lr=0.001,
        batch_size=32,
        epochs=20,
        val_acc=val_acc1,
        notes="Увеличили количество фильтров в 2 раза"
    )
    
    # --------------------------------------------------------------------------
    # ЭКСПЕРИМЕНТ 2: Меняем размер ядра на 5x5
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ЭКСПЕРИМЕНТ 2: Ядро 5x5")
    print("="*70)
    
    model2 = create_model_variant('kernel_5').to(DEVICE)
    optimizer2 = optim.Adam(model2.parameters(), lr=0.001)
    scheduler2 = optim.lr_scheduler.ReduceLROnPlateau(optimizer2, mode='max', factor=0.5, patience=3)
    
    val_acc2, losses2, accs2 = train_model(
        model2, train_loader, val_loader, criterion, optimizer2, scheduler2,
        num_epochs=20, patience=5,
        experiment_desc="Ядро 5x5 вместо 3x3",
        experiment_id=2
    )
    
    tracker.add_experiment(
        exp_id=2,
        description="Ядро 5x5",
        architecture="32→64→128→256, kernel=5, ReLU",
        optimizer_name="Adam",
        lr=0.001,
        batch_size=32,
        epochs=20,
        val_acc=val_acc2,
        notes="Увеличили размер ядра свертки"
    )
    
    # --------------------------------------------------------------------------
    # ЭКСПЕРИМЕНТ 3: Меняем функцию активации на LeakyReLU
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ЭКСПЕРИМЕНТ 3: LeakyReLU вместо ReLU")
    print("="*70)
    
    model3 = create_model_variant('leaky_relu').to(DEVICE)
    optimizer3 = optim.Adam(model3.parameters(), lr=0.001)
    scheduler3 = optim.lr_scheduler.ReduceLROnPlateau(optimizer3, mode='max', factor=0.5, patience=3)
    
    val_acc3, losses3, accs3 = train_model(
        model3, train_loader, val_loader, criterion, optimizer3, scheduler3,
        num_epochs=20, patience=5,
        experiment_desc="LeakyReLU (negative_slope=0.1)",
        experiment_id=3
    )
    
    tracker.add_experiment(
        exp_id=3,
        description="LeakyReLU",
        architecture="32→64→128→256, kernel=3, LeakyReLU",
        optimizer_name="Adam",
        lr=0.001,
        batch_size=32,
        epochs=20,
        val_acc=val_acc3,
        notes="Заменили ReLU на LeakyReLU"
    )
    
    # --------------------------------------------------------------------------
    # ЭКСПЕРИМЕНТ 4: Меняем оптимизатор на AdamW
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ЭКСПЕРИМЕНТ 4: AdamW оптимизатор")
    print("="*70)
    
    model4 = create_model_variant('baseline').to(DEVICE)  # Возвращаемся к baseline архитектуре
    optimizer4 = optim.AdamW(model4.parameters(), lr=0.001, weight_decay=0.01)  # AdamW с L2 регуляризацией
    scheduler4 = optim.lr_scheduler.ReduceLROnPlateau(optimizer4, mode='max', factor=0.5, patience=3)
    
    val_acc4, losses4, accs4 = train_model(
        model4, train_loader, val_loader, criterion, optimizer4, scheduler4,
        num_epochs=20, patience=5,
        experiment_desc="AdamW оптимизатор с weight_decay=0.01",
        experiment_id=4
    )
    
    tracker.add_experiment(
        exp_id=4,
        description="AdamW",
        architecture="32→64→128→256, kernel=3, ReLU",
        optimizer_name="AdamW",
        lr=0.001,
        batch_size=32,
        epochs=20,
        val_acc=val_acc4,
        notes="AdamW с weight_decay=0.01"
    )
    
    # --------------------------------------------------------------------------
    # ЭКСПЕРИМЕНТ 5: Меняем learning rate
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ЭКСПЕРИМЕНТ 5: Learning rate = 0.0001")
    print("="*70)
    
    model5 = create_model_variant('baseline').to(DEVICE)
    optimizer5 = optim.Adam(model5.parameters(), lr=0.0001)  # Меньший lr
    scheduler5 = optim.lr_scheduler.ReduceLROnPlateau(optimizer5, mode='max', factor=0.5, patience=3)
    
    val_acc5, losses5, accs5 = train_model(
        model5, train_loader, val_loader, criterion, optimizer5, scheduler5,
        num_epochs=25, patience=5,  # Больше эпох для маленького lr
        experiment_desc="Learning rate = 0.0001",
        experiment_id=5
    )
    
    tracker.add_experiment(
        exp_id=5,
        description="LR=0.0001",
        architecture="32→64→128→256, kernel=3, ReLU",
        optimizer_name="Adam",
        lr=0.0001,
        batch_size=32,
        epochs=25,
        val_acc=val_acc5,
        notes="Уменьшили learning rate в 10 раз"
    )
    
    # --------------------------------------------------------------------------
    # ЭКСПЕРИМЕНТ 6: Увеличиваем batch size
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ЭКСПЕРИМЕНТ 6: Batch size = 64")
    print("="*70)
    
    # Создаем новые загрузчики с batch_size=64
    train_loader64 = DataLoader(train_dataset, batch_size=64, shuffle=True, num_workers=2)
    val_loader64 = DataLoader(val_dataset, batch_size=64, shuffle=False, num_workers=2)
    
    model6 = create_model_variant('baseline').to(DEVICE)
    optimizer6 = optim.Adam(model6.parameters(), lr=0.001)
    scheduler6 = optim.lr_scheduler.ReduceLROnPlateau(optimizer6, mode='max', factor=0.5, patience=3)
    
    val_acc6, losses6, accs6 = train_model(
        model6, train_loader64, val_loader64, criterion, optimizer6, scheduler6,
        num_epochs=20, patience=5,
        experiment_desc="Batch size = 64",
        experiment_id=6
    )
    
    tracker.add_experiment(
        exp_id=6,
        description="Batch size=64",
        architecture="32→64→128→256, kernel=3, ReLU",
        optimizer_name="Adam",
        lr=0.001,
        batch_size=64,
        epochs=20,
        val_acc=val_acc6,
        notes="Увеличили batch size до 64"
    )
    
    # --------------------------------------------------------------------------
    # ФИНАЛЬНАЯ ОЦЕНКА: Выбираем лучшую модель и тестируем
    # --------------------------------------------------------------------------
    print("\n" + "="*70)
    print("ФИНАЛЬНАЯ ОЦЕНКА: Выбор лучшей модели по валидации")
    print("="*70)
    
    # Показываем сводку всех экспериментов
    tracker.show_summary()
    
    # Находим лучшую модель (кроме baseline, если он не лучший)
    best_exp = tracker.get_best_model()
    print(f"\n🏆 Лучшая модель: Эксперимент #{best_exp['exp_id']}")
    print(f"   Описание: {best_exp['description']}")
    print(f"   Val Acc: {best_exp['val_acc']}")
    
    # Загружаем лучшую модель и тестируем на тестовом наборе
    best_model_path = f"best_model_exp{best_exp['exp_id']}.pth"
    if os.path.exists(best_model_path):
        checkpoint = torch.load(best_model_path)
        
        # Создаем соответствующую модель
        if best_exp['exp_id'] == 0:
            best_model = create_model_variant('baseline').to(DEVICE)
        elif best_exp['exp_id'] == 1:
            best_model = create_model_variant('more_filters').to(DEVICE)
        elif best_exp['exp_id'] == 2:
            best_model = create_model_variant('kernel_5').to(DEVICE)
        elif best_exp['exp_id'] == 3:
            best_model = create_model_variant('leaky_relu').to(DEVICE)
        else:
            best_model = create_model_variant('baseline').to(DEVICE)
        
        best_model.load_state_dict(checkpoint['model_state_dict'])
        
        # Тестируем на тестовом наборе
        final_test_acc = test_model(best_model, test_loader, NUM_CLASSES)
        
        # Обновляем запись в трекере
        tracker.add_experiment(
            exp_id=f"{best_exp['exp_id']}_final",
            description=f"{best_exp['description']} (финальный тест)",
            architecture=best_exp['architecture'],
            optimizer_name=best_exp['optimizer'],
            lr=best_exp['lr'],
            batch_size=int(best_exp['batch_size']),
            epochs=best_exp['epochs'],
            val_acc=float(best_exp['val_acc'].replace('%', '')),
            test_acc=final_test_acc,
            notes="Финальное тестирование лучшей модели"
        )
    
    # Сохраняем итоговую таблицу в красивом формате
    print("\n" + "="*80)
    print("ИТОГОВАЯ ТАБЛИЦА ЭКСПЕРИМЕНТОВ")
    print("="*80)
    print(tracker.df[['exp_id', 'description', 'optimizer', 'lr', 'val_acc', 'test_acc']].to_string(index=False))
    
    # Сохраняем в CSV и Excel
    tracker.df.to_csv('experiments_final.csv', index=False)
    try:
        tracker.df.to_excel('experiments_final.xlsx', index=False)
        print("\n✅ Результаты сохранены в experiments_final.csv и experiments_final.xlsx")
    except:
        print("\n✅ Результаты сохранены в experiments_final.csv")
    
    # Визуализация сравнения экспериментов
    plt.figure(figsize=(12, 6))
    
    exp_ids = [0, 1, 2, 3, 4, 5, 6]
    val_accs = [val_acc0, val_acc1, val_acc2, val_acc3, val_acc4, val_acc5, val_acc6]
    exp_names = ['Baseline', 'More\nFilters', 'Kernel\n5x5', 'Leaky\nReLU', 'AdamW', 'LR\n0.0001', 'Batch\n64']
    
    colors = ['blue', 'green', 'red', 'purple', 'orange', 'brown', 'pink']
    bars = plt.bar(exp_names, val_accs, color=colors, alpha=0.7)
    
    # Добавляем значения на столбцы
    for bar, acc in zip(bars, val_accs):
        plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5, 
                f'{acc:.1f}%', ha='center', va='bottom', fontsize=10)
    
    plt.axhline(y=100/6, color='red', linestyle='--', alpha=0.7, label=f'Random ({100/6:.1f}%)')
    plt.xlabel('Эксперимент')
    plt.ylabel('Validation Accuracy (%)')
    plt.title('Сравнение результатов экспериментов')
    plt.legend()
    plt.grid(True, alpha=0.3, axis='y')
    plt.tight_layout()
    plt.savefig('experiments_comparison.png', dpi=150)
    plt.show()
    
    print("\n📊 График сравнения сохранен в 'experiments_comparison.png'")
    
    return tracker


# ------------------------------------------------------------------------------
# ЗАПУСК ЭКСПЕРИМЕНТОВ
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    print("🚀 ЗАПУСК СЕРИИ ЭКСПЕРИМЕНТОВ")
    print("="*70)
    
    tracker = run_experiments()
    
