"""Ejercicio 10: PCA y clasificación. Ejecutar: python ejercicio10_pca.py"""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, confusion_matrix, ConfusionMatrixDisplay

BASE = Path(__file__).resolve().parent
OUT = BASE / 'resultados_ejercicio10'
OUT.mkdir(exist_ok=True)
MOSTRAR = os.environ.get('MOSTRAR_GRAFICAS', '1') == '1'
SEED = 42

def guardar(nombre):
    plt.tight_layout()
    plt.savefig(OUT / nombre, dpi=180, bbox_inches='tight')
    if MOSTRAR:
        plt.show()
    plt.close()

def main():
    # 10.1.1: excluir el índice artificial y separar etiqueta binaria.
    df = pd.read_csv(BASE / 'brca.csv')
    cols = [c for c in df.columns if c.startswith('x.')]
    assert len(cols) == 30, 'Se esperaban exactamente 30 variables predictoras.'
    assert set(df['y'].dropna().unique()) == {'B', 'M'}, 'Etiquetas inesperadas.'
    X = df[cols].copy()
    y = (df['y'] == 'M').astype(int)  # Maligno = 1 (clase positiva).
    print('10.1.1 Dimensiones:', X.shape, ' | Distribución:', y.value_counts().to_dict())
    pd.DataFrame({'medida': ['filas', 'variables', 'clases', 'faltantes'],
                  'valor': [len(df), len(cols), y.nunique(), int(X.isna().sum().sum())]}).to_csv(
        OUT / '10_1_1_dimensiones.csv', index=False)
    clases = pd.DataFrame({'diagnostico': ['Benigno (B)', 'Maligno (M)'],
                           'conteo': [(y == 0).sum(), (y == 1).sum()]})
    clases.to_csv(OUT / '10_1_1_clases.csv', index=False)
    plt.figure(figsize=(6, 4))
    plt.bar(clases['diagnostico'], clases['conteo'])
    plt.ylabel('Número de pacientes'); plt.title('Distribución de diagnósticos')
    guardar('10_1_1_clases.png')
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=SEED)
    print('Training:', X_train.shape, 'Testing:', X_test.shape)

    # 10.1.2–10.1.4: ajustes exclusivamente en training.
    scaler = StandardScaler().fit(X_train)
    Z_train = scaler.transform(X_train)
    Z_test = scaler.transform(X_test)
    pca30 = PCA(n_components=30).fit(Z_train)
    pca15 = PCA(n_components=15).fit(Z_train)
    T30_train, T30_test = pca30.transform(Z_train), pca30.transform(Z_test)
    T15_train, T15_test = pca15.transform(Z_train), pca15.transform(Z_test)
    pd.DataFrame({'variable': cols, 'media_training': scaler.mean_,
                  'desviacion_training': scaler.scale_}).to_csv(
        OUT / '10_1_2_escalamiento_training.csv', index=False)
    print('PCA30:', T30_train.shape, T30_test.shape,
          '| PCA15:', T15_train.shape, T15_test.shape)

    # 10.2.1: mismo clasificador y folds para todas las representaciones.
    # Se usa regresión logística sin penalización para aislar el efecto de PCA.
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    modelos = {
        'Originales (30)': Pipeline([
            ('escalado', StandardScaler()),
            ('clasificador', LogisticRegression(penalty=None, max_iter=3000, random_state=SEED))]),
        'PCA (30)': Pipeline([
            ('escalado', StandardScaler()), ('pca', PCA(n_components=30)),
            ('clasificador', LogisticRegression(penalty=None, max_iter=3000, random_state=SEED))]),
        'PCA (15)': Pipeline([
            ('escalado', StandardScaler()), ('pca', PCA(n_components=15)),
            ('clasificador', LogisticRegression(penalty=None, max_iter=3000, random_state=SEED))])
    }
    # 10.2.2: varianza explicada de PCA ajustado únicamente con training.
    var = pd.DataFrame({'componente': np.arange(1, 31),
                        'varianza_explicada': pca30.explained_variance_ratio_,
                        'varianza_acumulada': np.cumsum(pca30.explained_variance_ratio_)})
    var.to_csv(OUT / '10_2_2_varianza_componentes.csv', index=False)
    ret = pd.DataFrame({'representacion': ['Originales (30)', 'PCA (30)', 'PCA (15)'],
                        'componentes': [30, 30, 15],
                        'varianza_retenida': [1.0, pca30.explained_variance_ratio_.sum(),
                                             pca15.explained_variance_ratio_.sum()]})
    ret.to_csv(OUT / '10_2_2_varianza_retenida.csv', index=False)
    plt.figure(figsize=(8, 5))
    plt.plot(var['componente'], var['varianza_acumulada'], marker='o', markersize=3)
    plt.axvline(15, linestyle='--', label='15 componentes')
    plt.xlabel('Número de componentes'); plt.ylabel('Varianza acumulada')
    plt.ylim(0, 1.03); plt.grid(alpha=.3); plt.legend()
    plt.title('PCA: varianza explicada acumulada')
    guardar('10_2_2_varianza_acumulada.png')

    # 10.3.1: CV sobre training, evaluación final única sobre testing.
    resultados = []
    for nombre, pipeline in modelos.items():
        print('Evaluando:', nombre, flush=True)
        cv_result = cross_validate(pipeline, X_train, y_train, cv=cv,
                                   scoring={'accuracy': 'accuracy', 'f1': 'f1',
                                            'roc_auc': 'roc_auc'}, n_jobs=1)
        pipeline.fit(X_train, y_train)
        pred = pipeline.predict(X_test)
        prob = pipeline.predict_proba(X_test)[:, 1]
        fila = {'representacion': nombre}
        for metrica in ('accuracy', 'f1', 'roc_auc'):
            valores = cv_result['test_' + metrica]
            fila[f'{metrica}_cv_media'] = valores.mean()
            fila[f'{metrica}_cv_de'] = valores.std(ddof=1)
        fila.update({'accuracy_test': accuracy_score(y_test, pred),
                     'f1_test': f1_score(y_test, pred),
                     'roc_auc_test': roc_auc_score(y_test, prob)})
        resultados.append(fila)
        matriz = confusion_matrix(y_test, pred, labels=[0, 1])
        pd.DataFrame(matriz, index=['Real_B', 'Real_M'],
                     columns=['Pred_B', 'Pred_M']).to_csv(
            OUT / ('10_3_1_matriz_' + nombre.replace(' ', '_').replace('(', '').replace(')', '') + '.csv'))
        disp = ConfusionMatrixDisplay(matriz, display_labels=['Benigno', 'Maligno'])
        disp.plot(cmap='Blues', values_format='d', colorbar=False)
        plt.title('Matriz de confusión: ' + nombre)
        guardar('10_3_1_matriz_' + nombre.replace(' ', '_').replace('(', '').replace(')', '') + '.png')
    tabla = pd.DataFrame(resultados)
    tabla.to_csv(OUT / '10_3_1_comparacion_metricas.csv', index=False)
    print('\n10.3.1 Comparación:\n', tabla.round(4).to_string(index=False))

    # 10.4.1: loadings PC1-PC5 y reconstrucción en espacio estandarizado.
    loadings = pd.DataFrame(pca30.components_[:5].T, index=cols,
                            columns=[f'PC{i}' for i in range(1, 6)])
    loadings.to_csv(OUT / '10_4_1_loadings.csv', index_label='variable')
    plt.figure(figsize=(10, 9))
    plt.imshow(loadings.values, cmap='coolwarm', aspect='auto',
               vmin=-np.abs(loadings.values).max(), vmax=np.abs(loadings.values).max())
    plt.colorbar(label='Coeficiente (loading)')
    plt.yticks(range(30), cols, fontsize=8)
    plt.xticks(range(5), loadings.columns)
    plt.title('Loadings PCA: variables × PC1–PC5')
    guardar('10_4_1_heatmap_loadings.png')

    Z_rec = pca15.inverse_transform(T15_test)
    errores = np.mean((Z_test - Z_rec) ** 2, axis=1)
    mse = float(np.mean(errores))
    pd.DataFrame({'medida': ['MSE_promedio_testing_estandarizado'],
                  'valor': [mse]}).to_csv(OUT / '10_4_1_mse_reconstruccion.csv', index=False)
    ejemplos = np.argsort(errores)[[0, len(errores)//2, -1]]
    detalles = []
    for etiqueta, pos in zip(['error_bajo', 'error_intermedio', 'error_alto'], ejemplos):
        detalles.append({'ejemplo': etiqueta, 'indice_original': X_test.index[pos],
                         'clase': 'M' if y_test.iloc[pos] else 'B',
                         'mse_individual': errores[pos]})
    pd.DataFrame(detalles).to_csv(OUT / '10_4_1_tres_ejemplos.csv', index=False)
    plt.figure(figsize=(11, 5))
    for etiqueta, pos in zip(['Bajo', 'Intermedio', 'Alto'], ejemplos):
        plt.plot(np.arange(1, 31), np.abs(Z_test[pos] - Z_rec[pos]),
                 marker='.', alpha=.8, label=f'{etiqueta} (MSE={errores[pos]:.4f})')
    plt.xlabel('Variable (1–30)'); plt.ylabel('Error absoluto estandarizado')
    plt.title('Tres ejemplos: error de reconstrucción PCA(15)')
    plt.legend(); plt.grid(alpha=.2)
    guardar('10_4_1_tres_ejemplos.png')
    print(f'\n10.4.1 MSE medio de reconstrucción en test: {mse:.6f}')
    print('Archivos guardados en:', OUT)

if __name__ == '__main__':
    main()
