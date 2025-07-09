"""
Script generado desde Jupyter Notebook (maps_scatter2.ipynb)
Contiene análisis geoespacial y visualización de datos usando GeoPandas y Matplotlib.

Cada bloque está comentado para facilitar su comprensión.
"""


import geopandas as gpd
import matplotlib.pyplot as plt
from matplotlib import colorbar
import numpy as np
import matplotlib.colors as mcolors
import pandas as pd
import seaborn as sns
from adjustText import adjust_text
import contextily as ctx
from sklearn.preprocessing import MinMaxScaler
from scipy.stats.mstats import winsorize


# Cargar datos geoespaciales
data = gpd.read_file('C:/Users/668084668/Urban vegetation main cities/datos/data_vf.shp')

data.columns

# Resumen estadístico de Relative.v por ciudad
summary_by_city = data.groupby('City')['Relative.v'].describe()

# Si quieres un resumen más personalizado:
custom_summary = data.groupby('City')['Relative.v'].agg(
    ['count', 'mean', 'median', 'std', 'min', 'max', 'quantile']
).rename(columns={
    'quantile': '75th_percentile'
})

# Para calcular el percentil 75 (ejemplo)
custom_summary['75th_percentile'] = data.groupby('City')['Relative.v'].quantile(0.75)

# Mostrar los resultados
print("Resumen estadístico completo:")
print(summary_by_city)

print("\nResumen personalizado:")
print(custom_summary)

# Si necesitas guardar los resultados a CSV
summary_by_city.to_csv('resumen_relative_v_por_ciudad.csv')
custom_summary.to_csv('resumen_personalizado_relative_v.csv')

data = data.rename(columns={
    'Wealth.Cha': 'Wealth.Change',
    'Relative.v': 'Relative.vegetation.trend',
    'Initial.We' : 'Initial Wealth'
})

# Seleccionar solo columnas numéricas
columnas_numericas = ['Wealth.Change','Initial Wealth', 'Relative.vegetation.trend'  ]
#columnas_numericas = ['Wealth.Cha','Initial.We', 'Initial.Ed','Initial.Po','Population', 'Initial St','Structural','Relative.v'  ]

# Configurar el layout de los subgráficos
n_columnas = 2  # Cantidad de columnas en el grid
n_filas = (len(columnas_numericas) + 1) // n_columnas  # Calcula las filas necesarias

# 1. Agrupar por ciudad y crear un gráfico por cada una
for ciudad in data['City'].unique():  # Asumiendo que hay una columna 'City'
    
    # Filtrar datos de la ciudad actual
    data_ciudad = data[data['City'] == ciudad]
    
    # Crear figura para esta ciudad
    fig, ejes = plt.subplots(n_filas, n_columnas, figsize=(15, 5*n_filas))
    fig.suptitle(f'Ciudad: {ciudad}', fontsize=14, y=1.02)  # Título general
    ejes = ejes.flatten()
    
    # Generar histogramas (igual que antes pero con data_ciudad)
    for i, columna in enumerate(columnas_numericas):
        ejes[i].hist(data_ciudad[columna].dropna(), bins=100, color='skyblue', edgecolor='black')
        ejes[i].set_title(f'{columna}', fontsize=10)
        ejes[i].set_xlabel('Valor')
        ejes[i].set_ylabel('Frecuencia')
    
    # Ocultar ejes vacíos y ajustar
    for j in range(i + 1, len(ejes)):
        ejes[j].set_visible(False)
    plt.tight_layout()
    plt.show()

data.columns

# Renombrar el valor "Buenos Air" a "Great Buenos Aires" en la columna 'City'
data['City'] = data['City'].replace('Buenos Air', 'Great Buenos Aires')
data['City'] = data['City'].replace('Salta', 'Great Salta')
data['City'] = data['City'].replace('Tucuman', 'Great San Miguel de Tucuman')
data['City'] = data['City'].replace('Rosario', 'Great Rosario')
data['City'] = data['City'].replace('Cordoba', 'Great Cordoba')

import matplotlib.pyplot as plt
import numpy as np

# Ordenar ciudades
ordered_categories = ['Great Salta', 'Great San Miguel de Tucuman', 'Great Rosario', 'Great Cordoba', 'Great Buenos Aires']
cities = data['City'].unique()
cities_sorted = sorted(cities, key=lambda x: ordered_categories.index(x) if x in ordered_categories else -1)

# Crear figura
fig, axes = plt.subplots(3, 2, figsize=(15, 18))
axes = axes.flatten()

for i, city in enumerate(cities_sorted):
    ax = axes[i]
    
    # Filtrar datos
    city_data = data[data['City'] == city]
    x = city_data['Wealth.Change']
    y = city_data['Relative.vegetation.trend']
    
    # Hexbin plot
    hb = ax.hexbin(x, y, gridsize=60, cmap='vlag', mincnt=1)
    
    # Líneas de referencia
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
    ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
    
    # Añadir números en esquinas (1-2-4-3 en sentido reloj)
    ax.text(0.05, 0.05, 'Q3', ha='left', va='bottom', 
            transform=ax.transAxes, fontsize=12, weight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))  # Esquina inferior izquierda
    
    ax.text(0.95, 0.05, 'Q4', ha='right', va='bottom', 
            transform=ax.transAxes, fontsize=12, weight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))  # Esquina inferior derecha
    
    ax.text(0.95, 0.95, 'Q2', ha='right', va='top', 
            transform=ax.transAxes, fontsize=12, weight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))  # Esquina superior derecha
    
    ax.text(0.05, 0.95, 'Q1', ha='left', va='top', 
            transform=ax.transAxes, fontsize=12, weight='bold',
            bbox=dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2))  # Esquina superior izquierda
    
    # Configuración adicional
    ax.set_title(f"{city}", fontsize=14)
    ax.set_xlabel('Wealth Change', fontsize=12)
    ax.set_ylabel('Relative vegetation trend (2000-2020)', fontsize=12)
    ax.grid(color='gray', linestyle='-', linewidth=0.2, alpha=0.5)
    
    # Colorbar
    cb = fig.colorbar(hb, ax=ax, fraction=0.04, pad=0.04)
    cb.set_label('Count', fontsize=10)
    cb.ax.tick_params(labelsize=8)

# Eliminar ejes vacíos
for ax in axes[len(cities):]:
    fig.delaxes(ax)

plt.tight_layout()
plt.show()

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

# Ordenar ciudades
ordered_categories = ['Great Salta', 'Great San Miguel de Tucuman', 'Great Rosario', 
                     'Great Cordoba', 'Great Buenos Aires']
cities = data['City'].unique()
cities_sorted = sorted(cities, key=lambda x: ordered_categories.index(x) if x in ordered_categories else -1)

# Limpiar datos - eliminar filas con NaN en las columnas relevantes
clean_data = data.dropna(subset=['Wealth.Change', 'Relative.vegetation.trend'])

# Calcular límites globales para la colorbar
all_counts = []
for city in cities_sorted:
    city_data = clean_data[clean_data['City'] == city]
    if len(city_data) > 0:  # Solo si hay datos para esta ciudad
        x = city_data['Wealth.Change']
        y = city_data['Relative.vegetation.trend']
        # Calcular conteos aproximados sin graficar
        counts, xedges, yedges = np.histogram2d(x, y, bins=60)
        all_counts.append(counts)

if all_counts:  # Solo si encontramos datos válidos
    global_min = min([np.min(c[c > 0]) for c in all_counts if np.any(c > 0)])  # Mínimo excluyendo ceros
    global_max = max([np.max(c) for c in all_counts])
else:
    global_min, global_max = 0, 1  # Valores por defecto si no hay datos

# Crear figura
fig, axes = plt.subplots(3, 2, figsize=(15, 18))
axes = axes.flatten()

for i, city in enumerate(cities_sorted):
    ax = axes[i]
    
    # Filtrar datos
    city_data = clean_data[clean_data['City'] == city]
    
    if len(city_data) == 0:
        ax.text(0.5, 0.5, 'No hay datos', ha='center', va='center')
        ax.set_title(f"{city}", fontsize=14)
        continue
        
    x = city_data['Wealth.Change']
    y = city_data['Relative.vegetation.trend']
    
    # Hexbin plot con límites globales
    hb = ax.hexbin(x, y, gridsize=60, cmap='vlag', 
                   mincnt=1, vmin=global_min, vmax=global_max)
    
    # Líneas de referencia
    ax.axhline(0, color='black', linestyle='--', linewidth=0.8)
    ax.axvline(0, color='black', linestyle='--', linewidth=0.8)
    
    # Añadir números en esquinas
    bbox_props = dict(facecolor='white', alpha=0.8, edgecolor='none', pad=2)
    ax.text(0.05, 0.05, 'Q3', ha='left', va='bottom', 
            transform=ax.transAxes, fontsize=12, weight='bold', bbox=bbox_props)
    ax.text(0.95, 0.05, 'Q4', ha='right', va='bottom', 
            transform=ax.transAxes, fontsize=12, weight='bold', bbox=bbox_props)
    ax.text(0.95, 0.95, 'Q2', ha='right', va='top', 
            transform=ax.transAxes, fontsize=12, weight='bold', bbox=bbox_props)
    ax.text(0.05, 0.95, 'Q1', ha='left', va='top', 
            transform=ax.transAxes, fontsize=12, weight='bold', bbox=bbox_props)
    
    # Configuración adicional
    ax.set_title(f"{city}", fontsize=14)
    ax.set_xlabel('Wealth Change', fontsize=12)
    ax.set_ylabel('Relative vegetation trend (2000-2020)', fontsize=12)
    ax.grid(color='gray', linestyle='-', linewidth=0.2, alpha=0.5)

# Crear una sola colorbar si hay datos
if any(len(clean_data[clean_data['City'] == city]) > 0 for city in cities_sorted):
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])
    cb = fig.colorbar(hb, cax=cbar_ax)
    cb.set_label('Count', fontsize=12)
    cb.ax.tick_params(labelsize=10)
    plt.tight_layout(rect=[0, 0, 0.9, 1])
else:
    plt.tight_layout()

# Eliminar ejes vacíos
for ax in axes[len(cities_sorted):]:
    fig.delaxes(ax)

plt.show()

import pandas as pd

def sign_based_categorization(group):
    # Asignar 1 a negativos y 2 a positivos
    return pd.Series(
        np.where(group > 0, 2, 1),  # 2 para positivos, 1 para negativos
        index=group.index
    )

# Aplicar a cada ciudad (aunque el agrupamiento no afecta la categorización)
data['Vegetation_Quantile'] = (
    data.groupby('City')['Relative.vegetation.trend']
    .transform(sign_based_categorization)
)

data['Wealth_quantile'] = (
    data.groupby('City')['Wealth.Change']
    .transform(sign_based_categorization)
)


# Resultado
print(data[['City', 'Relative.vegetation.trend', 'Vegetation_Quantile']].head())
print(data[['City', 'Wealth.Change', 'Wealth_quantile']].head())

data = data.dropna(subset=['Wealth_quantile', 'Vegetation_Quantile'])

# Suponiendo que tienes columnas 'Vegetation_Quantile' y 'Wealth_Quantile'
data['Quantile_combination'] = (
    data['Vegetation_Quantile'].astype(str) 
    + "-" 
    + data['Wealth_quantile'].astype(str)
)


import pandas as pd
import numpy as np

def median_based_categorization(group):
    med = group.median()
    return pd.Series(
        np.where(group > med, 2, 1),  # 2 si mayor a mediana, 1 si menor o igual
        index=group.index
    )

# Vegetation
data['Vegetation_Quantile'] = (
    data.groupby('City')['Relative.vegetation.trend']
        .transform(median_based_categorization)
)

# Wealth
data['Wealth_quantile_i'] = (
    data.groupby('City')['Initial Wealth']
    .transform(sign_based_categorization)
)

# Resultado
print(data[['City', 'Relative.vegetation.trend', 'Vegetation_Quantile']].head())
print(data[['City', 'Initial Wealth', 'Wealth_quantile_i']].head())





# Suponiendo que tienes columnas 'Vegetation_Quantile' y 'Wealth_Quantile'
data['Quantile_combination2'] = (
    data['Vegetation_Quantile'].astype(str) 
    + "-" 
    + data['Wealth_quantile_i'].astype(str)
)

print("Valores únicos en Quantile_combination:", data['Quantile_combination'].unique())

print("Valores únicos en Quantile_combination:", data['Quantile_combination2'].unique())

# 1. Crear la combinación de cuantiles
data['Quantile_combination'] = (
    data['Vegetation_Quantile'].astype(str) 
    + "-" 
    + data['Wealth_quantile'].astype(str)
)

# 2. Definir el orden deseado de las categorías
combination_order = ['1-1', '1-2', '2-1', '2-2']

# 3. Convertir a categoría ordenada
data['Quantile_combination'] = pd.Categorical(
    data['Quantile_combination'],
    categories=combination_order,
    ordered=True
)

# Verificar
print(data[['Vegetation_Quantile', 'Wealth_quantile', 'Quantile_combination']].head(10))
print("\nFrecuencias:\n", data['Quantile_combination'].value_counts().loc[combination_order])


# 2. Definir el orden deseado de las categorías
combination_order = ['1-1', '1-2', '2-1', '2-2']

# 3. Convertir a categoría ordenada
data['Quantile_combination2'] = pd.Categorical(
    data['Quantile_combination2'],
    categories=combination_order,
    ordered=True
)

# Verificar
print(data[['Vegetation_Quantile', 'Wealth_quantile_i', 'Quantile_combination2']].head(10))
print("\nFrecuencias:\n", data['Quantile_combination2'].value_counts().loc[combination_order])

# 1. Crear diccionario de mapeo de códigos a categorías
codigos_a_categorias = {
    '1-1': 'Low Vegetation & Low Wealth',
    '1-2': 'Low Vegetation & High Wealth',
    '2-1': 'High Vegetation & Low Wealth',
    '2-2': 'High Vegetation & High Wealth'
}

# 2. Reemplazar los códigos por las categorías textuales
data['Quantile_combination'] = data['Quantile_combination'].replace(codigos_a_categorias)

# 3. Convertir a categoría ordenada
cat_order = [
    'Low Vegetation & Low Wealth',
    'Low Vegetation & High Wealth',
    'High Vegetation & Low Wealth',
    'High Vegetation & High Wealth'
]

data['Quantile_combination'] = pd.Categorical(
    data['Quantile_combination'],
    categories=cat_order,
    ordered=True
)

# 1. Crear diccionario de mapeo de códigos a categorías
codigos_a_categorias = {
    '1-1': 'Low Vegetation & Low Wealth',
    '1-2': 'Low Vegetation & High Wealth',
    '2-1': 'High Vegetation & Low Wealth',
    '2-2': 'High Vegetation & High Wealth'
}

# 2. Reemplazar los códigos por las categorías textuales
data['Quantile_combination2'] = data['Quantile_combination2'].replace(codigos_a_categorias)

# 3. Convertir a categoría ordenada
cat_order = [
    'Low Vegetation & Low Wealth',
    'Low Vegetation & High Wealth',
    'High Vegetation & Low Wealth',
    'High Vegetation & High Wealth'
]

data['Quantile_combination2'] = pd.Categorical(
    data['Quantile_combination2'],
    categories=cat_order,
    ordered=True
)

# Verificar resultado
print(data['Quantile_combination'].unique())

# Verificar resultado
print(data['Quantile_combination2'].unique())

import geopandas as gpd
import matplotlib.pyplot as plt

# Lista de ciudades únicas en el GeoDataFrame
# Definir el orden deseado de categorías
ordered_categories = ['Great Salta','Great San Miguel de Tucuman', 'Great Rosario', 'Great Cordoba','Great Buenos Aires']

# Obtener los valores únicos de 'City'
cities = data['City'].unique()

# Ordenar los valores únicos según el orden en `ordered_categories`
cities_sorted = sorted(cities, key=lambda x: ordered_categories.index(x) if x in ordered_categories else -1)

# Verificar el resultado
print(cities_sorted)

import geopandas as gpd
import matplotlib.pyplot as plt


# Crear una figura con 2 columnas y 3 filas
fig, axes = plt.subplots(3, 2, figsize=(15, 18))  # Ajustar el tamaño según necesites
axes = axes.flatten()  # Convertir en una lista de ejes

# Iterar por cada ciudad y crear un mapa
for idx, city in enumerate(cities_sorted):
    # Filtrar los datos por ciudad
    city_df = data[data['City'] == city]
    
    # Crear el mapa en el subgráfico correspondiente
    ax = axes[idx]
    city_df.plot(
        column='Relative.vegetation.trend', 
        cmap='Greens',  
        scheme='Quantiles', 
        ax=ax, 
        legend=True,
        legend_kwds={
            'loc': 'center left',  # Posición a la izquierda del gráfico
            'bbox_to_anchor': (1, 0.5)  # Mover fuera del gráfico
        }
    )

    # Ajustar el título y etiquetas para cada subgráfico
    ax.set_title(f'{city}', fontsize=15)
    ax.set_xlabel('Longitude', fontsize=10)
    ax.set_ylabel('Latitude', fontsize=10)

# Remover ejes vacíos si el número de ciudades es menor que los subgráficos
for j in range(idx + 1, len(axes)):
    fig.delaxes(axes[j])

# Ajustar los espacios entre subgráficos
plt.tight_layout()
plt.show()


import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import pandas as pd
import geopandas as gpd
import contextily as ctx
import numpy as np

# 1. Configuración inicial
# 2. Ajustar matriz de colores para orientación correcta
# 1. Mapeo directo de códigos a colores (¡clave!)
codigo_a_color = {
    0: '#FFE0B2',  # Low Veg & Low Wealth
    1: '#a80909',   # Low Veg & High Wealth
    2: '#4CAF50',   # High Veg & Low Wealth
    3: '#083b88'    # High Veg & High Wealth
}

# 2. Ordenar ciudades
ordered_cities = ['Great Salta', 'Great San Miguel de Tucuman', 
                 'Great Rosario', 'Great Cordoba', 'Great Buenos Aires']
cities_sorted = sorted(data['City'].unique(), 
                      key=lambda x: ordered_cities.index(x) if x in ordered_cities else len(ordered_cities))

# 3. Configurar figura principal con GridSpec
fig = plt.figure(figsize=(12, 15))
gs = fig.add_gridspec(3, 2, hspace=0.3, wspace=0.1)  # 3 filas, 2 columnas
axes = [fig.add_subplot(gs[i]) for i in range(5)]  # 5 ciudades

# 4. Mapa principal para cada ciudad
# 2. Asignar colores directamente usando los códigos
for idx, (ax, city) in enumerate(zip(axes, cities_sorted)):
    city_data = data[data['City'] == city].to_crs('EPSG:3857')
    
    # Mapear códigos a colores hexadecimales
    city_data['color'] = city_data['Quantile_combination'].cat.codes.map(codigo_a_color)
    
    city_data.plot(
        ax=ax,
        color=city_data['color'],  # Usar colores directos
        categorical=True,
        legend=False,
        vmin=0,
        vmax=3
        #edgecolor='gray',
        #linewidth=0.3
    )
    
    ctx.add_basemap(ax, source=ctx.providers.CartoDB.Positron)
    ax.set_title(city, fontsize=12, pad=10, weight='bold')
    ax.set_axis_off()

# 3. Leyenda simplificada (sin complicar ejes)
ax_legend = fig.add_axes([0.55, 0.08, 0.3, 0.2])
legend_labels = [
    ('Q3', '#FFE0B2'),
    ('Q4', '#a80909'),
    ('Q1', '#4CAF50'),
    ('Q2', '#083b88')
]

for i, (label, color) in enumerate(legend_labels):
    ax_legend.add_patch(plt.Rectangle((i%2*0.5, i//2*0.5), 0.5, 0.5, color=color))
    ax_legend.text(i%2*0.5 + 0.25, i//2*0.5 + 0.25, label, 
                   ha='center', va='center', fontsize=8)

ax_legend.axis('off')

plt.show()

import matplotlib.pyplot as plt
import geopandas as gpd
import contextily as ctx

# Colores
codigo_a_color = {
    0: '#FFE0B2',
    1: '#a80909',
    2: '#4CAF50',
    3: '#083b88'
}

# Orden de ciudades
ordered_cities = ['Great Salta', 'Great San Miguel de Tucuman',
                  'Great Rosario', 'Great Cordoba', 'Great Buenos Aires']
cities_sorted = sorted(data['City'].unique(),
                       key=lambda x: ordered_cities.index(x) if x in ordered_cities else len(ordered_cities))

# Figura y gridspec — 6 filas (5 mapas + 1 leyenda), 2 columnas
fig = plt.figure(figsize=(14, 20))
gs = fig.add_gridspec(
    6, 2, 
    hspace=0.1, wspace=0.0,
    height_ratios=[1, 1, 1, 1, 1, 0.4]  # leyenda más angosta
)
axes = [fig.add_subplot(gs[i, j]) for i in range(5) for j in range(2)]

# Márgenes ajustados
fig.subplots_adjust(left=0.0, right=0.5, top=0.96, bottom=0.05)

# Títulos de columnas
fig.text(0.05, 0.98, "Quantile Combination (Wealth Change)", ha='center', va='center', fontsize=13, weight='bold')
fig.text(0.40, 0.98, "Quantile Combination (Initial Wealth)", ha='center', va='center', fontsize=13, weight='bold')

# Mapas
for idx, city in enumerate(cities_sorted):
    city_data = data[data['City'] == city].to_crs('EPSG:3857')

    city_data['color_q1'] = city_data['Quantile_combination'].cat.codes.map(codigo_a_color)
    city_data.plot(ax=axes[idx*2], color=city_data['color_q1'], legend=False)
    ctx.add_basemap(axes[idx*2], source=ctx.providers.CartoDB.Positron)
    axes[idx*2].set_title(f"{city}", fontsize=11)
    axes[idx*2].set_axis_off()

    city_data['color_q2'] = city_data['Quantile_combination2'].cat.codes.map(codigo_a_color)
    city_data.plot(ax=axes[idx*2+1], color=city_data['color_q2'], legend=False)
    ctx.add_basemap(axes[idx*2+1], source=ctx.providers.CartoDB.Positron)
    axes[idx*2+1].set_title(f"{city}", fontsize=11)
    axes[idx*2+1].set_axis_off()

# Leyenda cuadrada bivariada en la última fila ocupando ambas columnas
ax_legend = fig.add_subplot(gs[5, :])

# Definir cuadrantes bivariados — (col, row)
legend_labels = {
    (0, 0): ('Q3', '#FFE0B2'),
    (1, 0): ('Q4', '#a80909'),
    (0, 1): ('Q1', '#4CAF50'),
    (1, 1): ('Q2', '#083b88')
}

# Definir posición inicial y tamaño de los cuadrantes (para centrarlo)
start_x, start_y = 0.3, 0.3
square_size = 0.2  # más pequeño

# Dibujar cuadrados 2x2
for (col, row), (label, color) in legend_labels.items():
    x = start_x + col * square_size
    y = start_y + row * square_size
    ax_legend.add_patch(plt.Rectangle((x, y), square_size, square_size, color=color, ec='black'))

# Etiquetas de ejes de la leyenda bivariada
# Eje Y (Vertical)
ax_legend.text(start_x - 0.05, start_y + 1.5 * square_size, 'High Veg', ha='right', va='center', fontsize=11)
ax_legend.text(start_x - 0.05, start_y + 0.5 * square_size, 'Low Veg', ha='right', va='center', fontsize=11)

# Eje X (Horizontal)
ax_legend.text(start_x + 0.5 * square_size, start_y - 0.05, 'Low Wealth', ha='center', va='top', fontsize=11)
ax_legend.text(start_x + 1.5 * square_size, start_y - 0.05, 'High Wealth', ha='center', va='top', fontsize=11)

# Definir límites ajustados y quitar ejes
ax_legend.set_xlim(0, 1)
ax_legend.set_ylim(0, 1)
ax_legend.axis('off')


plt.show()


# Guardar el GeoDataFrame resultante en un nuevo shapefile
data.to_file("C:/Users/668084668/Urban vegetation main cities/data_quantil.shp")

import matplotlib.pyplot as plt
import pandas as pd

# 1. Definir ciudades y columnas
ordered_cities = [
    'Great Salta', 
    'Great San Miguel de Tucuman',
    'Great Rosario', 
    'Great Cordoba', 
    'Great Buenos Aires'
]

columnas = [
    "Education.level.change", 
    "Initial.Population.Density", 
    "Wealth.Change",
    "Population.Density.Change", 
    "Structural Poverty Change",
    "Initial.Wealth", 
    "Initial.Education",   
    "Initial Structural Poverty"
]

# 2. Crear histogramas por ciudad
for city in ordered_cities:
    # Filtrar datos por ciudad
    city_data = data[data['City'] == city]
    
    # Crear figura para la ciudad actual
    plt.figure(figsize=(15, 12))
    plt.suptitle(f'Distribuciones en {city}', fontsize=16, y=1.02)
    
    # Generar subplots para todas las variables
    for idx, col in enumerate(columnas, 1):
        ax = plt.subplot(3, 3, idx)  # 3 filas, 3 columnas (para 8 variables + espacio)
        ax.hist(
            city_data[col].dropna(),
            bins=30,
            color='#3498db',
            edgecolor='#2c3e50',
            alpha=0.8
        )
        ax.set_title(col, fontsize=10)
        ax.grid(linestyle='--', alpha=0.6)
        ax.set_xlabel('Valor', fontsize=8)
        ax.set_ylabel('Frecuencia', fontsize=8)
    
    # Ajustar layout y mostrar
    plt.tight_layout()
    plt.show()