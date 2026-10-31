"""Ejercicio 6: representaciones de texto y Naive Bayes.
Ejecutar: python ejercicio6_bbc.py
Requiere: pandas numpy matplotlib scikit-learn
"""
from pathlib import Path
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix, ConfusionMatrixDisplay

BASE = Path(__file__).resolve().parent
ARCHIVO = BASE / 'bbc-news-data.csv'
SALIDA = BASE / 'resultados_ejercicio6'
SALIDA.mkdir(exist_ok=True)
MOSTRAR_GRAFICAS = os.environ.get('MOSTRAR_GRAFICAS', '1') == '1'


def guardar_tabla(tabla, nombre):
    tabla.to_csv(SALIDA / nombre, index=False, encoding='utf-8-sig')
    print(f'\n{nombre}\n{tabla.to_string(index=False)}')


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(SALIDA / nombre, dpi=180, bbox_inches='tight')
    if MOSTRAR_GRAFICAS:
        plt.show()
    plt.close()


# 6.1.1 - Lectura, ejemplos y distribución de clases.
df = pd.read_csv(ARCHIVO, sep='\t')
requeridas = {'category', 'content'}
if not requeridas.issubset(df.columns):
    raise ValueError(f'Columnas esperadas: {requeridas}. Recibidas: {df.columns.tolist()}')
df = df.dropna(subset=['category', 'content']).copy()
df['content'] = df['content'].astype(str)
df = df[df['content'].str.strip().ne('')].reset_index(drop=True)
print(f'Documentos: {len(df)} | Columnas originales: {df.columns.tolist()}')

muestra = df[['category', 'content']].head(5).copy()
muestra['content'] = muestra['content'].str.slice(0, 200)
guardar_tabla(muestra.rename(columns={'category': 'Clase', 'content': 'Texto (200 caracteres)'}), '6_1_1_cinco_textos.csv')
clases = df['category'].value_counts().rename_axis('Clase').reset_index(name='Documentos')
clases['Porcentaje'] = (clases['Documentos'] / len(df) * 100).round(2)
guardar_tabla(clases, '6_1_1_distribucion_clases.csv')
fig, ax = plt.subplots(figsize=(9, 5))
barras = ax.bar(clases['Clase'], clases['Porcentaje'])
ax.bar_label(barras, fmt='%.1f%%', padding=3)
ax.set(xlabel='Categoría', ylabel='Porcentaje de documentos (%)', title='6.1.1 Distribución de documentos por categoría')
ax.set_ylim(0, clases['Porcentaje'].max() * 1.18)
guardar_figura('6_1_1_clases.png')

# 6.1.2 - Partición ANTES de aprender cualquier vocabulario.
X_train, X_test, y_train, y_test = train_test_split(
    df['content'], df['category'], test_size=0.20,
    random_state=42, stratify=df['category']
)
particiones = pd.concat([
    y_train.value_counts().rename('Training'),
    y_test.value_counts().rename('Testing')
], axis=1).fillna(0).astype(int).reset_index(names='Clase')
guardar_tabla(particiones, '6_1_2_particiones.csv')

# 6.1.3–6.1.5 y 6.3.1 - Vectorizadores entrenados solo con training.
configuraciones = {
    'Binaria + BernoulliNB': (CountVectorizer(binary=True), BernoulliNB()),
    'Conteos + MultinomialNB': (CountVectorizer(), MultinomialNB()),
    'TF-IDF + MultinomialNB': (TfidfVectorizer(), MultinomialNB()),
}
modelos = {}
resultados = []
predicciones = {}
for nombre, (vectorizador, clasificador) in configuraciones.items():
    modelo = Pipeline([('vectorizador', vectorizador), ('naive_bayes', clasificador)])
    modelo.fit(X_train, y_train)
    y_pred = modelo.predict(X_test)
    modelos[nombre] = modelo
    predicciones[nombre] = y_pred
    resultados.append({
        'Representación': nombre,
        'Vocabulario': len(modelo.named_steps['vectorizador'].vocabulary_),
        'Matriz training': str(modelo.named_steps['vectorizador'].transform(X_train).shape),
        'Matriz testing': str(modelo.named_steps['vectorizador'].transform(X_test).shape),
        'Accuracy': accuracy_score(y_test, y_pred),
        'F1 macro': f1_score(y_test, y_pred, average='macro'),
        'F1 weighted': f1_score(y_test, y_pred, average='weighted'),
    })
    print(f'\n{nombre}\n{classification_report(y_test, y_pred, zero_division=0)}')
    ConfusionMatrixDisplay.from_predictions(y_test, y_pred, xticks_rotation=30, cmap='Blues')
    plt.title(f'6.4.1 Matriz de confusión: {nombre}')
    guardar_figura('6_4_1_confusion_' + nombre.split(' + ')[0].replace('-', '_') + '.png')

# 6.2.1 - Misma muestra de cinco frases y vocabulario de al menos diez términos.
# Estas frases son ejemplos didácticos, NO se usan para ajustar los modelos de evaluación.
frases = [
    'the government announced a new economic policy for business',
    'the football team won the final match in the stadium',
    'the new computer technology improves internet security',
    'the film actor won an award at the music festival',
    'the bank and government discussed economic growth and markets',
]
vectorizador_demo = CountVectorizer()
matriz_conteos = vectorizador_demo.fit_transform(frases)
terminos = vectorizador_demo.get_feature_names_out()
# Vocabulario fijo de esta demostración para comparar las mismas columnas.
for nombre, vectorizador in [
    ('Binaria', CountVectorizer(binary=True, vocabulary=terminos)),
    ('Conteos', CountVectorizer(vocabulary=terminos)),
    ('TF_IDF', TfidfVectorizer(vocabulary=terminos)),
]:
    matriz = vectorizador.fit_transform(frases)
    tabla = pd.DataFrame(matriz.toarray(), columns=terminos)
    tabla.insert(0, 'Documento', [f'Frase {i}' for i in range(1, 6)])
    guardar_tabla(tabla.round(4), f'6_2_1_matriz_{nombre}.csv')
    print(f'{nombre}: {matriz.shape[0]} documentos × {matriz.shape[1]} términos')

# 6.4.1 - Métricas finales, diez términos característicos por clase.
comparacion = pd.DataFrame(resultados).sort_values('F1 macro', ascending=False)
guardar_tabla(comparacion.round(5), '6_4_1_comparacion.csv')
for nombre, modelo in modelos.items():
    vocab = modelo.named_steps['vectorizador'].get_feature_names_out()
    nb = modelo.named_steps['naive_bayes']
    # log P(término|clase) es un indicador descriptivo, no una explicación causal.
    filas = []
    for idx, clase in enumerate(nb.classes_):
        orden = np.argsort(nb.feature_log_prob_[idx])[-10:][::-1]
        for rango, pos in enumerate(orden, start=1):
            filas.append({'Clase': clase, 'Posición': rango,
                          'Término': vocab[pos], 'Log P(término|clase)': nb.feature_log_prob_[idx, pos]})
    guardar_tabla(pd.DataFrame(filas), '6_4_1_terminos_' + nombre.split(' + ')[0].replace('-', '_') + '.csv')

mejor_nombre = comparacion.iloc[0]['Representación']
mejor_pred = predicciones[mejor_nombre]
errores = pd.DataFrame({'Texto': X_test.to_numpy(), 'Real': y_test.to_numpy(), 'Predicha': mejor_pred})
errores = errores[errores['Real'] != errores['Predicha']].copy()
errores['Texto'] = errores['Texto'].str.slice(0, 300)
guardar_tabla(errores.head(10), '6_4_1_errores_ejemplos.csv')

with open(SALIDA / '6_4_1_interpretacion.txt', 'w', encoding='utf-8') as f:
    f.write('Comparación de tres representaciones de texto con Naive Bayes\n')
    f.write(comparacion.to_string(index=False, float_format=lambda x: f'{x:.4f}') + '\n\n')
    f.write(f'La mejor representación por F1 macro fue {mejor_nombre}.\n')
    f.write('Accuracy mide aciertos globales y F1 macro promedia el F1 de las cinco categorías sin ponderarlas por frecuencia.\n')
    f.write('Los diez términos por clase son los de mayor probabilidad condicional estimada por cada Naive Bayes.\n')
    f.write('Errores concretos del mejor modelo:\n')
    if errores.empty:
        f.write('No se observaron errores en testing.\n')
    else:
        for _, fila in errores.head(2).iterrows():
            f.write(f"Real: {fila['Real']} | Predicha: {fila['Predicha']} | Texto: {fila['Texto']}\n")
        f.write('Estos errores pueden reflejar vocabulario compartido entre categorías o contexto que el modelo no capta.\n')
print(f'\nProceso terminado. Resultados en: {SALIDA}')
