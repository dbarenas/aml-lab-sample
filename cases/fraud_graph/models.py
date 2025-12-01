from __future__ import annotations

from typing import Iterable, List

import networkx as nx
from pydantic import BaseModel, Field, validator


class TransactionEdge(BaseModel):
    """Arista que representa una transferencia dirigida entre cuentas."""

    origin: str = Field(..., description="Cuenta origen")
    destination: str = Field(..., description="Cuenta destino")
    amount: float = Field(..., ge=0, description="Monto de la transferencia")

    def __post_init__(self) -> None:
        if not self.origin.strip() or not self.destination.strip():
            raise ValueError("Las cuentas no pueden estar vacías")
        if self.amount < 0:
            raise ValueError("El monto debe ser no negativo")


class GraphAnalyticsService:
    """Encapsula la lógica de NetworkX para mantener el principio de responsabilidad única."""

    def __init__(self) -> None:
        self._graph = nx.DiGraph()

    def build_graph(self, edges: Iterable[TransactionEdge]) -> nx.DiGraph:
        self._graph.clear()
        for edge in edges:
            self._graph.add_edge(
                edge.origin,
                edge.destination,
                amount=edge.amount,
            )
        return self._graph

    def strongly_connected_components(self) -> List[list[str]]:
        return [list(component) for component in nx.strongly_connected_components(self._graph)]

    def communities(self) -> List[set[str]]:
        undirected_graph = self._graph.to_undirected()
        return list(nx.community.greedy_modularity_communities(undirected_graph))

    def betweenness_centrality(self) -> dict[str, float]:
        return nx.betweenness_centrality(self._graph)

    @property
    def graph(self) -> nx.DiGraph:
        return self._graph
