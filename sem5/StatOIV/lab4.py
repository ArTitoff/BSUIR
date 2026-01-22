import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from sklearn.decomposition import PCA
from sklearn.metrics import silhouette_score, davies_bouldin_score, calinski_harabasz_score
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
import warnings
warnings.filterwarnings('ignore')

# Создаем папку для графиков
import os
os.makedirs('plots', exist_ok=True)


df = pd.read_csv('/home/artem/Рабочий стол/BSUIR/StatOIV/real_drug_dataset.csv')
print(f"Размер датасета: {df.shape}")

#  ПРЕДОБРАБОТКА
print(f"Пропущенные значения: {df.isnull().sum().sum()}")

features = ['Age', 'Dosage_mg', 'Treatment_Duration_days', 'Improvement_Score', 
            'Gender', 'Condition', 'Drug_Name']
X = df[features]
true_labels = df['Condition'].copy()

preprocessor = ColumnTransformer([
    ('num', StandardScaler(), ['Age', 'Dosage_mg', 'Treatment_Duration_days', 'Improvement_Score']),
    ('cat', OneHotEncoder(drop='first', sparse_output=False), ['Gender', 'Condition', 'Drug_Name'])
])

X_processed = preprocessor.fit_transform(X)
print(f"Данные после препроцессинга: {X_processed.shape}")

# ОПТИМИЗАЦИЯ KMEANS
inertias = []
silhouette_scores = []
K_range = range(2, 11)  

for k in K_range:
    kmeans = KMeans(n_clusters=k, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_processed)
    inertias.append(kmeans.inertia_)
    silhouette_scores.append(silhouette_score(X_processed, labels))

# График локтя
plt.figure(figsize=(10, 4))
plt.plot(K_range, inertias, 'bo-')
plt.xlabel('Количество кластеров')
plt.ylabel('Inertia')
plt.title('Метод локтя для KMeans')
plt.grid(True, alpha=0.3)
plt.savefig('plots/kmeans_elbow.png', dpi=300)
plt.close()

# График силуэта - используем тот же K_range
plt.figure(figsize=(10, 4))
plt.plot(K_range, silhouette_scores, 'ro-') 
plt.xlabel('Количество кластеров')
plt.ylabel('Silhouette Score')
plt.title('Силуэтный анализ для KMeans')
plt.grid(True, alpha=0.3)
plt.savefig('plots/kmeans_silhouette.png', dpi=300)
plt.close()

optimal_k = K_range[np.argmax(silhouette_scores)]
print(f"\nОптимальное k для KMeans: {optimal_k}")

# ОБУЧЕНИЕ МОДЕЛЕЙ
# KMeans
kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
kmeans_labels = kmeans.fit_predict(X_processed)

# Agglomerative
agg = AgglomerativeClustering(n_clusters=3, linkage='ward')
agg_labels = agg.fit_predict(X_processed)

# DBSCAN
dbscan = DBSCAN(eps=1.7, min_samples=5)
dbscan_labels = dbscan.fit_predict(X_processed)

#ОЦЕНКА КАЧЕСТВА
def evaluate_model(X, labels, true_labels, name):
    results = {'Algorithm': name}
    n_clusters = len(set(labels)) - (1 if -1 in labels else 0)
    results['n_clusters'] = n_clusters
    
    mask = labels != -1 if -1 in labels else slice(None)
    X_filt, labels_filt = X[mask], labels[mask]
    
    if len(np.unique(labels_filt)) > 1:
        results['Silhouette'] = silhouette_score(X_filt, labels_filt)
        results['Davies-Bouldin'] = davies_bouldin_score(X_filt, labels_filt)
        results['Calinski-Harabasz'] = calinski_harabasz_score(X_filt, labels_filt)
    else:
        results['Silhouette'] = 0
        results['Davies-Bouldin'] = float('inf')
        results['Calinski-Harabasz'] = 0
    
    results['n_outliers'] = np.sum(labels == -1)
    results['outliers_%'] = results['n_outliers'] / len(labels) * 100
    results['ARI'] = adjusted_rand_score(true_labels, labels)
    results['NMI'] = normalized_mutual_info_score(true_labels, labels)
    
    return results

results = [
    evaluate_model(X_processed, kmeans_labels, true_labels, f"KMeans (k={optimal_k})"),
    evaluate_model(X_processed, agg_labels, true_labels, "Agglomerative (k=3)"),
    evaluate_model(X_processed, dbscan_labels, true_labels, "DBSCAN (eps=1.7)")
]

results_df = pd.DataFrame(results)
print("\nРЕЗУЛЬТАТЫ КЛАСТЕРИЗАЦИИ:")
print("="*50)
print(results_df.to_string(index=False))
results_df.to_csv('plots/clustering_results.csv', index=False)

# ВИЗУАЛИЗАЦИЯ
pca = PCA(n_components=2, random_state=42)
X_pca = pca.fit_transform(X_processed)

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
models = [
    (f'KMeans\n(k={optimal_k})', kmeans_labels),
    ('Agglomerative\n(k=3)', agg_labels),
    ('DBSCAN\n(eps=1.7)', dbscan_labels)
]

for i, (name, labels) in enumerate(models):
    scatter = axes[i].scatter(X_pca[:, 0], X_pca[:, 1], c=labels, 
                             cmap='tab20', alpha=0.7, s=30)
    axes[i].set_title(name)
    axes[i].set_xlabel(f'PC1 ({pca.explained_variance_ratio_[0]:.1%})')
    if i == 0:
        axes[i].set_ylabel(f'PC2 ({pca.explained_variance_ratio_[1]:.1%})')
    plt.colorbar(scatter, ax=axes[i])

plt.tight_layout()
plt.savefig('plots/clustering_pca.png', dpi=300)
plt.close()

# Гистограммы размеров кластеров
fig, axes = plt.subplots(1, 3, figsize=(18, 5))
for i, (name, labels) in enumerate(models):
    unique, counts = np.unique(labels, return_counts=True)
    axes[i].bar(range(len(unique)), counts)
    axes[i].set_title(f'Размеры кластеров: {name}')
    axes[i].set_xlabel('Кластер')
    axes[i].set_ylabel('Количество точек')
    axes[i].grid(True, alpha=0.3, axis='y')
    
    for j, count in enumerate(counts):
        axes[i].text(j, count + 5, str(count), ha='center')

plt.tight_layout()
plt.savefig('plots/cluster_sizes.png', dpi=300)
plt.close()

# Boxplot для лучшего алгоритма
best_idx = results_df['Silhouette'].idxmax()
best_algo = results_df.loc[best_idx, 'Algorithm']
best_labels = [kmeans_labels, agg_labels, dbscan_labels][best_idx]
df['Best_Cluster'] = best_labels

numeric_cols = ['Age', 'Dosage_mg', 'Treatment_Duration_days', 'Improvement_Score']
fig, axes = plt.subplots(2, 2, figsize=(12, 10))
axes = axes.flatten()

for i, col in enumerate(numeric_cols):
    plot_data = []
    cluster_ids = []
    
    for cluster in sorted(np.unique(best_labels)):
        if cluster != -1:
            data = df[df['Best_Cluster'] == cluster][col]
            if len(data) > 0:
                plot_data.append(data)
                cluster_ids.append(f'Cluster {cluster}')
    
    if plot_data:
        bp = axes[i].boxplot(plot_data, labels=cluster_ids, patch_artist=True)
        colors = plt.cm.Set3(np.linspace(0, 1, len(plot_data)))
        for patch, color in zip(bp['boxes'], colors):
            patch.set_facecolor(color)
        
        axes[i].set_title(f'Распределение {col} по кластерам')
        axes[i].set_ylabel(col)
        axes[i].tick_params(axis='x', rotation=45)
        axes[i].grid(True, alpha=0.3)

plt.tight_layout()
plt.savefig('plots/boxplots.png', dpi=300)
plt.close()

# АНАЛИЗ РЕЗУЛЬТАТОВ
print(f"\nЛучший алгоритм по Silhouette: {best_algo}")
print(f"Silhouette Score: {results_df.loc[best_idx, 'Silhouette']:.3f}")
print(f"Количество кластеров: {results_df.loc[best_idx, 'n_clusters']}")
print(f"Выбросов: {results_df.loc[best_idx, 'n_outliers']} ({results_df.loc[best_idx, 'outliers_%']:.1f}%)")

# Анализ кластеров
print(f"\nАНАЛИЗ КЛАСТЕРОВ {best_algo}:")
print("-" * 40)

for cluster in sorted(np.unique(best_labels)):
    if cluster != -1:
        cluster_data = df[df['Best_Cluster'] == cluster]
        print(f"\nКластер {cluster} ({len(cluster_data)} пациентов):")
        
        # Топ 2 состояния
        top_conds = cluster_data['Condition'].value_counts().head(2)
        print(f"  Основные состояния: {dict(top_conds)}")
        
        # Топ 2 препарата
        top_drugs = cluster_data['Drug_Name'].value_counts().head(2)
        print(f"  Основные препараты: {dict(top_drugs)}")
        
        print(f"  Средний возраст: {cluster_data['Age'].mean():.1f} лет")
        print(f"  Средняя дозировка: {cluster_data['Dosage_mg'].mean():.0f} мг")
        print(f"  Средняя оценка: {cluster_data['Improvement_Score'].mean():.2f}")


df.to_csv('plots/dataset_with_clusters.csv', index=False)

# Анализ DBSCAN кластеров
df['DBSCAN_Cluster'] = dbscan_labels

print("\nАНАЛИЗ КЛАСТЕРОВ DBSCAN:")
print("="*50)

for cluster in sorted(np.unique(dbscan_labels)):
    if cluster == -1:
        continue
        
    cluster_data = df[df['DBSCAN_Cluster'] == cluster]
    print(f"\n КЛАСТЕР {cluster} ({len(cluster_data)} пациентов):")
    
    # Основное состояние
    top_condition = cluster_data['Condition'].value_counts().index[0]
    cond_percent = cluster_data['Condition'].value_counts().iloc[0] / len(cluster_data) * 100
    
    # Основной препарат
    top_drug = cluster_data['Drug_Name'].value_counts().index[0]
    drug_percent = cluster_data['Drug_Name'].value_counts().iloc[0] / len(cluster_data) * 100
    
    print(f"   Основное состояние: {top_condition} ({cond_percent:.0f}%)")
    print(f"   Основной препарат: {top_drug} ({drug_percent:.0f}%)")
    
    # Характеристики
    print(f"   Возраст: {cluster_data['Age'].mean():.0f} лет")
    print(f"   Дозировка: {cluster_data['Dosage_mg'].mean():.0f} мг")

# Выбросы
outliers = df[df['DBSCAN_Cluster'] == -1]
print(f"\n ВЫБРОСЫ: {len(outliers)} пациентов")
print("Состояния:", outliers['Condition'].value_counts().head(3).to_dict())