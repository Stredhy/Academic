"""Ejercicio 8 - Clustering jerárquico del Zoo Dataset.

Coloca zoo(1).csv junto a este archivo y ejecuta:
    python ejercicio8_zoo.py

Las figuras se guardan y se muestran automáticamente (cierra la ventana para continuar).
Para ejecutar sin ventanas: MOSTRAR_GRAFICAS = False.
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.cluster.hierarchy import linkage, dendrogram, cut_tree
from scipy.spatial.distance import pdist, squareform
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score, silhouette_score

SEMILLA = 42
MOSTRAR_GRAFICAS = True
CARPETA = Path(__file__).resolve().parent
SALIDA = CARPETA / 'resultados_ejercicio8'
SALIDA.mkdir(exist_ok=True)


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(SALIDA / nombre, dpi=180, bbox_inches='tight')
    if MOSTRAR_GRAFICAS:
        plt.show()
    plt.close()


def guardar_tabla(tabla, nombre):
    tabla.to_csv(SALIDA / nombre, index=False, encoding='utf-8-sig')
    print(f'\n{nombre}\n{tabla.to_string(index=False)}')


# 8.1 Datos y distancia
archivo = CARPETA / 'zoo.csv'
df = pd.read_csv(archivo)
if {'animal_name', 'class_type', 'legs'} - set(df.columns):
    raise ValueError('Faltan columnas necesarias: animal_name, class_type o legs.')

identificador = 'animal_name'
etiqueta = 'class_type'
atributos = df.drop(columns=[identificador, etiqueta]).copy()

# 8.1.1 Número de animales, atributos, clases y conteos.
resumen = pd.DataFrame([{
    'animales': len(df),
    'atributos_originales': atributos.shape[1],
    'clases': df[etiqueta].nunique(),
}])
guardar_tabla(resumen, '8_1_1_resumen.csv')
conteos = df[etiqueta].value_counts().sort_index()
clases = pd.DataFrame({
    'clase': conteos.index,
    'conteo': conteos.values,
    'porcentaje': (conteos.values / len(df) * 100).round(2),
})
guardar_tabla(clases, '8_1_1_conteos_clases.csv')
plt.figure(figsize=(8, 5))
barras = plt.bar(clases['clase'].astype(str), clases['conteo'])
plt.bar_label(barras)
plt.xlabel('Clase real (class_type)')
plt.ylabel('Número de animales')
plt.title('8.1.1 - Distribución de clases del Zoo Dataset')
guardar_figura('8_1_1_clases.png')

# 8.1.2 Comprobar faltantes; imputación simple solo si hiciera falta.
faltantes = atributos.isna().sum().reset_index()
faltantes.columns = ['atributo', 'NaN']
guardar_tabla(faltantes, '8_1_2_faltantes.csv')
if atributos.isna().any().any():
    from sklearn.impute import SimpleImputer
    atributos = pd.DataFrame(
        SimpleImputer(strategy='most_frequent').fit_transform(atributos),
        columns=atributos.columns,
        index=atributos.index,
    )

# 8.1.3 Jaccard requiere atributos de presencia/ausencia.
# 'legs' es una categoría (0, 2, 4, 5, 6, 8) y se transforma a one-hot.
# El resto de columnas son binarias en la versión estándar de Zoo.
resto = atributos.drop(columns=['legs'])
if not resto.isin([0, 1]).all().all():
    raise ValueError('Se esperaban atributos binarios distintos de legs.')
patas = pd.get_dummies(atributos['legs'].astype(int).astype(str), prefix='legs', dtype=int)
X = pd.concat([resto.astype(int), patas], axis=1)
X = X.astype(bool)
guardar_tabla(pd.DataFrame({'atributo_binario': X.columns}), '8_1_3_atributos_jaccard.csv')

distancias_condensadas = pdist(X.to_numpy(), metric='jaccard')
matriz_distancias = squareform(distancias_condensadas)
pd.DataFrame(matriz_distancias, index=df[identificador], columns=df[identificador]).to_csv(
    SALIDA / '8_2_1_distancias_jaccard.csv', encoding='utf-8-sig'
)

# 8.2.1-8.2.2 Construir jerarquías y reportar alturas de fusión.
metodos = ['single', 'complete', 'average']
jerarquias = {}
resultados = []
alturas = []
cruces = []
tamanos = []
descripciones = []

for metodo in metodos:
    Z = linkage(distancias_condensadas, method=metodo)
    jerarquias[metodo] = Z
    alturas.append({
        'metodo': metodo,
        'altura_minima': Z[:, 2].min(),
        'altura_media': Z[:, 2].mean(),
        'altura_maxima': Z[:, 2].max(),
        'altura_ultima_fusion': Z[-1, 2],
    })
    pd.DataFrame({
        'fusion': np.arange(1, len(Z) + 1),
        'altura': Z[:, 2],
        'observaciones_en_grupo': Z[:, 3].astype(int),
    }).to_csv(SALIDA / f'8_2_2_alturas_{metodo}.csv', index=False)

    # 8.3.1 Cortar exactamente a 7 grupos. cut_tree garantiza 7 clusters,
    # incluso si algunas alturas están empatadas.
    grupos = cut_tree(Z, n_clusters=7).ravel() + 1
    conteo_grupos = pd.Series(grupos).value_counts().sort_index()
    tamanos.extend({
        'metodo': metodo, 'cluster': int(cluster), 'tamano': int(cantidad)
    } for cluster, cantidad in conteo_grupos.items())

    tabla_cruzada = pd.crosstab(
        pd.Series(grupos, name='cluster'),
        df[etiqueta].rename('class_type'),
    ).reindex(index=range(1, 8), columns=sorted(df[etiqueta].unique()), fill_value=0)
    tabla_cruzada.to_csv(SALIDA / f'8_3_1_cruce_{metodo}.csv', encoding='utf-8-sig')
    for cluster, fila in tabla_cruzada.iterrows():
        cruces.append({'metodo': metodo, 'cluster': cluster, **{
            f'clase_{c}': int(fila[c]) for c in tabla_cruzada.columns
        }})

    # Dos grupos por método: los dos mayores, con animales y composición.
    for cluster in conteo_grupos.sort_values(ascending=False).head(2).index:
        seleccion = df.loc[grupos == cluster]
        descripciones.append({
            'metodo': metodo,
            'cluster': int(cluster),
            'tamano': len(seleccion),
            'composicion_clases': str(seleccion[etiqueta].value_counts().sort_index().to_dict()),
            'animales': ', '.join(seleccion[identificador].astype(str).tolist()),
        })

    # 8.4.1 Silhouette precomputed usa exactamente la distancia Jaccard.
    silhouette = silhouette_score(matriz_distancias, grupos, metric='precomputed')
    resultados.append({
        'metodo': metodo,
        'n_clusters': len(np.unique(grupos)),
        'ARI': adjusted_rand_score(df[etiqueta], grupos),
        'NMI': normalized_mutual_info_score(df[etiqueta], grupos),
        'silhouette_jaccard': silhouette,
    })

guardar_tabla(pd.DataFrame(alturas), '8_2_2_resumen_alturas.csv')
guardar_tabla(pd.DataFrame(tamanos), '8_3_1_tamanos_clusters.csv')
guardar_tabla(pd.DataFrame(cruces), '8_3_1_cruces_todos.csv')
guardar_tabla(pd.DataFrame(descripciones), '8_3_1_dos_grupos_por_metodo.csv')
comparacion = pd.DataFrame(resultados)
guardar_tabla(comparacion, '8_4_1_metricas.csv')

# Etiquetas en el mismo orden de entrada para los tres dendrogramas.
# La posición horizontal de hojas puede cambiar: depende de la jerarquía.
for metodo in metodos:
    plt.figure(figsize=(19, 7))
    dendrogram(
        jerarquias[metodo], labels=df[identificador].astype(str).tolist(),
        leaf_rotation=90, leaf_font_size=6,
    )
    plt.xlabel('Animales (orden de hojas determinado por la jerarquía)')
    plt.ylabel('Distancia Jaccard / altura de fusión')
    plt.title(f'8.2 - Dendrograma: enlace {metodo}')
    guardar_figura(f'8_2_dendrograma_{metodo}.png')

# Comparación de métricas entre enlaces.
fig, ax = plt.subplots(figsize=(9, 5))
indices = np.arange(len(metodos))
ancho = 0.25
for posicion, metrica in enumerate(['ARI', 'NMI', 'silhouette_jaccard']):
    ax.bar(indices + (posicion - 1) * ancho, comparacion[metrica], ancho, label=metrica)
ax.set_xticks(indices, metodos)
ax.set_ylim(0, 1)
ax.set_xlabel('Criterio de enlace')
ax.set_ylabel('Puntuación')
ax.set_title('8.4.1 - Concordancia y separación de clusters')
ax.legend()
guardar_figura('8_4_1_comparacion.png')

mejor_ari = comparacion.loc[comparacion['ARI'].idxmax()]
mejor_silueta = comparacion.loc[comparacion['silhouette_jaccard'].idxmax()]
texto = (
    'Interpretación de resultados\n'
    f"Mayor ARI: {mejor_ari['metodo']} ({mejor_ari['ARI']:.4f}); "
    'mide correspondencia con las clases reales, ajustada por azar.\n'
    f"Mayor silhouette: {mejor_silueta['metodo']} "
    f"({mejor_silueta['silhouette_jaccard']:.4f}); "
    'mide separación interna usando distancias Jaccard.\n'
    'NMI mide información compartida entre clusters y clases, independientemente '
    'del número asignado a cada grupo.\n'
    'Single puede formar cadenas; complete favorece grupos compactos; '
    'average utiliza la distancia media entre grupos.\n'
    'Las clases reales no se usaron para entrenar ni cortar los dendrogramas.\n'
    'Las posiciones horizontales de las hojas no son necesariamente idénticas '
    'entre métodos, aunque se proporcionaron las mismas etiquetas.\n'
)
(SALIDA / '8_4_interpretacion.txt').write_text(texto, encoding='utf-8')
print('\n' + texto)
print(f'\nArchivos generados en: {SALIDA}')
