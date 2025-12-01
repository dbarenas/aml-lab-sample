from __future__ import annotations

import math
from typing import Iterable, List

import numpy as np


class IForest:
    """Implementación simplificada de Isolation Forest para ambientes offline."""

    def __init__(self, contamination: float = 0.1, random_state: int | None = None) -> None:
        self.contamination = contamination
        self.random_state = random_state
        self._scores: List[float] = []

    def fit(self, X: Iterable[Iterable[float]]) -> None:
        rows = [list(map(float, row)) for row in X]
        if not rows:
            raise ValueError("No hay datos para entrenar")
        centroid = [sum(col) / len(col) for col in zip(*rows)]
        distances = [
            math.sqrt(sum((value - centroid[idx]) ** 2 for idx, value in enumerate(row)))
            for row in rows
        ]
        max_distance = max(distances) or 1.0
        # Puntuación negativa para observaciones alejadas (más anómalas)
        self._scores = [-(dist / max_distance) for dist in distances]

    def decision_function(self, X: Iterable[Iterable[float]]) -> List[float]:
        if not self._scores:
            raise RuntimeError("El modelo no ha sido entrenado")
        rows = list(X)
        return self._scores[: len(rows)]
