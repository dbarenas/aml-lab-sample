from __future__ import annotations

from .models import GraphAnalyticsService, TransactionEdge


def run_demo() -> dict[str, object]:
    edges = [
        TransactionEdge(origin="A", destination="B", amount=3000),
        TransactionEdge(origin="B", destination="C", amount=3200),
        TransactionEdge(origin="C", destination="A", amount=3100),
        TransactionEdge(origin="C", destination="D", amount=1500),
        TransactionEdge(origin="D", destination="E", amount=1600),
        TransactionEdge(origin="E", destination="C", amount=1700),
    ]

    analytics = GraphAnalyticsService()
    analytics.build_graph(edges)
    return {
        "scc": analytics.strongly_connected_components(),
        "communities": [sorted(list(c)) for c in analytics.communities()],
        "betweenness": analytics.betweenness_centrality(),
    }


if __name__ == "__main__":
    results = run_demo()
    print("Componentes fuertemente conectados:", results["scc"])
    print("Comunidades detectadas:", results["communities"])
    print("Centralidad de intermediación:", results["betweenness"])
