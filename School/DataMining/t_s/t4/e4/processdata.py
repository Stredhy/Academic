"""Ejercicio 4: K-means frente a clases conocidas (Dry Bean Dataset).

Instalar: python -m pip install pandas numpy matplotlib scikit-learn
Ejecutar: python ejercicio4_dry_bean.py
Colocar Dry_Bean.csv junto a este archivo.
"""
from pathlib import Path
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.metrics import adjusted_rand_score, normalized_mutual_info_score
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parent
SALIDA = ROOT / 'resultados_ejercicio4'
SALIDA.mkdir(exist_ok=True)
MOSTRAR_GRAFICAS = True  # Cambiar a False para solo guardar las figuras.


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(SALIDA / nombre, dpi=200, bbox_inches='tight')
    if MOSTRAR_GRAFICAS:
        plt.show()
    plt.close()


def guardar_tabla(tabla, nombre):
    tabla.to_csv(SALIDA / nombre, index=False, encoding='utf-8-sig')
    print(f'\n{nombre}\n{tabla.to_string(index=False)}')


def main():
    # 4.1.1: Estadísticas descriptivas y distribución de variedades.
    df = pd.read_csv(ROOT / 'Dry_Bean.csv')
    if 'Class' not in df.columns:
        raise ValueError('El archivo debe contener la columna Class.')

    X = df.drop(columns='Class').copy()
    y = df['Class'].astype(str)
    X = X.apply(pd.to_numeric, errors='coerce')
    if X.shape[1] != 16:
        raise ValueError(f'Se esperaban 16 características, se encontraron {X.shape[1]}.')

    estadisticas = pd.DataFrame({
        'Caracteristica': X.columns,
        'Media': X.mean().values,
        'Desviacion_estandar': X.std().values,
    })
    guardar_tabla(estadisticas.round(6), '4_1_1_estadisticas.csv')

    conteos = y.value_counts().sort_index()
    clases = pd.DataFrame({
        'Variedad': conteos.index,
        'Conteo': conteos.values,
        'Porcentaje': (conteos.values / len(y) * 100).round(2),
    })
    guardar_tabla(clases, '4_1_1_variedades.csv')

    plt.figure(figsize=(10, 5))
    barras = plt.bar(clases['Variedad'], clases['Conteo'])
    plt.bar_label(barras, padding=3)
    plt.title('4.1.1 - Distribución de las siete variedades')
    plt.xlabel('Variedad real')
    plt.ylabel('Número de semillas')
    plt.xticks(rotation=30)
    guardar_figura('4_1_1_distribucion_variedades.png')

    # 4.1.2 y 4.1.3: Imputación y escalamiento sin usar Class.
    faltantes = pd.DataFrame({
        'Caracteristica': X.columns,
        'NaN': X.isna().sum().values,
        'Porcentaje_NaN': (X.isna().mean().values * 100).round(4),
    })
    guardar_tabla(faltantes, '4_1_2_faltantes.csv')
    imputador = SimpleImputer(strategy='median')
    escalador = StandardScaler()
    X_imputado = imputador.fit_transform(X)
    X_escalado = escalador.fit_transform(X_imputado)

    # 4.2.1: Entrenar K-means con exactamente siete clusters.
    kmeans = KMeans(n_clusters=7, random_state=42, n_init=10)
    clusters = kmeans.fit_predict(X_escalado)

    # 4.2.2 y 4.2.3: Tabla cruzada y clase mayoritaria de cada cluster.
    cruzada = pd.crosstab(
        pd.Series(clusters, name='Cluster'),
        y.reset_index(drop=True).rename('Variedad'),
    ).reindex(index=range(7), columns=sorted(y.unique()), fill_value=0)
    cruzada.to_csv(SALIDA / '4_2_3_cluster_por_variedad.csv', encoding='utf-8-sig')
    print('\n4.2.3 - Tabla cruzada cluster × variedad:\n', cruzada)

    resumen = pd.DataFrame({
        'Cluster': cruzada.index,
        'Tamano': cruzada.sum(axis=1).values,
        'Variedad_dominante': cruzada.idxmax(axis=1).values,
        'Porcentaje_dominante': (
            cruzada.max(axis=1) / cruzada.sum(axis=1) * 100
        ).round(2).values,
    })
    guardar_tabla(resumen, '4_2_2_resumen_clusters.csv')
    guardar_tabla(
        resumen[['Cluster', 'Variedad_dominante', 'Porcentaje_dominante']],
        '4_3_1_correspondencia_mayoritaria.csv',
    )
    print('\n4.3.1 - Cada cluster se asigna a su variedad más frecuente.')
    print('Dos clusters pueden tener la misma variedad dominante porque la asignación')
    print('se calcula independientemente para cada cluster, sin imponer unicidad.')

    # 4.4.1: PCA ajustado una sola vez sobre las características estandarizadas.
    pca = PCA(n_components=2)
    puntos = pca.fit_transform(X_escalado)
    variedades = sorted(y.unique())
    fig, ejes = plt.subplots(1, 2, figsize=(15, 6), sharex=True, sharey=True)
    for i, variedad in enumerate(variedades):
        mascara = y.to_numpy() == variedad
        ejes[0].scatter(puntos[mascara, 0], puntos[mascara, 1],
                        s=4, alpha=0.45, label=variedad)
    for cluster in range(7):
        mascara = clusters == cluster
        ejes[1].scatter(puntos[mascara, 0], puntos[mascara, 1],
                        s=4, alpha=0.45, label=f'Cluster {cluster}')
    for eje, titulo in zip(ejes, ['Variedad real (Class)', 'Clusters K-means']):
        eje.set_title(titulo)
        eje.set_xlabel('PC1')
        eje.set_ylabel('PC2')
        eje.legend(markerscale=3, fontsize=8)
    fig.suptitle('4.4.1 - PCA: clases conocidas frente a agrupamiento K-means')
    guardar_figura('4_4_1_pca_dos_paneles.png')

    # 4.4.2: Métricas externas y confusiones concretas.
    ari = adjusted_rand_score(y, clusters)
    nmi = normalized_mutual_info_score(y, clusters)
    metricas = pd.DataFrame({'Metrica': ['ARI', 'NMI'], 'Valor': [ari, nmi]})
    guardar_tabla(metricas.round(6), '4_4_2_metricas.csv')

    confusiones = []
    for cluster, fila in cruzada.iterrows():
        dominante = fila.idxmax()
        for variedad, cantidad in fila.items():
            if variedad != dominante and cantidad > 0:
                confusiones.append((cantidad, cluster, variedad, dominante))
    confusiones.sort(reverse=True)
    interpretacion = [
        '4.4.2 - Interpretación de resultados',
        f'ARI = {ari:.4f}; NMI = {nmi:.4f}.',
        'ARI compara pares de observaciones corrigiendo por coincidencias al azar;',
        'NMI mide información compartida entre clusters y clases reales.',
        'Los clusters no son clases: K-means agrupa por similitud geométrica.',
    ]
    for cantidad, cluster, variedad, dominante in confusiones[:2]:
        interpretacion.append(
            f'Confusión: {cantidad} semillas {variedad} aparecen en el cluster {cluster}, '
            f'cuya variedad dominante es {dominante}.'
        )
    texto = '\n'.join(interpretacion)
    print('\n' + texto)
    (SALIDA / '4_4_2_interpretacion.txt').write_text(texto, encoding='utf-8')
    print(f'\nResultados guardados en: {SALIDA}')


if __name__ == '__main__':
    main()
