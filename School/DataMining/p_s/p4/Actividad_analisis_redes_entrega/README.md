# Entrega — Actividad de análisis de redes

## Archivos principales
- `Reporte_actividad_redes.pdf`: reporte en español con metodología, gráficas, top 5 e interpretación de resultados.
- `Actividad_analisis_redes.ipynb`: notebook reproducible.
- `actividad_redes.py`: script Python equivalente.
- `musae_PTBR_edges.csv` y `musae_PTBR_target.csv`: datos originales utilizados.
- `centralidades.csv`: las cinco métricas para los 1,912 nodos.
- `top5_metricas.csv`: cinco nodos con mayor valor por métrica.
- `evaluacion_modelos.csv` y `resultados.json`: resultados de los modelos.
- Archivos PNG: visualizaciones y matrices de confusión.

## Cómo ejecutar
Instala las dependencias:
`pip install pandas numpy networkx matplotlib scikit-learn scipy`

Abre el notebook y ejecuta las celdas en orden, o ejecuta `python actividad_redes.py` desde la carpeta que contiene los CSV. El script guarda sus salidas en una subcarpeta `resultados`.

## Resultado principal
- Modelo A (adyacencia): accuracy 0.6736; F1 para `mature=1` 0.4444.
- Modelo B (distancias): accuracy 0.6762; F1 para `mature=1` 0.3542.
Se prioriza el F1 de la clase positiva para comparar la detección de usuarios `mature=1`.
