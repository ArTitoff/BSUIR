import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder, PolynomialFeatures
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import warnings
warnings.filterwarnings('ignore')

# Загрузка данных
df = pd.read_json('/home/artem/Рабочий стол/BSUIR/StatOIV/used_car_listings.json')

print("Размер датасета:", df.shape)
print("\nПервые 5 строк:")
print(df.head())
print("\nИнформация о данных:")
print(df.info())
print("\nСтатистика числовых признаков:")
print(df.describe())



# Анализ пропущенных значений
print("Пропущенные значения:")
print(df.isnull().sum())

# Обработка пропущенных значений
# Для числовых признаков заполняем медианой, для категориальных - модой
df['mileage'] = df['mileage'].fillna(df['mileage'].median())
df['price'] = df['price'].fillna(df['price'].median())
df['condition'] = df['condition'].fillna(df['condition'].mode()[0])
df['trim'] = df['trim'].fillna('Unknown')
df['features'] = df['features'].fillna('')

# Удаление строк с пропусками в ключевых признаках
df = df.dropna(subset=['make', 'model', 'year', 'fuel_type'])

print(f"Размер датасета после обработки пропусков: {df.shape}")

# Анализ выбросов
plt.figure(figsize=(15, 10))

plt.subplot(2, 3, 1)
df.boxplot(column='price')
plt.title('Выбросы в цене')

plt.subplot(2, 3, 2)
df.boxplot(column='mileage')
plt.title('Выбросы в пробеге')

plt.subplot(2, 3, 3)
df.boxplot(column='year')
plt.title('Выбросы в годе выпуска')

plt.tight_layout()
plt.show()

# Обработка выбросов в цене и пробеге
Q1_price = df['price'].quantile(0.25)
Q3_price = df['price'].quantile(0.75)
IQR_price = Q3_price - Q1_price

Q1_mileage = df['mileage'].quantile(0.25)
Q3_mileage = df['mileage'].quantile(0.75)
IQR_mileage = Q3_mileage - Q1_mileage

# Удаление выбросов
df_clean = df[
    (df['price'] >= Q1_price - 1.5 * IQR_price) & 
    (df['price'] <= Q3_price + 1.5 * IQR_price) &
    (df['mileage'] >= Q1_mileage - 1.5 * IQR_mileage) & 
    (df['mileage'] <= Q3_mileage + 1.5 * IQR_mileage)
]

print(f"Размер датасета после удаления выбросов: {df_clean.shape}")

# Создание новых признаков
df_clean['car_age'] = 2025 - df_clean['year']  # Предполагаем текущий год 2025
df_clean['mileage_per_year'] = df_clean['mileage'] / (df_clean['car_age'] + 1)  # +1 чтобы избежать деления на 0

# Кодирование категориальных переменных
categorical_columns = ['make', 'model', 'trim', 'body_type', 'fuel_type', 'transmission', 
                      'condition', 'location', 'seller_type']

label_encoders = {}
for col in categorical_columns:
    le = LabelEncoder()
    df_clean[col + '_encoded'] = le.fit_transform(df_clean[col].astype(str))
    label_encoders[col] = le

# Создание бинарных признаков для features
features_list = []
for features in df_clean['features']:
    if pd.notna(features):
        features_list.extend([feature.strip() for feature in features.split(',')])

common_features = pd.Series(features_list).value_counts().head(15).index

for feature in common_features:
    df_clean['has_' + feature.lower().replace(' ', '_')] = df_clean['features'].apply(
        lambda x: 1 if pd.notna(x) and feature in x else 0
    )

# Выбор признаков для модели
feature_columns = [
    'year', 'mileage', 'car_age', 'mileage_per_year',
    'make_encoded', 'model_encoded', 'body_type_encoded', 
    'fuel_type_encoded', 'transmission_encoded', 'condition_encoded',
    'seller_type_encoded'
] + ['has_' + feature.lower().replace(' ', '_') for feature in common_features]

X = df_clean[feature_columns]
y = df_clean['price']

print(f"Количество признаков: {len(feature_columns)}")

# Нормализация числовых признаков
scaler = StandardScaler()
numerical_columns = ['year', 'mileage', 'car_age', 'mileage_per_year']
X[numerical_columns] = scaler.fit_transform(X[numerical_columns])

# Разделение на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

print(f"Обучающая выборка: {X_train.shape}")
print(f"Тестовая выборка: {X_test.shape}")



# Функция для оценки моделей
def evaluate_model(model, X_train, X_test, y_train, y_test, model_name):
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    
    mae = mean_absolute_error(y_test, y_pred)
    mse = mean_squared_error(y_test, y_pred)
    rmse = np.sqrt(mse)
    r2 = r2_score(y_test, y_pred)
    
    return {
        'Model': model_name,
        'MAE': mae,
        'MSE': mse,
        'RMSE': rmse,
        'R2': r2
    }

# Обучение моделей
results = []

# 1. Линейная регрессия
lr = LinearRegression()
results.append(evaluate_model(lr, X_train, X_test, y_train, y_test, 'Linear Regression'))

# 2. Полиномиальная регрессия (степень 2)
poly = PolynomialFeatures(degree=2)
X_train_poly = poly.fit_transform(X_train)
X_test_poly = poly.transform(X_test)

lr_poly = LinearRegression()
lr_poly.fit(X_train_poly, y_train)
y_pred_poly = lr_poly.predict(X_test_poly)

results.append({
    'Model': 'Polynomial Regression (deg=2)',
    'MAE': mean_absolute_error(y_test, y_pred_poly),
    'MSE': mean_squared_error(y_test, y_pred_poly),
    'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_poly)),
    'R2': r2_score(y_test, y_pred_poly)
})

# 3. Ridge регрессия
ridge = Ridge(alpha=1.0)
results.append(evaluate_model(ridge, X_train, X_test, y_train, y_test, 'Ridge Regression'))

# 4. Lasso регрессия
lasso = Lasso(alpha=0.1)
results.append(evaluate_model(lasso, X_train, X_test, y_train, y_test, 'Lasso Regression'))

# 5. Случайный лес
rf = RandomForestRegressor(n_estimators=100, random_state=42)
results.append(evaluate_model(rf, X_train, X_test, y_train, y_test, 'Random Forest'))

# 6. Градиентный бустинг
gb = GradientBoostingRegressor(n_estimators=100, random_state=42)
results.append(evaluate_model(gb, X_train, X_test, y_train, y_test, 'Gradient Boosting'))

# Создание сравнительной таблицы
results_df = pd.DataFrame(results)
print("\nСравнительная таблица моделей:")
print(results_df.round(4))



# Визуализация результатов
plt.figure(figsize=(15, 10))

# График сравнения R²
plt.subplot(2, 2, 1)
plt.bar(results_df['Model'], results_df['R2'])
plt.title('Сравнение R² score')
plt.xticks(rotation=45)
plt.ylabel('R²')

# График сравнения RMSE
plt.subplot(2, 2, 2)
plt.bar(results_df['Model'], results_df['RMSE'])
plt.title('Сравнение RMSE')
plt.xticks(rotation=45)
plt.ylabel('RMSE')

# График сравнения MAE
plt.subplot(2, 2, 3)
plt.bar(results_df['Model'], results_df['MAE'])
plt.title('Сравнение MAE')
plt.xticks(rotation=45)
plt.ylabel('MAE')

plt.tight_layout()
plt.show()

# Вывод лучшей модели
best_model_idx = results_df['R2'].idxmax()
best_model_name = results_df.loc[best_model_idx, 'Model']
best_model_score = results_df.loc[best_model_idx, 'R2']

print(f"\nЛучшая модель: {best_model_name} с R² = {best_model_score:.4f}")



# Анализ важности признаков для Random Forest
if best_model_name == 'Random Forest':
    best_model = rf
elif best_model_name == 'Gradient Boosting':
    best_model = gb
else:
    # Для линейных моделей используем коэффициенты
    if best_model_name == 'Linear Regression':
        best_model = lr
    elif best_model_name == 'Ridge Regression':
        best_model = ridge
    elif best_model_name == 'Lasso Regression':
        best_model = lasso
    else:
        best_model = rf  # по умолчанию

# Важность признаков
if hasattr(best_model, 'feature_importances_'):
    feature_importance = pd.DataFrame({
        'feature': feature_columns,
        'importance': best_model.feature_importances_
    }).sort_values('importance', ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(data=feature_importance.head(15), x='importance', y='feature')
    plt.title(f'Топ-15 важных признаков ({best_model_name})')
    plt.tight_layout()
    plt.show()
    
    print("Топ-10 важных признаков:")
    print(feature_importance.head(10))
elif hasattr(best_model, 'coef_'):
    # Для линейных моделей
    coef_df = pd.DataFrame({
        'feature': feature_columns,
        'coefficient': best_model.coef_
    }).sort_values('coefficient', key=abs, ascending=False)
    
    plt.figure(figsize=(12, 8))
    sns.barplot(data=coef_df.head(15), x='coefficient', y='feature')
    plt.title(f'Топ-15 коэффициентов ({best_model_name})')
    plt.tight_layout()
    plt.show()

# График предсказаний vs реальных значений
best_model.fit(X_train, y_train)
y_pred_best = best_model.predict(X_test)

plt.figure(figsize=(10, 6))
plt.scatter(y_test, y_pred_best, alpha=0.5)
plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
plt.xlabel('Реальные значения')
plt.ylabel('Предсказанные значения')
plt.title(f'{best_model_name} - Предсказания vs Реальные значения')
plt.show()

# Анализ остатков
residuals = y_test - y_pred_best
plt.figure(figsize=(12, 4))

plt.subplot(1, 2, 1)
plt.scatter(y_pred_best, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Предсказанные значения')
plt.ylabel('Остатки')
plt.title('Остатки vs Предсказания')

plt.subplot(1, 2, 2)
plt.hist(residuals, bins=30, edgecolor='black')
plt.xlabel('Остатки')
plt.ylabel('Частота')
plt.title('Распределение остатков')

plt.tight_layout()
plt.show()




# Тюнинг гиперпараметров для лучшей модели
from sklearn.model_selection import GridSearchCV

if best_model_name in ['Random Forest', 'Gradient Boosting']:
    if best_model_name == 'Random Forest':
        param_grid = {
            'n_estimators': [50, 100, 200],
            'max_depth': [None, 10, 20],
            'min_samples_split': [2, 5, 10]
        }
        model = RandomForestRegressor(random_state=42)
    else:
        param_grid = {
            'n_estimators': [50, 100, 200],
            'learning_rate': [0.05, 0.1, 0.2],
            'max_depth': [3, 5, 7]
        }
        model = GradientBoostingRegressor(random_state=42)
    
    grid_search = GridSearchCV(model, param_grid, cv=5, scoring='r2', n_jobs=-1)
    grid_search.fit(X_train, y_train)
    
    print(f"Лучшие параметры: {grid_search.best_params_}")
    print(f"Лучший R²: {grid_search.best_score_:.4f}")
    
    # Оценка тюнингованной модели
    best_tuned_model = grid_search.best_estimator_
    y_pred_tuned = best_tuned_model.predict(X_test)
    
    print(f"R² на тестовой выборке после тюнинга: {r2_score(y_test, y_pred_tuned):.4f}")

# Создание новых признаков
df_clean['is_luxury'] = df_clean['make'].isin(['Mercedes-Benz', 'BMW', 'Audi', 'Tesla']).astype(int)
df_clean['is_high_mileage'] = (df_clean['mileage'] > df_clean['mileage'].median()).astype(int)
df_clean['price_per_mile'] = df_clean['price'] / (df_clean['mileage'] + 1)

print("\nАнализ завершен!")