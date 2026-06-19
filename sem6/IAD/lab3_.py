import os
import random
import numpy as np
import torch
import torch.nn as nn
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


# Создаем DataLoader'ы
train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2)
val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)
test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2)


import torchvision.models as models

loaded_model_2 = models.resnet34(weights=models.ResNet34_Weights.DEFAULT)

loaded_model_2.fc = nn.Sequential(
                                nn.Linear(loaded_model_2.fc.in_features, 256),    
                                nn.ReLU(),               
                                nn.Dropout(0.5),       
                                nn.Linear(256, NUM_CLASSES)       
                            )

if os.path.exists("best_animals_loaded_model_2.pth"):
    checkpoint = torch.load("best_animals_loaded_model_2.pth")
    loaded_model_2.load_state_dict(checkpoint['model_state_dict'])
    print(f"\nЗагружена лучшая модель с точностью {checkpoint['best_val_acc']:.2f}%")

loaded_model_2 = loaded_model_2.to(DEVICE)
loaded_model_2.eval()

#print(loaded_model_2)


print("\nЧАСТЬ A: Фильтры первого слоя")
filters = loaded_model_2.conv1.weight.detach().cpu()
print(filters.shape) # [out_channels, in_channels, H, W]
filters_norm = (filters - filters.min()) / (filters.max() - filters.min())

fig, axes = plt.subplots(8, 8, figsize=(12, 12))
for i in range(64):
    axes[i//8, i%8].imshow(filters_norm[i].permute(1,2,0).numpy())
    axes[i//8, i%8].axis('off')
plt.suptitle('Фильтры conv1 (64 шт 7x7)')
plt.tight_layout()
plt.savefig('A_filters.png')
plt.show()


print("\nЧАСТЬ B: Карты активаций")

def get_acts(model, img):
    activations = {}
    def hook_fn(name):
        def hook(module, input, output):
            activations[name] = output.detach().cpu()
        return hook
    h1 = model.layer1.register_forward_hook(hook_fn('layer1'))
    h3 = model.layer3.register_forward_hook(hook_fn('layer3'))
    with torch.no_grad():
        out = model(img.unsqueeze(0).to(DEVICE))
        print(out)
    h1.remove(); h3.remove()
    return activations

def plot_acts(acts, name, title):
    act = acts[name][0][:16]
    fig, axes = plt.subplots(4, 4, figsize=(8, 8))
    for i in range(16):
        axes[i//4, i%4].imshow(act[i])
        axes[i//4, i%4].axis('off')
    plt.suptitle(title)
    plt.tight_layout()
    plt.savefig(f'B_{title}.png')
    plt.show()

print(test_loader.batch_size)
# Ищем правильное и неправильное изображение
model = loaded_model_2.eval()
correct, wrong = None, None
with torch.no_grad():
    k = 0
    for x, y in test_loader:
        if k < 20:
            k += 1
            continue
        x, y = x.to(DEVICE), y.to(DEVICE)
        p = model(x).argmax(1)
        for i in range(len(x)):
            if p[i]==y[i] and correct is None: correct = (x[i].cpu(), y[i].cpu())
            elif p[i]!=y[i] and wrong is None: wrong = (x[i].cpu(), y[i].cpu(), p[i].cpu())
        if correct and wrong: break

class_names = train_dataset.classes
print(f"Правильно: {class_names[correct[1]]}")
print(f"Ошибка: {class_names[wrong[1]]} -> {class_names[wrong[2]]}")

for img, label, title in [(correct[0], correct[1], "Правильно"), (wrong[0], wrong[1], "Ошибка")]:
    img_display = img.numpy().transpose(1, 2, 0)  # [C, H, W] -> [H, W, C]
    img_display = img_display * np.array(imagenet_std) + np.array(imagenet_mean)  # денормализация
    img_display = np.clip(img_display, 0, 1)  # обрезаем в диапазон [0, 1]
    
    plt.figure(figsize=(6, 6))
    plt.imshow(img_display)
    plt.title(f'{title}: {class_names[label]}')
    plt.axis('off')
    plt.show()

    acts = get_acts(model, img)
    plot_acts(acts, 'layer1', f'layer1_{title}')
    plot_acts(acts, 'layer3', f'layer3_{title}')

# ============================================
# ЧАСТЬ C: Grad-CAM
# ============================================
print("\nЧАСТЬ C: Grad-CAM")
import torch.nn.functional as F

class GradCAM:
    def __init__(self, model):
        self.model = model
        self.acts = None
        self.grads = None
        model.layer4.register_forward_hook(self.save_acts)
        model.layer4.register_full_backward_hook(self.save_grads)
    def save_acts(self, m, i, o): self.acts = o.detach()
    def save_grads(self, m, gi, grad_output): self.grads = grad_output[0].detach()
    def cam(self, img, cls=None):
        out = self.model(img.unsqueeze(0))
        if cls is None: cls = out.argmax(1).item()
        self.model.zero_grad()
        out[0, cls].backward()
        w = self.grads.mean((2,3), keepdim=True)
        cam = (w * self.acts).sum(1, keepdim=True)
        cam = F.relu(cam)
        cam = F.interpolate(cam, size=224, mode='bilinear')[0,0].cpu().numpy()
        return (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)

# Ищем 8 изображений
correct, wrong = [], []
with torch.no_grad():
    for x, y in test_loader:
        x, y = x.to(DEVICE), y.to(DEVICE)
        p = model(x).argmax(1)
        for i in range(len(x)):
            if p[i]==y[i] and len(correct)<4 and y[i].item() not in [c[1].item() for c in correct]:
                correct.append((x[i].cpu(), y[i].cpu()))
            elif p[i]!=y[i] and len(wrong)<4:
                wrong.append((x[i].cpu(), y[i].cpu(), p[i].cpu()))
        if len(correct)>=4 and len(wrong)>=4: break

gc = GradCAM(model)
all_imgs = correct + wrong
for i, item in enumerate(all_imgs):
    img, true = item[0], item[1]
    pred = item[2] if len(item)>2 else true
    cam = gc.cam(img.to(DEVICE))
    img_disp = np.clip(img.numpy().transpose(1,2,0)*imagenet_std + imagenet_mean, 0, 1)
    plt.figure(figsize=(8,4))
    plt.subplot(121); plt.imshow(img_disp); plt.axis('off'); plt.title(f'Исходный: {class_names[true]}')
    plt.subplot(122); plt.imshow(img_disp); plt.imshow(cam, cmap='jet', alpha=0.5); plt.axis('off')
    plt.title(f'GradCAM\nПредсказанный: {class_names[pred]}')
    plt.tight_layout(); plt.savefig(f'C_{i}.png'); plt.show()

# Сравнение для ошибки
if wrong:
    img, true, pred = wrong[0]
    plt.figure(figsize=(12,4))
    img_disp = np.clip(img.numpy().transpose(1,2,0)*imagenet_std + imagenet_mean, 0, 1)
    for i, (cls, title) in enumerate([(true, f'Истинный {class_names[true]}'), 
                                       (pred, f'Предсказанный {class_names[pred]}')]):
        cam = gc.cam(img.to(DEVICE), cls)
        plt.subplot(1,3,i+2); plt.imshow(img_disp); plt.imshow(cam, cmap='jet', alpha=0.5)
        plt.axis('off'); plt.title(title)
    plt.subplot(131); plt.imshow(img_disp); plt.axis('off'); plt.title('Оригинал')
    plt.tight_layout(); plt.savefig('C_compare.png'); plt.show()

# ============================================
# ЧАСТЬ D: Анализ ошибок
# ============================================
print("\nЧАСТЬ D: Анализ ошибок")
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from collections import Counter

all_preds, all_labels = [], []
with torch.no_grad():
    for x, y in test_loader:
        all_preds.extend(model(x.to(DEVICE)).argmax(1).cpu().numpy())
        all_labels.extend(y.numpy())
all_preds, all_labels = np.array(all_preds), np.array(all_labels)

plt.figure(figsize=(10,10))
ConfusionMatrixDisplay(confusion_matrix(all_labels, all_preds), display_labels=class_names).plot(ax=plt.gca(), xticks_rotation=45)
plt.title(f'Confusion Matrix (Acc: {np.mean(all_preds==all_labels)*100:.1f}%)')
plt.tight_layout(); plt.savefig('D_matrix.png'); plt.show()

errors = [(class_names[t], class_names[p]) for t,p in zip(all_labels[all_preds!=all_labels], all_preds[all_preds!=all_labels])]
print("ТОП-3 ошибок:")
for (t,p),c in Counter(errors).most_common(3):
    print(f"{t} → {p}: {c} раз")

