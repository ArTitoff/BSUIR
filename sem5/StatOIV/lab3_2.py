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
df = pd.read_json('/home/artem/Рабочий стол/BSUIR/StatOIV/used_car_listings.json')


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

# 5. Анализ кластеров
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

# 6. Визуализация кластеров
plt.figure(figsize=(12, 5))

# График 1: Год vs Пробег
plt.subplot(1, 2, 1)
for cluster in df['auto_cluster'].unique():
    cluster_data = df[df['auto_cluster'] == cluster]
    plt.scatter(cluster_data['year'], cluster_data['mileage'], 
               label=f'Cluster {cluster} ({cluster_names[cluster]})', alpha=0.7)
plt.xlabel('Year')
plt.ylabel('Mileage')
plt.title('Кластеры: Год выпуска vs Пробег')
plt.legend()

# График 2: Цена vs Год
plt.subplot(1, 2, 2)
for cluster in df['auto_cluster'].unique():
    cluster_data = df[df['auto_cluster'] == cluster]
    plt.scatter(cluster_data['year'], cluster_data['price'], 
               label=f'Cluster {cluster} ({cluster_names[cluster]})', alpha=0.7)
plt.xlabel('Year')
plt.ylabel('Price')
plt.title('Кластеры: Год выпуска vs Цена')
plt.legend()

plt.tight_layout()
plt.savefig('plots/clusters_visualization.png')
plt.close()

# 7. Подготовка данных для классификации
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

# 8. Разделение на train/test и масштабирование
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=52, stratify=y)

# Масштабирование числовых признаков
numerical_cols = ['year', 'mileage']
scaler = StandardScaler()
X_train[numerical_cols] = scaler.fit_transform(X_train[numerical_cols])
X_test[numerical_cols] = scaler.transform(X_test[numerical_cols])

# 9. Построение и обучение моделей
models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=11),
    'K-Nearest Neighbors': KNeighborsClassifier(n_neighbors=5),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Naive Bayes': GaussianNB()
}

# 10. Оценка качества моделей
results = []

print("\n" + "="*50)
print("РЕЗУЛЬТАТЫ КЛАССИФИКАЦИИ ПО КЛАСТЕРАМ")
print("="*50)

for name, model in models.items():
    # Обучение модели
    model.fit(X_train, y_train)
    
    # Предсказания
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test) if hasattr(model, "predict_proba") else None
    
    # Расчет метрик
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # ROC-AUC
    roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr') if y_pred_proba is not None else None
    
    results.append({
        'Model': name,
        'Accuracy': accuracy,
        'Precision': precision,
        'Recall': recall,
        'F1-Score': f1,
        'ROC-AUC': roc_auc
    })
    
    # Confusion Matrix
    plt.figure(figsize=(8, 6))
    cm = confusion_matrix(y_test, y_pred)
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                xticklabels=[f'Cluster {i}' for i in le.classes_], 
                yticklabels=[f'Cluster {i}' for i in le.classes_])
    plt.title(f'Confusion Matrix - {name}\n(Clusters: {cluster_names})')
    plt.ylabel('True Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()
    plt.savefig(f'plots/confusion_matrix_cluster_{name.lower().replace(" ", "_")}.png')
    plt.close()
    
    print(f"\n{name}:")
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    if roc_auc is not None:
        print(f"ROC-AUC: {roc_auc:.4f}")

# Создание сравнительной таблицы
results_df = pd.DataFrame(results)
print("\n" + "="*60)
print("Сравнительная таблица результатов (Кластерная классификация):")
print("="*60)
print(results_df.round(4))

# Визуализация сравнения моделей
plt.figure(figsize=(12, 8))
metrics = ['Accuracy', 'Precision', 'Recall', 'F1-Score']
x = np.arange(len(models))
width = 0.2

for i, metric in enumerate(metrics):
    values = [results_df[results_df['Model'] == model][metric].values[0] for model in models.keys()]
    plt.bar(x + i*width, values, width, label=metric, alpha=0.8)

plt.xlabel('Models')
plt.ylabel('Scores')
plt.title('Comparison of Classification Models (Cluster-based)')
plt.xticks(x + width*1.5, models.keys(), rotation=45)
plt.legend()
plt.ylim(0, 1)
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig('plots/models_comparison_clusters.png')
plt.close()

print("\nГрафики сохранены в папку 'plots'")
print(f"Интерпретация кластеров: {cluster_names}")