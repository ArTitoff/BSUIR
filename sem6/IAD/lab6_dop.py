# -*- coding: utf-8 -*-
"""Сравнение CLIP VS SigLIP на CIFAR-100"""

import torch
import numpy as np
from torch.utils.data import DataLoader
from torchvision import datasets
from transformers import CLIPModel, CLIPProcessor, AutoProcessor, AutoModel
import os

os.makedirs('test_res', exist_ok=True)

# ======================== ЗАГРУЗКА ДАННЫХ ========================
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Устройство: {device}")

def collate_fn(batch):
    images, labels = zip(*batch)
    return list(images), torch.tensor(labels)

test_dataset = datasets.CIFAR100(root='./data', train=False, download=True, transform=None)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False, collate_fn=collate_fn)
class_names = test_dataset.classes

# ======================== CLIP (ViT-B/32) ========================
print("\n" + "=" * 50)
print("CLIP ViT-B/32")
print("=" * 50)

clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32").to(device)
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")

texts_clip = [f"a photo of a {name}" for name in class_names]
text_inputs_clip = clip_processor(text=texts_clip, return_tensors="pt", padding=True).to(device)

with torch.no_grad():
    text_outputs_clip = clip_model.get_text_features(**text_inputs_clip)
    text_features_clip = text_outputs_clip.pooler_output
    text_features_clip = text_features_clip / text_features_clip.norm(dim=-1, keepdim=True)

all_preds_clip = []
all_labels = []

clip_model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        image_inputs = clip_processor(images=images, return_tensors="pt", padding=True).to(device)
        image_outputs = clip_model.get_image_features(**image_inputs)
        image_features = image_outputs.pooler_output
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        similarity = image_features @ text_features_clip.T
        preds = similarity.argmax(dim=1)
        
        all_preds_clip.extend(preds.cpu().numpy())
        all_labels.extend(labels.numpy())

all_preds_clip = np.array(all_preds_clip)
all_labels = np.array(all_labels)
clip_acc = np.mean(all_preds_clip == all_labels)
print(f"CLIP accuracy: {clip_acc * 100:.2f}%")

# ======================== SigLIP (base-patch16-224) ========================
print("\n" + "=" * 50)
print("SigLIP (google/siglip-base-patch16-224)")
print("=" * 50)

siglip_model = AutoModel.from_pretrained("google/siglip-base-patch16-224").to(device)
siglip_processor = AutoProcessor.from_pretrained("google/siglip-base-patch16-224")

# Получение ТОЛЬКО текстовых эмбеддингов SigLIP через text_model
texts_siglip = [f"This is a photo of {name}." for name in class_names]
text_inputs_siglip = siglip_processor(
    text=texts_siglip,
    return_tensors="pt",
    padding="max_length",
    max_length=64
).to(device)

with torch.no_grad():
    # Используем text_model отдельно (не всю модель целиком)
    text_features_siglip = siglip_model.text_model(**text_inputs_siglip).pooler_output
    text_features_siglip = text_features_siglip / text_features_siglip.norm(dim=-1, keepdim=True)

# Классификация SigLIP
all_preds_siglip = []

siglip_model.eval()
with torch.no_grad():
    for images, labels in test_loader:
        image_inputs = siglip_processor(images=images, return_tensors="pt").to(device)
        # Используем vision_model отдельно
        image_outputs = siglip_model.vision_model(**image_inputs)
        image_features = image_outputs.pooler_output
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        similarity = image_features @ text_features_siglip.T
        preds = similarity.argmax(dim=1)
        
        all_preds_siglip.extend(preds.cpu().numpy())

all_preds_siglip = np.array(all_preds_siglip)
siglip_acc = np.mean(all_preds_siglip == all_labels)
print(f"SigLIP accuracy: {siglip_acc * 100:.2f}%")

# ======================== СРАВНЕНИЕ ========================
print("\n" + "=" * 50)
print("СРАВНЕНИЕ")
print("=" * 50)
print(f"CLIP:    {clip_acc * 100:.2f}%")
print(f"SigLIP:  {siglip_acc * 100:.2f}%")
print(f"Разница: {(siglip_acc - clip_acc) * 100:+.2f}%")

# Анализ по классам
class_acc_clip = {}
class_acc_siglip = {}

for i in range(len(class_names)):
    mask = all_labels == i
    if mask.sum() > 0:
        class_acc_clip[class_names[i]] = np.mean(all_preds_clip[mask] == all_labels[mask])
        class_acc_siglip[class_names[i]] = np.mean(all_preds_siglip[mask] == all_labels[mask])

improvements = []
for name in class_names:
    diff = class_acc_siglip[name] - class_acc_clip[name]
    improvements.append((name, diff, class_acc_clip[name], class_acc_siglip[name]))

improvements.sort(key=lambda x: x[1], reverse=True)

print("\n" + "=" * 50)
print("ТОП-10 УЛУЧШЕНИЙ SigLIP VS CLIP")
print("=" * 50)
print(f"{'Класс':<25s} | {'CLIP':>8s} | {'SigLIP':>8s} | {'Улучшение':>10s}")
print("-" * 58)
for name, diff, clip_c, siglip_c in improvements[:10]:
    print(f"{name:<25s} | {clip_c*100:>7.1f}% | {siglip_c*100:>7.1f}% | {diff*100:>+9.1f}%")

print("\nТОП-10 УХУДШЕНИЙ:")
for name, diff, clip_c, siglip_c in improvements[-10:][::-1]:
    print(f"{name:<25s} | {clip_c*100:>7.1f}% | {siglip_c*100:>7.1f}% | {diff*100:>+9.1f}%")

# Худшие классы CLIP
worst_clip = sorted([(name, class_acc_clip[name]) for name in class_names], key=lambda x: x[1])[:10]

print("\n" + "=" * 50)
print("ХУДШИЕ КЛАССЫ ДЛЯ CLIP (результаты SigLIP)")
print("=" * 50)
for name, acc in worst_clip:
    sig = class_acc_siglip[name]
    status = "✓ улучшился" if sig > acc else "✗ ухудшился"
    print(f"{name:<25s}: CLIP={acc*100:5.1f}% → SigLIP={sig*100:5.1f}% ({status})")

# Сохраняем
with open('test_res/clip_vs_siglip.txt', 'w') as f:
    f.write("СРАВНЕНИЕ CLIP VS SigLIP на CIFAR-100\n")
    f.write("=" * 60 + "\n\n")
    f.write(f"CLIP accuracy:   {clip_acc * 100:.2f}%\n")
    f.write(f"SigLIP accuracy: {siglip_acc * 100:.2f}%\n")
    f.write(f"Разница:         {(siglip_acc - clip_acc) * 100:+.2f}%\n\n")
    
    f.write("ТОП-10 УЛУЧШЕНИЙ:\n")
    for name, diff, clip_c, siglip_c in improvements[:10]:
        f.write(f"  {name:<25s}: {clip_c*100:5.1f}% → {siglip_c*100:5.1f}% (+{diff*100:.1f}%)\n")

print("\nРезультаты сохранены в test_res/clip_vs_siglip.txt")