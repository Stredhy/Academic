"""Ejercicio 5: comparación SVM lineal y RBF en Phishing.
Coloca phishing.csv junto a este script. Python >=3.10.
"""
from pathlib import Path
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.base import clone
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.metrics import (accuracy_score, precision_score, recall_score, f1_score,
                             roc_auc_score, confusion_matrix, ConfusionMatrixDisplay)
from sklearn.model_selection import (train_test_split, GridSearchCV,
                                     StratifiedKFold)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'resultados_ejercicio5'
OUT.mkdir(exist_ok=True)
MOSTRAR_GRAFICAS = True
SEMILLA = 42
POSITIVA = 1  # Etiqueta positiva para precision, recall, F1 y ROC-AUC.


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(OUT / nombre, dpi=180, bbox_inches='tight')
    if MOSTRAR_GRAFICAS:
        plt.show()
    plt.close()


def guardar_tabla(tabla, nombre):
    tabla.to_csv(OUT / nombre, index=False, encoding='utf-8-sig')
    print(f'\n{nombre}\n{tabla.to_string(index=False)}')


# 5.1 Preparación: el CSV no tiene fila de encabezados.
datos = pd.read_csv(ROOT / 'phishing.csv', header=None)
if datos.shape[1] != 31:
    raise ValueError(f'Se esperaban 31 columnas, se encontraron {datos.shape[1]}')
columnas = [f'Feature_{i:02d}' for i in range(1, 31)]
datos.columns = columnas + ['Class']
datos[columnas] = datos[columnas].apply(pd.to_numeric, errors='coerce')
datos['Class'] = pd.to_numeric(datos['Class'], errors='raise')
if datos['Class'].isna().any() or set(datos['Class'].unique()) != {-1, 1}:
    raise ValueError('Se esperan clases -1 y 1, sin etiquetas faltantes.')

resumen = pd.DataFrame({
    'Variable': datos.columns,
    'Tipo': datos.dtypes.astype(str).values,
    'NaN': datos.isna().sum().values,
    'Porcentaje_NaN': (datos.isna().mean() * 100).round(3).values
})
guardar_tabla(resumen, '5_1_1_tipos_faltantes.csv')
conteos = datos['Class'].value_counts().sort_index()
tabla_clases = pd.DataFrame({
    'Class': conteos.index, 'Conteo': conteos.values,
    'Porcentaje': (100 * conteos.values / len(datos)).round(3)
})
guardar_tabla(tabla_clases, '5_1_1_clases.csv')
plt.figure(figsize=(7, 4))
plt.bar([str(c) for c in conteos.index], conteos.values)
plt.title('5.1.1 Distribución de clases')
plt.xlabel('Class (etiqueta original)')
plt.ylabel('Número de sitios')
for i, n in enumerate(conteos.values):
    plt.text(i, n + 50, f'{n:,} ({100*n/len(datos):.2f}%)', ha='center')
guardar_figura('5_1_1_distribucion.png')

X = datos[columnas]
y = datos['Class']
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.20, stratify=y, random_state=SEMILLA
)
# Reservar parte de training para interpretar sin utilizar testing.
X_subtrain, X_val, y_subtrain, y_val = train_test_split(
    X_train, y_train, test_size=0.20, stratify=y_train, random_state=SEMILLA
)
guardar_tabla(pd.DataFrame([
    {'Subconjunto': nombre, 'N': len(ys), 'Class_-1': int((ys == -1).sum()),
     'Class_1': int((ys == 1).sum())}
    for nombre, ys in [('Training', y_train), ('Validation_interpretacion', y_val),
                       ('Testing', y_test)]
]), '5_1_2_particiones.csv')


def crear_pipeline(kernel):
    return Pipeline([
        ('imputer', SimpleImputer(strategy='median')),
        ('scaler', StandardScaler()),
        ('svm', SVC(kernel=kernel, random_state=SEMILLA))
    ])

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA)
parametros = {
    'Lineal': {'svm__C': [0.1, 1, 10, 100]},
    'RBF': {'svm__C': [0.1, 1, 10, 100],
            'svm__gamma': [0.001, 0.01, 0.1, 1]}
}
modelos = {}
resultados_cv = []

# 5.2 Optimización únicamente en training, preprocesamiento dentro de cada fold.
for nombre, kernel in [('Lineal', 'linear'), ('RBF', 'rbf')]:
    print(f'\nEntrenando SVM {nombre}...')
    busqueda = GridSearchCV(
        crear_pipeline(kernel), parametros[nombre], scoring='roc_auc',
        cv=cv, refit=True, n_jobs=1, return_train_score=True
    )
    busqueda.fit(X_train, y_train)
    modelos[nombre] = busqueda.best_estimator_
    print(f'Mejores parámetros {nombre}: {busqueda.best_params_}')
    tabla = pd.DataFrame(busqueda.cv_results_)
    for _, fila in tabla.iterrows():
        resultados_cv.append({
            'Kernel': nombre,
            'C': fila['param_svm__C'],
            'gamma': fila.get('param_svm__gamma', 'No aplica'),
            'ROC_AUC_CV_media': fila['mean_test_score'],
            'ROC_AUC_CV_desv_est': fila['std_test_score'],
            'ROC_AUC_training_media': fila['mean_train_score'],
            'Ranking': fila['rank_test_score']
        })

tabla_cv = pd.DataFrame(resultados_cv)
guardar_tabla(tabla_cv, '5_2_3_combinaciones_cv.csv')

# 5.3.1 Sensibilidad de hiperparámetros.
lineal = tabla_cv[tabla_cv['Kernel'] == 'Lineal'].sort_values('C')
plt.figure(figsize=(7, 4))
plt.errorbar(lineal['C'], lineal['ROC_AUC_CV_media'],
             yerr=lineal['ROC_AUC_CV_desv_est'], marker='o', capsize=4)
plt.xscale('log')
plt.xlabel('C (escala logarítmica)')
plt.ylabel('ROC-AUC medio (5 folds)')
plt.title('5.3.1 SVM lineal: sensibilidad a C')
plt.grid(alpha=0.3)
guardar_figura('5_3_1_lineal_C.png')

rbf = tabla_cv[tabla_cv['Kernel'] == 'RBF'].copy()
matriz = rbf.pivot(index='C', columns='gamma', values='ROC_AUC_CV_media')
fig, ax = plt.subplots(figsize=(8, 5))
im = ax.imshow(matriz.values, aspect='auto', cmap='viridis')
ax.set_xticks(range(len(matriz.columns)), [str(v) for v in matriz.columns])
ax.set_yticks(range(len(matriz.index)), [str(v) for v in matriz.index])
ax.set_xlabel('gamma')
ax.set_ylabel('C')
ax.set_title('5.3.1 SVM RBF: ROC-AUC medio en CV')
for i in range(len(matriz.index)):
    for j in range(len(matriz.columns)):
        ax.text(j, i, f'{matriz.iloc[i, j]:.3f}', ha='center', va='center',
                color='white' if matriz.iloc[i, j] < matriz.values.mean() else 'black')
fig.colorbar(im, ax=ax, label='ROC-AUC')
guardar_figura('5_3_1_heatmap_rbf.png')

# 5.3.2 PCA se ajusta solo con training transformado; los SVM usan las 30 variables.
prepro = Pipeline([('imputer', SimpleImputer(strategy='median')),
                   ('scaler', StandardScaler())])
X_train_proc = prepro.fit_transform(X_train)
X_test_proc = prepro.transform(X_test)
pca = PCA(n_components=2, random_state=SEMILLA)
pca.fit(X_train_proc)
coords = pca.transform(X_test_proc)
fig, axes = plt.subplots(1, 3, figsize=(17, 5), sharex=True, sharey=True)
for ax, (nombre, etiquetas) in zip(axes, [
    ('Clase real', y_test.to_numpy()),
    ('SVM lineal', modelos['Lineal'].predict(X_test)),
    ('SVM RBF', modelos['RBF'].predict(X_test))
]):
    for clase, color in [(-1, 'tab:blue'), (1, 'tab:orange')]:
        mascara = etiquetas == clase
        ax.scatter(coords[mascara, 0], coords[mascara, 1], s=8, alpha=0.4,
                   c=color, label=f'Class {clase}')
    ax.set_title(nombre)
    ax.set_xlabel('PC1')
    ax.set_ylabel('PC2')
    ax.legend()
fig.suptitle('5.3.2 PCA de testing (visualización solamente; SVM usa 30 variables)')
guardar_figura('5_3_2_pca_real_predicho.png')

# 5.4.1 Importancia por permutación: validación derivada de training.
# Para no medir importancia sobre los datos usados en ajuste, reajustamos
# los mejores hiperparámetros sobre subtraining y evaluamos en validation.
metricas = []
for nombre, modelo in modelos.items():
    modelo_val = clone(modelo).fit(X_subtrain, y_subtrain)
    importancia = permutation_importance(
        modelo_val, X_val, y_val, scoring='roc_auc', n_repeats=10,
        random_state=SEMILLA, n_jobs=1
    )
    ranking = pd.DataFrame({
        'Variable': columnas,
        'Importancia_media': importancia.importances_mean,
        'Desviacion_estandar': importancia.importances_std
    }).sort_values('Importancia_media', ascending=False).head(10)
    guardar_tabla(ranking, f'5_4_1_importancia_{nombre.lower()}.csv')
    plt.figure(figsize=(9, 5))
    plt.barh(ranking['Variable'][::-1], ranking['Importancia_media'][::-1],
             xerr=ranking['Desviacion_estandar'][::-1])
    plt.xlabel('Reducción de ROC-AUC al permutar')
    plt.ylabel('Característica')
    plt.title(f'5.4.1 Permutation importance top-10: SVM {nombre} (validation)')
    guardar_figura(f'5_4_1_importancia_{nombre.lower()}.png')

    # Testing solo para evaluación final.
    pred = modelo.predict(X_test)
    score = modelo.decision_function(X_test)
    cm = confusion_matrix(y_test, pred, labels=[-1, 1])
    metricas.append({
        'Kernel': nombre,
        'Accuracy': accuracy_score(y_test, pred),
        'Precision': precision_score(y_test, pred, pos_label=POSITIVA),
        'Recall': recall_score(y_test, pred, pos_label=POSITIVA),
        'F1': f1_score(y_test, pred, pos_label=POSITIVA),
        'ROC_AUC': roc_auc_score((y_test == POSITIVA).astype(int), score),
        'TN': int(cm[0, 0]), 'FP': int(cm[0, 1]),
        'FN': int(cm[1, 0]), 'TP': int(cm[1, 1])
    })
    disp = ConfusionMatrixDisplay(cm, display_labels=['Class -1', 'Class 1'])
    disp.plot(cmap='Blues', values_format='d')
    plt.title(f'5.4.1 Matriz de confusión: SVM {nombre} (testing)')
    guardar_figura(f'5_4_1_confusion_{nombre.lower()}.png')

tabla_final = pd.DataFrame(metricas)
guardar_tabla(tabla_final, '5_4_1_comparacion_testing.csv')
mejor = tabla_final.loc[tabla_final['ROC_AUC'].idxmax()]
texto = (
    'Interpretación de resultados:\n'
    f'En testing, el mayor ROC-AUC fue el de SVM {mejor.Kernel} '
    f'({mejor.ROC_AUC:.4f}).\n'
    'Las diferencias entre C y gamma en la tabla CV muestran la sensibilidad '\
    'del ajuste y su capacidad de generalización.\n'
    'Las importancias por permutación se calcularon sobre validation, '\
    'no sobre testing.\n'
    'PCA sirve solo para representar los datos en dos dimensiones; '\
    'los clasificadores fueron entrenados con las 30 variables.\n'
    'Class=1 es la clase positiva usada en precision, recall, F1 y ROC-AUC.\n'
    'Como el archivo no incluye nombres descriptivos, las importancias '\
    'se identifican por posición de columna y no por concepto clínico o web.\n'
)
(OUT / '5_4_1_interpretacion.txt').write_text(texto, encoding='utf-8')
print('\n' + texto)
print(f'Archivos guardados en: {OUT}')
