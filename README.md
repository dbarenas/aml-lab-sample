# AML Lab Sample

Este laboratorio muestra cómo aplicar **IA para Detección de Lavado de Dinero (AML)** combinando PyOD (detección de anomalías) y NetworkX (análisis de grafos), con énfasis en principios SOLID, validación de datos con Pydantic, carpetas separadas por caso y pruebas automatizadas.

## 1. 🔍 Detección AML con PyOD (IA: Machine Learning No Supervisado)

**Caso de Uso:** Detección de Structuring (Pitufeo).

| Etapa de IA | Tarea con PyOD | Explicación del Rol de la IA |
| :--- | :--- | :--- |
| **1. Feature Engineering** | Crear métricas de comportamiento por cuenta. | Las features como número de transacciones por día, monto promedio y desviación estándar permiten que la IA distinga patrones fraccionados (pitufo) de comportamientos normales. |
| **2. Entrenamiento del Modelo** | Aplicar **Isolation Forest** (IForest) de PyOD. | Isolation Forest aísla observaciones raras en menos divisiones, resultando efectivo para anomalías sin necesidad de etiquetar datos. |
| **3. Detección y Puntuación** | Calcular la **puntuación de anomalía** (`decision_scores_`). | La puntuación refleja qué tan aislada es una cuenta; cuanto mayor sea, más sospechosa y más rápido activa una alerta. |

**Ejemplo Conceptual de PyOD (IForest)**

```python
import numpy as np
from pyod.models.iforest import IForest

# X contiene las features numéricas (una fila por cuenta)
model = IForest(contamination=0.05, random_state=7)
model.fit(X)
anomaly_scores = model.decision_function(X)
```

## 2. 🕸️ Grafos AML con NetworkX (IA: Análisis de Redes y Grafos)

**Caso de Uso:** Descubrimiento de Anillos de Fraude y "Nodos Mula".

| Etapa de IA | Tarea con NetworkX | Explicación del Rol de la IA |
| :--- | :--- | :--- |
| **1. Construcción del Grafo** | Mapear cuentas como **Nodos** y transacciones como **Aristas**. | Representar la red permite aplicar teoría de grafos para descubrir relaciones encubiertas entre cuentas. |
| **2. Detección de Patrones Estructurales** | Encontrar **Componentes Fuertemente Conectados** y **Detección de Comunidades**. | Estos algoritmos identifican automáticamente anillos cíclicos o grupos densamente conectados que suelen operar coordinadamente. |
| **3. Identificación de Influencia** | Calcular la **Centralidad de Intermediación** (*Betweenness Centrality*). | Localiza nodos puente o cuentas mula que controlan el flujo en la red criminal. |

**Ejemplo Conceptual de NetworkX**

```python
import networkx as nx

G = nx.DiGraph()
G.add_edge("A", "B")
G.add_edge("B", "C")
G.add_edge("C", "A")

scc = list(nx.strongly_connected_components(G))
```

## Estructura del proyecto

```
cases/
  fraud_graph/          # Análisis de grafos con NetworkX
    demo.py
    models.py
  structuring_pyod/     # Detección de pitufeo con PyOD
    demo.py
    detector.py
    models.py
tests/
  test_networkx_graph.py
  test_pyod_detector.py
```

## Cómo ejecutar el demo

```bash
python -m cases.structuring_pyod.demo
python -m cases.fraud_graph.demo
```

## Cómo ejecutar pruebas

```bash
python -m pytest
```

## Conclusión

La combinación de PyOD para puntuar anomalías y NetworkX para revelar la estructura de relaciones proporciona una visión integral y moderna en la detección de lavado de dinero.
