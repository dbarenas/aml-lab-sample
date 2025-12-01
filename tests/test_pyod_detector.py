from datetime import date

import numpy as np

from cases.structuring_pyod.demo import run_demo
from cases.structuring_pyod.detector import StructuringDetector
from cases.structuring_pyod.models import FeatureEngineeringService, TransactionRecord


def test_feature_engineering_builds_vectors():
    transactions = [
        TransactionRecord(account_id="X", amount=1000, operation_date=date(2024, 1, 1)),
        TransactionRecord(account_id="X", amount=1500, operation_date=date(2024, 1, 2)),
        TransactionRecord(account_id="Y", amount=5000, operation_date=date(2024, 1, 1)),
        TransactionRecord(account_id="Y", amount=5200, operation_date=date(2024, 1, 1)),
    ]

    vectors = FeatureEngineeringService(min_transactions=2).build_feature_vectors(transactions)
    assert len(vectors) == 2
    assert {v.account_id for v in vectors} == {"X", "Y"}
    for vector in vectors:
        assert vector.to_numpy().shape == (4,)


def test_detector_flags_outlier_with_high_anomaly_score():
    transactions = [
        TransactionRecord(account_id="A", amount=9500, operation_date=date(2024, 1, 10)),
        TransactionRecord(account_id="A", amount=9700, operation_date=date(2024, 1, 11)),
        TransactionRecord(account_id="B", amount=2000, operation_date=date(2024, 1, 10)),
        TransactionRecord(account_id="B", amount=2100, operation_date=date(2024, 1, 12)),
        TransactionRecord(account_id="C", amount=50000, operation_date=date(2024, 1, 10)),
        TransactionRecord(account_id="C", amount=52000, operation_date=date(2024, 1, 11)),
    ]

    feature_service = FeatureEngineeringService(min_transactions=2)
    vectors = feature_service.build_feature_vectors(transactions)

    detector = StructuringDetector(contamination=0.2, random_state=7)
    detector.fit(vectors)
    scored_accounts = detector.score_accounts(vectors)

    scores = {account: score for account, score in scored_accounts}
    lowest_risk = max(scores, key=scores.get)
    highest_risk = min(scores, key=scores.get)

    assert lowest_risk != highest_risk
    assert highest_risk == "C"
    assert np.isfinite(list(scores.values())).all()


def test_demo_runs_and_returns_scores():
    scores = run_demo()
    assert scores
    for account_id, score in scores:
        assert isinstance(account_id, str)
        assert isinstance(score, float)
