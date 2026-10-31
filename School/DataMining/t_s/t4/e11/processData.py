"""Ejercicio 11: Tratamiento de NaN en Titanic (apartados 11.1–11.4).

Ejecutar: python ejercicio11_titanic.py
Requiere: pandas, numpy, matplotlib, scikit-learn
Las figuras se muestran por defecto; MOSTRAR_GRAFICAS=0 las guarda sin abrir ventanas.
"""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer, KNNImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, f1_score, roc_auc_score,
                             confusion_matrix, ConfusionMatrixDisplay)
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_validate
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

SEMILLA = 42
BASE = Path(__file__).resolve().parent
ARCHIVO = BASE / 'train.csv'
SALIDA = BASE / 'resultados_ejercicio11'
SALIDA.mkdir(exist_ok=True)
MOSTRAR = os.environ.get('MOSTRAR_GRAFICAS', '1') == '1'


def guardar(nombre):
    plt.tight_layout()
    plt.savefig(SALIDA / nombre, dpi=160, bbox_inches='tight')
    if MOSTRAR:
        plt.show()
    plt.close()


def construir_pipeline(metodo, k=None):
    """Preprocesamiento dentro de Pipeline: cada fold aprende solo de su training."""
    if metodo == 'Eliminar columnas con NaN':
        numericas = ['Pclass', 'SibSp', 'Parch', 'Fare']
        categoricas = ['Sex']
    else:
        numericas = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
        categoricas = ['Sex', 'Embarked']

    if metodo.startswith('KNN'):
        # La escala se aprende en training ANTES de calcular las distancias KNN.
        proc_num = Pipeline([
            ('escala_pre_knn', StandardScaler()),
            ('imputacion', KNNImputer(n_neighbors=k, weights='uniform')),
        ])
    else:
        estrategia = 'median' if metodo == 'Mediana' else 'mean'
        proc_num = Pipeline([
            ('imputacion', SimpleImputer(strategy=estrategia)),
            ('escala', StandardScaler()),
        ])
    proc_cat = Pipeline([
        ('imputacion', SimpleImputer(strategy='most_frequent')),
        ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
    ])
    preprocesador = ColumnTransformer([
        ('numericas', proc_num, numericas),
        ('categoricas', proc_cat, categoricas),
    ], remainder='drop')
    return Pipeline([
        ('preprocesamiento', preprocesador),
        ('clasificador', LogisticRegression(max_iter=2000, solver='lbfgs', C=1.0,
                                            random_state=SEMILLA)),
    ])


def main():
    datos = pd.read_csv(ARCHIVO)
    print('11.1 Exploración:', datos.shape)
    assert 'Survived' in datos.columns
    faltantes = pd.DataFrame({
        'columna': datos.columns,
        'NaN': datos.isna().sum().values,
        'porcentaje_NaN': (datos.isna().mean().values * 100).round(2),
    })
    faltantes.to_csv(SALIDA / '11_1_1_faltantes.csv', index=False)
    datos['Survived'].value_counts().sort_index().rename_axis('Survived').reset_index(name='pasajeros').to_csv(
        SALIDA / '11_1_1_clases.csv', index=False)
    pd.DataFrame([{'filas': len(datos), 'columnas': len(datos),
                   'supervivientes': int(datos.Survived.sum()),
                   'no_supervivientes': int((datos.Survived == 0).sum())}]).to_csv(
        SALIDA / '11_1_1_dimensiones.csv', index=False)

    fig, ax = plt.subplots(figsize=(12, 5))
    matriz = datos.isna().to_numpy().T.astype(int)
    ax.imshow(matriz, aspect='auto', interpolation='nearest', cmap='Greys', vmin=0, vmax=1)
    ax.set_yticks(range(len(datos.columns)), datos.columns)
    ax.set_xlabel('Índice del pasajero')
    ax.set_title('11.1.2 Mapa de NaN (oscuro = faltante)')
    guardar('11_1_2_mapa_NaN.png')

    fig, axes = plt.subplots(1, 2, figsize=(11, 4))
    for ax, col in zip(axes, ['Age', 'Fare']):
        ax.hist(datos[col].dropna(), bins=25, edgecolor='white')
        ax.set_title(f'{col} original (NaN excluidos)')
        ax.set_xlabel(col)
        ax.set_ylabel('Frecuencia')
    guardar('11_1_2_histogramas_age_fare.png')

    # 11.1.3 División antes de ajustar cualquier transformación.
    X = datos.drop(columns='Survived')
    y = datos['Survived']
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=SEMILLA)
    print('Training:', len(X_train), 'Testing:', len(X_test))

    # Se excluyen identificadores y columnas de texto de cardinalidad alta para
    # mantener una comparación razonable. Cabin tiene 77 % de NaN y se excluye
    # de todas las estrategias. En eliminación también se retiran Age y Embarked.
    print('Excluidas en todos los métodos: PassengerId, Name, Ticket, Cabin.')
    print('Eliminación: además se excluyen Age y Embarked (contienen NaN).')
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEMILLA)
    metodos = [('Eliminar columnas con NaN', None), ('Media', None),
               ('Mediana', None), ('KNN k=2', 2), ('KNN k=5', 5), ('KNN k=10', 10)]
    filas_cv = []
    for metodo, k in metodos:
        print('CV:', metodo, flush=True)
        modelo = construir_pipeline(metodo, k)
        resultado = cross_validate(modelo, X_train, y_train, cv=cv,
                                   scoring={'accuracy': 'accuracy', 'f1': 'f1',
                                            'roc_auc': 'roc_auc'}, n_jobs=1)
        filas_cv.append({'metodo': metodo, 'k': k,
                         **{f'cv_{metrica}_{estadistico}': float(getattr(np, estadistico)(resultado['test_' + metrica], ddof=1))
                            if estadistico == 'std' else float(np.mean(resultado['test_' + metrica]))
                            for metrica in ['accuracy', 'f1', 'roc_auc']
                            for estadistico in ['mean', 'std']}})
    tabla_cv = pd.DataFrame(filas_cv)
    tabla_cv.to_csv(SALIDA / '11_2_1_validacion_cruzada.csv', index=False)
    knn_cv = tabla_cv[tabla_cv.metodo.str.startswith('KNN')].sort_values(
        ['cv_roc_auc_mean', 'cv_f1_mean'], ascending=False)
    mejor_knn = str(knn_cv.iloc[0]['metodo'])
    print('Mejor KNN por CV ROC-AUC:', mejor_knn)

    # 11.2.4 Evaluación del mismo testing para todos los métodos.
    filas_test = []
    predicciones = {}
    for metodo, k in metodos:
        modelo = construir_pipeline(metodo, k)
        modelo.fit(X_train, y_train)
        pred = modelo.predict(X_test)
        prob = modelo.predict_proba(X_test)[:, 1]
        predicciones[metodo] = pred
        columnas_transformadas = modelo.named_steps['preprocesamiento'].get_feature_names_out()
        filas_test.append({
            'metodo': metodo,
            'accuracy_test': accuracy_score(y_test, pred),
            'f1_test': f1_score(y_test, pred, zero_division=0),
            'roc_auc_test': roc_auc_score(y_test, prob),
            'numero_variables_finales': len(columnas_transformadas),
            'porcentaje_filas_aprovechadas': 100.0,
            'numero_filas_training': len(X_train),
            'numero_filas_testing': len(X_test),
        })
    tabla_test = pd.DataFrame(filas_test)
    tabla_final = tabla_cv.merge(tabla_test, on='metodo')
    tabla_final['seleccionado_entre_KNN'] = tabla_final.metodo.eq(mejor_knn)
    tabla_final.to_csv(SALIDA / '11_4_1_comparacion_completa.csv', index=False)
    # Elegir por CV, no por el resultado de testing.
    elegibles = tabla_cv[~tabla_cv.metodo.str.startswith('KNN') |
                        tabla_cv.metodo.eq(mejor_knn)]
    mejor = str(elegibles.sort_values(['cv_roc_auc_mean', 'cv_f1_mean'],
                                      ascending=False).iloc[0]['metodo'])
    print('Mejor estrategia seleccionada por CV:', mejor)
    cm = confusion_matrix(y_test, predicciones[mejor], labels=[0, 1])
    pd.DataFrame(cm, index=['Real 0', 'Real 1'],
                 columns=['Predicho 0', 'Predicho 1']).to_csv(
        SALIDA / '11_4_1_matriz_confusion.csv')
    ConfusionMatrixDisplay(cm, display_labels=['No sobrevivió', 'Sobrevivió']).plot(
        cmap='Blues', values_format='d')
    plt.title(f'11.4.1 Matriz de confusión: {mejor}')
    guardar('11_4_1_matriz_confusion.png')

    # 11.3: edades faltantes del training, nunca del testing.
    edad = X_train['Age'].copy()
    imputados = {'Media': SimpleImputer(strategy='mean').fit_transform(
        X_train[['Age']]).ravel(),
        'Mediana': SimpleImputer(strategy='median').fit_transform(
            X_train[['Age']]).ravel()}
    for k in [2, 5, 10]:
        # Mismas cinco variables numéricas y mismo orden que en el pipeline.
        columnas = ['Pclass', 'Age', 'SibSp', 'Parch', 'Fare']
        esc = StandardScaler().fit(X_train[columnas])
        escalados = esc.transform(X_train[columnas])
        imputados_escalados = KNNImputer(n_neighbors=k).fit_transform(escalados)
        imputados[f'KNN k={k}'] = esc.inverse_transform(imputados_escalados)[:, 1]

    fig, axes = plt.subplots(2, 3, figsize=(14, 8), sharex=True, sharey=True)
    for ax, (titulo, valores) in zip(axes.flat, [('Original (sin NaN)', edad.dropna())] +
                                     list(imputados.items())):
        ax.hist(valores, bins=np.arange(0, 85, 5), edgecolor='white')
        ax.set_title(titulo)
        ax.set_xlabel('Edad (años)')
        ax.set_ylabel('Frecuencia')
    guardar('11_3_1_age_antes_despues.png')

    indices = edad[edad.isna()].index[:5]
    ejemplos = pd.DataFrame({'PassengerId': X_train.loc[indices, 'PassengerId'],
                             'Age_original': edad.loc[indices]})
    posiciones = X_train.index.get_indexer(indices)
    for titulo, valores in imputados.items():
        ejemplos[f'Age_{titulo}'] = np.asarray(valores)[posiciones].round(2)
    ejemplos['Age_eliminar_columna'] = 'No disponible (columna excluida)'
    ejemplos.to_csv(SALIDA / '11_3_1_cinco_ejemplos.csv', index=False)

    registro = tabla_final.set_index('metodo')
    a = registro.loc['Eliminar columnas con NaN']
    b = registro.loc['Mediana']
    c = registro.loc[mejor_knn]
    texto = f'''Ejercicio 11 — Interpretación de resultados reales\n\n'''
    texto += ('Diseño: train/test estratificado 80/20 (semilla 42). Cada imputador, '
              'escalador y codificador se ajusta exclusivamente con training. '
              'En CV, se ajusta de nuevo dentro de cada fold. Clasificador fijo: '
              'LogisticRegression(C=1, max_iter=2000, solver=lbfgs).\n\n')
    texto += ('Comparación 1: Eliminar columnas con NaN elimina Age y Embarked, '
              f'y produce {int(a.numero_variables_finales)} columnas codificadas, '
              f'frente a {int(b.numero_variables_finales)} con imputación por mediana. '
              f'La accuracy en test cambia de {a.accuracy_test:.4f} a {b.accuracy_test:.4f}; '
              'la diferencia refleja tanto la imputación como la disponibilidad de variables.\n\n')
    texto += (f'Comparación 2: El KNN elegido mediante CV es {mejor_knn} '
              f'(ROC-AUC CV={c.cv_roc_auc_mean:.4f} ± {c.cv_roc_auc_std:.4f}), '
              f'con F1 en test={c.f1_test:.4f}; la mediana alcanza F1={b.f1_test:.4f}. '
              'KNN estima Age a partir de vecinos en variables numéricas escaladas, '
              'mientras la mediana asigna el mismo valor a todas las edades faltantes.\n\n')
    texto += (f'Selección de estrategia final por CV: {mejor}. '
              'Las 891 filas son utilizables porque no se eliminan observaciones; '
              'el método de eliminación retira columnas. Cabin se excluye en todos '
              'los métodos por su elevada proporción de NaN; PassengerId, Name y '
              'Ticket se excluyen como identificadores/texto de alta cardinalidad.\n')
    (SALIDA / '11_4_1_interpretacion.txt').write_text(texto, encoding='utf-8')
    print('\nResultados:\n', tabla_final[['metodo', 'cv_roc_auc_mean', 'accuracy_test',
                                         'f1_test', 'roc_auc_test',
                                         'numero_variables_finales']].to_string(index=False))
    print('\nArchivos guardados en:', SALIDA)


if __name__ == '__main__':
    main()
