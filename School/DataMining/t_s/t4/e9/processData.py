"""Ejercicio 9: PCA frente a t-SNE con Dry Bean Dataset.
Ejecutar: python ejercicio9_pca_tsne.py
"""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE

ROOT = Path(__file__).resolve().parent
INPUT = ROOT / 'Dry_Bean_Dataset.xlsx'
OUT = ROOT / 'ejercicio9_resultados'
OUT.mkdir(exist_ok=True)
SHOW_PLOTS = os.environ.get('SHOW_PLOTS', '1') == '1'
RANDOM_STATE = 42


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(OUT / nombre, dpi=180, bbox_inches='tight')
    if SHOW_PLOTS:
        plt.show()
    plt.close()


def scatter_clases(ax, coords, etiquetas, clases, titulo, alpha=0.5):
    for clase in clases:
        mascara = (etiquetas == clase).to_numpy()
        ax.scatter(coords[mascara, 0], coords[mascara, 1],
                   label=clase, s=8, alpha=alpha, rasterized=True)
    ax.set_title(titulo)
    ax.set_xlabel('Componente 1')
    ax.set_ylabel('Componente 2')
    ax.grid(alpha=0.15)


def main():
    # 9.1.1 Exploración: dimensiones, estadísticos, distribución y NaN
    df = pd.read_excel(INPUT)
    if 'Class' not in df:
        raise ValueError('El archivo debe contener la columna Class.')
    y = df['Class'].astype(str)
    X = df.drop(columns='Class').apply(pd.to_numeric, errors='coerce')
    if X.shape[1] != 16:
        raise ValueError(f'Se esperaban 16 características, hay {X.shape[1]}.')
    clases = sorted(y.unique())
    resumen = pd.DataFrame([{'filas': len(df), 'columnas': len(df.columns),
                             'caracteristicas': X.shape[1], 'clases': len(clases),
                             'NaN_total': int(X.isna().sum().sum())}])
    resumen.to_csv(OUT / '9_1_1_dimensiones.csv', index=False)
    estadisticos = X.agg(['count', 'mean', 'std', 'min', 'median', 'max']).T
    estadisticos['NaN'] = X.isna().sum()
    estadisticos.to_csv(OUT / '9_1_1_estadisticos.csv', index_label='variable')
    distribucion = y.value_counts().rename_axis('variedad').reset_index(name='conteo')
    distribucion['porcentaje'] = 100 * distribucion['conteo'] / len(y)
    distribucion.to_csv(OUT / '9_1_1_variedades.csv', index=False)
    fig, ax = plt.subplots(figsize=(10, 5))
    bars = ax.bar(distribucion['variedad'], distribucion['conteo'])
    for bar, pct in zip(bars, distribucion['porcentaje']):
        ax.text(bar.get_x() + bar.get_width()/2, bar.get_height()+25,
                f'{pct:.1f}%', ha='center', fontsize=9)
    ax.set_title('9.1.1 Distribución de las siete variedades')
    ax.set_xlabel('Variedad')
    ax.set_ylabel('Cantidad de semillas')
    guardar_figura('9_1_1_distribucion.png')

    # 9.1.2 Imputación y estandarización sin usar Class
    imputer = SimpleImputer(strategy='median')
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(imputer.fit_transform(X))

    # 9.2.1 PCA, varianza explicada y loadings
    pca = PCA(random_state=RANDOM_STATE)
    X_pca = pca.fit_transform(X_scaled)
    explained = pca.explained_variance_ratio_
    pd.DataFrame({'PC': np.arange(1, len(explained)+1),
                  'varianza_explicada': explained,
                  'varianza_acumulada': np.cumsum(explained)}).to_csv(
                      OUT / '9_2_1_varianza.csv', index=False)
    loadings = pd.DataFrame(pca.components_[:5].T,
                            index=X.columns,
                            columns=[f'PC{i}' for i in range(1, 6)])
    loadings.to_csv(OUT / '9_2_1_loadings.csv', index_label='variable')
    tops = []
    for pc in ['PC1', 'PC2']:
        for variable, valor in loadings[pc].abs().nlargest(5).items():
            tops.append({'componente': pc, 'variable': variable,
                         'loading': loadings.loc[variable, pc],
                         'valor_absoluto': valor})
    pd.DataFrame(tops).to_csv(OUT / '9_2_1_top5_loadings.csv', index=False)

    fig, ax = plt.subplots(figsize=(10, 7))
    scatter_clases(ax, X_pca[:, :2], y, clases, '9.2 PCA: variedades reales')
    ax.set_xlabel(f'PC1 ({explained[0]*100:.2f}% de varianza)')
    ax.set_ylabel(f'PC2 ({explained[1]*100:.2f}% de varianza)')
    ax.legend(title='Variedad', markerscale=3, bbox_to_anchor=(1.01, 1), loc='upper left')
    guardar_figura('9_2_1_pca_scatter.png')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.bar(np.arange(1, 17), explained * 100)
    ax.set_xticks(np.arange(1, 17))
    ax.set_xlabel('Componente principal')
    ax.set_ylabel('Varianza explicada (%)')
    ax.set_title('9.2 Scree plot de PCA')
    guardar_figura('9_2_1_scree.png')

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.plot(np.arange(1, 17), np.cumsum(explained)*100, marker='o')
    ax.axhline(90, color='gray', linestyle='--', label='90%')
    ax.set_xticks(np.arange(1, 17))
    ax.set_xlabel('Número de componentes')
    ax.set_ylabel('Varianza acumulada (%)')
    ax.set_title('9.2 Varianza explicada acumulada')
    ax.legend()
    guardar_figura('9_2_1_varianza_acumulada.png')

    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(loadings.values, cmap='coolwarm', vmin=-1, vmax=1, aspect='auto')
    ax.set_yticks(np.arange(len(X.columns)), X.columns)
    ax.set_xticks(np.arange(5), loadings.columns)
    ax.set_xlabel('Componente principal')
    ax.set_ylabel('Característica')
    ax.set_title('9.2 Loadings PCA (PC1–PC5)')
    fig.colorbar(im, ax=ax, label='Loading')
    guardar_figura('9_2_1_heatmap_loadings.png')

    # 9.3.1 t-SNE sobre exactamente los mismos datos estandarizados
    # Los resultados de t-SNE no deben compararse por distancia global.
    for perplexity in [5, 30, 50]:
        print(f'Calculando t-SNE perplexity={perplexity}...', flush=True)
        tsne = TSNE(n_components=2, perplexity=perplexity,
                    random_state=RANDOM_STATE, init='pca',
                    learning_rate='auto', method='barnes_hut')
        coords = tsne.fit_transform(X_scaled)
        pd.DataFrame({'TSNE1': coords[:, 0], 'TSNE2': coords[:, 1],
                      'Class': y}).to_csv(
                          OUT / f'9_3_1_tsne_{perplexity}_coordenadas.csv', index=False)
        fig, ax = plt.subplots(figsize=(10, 7))
        scatter_clases(ax, coords, y, clases,
                       f'9.3 t-SNE: perplexity={perplexity}')
        ax.set_xlabel('t-SNE dimensión 1')
        ax.set_ylabel('t-SNE dimensión 2')
        ax.legend(title='Variedad', markerscale=3,
                  bbox_to_anchor=(1.01, 1), loc='upper left')
        guardar_figura(f'9_3_1_tsne_{perplexity}.png')

    # 9.4 Comparación e interpretación
    comparacion = pd.DataFrame([
        {'metodo': 'PCA', 'interpretabilidad_ejes': 'Alta: combinaciones lineales y loadings',
         'estructura': 'Maximiza varianza global proyectada',
         'distancias': 'Distancias proyectadas en escala lineal; hay pérdida de información'},
        {'metodo': 't-SNE', 'interpretabilidad_ejes': 'Baja: ejes sin significado físico directo',
         'estructura': 'Prioriza vecindades locales',
         'distancias': 'No interpretar distancias globales ni tamaños de grupos como PCA'}
    ])
    comparacion.to_csv(OUT / '9_4_1_comparacion.csv', index=False)
    with open(OUT / '9_4_2_interpretacion.txt', 'w', encoding='utf-8') as f:
        f.write('PCA conserva direcciones lineales de máxima varianza y permite identificar '
                'las variables que contribuyen a PC1 y PC2 mediante loadings.\n'
                't-SNE busca mantener vecindades locales y puede separar visualmente grupos '
                'que se superponen en PCA, aunque la forma de sus islas depende de perplexity.\n'
                'Comparar las figuras para identificar dos variedades con distinto grado de '
                'solapamiento y cómo cambian al variar perplexity.\n'
                'Las distancias entre islas, sus tamaños y la separación global en t-SNE '
                'NO equivalen a distancias en PCA ni prueban clases naturalmente separadas.\n'
                f'PC1 explica {explained[0]*100:.2f}% y PC2 {explained[1]*100:.2f}% '
                f'(total {sum(explained[:2])*100:.2f}%).\n')
    print('Resultados guardados en:', OUT)


if __name__ == '__main__':
    main()
