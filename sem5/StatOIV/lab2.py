import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, OneHotEncoder, PolynomialFeatures
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')
import os

# Создаем папку для графиков
os.makedirs('plots', exist_ok=True)

# Загрузка данных из JSON файла
df = pd.read_json('/home/artem/Рабочий стол/BSUIR/StatOIV/used_car_listings.json')

print("Размер датасета:", df.shape)
print("\nПервые 5 строк:")
print(df.head())

# 1. Анализ данных
print("\n" + "="*50)
print("1. АНАЛИЗ ДАННЫХ")
print("="*50)

print("\nИнформация о данных:")
print(df.info())

print("\nСтатистика числовых признаков:")
print(df.describe())

print("\nПропущенные значения:")
print(df.isnull().sum())

# 2. Предобработка данных
print("\n" + "="*50)
print("2. ПРЕДОБРАБОТКА ДАННЫХ")
print("="*50)

# Анализ и визуализация пропущенных значений
plt.figure(figsize=(12, 6))
sns.heatmap(df.isnull(), cbar=True, yticklabels=False, cmap='viridis')
plt.title('Карта пропущенных значений')
plt.tight_layout()
plt.savefig('plots/missing_values.png', dpi=300, bbox_inches='tight')
plt.close()

# Обработка пропусков
print("\nОбработка пропущенных значений")


# Заполняем числовые пропуски медианой
numeric_columns = ['year', 'mileage', 'price']
for col in numeric_columns:
    if col in df.columns and df[col].isnull().sum() > 0:
        missing_count = df[col].isnull().sum()
        df[col].fillna(df[col].median(), inplace=True)
        print(f"Заполнено пропусков в {col}: {missing_count}")

# Заполняем категориальные пропуски модой или специальным значением
categorical_columns = ['trim', 'condition', 'features']
for col in categorical_columns:
    if col in df.columns and df[col].isnull().sum() > 0:
        missing_count = df[col].isnull().sum()
        if not df[col].mode().empty:
            df[col].fillna(df[col].mode()[0], inplace=True)
        else:
            df[col].fillna('unknown', inplace=True)
        print(f"Заполнено пропусков в {col}: {missing_count}")

print("\nПропуски после обработки:")
print(df.isnull().sum())

# Анализ и обработка выбросов
print("\nАнализ выбросов")

plt.figure(figsize=(15, 10))

# Визуализация выбросов в числовых признаках
numeric_features = ['year', 'mileage', 'price']
for i, feature in enumerate(numeric_features, 1):
    plt.subplot(2, 3, i)
    sns.boxplot(y=df[feature])
    plt.title(f'Выбросы в {feature}')
    
    plt.subplot(2, 3, i+3)
    sns.histplot(df[feature], kde=True)
    plt.title(f'Распределение {feature}')

plt.tight_layout()
plt.savefig('plots/outliers_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# Обработка выбросов в цене и пробеге с помощью IQR
def remove_outliers_iqr(df, column):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]

original_size = len(df)
if 'price' in df.columns:
    df = remove_outliers_iqr(df, 'price')
    print(f"Удалено выбросов по цене: {original_size - len(df)}")
    original_size = len(df)

if 'mileage' in df.columns:
    df = remove_outliers_iqr(df, 'mileage')
    print(f"Удалено выбросов по пробегу: {original_size - len(df)}")

# Создание новых признаков
print("\nСоздание новых признаков")

# Логарифмирование цены для нормализации распределения
if 'price' in df.columns:
    df['log_price'] = np.log1p(df['price'])

# Количество функций в features
if 'features' in df.columns:
    df['num_features'] = df['features'].apply(lambda x: len(str(x).split(',')) if pd.notnull(x) else 0)

# Извлечение страны из location
if 'location' in df.columns:
    df['country'] = df['location'].apply(lambda x: str(x).split(',')[-1].strip() if pd.notnull(x) else 'Unknown')

# Анализ категориальных признаков
print("\nАнализ категориальных признаков:")
categorical_cols = ['make', 'model', 'body_type', 'fuel_type', 'transmission', 'condition', 'seller_type', 'country']
available_categorical = [col for col in categorical_cols if col in df.columns]

for col in available_categorical:
    print(f"\n{col}: {df[col].nunique()} уникальных значений")
    print(df[col].value_counts().head())

# Визуализация распределения целевой переменной
plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
if 'price' in df.columns:
    sns.histplot(df['price'], kde=True)
    plt.title('Распределение цены')

plt.subplot(1, 2, 2)
if 'log_price' in df.columns:
    sns.histplot(df['log_price'], kde=True)
    plt.title('Распределение логарифма цены')

plt.tight_layout()
plt.savefig('plots/price_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# 3. Подготовка данных для моделирования
print("\n" + "="*50)
print("3. ПОДГОТОВКА ДАННЫХ ДЛЯ МОДЕЛИРОВАНИЯ")
print("="*50)

# Выбор признаков для модели (только те, которые есть в данных)
available_features = []
numeric_features_available = []
categorical_features_available = []

# Проверяем доступность признаков
potential_numeric = ['year', 'mileage',  'num_features']
potential_categorical = ['make', 'model', 'body_type', 'fuel_type', 'transmission', 'condition', 'seller_type', 'country']

for feature in potential_numeric:
    if feature in df.columns:
        available_features.append(feature)
        numeric_features_available.append(feature)

for feature in potential_categorical:
    if feature in df.columns:
        available_features.append(feature)
        categorical_features_available.append(feature)

print(f"Используемые признаки: {available_features}")
print(f"Числовые признаки: {numeric_features_available}")
print(f"Категориальные признаки: {categorical_features_available}")

if 'price' not in df.columns:
    print("ОШИБКА: Целевая переменная 'price' не найдена в данных!")
    print("Доступные колонки:", df.columns.tolist())
    exit()

X = df[available_features]
y = df['price']  # Используем исходную цену как целевую переменную

print(f"Размеры: X {X.shape}, y {y.shape}")

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Обучающая выборка: {X_train.shape}")
print(f"Тестовая выборка: {X_test.shape}")

# Создание препроцессора
preprocessor = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), numeric_features_available),
        ('cat', OneHotEncoder(handle_unknown='ignore', sparse_output=False), categorical_features_available)
    ]
)

# 4. Построение и обучение моделей
print("\n" + "="*50)
print("4. ПОСТРОЕНИЕ И ОБУЧЕНИЕ МОДЕЛЕЙ")
print("="*50)

# Определение моделей
models = {
    'Linear Regression': LinearRegression(),
    'Polynomial Regression (deg=2)': Pipeline([
        ('poly', PolynomialFeatures(degree=2, include_bias=False)),
        ('linear', LinearRegression())
    ]),
    'Ridge Regression': Ridge(alpha=1.0),
    'Lasso Regression': Lasso(alpha=1.0),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'Gradient Boosting': GradientBoostingRegressor(n_estimators=100, random_state=42)
}

# Создание пайплайнов с препроцессором
pipelines = {}
for name, model in models.items():
    pipelines[name] = Pipeline(steps=[
        ('preprocessor', preprocessor),
        ('model', model)
    ])

# Обучение моделей и оценка качества
results = {}

for name, pipeline in pipelines.items():
    print(f"\nОбучение {name}")
    
    # Обучение модели
    pipeline.fit(X_train, y_train)
    
    # Предсказания
    y_pred = pipeline.predict(X_test)
    
    # Расчет метрик
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    results[name] = {
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2,
        'pipeline': pipeline
    }
    
    print(f"MAE: {mae:.2f}, MSE: {mse:.2f}, RMSE: {rmse:.2f}, R2: {r2:.4f}")

# 5. Сравнительная таблица результатов
print("\n" + "="*50)
print("5. СРАВНИТЕЛЬНАЯ ТАБЛИЦА РЕЗУЛЬТАТОВ")
print("="*50)

results_df = pd.DataFrame(results).T
# Преобразуем числовые колонки к float для избежания ошибок с heatmap
for col in ['MAE', 'MSE', 'RMSE', 'R2']:
    results_df[col] = pd.to_numeric(results_df[col], errors='coerce')
    
results_df = results_df.round(4)

# Выводим таблицу в консоль
print("Сравнительная таблица всех моделей:")
print(results_df)


# Создаем красивую таблицу для отчета
print("\n" + "="*60)
print("ТАБЛИЦА РЕЗУЛЬТАТОВ (отсортировано по R²)")
print("="*60)

# Сортируем по R² (от лучшего к худшему)
sorted_results = results_df.sort_values('R2', ascending=False)

# Форматируем вывод для лучшей читаемости
formatted_table = sorted_results.copy()
formatted_table['MAE'] = formatted_table['MAE'].apply(lambda x: f"{x:.0f}")
formatted_table['MSE'] = formatted_table['MSE'].apply(lambda x: f"{x:.0f}")
formatted_table['RMSE'] = formatted_table['RMSE'].apply(lambda x: f"{x:.0f}")
formatted_table['R2'] = formatted_table['R2'].apply(lambda x: f"{x:.4f}")

print(formatted_table)

# Визуализация сравнения моделей (ТОЛЬКО ГРАФИКИ, без наложения текста)
plt.figure(figsize=(16, 10))

# 1. Сравнение R2 (горизонтальные барчики)
plt.subplot(2, 2, 1)
r2_sorted = results_df['R2'].sort_values()
bars = plt.barh(range(len(r2_sorted)), r2_sorted.values, color='skyblue')
plt.title('Сравнение R² score (чем больше - тем лучше)')
plt.yticks(range(len(r2_sorted)), r2_sorted.index)
plt.xlabel('R² Score')

# Добавляем значения на барчики
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + 0.01, bar.get_y() + bar.get_height()/2, 
             f'{width:.3f}', ha='left', va='center', fontsize=9)

# 2. Сравнение RMSE (горизонтальные барчики)
plt.subplot(2, 2, 2)
rmse_sorted = results_df['RMSE'].sort_values(ascending=True)  # Лучшие модели сверху
bars = plt.barh(range(len(rmse_sorted)), rmse_sorted.values, color='lightcoral')
plt.title('Сравнение RMSE (чем меньше - тем лучше)')
plt.yticks(range(len(rmse_sorted)), rmse_sorted.index)
plt.xlabel('RMSE')

# Добавляем значения на барчики
for i, bar in enumerate(bars):
    width = bar.get_width()
    plt.text(width + max(rmse_sorted)*0.01, bar.get_y() + bar.get_height()/2, 
             f'{width:.0f}', ha='left', va='center', fontsize=9)

# 3. Сравнение MAE и RMSE на одном графике
plt.subplot(2, 2, 3)
metrics_to_plot = ['MAE', 'RMSE']
results_df[metrics_to_plot].plot(kind='bar', ax=plt.gca())
plt.title('Сравнение MAE и RMSE')
plt.xticks(rotation=45)
plt.ylabel('Значение')
plt.legend()

# 4. Рейтинг моделей по качеству
plt.subplot(2, 2, 4)
# Создаем комплексный score (можно настроить веса)
composite_score = (results_df['R2'] * 1000) - results_df['RMSE']  # Пример весов
composite_score_sorted = composite_score.sort_values(ascending=False)

bars = plt.bar(range(len(composite_score_sorted)), composite_score_sorted.values, 
               color=['gold', 'silver', 'brown', 'lightblue', 'lightgreen', 'pink'])
plt.title('Комплексный рейтинг моделей')
plt.xticks(range(len(composite_score_sorted)), composite_score_sorted.index, rotation=45)
plt.ylabel('Комплексный score')

# Добавляем значения на барчики
for i, bar in enumerate(bars):
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2, height + max(composite_score_sorted)*0.01, 
             f'{height:.0f}', ha='center', va='bottom', fontsize=9)

plt.tight_layout()
plt.savefig('plots/model_comparison.png', dpi=300, bbox_inches='tight')
plt.close()


# 6. Выбор лучшей модели и анализ
print("\n" + "="*50)
print("6. ВЫБОР ЛУЧШЕЙ МОДЕЛИ И АНАЛИЗ")
print("="*50)

# Выбор лучшей модели по R2 score
best_model_name = results_df['R2'].idxmax()
best_model = results[best_model_name]['pipeline']
best_metrics = results[best_model_name]

print(f"Лучшая модель: {best_model_name}")
print(f"Метрики лучшей модели: R2 = {best_metrics['R2']:.4f}, RMSE = {best_metrics['RMSE']:.2f}")

# Анализ важности признаков для моделей, которые поддерживают feature_importances_
if hasattr(best_model.named_steps['model'], 'feature_importances_'):
    print("\nАнализ важности признаков для лучшей модели...")
    
    # Получаем имена признаков после OneHot кодирования
    feature_names = []
    
    # Числовые признаки - используем правильную переменную
    feature_names.extend(numeric_features_available)
    
    # Категориальные признаки после OneHot - используем правильную переменную
    categorical_encoder = best_model.named_steps['preprocessor'].named_transformers_['cat']
    if hasattr(categorical_encoder, 'get_feature_names_out'):
        # Используем categorical_features_available вместо categorical_features
        cat_features = categorical_encoder.get_feature_names_out(categorical_features_available)
        feature_names.extend(cat_features)
    
    # Важности признаков
    importances = best_model.named_steps['model'].feature_importances_
    

    print("\nВывод ONEHOT")
    simple_onehot = pd.get_dummies(X_train[categorical_features_available])
    print(simple_onehot.head())

    # Создаем DataFrame с важностями
    feature_importance_df = pd.DataFrame({
        'feature': feature_names,
        'importance': importances
    }).sort_values('importance', ascending=False)
    
    print("\nТоп-10 самых важных признаков:")
    print(feature_importance_df.head(10))
    
    # Визуализация важности признаков
    plt.figure(figsize=(12, 8))
    top_features = feature_importance_df.head(15)
    sns.barplot(data=top_features, x='importance', y='feature')
    plt.title(f'Топ-15 самых важных признаков ({best_model_name})')
    plt.tight_layout()
    plt.savefig('plots/feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
else:
    print(f"\nМодель {best_model_name} не поддерживает анализ важности признаков.")

# График предсказаний vs реальные значения для лучшей модели
y_pred_best = best_model.predict(X_test)

plt.figure(figsize=(12, 5))

plt.subplot(1, 2, 1)
plt.scatter(y_test, y_pred_best, alpha=0.6)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title(f'{best_model_name}\nПредсказания vs Реальные значения')

plt.subplot(1, 2, 2)
residuals = y_test - y_pred_best
plt.scatter(y_pred_best, residuals, alpha=0.6)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Предсказанные значения')
plt.ylabel('Остатки')
plt.title('Остатки модели')

plt.tight_layout()
plt.savefig('plots/best_model_predictions.png', dpi=300, bbox_inches='tight')
plt.close()

# 7. Дополнительный анализ

# Анализ влияния года выпуска на цену
plt.figure(figsize=(12, 6))
if 'year' in df.columns and 'price' in df.columns and 'fuel_type' in df.columns:
    sns.scatterplot(data=df, x='year', y='price', hue='fuel_type', alpha=0.7)
    plt.title('Влияние года выпуска и типа топлива на цену')
    plt.tight_layout()
    plt.savefig('plots/year_price_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()

# Анализ влияния пробега на цену
plt.figure(figsize=(12, 6))
if 'mileage' in df.columns and 'price' in df.columns and 'condition' in df.columns:
    sns.scatterplot(data=df, x='mileage', y='price', hue='condition', alpha=0.7)
    plt.title('Влияние пробега и состояния на цену')
    plt.tight_layout()
    plt.savefig('plots/mileage_price_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()


# Создание отчета
print("\n" + "="*50)
print("ФИНАЛЬНЫЙ ОТЧЕТ")
print("="*50)
print(f"Лучшая модель: {best_model_name}")
print(f"R² score: {best_metrics['R2']:.4f}")
print(f"RMSE: {best_metrics['RMSE']:.2f}")
print(f"MAE: {best_metrics['MAE']:.2f}")
print(f"\nВсе графики сохранены в папку 'plots/'")
print(f"Результаты моделей сохранены в 'model_results.csv'")