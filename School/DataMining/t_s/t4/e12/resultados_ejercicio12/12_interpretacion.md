# Ejercicio 12 — Interpretación de resultados

## 12.1
El grafo tiene 7624 nodos, 27806 aristas, densidad 0.000957 y 1 componentes conexas. Se dividieron las etiquetas en 6099 nodos training y 1525 testing. Se permite utilizar el grafo completo (evaluación transductiva), pero no las etiquetas testing para construir las características ni entrenar.

## Limitación de datos
Los CSV suministrados SOLO incluyen aristas e identificador/clase, no atributos de perfil de usuario. Para las representaciones «atributos propios» se utilizó como proxy estructural el grado del nodo, y para «promedio de vecinos» el grado medio de los vecinos. Por ello no es una comparación entre atributos individuales auténticos y topología independiente: todas las representaciones proceden del grafo. «Propios + métricas» duplica la información del grado deliberadamente para seguir la lista de cinco variantes; no se presenta como una nueva fuente de datos.

## 12.2
Las seis coloraciones usan exactamente la misma subred y posiciones. La clase se usa SOLO para colorear, nunca para crear características predictoras. Betweenness se aproxima con 128 nodos fuente para reducir el coste computacional.

## 12.3
La matriz de adyacencia tiene 7624 columnas; una por posible vecino. Los nodos sin vecinos reciben promedio vecinal 0. Las métricas son grado, betweenness, closeness aproximada, eigenvector y coeficiente de clustering.

## 12.4
Mejor F1 macro: Adyacencia (0.6523); peor F1 macro: Atributos propios (proxy grado) (0.0401). La adyacencia representa identidades de vecinos y puede generalizar peor a nodos completamente nuevos; este experimento es transductivo. Las centralidades resumen patrones estructurales de forma compacta. Ninguna característica utiliza las etiquetas de testing. La interpretación de importancias se limita a la importancia de impureza del Random Forest, que puede favorecer variables continuas o de alta cardinalidad.
