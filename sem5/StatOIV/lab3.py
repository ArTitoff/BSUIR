import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, confusion_matrix, classification_report
from sklearn.impute import SimpleImputer
import warnings
warnings.filterwarnings('ignore')

# Загрузка данных
df = pd.read_json('/home/artem/Рабочий стол/BSUIR/StatOIV/used_car_listings.json')

# 1. Предобработка данных

# Анализ пропущенных значений
print("Пропущенные значения:")
print(df.isnull().sum())

# Заполнение пропусков
df['condition'].fillna('unknown', inplace=True)
df['trim'].fillna('Unknown', inplace=True)
df['features'].fillna('', inplace=True)

# Преобразование целевой переменной в категории (условие автомобиля)
print("\nРаспределение целевой переменной (condition):")
print(df['condition'].value_counts())

# Кодирование категориальных переменных
categorical_columns = ['make', 'model', 'trim', 'body_type', 'fuel_type', 'transmission', 'location', 'seller_type']
label_encoders = {}

for col in categorical_columns:
    le = LabelEncoder()
    df[col] = le.fit_transform(df[col].astype(str))
    label_encoders[col] = le

# Кодирование целевой переменной
condition_encoder = LabelEncoder()
df['condition_encoded'] = condition_encoder.fit_transform(df['condition'])

# Создание признаков из features
df['num_features'] = df['features'].apply(lambda x: len(str(x).split(', ')) if x else 0)

# Выбор признаков для модели
feature_columns = ['make', 'model', 'year', 'mileage', 'price', 'body_type', 
                   'fuel_type', 'transmission', 'seller_type', 'num_features']

X = df[feature_columns]
y = df['condition_encoded']

# Обработка выбросов в числовых признаках
def remove_outliers(df, columns):
    for col in columns:
        if col in ['mileage', 'price']:
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    return df

X_clean = remove_outliers(pd.concat([X, y], axis=1), ['mileage', 'price'])
X = X_clean[feature_columns]
y = X_clean['condition_encoded']

# Масштабирование числовых признаков
scaler = StandardScaler()
numerical_columns = ['year', 'mileage', 'price', 'num_features']
X[numerical_columns] = scaler.fit_transform(X[numerical_columns])

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

print(f"\nРазмер обучающей выборки: {X_train.shape}")
print(f"Размер тестовой выборки: {X_test.shape}")
print(f"Распределение классов в обучающей выборке:")
print(pd.Series(y_train).value_counts())

# 2. Построение и обучение моделей

models = {
    'Decision Tree': DecisionTreeClassifier(random_state=42),
    'K-Nearest Neighbors': KNeighborsClassifier(),
    'Logistic Regression': LogisticRegression(random_state=42, max_iter=1000),
    'Naive Bayes': GaussianNB()
}

results = {}

# Обучение и оценка моделей
for name, model in models.items():
    print(f"\n--- Обучение модели: {name} ---")
    
    # Обучение модели
    model.fit(X_train, y_train)
    
    # Предсказания
    y_pred = model.predict(X_test)
    y_pred_proba = model.predict_proba(X_test) if hasattr(model, 'predict_proba') else None
    
    # Расчет метрик
    accuracy = accuracy_score(y_test, y_pred)
    precision = precision_score(y_test, y_pred, average='weighted', zero_division=0)
    recall = recall_score(y_test, y_pred, average='weighted', zero_division=0)
    f1 = f1_score(y_test, y_pred, average='weighted', zero_division=0)
    
    # ROC-AUC (только для моделей с вероятностями)
    roc_auc = roc_auc_score(y_test, y_pred_proba, multi_class='ovr') if y_pred_proba is not None else None
    
    # Сохранение результатов
    results[name] = {
        'model': model,
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1': f1,
        'roc_auc': roc_auc,
        'y_pred': y_pred,
        'y_pred_proba': y_pred_proba
    }
    
    print(f"Accuracy: {accuracy:.4f}")
    print(f"Precision: {precision:.4f}")
    print(f"Recall: {recall:.4f}")
    print(f"F1-Score: {f1:.4f}")
    if roc_auc is not None:
        print(f"ROC-AUC: {roc_auc:.4f}")

# 3. Сравнительная таблица результатов
print("\n" + "="*60)
print("СРАВНИТЕЛЬНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
print("="*60)

comparison_df = pd.DataFrame({
    'Model': list(results.keys()),
    'Accuracy': [results[name]['accuracy'] for name in results.keys()],
    'Precision': [results[name]['precision'] for name in results.keys()],
    'Recall': [results[name]['recall'] for name in results.keys()],
    'F1-Score': [results[name]['f1'] for name in results.keys()],
    'ROC-AUC': [results[name]['roc_auc'] if results[name]['roc_auc'] is not None else 'N/A' for name in results.keys()]
})

print(comparison_df.to_string(index=False))

# 4. Матрицы ошибок
fig, axes = plt.subplots(2, 2, figsize=(15, 12))
axes = axes.ravel()

class_names = condition_encoder.classes_

for idx, (name, result) in enumerate(results.items()):
    cm = confusion_matrix(y_test, result['y_pred'])
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=class_names, 
                yticklabels=class_names, ax=axes[idx])
    axes[idx].set_title(f'Confusion Matrix - {name}')
    axes[idx].set_xlabel('Predicted')
    axes[idx].set_ylabel('Actual')

plt.tight_layout()
plt.show()


# 6. Анализ важности признаков (для Decision Tree)
if hasattr(results['Decision Tree']['model'], 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': results['Decision Tree']['model'].feature_importances_
    }).sort_values('importance', ascending=False)
    
    print("\nВажность признаков (Decision Tree):")
    print(feature_importance)
    
    plt.figure(figsize=(10, 6))
    sns.barplot(data=feature_importance, x='importance', y='feature')
    plt.title('Feature Importance - Decision Tree')
    plt.tight_layout()
    plt.show()