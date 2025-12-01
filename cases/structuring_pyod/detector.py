from __future__ import annotations

from typing import Iterable, List

import numpy as np
from pyod.models.iforest import IForest

from .models import AccountFeatureVector


class StructuringDetector:
    """Capa de aplicación SOLID que orquesta el uso de PyOD para detección de pitufeo."""

    def __init__(self, contamination: float = 0.05, random_state: int | None = None) -> None:
        self._model = IForest(contamination=contamination, random_state=random_state)
        self._fitted = False

    def fit(self, features: Iterable[AccountFeatureVector]) -> None:
        """Entrena IsolationForest a partir de las features calculadas."""

        matrix = np.vstack([vector.to_numpy() for vector in features])
        self._model.fit(matrix)
        self._fitted = True

    def score_accounts(
        self, features: Iterable[AccountFeatureVector]
    ) -> List[tuple[str, float]]:
        """Devuelve la puntuación de anomalía por cuenta."""

        if not self._fitted:
            raise RuntimeError("El modelo debe entrenarse antes de puntuar cuentas")

        vectors = list(features)
        matrix = np.vstack([vector.to_numpy() for vector in vectors])
        scores = self._model.decision_function(matrix)
        return list(zip([v.account_id for v in vectors], scores))

    @property
    def model(self) -> IForest:
        return self._model
