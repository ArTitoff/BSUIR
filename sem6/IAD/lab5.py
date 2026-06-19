import torch
import torch.nn.functional as F
from torchvision import transforms, models
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

# ==================== ЧАСТЬ A: ПОДГОТОВКА ====================

# Воспроизводимость
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Устройство
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")

# Создаем папку для результатов
Path('results_2_tur').mkdir(exist_ok=True)

# Параметры ImageNet
imagenet_mean = [0.485, 0.456, 0.406]
imagenet_std = [0.229, 0.224, 0.225]

def load_image(path, size=512):
    """Загрузка и нормализация изображения"""
    image = Image.open(path).convert('RGB')
    transform = transforms.Compose([
        transforms.Resize((size, size)),
        transforms.ToTensor(),
        transforms.Normalize(imagenet_mean, imagenet_std),
    ])
    return transform(image).unsqueeze(0).to(device)


def denormalize(tensor):
    """Обратная нормализация"""
    mean = torch.tensor(imagenet_mean).view(3, 1, 1) #форма для перемножения
    std = torch.tensor(imagenet_std).view(3, 1, 1)
    # Отключаем градиенты и перемещаем на CPU
    img = tensor.detach().clone().squeeze(0).cpu()                                                                                            #squeeze(0) - удаляет размерность batch, detach() - отсоединяет тензор от графа вычислений
    img = img * std + mean
    return img.clamp(0, 1).permute(1, 2, 0).numpy()

def save_image(tensor, path):
    """Сохранение изображения"""
    img = denormalize(tensor)
    plt.imsave(path, img)


STYLE_PATH = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/pony.jpg"    
CONTENT_PATH = "/home/artem/Рабочий стол/BSUIR/sem6/IAD/turtle.png"        
SIZE = 256                     

content_img = load_image(CONTENT_PATH, SIZE)
style_img = load_image(STYLE_PATH, SIZE)

print(f"Content image shape: {content_img.shape}")
print(f"Style image shape: {style_img.shape}")

# ==================== ЧАСТЬ B: ИЗВЛЕЧЕНИЕ ПРИЗНАКОВ ====================

# Загрузка модели VGG19
print("Загрузка VGG19...")
vgg = models.vgg19(weights=models.VGG19_Weights.DEFAULT).features.to(device)
for param in vgg.parameters():
    param.requires_grad = False
vgg.eval()
print("Модель загружена")

# Определение слоев
style_layers = {
    'conv1_1': 0,
    'conv2_1': 5,
    'conv3_1': 10,
    'conv4_1': 19,
    'conv5_1': 28,
}

content_layers = {
    'conv4_2': 21,
}

all_layers = {**style_layers, **content_layers}

def get_features(image, model, layers):
    """Извлечение признаков из указанных слоев"""
    idx_to_name = {v: k for k, v in layers.items()}
    max_idx = max(idx_to_name.keys())
    features = {}
    x = image
    
    for i, layer in enumerate(model):
        x = layer(x)
        if i in idx_to_name:
            features[idx_to_name[i]] = x
        if i == max_idx:
            break
    return features

def gram_matrix(features):
    """Вычисление матрицы Грама"""
    b, c, h, w = features.shape
    F = features.view(b, c, h * w)
    G = torch.bmm(F, F.transpose(1, 2))
    return G / ( h * w) # убрал с

def content_loss(generated, content):
    """Loss содержания"""
    return F.mse_loss(generated, content)

def style_loss(generated, style):
    """Loss стиля"""
    G_gen = gram_matrix(generated)
    G_style = gram_matrix(style)
    return F.mse_loss(G_gen, G_style)

# ==================== ЧАСТЬ C: ОПТИМИЗАЦИЯ ====================

def neural_style_transfer(content_img, style_img, alpha=1, beta=1e5, 
                          num_steps=300, init_noise=False, 
                          style_weights=None, experiment_name="result"):
    """
    Выполнение переноса стиля
    """
    
    if style_weights is None:
        style_weights = {
            'conv1_1': 1.0,
            'conv2_1': 0.8,
            'conv3_1': 0.5,
            'conv4_1': 0.3,
            'conv5_1': 0.1,
        }
    
    # Инициализация генерируемого изображения
    if init_noise:
        generated = torch.randn_like(content_img).requires_grad_(True)
        init_type = "noise"
    else:
        generated = content_img.clone().requires_grad_(True)
        init_type = "content"
    
    orig_generated = denormalize(generated)

    # Извлечение признаков content и style (один раз)
    with torch.no_grad():
        content_features = get_features(content_img, vgg, all_layers)
        style_features = get_features(style_img, vgg, all_layers)
    
    # Оптимизатор
    optimizer = torch.optim.LBFGS([generated], lr=1.0, max_iter=20) # Использует градиент + аппроксимацию кривизны (матрицу Гессе). Матрица Гессе показывает, как быстро меняется градиент:
    
    # Для зажима значений
    mean = torch.tensor(imagenet_mean, device=device).view(1, 3, 1, 1)
    std = torch.tensor(imagenet_std, device=device).view(1, 3, 1, 1)
    
    # Для сохранения прогресса
    progress_images = []
    losses_history = []
    
    def closure():
        optimizer.zero_grad()
        gen_features = get_features(generated, vgg, all_layers)
        
        # Content loss
        c_loss = content_loss(gen_features['conv4_2'], content_features['conv4_2'])
        
        # Style loss
        s_loss = 0
        for layer in style_layers:
            weight = style_weights[layer]
            s_loss += weight * style_loss(gen_features[layer], style_features[layer])
        
        total_loss = alpha * c_loss + beta * s_loss
        total_loss.backward()
        
        closure.last_losses = (total_loss.item(), c_loss.item(), s_loss.item())
        return total_loss
    
    print(f"\n--- {experiment_name} ---")
    print(f"α={alpha}, β={beta}, инициализация={init_type}")
    
    for step in range(num_steps):
        optimizer.step(closure)
        
        # Зажимаем пиксели в допустимый диапазон
        with torch.no_grad():
            generated.data = (generated.data * std + mean).clamp(0, 1)
            generated.data = (generated.data - mean) / std
        
        total_loss, c_loss, s_loss = closure.last_losses
        losses_history.append((total_loss, c_loss, s_loss))
        
        if step % 50 == 0:
            print(f"Шаг {step}: total={total_loss:.2f}, content={c_loss:.2f}, style={s_loss:.2f}")
            
            if step % 100 == 0 and step > 0:
                progress_images.append(generated.clone())
    
    # Сохранение результата
    save_image(generated, f'results_2_tur/{experiment_name}.png')
    
    # График потерь
    plt.figure(figsize=(10, 6))
    steps = range(0, num_steps)
    plt.plot(steps, [l[0] for l in losses_history], label='Total Loss')
    plt.plot(steps, [l[1] for l in losses_history], label='Content Loss')
    plt.plot(steps, [l[2] for l in losses_history], label='Style Loss')
    plt.xlabel('Step')
    plt.ylabel('Loss')
    plt.title(f'Losses - {experiment_name}')
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.savefig(f'results_2_tur/losses_{experiment_name}.png', dpi=150)
    plt.close()
    
    # Визуализация прогресса
    if progress_images:
        fig, axes = plt.subplots(1, len(progress_images) + 2, figsize=(4*(len(progress_images)+2), 4))
        axes[0].imshow(orig_generated)
        axes[0].set_title("Content", fontsize=10)
        axes[0].axis('off')
        
        axes[1].imshow(denormalize(style_img))
        axes[1].set_title("Style", fontsize=10)
        axes[1].axis('off')
        
        for i, img in enumerate(progress_images):
            axes[i+2].imshow(denormalize(img))
            axes[i+2].set_title(f"Step {(i+1)*100}", fontsize=10)
            axes[i+2].axis('off')
        
        plt.suptitle(f"Progress - {experiment_name}")
        plt.tight_layout()
        plt.savefig(f'results_2_tur/progress_{experiment_name}.png', dpi=150)
        plt.close()
    

#==================== ЗАПУСК ОСНОВНОГО ЭКСПЕРИМЕНТА ====================

print("\n" + "="*60)
print("ЗАПУСК NEURAL STYLE TRANSFER")
print("="*60)

# Основной результат
neural_style_transfer(
    content_img, style_img,
    alpha=1, beta=1e5,
    num_steps=300,
    init_noise=False,
    experiment_name="main_result"
)

print("\n" + "="*60)
print(f"РЕЗУЛЬТАТ СОХРАНЕН: results_2_tur/main_result.png")
print("="*60)

# ==================== ЭКСПЕРИМЕНТЫ ====================


# ЭКСПЕРИМЕНТ 2: Разные веса стиля
print("\n" + "="*60)
print("ЭКСПЕРИМЕНТ: Влияние β")
print("="*60)

for beta in [1e3, 1e4, 1e5, 1e6]:
    neural_style_transfer(
        content_img, style_img,
        alpha=1, beta=beta,
        num_steps=200,
        experiment_name=f"beta_{beta:.0e}"
    )

#ЭКСПЕРИМЕНТ 3: Инициализация шумом
print("\n" + "="*60)
print("ЭКСПЕРИМЕНТ: Инициализация шумом")
print("="*60)

neural_style_transfer(
    content_img, style_img,
    alpha=1, beta=1e5,
    num_steps=300,
    init_noise=True,
    experiment_name="noise_init"
)
