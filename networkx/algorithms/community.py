from __future__ import annotations

from typing import Iterable, List, Set

from ..classes import DiGraph


def greedy_modularity_communities(graph: DiGraph) -> List[Set[str]]:
    # Algoritmo muy simplificado: cada componente conexo no dirigido es una comunidad
    visited: set[str] = set()
    communities: list[set[str]] = []
    undirected_adj = graph.to_undirected().adj

    for node in undirected_adj:
        if node in visited:
            continue
        stack = [node]
        community: set[str] = set()
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            visited.add(current)
            community.add(current)
            stack.extend(undirected_adj[current].keys())
        communities.append(community)
    return communities
