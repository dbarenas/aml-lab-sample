from __future__ import annotations

from datetime import date
from typing import Iterable, List

import numpy as np
from pydantic import BaseModel, Field, validator


class TransactionRecord(BaseModel):
    """Domain object que describe una transacción sencilla para análisis AML."""

    account_id: str = Field(..., description="Identificador único de la cuenta")
    amount: float = Field(..., ge=0, description="Monto de la transacción en USD")
    operation_date: date = Field(..., description="Fecha de la operación")

    def __post_init__(self) -> None:
        if not self.account_id.strip():
            raise ValueError("account_id no puede estar vacío")
        if self.amount < 0:
            raise ValueError("amount no puede ser negativo")


class AccountFeatureVector(BaseModel):
    """Vector de características por cuenta, listo para alimentar a PyOD."""

    account_id: str
    tx_count: int = Field(..., ge=1, description="Número de transacciones observadas")
    avg_amount: float = Field(..., ge=0, description="Promedio de montos")
    std_amount: float = Field(..., ge=0, description="Desviación estándar del monto")
    daily_density: float = Field(
        ..., ge=0, description="Transacciones promedio por día activo"
    )

    def __post_init__(self) -> None:
        if not self.account_id.strip():
            raise ValueError("account_id no puede estar vacío")
        if self.tx_count < 1:
            raise ValueError("tx_count debe ser al menos 1")
        for field in (self.avg_amount, self.std_amount, self.daily_density):
            if field < 0:
                raise ValueError("Las métricas no pueden ser negativas")

    def to_numpy(self) -> np.ndarray:
        """Convierte las features a un arreglo para PyOD."""

        return np.array([self.tx_count, self.avg_amount, self.std_amount, self.daily_density])


class FeatureEngineeringService:
    """Aplica principios SOLID al separar claramente la responsabilidad de cálculo de features."""

    def __init__(self, min_transactions: int = 1) -> None:
        self._min_transactions = min_transactions

    def build_feature_vectors(
        self, transactions: Iterable[TransactionRecord]
    ) -> List[AccountFeatureVector]:
        grouped: dict[str, list[TransactionRecord]] = {}
        for tx in transactions:
            grouped.setdefault(tx.account_id, []).append(tx)

        feature_vectors: List[AccountFeatureVector] = []
        for account_id, account_txs in grouped.items():
            if len(account_txs) < self._min_transactions:
                continue

            amounts = [tx.amount for tx in account_txs]
            std_amount = float(np.std(amounts))
            avg_amount = float(np.mean(amounts))
            days_active = len({tx.operation_date for tx in account_txs})
            daily_density = len(account_txs) / days_active

            feature_vectors.append(
                AccountFeatureVector(
                    account_id=account_id,
                    tx_count=len(account_txs),
                    avg_amount=avg_amount,
                    std_amount=std_amount,
                    daily_density=daily_density,
                )
            )
        return feature_vectors
