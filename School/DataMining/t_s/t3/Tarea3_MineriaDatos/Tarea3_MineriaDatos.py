
# TAREA 3 - MINERÍA DE DATOS: PRUEBAS ESTADÍSTICAS
# Dataset: Customer Personality Analysis (Kaggle)
#
# El programa realiza los apartados 1, 2, 3, 4 y 5 de la tarea.
# Para los apartados 1-4 se reutiliza el mismo dataset, seleccionando
# las variables que corresponden al tipo de análisis solicitado.
#
# Fuente indicada por la tarea:
# https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis
#
# Si marketing_campaign.csv está en la misma carpeta, se usa ese archivo.
# Si no existe, se intenta descargar una copia pública del mismo dataset
# desde GitHub. Para una entrega formal, se recomienda descargar el CSV
# directamente de Kaggle y colocarlo junto a este script.

from pathlib import Path
import urllib.request
import warnings
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
from statsmodels.stats.multitest import multipletests

warnings.filterwarnings("ignore")

BASE = Path(__file__).resolve().parent
DATA_FILE = BASE / "marketing_campaign.csv"
OUT = BASE / "resultados_tarea3"
OUT.mkdir(exist_ok=True)

KAGGLE_URL = "https://www.kaggle.com/datasets/imakash3011/customer-personality-analysis"
MIRROR_URL = (
    "https://raw.githubusercontent.com/priyanshu-arya/"
    "Customer-Personality-Analysis/refs/heads/main/marketing_campaign.csv"
)

PRODUCTS = [
    "MntWines",
    "MntFruits",
    "MntMeatProducts",
    "MntFishProducts",
    "MntSweetProducts",
    "MntGoldProds",
]

def cargar_datos():
    if not DATA_FILE.exists():
        print("No se encontró marketing_campaign.csv.")
        print("Intentando descargar una copia pública del dataset...")
        try:
            urllib.request.urlretrieve(MIRROR_URL, DATA_FILE)
            print("Dataset descargado.")
        except Exception as e:
            raise RuntimeError(
                "\nNo se pudo descargar automáticamente el dataset.\n"
                "Descarga marketing_campaign.csv desde Kaggle y colócalo junto "
                "a este script.\n\n"
                f"Kaggle: {KAGGLE_URL}\n"
                f"Detalle técnico: {e}"
            )

    # Kaggle suele entregar el archivo separado por tabuladores.
    try:
        df = pd.read_csv(DATA_FILE, sep="\t")
        if len(df.columns) == 1:
            df = pd.read_csv(DATA_FILE)
    except Exception:
        df = pd.read_csv(DATA_FILE)

    # Normalizar nombres y tipos usados por el análisis.
    df.columns = [str(c).strip() for c in df.columns]
    if "Response" in df.columns:
        df["Response"] = pd.to_numeric(df["Response"], errors="coerce")
    for col in ["Income"] + PRODUCTS:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    required = ["Response", "Income", *PRODUCTS, "Education", "Marital_Status"]
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(
            "Faltan columnas requeridas en marketing_campaign.csv: "
            + ", ".join(missing)
        )

    return df


def guardar_figura(nombre):
    plt.tight_layout()
    plt.savefig(OUT / nombre, dpi=180, bbox_inches="tight")
    plt.show()
    plt.close()


def normalidad(x):
    x = pd.Series(x).dropna().astype(float)
    stat, p = stats.shapiro(x)
    return stat, p


def fuerza_correlacion(r):
    a = abs(r)
    if a < 0.3:
        return "débil"
    elif a <= 0.6:
        return "moderada"
    return "fuerte"


def cohens_d(a, b):
    a = np.asarray(pd.Series(a).dropna(), dtype=float)
    b = np.asarray(pd.Series(b).dropna(), dtype=float)
    na, nb = len(a), len(b)
    va, vb = np.var(a, ddof=1), np.var(b, ddof=1)
    pooled = np.sqrt(((na - 1) * va + (nb - 1) * vb) / (na + nb - 2))
    return (np.mean(a) - np.mean(b)) / pooled if pooled != 0 else np.nan


def pct(p):
    return f"{100*p:.4f}%"


def ptxt(p):
    if p < 0.0001:
        return "<0.0001"
    return f"{p:.6f}"


def main():
    df = cargar_datos()

    # ================================================================
    # INFORMACIÓN GENERAL
    # ================================================================
    info = []
    info.append("# Tarea 3 - Minería de datos\n")
    info.append("## Fuente y preparación\n")
    info.append(
        "Dataset: **Customer Personality Analysis**, indicado en la consigna "
        "como dataset de Kaggle. El archivo utilizado es `marketing_campaign.csv`.\n"
    )
    info.append(f"- Filas originales: **{df.shape[0]}**")
    info.append(f"- Columnas originales: **{df.shape[1]}**")
    info.append(f"- Valores faltantes por columna: {df.isna().sum().sum()} en total.\n")

    # ================================================================
    # 1) CONTINUA - CONTINUA
    # Income vs MntWines
    # ================================================================
    info.append("## 1. Salida continua - entrada continua\n")
    info.append(
        "Se analiza la relación entre `Income` (ingreso anual del hogar) y "
        "`MntWines` (gasto en vinos durante los últimos dos años).\n"
    )

    d1 = df[["Income", "MntWines"]].dropna()
    sh_income = normalidad(d1["Income"])
    sh_wines = normalidad(d1["MntWines"])

    info.append(f"- Filas utilizadas: **{len(d1)}**")
    info.append(f"- Variables numéricas: **{df.select_dtypes(include=np.number).shape[1]}**")
    info.append(f"- Variables categóricas: **{df.select_dtypes(exclude=np.number).shape[1]}**")
    info.append(
        "\n**Pregunta de investigación:** ¿Existe correlación entre el ingreso "
        "anual y el gasto en vinos?\n"
    )
    info.append("- H0: No existe correlación entre Income y MntWines.")
    info.append("- H1: Sí existe correlación entre Income y MntWines.\n")

    info.append("### Prueba de normalidad")
    info.append(
        f"- Income: Shapiro-Wilk W={sh_income[0]:.5f}, p={ptxt(sh_income[1])} "
        f"→ {'normal' if sh_income[1] >= .05 else 'no normal'}."
    )
    info.append(
        f"- MntWines: Shapiro-Wilk W={sh_wines[0]:.5f}, p={ptxt(sh_wines[1])} "
        f"→ {'normal' if sh_wines[1] >= .05 else 'no normal'}."
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(d1["Income"], bins=30)
    ax.set_title("Distribución de Income")
    ax.set_xlabel("Income")
    ax.set_ylabel("Frecuencia")
    guardar_figura("1_hist_income.png")

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.hist(d1["MntWines"], bins=30)
    ax.set_title("Distribución de MntWines")
    ax.set_xlabel("MntWines")
    ax.set_ylabel("Frecuencia")
    guardar_figura("1_hist_mntwines.png")

    fig = sm.qqplot(d1["Income"], line="45", fit=True)
    plt.title("QQ-Plot de Income")
    guardar_figura("1_qq_income.png")

    fig = sm.qqplot(d1["MntWines"], line="45", fit=True)
    plt.title("QQ-Plot de MntWines")
    guardar_figura("1_qq_mntwines.png")

    if sh_income[1] >= .05 and sh_wines[1] >= .05:
        corr_name = "Pearson"
        r, p = stats.pearsonr(d1["Income"], d1["MntWines"])
        symbol = "r"
    else:
        corr_name = "Spearman"
        r, p = stats.spearmanr(d1["Income"], d1["MntWines"])
        symbol = "ρ"

    info.append(f"\n### Prueba estadística: {corr_name}")
    info.append(
        f"Se utiliza {corr_name} porque "
        + ("ambas variables cumplen normalidad."
           if corr_name == "Pearson"
           else "al menos una de las variables no cumple normalidad.")
    )
    info.append(f"- {symbol} = **{r:.5f}**")
    info.append(f"- p-value = **{ptxt(p)}**")
    info.append(
        f"- Dirección: **{'positiva' if r > 0 else 'negativa' if r < 0 else 'nula'}**"
    )
    info.append(f"- Fuerza: **{fuerza_correlacion(r)}**")
    info.append(
        f"- Decisión: **{'se rechaza H0' if p < .05 else 'no se rechaza H0'}** "
        "con α=0.05."
    )
    info.append(
        f"- Interpretación del p-value: si H0 fuera cierta, la probabilidad de "
        f"observar un coeficiente como el obtenido sería aproximadamente {pct(p)}.\n"
    )

    # Regresión lineal para visualización, aunque la prueba principal sea Spearman.
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.scatter(d1["Income"], d1["MntWines"], alpha=.35, s=18)
    x = d1["Income"].to_numpy()
    y = d1["MntWines"].to_numpy()
    slope, intercept, *_ = stats.linregress(x, y)
    xs = np.linspace(x.min(), x.max(), 200)
    ax.plot(xs, intercept + slope * xs, linewidth=2)
    ax.set_title("Income vs MntWines")
    ax.set_xlabel("Income")
    ax.set_ylabel("MntWines")
    guardar_figura("1_dispersion_regresion.png")

    # ================================================================
    # 2) CONTINUA - CATEGÓRICA
    # MntWines según Response
    # ================================================================
    info.append("## 2. Salida continua - entrada categórica\n")
    d2 = df[["Response", "MntWines"]].dropna()
    g0 = d2.loc[d2["Response"] == 0, "MntWines"]
    g1 = d2.loc[d2["Response"] == 1, "MntWines"]

    n0, p0 = normalidad(g0)
    n1, p1 = normalidad(g1)
    lev_stat, lev_p = stats.levene(g0, g1, center="median")

    info.append(
        "Se compara el gasto en vinos entre clientes que no aceptaron "
        "(`Response=0`) y clientes que aceptaron (`Response=1`) la campaña.\n"
    )
    info.append("- H0: los grupos no presentan una diferencia estadísticamente significativa.")
    info.append("- H1: los grupos presentan una diferencia estadísticamente significativa.\n")
    info.append("### Normalidad y homogeneidad")
    info.append(
        f"- Response=0: Shapiro W={n0:.5f}, p={ptxt(p0)} "
        f"→ {'normal' if p0 >= .05 else 'no normal'}."
    )
    info.append(
        f"- Response=1: Shapiro W={n1:.5f}, p={ptxt(p1)} "
        f"→ {'normal' if p1 >= .05 else 'no normal'}."
    )
    info.append(
        f"- Levene: estadístico={lev_stat:.5f}, p={ptxt(lev_p)} "
        f"→ {'varianzas razonablemente homogéneas' if lev_p >= .05 else 'varianzas diferentes'}."
    )

    if p0 >= .05 and p1 >= .05 and lev_p >= .05:
        test2 = "t-test independiente"
        stat2, p2 = stats.ttest_ind(g0, g1, equal_var=True)
        stat_label = "t"
    else:
        test2 = "Mann-Whitney U"
        stat2, p2 = stats.mannwhitneyu(g0, g1, alternative="two-sided")
        stat_label = "U"

    info.append(f"\n### Prueba aplicada: {test2}")
    info.append(
        "Se seleccionó la prueba con base en normalidad y homogeneidad de varianzas, "
        "tal como solicita la consigna."
    )
    info.append(f"- {stat_label} = **{stat2:.5f}**")
    info.append(f"- p-value = **{ptxt(p2)}**")
    info.append(f"- Media Response=0: **{g0.mean():.3f}**")
    info.append(f"- Media Response=1: **{g1.mean():.3f}**")
    info.append(f"- Mediana Response=0: **{g0.median():.3f}**")
    info.append(f"- Mediana Response=1: **{g1.median():.3f}**")
    info.append(f"- Diferencia de medias (1 - 0): **{g1.mean()-g0.mean():.3f}**")
    info.append(f"- Cohen's d: **{cohens_d(g1, g0):.5f}**")
    info.append(
        f"- Decisión: **{'se rechaza H0' if p2 < .05 else 'no se rechaza H0'}** "
        "con α=0.05.\n"
    )

    fig, ax = plt.subplots(figsize=(7, 5))
    ax.boxplot([g0, g1], tick_labels=["Response=0", "Response=1"])
    ax.set_title("MntWines por respuesta a la campaña")
    ax.set_ylabel("MntWines")
    guardar_figura("2_boxplot_response_mntwines.png")

    # ================================================================
    # 3) CATEGÓRICA - CATEGÓRICA
    # Response vs Education
    # ================================================================
    info.append("## 3. Salida categórica - entrada categórica\n")
    d3 = df[["Response", "Education"]].dropna()
    tabla3 = pd.crosstab(d3["Education"], d3["Response"])

    chi3, p3, gl3, expected3 = stats.chi2_contingency(tabla3)
    exp_min3 = expected3.min()
    denom3 = tabla3.values.sum() * min(tabla3.shape[0]-1, tabla3.shape[1]-1)
    cramers_v3 = np.sqrt(chi3 / denom3) if denom3 > 0 else np.nan

    info.append(
        "Se estudia si existe asociación entre el nivel educativo y la respuesta "
        "a la campaña.\n"
    )
    info.append("- H0: Education y Response son independientes.")
    info.append("- H1: existe asociación entre Education y Response.\n")
    info.append("### Tabla de contingencia")
    info.append(tabla3.to_markdown())
    info.append("\n### Conteos esperados")
    exp_df3 = pd.DataFrame(expected3, index=tabla3.index, columns=tabla3.columns)
    info.append(exp_df3.round(2).to_markdown())
    info.append(
        f"\nEl menor conteo esperado es **{exp_min3:.3f}**, por lo que "
        + ("se puede usar Chi-cuadrado."
           if exp_min3 >= 5
           else "hay celdas menores a 5 y debe revisarse la alternativa exacta; "
                "al haber más de dos categorías, la prueba exacta de Fisher clásica "
                "2x2 no es aplicable directamente.")
    )
    info.append("\n### Chi-cuadrado de independencia")
    info.append(f"- χ² = **{chi3:.5f}**")
    info.append(f"- gl = **{gl3}**")
    info.append(f"- p-value = **{ptxt(p3)}**")
    info.append(f"- Cramer's V = **{cramers_v3:.5f}**")
    info.append(
        f"- Decisión: **{'se rechaza H0' if p3 < .05 else 'no se rechaza H0'}** "
        "con α=0.05."
    )

    tabla3.to_csv(OUT / "3_tabla_contingencia_education_response.csv")
    fig, ax = plt.subplots(figsize=(8, 5))
    im = ax.imshow(tabla3.values, aspect="auto")
    ax.set_xticks(range(len(tabla3.columns)))
    ax.set_xticklabels(tabla3.columns)
    ax.set_yticks(range(len(tabla3.index)))
    ax.set_yticklabels(tabla3.index)
    ax.set_xlabel("Response")
    ax.set_ylabel("Education")
    ax.set_title("Heatmap de frecuencias: Education vs Response")
    for i in range(tabla3.shape[0]):
        for j in range(tabla3.shape[1]):
            ax.text(j, i, tabla3.iloc[i, j], ha="center", va="center")
    guardar_figura("3_heatmap_education_response.png")

    # ================================================================
    # 4) CATEGÓRICA - CONTINUA
    # Response <- Income, regresión logística
    # ================================================================
    info.append("## 4. Salida categórica - entrada continua\n")
    d4 = df[["Response", "Income"]].dropna().copy()
    d4["Response"] = d4["Response"].astype(int)

    model4 = smf.logit("Response ~ Income", data=d4).fit(disp=False)
    beta0 = model4.params["Intercept"]
    beta1 = model4.params["Income"]
    p_beta1 = model4.pvalues["Income"]
    or1 = np.exp(beta1)
    or10k = np.exp(beta1 * 10000)

    info.append(
        "Se utiliza `Response` como variable categórica binaria dependiente e "
        "`Income` como variable continua independiente.\n"
    )
    info.append("- H0: Income no predice la ocurrencia de Response=1.")
    info.append("- H1: Income sí predice la ocurrencia de Response=1.\n")
    info.append("### Regresión logística")
    info.append(f"- β0 (intercepto) = **{beta0:.8f}**")
    info.append(f"- β1 (Income) = **{beta1:.8f}**")
    info.append(f"- p-value de β1 = **{ptxt(p_beta1)}**")
    info.append(f"- OR por cada unidad monetaria = **{or1:.8f}**")
    info.append(f"- OR por cada $10,000 de Income = **{or10k:.5f}**")
    info.append(
        f"- Decisión: **{'se rechaza H0' if p_beta1 < .05 else 'no se rechaza H0'}** "
        "con α=0.05."
    )
    info.append(
        "La interpretación del OR se expresa también por $10,000 porque un incremento "
        "de una sola unidad monetaria produce un OR muy cercano a 1 y es poco práctico "
        "para interpretar.\n"
    )

    # Curva logística y banda aproximada usando get_prediction.
    xgrid = np.linspace(d4["Income"].quantile(.01), d4["Income"].quantile(.99), 250)
    pred_df = pd.DataFrame({"Income": xgrid})
    pred = model4.get_prediction(pred_df).summary_frame(alpha=.05)

    fig, ax = plt.subplots(figsize=(8, 5))
    jitter = np.random.default_rng(123).normal(0, .025, len(d4))
    ax.scatter(d4["Income"], d4["Response"] + jitter, alpha=.15, s=12)
    ax.plot(xgrid, pred.iloc[:, 0], linewidth=2)
    # statsmodels cambia los nombres de las columnas según la versión.
    ax.fill_between(
        xgrid, pred.iloc[:, 1], pred.iloc[:, 2], alpha=.2
    )
    ax.set_ylim(-.08, 1.08)
    ax.set_xlabel("Income")
    ax.set_ylabel("Probabilidad estimada de Response=1")
    ax.set_title("Regresión logística: Income → Response")
    guardar_figura("4_curva_logistica_income_response.png")

    # ================================================================
    # 5) EVALUACIÓN INTEGRAL
    # ================================================================
    info.append("## 5. Evaluación estadística integral de una campaña de marketing\n")
    info.append(
        "Se realizan las 14 pruebas mínimas solicitadas: 6 comparaciones de gasto, "
        "6 correlaciones con Income y 2 asociaciones categóricas.\n"
    )

    tests = []

    # ---------------- A1-A6 ----------------
    info.append("### 5.1. Comparación de gasto según Response\n")
    for i, var in enumerate(PRODUCTS, 1):
        tmp = df[["Response", var]].dropna()
        a = tmp.loc[tmp["Response"] == 0, var]
        b = tmp.loc[tmp["Response"] == 1, var]

        pa_norm = normalidad(a)[1]
        pb_norm = normalidad(b)[1]
        lev = stats.levene(a, b, center="median")

        if pa_norm >= .05 and pb_norm >= .05 and lev.pvalue >= .05:
            stat, pv = stats.ttest_ind(a, b, equal_var=True)
            method = "t-test independiente"
            statistic_name = "t"
        else:
            stat, pv = stats.mannwhitneyu(a, b, alternative="two-sided")
            method = "Mann-Whitney U"
            statistic_name = "U"

        effect = cohens_d(b, a)
        tests.append({
            "Prueba": f"A{i}",
            "Variable": var,
            "Método": method,
            "Estadístico": stat,
            "p_original": pv,
            "Efecto": effect,
            "Media_R0": a.mean(),
            "Media_R1": b.mean(),
            "Mediana_R0": a.median(),
            "Mediana_R1": b.median(),
            "Detalle": statistic_name,
        })

    A = pd.DataFrame(tests)

    # ---------------- B1-B6 ----------------
    info.append("### 5.2. Correlación entre Income y gasto\n")
    for i, var in enumerate(PRODUCTS, 1):
        tmp = df[["Income", var]].dropna()

        p_income = normalidad(tmp["Income"])[1]
        p_var = normalidad(tmp[var])[1]

        # Regla de la consigna: Spearman si no hay normalidad
        if p_income >= .05 and p_var >= .05:
            coef, pv = stats.pearsonr(tmp["Income"], tmp[var])
            method = "Pearson"
            coef_name = "r"
        else:
            coef, pv = stats.spearmanr(tmp["Income"], tmp[var])
            method = "Spearman"
            coef_name = "rho"

        tests.append({
            "Prueba": f"B{i}",
            "Variable": f"Income vs {var}",
            "Método": method,
            "Estadístico": coef,
            "p_original": pv,
            "Efecto": np.nan,
            "Media_R0": np.nan,
            "Media_R1": np.nan,
            "Mediana_R0": np.nan,
            "Mediana_R1": np.nan,
            "Detalle": coef_name,
        })

    # ---------------- C1-C2 ----------------
    info.append("### 5.3. Asociación de Response con Education y Marital_Status\n")
    for i, cat in enumerate(["Education", "Marital_Status"], 1):
        tmp = df[["Response", cat]].dropna()
        tab = pd.crosstab(tmp[cat], tmp["Response"])
        chi, pv, gl, exp = stats.chi2_contingency(tab)
        denom = tab.values.sum() * min(tab.shape[0] - 1, tab.shape[1] - 1)
        v = np.sqrt(chi / denom) if denom > 0 else np.nan
        tests.append({
            "Prueba": f"C{i}",
            "Variable": f"Response vs {cat}",
            "Método": "Chi-cuadrado de independencia",
            "Estadístico": chi,
            "p_original": pv,
            "Efecto": v,
            "Media_R0": np.nan,
            "Media_R1": np.nan,
            "Mediana_R0": np.nan,
            "Mediana_R1": np.nan,
            "Detalle": f"gl={gl}; Cramer's V={v:.5f}",
        })
        tab.to_csv(OUT / f"5_{cat}_response_contingencia.csv")

    ALL = pd.DataFrame(tests)

    # Correcciones múltiples
    bonf_rej, bonf_p, _, _ = multipletests(ALL["p_original"], alpha=.05, method="bonferroni")
    fdr_rej, fdr_p, _, _ = multipletests(ALL["p_original"], alpha=.05, method="fdr_bh")

    ALL["p_Bonferroni"] = bonf_p
    ALL["p_FDR_BH"] = fdr_p
    ALL["Significativa_original"] = ALL["p_original"] < .05
    ALL["Significativa_Bonferroni"] = bonf_rej
    ALL["Significativa_FDR"] = fdr_rej

    alpha_adj = .05 / len(ALL)

    ALL.to_csv(OUT / "5_tabla_resumen_14_pruebas.csv", index=False)

    # Resumen de las 14 pruebas
    info.append("\n### 5.4. Corrección por comparaciones múltiples")
    info.append(f"- Número de pruebas: **k = {len(ALL)}**")
    info.append(f"- α ajustado por Bonferroni = **0.05/{len(ALL)} = {alpha_adj:.8f}**")
    info.append(
        "Se aplicaron Bonferroni y Benjamini-Hochberg (FDR) a los mismos 14 p-values."
    )

    table_cols = [
        "Prueba", "Variable", "Método", "p_original",
        "p_Bonferroni", "p_FDR_BH",
        "Significativa_original",
        "Significativa_Bonferroni",
        "Significativa_FDR"
    ]
    info.append("\n" + ALL[table_cols].to_markdown(index=False))

    # Hallazgos textuales
    info.append("\n### 5.5. Integración de hallazgos\n")

    A_res = ALL[ALL["Prueba"].str.startswith("A")]
    B_res = ALL[ALL["Prueba"].str.startswith("B")]
    C_res = ALL[ALL["Prueba"].str.startswith("C")]

    sig_A = A_res.loc[A_res["p_original"] < .05, "Variable"].tolist()
    sig_B = B_res.loc[B_res["p_original"] < .05, "Variable"].tolist()
    sig_C = C_res.loc[C_res["p_original"] < .05, "Variable"].tolist()

    info.append(
        "- Diferencias significativas antes de corregir en A: "
        + (", ".join(sig_A) if sig_A else "ninguna") + "."
    )
    info.append(
        "- Correlaciones significativas antes de corregir en B: "
        + (", ".join(sig_B) if sig_B else "ninguna") + "."
    )
    info.append(
        "- Asociaciones significativas antes de corregir en C: "
        + (", ".join(sig_C) if sig_C else "ninguna") + "."
    )

    sig_bonf = ALL.loc[ALL["Significativa_Bonferroni"], "Prueba"].tolist()
    sig_fdr = ALL.loc[ALL["Significativa_FDR"], "Prueba"].tolist()

    info.append(
        "- Pruebas que permanecen significativas con Bonferroni: "
        + (", ".join(sig_bonf) if sig_bonf else "ninguna") + "."
    )
    info.append(
        "- Pruebas que permanecen significativas con FDR/BH: "
        + (", ".join(sig_fdr) if sig_fdr else "ninguna") + "."
    )

    info.append(
        "\n**Recomendación final para la empresa:** utilizar únicamente las relaciones "
        "que permanezcan respaldadas por el nivel de significancia después de considerar "
        "la corrección por comparaciones múltiples. Las diferencias o asociaciones que "
        "desaparezcan después del ajuste deben considerarse evidencia insuficiente para "
        "tomar una conclusión estadística fuerte."
    )

    # Guardar reporte y resumen
    report_path = OUT / "reporte_tarea3.md"
    report_path.write_text("\n\n".join(info), encoding="utf-8")

    # Guardar un resumen sencillo para copiar a Word
    resumen = [
        "TAREA 3 - MINERÍA DE DATOS",
        "Customer Personality Analysis",
        "",
        f"Filas: {df.shape[0]}",
        f"Columnas: {df.shape[1]}",
        "",
        "Los resultados completos se encuentran en reporte_tarea3.md",
        "y en las tablas CSV dentro de la carpeta resultados_tarea3.",
    ]
    (OUT / "LEEME.txt").write_text("\n".join(resumen), encoding="utf-8")

    print("=" * 70)
    print("TAREA 3 TERMINADA")
    print("=" * 70)
    print(f"Reporte: {report_path}")
    print(f"Resultados: {OUT}")
    print("\nResumen de las 14 pruebas:")
    print(
        ALL[["Prueba", "Variable", "Método", "p_original",
             "p_Bonferroni", "p_FDR_BH",
             "Significativa_Bonferroni", "Significativa_FDR"]]
        .to_string(index=False)
    )


if __name__ == "__main__":
    main()
