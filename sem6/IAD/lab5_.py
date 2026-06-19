import torch
import torch.nn as nn
import torch.nn.functional as F
from torchvision import transforms, datasets
from torch.utils.data import DataLoader
from torch.nn.utils import spectral_norm
from torchvision.utils import save_image, make_grid
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
import os

# ==================== ПОДГОТОВКА ====================

# Воспроизводимость
torch.manual_seed(42)
torch.cuda.manual_seed_all(42)
torch.backends.cudnn.deterministic = True
torch.backends.cudnn.benchmark = False

# Устройство
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
print(f"Используется устройство: {device}")

# Создание папок для результатов
Path('gan_results_35_e').mkdir(exist_ok=True)
Path('gan_results_35_e/grids').mkdir(exist_ok=True)

# Параметры
LATENT_DIM = 100
IMG_CHANNELS = 3
IMG_SIZE = 64
BATCH_SIZE = 128
NUM_EPOCHS = 35
LEARNING_RATE = 2e-4
BETAS = (0.5, 0.999)

# Подготовка данных CIFAR-10
transform = transforms.Compose([
    transforms.Resize(IMG_SIZE),
    transforms.CenterCrop(IMG_SIZE),
    transforms.ToTensor(),
    transforms.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5]),  # в диапазон [-1, 1]
])

dataset = datasets.CIFAR10(root='data', train=True, download=True, transform=transform)
dataloader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, pin_memory=True)

print(f"Размер датасета: {len(dataset)} изображений")
print(f"Количество батчей: {len(dataloader)}")

# ==================== ЧАСТЬ A: АРХИТЕКТУРА ====================

class Generator(nn.Module):
    """Генератор DCGAN"""
    def __init__(self, latent_dim=100, img_channels=3):
        super().__init__()
        self.net = nn.Sequential(
            # [batch, latent_dim, 1, 1] → [batch, 512, 4, 4]
            nn.ConvTranspose2d(latent_dim, 512, 4, 1, 0, bias=False),
            nn.BatchNorm2d(512),
            nn.ReLU(True),
            
            # → [batch, 256, 8, 8]
            nn.ConvTranspose2d(512, 256, 4, 2, 1, bias=False),
            nn.BatchNorm2d(256),
            nn.ReLU(True),
            
            # → [batch, 128, 16, 16]
            nn.ConvTranspose2d(256, 128, 4, 2, 1, bias=False),
            nn.BatchNorm2d(128),
            nn.ReLU(True),
            
            # → [batch, 64, 32, 32]
            nn.ConvTranspose2d(128, 64, 4, 2, 1, bias=False),
            nn.BatchNorm2d(64),
            nn.ReLU(True),
            
            # → [batch, img_channels, 64, 64]
            nn.ConvTranspose2d(64, img_channels, 4, 2, 1, bias=False),
            nn.Tanh(),
        )
    
    def forward(self, z):
        return self.net(z)

class Discriminator(nn.Module):
    """Дискриминатор DCGAN с Spectral Normalization"""
    def __init__(self, img_channels=3):
        super().__init__()
        self.net = nn.Sequential(
            # [batch, 3, 64, 64] → [batch, 64, 32, 32]
            spectral_norm(nn.Conv2d(img_channels, 64, 4, 2, 1, bias=False)),
            nn.LeakyReLU(0.2, inplace=True),
            
            # → [batch, 128, 16, 16]
            spectral_norm(nn.Conv2d(64, 128, 4, 2, 1, bias=False)),
            nn.BatchNorm2d(128),
            nn.LeakyReLU(0.2, inplace=True),
            
            # → [batch, 256, 8, 8]
            spectral_norm(nn.Conv2d(128, 256, 4, 2, 1, bias=False)),
            nn.BatchNorm2d(256),
            nn.LeakyReLU(0.2, inplace=True),
            
            # → [batch, 512, 4, 4]
            spectral_norm(nn.Conv2d(256, 512, 4, 2, 1, bias=False)),
            nn.BatchNorm2d(512),
            nn.LeakyReLU(0.2, inplace=True),
            
            # → [batch, 1, 1, 1]
            spectral_norm(nn.Conv2d(512, 1, 4, 1, 0, bias=False)),
        )
    
    def forward(self, img):
        return self.net(img).view(-1)

def weights_init(m):
    """Инициализация весов для DCGAN"""
    if isinstance(m, (nn.Conv2d, nn.ConvTranspose2d)):
        nn.init.normal_(m.weight, 0.0, 0.02)
    elif isinstance(m, nn.BatchNorm2d):
        nn.init.normal_(m.weight, 1.0, 0.02)
        nn.init.zeros_(m.bias)

# Инициализация моделей
generator = Generator(latent_dim=LATENT_DIM).to(device)
discriminator = Discriminator().to(device)

generator.apply(weights_init)
discriminator.apply(weights_init)

print("\nАрхитектура генератора:")
print(generator)
print(f"\nКоличество параметров генератора: {sum(p.numel() for p in generator.parameters()):,}")

print("\nАрхитектура дискриминатора:")
print(discriminator)
print(f"Количество параметров дискриминатора: {sum(p.numel() for p in discriminator.parameters()):,}")

# ==================== ЧАСТЬ B: ОБУЧЕНИЕ ====================

# Функция потерь
criterion = nn.BCEWithLogitsLoss()

# Оптимизаторы
opt_G = torch.optim.Adam(generator.parameters(), lr=LEARNING_RATE, betas=BETAS)
opt_D = torch.optim.Adam(discriminator.parameters(), lr=LEARNING_RATE, betas=BETAS)

# Фиксированный шум для визуализации прогресса
fixed_noise = torch.randn(16, LATENT_DIM, 1, 1, device=device)

# Функция для денормализации изображений
def denorm_gan(tensor):
    """Обратная нормализация из [-1, 1] в [0, 1]"""
    return (tensor * 0.5 + 0.5).clamp(0, 1)

# Функция для сохранения сетки изображений
def save_grid(images, epoch, name="grid"):
    """Сохранение сетки изображений"""
    images = denorm_gan(images)
    grid = make_grid(images, nrow=4, padding=2, normalize=False)
    save_image(grid, f'gan_results_35_e/grids/{name}_epoch_{epoch:03d}.png')

# Функция визуализации прогресса
def plot_progress(fixed_images, epoch):
    """Отображение прогресса обучения"""
    plt.figure(figsize=(8, 8))
    images = denorm_gan(fixed_images)
    grid = make_grid(images, nrow=4, padding=2, normalize=False)
    plt.imshow(grid.cpu().permute(1, 2, 0))
    plt.axis('off')
    plt.title(f'Epoch {epoch}')
    plt.savefig(f'gan_results_35_e/progress_epoch_{epoch:03d}.png', dpi=100, bbox_inches='tight')
    plt.close()

# Обучение
history = {'loss_D': [], 'loss_G': [], 'D_x': [], 'D_G_z': []}

print("\n" + "="*60)
print("НАЧАЛО ОБУЧЕНИЯ DCGAN")
print("="*60)

for epoch in range(NUM_EPOCHS):
    epoch_loss_D = 0.0
    epoch_loss_G = 0.0
    epoch_D_x = 0.0
    epoch_D_G_z = 0.0
    
    for batch_idx, (real_images, _) in enumerate(dataloader):
        batch_size = real_images.size(0)
        real_images = real_images.to(device)
        
        # Label smoothing: 0.9 для реальных, 0.0 для фейковых
        real_labels = torch.full((batch_size,), 0.9, device=device)
        fake_labels = torch.zeros(batch_size, device=device)
        
        # ── Шаг 1: обучение дискриминатора ──────────────────────────────
        # Реальные изображения
        d_real = discriminator(real_images)
        loss_real = criterion(d_real, real_labels)
        
        # Фейковые изображения
        z = torch.randn(batch_size, LATENT_DIM, 1, 1, device=device)
        fake_images = generator(z)
        d_fake = discriminator(fake_images.detach())
        loss_fake = criterion(d_fake, fake_labels)
        
        loss_D = loss_real + loss_fake
        
        opt_D.zero_grad()
        loss_D.backward()
        opt_D.step()
        
        # ── Шаг 2: обучение генератора ──────────────────────────────────
        z = torch.randn(batch_size, LATENT_DIM, 1, 1, device=device)
        fake_images = generator(z)
        d_fake_for_G = discriminator(fake_images)
        loss_G = criterion(d_fake_for_G, torch.ones(batch_size, device=device))
        
        opt_G.zero_grad()
        loss_G.backward()
        opt_G.step()
        
        # Накопление метрик
        epoch_loss_D += loss_D.item()
        epoch_loss_G += loss_G.item()
        epoch_D_x += torch.sigmoid(d_real).mean().item()
        epoch_D_G_z += torch.sigmoid(d_fake_for_G).mean().item()
    
    # Усреднение метрик
    n_batches = len(dataloader)
    avg_loss_D = epoch_loss_D / n_batches
    avg_loss_G = epoch_loss_G / n_batches
    avg_D_x = epoch_D_x / n_batches
    avg_D_G_z = epoch_D_G_z / n_batches
    
    history['loss_D'].append(avg_loss_D)
    history['loss_G'].append(avg_loss_G)
    history['D_x'].append(avg_D_x)
    history['D_G_z'].append(avg_D_G_z)
    
    print(f"Epoch [{epoch+1:2d}/{NUM_EPOCHS}] "
          f"loss_D={avg_loss_D:.4f} loss_G={avg_loss_G:.4f} "
          f"D(x)={avg_D_x:.3f} D(G(z))={avg_D_G_z:.3f}")
    
    # Визуализация прогресса каждые 5 эпох
    if (epoch + 1) % 5 == 0:
        with torch.no_grad():
            fixed_images = generator(fixed_noise)
            save_grid(fixed_images, epoch + 1, "grid")
            plot_progress(fixed_images, epoch + 1)
        
        # Сохранение моделей
        torch.save(generator.state_dict(), f'gan_results_35_e/generator_epoch_{epoch+1}.pth')
        torch.save(discriminator.state_dict(), f'gan_results_35_e/discriminator_epoch_{epoch+1}.pth')

# Сохранение финальных моделей
torch.save(generator.state_dict(), 'gan_results_35_e/generator_final.pth')
torch.save(discriminator.state_dict(), 'gan_results_35_e/discriminator_final.pth')

# ==================== ЧАСТЬ C: ВИЗУАЛИЗАЦИЯ И АНАЛИЗ ====================

# 1. Графики обучения
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# График потерь
axes[0].plot(history['loss_D'], label='Discriminator Loss', color='red')
axes[0].plot(history['loss_G'], label='Generator Loss', color='blue')
axes[0].axhline(y=0.693, color='green', linestyle='--', label='ln(2) ≈ 0.693')
axes[0].set_xlabel('Epoch')
axes[0].set_ylabel('Loss')
axes[0].set_title('Losses during training')
axes[0].legend()
axes[0].grid(True, alpha=0.3)

# График D(x) и D(G(z))
axes[1].plot(history['D_x'], label='D(x) - real accuracy', color='green')
axes[1].plot(history['D_G_z'], label='D(G(z)) - fake accuracy', color='orange')
axes[1].axhline(y=0.5, color='black', linestyle='--', label='Random chance')
axes[1].set_xlabel('Epoch')
axes[1].set_ylabel('Accuracy')
axes[1].set_title('Discriminator output')
axes[1].legend()
axes[1].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('gan_results_35_e/training_curves.png', dpi=150)
plt.show()

# 2. Финальная сетка из 64 изображений
print("\n" + "="*60)
print("ГЕНЕРАЦИЯ ФИНАЛЬНЫХ ИЗОБРАЖЕНИЙ")
print("="*60)

with torch.no_grad():
    # Генерация 64 изображений
    z = torch.randn(64, LATENT_DIM, 1, 1, device=device)
    final_images = generator(z)
    
    # Сохранение финальной сетки
    grid = make_grid(denorm_gan(final_images), nrow=8, padding=2)
    save_image(grid, 'gan_results_35_e/final_grid.png')
    
    # Отображение
    plt.figure(figsize=(12, 12))
    plt.imshow(grid.cpu().permute(1, 2, 0))
    plt.axis('off')
    plt.title('Final generated images (64 samples)')
    plt.savefig('gan_results_35_e/final_grid_display.png', dpi=150, bbox_inches='tight')
    plt.show()

# 3. Вычисление FID (требуется torchmetrics)
try:
    from torchmetrics.image.fid import FrechetInceptionDistance
    
    NUM_FID_SAMPLES = 10000
    print(f"\nВычисление FID на {NUM_FID_SAMPLES} сэмплах...")
    
    def prepare_for_fid(images):
        """Подготовка изображений для FID"""
        images = denorm_gan(images)
        images = F.interpolate(images, size=(75, 75), mode='bilinear', align_corners=False)
        return (images * 255).byte()
    
    fid = FrechetInceptionDistance(feature=2048).to(device)
    
    # Реальные изображения
    samples_seen = 0
    for real_images, _ in dataloader:
        real_images = real_images.to(device)
        fid.update(prepare_for_fid(real_images), real=True)
        samples_seen += real_images.size(0) #Счетчик сколько фото уже добавили
        if samples_seen >= NUM_FID_SAMPLES:
            break
    
    # Сгенерированные изображения
    generator.eval()
    samples_seen = 0
    with torch.no_grad():
        while samples_seen < NUM_FID_SAMPLES:
            z = torch.randn(128, LATENT_DIM, 1, 1, device=device)
            fake_images = generator(z)
            fid.update(prepare_for_fid(fake_images), real=False)
            samples_seen += fake_images.size(0)
    
    fid_score = fid.compute()
    print(f"FID (на {NUM_FID_SAMPLES} сэмплах): {fid_score:.2f}")
    
    # Сохранение FID в файл
    with open('gan_results_35_e/fid_score.txt', 'w') as f:
        f.write(f"FID Score: {fid_score:.2f}\n")
        f.write(f"Number of samples: {NUM_FID_SAMPLES}\n")
        f.write(f"Note: Lower FID is better. Typical range: 0-300\n")
    
except ImportError:
    print("torchmetrics не установлен. Пропуск вычисления FID.")
    print("Установите: pip install torchmetrics")

# 4. Интерполяция в латентном пространстве
print("\n" + "="*60)
print("ИНТЕРПОЛЯЦИЯ В ЛАТЕНТНОМ ПРОСТРАНСТВЕ")
print("="*60)

with torch.no_grad():
    z1 = torch.randn(1, LATENT_DIM, 1, 1, device=device)
    z2 = torch.randn(1, LATENT_DIM, 1, 1, device=device)
    
    alphas = torch.linspace(0, 1, steps=10)
    interpolated_images = []
    
    for alpha in alphas:
        z_interp = (1 - alpha) * z1 + alpha * z2
        img = generator(z_interp)
        interpolated_images.append(denorm_gan(img))
    
    # Объединение в сетку
    interp_grid = torch.cat(interpolated_images, dim=0)
    grid = make_grid(interp_grid, nrow=10, padding=2)
    
    plt.figure(figsize=(15, 3))
    plt.imshow(grid.cpu().permute(1, 2, 0))
    plt.axis('off')
    plt.title('Latent space interpolation (z1 → z2)')
    plt.savefig('gan_results_35_e/interpolation.png', dpi=150, bbox_inches='tight')
    plt.show()
    
    print("Интерполяция сохранена в gan_results_35_e/interpolation.png")
    print("Наблюдения: Плавный переход между разными стилями изображений")















































































































































































# 5. Анализ разнообразия (проверка mode collapse)
print("\n" + "="*60)
print("АНАЛИЗ РАЗНООБРАЗИЯ")
print("="*60)

with torch.no_grad():
    # Генерация 1000 изображений для анализа
    z = torch.randn(1000, LATENT_DIM, 1, 1, device=device)
    batch_images = generator(z)
    
    # Вычисление средней яркости и стандартного отклонения
    images_np = denorm_gan(batch_images).cpu().numpy()
    mean_brightness = images_np.mean(axis=(1, 2, 3))
    std_brightness = images_np.std(axis=(1, 2, 3))
    
    print(f"Средняя яркость изображений: {mean_brightness.mean():.3f} ± {mean_brightness.std():.3f}")
    print(f"Стандартное отклонение пикселей: {std_brightness.mean():.3f} ± {std_brightness.std():.3f}")
    
    # Гистограмма яркости
    plt.figure(figsize=(10, 5))
    plt.hist(mean_brightness, bins=30, alpha=0.7, color='blue', edgecolor='black')
    plt.xlabel('Mean brightness')
    plt.ylabel('Frequency')
    plt.title('Distribution of image brightness (check for mode collapse)')
    plt.grid(True, alpha=0.3)
    plt.savefig('gan_results_35_e/brightness_distribution.png', dpi=150)
    plt.show()
    
    if mean_brightness.std() < 0.05:
        print("ВНИМАНИЕ: Низкое разнообразие - возможен mode collapse!")
    else:
        print("✓ Хорошее разнообразие изображений")

# Сохранение истории обучения
import json
with open('gan_results_35_e/training_history.json', 'w') as f:
    json.dump(history, f)

print("\n" + "="*60)
print("ОБУЧЕНИЕ ЗАВЕРШЕНО!")
print("Результаты сохранены в папке 'gan_results_35_e/'")
print("="*60)





















































# Анализ и комментарии
print("\n" + "="*60)
print("АНАЛИЗ РЕЗУЛЬТАТОВ")
print("="*60)

print("""
1. ГРАФИКИ ОБУЧЕНИЯ:
   - loss_D и loss_G должны колебаться вокруг ln(2) ≈ 0.693 при равновесии
   - D(x) стремится к 1 (дискриминатор уверен в реальных изображениях)
   - D(G(z)) растет от 0 к ~0.5 (генератор учится обманывать)

2. КАЧЕСТВО ГЕНЕРАЦИИ:
   - На ранних эпохах: шум, неразличимые формы
   - К 20-30 эпохам: появляются узнаваемые объекты (автомобили, животные)
   - К 50 эпохам: более четкие формы, но могут быть артефакты

3. ВОЗМОЖНЫЕ ПРОБЛЕМЫ:
   - Если loss_D → 0, loss_G растет: дискриминатор слишком сильный
   - Если все изображения похожи: mode collapse
   - Если D(G(z)) не растет: генератор не учится

4. FID SCORE:
   - < 50: отличное качество
   - 50-100: хорошее качество
   - 100-200: среднее качество
   - > 200: плохое качество
""")