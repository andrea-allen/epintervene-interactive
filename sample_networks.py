import networkx as nx
from epintervene.simobjects import network

def erdos_renyi(n, p):
    nb = network.NetworkBuilder
    graph = nx.generators.erdos_renyi_graph(n, p)
    adjlist = nb.create_adjacency_list(graph)
    return adjlist

def balanced_tree():
    nb = network.NetworkBuilder
    graph = nx.generators.balanced_tree(2, 5)
    adjlist = nb.create_adjacency_list(graph)
    return adjlist

def small_world(n, k, p):
    nb = network.NetworkBuilder
    graph = nx.generators.watts_strogatz_graph(n, k, p)
    adjlist = nb.create_adjacency_list(graph)
    return adjlist
