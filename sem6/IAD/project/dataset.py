import torch
from torch.utils.data import Dataset
import cv2
import numpy as np
import os
from pathlib import Path

class BUSIDataset(Dataset):
    """Датасет BUSI для бинарной сегментации (фон = 0, опухоль = 1)"""
    
    def __init__(self, root_dir, transform=None):
        self.root_dir = Path(root_dir)
        self.transform = transform
        self.images = []
        
        # Загружаем только benign и malignant (в normal нет масок)
        for class_name in ['benign', 'malignant']:
            class_dir = self.root_dir / class_name
            if not class_dir.exists():
                print(f"Папка {class_dir} не найдена!")
                continue
                
            for img_path in class_dir.glob("*.png"):
                if '_mask' not in img_path.stem:  # исключаем маски
                    self.images.append(img_path)
        
        print(f"Загружено {len(self.images)} изображений")
    
    def __len__(self):
        return len(self.images)
    
    def __getitem__(self, idx):
        img_path = self.images[idx]
        
        # Загружаем изображение
        image = cv2.imread(str(img_path))
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        # Загружаем маску
        mask_path = img_path.parent / f"{img_path.stem}_mask.png"
        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        
        # Бинарная маска: 0 = фон, 1 = опухоль
        mask = (mask > 0).astype(np.int64)
        
        # Применяем трансформации
        if self.transform:
            transformed = self.transform(image=image, mask=mask)
            image = transformed['image']
            mask = transformed['mask']
        
        return image, mask.long()


# Функция для проверки данных
def visualize_sample(dataset, idx):
    import matplotlib.pyplot as plt
    
    image, mask = dataset[idx]
    
    if torch.is_tensor(image):
        # Денормализация
        mean = np.array([0.485, 0.456, 0.406])
        std = np.array([0.229, 0.224, 0.225])
        image = image.permute(1, 2, 0).cpu().numpy()
        image = image * std + mean
        image = np.clip(image, 0, 1)
    
    if torch.is_tensor(mask):
        mask = mask.cpu().numpy()
    
    fig, axes = plt.subplots(1, 2, figsize=(10, 5))
    axes[0].imshow(image)
    axes[0].set_title('УЗИ-изображение')
    axes[0].axis('off')
    
    axes[1].imshow(mask, cmap='gray')
    axes[1].set_title('Маска (опухоль = белый)')
    axes[1].axis('off')
    
    plt.show()