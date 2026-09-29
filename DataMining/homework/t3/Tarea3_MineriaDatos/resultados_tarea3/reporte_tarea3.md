# Tarea 3 - Minería de datos


## Fuente y preparación


Dataset: **Customer Personality Analysis**, indicado en la consigna como dataset de Kaggle. El archivo utilizado es `marketing_campaign.csv`.


- Filas originales: **2240**

- Columnas originales: **29**

- Valores faltantes por columna: 24 en total.


## 1. Salida continua - entrada continua


Se analiza la relación entre `Income` (ingreso anual del hogar) y `MntWines` (gasto en vinos durante los últimos dos años).


- Filas utilizadas: **2216**

- Variables numéricas: **26**

- Variables categóricas: **3**


**Pregunta de investigación:** ¿Existe correlación entre el ingreso anual y el gasto en vinos?


- H0: No existe correlación entre Income y MntWines.

- H1: Sí existe correlación entre Income y MntWines.


### Prueba de normalidad

- Income: Shapiro-Wilk W=0.77705, p=<0.0001 → no normal.

- MntWines: Shapiro-Wilk W=0.83881, p=<0.0001 → no normal.


### Prueba estadística: Spearman

Se utiliza Spearman porque al menos una de las variables no cumple normalidad.

- ρ = **0.83006**

- p-value = **<0.0001**

- Dirección: **positiva**

- Fuerza: **fuerte**

- Decisión: **se rechaza H0** con α=0.05.

- Interpretación del p-value: si H0 fuera cierta, la probabilidad de observar un coeficiente como el obtenido sería aproximadamente 0.0000%.


## 2. Salida continua - entrada categórica


Se compara el gasto en vinos entre clientes que no aceptaron (`Response=0`) y clientes que aceptaron (`Response=1`) la campaña.


- H0: los grupos no presentan una diferencia estadísticamente significativa.

- H1: los grupos presentan una diferencia estadísticamente significativa.


### Normalidad y homogeneidad

- Response=0: Shapiro W=0.82905, p=<0.0001 → no normal.

- Response=1: Shapiro W=0.91224, p=<0.0001 → no normal.

- Levene: estadístico=100.14470, p=<0.0001 → varianzas diferentes.


### Prueba aplicada: Mann-Whitney U

Se seleccionó la prueba con base en normalidad y homogeneidad de varianzas, tal como solicita la consigna.

- U = **215610.00000**

- p-value = **<0.0001**

- Media Response=0: **269.104**

- Media Response=1: **502.704**

- Mediana Response=0: **152.000**

- Mediana Response=1: **448.000**

- Diferencia de medias (1 - 0): **233.599**

- Cohen's d: **0.71608**

- Decisión: **se rechaza H0** con α=0.05.


## 3. Salida categórica - entrada categórica


Se estudia si existe asociación entre el nivel educativo y la respuesta a la campaña.


- H0: Education y Response son independientes.

- H1: existe asociación entre Education y Response.


### Tabla de contingencia

| Education   |   0 |   1 |
|:------------|----:|----:|
| 2n Cycle    | 181 |  22 |
| Basic       |  52 |   2 |
| Graduation  | 975 | 152 |
| Master      | 313 |  57 |
| PhD         | 385 | 101 |


### Conteos esperados

| Education   |      0 |      1 |
|:------------|-------:|-------:|
| 2n Cycle    | 172.73 |  30.27 |
| Basic       |  45.95 |   8.05 |
| Graduation  | 958.96 | 168.04 |
| Master      | 314.83 |  55.17 |
| PhD         | 413.53 |  72.47 |


El menor conteo esperado es **8.052**, por lo que se puede usar Chi-cuadrado.


### Chi-cuadrado de independencia

- χ² = **23.07610**

- gl = **4**

- p-value = **0.000122**

- Cramer's V = **0.10150**

- Decisión: **se rechaza H0** con α=0.05.

## 4. Salida categórica - entrada continua


Se utiliza `Response` como variable categórica binaria dependiente e `Income` como variable continua independiente.


- H0: Income no predice la ocurrencia de Response=1.

- H1: Income sí predice la ocurrencia de Response=1.


### Regresión logística

- β0 (intercepto) = **-2.60555348**

- β1 (Income) = **0.00001596**

- p-value de β1 = **<0.0001**

- OR por cada unidad monetaria = **1.00001596**

- OR por cada $10,000 de Income = **1.17299**

- Decisión: **se rechaza H0** con α=0.05.

La interpretación del OR se expresa también por $10,000 porque un incremento de una sola unidad monetaria produce un OR muy cercano a 1 y es poco práctico para interpretar.


## 5. Evaluación estadística integral de una campaña de marketing


Se realizan las 14 pruebas mínimas solicitadas: 6 comparaciones de gasto, 6 correlaciones con Income y 2 asociaciones categóricas.


### 5.1. Comparación de gasto según Response


### 5.2. Correlación entre Income y gasto


### 5.3. Asociación de Response con Education y Marital_Status



### 5.4. Corrección por comparaciones múltiples

- Número de pruebas: **k = 14**

- α ajustado por Bonferroni = **0.05/14 = 0.00357143**

Se aplicaron Bonferroni y Benjamini-Hochberg (FDR) a los mismos 14 p-values.


| Prueba   | Variable                   | Método                        |   p_original |   p_Bonferroni |     p_FDR_BH | Significativa_original   | Significativa_Bonferroni   | Significativa_FDR   |
|:---------|:---------------------------|:------------------------------|-------------:|---------------:|-------------:|:-------------------------|:---------------------------|:--------------------|
| A1       | MntWines                   | Mann-Whitney U                | 4.57817e-21  |   6.40943e-20  | 8.01179e-21  | True                     | True                       | True                |
| A2       | MntFruits                  | Mann-Whitney U                | 1.83067e-12  |   2.56294e-11  | 2.56294e-12  | True                     | True                       | True                |
| A3       | MntMeatProducts            | Mann-Whitney U                | 4.51982e-26  |   6.32775e-25  | 9.03965e-26  | True                     | True                       | True                |
| A4       | MntFishProducts            | Mann-Whitney U                | 4.72252e-08  |   6.61153e-07  | 5.08579e-08  | True                     | True                       | True                |
| A5       | MntSweetProducts           | Mann-Whitney U                | 1.03249e-10  |   1.44548e-09  | 1.31408e-10  | True                     | True                       | True                |
| A6       | MntGoldProds               | Mann-Whitney U                | 4.13761e-18  |   5.79265e-17  | 6.43628e-18  | True                     | True                       | True                |
| B1       | Income vs MntWines         | Spearman                      | 0            |   0            | 0            | True                     | True                       | True                |
| B2       | Income vs MntFruits        | Spearman                      | 2.02535e-201 |   2.83548e-200 | 9.45161e-201 | True                     | True                       | True                |
| B3       | Income vs MntMeatProducts  | Spearman                      | 0            |   0            | 0            | True                     | True                       | True                |
| B4       | Income vs MntFishProducts  | Spearman                      | 3.16284e-197 |   4.42797e-196 | 1.10699e-196 | True                     | True                       | True                |
| B5       | Income vs MntSweetProducts | Spearman                      | 8.68342e-189 |   1.21568e-187 | 2.43136e-188 | True                     | True                       | True                |
| B6       | Income vs MntGoldProds     | Spearman                      | 4.23349e-144 |   5.92688e-143 | 9.87813e-144 | True                     | True                       | True                |
| C1       | Response vs Education      | Chi-cuadrado de independencia | 0.00012227   |   0.00171178   | 0.00012227   | True                     | True                       | True                |
| C2       | Response vs Marital_Status | Chi-cuadrado de independencia | 2.10675e-09  |   2.94945e-08  | 2.45787e-09  | True                     | True                       | True                |


### 5.5. Integración de hallazgos


- Diferencias significativas antes de corregir en A: MntWines, MntFruits, MntMeatProducts, MntFishProducts, MntSweetProducts, MntGoldProds.

- Correlaciones significativas antes de corregir en B: Income vs MntWines, Income vs MntFruits, Income vs MntMeatProducts, Income vs MntFishProducts, Income vs MntSweetProducts, Income vs MntGoldProds.

- Asociaciones significativas antes de corregir en C: Response vs Education, Response vs Marital_Status.

- Pruebas que permanecen significativas con Bonferroni: A1, A2, A3, A4, A5, A6, B1, B2, B3, B4, B5, B6, C1, C2.

- Pruebas que permanecen significativas con FDR/BH: A1, A2, A3, A4, A5, A6, B1, B2, B3, B4, B5, B6, C1, C2.


**Recomendación final para la empresa:** utilizar únicamente las relaciones que permanezcan respaldadas por el nivel de significancia después de considerar la corrección por comparaciones múltiples. Las diferencias o asociaciones que desaparezcan después del ajuste deben considerarse evidencia insuficiente para tomar una conclusión estadística fuerte.