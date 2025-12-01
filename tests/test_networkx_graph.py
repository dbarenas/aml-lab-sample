from cases.fraud_graph.demo import run_demo
from cases.fraud_graph.models import GraphAnalyticsService, TransactionEdge


def test_build_graph_and_components():
    edges = [
        TransactionEdge(origin="A", destination="B", amount=1000),
        TransactionEdge(origin="B", destination="A", amount=1100),
        TransactionEdge(origin="B", destination="C", amount=1200),
    ]
    analytics = GraphAnalyticsService()
    graph = analytics.build_graph(edges)

    assert graph.number_of_nodes() == 3
    assert graph.number_of_edges() == 3

    components = analytics.strongly_connected_components()
    assert any(set(comp) == {"A", "B"} for comp in components)

    centrality = analytics.betweenness_centrality()
    assert centrality.get("B", 0) >= centrality.get("A", 0)


def test_demo_returns_expected_keys():
    results = run_demo()
    assert set(results.keys()) == {"scc", "communities", "betweenness"}
    assert results["scc"]
    assert results["communities"]
    assert results["betweenness"]
