from __future__ import annotations

from typing import Dict, Iterable, List


class DiGraph:
    def __init__(self) -> None:
        self._adj: Dict[str, Dict[str, dict]] = {}

    def clear(self) -> None:
        self._adj = {}

    def add_edge(self, u: str, v: str, **attrs) -> None:
        self._adj.setdefault(u, {})[v] = attrs
        self._adj.setdefault(v, {})

    def to_undirected(self):
        undirected = DiGraph()
        for u, neighbors in self._adj.items():
            for v, attrs in neighbors.items():
                undirected.add_edge(u, v, **attrs)
                undirected.add_edge(v, u, **attrs)
        return undirected

    def number_of_nodes(self) -> int:
        return len(self._adj)

    def number_of_edges(self) -> int:
        return sum(len(neighbors) for neighbors in self._adj.values())

    def nodes(self) -> List[str]:
        return list(self._adj.keys())

    def neighbors(self, node: str) -> Iterable[str]:
        return self._adj.get(node, {}).keys()

    @property
    def adj(self) -> Dict[str, Dict[str, dict]]:
        return self._adj
