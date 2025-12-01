from __future__ import annotations

from datetime import date
from typing import List

from .detector import StructuringDetector
from .models import FeatureEngineeringService, TransactionRecord


def run_demo() -> List[tuple[str, float]]:
    """Ejecución conceptual: genera features, entrena y devuelve scores por cuenta."""

    transactions = [
        TransactionRecord(account_id="A", amount=9500, operation_date=date(2024, 1, 10)),
        TransactionRecord(account_id="A", amount=9700, operation_date=date(2024, 1, 11)),
        TransactionRecord(account_id="A", amount=9800, operation_date=date(2024, 1, 11)),
        TransactionRecord(account_id="B", amount=2000, operation_date=date(2024, 1, 10)),
        TransactionRecord(account_id="B", amount=2100, operation_date=date(2024, 1, 12)),
        TransactionRecord(account_id="C", amount=50000, operation_date=date(2024, 1, 10)),
    ]

    feature_service = FeatureEngineeringService(min_transactions=2)
    vectors = feature_service.build_feature_vectors(transactions)

    detector = StructuringDetector(contamination=0.25, random_state=7)
    detector.fit(vectors)
    return detector.score_accounts(vectors)


if __name__ == "__main__":
    scores = run_demo()
    for account_id, score in scores:
        print(f"Cuenta: {account_id} | Puntuación de anomalía: {score:.4f}")
