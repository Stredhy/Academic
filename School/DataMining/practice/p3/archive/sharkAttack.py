import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns

from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.inspection import permutation_importance
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.tree import DecisionTreeClassifier, plot_tree

# =========================================================
# 1. CARGA Y PREPROCESAMIENTO DE DATOS
# =========================================================
df = pd.read_csv('global_shark_attacks.csv', low_memory=False)

# Limpieza de la variable objetivo (Ataque fatal: 1 = Sí, 0 = No)
df['fatal'] = df['fatal_y_n'].astype(str).str.strip().str.upper()
df = df[df['fatal'].isin(['Y', 'N'])].copy()
df['target'] = (df['fatal'] == 'Y').astype(int)

# Limpieza y preparación de las features requeridas:
# 1. Ubicación (combinación país - área)
df['ubicacion'] = (
    df['country'].fillna('Desconocido').astype(str)
    + ' - '
    + df['area'].fillna('Desconocido').astype(str)
)

# 2. Actividad
df['actividad'] = (
    df['activity'].fillna('Desconocido').astype(str).str.lower().str.strip()
)

# 3. Especie
df['especie'] = (
    df['species'].fillna('Desconocido').astype(str).str.lower().str.strip()
)

# 4. Edad (extracción numérica)
df['edad'] = pd.to_numeric(
    df['age'].astype(str).str.extract(r'(\d+)')[0], errors='coerce'
)

# 5. Hora (extracción numérica del rango 0-23)
df['hora'] = pd.to_numeric(
    df['time'].astype(str).str.extract(r'(\d{1,2})')[0], errors='coerce'
)
df.loc[(df['hora'] < 0) | (df['hora'] > 23), 'hora'] = np.nan

# Reducción de cardinalidad alta agrupando categorías infrecuentes
for col in ['ubicacion', 'actividad', 'especie']:
  top_cats = df[col].value_counts().nlargest(20).index
  df[col] = df[col].apply(lambda x: x if x in top_cats else 'Otros')

features = ['actividad', 'especie', 'ubicacion', 'edad', 'hora']
X = df[features]
y = df['target']

# División train / test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

cat_cols = ['actividad', 'especie', 'ubicacion']
num_cols = ['edad', 'hora']

# Preprocesadores en Pipeline
preprocessor = ColumnTransformer([
    (
        'num',
        Pipeline([
            ('imputer', SimpleImputer(strategy='median')),
            ('scaler', StandardScaler()),
        ]),
        num_cols,
    ),
    (
        'cat',
        Pipeline([
            ('imputer', SimpleImputer(strategy='constant', fill_value='Otros')),
            (
                'encoder',
                OneHotEncoder(handle_unknown='ignore', sparse_output=False),
            ),
        ]),
        cat_cols,
    ),
])

# Transformación de datos
X_train_proc = preprocessor.fit_transform(X_train)
X_test_proc = preprocessor.transform(X_test)

# Obtención de nombres de variables codificadas
cat_encoder = preprocessor.named_transformers_['cat'].named_steps['encoder']
feature_names = num_cols + list(cat_encoder.get_feature_names_out(cat_cols))

# =========================================================
# 2. ENTRENAMIENTO Y EVALUACIÓN DE MODELOS
# =========================================================
models = {
    'Regresión Logística': LogisticRegression(max_iter=1000, random_state=42),
    'Naive Bayes': GaussianNB(),
    'Árbol de Decisión': DecisionTreeClassifier(max_depth=4, random_state=42),
    'Random Forest': RandomForestClassifier(
        n_estimators=100, max_depth=6, random_state=42
    ),
}

results = []

# Curva ROC Comparativa
plt.figure(figsize=(8, 6))
for name, model in models.items():
  model.fit(X_train_proc, y_train)
  y_pred = model.predict(X_test_proc)
  y_prob = (
      model.predict_proba(X_test_proc)[:, 1]
      if hasattr(model, 'predict_proba')
      else y_pred
  )

  acc = accuracy_score(y_test, y_pred)
  sens = recall_score(y_test, y_pred)  # Sensitivity / Recall
  cm = confusion_matrix(y_test, y_pred)
  spec = cm[0, 0] / (cm[0, 0] + cm[0, 1])  # Specificity
  prec = precision_score(y_test, y_pred, zero_division=0)
  f1 = f1_score(y_test, y_pred, zero_division=0)
  auc = roc_auc_score(y_test, y_prob)

  results.append({
      'Algoritmo': name,
      'Accuracy': acc,
      'Sensitivity': sens,
      'Specificity': spec,
      'Precision': prec,
      'F1-score': f1,
      'ROC-AUC': auc,
  })

  fpr, tpr, _ = roc_curve(y_test, y_prob)
  plt.plot(fpr, tpr, label=f'{name} (AUC = {auc:.3f})')

plt.plot([0, 1], [0, 1], 'k--', label='Azar')
plt.title('Curvas ROC Comparativas')
plt.xlabel('Tasa de Falsos Positivos (1 - Specificity)')
plt.ylabel('Tasa de Verdaderos Positivos (Sensitivity)')
plt.legend()
plt.grid(True)
plt.show()

# Tabla de Métricas Comparativas
df_metrics = pd.DataFrame(results)
print('\n=== TABLA COMPARATIVA DE MÉTRICAS ===')
print(df_metrics.to_string(index=False))

# Matrices de Confusión
fig, axes = plt.subplots(2, 2, figsize=(10, 8))
axes = axes.ravel()
for idx, (name, model) in enumerate(models.items()):
  y_pred = model.predict(X_test_proc)
  cm = confusion_matrix(y_test, y_pred)
  sns.heatmap(
      cm,
      annot=True,
      fmt='d',
      cmap='Blues',
      ax=axes[idx],
      xticklabels=['No Fatal', 'Fatal'],
      yticklabels=['No Fatal', 'Fatal'],
  )
  axes[idx].set_title(f'Matriz de Confusión: {name}')
  axes[idx].set_xlabel('Predicción')
  axes[idx].set_ylabel('Real')
plt.tight_layout()
plt.show()

# =========================================================
# 3. VISUALIZACIÓN / INTERPRETACIÓN ESPECÍFICA POR MODELO
# =========================================================

# --- A) REGRESIÓN LOGÍSTICA: Coeficientes Beta y Odds Ratios (OR = exp(β)) ---
log_reg = models['Regresión Logística']
coefs = log_reg.coef_[0]
odds_ratios = np.exp(coefs)

df_log_reg = pd.DataFrame({
    'Característica': feature_names,
    'Coeficiente_Beta': coefs,
    'Odds_Ratio': odds_ratios,
}).sort_values(by='Odds_Ratio', ascending=False)

print('\n=== REGRESIÓN LOGÍSTICA: Coeficientes y Odds Ratios (Top 10) ===')
print(df_log_reg.head(10).to_string(index=False))

plt.figure(figsize=(10, 5))
top_or = pd.concat([df_log_reg.head(5), df_log_reg.tail(5)])
sns.barplot(x='Odds_Ratio', y='Característica', data=top_or, palette='vlag')
plt.axvline(1.0, color='red', linestyle='--', label='OR = 1 (Sin Efecto)')
plt.title('Regresión Logística: Odds Ratios (OR = exp(β))')
plt.xlabel('Odds Ratio')
plt.legend()
plt.show()

# --- B) NAIVE BAYES: Probabilidades/Verosimilitudes (μ y σ por clase) ---
gnb = models['Naive Bayes']
df_nb = pd.DataFrame({
    'Característica': feature_names,
    'Media_Clase_No_Fatal (μ0)': gnb.theta_[0],
    'Std_Clase_No_Fatal (σ0)': np.sqrt(gnb.var_[0]),
    'Media_Clase_Fatal (μ1)': gnb.theta_[1],
    'Std_Clase_Fatal (σ1)': np.sqrt(gnb.var_[1]),
})

print('\n=== NAIVE BAYES: Parámetros Gaussianos (μ y σ) por Clase ===')
print(df_nb.head(10).to_string(index=False))

# --- C) ÁRBOL DE DECISIÓN: Diagrama del Árbol e Importancia Gini ---
dt = models['Árbol de Decisión']

plt.figure(figsize=(18, 9))
plot_tree(
    dt,
    feature_names=feature_names,
    class_names=['No Fatal', 'Fatal'],
    filled=True,
    fontsize=7,
)
plt.title(
    'Árbol de Decisión: Estructura de Reglas (Variables, Umbrales, Clases y'
    ' Gini)'
)
plt.show()

df_dt_imp = pd.DataFrame({
    'Característica': feature_names,
    'Importancia_Gini': dt.feature_importances_,
}).sort_values(by='Importancia_Gini', ascending=False)

plt.figure(figsize=(10, 4))
sns.barplot(
    x='Importancia_Gini',
    y='Característica',
    data=df_dt_imp.head(10),
    palette='viridis',
)
plt.title('Árbol de Decisión: Feature Importance basada en Gini (MDI)')
plt.show()

# --- D) RANDOM FOREST: Importancia Gini y Permutation Importance ---
rf = models['Random Forest']

df_rf_gini = pd.DataFrame({
    'Característica': feature_names,
    'Importancia_Gini': rf.feature_importances_,
}).sort_values(by='Importancia_Gini', ascending=False)

perm_imp = permutation_importance(
    rf, X_test_proc, y_test, n_repeats=10, random_state=42
)
df_rf_perm = pd.DataFrame({
    'Característica': feature_names,
    'Importancia_Permutacion': perm_imp.importances_mean,
}).sort_values(by='Importancia_Permutacion', ascending=False)

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sns.barplot(
    x='Importancia_Gini',
    y='Característica',
    data=df_rf_gini.head(8),
    ax=axes[0],
    palette='magma',
)
axes[0].set_title('Random Forest: Gini Importance (MDI)')

sns.barplot(
    x='Importancia_Permutacion',
    y='Característica',
    data=df_rf_perm.head(8),
    ax=axes[1],
    palette='crest',
)
axes[1].set_title('Random Forest: Permutation Importance')

plt.tight_layout()
plt.show()