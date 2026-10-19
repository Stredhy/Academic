"""Ejercicio 2: clasificación de fraudes con cinco estrategias de balanceo.

Requisitos: pip install pandas numpy matplotlib scikit-learn imbalanced-learn
Colocar este archivo junto a creditCard.csv y ejecutar:
    python ejercicio2_fraude.py

Las figuras se guardan en PNG y se muestran en ventanas (cerrar para continuar).
El entrenamiento puede tardar varios minutos por el tamaño del dataset.
"""

from pathlib import Path
import time

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from imblearn.ensemble import BalancedRandomForestClassifier
from imblearn.over_sampling import RandomOverSampler, SMOTE
from imblearn.under_sampling import RandomUnderSampler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    ConfusionMatrixDisplay,
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_recall_curve,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ========================== CONFIGURACIÓN ==========================
BASE = Path(__file__).resolve().parent
DATASET = BASE / "creditCard.csv"
OUTPUT = BASE / "resultados_ejercicio2"
OUTPUT.mkdir(parents=True, exist_ok=True)
SEED = 42
MOSTRAR_GRAFICAS = True  # Cambiar a False para generar PNG sin abrir ventanas.
N_ESTIMATORS = 100  # Igual en los cinco modelos.
N_JOBS = -1
# Para visualizar sin saturar memoria, se muestrean puntos SOLO para dibujar.
MAX_PUNTOS_PCA_POR_CLASE = 3000


def guardar_figura(nombre):
    """Guarda y, opcionalmente, muestra la figura actual."""
    plt.tight_layout()
    plt.savefig(OUTPUT / nombre, dpi=180, bbox_inches="tight")
    if MOSTRAR_GRAFICAS:
        plt.show(block=True)
    plt.close()


def tabla_clases(y, etiqueta):
    """Devuelve conteos y porcentajes de ambas clases."""
    conteos = pd.Series(y).value_counts().reindex([0, 1], fill_value=0)
    return pd.DataFrame({
        "Conjunto": etiqueta,
        "Class": [0, 1],
        "Conteo": conteos.to_numpy(),
        "Porcentaje": (conteos.to_numpy() / len(y) * 100).round(5),
    })


def dibujar_pca(X, y, pca, titulo, nombre):
    """Proyecta con el MISMO PCA; limita únicamente puntos dibujados."""
    rng = np.random.default_rng(SEED)
    y = np.asarray(y)
    fig, ax = plt.subplots(figsize=(9, 6))
    for clase, color, etiqueta in [(0, "#3577b8", "Legítima"), (1, "#e07b39", "Fraude")]:
        indices = np.flatnonzero(y == clase)
        if len(indices) > MAX_PUNTOS_PCA_POR_CLASE:
            indices = rng.choice(indices, MAX_PUNTOS_PCA_POR_CLASE, replace=False)
        puntos = pca.transform(X[indices])
        ax.scatter(puntos[:, 0], puntos[:, 1], s=7, alpha=0.4,
                   color=color, label=f"{etiqueta}: {np.sum(y == clase):,} (mostradas: {len(indices):,})")
    ax.set(title=titulo, xlabel="Componente principal 1 (PC1)", ylabel="Componente principal 2 (PC2)")
    ax.legend(fontsize=9)
    ax.grid(alpha=0.2)
    guardar_figura(nombre)


def crear_bosque(balanceado=False):
    """Los hiperparámetros comparables son idénticos en las estrategias."""
    parametros = dict(n_estimators=N_ESTIMATORS, random_state=SEED,
                      n_jobs=N_JOBS, max_depth=None, min_samples_leaf=1)
    if balanceado:
        return BalancedRandomForestClassifier(**parametros, sampling_strategy="all",
                                              replacement=True, bootstrap=False)
    return RandomForestClassifier(**parametros)


def main():
    inicio = time.perf_counter()
    if not DATASET.is_file():
        raise FileNotFoundError(f"No se encontró {DATASET}. Pon el CSV junto al .py")

    # ==================== 2.1 DATOS Y MODELO BASE ====================
    df = pd.read_csv(DATASET)
    if "Class" not in df.columns:
        raise ValueError("El dataset debe contener la columna 'Class'.")
    df["Class"] = pd.to_numeric(df["Class"], errors="raise").astype(int)
    if not set(df["Class"].unique()).issubset({0, 1}):
        raise ValueError("Class debe contener únicamente 0 y 1.")
    X = df.drop(columns="Class")
    y = df["Class"]
    if not all(pd.api.types.is_numeric_dtype(dtype) for dtype in X.dtypes):
        raise ValueError("Todas las variables predictoras deben ser numéricas.")

    # 2.1.1 Conteos y porcentajes.
    distribucion = tabla_clases(y, "Original")
    distribucion.to_csv(OUTPUT / "2_1_1_distribucion.csv", index=False)
    print("\n2.1.1 Distribución original:\n", distribucion.to_string(index=False))

    # 2.1.2 Distribución con escala logarítmica.
    fig, ax = plt.subplots(figsize=(7, 5))
    barras = ax.bar(["Class 0: legítima", "Class 1: fraude"],
                    distribucion["Conteo"], color=["#3577b8", "#e07b39"])
    ax.set_yscale("log")
    ax.set(title="2.1.2 Distribución de transacciones (escala logarítmica)",
           xlabel="Clase", ylabel="Número de transacciones (log)")
    for barra, fila in zip(barras, distribucion.itertuples()):
        ax.text(barra.get_x() + barra.get_width() / 2, barra.get_height() * 1.12,
                f"{fila.Conteo:,} ({fila.Porcentaje:.4f}%)", ha="center", fontsize=9)
    ax.set_ylim(1, distribucion["Conteo"].max() * 2)
    guardar_figura("2_1_2_distribucion.png")

    # 2.1.3 y 2.1.4: split estratificado y conteos.
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=SEED
    )
    particiones = pd.concat([
        tabla_clases(y_train, "Training (80%)"),
        tabla_clases(y_test, "Testing (20%)"),
    ], ignore_index=True)
    particiones.to_csv(OUTPUT / "2_1_4_particiones.csv", index=False)
    print("\n2.1.4 Particiones:\n", particiones.to_string(index=False))

    # 2.1.5–2.1.9: imputación y escalado SOLO con training.
    faltantes = X_train.isna().sum().rename("NaN_training").reset_index()
    faltantes.columns = ["Variable", "NaN_training"]
    faltantes.to_csv(OUTPUT / "2_1_5_faltantes_training.csv", index=False)
    print("\n2.1.5 Total NaN en training:", int(faltantes["NaN_training"].sum()))
    imputador = SimpleImputer(strategy="median")
    escalador = StandardScaler()
    X_train_imputado = imputador.fit_transform(X_train)
    X_train_escalado = escalador.fit_transform(X_train_imputado)
    X_test_escalado = escalador.transform(imputador.transform(X_test))
    # No se realiza CV: ambos transformadores se ajustan una sola vez en training.
    # El conjunto de testing permanece intacto en etiquetas y distribución.

    # ======================== 2.2 BALANCEO ==========================
    remuestreadores = {
        "Sin balanceo": None,
        "RandomUnderSampler": RandomUnderSampler(random_state=SEED),
        "RandomOverSampler": RandomOverSampler(random_state=SEED),
        "SMOTE": SMOTE(random_state=SEED),
        "BalancedRandomForest": None,
    }
    conjuntos = {}
    balanceo_filas = []
    conteo_original = np.bincount(y_train.to_numpy(), minlength=2)
    for nombre, sampler in remuestreadores.items():
        if sampler is None:
            X_bal, y_bal = X_train_escalado, y_train.to_numpy()
        else:
            X_bal, y_bal = sampler.fit_resample(X_train_escalado, y_train)
        conjuntos[nombre] = (X_bal, np.asarray(y_bal))
        conteo_nuevo = np.bincount(np.asarray(y_bal), minlength=2)
        balanceo_filas.append({
            "Estrategia": nombre,
            "Antes_Class_0": int(conteo_original[0]),
            "Antes_Class_1": int(conteo_original[1]),
            "Despues_Class_0": int(conteo_nuevo[0]),
            "Despues_Class_1": int(conteo_nuevo[1]),
            "Observacion": "Balanceo interno por árbol" if nombre == "BalancedRandomForest"
                           else "Conjunto usado para entrenar",
        })
    balanceo = pd.DataFrame(balanceo_filas)
    balanceo.to_csv(OUTPUT / "2_2_8_conteos_balanceo.csv", index=False)
    print("\n2.2.8 Conteos por estrategia:\n", balanceo.to_string(index=False))

    # ===================== 2.3 VISUALIZACIÓN ========================
    # PCA se ajusta UNA SOLA VEZ con training original imputado y escalado.
    pca = PCA(n_components=2, random_state=SEED)
    pca.fit(X_train_escalado)
    varianza = pd.DataFrame({
        "Componente": ["PC1", "PC2"],
        "Varianza_explicada": pca.explained_variance_ratio_,
    })
    varianza.to_csv(OUTPUT / "2_3_1_varianza_pca.csv", index=False)
    for nombre in ["Sin balanceo", "RandomUnderSampler", "RandomOverSampler", "SMOTE"]:
        X_bal, y_bal = conjuntos[nombre]
        dibujar_pca(X_bal, y_bal, pca,
                    f"2.3 PCA — {nombre} (PCA ajustado solo en training original)",
                    f"2_3_pca_{nombre}.png")

    # ======================= 2.4 EVALUACIÓN =========================
    resultados = []
    curvas = {}
    for nombre, (X_bal, y_bal) in conjuntos.items():
        print(f"\nEntrenando: {nombre} ...", flush=True)
        modelo = crear_bosque(balanceado=(nombre == "BalancedRandomForest"))
        modelo.fit(X_bal, y_bal)
        pred = modelo.predict(X_test_escalado)
        prob = modelo.predict_proba(X_test_escalado)[:, 1]
        tn, fp, fn, tp = confusion_matrix(y_test, pred, labels=[0, 1]).ravel()
        resultados.append({
            "Estrategia": nombre,
            "Accuracy": accuracy_score(y_test, pred),
            "Precision": precision_score(y_test, pred, zero_division=0),
            "Recall": recall_score(y_test, pred, zero_division=0),
            "F1": f1_score(y_test, pred, zero_division=0),
            "ROC_AUC": roc_auc_score(y_test, prob),
            "PR_AUC": average_precision_score(y_test, prob),
            "FP": int(fp), "FN": int(fn), "TP": int(tp), "TN": int(tn),
        })
        curvas[nombre] = {
            "roc": roc_curve(y_test, prob),
            "pr": precision_recall_curve(y_test, prob),
        }
        # 2.4.4 Matriz de confusión con etiquetas y conteos.
        fig, ax = plt.subplots(figsize=(6, 5))
        ConfusionMatrixDisplay.from_predictions(
            y_test, pred, labels=[0, 1], display_labels=["Legítima", "Fraude"],
            cmap="Blues", values_format="d", ax=ax, colorbar=False
        )
        ax.set(title=f"2.4.4 Matriz de confusión — {nombre}",
               xlabel="Clase predicha", ylabel="Clase real")
        guardar_figura(f"2_4_4_confusion_{nombre}.png")
        # Se guarda el progreso después de CADA modelo.
        pd.DataFrame(resultados).to_csv(OUTPUT / "2_4_2_comparacion.csv", index=False)

    tabla = pd.DataFrame(resultados)
    print("\n2.4.2 Comparación en testing original:\n", tabla.round(5).to_string(index=False))

    # 2.4.3 Curvas ROC y Precision–Recall.
    fig, ax = plt.subplots(figsize=(8, 6))
    for fila in resultados:
        nombre = fila["Estrategia"]
        fpr, tpr, _ = curvas[nombre]["roc"]
        ax.plot(fpr, tpr, label=f"{nombre} (AUC={fila['ROC_AUC']:.4f})")
    ax.plot([0, 1], [0, 1], "k--", alpha=0.5, label="Aleatorio")
    ax.set(title="2.4.3 Curvas ROC — cinco estrategias", xlabel="Tasa de falsos positivos (FPR)",
           ylabel="Tasa de verdaderos positivos (Recall)")
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    guardar_figura("2_4_3_roc.png")

    fig, ax = plt.subplots(figsize=(8, 6))
    for fila in resultados:
        nombre = fila["Estrategia"]
        precision, recall, _ = curvas[nombre]["pr"]
        ax.plot(recall, precision, label=f"{nombre} (AP={fila['PR_AUC']:.4f})")
    ax.axhline(y_test.mean(), color="black", linestyle="--", alpha=0.5,
               label=f"Prevalencia de fraude ({y_test.mean():.4%})")
    ax.set(title="2.4.3 Curvas Precision–Recall — cinco estrategias",
           xlabel="Recall", ylabel="Precision", xlim=(0, 1), ylim=(0, 1.02))
    ax.legend(fontsize=8)
    ax.grid(alpha=0.2)
    guardar_figura("2_4_3_precision_recall.png")

    # 2.4.5 Mayor recall y falsos positivos (desempate: menos FP).
    ganador = tabla.sort_values(["Recall", "FP"], ascending=[False, True]).iloc[0]
    resumen = (
        f"Mayor recall: {ganador['Estrategia']} ({ganador['Recall']:.4%}).\n"
        f"Falsos positivos: {int(ganador['FP'])}.\n"
        f"Falsos negativos: {int(ganador['FN'])}.\n"
        f"Precision: {ganador['Precision']:.4%}.\n"
        "Interpretación: mayor recall implica detectar más fraudes, pero debe "
        "contrastarse con las alertas falsas (FP) y precision.\n"
        "PR-AUC se reporta como Average Precision (AP), especialmente informativa "
        "cuando la clase positiva es muy minoritaria.\n"
        "Las figuras PCA muestran una muestra para legibilidad, con los conteos "
        "reales indicados en las leyendas.\n"
    )
    (OUTPUT / "2_4_5_interpretacion.txt").write_text(resumen, encoding="utf-8")
    print("\n2.4.5\n" + resumen)
    print(f"Archivos generados en: {OUTPUT}")
    print(f"Tiempo total: {(time.perf_counter() - inicio) / 60:.1f} minutos")


if __name__ == "__main__":
    main()
