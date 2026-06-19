import torch
import numpy as np
from torch.utils.data import DataLoader
from torchvision import datasets
from transformers import CLIPModel, CLIPProcessor
import os

os.makedirs('res_6', exist_ok=True)


device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")

model_id = "openai/clip-vit-base-patch32"
model = CLIPModel.from_pretrained(model_id).to(device)
processor = CLIPProcessor.from_pretrained(model_id)

def collate_fn(batch):
    images, labels = zip(*batch)
    return list(images), torch.tensor(labels)

test_dataset = datasets.CIFAR100(root='./data', train=False, download=True, transform=None)
test_loader = DataLoader(test_dataset, batch_size=64, shuffle=False, collate_fn=collate_fn)

class_names = test_dataset.classes
print(f"Классов: {len(class_names)}")

# ======================== 100 УНИКАЛЬНЫХ ПРОМПТОВ ========================

def get_unique_prompt(class_name):
    class_lower = class_name.lower()
    class_original = class_name
    
    # Словарь уникальных промптов для каждого класса (с сохранением названия класса)
    prompts = {
        'apple': f"a photo of a crisp red {class_original} fruit hanging from a tree",
        'aquarium_fish': f"an image of a colorful tropical {class_original} swimming in a glass tank",
        'baby': f"a photograph of a smiling infant {class_original} crawling on a soft carpet",
        'bear': f"a picture of a large brown grizzly {class_original} catching salmon in a river",
        'beaver': f"a photo of a {class_original} rodent ",
        'bed': f"an image of a cozy queen-sized {class_original} with white pillows and a blue blanket",
        'bee': f"a photograph of a fuzzy honey {class_original} collecting pollen from a yellow sunflower",
        'beetle': f"a picture of a shiny black {class_original} with six legs crawling on a green leaf",
        'bicycle': f"a photo of a red mountain {class_original} parked next to a tree in a park",
        'bottle': f"an image of an empty green glass {class_original} standing on a wooden table",
        'bowl': f"a photo of a {class_original} container",
        'boy': f"a picture of a young {class_original} wearing a red t-shirt playing with a toy car",
        'bridge': f"a photo of an old stone {class_original} crossing over a calm river",
        'bus': f"an image of a yellow school {class_original} driving on a city road",
        'butterfly': f"a photograph of a beautiful monarch {class_original} with orange and black wings",
        'camel': f"a picture of a tall one-humped {class_original} walking across a hot desert sand dune",
        'can': f"a photo of a silver soda {class_original} with condensation droplets on its surface",
        'castle': f"an image of a medieval stone {class_original} with tall towers and a drawbridge",
        'caterpillar': f"a photograph of a green striped {class_original} eating a fresh green leaf",
        'cattle': f"a picture of a brown and white {class_original} cow grazing in a green pasture",
        'chair': f"a photo of a wooden dining {class_original} with a cushioned seat",
        'chimpanzee': f"an image of a {class_original} swinging from a vine in the jungle canopy",
        'clock': f"a photograph of a round wall {class_original} showing 10:10 with roman numerals",
        'cloud': f"a picture of a fluffy white {class_original} in a bright blue sky",
        'cockroach': f"a photo of a brown {class_original} with long antennae scurrying across a floor",
        'computer': f"an image of a silver laptop {class_original} with a glowing screen on a desk",
        'couch': f"a photograph of a comfortable gray leather {class_original} in a living room",
        'crab': f"a picture of a red {class_original} with large pincers walking sideways on a sandy beach",
        'crocodile': f"a photo of a {class_original}",
        'cup': f"a photo of a {class_original}",
        'dinosaur': f"a photograph of a toy tyrannosaurus rex {class_original} figurine with sharp teeth",
        'dolphin': f"a picture of a friendly gray {class_original} jumping out of the ocean waves",
        'elephant': f"a photo of a large gray African {class_original} with long white tusks",
        'flatfish': f"a photo of a {class_original} fish",
        'forest': f"a photo of a  {class_original}",
        'fox': f"a picture of a red {class_original} with a bushy tail hunting in a snowy field",
        'girl': f"a photo of a young {class_original}",
        'hamster': f"an image of a small fluffy golden {class_original} running on an exercise wheel",
        'house': f"a photograph of a two-story white suburban {class_original} with a red roof",
        'kangaroo': f"a picture of a brown {class_original} hopping across the Australian outback",
        'keyboard': f"a photo of a black computer {class_original} with white backlit keys",
        'lamp': f"an image of a tall floor {class_original} with a yellow fabric shade in a dark corner",
        'lawn_mower': f"a photograph of a red push {class_original} sitting on freshly cut green grass",
        'leopard': f"a picture of a spotted {class_original} resting on a tree branch in the savanna",
        'lion': f"a photo of a male {class_original} with a large golden mane roaring loudly",
        'lizard': f"an image of a small green gecko {class_original} clinging to a white wall",
        'lobster': f"a photo of a {class_original}", 
        'man': f"a picture of an adult {class_original} wearing a business suit and tie walking to work",
        'maple_tree': f"a photo of a tall {class_original.replace('_', ' ')} with bright red autumn leaves",
        'motorcycle': f"an image of a black Harley Davidson {class_original} parked on a city street",
        'mountain': f"a photograph of a snow-capped rocky {class_original} peak against a blue sky",
        'mouse': f"a photo of a small rodent {class_original} animal",
        'mushroom': f"a photo of a red and white spotted toadstool {class_original} on forest floor",
        'oak_tree': f"an image of a massive old {class_original.replace('_', ' ')} with thick branches and acorns",
        'orange': f"a photograph of a round juicy {class_original} fruit with green leaves attached",
        'orchid': f"a picture of a beautiful purple {class_original} flower with yellow centers in a pot",
        'otter': f"a photo of an {class_original}",
        'palm_tree': f"an image of a tall coconut {class_original.replace('_', ' ')} bending in the tropical wind",
        'pear': f"a photograph of a ripe yellow {class_original} fruit with small brown spots",
        'pickup_truck': f"a picture of a blue Ford {class_original.replace('_', ' ')} with a dirty bed",
        'pine_tree': f"a photo of a tall green {class_original.replace('_', ' ')} covered in fresh snow",
        'plain': f"an image of a flat grassy {class_original} stretching to the horizon",
        'plate': f"a photograph of a white ceramic dinner {class_original} with a silver fork",
        'poppy': f"a picture of a bright red {class_original} flower with a black center",
        'possum': f"a photo of a {class_original} marsupial",
        'rabbit': f"an image of a fluffy white {class_original} with long ears eating a carrot",
        'raccoon': f"a photograph of a masked {class_original} with a striped tail digging in a trash can",
        'ray': f"a picture of a wide flat {class_original} fish gliding through crystal clear water",
        'road': f"a photo of a winding asphalt {class_original} disappearing into a distant forest",
        'rocket': f"an image of a tall white {class_original} spacecraft launching with flames and smoke",
        'rose': f"a photograph of a romantic red {class_original} flower with dew drops on petals",
        'sea': f"a picture of a vast blue {class_original} with white caps and crashing waves",
        'seal': f"a photo of a {class_original} mammal",
        'shark': f"an image of a fearsome great white {class_original} with sharp teeth swimming underwater",
        'shrew': f"a photograph of a tiny brown {class_original} with a long pointy nose",
        'skunk': f"a picture of a black and white {class_original} with a striped tail raising its tail",
        'skyscraper': f"a photo of a tall glass {class_original} building reaching into the clouds",
        'snail': f"an image of a slow brown {class_original} with a spiral shell on a leaf",
        'snake': f"a photograph of a green {class_original} coiled up on a warm rock",
        'spider': f"a picture of a black widow {class_original} with long legs in a intricate web",
        'squirrel': f"a photo of a {class_original}",
        'streetcar': f"an image of an old vintage {class_original} running on tracks down a city street",
        'sunflower': f"a photograph of a tall yellow {class_original} flower with large brown center",
        'sweet_pepper': f"a picture of a fresh red bell {class_original.replace('_', ' ')} on a cutting board",
        'table': f"a photo of a wooden dining {class_original} with four chairs around it",
        'tank': f"an image of a green military {class_original} with a long cannon on a battlefield",
        'telephone': f"a photograph of an old rotary {class_original} with a coiled cord",
        'television': f"a picture of a flat screen {class_original} mounted on a white wall",
        'tiger': f"a photo of a majestic Bengal {class_original} with orange fur and black stripes",
        'tractor': f"an image of a green farm {class_original} plowing a brown field",
        'train': f"a photograph of a old steam {class_original} locomotive with black smoke billowing",
        'trout': f"a picture of a spotted brown {class_original} fish swimming in a clear stream",
        'tulip': f"a photo of a bright red {class_original} flower in a beautiful spring garden",
        'turtle': f"an image of a green {class_original}",
        'wardrobe': f"a photograph of a tall wooden {class_original} with a mirror on the front door",
        'whale': f"a picture of a massive blue {class_original} spouting water from its blowhole",
        'willow_tree': f"a photo of a weeping {class_original.replace('_', ' ')} with long drooping branches near a pond",
        'wolf': f"an image of a gray {class_original} howling at the full moon in a forest",
        'woman': f"a photograph of an adult human female person", 
        'worm': f"a picture of a long pink {class_original} wriggling in fresh garden soil",
    }
    
    # Если класс есть в словаре, возвращаем уникальный промпт
    if class_lower in prompts:
        return prompts[class_lower]
    # Иначе базовый промпт
    else:
        return f"a photo of a {class_original}"

# Генерируем уникальные промпты для всех классов
unique_prompts = []
for class_name in class_names:
    prompt = get_unique_prompt(class_name)
    unique_prompts.append(prompt)

# Выводим примеры
print("\nПримеры уникальных промптов (с названием класса внутри):")
print("-" * 80)
for i in range(20):
    print(f"{class_names[i]:20s} -> {unique_prompts[i][:60]}...")

# Сохраняем все промпты в файл
with open('res_6/new_unique_prompts.txt', 'w') as f:
    f.write("100 УНИКАЛЬНЫХ ПРОМПТОВ ДЛЯ CIFAR-100\n")
    f.write("=" * 80 + "\n\n")
    for i, (class_name, prompt) in enumerate(zip(class_names, unique_prompts)):
        f.write(f"{i:3d}. {class_name:25s} -> {prompt}\n")

print(f"\nСохранено {len(unique_prompts)} уникальных промптов в res_6/unique_prompts.txt")

# ======================== ВЫЧИСЛЕНИЕ ЭМБЕДДИНГОВ И КЛАССИФИКАЦИЯ ========================
print("\n" + "=" * 60)
print("ВЫЧИСЛЕНИЕ ЭМБЕДДИНГОВ И ZERO-SHOT КЛАССИФИКАЦИЯ")
print("=" * 60)

# Вычисляем текстовые эмбеддинги
text_inputs = processor(text=unique_prompts, return_tensors="pt", padding=True).to(device)

with torch.no_grad():
    text_outputs = model.get_text_features(**text_inputs)
    text_features = text_outputs.pooler_output
    text_features = text_features / text_features.norm(dim=-1, keepdim=True)

print("Текстовые эмбеддинги вычислены")

# Классификация
all_preds = []
all_labels = []

model.eval()
with torch.no_grad():
    for batch_idx, (images, labels) in enumerate(test_loader):
        image_inputs = processor(images=images, return_tensors="pt", padding=True).to(device)
        image_outputs = model.get_image_features(**image_inputs)
        image_features = image_outputs.pooler_output
        image_features = image_features / image_features.norm(dim=-1, keepdim=True)
        
        similarity = image_features @ text_features.T
        preds = similarity.argmax(dim=1)
        
        all_preds.extend(preds.cpu().numpy())
        all_labels.extend(labels.cpu().numpy())
        
        if (batch_idx + 1) % 50 == 0:
            print(f"Обработано {batch_idx + 1} батчей...")

all_preds = np.array(all_preds)
all_labels = np.array(all_labels)
accuracy = np.mean(all_preds == all_labels)

# ======================== СОХРАНЕНИЕ РЕЗУЛЬТАТОВ ========================
print("\n" + "=" * 60)
print("СОХРАНЕНИЕ РЕЗУЛЬТАТОВ")
print("=" * 60)

# Общая accuracy
with open('res_6/new_accuracy.txt', 'w') as f:
    f.write("РЕЗУЛЬТАТЫ ZERO-SHOT КЛАССИФИКАЦИИ CIFAR-100\n")
    f.write("=" * 60 + "\n")
    f.write(f"Модель: openai/clip-vit-base-patch32\n")
    f.write(f"Количество классов: {len(class_names)}\n")
    f.write(f"Размер тестовой выборки: {len(test_dataset)}\n")
    f.write(f"\nAccuracy с УНИКАЛЬНЫМИ промптами: {accuracy * 100:.2f}%\n")

print(f"\nОбщая accuracy: {accuracy * 100:.2f}%")
print("Сохранено в res_6/accuracy.txt")

# Accuracy по каждому классу
class_accuracies = []
with open('res_6/new_class_accuracy.txt', 'w') as f:
    f.write("ACCURACY ПО КАЖДОМУ КЛАССУ С УНИКАЛЬНЫМИ ПРОМПТАМИ\n")
    f.write("=" * 100 + "\n\n")
    f.write(f"{'Класс':<25s} | {'Accuracy':>10s} | Промпт\n")
    f.write("-" * 100 + "\n")
    
    for i, class_name in enumerate(class_names):
        mask = all_labels == i
        if mask.sum() > 0:
            class_acc = np.mean(all_preds[mask] == all_labels[mask])
            class_accuracies.append((class_name, class_acc, unique_prompts[i]))
            f.write(f"{class_name:<25s} | {class_acc * 100:>9.1f}% | {unique_prompts[i]}\n")

# Лучшие и худшие классы
class_accuracies.sort(key=lambda x: x[1])

print("\nХудшие 10 классов:")
with open('res_6/new_best_worst_classes.txt', 'w') as f:
    f.write("ЛУЧШИЕ И ХУДШИЕ КЛАССЫ\n")
    f.write("=" * 80 + "\n\n")
    
    f.write("ХУДШИЕ 10 КЛАССОВ (самая низкая accuracy):\n")
    f.write("-" * 80 + "\n")
    for name, acc, prompt in class_accuracies[:10]:
        print(f"  {name:20s}: {acc * 100:.1f}%")
        f.write(f"{name:25s}: {acc * 100:5.1f}%\n")
        f.write(f"  Промпт: {prompt}\n\n")
    
    f.write("\nЛУЧШИЕ 10 КЛАССОВ (самая высокая accuracy):\n")
    f.write("-" * 80 + "\n")
    for name, acc, prompt in class_accuracies[-10:][::-1]:
        print(f"  {name:20s}: {acc * 100:.1f}%")
        f.write(f"{name:25s}: {acc * 100:5.1f}%\n")
        f.write(f"  Промпт: {prompt}\n\n")

