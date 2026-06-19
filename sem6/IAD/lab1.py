import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
import os

# Создаем папку для графиков
os.makedirs('plots', exist_ok=True)

import warnings
warnings.filterwarnings('ignore')

# Загрузка данных
df = pd.read_json('/home/artem/Рабочий стол/BSUIR/sem5/StatOIV/used_car_listings.json')


# 2. Предобработка данных
print("Размер датасета:", df.shape)
print("\nПропущенные значения:")
print(df.isnull().sum())

# Заполнение пропусков
df['trim'].fillna('Unknown', inplace=True)
df['features'].fillna('', inplace=True)
df['condition'].fillna('unknown', inplace=True)

# 3. Создание составных признаков для кластеризации
print("\nСоздание составных признаков...")

# Признак 1: Является ли марка премиальной
premium_brands = ['Audi', 'BMW', 'Mercedes-Benz', 'Tesla']
df['is_luxury_brand'] = df['make'].isin(premium_brands).astype(int)

# Признак 2: Богатая ли комплектация (много опций)
df['has_many_features'] = (df['features'].str.count(',') > 5).astype(int)

# Признак 3: Современный ли тип топлива
df['is_modern_fuel'] = df['fuel_type'].isin(['Electric', 'Hybrid', 'Plug-in Hybrid']).astype(int)

print(f"Премиальные марки: {df['is_luxury_brand'].sum()}")
print(f"Богатая комплектация: {df['has_many_features'].sum()}")
print(f"Современное топливо: {df['is_modern_fuel'].sum()}")

# 4. Кластеризация K-means для автоматического определения классов
print("\nВыполнение кластеризации K-means...")

# Признаки для кластеризации
cluster_features = ['year', 'mileage', 'is_luxury_brand', 'has_many_features', 'is_modern_fuel']

# Масштабируем признаки для кластеризации
scaler_cluster = StandardScaler()
scaled_features = scaler_cluster.fit_transform(df[cluster_features])

# Кластеризация
kmeans = KMeans(n_clusters=3, random_state=52, n_init=10)
df['auto_cluster'] = kmeans.fit_predict(scaled_features)

print("Кластеризация завершена!")


print("\nАнализ кластеров:")
cluster_analysis = df.groupby('auto_cluster').agg({
    'year': 'mean',
    'mileage': 'mean',
    'is_luxury_brand': 'mean',
    'has_many_features': 'mean', 
    'is_modern_fuel': 'mean',
    'price': 'mean',
    'make': lambda x: x.value_counts().index[0]  # самая частая марка
}).round(2)

cluster_analysis.columns = ['avg_year', 'avg_mileage', 'luxury_ratio', 'features_ratio', 
                           'modern_fuel_ratio', 'avg_price', 'most_common_make']

print(cluster_analysis)

# интерпретация кластеров
cluster_names = {}
for cluster in sorted(df['auto_cluster'].unique()):
    cluster_data = cluster_analysis.loc[cluster]
    
    if cluster_data['luxury_ratio'] > 0.5:  # Премиальные марки
        cluster_names[cluster] = 'premium'
    elif cluster_data['avg_year'] < 2015 and cluster_data['avg_mileage'] > 150000:
        cluster_names[cluster] = 'budget_used'
    else:
        cluster_names[cluster] = 'standard'

df['cluster_name'] = df['auto_cluster'].map(cluster_names)
print(f"\nИнтерпретация кластеров: {cluster_names}")


print("\nПодготовка данных для классификации...")

# Кодирование категориальных переменных
categorical_cols = ['make', 'model', 'body_type', 'fuel_type', 'transmission', 'seller_type']
df_encoded = pd.get_dummies(df, columns=categorical_cols, drop_first=True)

# Создание бинарных признаков из features
feature_keywords = ['Alloy Wheels', 'Android Auto', 'Apple CarPlay', 'Backup Camera', 
                   'Blind Spot Monitor', 'Bluetooth', 'Fog Lights', 'Heated Seats',
                   'Keyless Entry', 'LED Headlights', 'Leather Seats', 'Navigation',
                   'Panoramic Roof', 'Parking Sensors', 'Push Button Start', 'Sunroof',
                   'Ventilated Seats', 'Wireless Charging', 'Lane Keep Assist', 'Adaptive Cruise Control']

for feature in feature_keywords:
    df_encoded[f'has_{feature.lower().replace(" ", "_")}'] = df_encoded['features'].str.contains(feature, case=False, na=False).astype(int)

# Целевая переменная - кластеры
le = LabelEncoder()
df_encoded['target'] = le.fit_transform(df_encoded['auto_cluster'])

# Признаки для модели (ИСКЛЮЧАЕМ цену и кластерные признаки чтобы избежать утечки данных)
feature_columns = [col for col in df_encoded.columns if col not in 
                  ['listing_id', 'vin', 'location', 'features', 'condition', 
                   'auto_cluster', 'cluster_name', 'target', 'trim', 'price',
                   'is_luxury_brand', 'has_many_features', 'is_modern_fuel']]  # Исключаем составные признаки

X = df_encoded[feature_columns]
y = df_encoded['target']

print(f"Количество признаков для классификации: {X.shape[1]}")
print(f"Распределение классов: {dict(zip(le.classes_, np.bincount(y)))}")


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=52, stratify=y)

# Масштабирование числовых признаков
numerical_cols = ['year', 'mileage']
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

print(y_train)


import torch

# Сбрасываем индексы и заполняем пропуски
X_train = X_train.reset_index(drop=True).fillna(0)
X_test = X_test.reset_index(drop=True).fillna(0)


X_train = X_train.astype('float32')
X_test = X_test.astype('float32')

X_train_tensor = torch.FloatTensor(X_train.values)
y_train_tensor = torch.LongTensor(y_train.values)
X_test_tensor = torch.FloatTensor(X_test.values)
y_test_tensor = torch.LongTensor(y_test.values)

print(f"X_train_tensor: {X_train_tensor.shape}")
print(f"y_train_tensor: {y_train_tensor.shape}")




import torch.nn as nn
import torch.optim as optim


print("="*50)
print("ОБУЧЕНИЕ НЕЙРОННОЙ СЕТИ")
print("="*50)


class DeepNeuralNetwork(nn.Module):
    def __init__(self, input_size, hidden_size1 , num_classes):
        super(DeepNeuralNetwork, self).__init__()
        
        self.fc1 = nn.Linear(input_size, hidden_size1)
        self.relu1 = nn.ReLU()
        
 

        self.fc2 = nn.Linear(hidden_size1, num_classes)
    
    def forward(self, x):

        x = self.fc1(x)
        x = self.relu1(x)

        
    

        x = self.fc2(x)
        return x

input_size = X_train_tensor.shape[1]    
hidden_size1 = 64                          
hidden_size2 = 32                            
hidden_size3 = 16
hidden_size4 = 8
num_classes = len(torch.unique(y_train_tensor))  # 3 класса



model = DeepNeuralNetwork(input_size, hidden_size1,  num_classes)


device = torch.device("cpu")
model = model.to(device)
X_train_tensor = X_train_tensor.to(device)
X_test_tensor = X_test_tensor.to(device)
y_train_tensor = y_train_tensor.to(device)
y_test_tensor = y_test_tensor.to(device)

print(f"Устройство: {device}")



loss_func = nn.CrossEntropyLoss()  
optimizer = optim.Adam(model.parameters(), lr=0.001) 

print(f"\nФункция потерь: CrossEntropyLoss")
print(f"Оптимизатор: Adam (lr=0.001)")


def calculate_accuracy(model, X, y):
    """Вычисляет точность модели на данных X, y"""
    model.eval()  # режим оценки (не тренировки)
    with torch.no_grad():  # не считаем градиенты
        outputs = model(X)
        _, predicted = torch.max(outputs, 1)  # получаем предсказанные классы
        correct = (predicted == y).sum().item()  # количество правильных
        total = y.size(0)  # всего объектов
        accuracy = correct / total
    model.train()  # возвращаемся в режим обучения
    return accuracy



num_epochs = 220 
print(f"\nНачинаем обучение на {num_epochs} эпох...")
print("-"*50)


train_losses = []
train_accuracies = []
test_losses = []
test_accuracies = []

for epoch in range(num_epochs):
    model.train()  

    optimizer.zero_grad()
    
    outputs = model(X_train_tensor)
    
    loss = loss_func(outputs, y_train_tensor)

    loss.backward()
    
    # Обновляем веса
    optimizer.step()
    

    train_acc = calculate_accuracy(model, X_train_tensor, y_train_tensor)
    

    model.eval()
    with torch.no_grad():
        test_outputs = model(X_test_tensor)
        test_loss = loss_func(test_outputs, y_test_tensor)
        test_acc = calculate_accuracy(model, X_test_tensor, y_test_tensor)
    
    # Сохраняем метрики
    train_losses.append(loss.item())
    train_accuracies.append(train_acc)
    test_losses.append(test_loss.item())
    test_accuracies.append(test_acc)
    
    print(f"Эпоха [{epoch+1}/{num_epochs}]")
    print(f"  Train Loss: {loss.item():.4f}, Train Acc: {train_acc:.4f}")
    print(f"  Test Loss: {test_loss.item():.4f}, Test Acc: {test_acc:.4f}")

print("-"*50)
print("Обучение завершено!")
print(f"Финальная точность на train: {train_accuracies[-1]:.4f}")
print(f"Финальная точность на test: {test_accuracies[-1]:.4f}")

from sklearn.metrics import f1_score
import numpy as np
model.eval()

# Получаем предсказания для тестовой выборки
with torch.no_grad():
    outputs = model(X_test_tensor)
    _, y_pred = torch.max(outputs, 1)  # получаем предсказанные классы

# Преобразуем тензоры в numpy (если они на GPU, сначала .cpu())
y_true = y_test_tensor.cpu().numpy()
y_pred = y_pred.cpu().numpy()


f1_weighted = f1_score(y_true, y_pred, average='weighted')  # взвешенный по размеру классов

print(f"F1-score (weighted): {f1_weighted:.4f}")




# Создаем фигуру с двумя подграфиками
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))

# График 1: Функция потерь (Loss)
ax1.plot(range(1, num_epochs+1), train_losses, label='Train Loss', color='blue')
ax1.plot(range(1, num_epochs+1), test_losses, label='Test Loss', color='red', linestyle='--')
ax1.set_xlabel('Эпоха')
ax1.set_ylabel('Loss')
ax1.set_title('Функция потерь')
ax1.legend()
ax1.grid(True, alpha=0.3)

# График 2: Точность (Accuracy)
ax2.plot(range(1, num_epochs+1), train_accuracies, label='Train Accuracy', color='blue')
ax2.plot(range(1, num_epochs+1), test_accuracies, label='Test Accuracy', color='red', linestyle='--')
ax2.set_xlabel('Эпоха')
ax2.set_ylabel('Accuracy')
ax2.set_title('Точность')
ax2.legend()
ax2.grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plots/training_history.png', dpi=150, bbox_inches='tight')
plt.show()

print("Графики сохранены в папку 'plots'")




from sklearn.linear_model import LogisticRegression

# Построение и обучение LogisticRegression
logistic_model = {
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=10)
}
results = []


for name, model in logistic_model.items():
    # Обучение модели
    model.fit(X_train, y_train)
    
    # Предсказания
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
    
    # Расчет метрик
    accuracy = accuracy_score(y_test, y_pred)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    

    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'F1-Score': f1
    })

results.append({
    'Model': "NN",
    'Accuracy': test_accuracies[-1],
    'F1-Score': f1_weighted
})  

# Создание сравнительной таблицы
results_df = pd.DataFrame(results)
print("\n" + "="*60)
print("Сравнительная таблица результатов:")
print("="*60)
print(results_df.round(4))