import torch
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from torch.utils.data import DataLoader
from torchvision import datasets
from transformers import CLIPModel, CLIPProcessor
import os

os.makedirs('results', exist_ok=True)

# ======================== ЧАСТЬ A. ПОДГОТОВКА ДАТАСЕТА ========================
print("=" * 60)
print("ЧАСТЬ A. ПОДГОТОВКА ДАТАСЕТА")
print("=" * 60)

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")

model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)
print("Модель CLIP успешно загружена")

def collate_fn(batch):
    images, labels = zip(*batch)
    return list(images), torch.tensor(labels)

test_dataset = datasets.CIFAR100(root='./data', train=False, download=True, transform=None)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False, collate_fn=collate_fn)

class_names = test_dataset.classes
print(f"Классов: {len(class_names)}")
print(f"Примеры: {class_names[:5]}")

# ======================== ЧАСТЬ B. БАЗОВАЯ КЛАССИФИКАЦИЯ ========================
print("\n" + "=" * 60)
print("ЧАСТЬ B. ZERO-SHOT КЛАССИФИКАЦИЯ (БАЗОВЫЙ ПРОМПТ)")
print("=" * 60)

# Базовый промпт
base_descriptions = [f"a photo of a {name}" for name in class_names]
base_inputs = processor(text=base_descriptions, return_tensors="pt", padding=True).to(device)                               #"pt" = PyTorch - возвращать данные как тензоры PyTorch (не списки) padding=True	добавляет специальные токены, чтобы все строки стали одинаковой длины (выравнивание)

with torch.no_grad():
    base_outputs = model.get_text_features(**base_inputs)
    base_features = base_outputs.pooler_output                                                                               # pooler_output:   Это финальный вектор размерностью 512
    base_features = base_features / base_features.norm(dim=-1, keepdim=True)                                                   # dim -1 длина каждого вектора

all_preds = []
all_labels = []

model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        image_inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
        image_outputs = model.get_image_features(**image_inputs)
        image_features = image_outputs.pooler_output
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        similarity = image_features @ base_features.T
        preds = similarity.argmax(dim=1)
        
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())

all_preds = np.array(all_preds)
all_labels = np.array(all_labels)
base_accuracy = np.mean(all_preds == all_labels)
print(f"Zero-shot accuracy (базовый 'a photo of a'): {base_accuracy * 100:.2f}%")


# ======================== МАТРИЦА ОШИБОК ДЛЯ CIFAR-100 ========================
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
import matplotlib.pyplot as plt

# Вычисляем матрицу ошибок
cm = confusion_matrix(all_labels, all_preds)

# Для 100 классов делаем большой график, но без подписей (они нечитаемы)
n_classes = len(class_names)
figsize = (20, 18)  # фиксированный большой размер для 100 классов

# Создаем фигуру
fig, ax = plt.subplots(figsize=figsize)

# Отображаем матрицу ошибок
disp = ConfusionMatrixDisplay(cm, display_labels=class_names)
disp.plot(ax=ax, xticks_rotation=90, cmap='Blues', values_format='d')

# Настройки для лучшего отображения
ax.set_title("Confusion Matrix (CLIP zero-shot on CIFAR-100)", fontsize=14)
ax.set_xlabel("Predicted Class", fontsize=12)
ax.set_ylabel("True Class", fontsize=12)

# Уменьшаем размер шрифта подписей, но делаем их видимыми
ax.tick_params(axis='x', labelsize=6, rotation=90)
ax.tick_params(axis='y', labelsize=6)

# Добавляем сетку для лучшей читаемости
ax.grid(True, alpha=0.3, linestyle='--')

plt.tight_layout()
plt.savefig('confusion_matrix_cifar100.png', dpi=200, bbox_inches='tight')
plt.show()

print("Матрица ошибок сохранена как 'confusion_matrix_cifar100.png'")

# Дополнительно: компактная версия для анализа (каждый 5-й класс)
print("\n" + "=" * 60)
print("КОМПАКТНАЯ МАТРИЦА ОШИБОК (каждый 5-й класс)")
print("=" * 60)

# Берем каждый 5-й класс для компактного отображения
step = 5
indices = list(range(0, n_classes, step))
cm_compact = cm[indices][:, indices]
labels_compact = [class_names[i] for i in indices]

plt.figure(figsize=(16, 14))
disp_compact = ConfusionMatrixDisplay(cm_compact, display_labels=labels_compact)
disp_compact.plot(xticks_rotation=90, cmap='Blues', values_format='d')
plt.title("Confusion Matrix (CLIP zero-shot on CIFAR-100) - Every 5th class", fontsize=14)
plt.tight_layout()
plt.savefig('confusion_matrix_compact.png', dpi=150, bbox_inches='tight')
plt.show()

print("Компактная матрица ошибок сохранена как 'confusion_matrix_compact.png'")

# ======================== ЧАСТЬ C. ЭКСПЕРИМЕНТЫ С ПРОМПТАМИ ========================
print("\n" + "=" * 60)
print("ЧАСТЬ C. ЭКСПЕРИМЕНТЫ С ПРОМПТАМИ")
print("=" * 60)

# Словарь с уникальными контекстными шаблонами для разных типов классов
def get_custom_prompt(class_name):
    """Генерация уникального промпта в зависимости от класса"""
    class_lower = class_name.lower()
    
    # Животные
    if class_lower in ['bear', 'beaver', 'camel', 'dolphin', 'elephant', 'fox', 'hamster', 'kangaroo', 'leopard', 'lion', 'otter', 'rabbit', 'raccoon', 'seal', 'shrew', 'squirrel', 'tiger', 'wolf']:
        return f"a wild {class_lower} animal in its natural habitat"
    # Домашние животные
    elif class_lower in ['baby', 'boy', 'girl', 'man', 'woman']:
        return f"a person who is a {class_lower}"
    # Птицы
    elif class_lower in ['beaver', 'butterfly', 'bee', 'beetle', 'caterpillar', 'cockroach', 'crab', 'lobster', 'snail', 'spider', 'worm']:
        return f"a close-up macro photo of a {class_lower}"
    # Цветы
    elif class_lower in ['rose', 'tulip', 'sunflower', 'daisy', 'orchid', 'poppy']:
        return f"a beautiful blooming {class_lower} flower"
    # Деревья
    elif class_lower in ['maple_tree', 'oak_tree', 'palm_tree', 'pine_tree', 'willow_tree']:
        return f"a large {class_lower.replace('_', ' ')} in a forest"
    # Фрукты и овощи
    elif class_lower in ['apple', 'pear', 'orange', 'mushroom', 'sweet_pepper']:
        return f"a fresh {class_lower.replace('_', ' ')} on a wooden table"
    # Транспорт
    elif class_lower in ['bicycle', 'bus', 'motorcycle', 'train', 'streetcar', 'truck', 'rocket']:
        return f"a modern {class_lower} on the street"
    # Мебель
    elif class_lower in ['bed', 'chair', 'couch', 'table', 'wardrobe']:
        return f"a piece of furniture: {class_lower}"
    # Посуда
    elif class_lower in ['bowl', 'cup', 'plate', 'bottle']:
        return f"a {class_lower} on a dining table"
    # Электроника
    elif class_lower in ['television', 'computer', 'telephone', 'keyboard', 'lamp']:
        return f"an electronic device: {class_lower}"
    else:
        return f"a photo of a {class_lower}"

# 5 различных шаблонов для сравнения
templates = {
    "1. Только название класса": lambda x: x,
    "2. a photo of a": lambda x: f"a photo of a {x}",
    "3. a photograph of a": lambda x: f"a photograph of a {x}",
    "4. an image of a": lambda x: f"an image of a {x}",
    "5. Уникальные контекстные промпты": get_custom_prompt
}

results = {}

for template_name, template_func in templates.items():
    print(f"\nТестирование: {template_name}")
    
    # Генерируем уникальные промпты для каждого класса
    text_descriptions = [template_func(name) for name in class_names]
    text_inputs = processor(text=text_descriptions, return_tensors="pt", padding=True).to(device)
    
    with torch.no_grad():
        text_outputs = model.get_text_features(**text_inputs)
        text_features_temp = text_outputs.pooler_output
        text_features_temp = text_features_temp / text_features_temp.norm(dim=-1, keepdim=True)
    
    all_preds_temp = []
    with torch.no_grad():
        for images, labels in test_loader:
            image_inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
            image_outputs = model.get_image_features(**image_inputs)
            image_features = image_outputs.pooler_output
            image_features = image_features / image_features.norm(dim=-1, keepdim=True)
            similarity = image_features @ text_features_temp.T
            preds = similarity.argmax(dim=1)
            all_preds_temp.extend(preds.cpu().numpy())
    
    acc = np.mean(np.array(all_preds_temp) == all_labels)
    results[template_name] = acc
    print(f"  Accuracy: {acc * 100:.2f}%")

# Ансамблирование лучших 5 шаблонов
print("\n" + "-" * 60)
print("АНСАМБЛИРОВАНИЕ ПРОМПТОВ")
print("-" * 60)

ensemble_templates = [
    "a photo of a {}",
    "a photograph of a {}",
    "an image of a {}",
    "a picture of a {}",
    "a {} in a photo"
]

text_features_ensemble = []
for class_name in class_names:
    descriptions = [t.format(class_name) for t in ensemble_templates]
    text_inputs = processor(text=descriptions, return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        features = model.get_text_features(**text_inputs)
        features = features.pooler_output
        features = features / features.norm(dim=-1, keepdim=True)
        avg_feature = features.mean(dim=0)
        avg_feature = avg_feature / avg_feature.norm()
        text_features_ensemble.append(avg_feature)

text_features_ensemble = torch.stack(text_features_ensemble)

all_preds_ensemble = []
with torch.no_grad():
    for images, labels in test_loader:
        image_inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
        image_outputs = model.get_image_features(**image_inputs)
        image_features = image_outputs.pooler_output
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        similarity = image_features @ text_features_ensemble.T
        preds = similarity.argmax(dim=1)
        all_preds_ensemble.extend(preds.cpu().numpy())

ensemble_acc = np.mean(np.array(all_preds_ensemble) == all_labels)
print(f"Ансамбль (5 шаблонов): {ensemble_acc * 100:.2f}%")

# Итоговая таблица
print("\n" + "=" * 60)
print("ИТОГОВАЯ ТАБЛИЦА ПО ПРОМПТАМ")
print("=" * 60)

worst_acc = min(results.values())
best_acc = max(results.values())

print(f"\n{'Шаблон':50s} | {'Accuracy':>10s}")
print("-" * 65)
for name, acc in results.items():
    print(f"{name:50s} | {acc * 100:>9.2f}%")
print("-" * 65)
print(f"{'Худший одиночный шаблон':50s} | {worst_acc * 100:>9.2f}%")
print(f"{'Лучший одиночный шаблон':50s} | {best_acc * 100:>9.2f}%")
print(f"{'Ансамбль (5 шаблонов)':50s} | {ensemble_acc * 100:>9.2f}%")

# Сохраняем результаты
with open('results/prompt_results.txt', 'w') as f:
    f.write("ИТОГОВАЯ ТАБЛИЦА ПО ПРОМПТАМ\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"{'Шаблон':50s} | {'Accuracy':>10s}\n")
    f.write("-" * 65 + "\n")
    for name, acc in results.items():
        f.write(f"{name:50s} | {acc * 100:>9.2f}%\n")
    f.write("-" * 65 + "\n")
    f.write(f"{'Худший одиночный шаблон':50s} | {worst_acc * 100:>9.2f}%\n")
    f.write(f"{'Лучший одиночный шаблон':50s} | {best_acc * 100:>9.2f}%\n")
    f.write(f"{'Ансамбль (5 шаблонов)':50s} | {ensemble_acc * 100:>9.2f}%\n")

# Вывод примеров уникальных промптов
print("\n" + "=" * 60)
print("ПРИМЕРЫ УНИКАЛЬНЫХ ПРОМПТОВ ДЛЯ РАЗНЫХ КЛАССОВ")
print("=" * 60)
example_classes = ['bear', 'rose', 'apple', 'bus', 'baby']
for class_name in example_classes:
    if class_name in class_names:
        prompt = get_custom_prompt(class_name)
        print(f"{class_name:15s} -> {prompt}")

# ======================== ВИЗУАЛИЗАЦИЯ ТОП ОШИБОК ========================
print("\n" + "=" * 60)
print("ВИЗУАЛИЗАЦИЯ ТОП ОШИБОК CLIP")
print("=" * 60)

# Используем базовые текстовые фичи
all_similarities = []  
all_preds_detailed = []
all_images = []

with torch.no_grad():
    for images, labels in test_loader:
        image_inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
        image_outputs = model.get_image_features(**image_inputs)
        image_features = image_outputs.pooler_output
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        similarity = image_features @ base_features.T  
        preds = similarity.argmax(dim=-1)
        
        for i in range(len(images)):
            all_images.append(images[i])
            all_preds_detailed.append(preds[i].item())
            all_similarities.append(similarity[i, preds[i]].item())  

all_preds_detailed = np.array(all_preds_detailed)
all_similarities = np.array(all_similarities)  

error_mask = all_preds_detailed != all_labels
error_indices = np.where(error_mask)[0]

if len(error_indices) > 0:
    error_scores = all_similarities[error_mask]  
    error_true_labels = all_labels[error_mask]
    error_pred_labels = all_preds_detailed[error_mask]
    error_images = [all_images[i] for i in error_indices]
    
    # Сортируем по убыванию сходства (чем выше, тем увереннее модель ошиблась)
    sorted_error_idx = np.argsort(error_scores)[::-1]
    top_errors_indices = sorted_error_idx[:8]
    
    fig, axes = plt.subplots(2, 4, figsize=(20, 12))
    axes = axes.flatten()
    
    print("\nТоп-8 ошибок с наибольшим сходством:\n")
    
    with open('results/top_errors.txt', 'w') as f:
        f.write("ТОП-8 ОШИБОК CLIP\n")
        f.write("=" * 60 + "\n\n")
        
        for plot_idx, err_pos in enumerate(top_errors_indices):
            img = error_images[err_pos]
            true_label = error_true_labels[err_pos]
            pred_label = error_pred_labels[err_pos]
            similarity_score = error_scores[err_pos]  
            
            axes[plot_idx].imshow(img)
            axes[plot_idx].axis('off')
            
            true_name = class_names[true_label].replace('_', ' ')
            pred_name = class_names[pred_label].replace('_', ' ')
            
            title = f"True: {true_name}\nPred: {pred_name}\nSim: {similarity_score:.3f}"
            axes[plot_idx].set_title(title, fontsize=10, pad=5)
            
            print(f"\n--- Ошибка {plot_idx + 1} ---")
            print(f"  Истинный класс: {class_names[true_label]}")
            print(f"  Предсказанный класс: {class_names[pred_label]} (сходство: {similarity_score:.3f})")
            
            f.write(f"\n--- Ошибка {plot_idx + 1} ---\n")
            f.write(f"  Истинный класс: {class_names[true_label]}\n")
            f.write(f"  Предсказанный класс: {class_names[pred_label]} (сходство: {similarity_score:.3f})\n")
    
    plt.suptitle("Топ-8 ошибок CLIP на CIFAR-100", fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('results/top_errors.png', dpi=150, bbox_inches='tight')
    plt.close()
    print("\nВизуализация ошибок сохранена в results/top_errors.png")

print("\n" + "=" * 60)
print("РЕЗУЛЬТАТЫ СОХРАНЕНЫ В ПАПКУ 'results'")
print("=" * 60)