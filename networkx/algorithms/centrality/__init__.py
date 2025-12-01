from __future__ import annotations

from collections import deque

from ...classes import DiGraph


def betweenness_centrality(graph: DiGraph) -> dict[str, float]:
    centrality = {node: 0.0 for node in graph.nodes()}
    for s in graph.nodes():
        stack: list[str] = []
        predecessors: dict[str, list[str]] = {w: [] for w in graph.nodes()}
        sigma = dict.fromkeys(graph.nodes(), 0.0)
        sigma[s] = 1.0
        distance = dict.fromkeys(graph.nodes(), -1)
        distance[s] = 0
        queue = deque([s])
        while queue:
            v = queue.popleft()
            stack.append(v)
            for w in graph.neighbors(v):
                if distance[w] < 0:
                    queue.append(w)
                    distance[w] = distance[v] + 1
                if distance[w] == distance[v] + 1:
                    sigma[w] += sigma[v]
                    predecessors[w].append(v)
        delta = dict.fromkeys(graph.nodes(), 0.0)
        while stack:
            w = stack.pop()
            for v in predecessors[w]:
                delta_v = (sigma[v] / sigma[w]) * (1 + delta[w]) if sigma[w] else 0
                delta[v] += delta_v
            if w != s:
                centrality[w] += delta[w]
    scale = 1 / ((len(graph.nodes()) - 1) * (len(graph.nodes()) - 2)) if len(graph.nodes()) > 2 else 1.0
    for node in centrality:
        centrality[node] *= scale
    return centrality
