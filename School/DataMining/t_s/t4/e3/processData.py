"""Ejercicio 3: evaluación SVM con y sin estratificación.

Ejecutar junto a diabetes.csv. Se guardan tablas y gráficas en resultados_ejercicio3.
Dependencias: pandas numpy matplotlib scikit-learn
"""
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.model_selection import (train_test_split, KFold, StratifiedKFold,
                                     GridSearchCV, cross_validate)
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score

SEMILLA = 42
MOSTRAR_GRAFICAS = True
BASE = Path(__file__).resolve().parent
SALIDA = BASE / 'resultados_ejercicio3'
SALIDA.mkdir(exist_ok=True)
INVALIDAS = ['Glucose', 'BloodPressure', 'SkinThickness', 'Insulin', 'BMI']
METRICAS = {'accuracy': 'accuracy', 'f1': 'f1', 'roc_auc': 'roc_auc'}


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(SALIDA / nombre, dpi=180, bbox_inches='tight')
    if MOSTRAR_GRAFICAS:
        plt.show()
    plt.close()


def crear_modelo(c=1, gamma='scale'):
    """Imputación y escalado se ajustan únicamente en training."""
    return Pipeline([
        ('imputador', SimpleImputer(strategy='median')),
        ('escalador', StandardScaler()),
        ('svm', SVC(kernel='rbf', C=c, gamma=gamma))
    ])


def evaluar(modelo, x, y):
    pred = modelo.predict(x)
    scores = modelo.decision_function(x)
    return {
        'accuracy': accuracy_score(y, pred),
        'F1': f1_score(y, pred, zero_division=0),
        'ROC-AUC': roc_auc_score(y, scores)
    }


def registrar_subconjunto(registros, esquema, estratificado, nombre, y):
    n = len(y)
    unos = int(np.sum(y == 1))
    registros.append({
        'Esquema': esquema, 'Estratificación': 'Sí' if estratificado else 'No',
        'Subconjunto': nombre, 'Total': n, 'Outcome=0': n - unos,
        'Outcome=1': unos, '% Outcome=0': 100 * (n - unos) / n,
        '% Outcome=1': 100 * unos / n
    })


def cv_objeto(estratificado, n_splits):
    clase = StratifiedKFold if estratificado else KFold
    return clase(n_splits=n_splits, shuffle=True, random_state=SEMILLA)


def graficar_proporciones(tabla):
    """Cada barra representa un subconjunto o fold concreto."""
    for esquema in tabla['Esquema'].unique():
        sub = tabla[tabla['Esquema'] == esquema].copy()
        etiquetas = [f"{r['Estratificación']} | {r['Subconjunto']}"
                     for _, r in sub.iterrows()]
        y = np.arange(len(sub))
        fig, ax = plt.subplots(figsize=(11, max(4, len(sub) * 0.38)))
        ax.barh(y, sub['% Outcome=0'], label='Outcome=0')
        ax.barh(y, sub['% Outcome=1'], left=sub['% Outcome=0'], label='Outcome=1')
        ax.set_yticks(y, etiquetas)
        ax.invert_yaxis()
        ax.set_xlim(0, 100)
        ax.set_xlabel('Porcentaje de registros (%)')
        ax.set_title(f'3.4.2 Composición de clases: {esquema}')
        ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.08), ncol=2)
        guardar_figura('3_4_2_clases_' + esquema.replace('/', '_').replace(' ', '_') + '.png')


def graficar_heatmap(resultados):
    esquemas = ['Train/Test', 'Train/Validation/Test', '5-fold CV', 'Nested 5x3 CV']
    for metrica in ['accuracy', 'F1', 'ROC-AUC']:
        tabla = resultados.pivot(index='Esquema', columns='Estratificación', values=metrica)
        tabla = tabla.reindex(index=esquemas, columns=['No', 'Sí'])
        fig, ax = plt.subplots(figsize=(7, 4.5))
        imagen = ax.imshow(tabla.values, cmap='viridis', vmin=0, vmax=1, aspect='auto')
        ax.set_xticks([0, 1], ['No', 'Sí'])
        ax.set_yticks(np.arange(len(esquemas)), esquemas)
        ax.set_xlabel('Estratificación')
        ax.set_ylabel('Esquema de evaluación')
        ax.set_title(f'3.4.2 Heatmap de {metrica}')
        for i in range(len(esquemas)):
            for j in range(2):
                v = tabla.iloc[i, j]
                ax.text(j, i, f'{v:.3f}', ha='center', va='center',
                        color='white' if v < 0.65 else 'black')
        fig.colorbar(imagen, ax=ax, label=metrica)
        guardar_figura('3_4_2_heatmap_' + metrica.replace('-', '_') + '.png')


def main():
    df = pd.read_csv(BASE / 'diabetes.csv')
    if 'Outcome' not in df.columns:
        raise ValueError('El CSV debe incluir la columna Outcome.')
    variables = [c for c in df.columns if c != 'Outcome']
    if len(variables) != 8:
        raise ValueError('Se esperaban ocho variables predictoras.')

    # 3.1.1: descripción de las ocho variables y distribución de Outcome.
    descripcion = pd.DataFrame({
        'Variable': variables,
        'Tipo': [str(df[c].dtype) for c in variables],
        'Mínimo': [df[c].min() for c in variables],
        'Máximo': [df[c].max() for c in variables],
        'Número de ceros': [(df[c] == 0).sum() for c in variables]
    })
    descripcion.to_csv(SALIDA / '3_1_1_variables.csv', index=False)
    conteos = df['Outcome'].value_counts().reindex([0, 1], fill_value=0)
    distribucion = pd.DataFrame({'Outcome': [0, 1], 'Conteo': conteos.values,
                                  'Porcentaje': 100 * conteos.values / len(df)})
    distribucion.to_csv(SALIDA / '3_1_1_outcome.csv', index=False)
    print('\n3.1.1 Variables:\n', descripcion.to_string(index=False))
    print('\nDistribución:\n', distribucion.to_string(index=False))
    fig, ax = plt.subplots(figsize=(7, 4))
    barras = ax.bar(['Outcome=0', 'Outcome=1'], conteos.values)
    ax.bar_label(barras, labels=[f'{n} ({100*n/len(df):.2f}%)' for n in conteos.values])
    ax.set_ylim(0, max(conteos.values) * 1.15)
    ax.set_ylabel('Número de pacientes')
    ax.set_xlabel('Clase')
    ax.set_title('3.1.1 Distribución de Outcome')
    guardar_figura('3_1_1_outcome.png')

    # 3.1.2: solo los ceros de estas cinco columnas se vuelven NaN.
    X = df[variables].copy()
    y = df['Outcome'].astype(int)
    ceros_invalidos = (X[INVALIDAS] == 0).sum().rename('Ceros convertidos a NaN')
    X[INVALIDAS] = X[INVALIDAS].replace(0, np.nan)
    ceros_invalidos.to_csv(SALIDA / '3_1_2_ceros_invalidos.csv')
    print('\n3.1.2 Ceros inválidos:\n', ceros_invalidos.to_string())
    print('Los NaN se imputarán DENTRO de cada training/fold mediante Pipeline.')

    resultados = []
    composiciones = []
    seleccion = []
    for estratificado in [False, True]:
        etiqueta = 'Sí' if estratificado else 'No'
        print(f'\n===== ESTRATIFICACIÓN: {etiqueta} =====')
        estrato = y if estratificado else None

        # 3.3.1: train/test 80/20. Parámetros fijos.
        x_tr, x_te, y_tr, y_te = train_test_split(
            X, y, test_size=0.20, random_state=SEMILLA, stratify=estrato
        )
        registrar_subconjunto(composiciones, 'Train/Test', estratificado, 'Training', y_tr)
        registrar_subconjunto(composiciones, 'Train/Test', estratificado, 'Testing', y_te)
        modelo = crear_modelo()
        modelo.fit(x_tr, y_tr)
        r = evaluar(modelo, x_te, y_te)
        resultados.append({'Esquema': 'Train/Test', 'Estratificación': etiqueta,
                           'Partición': '80/20', **r, 'Desviación estándar': np.nan,
                           'Fuente de evaluación': 'Testing (20%)'})

        # 3.3.2: train/validation/test 60/20/20.
        # Primero separar test 20%; después validation = 25% del 80% restante.
        x_dev, x_te, y_dev, y_te = train_test_split(
            X, y, test_size=0.20, random_state=SEMILLA, stratify=estrato
        )
        x_tr, x_val, y_tr, y_val = train_test_split(
            x_dev, y_dev, test_size=0.25, random_state=SEMILLA,
            stratify=y_dev if estratificado else None
        )
        for nombre, etiquetas in [('Training', y_tr), ('Validation', y_val),
                                  ('Testing', y_te)]:
            registrar_subconjunto(composiciones, 'Train/Validation/Test',
                                  estratificado, nombre, etiquetas)
        candidatos = []
        for c in [0.1, 1, 10]:
            candidato = crear_modelo(c=c)
            candidato.fit(x_tr, y_tr)
            valor = evaluar(candidato, x_val, y_val)
            candidatos.append((c, valor['ROC-AUC']))
        mejor_c = max(candidatos, key=lambda z: z[1])[0]
        # Reajuste con train+validation, sin tocar test.
        final = crear_modelo(c=mejor_c)
        final.fit(x_dev, y_dev)
        r = evaluar(final, x_te, y_te)
        seleccion.append({'Estratificación': etiqueta, 'Esquema': 'Train/Validation/Test',
                          'C seleccionado': mejor_c, 'ROC-AUC validation':
                          max(v for _, v in candidatos)})
        resultados.append({'Esquema': 'Train/Validation/Test', 'Estratificación': etiqueta,
                           'Partición': '60/20/20', **r, 'Desviación estándar': np.nan,
                           'Fuente de evaluación': 'Testing (20%); C elegido en validation'})

        # 3.3.3: CV 5-fold, parámetros fijos, sin test separado.
        cv = cv_objeto(estratificado, 5)
        for i, (idx_tr, idx_val) in enumerate(cv.split(X, y), start=1):
            registrar_subconjunto(composiciones, '5-fold CV', estratificado,
                                  f'Fold {i} train', y.iloc[idx_tr])
            registrar_subconjunto(composiciones, '5-fold CV', estratificado,
                                  f'Fold {i} validation', y.iloc[idx_val])
        scores = cross_validate(crear_modelo(), X, y, cv=cv, scoring=METRICAS)
        resultados.append({'Esquema': '5-fold CV', 'Estratificación': etiqueta,
                           'Partición': '5 folds',
                           'accuracy': np.mean(scores['test_accuracy']),
                           'F1': np.mean(scores['test_f1']),
                           'ROC-AUC': np.mean(scores['test_roc_auc']),
                           'Desviación estándar': np.std(scores['test_roc_auc']),
                           'Fuente de evaluación': 'Media de 5 folds externos'})

        # 3.3.4: Nested CV 5x3; GridSearch ajusta solo folds internos.
        externo = cv_objeto(estratificado, 5)
        valores = []
        for i, (idx_tr, idx_val) in enumerate(externo.split(X, y), start=1):
            x_tr, x_val = X.iloc[idx_tr], X.iloc[idx_val]
            y_tr, y_val = y.iloc[idx_tr], y.iloc[idx_val]
            registrar_subconjunto(composiciones, 'Nested 5x3 CV', estratificado,
                                  f'Outer {i} train', y_tr)
            registrar_subconjunto(composiciones, 'Nested 5x3 CV', estratificado,
                                  f'Outer {i} validation', y_val)
            busqueda = GridSearchCV(
                crear_modelo(),
                param_grid={'svm__C': [0.1, 1, 10],
                            'svm__gamma': ['scale', 'auto']},
                cv=cv_objeto(estratificado, 3), scoring='roc_auc', refit=True
            )
            busqueda.fit(x_tr, y_tr)
            valores.append(evaluar(busqueda.best_estimator_, x_val, y_val))
            seleccion.append({'Estratificación': etiqueta,
                              'Esquema': f'Nested outer fold {i}',
                              'C seleccionado': busqueda.best_params_['svm__C'],
                              'gamma seleccionado': busqueda.best_params_['svm__gamma'],
                              'ROC-AUC validation': valores[-1]['ROC-AUC']})
        resultados.append({'Esquema': 'Nested 5x3 CV', 'Estratificación': etiqueta,
                           'Partición': '5 folds externos x 3 internos',
                           'accuracy': np.mean([v['accuracy'] for v in valores]),
                           'F1': np.mean([v['F1'] for v in valores]),
                           'ROC-AUC': np.mean([v['ROC-AUC'] for v in valores]),
                           'Desviación estándar': np.std([v['ROC-AUC'] for v in valores]),
                           'Fuente de evaluación': 'Media de 5 folds externos nested'})

    # 3.4.1 y 3.4.2: tablas y figuras.
    tabla = pd.DataFrame(resultados)
    clases = pd.DataFrame(composiciones)
    tabla.to_csv(SALIDA / '3_4_1_comparacion_ocho_configuraciones.csv', index=False)
    clases.to_csv(SALIDA / '3_2_2_composicion_subconjuntos.csv', index=False)
    pd.DataFrame(seleccion).to_csv(SALIDA / '3_3_2_hiperparametros.csv', index=False)
    print('\n3.4.1 RESULTADOS:\n', tabla.round(4).to_string(index=False))
    print('\n3.2.2 COMPOSICIÓN:\n', clases.round(2).to_string(index=False))
    graficar_proporciones(clases)
    graficar_heatmap(tabla)

    # 3.5: síntesis numérica, sin equiparar test con CV.
    lineas = [
        '3.5.1 Interpretación (comparaciones dentro de cada esquema):',
    ]
    for esquema in tabla['Esquema'].unique():
        a = tabla[(tabla['Esquema'] == esquema) &
                  (tabla['Estratificación'] == 'No')].iloc[0]
        b = tabla[(tabla['Esquema'] == esquema) &
                  (tabla['Estratificación'] == 'Sí')].iloc[0]
        lineas.append(f"{esquema}: cambio al estratificar: accuracy "
                      f"{b['accuracy']-a['accuracy']:+.4f}, F1 "
                      f"{b['F1']-a['F1']:+.4f}, ROC-AUC "
                      f"{b['ROC-AUC']-a['ROC-AUC']:+.4f}.")
    c = clases[clases['Subconjunto'].str.contains('Testing|validation', case=False)]
    lineas.append('Los porcentajes de Outcome=1 por subconjunto se muestran en 3_2_2_composicion_subconjuntos.csv.')
    lineas.append('Las desviaciones estándar reportadas corresponden al ROC-AUC entre folds externos.')
    lineas.append('Testing es una evaluación final de un modelo; CV promedia distintas particiones y modelos entrenados.')
    lineas.append('Las diferencias no se deben atribuir solo a estratificación: también intervienen el azar de la partición,')
    lineas.append('el tamaño de entrenamiento y la selección de C; no se comparan test y CV como estimaciones equivalentes.')
    (SALIDA / '3_5_interpretacion.txt').write_text('\n'.join(lineas), encoding='utf-8')
    print('\n' + '\n'.join(lineas))
    print('\nArchivos guardados en:', SALIDA)


if __name__ == '__main__':
    main()
