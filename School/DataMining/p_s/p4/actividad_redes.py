"""
Actividad de análisis de redes Twitch PT.
Requisitos: pandas, numpy, networkx, matplotlib, scikit-learn, scipy.
Ejecutar desde la carpeta que contiene musae_PTBR_edges.csv y musae_PTBR_target.csv.
"""
from pathlib import Path
import json
import warnings
import numpy as np
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report
from scipy import sparse

BASE = Path(".")
OUT = BASE / "resultados"
OUT.mkdir(exist_ok=True)
EDGES_FILE = BASE / "musae_PTBR_edges.csv"
TARGET_FILE = BASE / "musae_PTBR_target.csv"

edges = pd.read_csv(EDGES_FILE)
target = pd.read_csv(TARGET_FILE)
assert {"from", "to"}.issubset(edges.columns), "El CSV de aristas debe tener from y to."
assert {"new_id", "mature"}.issubset(target.columns), "El CSV target debe tener new_id y mature."

# 1. Grafo no dirigido, sin pesos. new_id corresponde al identificador de nodo de las aristas.
G = nx.from_pandas_edgelist(edges, source="from", target="to", create_using=nx.Graph())
nodes = np.array(sorted(G.nodes()))
labels = target.set_index("new_id")["mature"].astype(int).reindex(nodes)
if labels.isna().any():
    raise ValueError("Hay nodos sin etiqueta mature asociada.")
y = labels.to_numpy()

# Estadísticas descriptivas
stats = {
    "nodes": G.number_of_nodes(),
    "edges": G.number_of_edges(),
    "components": nx.number_connected_components(G),
    "density": nx.density(G),
    "average_degree": float(np.mean([d for _, d in G.degree()])),
    "average_clustering": nx.average_clustering(G),
    "diameter": nx.diameter(G) if nx.is_connected(G) else None,
    "mature_0": int((y == 0).sum()),
    "mature_1": int((y == 1).sum()),
}
print("Resumen de la red:", json.dumps(stats, indent=2, ensure_ascii=False))

# 2. Una única distribución espacial para todos los grafos.
pos = nx.spring_layout(G, seed=42, iterations=80, k=0.12)

def save_network(filename, title, node_values=None, categorical=False, colorbar_label=None):
    fig, ax = plt.subplots(figsize=(12, 9))
    nx.draw_networkx_edges(G, pos, alpha=0.05, width=0.3, edge_color="#aab0b6", ax=ax)
    if categorical:
        colors = np.where(np.asarray(node_values) == 1, "#d94841", "#4c78a8")
        nx.draw_networkx_nodes(G, pos, nodelist=list(nodes), node_size=8,
                               node_color=colors, linewidths=0, ax=ax)
        from matplotlib.lines import Line2D
        ax.legend(handles=[
            Line2D([0], [0], marker="o", color="w", label="mature = 0",
                   markerfacecolor="#4c78a8", markersize=8),
            Line2D([0], [0], marker="o", color="w", label="mature = 1",
                   markerfacecolor="#d94841", markersize=8)],
            loc="upper right")
    elif node_values is None:
        nx.draw_networkx_nodes(G, pos, node_size=7, node_color="#9ca3af",
                               linewidths=0, ax=ax)
    else:
        sc = nx.draw_networkx_nodes(G, pos, nodelist=list(nodes), node_size=9,
                                    node_color=np.asarray(node_values), cmap=plt.cm.viridis,
                                    linewidths=0, ax=ax)
        fig.colorbar(sc, ax=ax, shrink=0.72, label=colorbar_label)
    ax.set_title(title)
    ax.axis("off")
    fig.tight_layout()
    fig.savefig(OUT / filename, dpi=180, bbox_inches="tight")
    plt.close(fig)

save_network("01_red_gris.png", "Red de Twitch PT — todos los usuarios en gris")
save_network("02_red_target.png", "Red de Twitch PT — coloreada por mature", y, categorical=True)

# 3. Métricas de red
metrics = {
    "degree": nx.degree_centrality(G),
    "betweenness": nx.betweenness_centrality(G, normalized=True),
    "closeness": nx.closeness_centrality(G),
}
with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    metrics["eigenvector"] = nx.eigenvector_centrality(G, max_iter=2000, tol=1e-10)
metrics["clustering"] = nx.clustering(G)
metric_labels = {
    "degree": "Degree centrality",
    "betweenness": "Betweenness centrality",
    "closeness": "Closeness centrality",
    "eigenvector": "Eigenvector centrality",
    "clustering": "Clustering coefficient",
}
centrality = pd.DataFrame({"node": nodes, "mature": y})
for name, values in metrics.items():
    centrality[name] = [values[int(n)] for n in nodes]
    save_network(f"metric_{name}.png", metric_labels[name],
                 [values[int(n)] for n in nodes], colorbar_label=metric_labels[name])
centrality.to_csv(OUT / "centralidades.csv", index=False)

top_rows = []
for name in metrics:
    top = centrality.sort_values(name, ascending=False).head(5)
    for rank, (_, row) in enumerate(top.iterrows(), start=1):
        top_rows.append({"metric": name, "rank": rank, "node": int(row.node),
                         "mature": int(row.mature), "value": float(row[name]),
                         "degree": int(G.degree(int(row.node)))})
top5 = pd.DataFrame(top_rows)
top5.to_csv(OUT / "top5_metricas.csv", index=False)
print("\\nTop 5 por métrica:\\n", top5.to_string(index=False))

# 4. División estratificada 80/20, idéntica para ambos modelos.
train_nodes, test_nodes = train_test_split(
    nodes, test_size=0.2, random_state=42, stratify=y
)
node_to_idx = {int(n): i for i, n in enumerate(nodes)}
train_idx = np.array([node_to_idx[int(n)] for n in train_nodes])
test_idx = np.array([node_to_idx[int(n)] for n in test_nodes])

# Modelo A: fila de adyacencia restringida a columnas de usuarios training.
A = nx.to_scipy_sparse_array(G, nodelist=list(nodes), format="csr", dtype=np.uint8)
X_adj = np.asarray(A[:, train_idx].toarray(), dtype=np.uint8)

# Modelo B: distancias mínimas desde cada nodo a cada nodo training.
X_dist = np.full((len(nodes), len(train_nodes)), np.inf, dtype=np.float32)
for j, source in enumerate(train_nodes):
    lengths = nx.single_source_shortest_path_length(G, int(source))
    for node, distance in lengths.items():
        X_dist[node_to_idx[int(node)], j] = distance
finite_values = X_dist[np.isfinite(X_dist)]
max_finite = float(finite_values.max())
infinite_count = int(np.isinf(X_dist).sum())
imputation_value = max_finite + 1
X_dist[~np.isfinite(X_dist)] = imputation_value
print(f"Distancias infinitas: {infinite_count}; imputación explícita: {imputation_value}")

# 5. Random Forest comparable para ambas representaciones.
evaluation = {}
for model_name, X in [("Modelo A - Adyacencia", X_adj),
                      ("Modelo B - Distancias", X_dist)]:
    clf = RandomForestClassifier(n_estimators=300, random_state=42, n_jobs=-1)
    clf.fit(X[train_idx], y[train_idx])
    pred = clf.predict(X[test_idx])
    cm = confusion_matrix(y[test_idx], pred, labels=[0, 1])
    report = classification_report(
        y[test_idx], pred, labels=[0, 1],
        target_names=["mature=0", "mature=1"], output_dict=True, zero_division=0
    )
    evaluation[model_name] = {
        "accuracy": float(accuracy_score(y[test_idx], pred)),
        "f1_mature_1": float(f1_score(y[test_idx], pred, zero_division=0)),
        "confusion_matrix": cm.tolist(),
        "classification_report": report,
    }

rows = []
for name, result in evaluation.items():
    cm = result["confusion_matrix"]
    rows.append({
        "modelo": name, "accuracy": result["accuracy"],
        "f1_mature_1": result["f1_mature_1"],
        "TN": cm[0][0], "FP": cm[0][1], "FN": cm[1][0], "TP": cm[1][1],
    })
pd.DataFrame(rows).to_csv(OUT / "evaluacion_modelos.csv", index=False)
with open(OUT / "resultados.json", "w", encoding="utf-8") as f:
    json.dump({"stats": stats, "evaluation": evaluation,
               "infinite_distances": infinite_count,
               "distance_imputation_value": imputation_value},
              f, ensure_ascii=False, indent=2)

# Matrices de confusión
fig, axes = plt.subplots(1, 2, figsize=(10, 4))
for ax, (name, result) in zip(axes, evaluation.items()):
    cm = np.array(result["confusion_matrix"])
    ax.imshow(cm, cmap="Blues")
    ax.set_title(name)
    ax.set_xlabel("Predicción")
    ax.set_ylabel("Clase real")
    ax.set_xticks([0, 1], labels=["0", "1"])
    ax.set_yticks([0, 1], labels=["0", "1"])
    for (i, j), value in np.ndenumerate(cm):
        ax.text(j, i, str(value), ha="center", va="center")
fig.tight_layout()
fig.savefig(OUT / "matrices_confusion.png", dpi=180, bbox_inches="tight")
plt.close(fig)

print("\\nEvaluación:\\n", pd.DataFrame(rows).to_string(index=False))
print(f"Resultados guardados en: {OUT.resolve()}")
