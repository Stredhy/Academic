"""Ejercicio 1: clasificación e interpretación de Telco Customer Churn."""

import json
import os
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split, StratifiedKFold, GridSearchCV
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier, plot_tree, export_text
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score, ConfusionMatrixDisplay
from sklearn.inspection import permutation_importance
from scipy.stats import norm
warnings.filterwarnings('ignore', category=FutureWarning)
ROOT = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(ROOT, 'telco_resultados')
os.makedirs(OUT, exist_ok=True)

# True: muestra cada gráfica durante la ejecución (cierra la ventana para continuar).
MOSTRAR_GRAFICAS = True

def save_table(df, name):
    df.to_csv(os.path.join(OUT, name + '.csv'), index=False, encoding='utf-8-sig')

def save_plot(name):
    plt.tight_layout()
    plt.savefig(os.path.join(OUT, name + '.png'), dpi=160, bbox_inches='tight')
    if MOSTRAR_GRAFICAS:
        print(f'Gráfica: {name} (cierra la ventana para continuar)')
        plt.show()
    plt.close()

# =================================================================
# 1.1 Preparación del dataset
# =================================================================
df = pd.read_csv(os.path.join(ROOT, 'TelcoCustomerChurn.csv'))
save_table(pd.DataFrame([{'filas': len(df), 'columnas': df.shape[1]}]), '1_1_1_dimensiones')
save_table(pd.DataFrame({'variable': df.columns, 'tipo': df.dtypes.astype(str).values}), '1_1_2_tipos')
save_table(pd.DataFrame({'variable': df.columns, 'nan_originales': df.isna().sum().values, 'porcentaje_original': (df.isna().mean() * 100).round(2).values}), '1_1_3_faltantes_originales')
counts = df.Churn.value_counts().reindex(['No', 'Yes'])
fig, ax = plt.subplots(figsize=(6, 4))
bars = ax.bar(counts.index, counts.values)
ax.set(title='Distribución de Churn', xlabel='Churn', ylabel='Clientes')
for bar, v in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 40, f'{v} ({v / len(df):.1%})', ha='center')
save_plot('1_1_4_churn')
ids = [c for c in df.columns if c.lower().endswith('id') or c.lower() == 'id']
print('Identificadores excluidos:', ids)
df['TotalCharges'] = pd.to_numeric(df['TotalCharges'], errors='coerce')
print('NaN TotalCharges tras conversión:', df.TotalCharges.isna().sum())
save_table(pd.DataFrame({'variable': df.columns, 'nan_despues_conversion': df.isna().sum().values, 'porcentaje': (df.isna().mean() * 100).round(2).values}), '1_1_6_faltantes_convertidos')
X = df.drop(columns=ids + ['Churn'])
y = (df.Churn == 'Yes').astype(int)
# Tratar SeniorCitizen como categoría, no como una distancia numérica.
X['SeniorCitizen'] = X['SeniorCitizen'].astype(str)
num = X.select_dtypes(include='number').columns.tolist()
cat = X.select_dtypes(exclude='number').columns.tolist()
Xtr, Xte, ytr, yte = train_test_split(X, y, test_size=0.2, stratify=y, random_state=42)
pre = ColumnTransformer(
    transformers=[
        (
            'num',
            Pipeline([
                ('imputer', SimpleImputer(strategy='median')),
                ('scaler', StandardScaler()),
            ]),
            num,
        ),
        (
            'cat',
            Pipeline([
                ('imputer', SimpleImputer(strategy='most_frequent')),
                ('onehot', OneHotEncoder(handle_unknown='ignore', sparse_output=False)),
            ]),
            cat,
        ),
    ],
    sparse_threshold=0,
)
models = {
    'KNN': (
        KNeighborsClassifier(),
        {'model__n_neighbors': [3, 5, 7, 11, 15]},
    ),
    'Logistica': (
        LogisticRegression(max_iter=2000, random_state=42),
        {'model__C': [0.1, 1, 10]},
    ),
    'NaiveBayes': (
        GaussianNB(),
        {'model__var_smoothing': [1e-9, 1e-8, 1e-7]},
    ),
    'Arbol': (
        DecisionTreeClassifier(random_state=42),
        {'model__max_depth': [3, 5, 10]},
    ),
    'RandomForest': (
        RandomForestClassifier(random_state=42, n_jobs=1),
        {'model__n_estimators': [100, 300]},
    ),
    'SVM': (
        SVC(probability=True, random_state=42),
        {'model__kernel': ['linear', 'rbf'], 'model__C': [0.1, 1, 10]},
    ),
}

# =================================================================
# 1.2 Comparación de modelos
# =================================================================
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
fitted = {}
rows = []
cvrows = []
for name, (est, params) in models.items():
    print('Entrenando', name, flush=True)
    grid = GridSearchCV(Pipeline([('pre', pre), ('model', est)]), params, cv=cv, scoring='roc_auc', refit=True, n_jobs=1)
    grid.fit(Xtr, ytr)
    fitted[name] = grid.best_estimator_
    pred = grid.predict(Xte)
    prob = grid.predict_proba(Xte)[:, 1]
    rows.append({
        'algoritmo': name,
        'mejores_hiperparametros': json.dumps(grid.best_params_),
        'accuracy': accuracy_score(yte, pred),
        'precision': precision_score(yte, pred, zero_division=0),
        'recall': recall_score(yte, pred),
        'F1': f1_score(yte, pred),
        'ROC_AUC': roc_auc_score(yte, prob),
    })
    for p, score in zip(grid.cv_results_['params'], grid.cv_results_['mean_test_score']):
        cvrows.append({'algoritmo': name, **p, 'ROC_AUC_CV': score})
    ConfusionMatrixDisplay.from_predictions(yte, pred, display_labels=['No', 'Yes'], cmap='Blues', values_format='d')
    plt.title('Matriz de confusión - ' + name)
    save_plot('1_2_3_confusion_' + name)
    if name == 'KNN':
        transformed = grid.best_estimator_.named_steps['pre'].transform(Xtr)
        testvec = grid.best_estimator_.named_steps['pre'].transform(Xte.iloc[[0]])
        distances, indices = grid.best_estimator_.named_steps['model'].kneighbors(testvec)
        save_table(pd.DataFrame({'indice_training': Xtr.iloc[indices[0]].index, 'distancia': distances[0], 'churn_real': ytr.iloc[indices[0]].values}), '1_3_1_vecinos_ejemplo')
        save_table(pd.DataFrame([{'churn_real_ejemplo': int(yte.iloc[0]), 'probabilidad_churn': float(prob[0])}]), '1_3_1_prediccion_ejemplo')
    if name == 'Logistica':
        names = grid.best_estimator_.named_steps['pre'].get_feature_names_out()
        beta = grid.best_estimator_.named_steps['model'].coef_[0]
        order = np.argsort(np.abs(beta))[::-1][:10]
        save_table(pd.DataFrame({'variable': names[order], 'beta': beta[order], 'exp_beta': np.exp(beta[order])}), '1_3_2_coeficientes')
        base = Xtr.mode().iloc[0].copy()
        base[num] = Xtr[num].median()
        values = np.linspace(Xtr.tenure.min(), Xtr.tenure.max(), 100)
        gridx = pd.DataFrame([base] * len(values))
        gridx['tenure'] = values
        plt.figure(figsize=(7, 4))
        plt.plot(values, grid.predict_proba(gridx)[:, 1])
        plt.xlabel('tenure (meses)')
        plt.ylabel('Probabilidad de Churn')
        plt.title('Logística: efecto de tenure, resto fijo')
        save_plot('1_3_2_tenure')
    if name == 'NaiveBayes':
        # GaussianNB utiliza las columnas transformadas para estimar densidades.
        trmat = grid.best_estimator_.named_steps['pre'].transform(Xtr)
        nb = grid.best_estimator_.named_steps['model']
        for feature in ['tenure', 'MonthlyCharges']:
            idx = num.index(feature)
            vals = trmat[:, idx]
            xs = np.linspace(np.min(vals), np.max(vals), 250)
            fig, ax = plt.subplots(figsize=(7, 4))
            for cls, lab in [(0, 'No'), (1, 'Yes')]:
                ax.hist(vals[ytr.values == cls], bins=25, density=True, alpha=0.25, label='Histograma ' + lab)
                ax.plot(xs, norm.pdf(xs, nb.theta_[cls, idx], np.sqrt(nb.var_[cls, idx])), label='Gaussiana ' + lab)
            ax.set(title='Naive Bayes: ' + feature, xlabel=feature + ' (estandarizada)', ylabel='Densidad')
            ax.legend()
            save_plot('1_3_3_nb_' + feature)
    if name == 'Arbol':
        tree = grid.best_estimator_.named_steps['model']
        names = grid.best_estimator_.named_steps['pre'].get_feature_names_out()
        plt.figure(figsize=(22, 11))
        plot_tree(tree, max_depth=4, feature_names=names, class_names=['No', 'Yes'], filled=True, fontsize=8, rounded=True)
        plt.title('Árbol de decisión (hasta profundidad 4)')
        save_plot('1_3_4_arbol')
        with open(os.path.join(OUT, '1_3_4_reglas.txt'), 'w', encoding='utf-8') as f:
            f.write(export_text(tree, feature_names=list(names), max_depth=4))
    if name == 'RandomForest':
        forest = grid.best_estimator_.named_steps['model']
        names = grid.best_estimator_.named_steps['pre'].get_feature_names_out()
        gini = forest.feature_importances_
        order = np.argsort(gini)[::-1][:10]
        save_table(pd.DataFrame({'variable': names[order], 'importancia_gini': gini[order]}), '1_3_5_gini')
        # Calcular permutación sobre las variables originales.
        perm = permutation_importance(grid.best_estimator_, Xte, yte, n_repeats=5, random_state=42, scoring='roc_auc', n_jobs=1)
        order = np.argsort(perm.importances_mean)[::-1][:10]
        save_table(pd.DataFrame({'variable': Xte.columns[order], 'caida_ROC_AUC': perm.importances_mean[order], 'desviacion': perm.importances_std[order]}), '1_3_5_permutacion')
        for fname, values, labels in [('gini', gini, names), ('permutacion', perm.importances_mean, np.array(Xte.columns))]:
            order = np.argsort(values)[::-1][:10]
            plt.figure(figsize=(9, 5))
            plt.barh(np.array(labels)[order][::-1], values[order][::-1])
            plt.xlabel('Importancia' if fname == 'gini' else 'Caída de ROC-AUC')
            plt.title('Random Forest: top 10 ' + fname)
            save_plot('1_3_5_' + fname)
    if name == 'SVM':
        svm = grid.best_estimator_.named_steps['model']
        save_table(pd.DataFrame({'clase': ['No', 'Yes'], 'vectores_soporte': svm.n_support_}), '1_3_6_vectores_soporte')

# =================================================================
# 1.4 Síntesis y gráficas comparativas
# =================================================================
save_table(pd.DataFrame(rows).round(5), '1_4_1_comparacion_final')
save_table(pd.DataFrame(cvrows), '1_2_1_resultados_cv')
cvdf = pd.DataFrame(cvrows)
k = cvdf[cvdf.algoritmo == 'KNN'].sort_values('model__n_neighbors')
plt.figure(figsize=(6, 4))
plt.plot(k['model__n_neighbors'], k.ROC_AUC_CV, marker='o')
plt.xlabel('k (vecinos)')
plt.ylabel('ROC-AUC medio en CV')
plt.title('KNN: k frente a ROC-AUC')
save_plot('1_3_1_curva_knn')
s = cvdf[cvdf.algoritmo == 'SVM']
plt.figure(figsize=(7, 4))
for kernel, sub in s.groupby('model__kernel'):
    plt.plot(sub['model__C'], sub.ROC_AUC_CV, marker='o', label=kernel)
plt.xscale('log')
plt.xlabel('C')
plt.ylabel('ROC-AUC medio en CV')
plt.title('SVM: comparación de kernels')
plt.legend()
save_plot('1_3_6_kernels')
result = pd.DataFrame(rows)
print('\nRESULTADOS\n', result.to_string(index=False))
print('Mayor ROC-AUC:', result.loc[result.ROC_AUC.idxmax(), 'algoritmo'])
print('Mayor recall:', result.loc[result.recall.idxmax(), 'algoritmo'])
print('Árbol: más interpretable por reglas explícitas')
print('Archivos en', OUT)
