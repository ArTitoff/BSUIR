import torch
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import DataLoader
from torchvision import datasets, transforms as T
from transformers import CLIPModel, CLIPProcessor
from sklearn.manifold import TSNE
import os

os.makedirs('res_', exist_ok=True)

# ======================== ЗАГРУЗКА МОДЕЛИ И ДАТАСЕТА ========================
print("=" * 60)
print("ЗАГРУЗКА МОДЕЛИ И ДАТАСЕТА")
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
print(f"Классов: {class_names}")

# ======================== ЧАСТЬ A. ИНДЕКСИРОВАНИЕ КОЛЛЕКЦИИ ИЗОБРАЖЕНИЙ ========================
print("\n" + "=" * 60)
print("ЧАСТЬ A. ИНДЕКСИРОВАНИЕ КОЛЛЕКЦИИ ИЗОБРАЖЕНИЙ")
print("=" * 60)

all_image_features = []
all_images_raw = []
all_labels_list = []

model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        image_inputs = processor(images=list(images), return_tensors="pt", padding=True).to(device)
        features = model.get_image_features(**image_inputs)
        features = features.pooler_output
        features = features / features.norm(dim=-1, keepdim=True)
        all_image_features.append(features.cpu())
        all_images_raw.append(torch.stack([T.ToTensor()(img) for img in images]))
        all_labels_list.append(labels)

all_image_features = torch.cat(all_image_features)
all_images_raw = torch.cat(all_images_raw)
all_labels_list = torch.cat(all_labels_list)

print(f"Проиндексировано изображений: {len(all_image_features)}")
print(f"Размерность эмбеддинга: {all_image_features.shape[1]}")

# Сохраняем индекс
torch.save({
    'features': all_image_features,
    'labels': all_labels_list,
}, 'res_/image_index.pt')
print("Индекс сохранен в res_/image_index.pt")

# ======================== ЧАСТЬ B. ФУНКЦИЯ ПОИСКА ========================
print("\n" + "=" * 60)
print("ЧАСТЬ B. ФУНКЦИЯ ПОИСКА")
print("=" * 60)

def search_by_text(query, image_features, top_k=8):
    """Поиск изображений по текстовому запросу"""
    text_inputs = processor(text=[query], return_tensors="pt", padding=True).to(device)
    with torch.no_grad():
        text_outputs = model.get_text_features(**text_inputs)
        text_feat = text_outputs.pooler_output
        text_feat = text_feat / text_feat.norm(dim=-1, keepdim=True)
        similarity = (image_features @ text_feat.cpu().T).squeeze()
        top_indices = similarity.argsort(descending=True)[:top_k]
        top_scores = similarity[top_indices]
        return top_indices, top_scores

def visualize_search_results(query, indices, scores, images, labels, class_names):
    """Визуализация результатов поиска"""
    n = len(indices)
    fig, axes = plt.subplots(1, n, figsize=(2.5 * n, 3))
    fig.suptitle(f'Запрос: "{query}"', fontsize=14, y=1.02)
    for i, (idx, score) in enumerate(zip(indices, scores)):
        img = images[idx].permute(1, 2, 0).numpy().clip(0, 1)
        axes[i].imshow(img)
        axes[i].set_title(f"{class_names[labels[idx]]}\n{score:.3f}", fontsize=9)
        axes[i].axis('off')
    plt.tight_layout()
    return fig

print("Функции поиска созданы")

# ======================== ЧАСТЬ C. ТЕСТИРОВАНИЕ СИСТЕМЫ ПОИСКА ========================
print("\n" + "=" * 60)
print("ЧАСТЬ C. ТЕСТИРОВАНИЕ СИСТЕМЫ ПОИСКА")
print("=" * 60)

# Запросы по классу (прямое название объекта)
queries_by_class = [
    "a photo of a bear",
    "a photo of a dolphin",
    "a photo of a chair",
    "a photo of a rose",
    "a photo of a rocket",
]

# Запросы по атрибуту (описание свойств без названия класса)
queries_by_attribute = [
    "a large dangerous wild animal",
    "an animal that swims in the ocean",
    "something you sit on",
    "a beautiful flower",
    "a vehicle that flies",
]

# Абстрактные запросы (нестандартные описания)
queries_abstract = [
    "something cute and fluffy",
    "something that can kill you",
    "red and delicious fruit",
    "something that makes sound",
    "a living creature with four legs",
]

# Объединяем все запросы
all_queries = queries_by_class + queries_by_attribute + queries_abstract
print(f"\nВсего запросов: {len(all_queries)}")

# Выполняем поиск по каждому запросу и сохраняем результаты
print("\nРезультаты поиска:")
for i, query in enumerate(all_queries):
    print(f"\n{i+1}. Запрос: '{query}'")
    indices, scores = search_by_text(query, all_image_features, top_k=8)
    print(f"   Найдено {len(indices)} изображений")
    print(f"   Топ-3 класса: {class_names[all_labels_list[indices[0]]]}, {class_names[all_labels_list[indices[1]]]}, {class_names[all_labels_list[indices[2]]]}")
    
    fig = visualize_search_results(query, indices, scores, all_images_raw, all_labels_list, class_names)
    plt.savefig(f'res_/search_result_{i+1:02d}.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"   Сохранено: res_/search_result_{i+1:02d}.png")

print("\nСохранено 15 результатов поиска в папку res_/")

# ======================== ЧАСТЬ D. АНАЛИЗ КАЧЕСТВА ПОИСКА ========================
print("\n" + "=" * 60)
print("ЧАСТЬ D. АНАЛИЗ КАЧЕСТВА ПОИСКА")
print("=" * 60)

def recall_at_k(class_names, image_features, labels, k=10):
    """Вычисление Recall@10 для всех классов"""
    recalls = {}
    
    for class_idx, class_name in enumerate(class_names):
        query = f"a photo of a {class_name}"
        top_indices, _ = search_by_text(query, image_features, top_k=k)
        top_labels = labels[top_indices].numpy()
        hit = int(class_idx in top_labels)
        recalls[class_name] = hit
    
    mean_recall = np.mean(list(recalls.values()))
    return recalls, mean_recall

print("\nВычисление Recall@10 для всех 100 классов...")
recalls_k10, mean_recall = recall_at_k(class_names, all_image_features, all_labels_list, k=10)

# Сохраняем результаты Recall@10
with open('res_/recall_at_10.txt', 'w') as f:
    f.write("RECALL@10 ДЛЯ ВСЕХ КЛАССОВ\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"Mean Recall@10: {mean_recall * 100:.1f}%\n\n")
    f.write("Детализация по классам:\n")
    f.write("-" * 40 + "\n")
    
    classes_found = []
    classes_not_found = []
    
    for class_name, recall in recalls_k10.items():
        if recall:
            classes_found.append(class_name)
        else:
            classes_not_found.append(class_name)
        f.write(f"{class_name:30s}: {'✓' if recall else '✗'}\n")

print(f"\nMean Recall@10: {mean_recall * 100:.1f}%")
print(f"Классов в топ-10: {len(classes_found)} / {len(class_names)}")
print(f"Классов НЕ в топ-10: {len(classes_not_found)}")

if classes_not_found:
    print(f"\nКлассы, которые НЕ попали в топ-10:")
    for cls in classes_not_found[:15]:
        print(f"  - {cls}")

# ======================== t-SNE ВИЗУАЛИЗАЦИЯ ========================
print("\n" + "=" * 60)
print("t-SNE ВИЗУАЛИЗАЦИЯ ЭМБЕДДИНГОВ")
print("=" * 60)

# Вычисляем текстовые эмбеддинги для всех классов
print("Вычисление текстовых эмбеддингов...")
text_descriptions = [f"a photo of a {name}" for name in class_names]
text_inputs = processor(text=text_descriptions, return_tensors="pt", padding=True).to(device)
with torch.no_grad():
    text_outputs = model.get_text_features(**text_inputs)
    text_features = text_outputs.pooler_output
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

text_features_np = text_features.cpu().numpy()
image_features_np = all_image_features.numpy()

print(f"Выполняется t-SNE ({len(image_features_np)} изображений, 100 текстов)...")
sample_size = min(2000, len(image_features_np))
np.random.seed(42)
sample_idx = np.random.choice(len(image_features_np), sample_size, replace=False)
image_sample = image_features_np[sample_idx]
label_sample = all_labels_list.numpy()[sample_idx]

combined = np.vstack([image_sample, text_features_np])
tsne = TSNE(n_components=2, random_state=42, perplexity=30, max_iter=1000)
combined_2d = tsne.fit_transform(combined)

image_2d = combined_2d[:sample_size]
text_2d = combined_2d[sample_size:]

# Визуализация
plt.figure(figsize=(14, 12))
scatter = plt.scatter(
    image_2d[:, 0], image_2d[:, 1],
    c=label_sample, cmap='tab10',
    s=5, alpha=0.5, label='Изображения'
)

# Отображаем текстовые эмбеддинги (каждый 5-й класс для читаемости)
for i in range(0, len(class_names), 5):
    plt.scatter(text_2d[i, 0], text_2d[i, 1], s=200, marker='*', color='red', zorder=5)
    plt.annotate(
        class_names[i].replace('_', ' '),
        (text_2d[i, 0], text_2d[i, 1]),
        fontsize=8, fontweight='bold',
        xytext=(3, 3), textcoords='offset points'
    )

plt.colorbar(scatter, label='Класс')
plt.title("t-SNE: эмбеддинги изображений и текстовых описаний (CLIP)\nЗвездочки = текстовые эмбеддинги классов", fontsize=12)
plt.xlabel("t-SNE 1")
plt.ylabel("t-SNE 2")
plt.legend(['Изображения', 'Тексты классов'], loc='upper right')
plt.tight_layout()
plt.savefig('res_/tsne_visualization.png', dpi=150, bbox_inches='tight')
plt.close()

print("t-SNE визуализация сохранена в res_/tsne_visualization.png")

