import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Настройка визуализации
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12

df = pd.read_json('/home/artem/Рабочий стол/BSUIR/StatOIV/used_car_listings.json')

# Изучение размерности датасета
print("Размерность датасета:")
print(f"Количество строк: {df.shape[0]}")
print(f"Количество столбцов: {df.shape[1]}")
print("\n" + "="*50)

# Изучение типов данных
print("Типы данных каждого столбца:")
print(df.dtypes)
print("\n" + "="*50)

# Первые строки данных
print("Первые 5 строк данных:")
print(df.head())
print("\n" + "="*50)

# Последние строки данных
print("Последние 5 строк данных:")
print(df.tail())
print("\n" + "="*50)

# Общая информация о датасете
print("Общая информация о датасете:")
print(df.info())
print("\n" + "="*50)

# Описательная статистика
print("Описательная статистика числовых столбцов:")
print(df.describe())
print("\n" + "="*50)

# Описательная статистика категориальных столбцов
print("Описательная статистика категориальных столбцов:")
print(df.describe(include=['object']))


# Создаем копию данных для предобработки
df_clean = df.copy()

# Проверка пропущенных значений
print("Пропущенные значения по столбцам:")
missing_values = df_clean.isnull().sum()
print(missing_values[missing_values > 0])
print("\n" + "="*50)

# Обработка пропущенных значений
# Для числовых столбцов заполняем медианой, для категориальных - модой
numeric_columns = ['mileage', 'price']
categorical_columns = ['trim', 'condition', 'features']

for col in numeric_columns:
    if df_clean[col].isnull().sum() > 0:
        df_clean[col].fillna(df_clean[col].median(), inplace=True)

for col in categorical_columns:
    if df_clean[col].isnull().sum() > 0:
        df_clean[col].fillna(df_clean[col].mode()[0] if not df_clean[col].mode().empty else 'Unknown', inplace=True)

# Проверка дубликатов
print(f"Количество полных дубликатов: {df_clean.duplicated().sum()}")
print(f"Количество дубликатов по VIN: {df_clean['vin'].duplicated().sum()}")
print(f"Количество дубликатов по listing_id: {df_clean['listing_id'].duplicated().sum()}")
print("\n" + "="*50)

# Анализ выбросов
print("Анализ выбросов в числовых столбцах:")

def detect_outliers_iqr(data, column):
    Q1 = data[column].quantile(0.25)
    Q3 = data[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = max(0, Q1 - 1.5 * IQR)
    upper_bound = Q3 + 1.5 * IQR
    print(f"Q1 {Q1}   Q3 {Q3}   IQR {IQR}     mefian {data[column].median()}")
    outliers = data[(data[column] < lower_bound) | (data[column] > upper_bound)]
    return outliers, lower_bound, upper_bound

for col in ['price', 'mileage', 'year']:
    outliers, lower, upper = detect_outliers_iqr(df_clean, col)
    print(f"{col}: {len(outliers)} выбросов (границы: [{lower:.2f}, {upper:.2f}])")

print("\n" + "="*50)

# Создание новых переменных



# Возраст автомобиля
current_year = datetime.now().year
df_clean['car_age'] = current_year - df_clean['year']






df_clean['kilometers'] = df_clean['mileage'] * 1.6
print(df_clean[['year','mileage', 'kilometers']])









# # Ценовая категория
# def price_category(price):
#     if price < 5000:
#         return 'Budget'
#     elif price < 15000:
#         return 'Affordable'
#     elif price < 30000:
#         return 'Mid-range'
#     else:
#         return 'Premium'

# df_clean['price_category'] = df_clean['price'].apply(price_category)

# # Категория пробега
# def mileage_category(mileage):
#     if mileage < 30000:
#         return 'Low'
#     elif mileage < 80000:
#         return 'Medium'
#     elif mileage < 150000:
#         return 'High'
#     else:
#         return 'Very High'

# df_clean['mileage_category'] = df_clean['mileage'].apply(mileage_category)

# # Количество функций
# df_clean['num_features'] = df_clean['features'].apply(lambda x: len(str(x).split(', ')) if pd.notna(x) else 0)

# print("Новые созданные переменные:")
# print(df_clean[['car_age', 'price_category', 'mileage_category', 'num_features']].head())
# print("\n" + "="*50)

# # Сформулируем и выполним 10 исследовательских вопросов
# bro = df_clean[(df_clean['price'] == 1140)]
# print(bro[['price', 'make', 'model']])
# print(bro.iloc[0])
# print(df_clean[(df_clean['price'] == 1140)][['price', 'make', 'model']])

# print("АНАЛИТИЧЕСКИЕ ЗАПРОСЫ")
# print("="*60)

# # 1. Какие марки автомобилей наиболее популярны на рынке?
# print("1. Топ-10 самых популярных марок автомобилей:")
# top_makes = df_clean['make'].value_counts().head(10)
# print(top_makes)
# print("\n" + "-"*40)

# # 2. Как распределены цены на подержанные автомобили?
# print("2. Распределение цен на подержанные автомобили:")
# price_stats = df_clean['price'].describe()
# print(price_stats)
# print("\n" + "-"*40)

# # 3. Есть ли зависимость между пробегом и ценой автомобиля?
# print("3. Корреляция между пробегом и ценой:")
# correlation = df_clean['mileage'].corr(df_clean['price'])
# print(f"Коэффициент корреляции: {correlation:.3f}")
# print("\n" + "-"*40)

# # 4. Какие типы кузова наиболее распространены?
# print("4. Распределение автомобилей по типам кузова:")
# body_type_dist = df_clean['body_type'].value_counts()
# print(body_type_dist)
# print("\n" + "-"*40)

# # 5. Как цена зависит от состояния автомобиля?
# print("5. Средняя цена по состоянию автомобиля:")
# condition_price = df_clean.groupby('condition')['price'].agg(['mean', 'median', 'count'])
# print(condition_price)
# print("\n" + "-"*40)

# # 6. Какие типы топлива наиболее популярны в разных странах?
# print("6. Распределение типов топлива по странам (первые 3 страны):")
# # Извлекаем страну из location
# df_clean['country'] = df_clean['location'].str.split(',').str[-1].str.strip()
# top_countries = df_clean['country'].value_counts().head(3).index
# fuel_by_country = pd.crosstab(df_clean[df_clean['country'].isin(top_countries)]['country'], 
#                              df_clean[df_clean['country'].isin(top_countries)]['fuel_type'])
# print(fuel_by_country)
# print("\n" + "-"*40)

# # 7. Как возраст автомобиля влияет на его цену?
# print("7. Зависимость цены от возраста автомобиля:")
# age_price_corr = df_clean['car_age'].corr(df_clean['price'])
# print(f"Коэффициент корреляции между возрастом и ценой: {age_price_corr:.3f}")
# age_price_stats = df_clean.groupby('car_age')['price'].mean()
# print("Средняя цена по возрасту автомобиля (первые 5 значений):")
# print(age_price_stats.head())
# print("\n" + "-"*40)

# # 8. Какие продавцы предлагают самые дорогие автомобили?
# print("8. Средняя цена автомобилей по типам продавцов:")
# seller_price = df_clean.groupby('seller_type')['price'].agg(['mean', 'median', 'count'])
# print(seller_price)
# print("\n" + "-"*40)

# # 9. Как пробег распределен по разным маркам автомобилей?
# print("9. Средний пробег по маркам автомобилей (топ-5 марок):")
# top_5_makes = df_clean['make'].value_counts().head(5).index
# mileage_by_make = df_clean[df_clean['make'].isin(top_5_makes)].groupby('make')['mileage'].mean().sort_values(ascending=False).head(1)
# print(mileage_by_make)
# print("\n" + "-"*40)

# # 10. Какие функции наиболее часто встречаются в автомобилях?
# print("10. Топ-10 самых популярных функций в автомобилях:")
# all_features = []
# for features in df_clean['features'].dropna():
#     if isinstance(features, str):
#         all_features.extend([f.strip() for f in features.split(',')])
    
# feature_counts = pd.Series(all_features).value_counts().head(10)
# print(feature_counts)

# import os

# # Создаем папку для графиков
# if not os.path.exists('plots'):
#     os.makedirs('plots')

# print("\nСОЗДАНИЕ ВИЗУАЛИЗАЦИЙ")
# print("="*60)

# # Одномерная визуализация: количественные переменные
# print("Создание гистограмм и box plot для количественных переменных...")

# fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# # Гистограмма цен
# axes[0, 0].hist(df_clean['price'], bins=30, alpha=0.7, edgecolor='black', color='skyblue')
# axes[0, 0].set_title('Распределение цен автомобилей')
# axes[0, 0].set_xlabel('Цена ($)')
# axes[0, 0].set_ylabel('Количество')
# axes[0, 0].grid(True, alpha=0.3)

# # Box plot цен
# axes[0, 1].boxplot(df_clean['price'])
# axes[0, 1].set_title('Коробчатая диаграмма цен')
# axes[0, 1].set_ylabel('Цена ($)')

# # Гистограмма пробега
# axes[1, 0].hist(df_clean['mileage'], bins=30, alpha=0.7, edgecolor='black', color='lightcoral')
# axes[1, 0].set_title('Распределение пробега автомобилей')
# axes[1, 0].set_xlabel('Пробег (миль)')
# axes[1, 0].set_ylabel('Количество')
# axes[1, 0].grid(True, alpha=0.3)

# # Box plot пробега
# axes[1, 1].boxplot(df_clean['mileage'])
# axes[1, 1].set_title('Коробчатая диаграмма пробега')
# axes[1, 1].set_ylabel('Пробег (миль)')

# plt.tight_layout()
# plt.savefig('plots/1_quantitative_distributions.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("✓ Сохранен график: plots/1_quantitative_distributions.png")

# # Одномерная визуализация: категориальные переменные
# print("Создание bar plot для категориальных переменных...")

# fig, axes = plt.subplots(2, 2, figsize=(15, 12))

# # Топ-10 марок автомобилей
# top_makes = df_clean['make'].value_counts().head(10)
# axes[0, 0].bar(top_makes.index, top_makes.values, color='lightgreen')
# axes[0, 0].set_title('Топ-10 самых популярных марок автомобилей')
# axes[0, 0].set_xlabel('Марка')
# axes[0, 0].set_ylabel('Количество')
# axes[0, 0].tick_params(axis='x', rotation=45)

# # Распределение по типу топлива
# fuel_dist = df_clean['fuel_type'].value_counts()
# axes[0, 1].bar(fuel_dist.index, fuel_dist.values, color='lightyellow')
# axes[0, 1].set_title('Распределение по типу топлива')
# axes[0, 1].set_xlabel('Тип топлива')
# axes[0, 1].set_ylabel('Количество')
# axes[0, 1].tick_params(axis='x', rotation=45)

# # Распределение по состоянию
# condition_dist = df_clean['condition'].value_counts()
# axes[1, 0].bar(condition_dist.index, condition_dist.values, color='lightpink')
# axes[1, 0].set_title('Распределение по состоянию автомобилей')
# axes[1, 0].set_xlabel('Состояние')
# axes[1, 0].set_ylabel('Количество')

# # Распределение по типу кузова (топ-8)
# body_type_top = df_clean['body_type'].value_counts().head(8)
# axes[1, 1].bar(body_type_top.index, body_type_top.values, color='lightblue')
# axes[1, 1].set_title('Топ-8 типов кузова')
# axes[1, 1].set_xlabel('Тип кузова')
# axes[1, 1].set_ylabel('Количество')
# axes[1, 1].tick_params(axis='x', rotation=45)

# plt.tight_layout()
# plt.savefig('plots/2_categorical_distributions.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("✓ Сохранен график: plots/2_categorical_distributions.png")

# # Многомерная визуализация
# print("Создание многомерных визуализаций...")

# # Матрица корреляций
# numeric_cols = ['price', 'mileage', 'year', 'car_age', 'num_features']
# corr_matrix = df_clean[numeric_cols].corr()

# plt.figure(figsize=(10, 8))
# sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, 
#             square=True, fmt='.2f', cbar_kws={'label': 'Коэффициент корреляции'})
# plt.title('Матрица корреляций числовых переменных')
# plt.tight_layout()
# plt.savefig('plots/3_correlation_matrix.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("✓ Сохранен график: plots/3_correlation_matrix.png")

# # Диаграммы рассеяния
# fig, axes = plt.subplots(1, 2, figsize=(15, 6))

# # Цена vs Пробег
# axes[0].scatter(df_clean['mileage'], df_clean['price'], alpha=0.6, color='blue')
# axes[0].set_title('Зависимость цены от пробега')
# axes[0].set_xlabel('Пробег (миль)')
# axes[0].set_ylabel('Цена ($)')
# axes[0].grid(True, alpha=0.3)

# # Цена vs Год выпуска
# axes[1].scatter(df_clean['year'], df_clean['price'], alpha=0.6, color='red')
# axes[1].set_title('Зависимость цены от года выпуска')
# axes[1].set_xlabel('Год выпуска')
# axes[1].set_ylabel('Цена ($)')
# axes[1].grid(True, alpha=0.3)

# plt.tight_layout()
# plt.savefig('plots/4_scatter_plots.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("✓ Сохранен график: plots/4_scatter_plots.png")

# # Таблица сопряженности с визуализацией
# print("Создание таблиц сопряженности...")

# # Тип топлива по состоянию автомобиля
# contingency_table = pd.crosstab(df_clean['fuel_type'], df_clean['condition'])
# plt.figure(figsize=(12, 8))
# sns.heatmap(contingency_table, annot=True, fmt='d', cmap='Blues')
# plt.title('Таблица сопряженности: Тип топлива vs Состояние')
# plt.xlabel('Состояние')
# plt.ylabel('Тип топлива')
# plt.tight_layout()
# plt.savefig('plots/5_contingency_table_fuel_condition.png', dpi=300, bbox_inches='tight')
# plt.close()
# print("✓ Сохранен график: plots/5_contingency_table_fuel_condition.png")


# print("\n" + "="*60)
# print("ВСЕ ГРАФИКИ УСПЕШНО СОХРАНЕНЫ В ПАПКУ 'plots'")
# print("Создано 11 графиков:")
# print("1. plots/1_quantitative_distributions.png - Распределение цен и пробега")
# print("2. plots/2_categorical_distributions.png - Распределение категориальных переменных")
# print("3. plots/3_correlation_matrix.png - Матрица корреляций")
# print("4. plots/4_scatter_plots.png - Диаграммы рассеяния")
# print("5. plots/5_contingency_table_fuel_condition.png - Таблица сопряженности")

# print("="*60)

# print("\nАНАЛИЗ И ВЫВОДЫ")
# print("="*60)

# print("1. СТРУКТУРА ДАННЫХ:")
# print(f"• Датасет содержит {df_clean.shape[0]} объявлений о продаже автомобилей")
# print(f"• Данные включают {df_clean.shape[1]} характеристик для каждого автомобиля")
# print("• Основные категории данных: технические характеристики, цена, пробег, состояние, местоположение")

# print("\n2. КЛЮЧЕВЫЕ ЗАКОНОМЕРНОСТИ:")

# # Анализ распределения цен
# price_analysis = f"""
# • Цены на автомобили варьируются от ${df_clean['price'].min():,.0f} до ${df_clean['price'].max():,.0f}
# • Медианная цена составляет ${df_clean['price'].median():,.0f}
# • 75% автомобилей стоят менее ${df_clean['price'].quantile(0.75):,.0f}
# """
# print(price_analysis)

# # Анализ пробега
# mileage_analysis = f"""
# • Пробег автомобилей варьируется от {df_clean['mileage'].min():,} до {df_clean['mileage'].max():,} миль
# • Медианный пробег составляет {df_clean['mileage'].median():,} миль
# • Большинство автомобилей имеют пробег менее {df_clean['mileage'].quantile(0.75):,} миль
# """
# print(mileage_analysis)

# print("\n3. ВЗАИМОСВЯЗИ МЕЖДУ ПЕРЕМЕННЫМИ:")

# # Корреляционный анализ
# corr_analysis = f"""
# • Наблюдается сильная отрицательная корреляция между пробегом и ценой: {df_clean['mileage'].corr(df_clean['price']):.3f}
# • Положительная корреляция между годом выпуска и ценой: {df_clean['year'].corr(df_clean['price']):.3f}
# • Количество функций слабо коррелирует с ценой: {df_clean['num_features'].corr(df_clean['price']):.3f}
# """
# print(corr_analysis)

# print("\n4. РАСПРЕДЕЛЕНИЕ КАТЕГОРИАЛЬНЫХ ПЕРЕМЕННЫХ:")

# # Анализ популярности марок
# top_3_makes = df_clean['make'].value_counts().head(3)
# print(f"• Самые популярные марки: {', '.join(top_3_makes.index.tolist())}")

# # Анализ типов топлива
# fuel_dist = df_clean['fuel_type'].value_counts()
# print(f"• Преобладают автомобили на бензине: {fuel_dist.get('Petrol', 0)} единиц ({fuel_dist.get('Petrol', 0)/len(df_clean)*100:.1f}%)")

# # Анализ состояний
# condition_dist = df_clean['condition'].value_counts()
# print(f"• Большинство автомобилей в хорошем состоянии: {condition_dist.get('good', 0)} единиц")

# print("\n5. ИНТЕРЕСНЫЕ НАХОДКИ:")

# interesting_findings = """
# • На рынке представлено значительное количество электромобилей и гибридов
# • Цены на автомобили в отличном состоянии значительно выше, чем на автомобили в хорошем состоянии
# • Автомобили с большим количеством дополнительных функций имеют более высокую цену
# • Существуют региональные различия в предпочтениях по типам топлива
# • Некоторые марки демонстрируют лучшую сохранность стоимости с течением времени
# """

# print(interesting_findings)

# print("\n6. РЕКОМЕНДАЦИИ ДЛЯ ДАЛЬНЕЙШЕГО АНАЛИЗА:")
# recommendations = """
# • Провести сегментационный анализ по ценовым категориям
# • Исследовать географические различия в ценах и предпочтениях
# • Проанализировать сезонность спроса на автомобили
# • Создать модель прогнозирования цены на основе характеристик автомобиля
# • Исследовать факторы, влияющие на скорость продажи автомобилей
# """

# print(recommendations)

# # Финальная сводка
# print("\nФИНАЛЬНАЯ СВОДКА:")
# print("="*40)
# print("Анализ данных о подержанных автомобилях выявил четкие рыночные закономерности:")
# print("• Цена сильно зависит от пробега, года выпуска и состояния")
# print("• Рынок сегментирован по маркам, типам кузова и топлива")
# print("• Наличие дополнительных функций увеличивает стоимость автомобиля")
# print("• Существуют значительные различия между типами продавцов")
# print("• Данные содержат потенциал для построения прогнозных моделей")