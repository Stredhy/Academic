"""Ejercicio 12: clasificación transductiva de nodos LastFM Asia.
Uso: python ejercicio12_lastfm.py
Requiere: pandas numpy scipy scikit-learn networkx matplotlib
"""
from pathlib import Path
import os
import time
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from scipy import sparse
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, ConfusionMatrixDisplay

SEED = 42
BASE = Path(__file__).resolve().parent
OUT = BASE / 'resultados_ejercicio12'
OUT.mkdir(exist_ok=True)
MOSTRAR = os.getenv('MOSTRAR_GRAFICAS', '1') == '1'

def figura(nombre):
    plt.savefig(OUT / nombre, dpi=160, bbox_inches='tight')
    if MOSTRAR:
        plt.show()
    plt.close()

def guardar(df, nombre):
    df.to_csv(OUT / nombre, index=False, encoding='utf-8-sig')

print('12.1 Carga y exploración', flush=True)
edges = pd.read_csv(BASE / 'lastfm_asia_edges.csv')
targets = pd.read_csv(BASE / 'lastfm_asia_target.csv')
ids = targets['id'].astype(int).to_numpy()
y = targets['target'].to_numpy()
assert len(np.unique(ids)) == len(ids)
g = nx.Graph()
g.add_nodes_from(ids)
g.add_edges_from(edges[['node_1', 'node_2']].itertuples(index=False, name=None))
assert g.number_of_nodes() == len(ids), 'Hay nodos sin etiqueta; revisar el dataset.'
components = sorted((len(c) for c in nx.connected_components(g)), reverse=True)
classes, counts = np.unique(y, return_counts=True)
guardar(pd.DataFrame({'clase': classes, 'cantidad': counts}), '12_1_1_clases.csv')
guardar(pd.DataFrame([{
    'nodos': g.number_of_nodes(), 'aristas': g.number_of_edges(),
    'densidad': nx.density(g), 'componentes_conexas': len(components),
    'tamano_componente_mayor': components[0], 'n_clases': len(classes),
    'atributos_individuales_disponibles': 0,
    'nota': 'Solo hay aristas y etiquetas; no hay atributos propios de usuario.'
}]), '12_1_1_resumen.csv')
print('Nodos:', g.number_of_nodes(), 'Aristas:', g.number_of_edges(), 'Clases:', len(classes), flush=True)

# 12.1.2 División de nodos: grafo completo visible, etiquetas test ocultas al modelo.
train_idx, test_idx = train_test_split(np.arange(len(ids)), test_size=.20,
                                       stratify=y, random_state=SEED)
guardar(pd.DataFrame({'id': ids, 'particion': np.where(np.isin(np.arange(len(ids)), train_idx), 'train', 'test')}),
        '12_1_2_particion.csv')

# 12.3.1 Matriz de adyacencia: 7624 dimensiones, almacenada dispersa.
print('12.3 Matriz de adyacencia', flush=True)
A = nx.to_scipy_sparse_array(g, nodelist=ids.tolist(), format='csr', dtype=np.float32)
A = sparse.csr_matrix(A)

# 12.3.1 Cinco métricas topológicas; betweenness aproximada reproducible.
print('12.3 Centralidades (betweenness aproximada, k=32)', flush=True)
degree = dict(g.degree())
between = nx.betweenness_centrality(g, k=min(32, len(ids)), normalized=True, seed=SEED)
print('12.3 Closeness', flush=True)
# Closeness exacta en NetworkX es costosa; aproximación con 64 fuentes
# usando caminos mínimos dispersos, misma muestra para todos los nodos.
from scipy.sparse.csgraph import shortest_path
rng = np.random.default_rng(SEED)
sources = rng.choice(len(ids), size=min(64, len(ids)), replace=False)
dist_sample = shortest_path(A, directed=False, unweighted=True, indices=sources)
reach = np.isfinite(dist_sample)
reach_count = reach.sum(axis=0)
dist_sum = np.where(reach, dist_sample, 0).sum(axis=0)
closeness_est = np.divide(np.maximum(reach_count - 1, 0), dist_sum,
                          out=np.zeros(len(ids)), where=dist_sum > 0)
close = dict(zip(ids, closeness_est))
print('12.3 Eigenvector', flush=True)
try:
    eigen = nx.eigenvector_centrality(g, max_iter=1500, tol=1e-6)
except nx.PowerIterationFailedConvergence:
    eigen = nx.eigenvector_centrality_numpy(g)
cluster = nx.clustering(g)
metrics_names = ['degree', 'betweenness_aprox', 'closeness_aprox', 'eigenvector', 'clustering_coefficient']
M = np.array([[degree[i], between[i], close[i], eigen[i], cluster[i]] for i in ids], dtype=np.float32)
guardar(pd.DataFrame({'id': ids, **{name: M[:, j] for j, name in enumerate(metrics_names)}}),
        '12_3_1_metricas_topologicas.csv')

# No existen atributos individuales en los CSV. Para hacer explícita la
# limitación, se usa grado como único atributo estructural propio (proxy).
# Esto NO constituye información de perfil individual independiente del grafo.
Xown = M[:, :1].copy()
# Agregación de atributo proxy de vecinos: media del grado de los vecinos.
neighbor_count = np.asarray(A.sum(axis=1)).ravel()
neighbor_sum = np.asarray(A @ Xown).reshape(-1, 1)
Xneighbor = np.divide(neighbor_sum, neighbor_count[:, None],
                      out=np.zeros_like(neighbor_sum), where=neighbor_count[:, None] != 0)
Xboth = np.column_stack([Xown, M])

representations = {
    'Atributos propios (proxy grado)': (Xown, ['grado_proxy']),
    'Adyacencia': (A, [f'vecino_id_{i}' for i in ids]),
    'Cinco metricas topologicas': (M, metrics_names),
    'Promedio de vecinos (grado)': (Xneighbor, ['grado_medio_vecinos']),
    'Propios + metricas': (Xboth, ['grado_proxy'] + metrics_names),
}
guardar(pd.DataFrame([{'representacion': name, 'filas': X.shape[0], 'columnas': X.shape[1],
                       'nodos_sin_vecinos': int(np.sum(neighbor_count == 0)),
                       'tratamiento_aislados': 'promedio vecino=0; métricas estructurales según NetworkX'}
                      for name, (X, _) in representations.items()]), '12_3_2_dimensiones.csv')

# 12.2 Una sola subred, posiciones fijas y seis coloraciones.
# Selección reproducible: BFS desde nodo de mayor grado hasta 100 nodos.
print('12.2 Visualización de subred', flush=True)
seed_node = max(g, key=lambda n: (g.degree(n), -n))
selected = list(nx.bfs_tree(g, seed_node).nodes())[:100]
sub = g.subgraph(selected).copy()
pos = nx.spring_layout(sub, seed=SEED)
index = {node: j for j, node in enumerate(ids)}
labels_map = dict(zip(ids, y))
color_values = [np.array([labels_map[n] for n in selected], dtype=float)] + [
    np.array([M[index[n], j] for n in selected], dtype=float) for j in range(5)]
titles = ['Clase real (solo visualización)', 'Degree', 'Betweenness (aprox.)',
          'Closeness', 'Eigenvector centrality', 'Clustering coefficient']
fig, axes = plt.subplots(2, 3, figsize=(19, 12))
for j, ax in enumerate(axes.flat):
    nx.draw_networkx_edges(sub, pos, ax=ax, alpha=.20, width=.5)
    vals = color_values[j]
    cm = 'tab20' if j == 0 else 'viridis'
    nodes = nx.draw_networkx_nodes(sub, pos, nodelist=selected, ax=ax, node_size=32,
                                   node_color=vals, cmap=plt.get_cmap(cm),
                                   vmin=float(vals.min()), vmax=float(vals.max()) if vals.max() > vals.min() else float(vals.min()+1))
    fig.colorbar(nodes, ax=ax, shrink=.75, label=titles[j])
    ax.set_title(titles[j]); ax.axis('off')
fig.suptitle('Mismos 100 nodos y layout fijo — LastFM Asia', fontsize=15)
figura('12_2_1_seis_coloraciones.png')

# 12.4 Preprocesamiento ajustado exclusivamente en training.
# Para adyacencia dispersa: SimpleImputer no necesario (sin NaN), StandardScaler(with_mean=False).
print('12.4 Clasificación con RandomForest 200 árboles', flush=True)
results = []
importance_rows = []
for name, (X, feature_names) in representations.items():
    print('  Modelo:', name, flush=True)
    is_sparse = sparse.issparse(X)
    # Sin NaN en datos derivados; imputación incluida para datos densos por protocolo.
    if is_sparse:
        prep = StandardScaler(with_mean=False)
    else:
        prep = Pipeline([('imputer', SimpleImputer(strategy='median')),
                         ('scaler', StandardScaler())])
    Xtr = prep.fit_transform(X[train_idx])
    Xte = prep.transform(X[test_idx])
    clf = RandomForestClassifier(n_estimators=200, random_state=SEED, n_jobs=-1)
    clf.fit(Xtr, y[train_idx])
    pred = clf.predict(Xte)
    results.append({'representacion': name, 'accuracy': accuracy_score(y[test_idx], pred),
                    'f1_macro': f1_score(y[test_idx], pred, average='macro', zero_division=0),
                    'f1_weighted': f1_score(y[test_idx], pred, average='weighted', zero_division=0),
                    'n_variables': X.shape[1], 'n_train': len(train_idx), 'n_test': len(test_idx)})
    cm = confusion_matrix(y[test_idx], pred, labels=classes)
    slug = list(representations).index(name) + 1
    pd.DataFrame(cm, index=[f'real_{c}' for c in classes],
                 columns=[f'pred_{c}' for c in classes]).to_csv(OUT / f'12_4_2_confusion_{slug}.csv')
    fig, ax = plt.subplots(figsize=(7, 6))
    ConfusionMatrixDisplay(cm, display_labels=classes).plot(ax=ax, colorbar=False, cmap='Blues')
    ax.set_title(name)
    figura(f'12_4_2_confusion_{slug}.png')
    top = np.argsort(clf.feature_importances_)[::-1][:10]
    for rank, j in enumerate(top, 1):
        importance_rows.append({'representacion': name, 'puesto': rank,
                                'caracteristica': feature_names[j],
                                'importancia': float(clf.feature_importances_[j])})
    print('   Accuracy:', round(results[-1]['accuracy'], 4), 'F1 macro:', round(results[-1]['f1_macro'], 4), flush=True)

r = pd.DataFrame(results).sort_values('f1_macro', ascending=False)
guardar(r, '12_4_2_comparacion.csv')
guardar(pd.DataFrame(importance_rows), '12_4_2_top10_importancias.csv')
fig, ax = plt.subplots(figsize=(11, 5))
x = np.arange(len(r)); width = .35
ax.bar(x-width/2, r['accuracy'], width, label='Accuracy')
ax.bar(x+width/2, r['f1_macro'], width, label='F1 macro')
ax.set_xticks(x, r['representacion'], rotation=18, ha='right')
ax.set_ylim(0, 1); ax.legend(); ax.set_title('Comparación de cinco representaciones')
figura('12_4_2_comparacion.png')

best = r.iloc[0]
worst = r.iloc[-1]
text = f'''# Ejercicio 12 — Interpretación de resultados\n\n## 12.1\nEl grafo tiene {g.number_of_nodes()} nodos, {g.number_of_edges()} aristas, densidad {nx.density(g):.6f} y {len(components)} componentes conexas. Se dividieron las etiquetas en {len(train_idx)} nodos training y {len(test_idx)} testing. Se permite utilizar el grafo completo (evaluación transductiva), pero no las etiquetas testing para construir las características ni entrenar.\n\n## Limitación de datos\nLos CSV suministrados SOLO incluyen aristas e identificador/clase, no atributos de perfil de usuario. Para las representaciones «atributos propios» se utilizó como proxy estructural el grado del nodo, y para «promedio de vecinos» el grado medio de los vecinos. Por ello no es una comparación entre atributos individuales auténticos y topología independiente: todas las representaciones proceden del grafo. «Propios + métricas» duplica la información del grado deliberadamente para seguir la lista de cinco variantes; no se presenta como una nueva fuente de datos.\n\n## 12.2\nLas seis coloraciones usan exactamente la misma subred y posiciones. La clase se usa SOLO para colorear, nunca para crear características predictoras. Betweenness se aproxima con 128 nodos fuente para reducir el coste computacional.\n\n## 12.3\nLa matriz de adyacencia tiene {len(ids)} columnas; una por posible vecino. Los nodos sin vecinos reciben promedio vecinal 0. Las métricas son grado, betweenness, closeness aproximada, eigenvector y coeficiente de clustering.\n\n## 12.4\nMejor F1 macro: {best['representacion']} ({best['f1_macro']:.4f}); peor F1 macro: {worst['representacion']} ({worst['f1_macro']:.4f}). La adyacencia representa identidades de vecinos y puede generalizar peor a nodos completamente nuevos; este experimento es transductivo. Las centralidades resumen patrones estructurales de forma compacta. Ninguna característica utiliza las etiquetas de testing. La interpretación de importancias se limita a la importancia de impureza del Random Forest, que puede favorecer variables continuas o de alta cardinalidad.\n'''
(OUT / '12_interpretacion.md').write_text(text, encoding='utf-8')
print('\nFinalizado. Resultados:', OUT, flush=True)
print(r.to_string(index=False), flush=True)
